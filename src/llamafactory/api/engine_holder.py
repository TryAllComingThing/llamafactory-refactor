# Copyright 2025 the LlamaFactory team.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

r"""Engine holder: singleton that manages training subprocesses and chat model lifecycle for the API."""

import asyncio
import json
import os
from collections.abc import AsyncGenerator
from copy import deepcopy
from enum import StrEnum
from subprocess import PIPE, Popen
from typing import Any

from transformers.utils import is_torch_npu_available

from ..chat import ChatModel
from ..extras.constants import LLAMABOARD_CONFIG, MULTIMODAL_SUPPORTED_MODELS, PEFT_METHODS, RUNNING_LOG, TRAINER_LOG, TRAINING_STAGES
from ..extras.misc import torch_gc
from ..webui.common import (
    DEFAULT_CACHE_DIR,
    abort_process,
    calculate_pixels,
    gen_cmd,
    get_save_dir,
    load_config,
    save_args,
    save_cmd,
)


class EngineState(StrEnum):
    IDLE = "idle"
    TRAINING = "training"
    EVALUATING = "evaluating"
    MODEL_LOADED = "model_loaded"


def _read_trainer_log(output_path: str) -> list[dict[str, Any]]:
    r"""Read trainer_log.jsonl and return parsed lines."""
    trainer_log_path = os.path.join(output_path, TRAINER_LOG)
    if not os.path.isfile(trainer_log_path):
        return []
    records: list[dict[str, Any]] = []
    with open(trainer_log_path, encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line:
                records.append(json.loads(line))
    return records


def _read_running_log(output_path: str) -> str:
    r"""Read running_log.txt and return the last portion."""
    running_log_path = os.path.join(output_path, RUNNING_LOG)
    if not os.path.isfile(running_log_path):
        return ""
    with open(running_log_path, encoding="utf-8") as f:
        content = f.read()[-20000:]
    return "```\n" + content + "\n```\n"


class ApiRunner:
    r"""Manages training/evaluation subprocesses for the API (no Gradio dependencies)."""

    def __init__(self) -> None:
        self.trainer: Popen | None = None
        self.do_train: bool = True
        self.aborted: bool = False
        self.running: bool = False
        self.current_run_id: str | None = None
        self._output_path: str | None = None
        # Store active WebSocket connections for progress push
        self._ws_queues: list[asyncio.Queue] = []

    def register_ws_queue(self, queue: asyncio.Queue) -> None:
        self._ws_queues.append(queue)

    def unregister_ws_queue(self, queue: asyncio.Queue) -> None:
        if queue in self._ws_queues:
            self._ws_queues.remove(queue)

    async def _broadcast(self, msg: dict[str, Any]) -> None:
        for queue in self._ws_queues:
            await queue.put(msg)

    def set_abort(self) -> None:
        self.aborted = True
        if self.trainer is None:
            return
        try:
            abort_process(self.trainer.pid)
        except Exception:
            pass

    @staticmethod
    def build_args(params: dict[str, Any], do_train: bool) -> dict[str, Any]:
        r"""Build training/eval args from a flat parameter dict (same keys as webui component IDs)."""
        def _g(key, default=None):
            v = params.get(key)
            return default if v is None or v == "" else v

        if do_train:
            args = dict(
                stage=TRAINING_STAGES.get(_g("training_stage"), "sft"),
                do_train=True,
                model_name_or_path=_g("model_path"),
                cache_dir=_g("cache_dir") or load_config().get("cache_dir"),
                preprocessing_num_workers=16,
                finetuning_type=_g("finetuning_type"),
                template=_g("template"),
                rope_scaling=_g("rope_scaling") if _g("rope_scaling") and _g("rope_scaling") != "none" else None,
                flash_attn="fa2" if _g("booster") == "flashattn2" else "auto",
                use_unsloth=(_g("booster") == "unsloth"),
                enable_liger_kernel=(_g("booster") == "liger_kernel"),
                dataset_dir=_g("dataset_dir"),
                dataset=",".join(_g("dataset", [])),
                cutoff_len=_g("cutoff_len"),
                learning_rate=float(_g("learning_rate", 5e-5)),
                num_train_epochs=float(_g("num_train_epochs", 3.0)),
                max_samples=int(_g("max_samples", 0)),
                per_device_train_batch_size=_g("batch_size", 2),
                gradient_accumulation_steps=_g("gradient_accumulation_steps", 4),
                lr_scheduler_type=_g("lr_scheduler_type", "cosine"),
                max_grad_norm=float(_g("max_grad_norm", 1.0)),
                logging_steps=_g("logging_steps", 5),
                save_steps=_g("save_steps", 100),
                warmup_steps=_g("warmup_steps", 0),
                neftune_noise_alpha=_g("neftune_alpha") or None,
                packing=_g("packing") or _g("neat_packing"),
                neat_packing=_g("neat_packing"),
                train_on_prompt=_g("train_on_prompt"),
                mask_history=_g("mask_history"),
                resize_vocab=_g("resize_vocab"),
                use_llama_pro=_g("use_llama_pro"),
                enable_thinking=_g("enable_thinking"),
                report_to=_g("report_to", "none"),
                use_galore=_g("use_galore"),
                use_apollo=_g("use_apollo"),
                use_badam=_g("use_badam"),
                use_swanlab=_g("use_swanlab"),
                output_dir=get_save_dir(
                    _g("model_name", "unknown"),
                    _g("finetuning_type", "full"),
                    _g("output_dir", "train_default"),
                ),
                fp16=(_g("compute_type") == "fp16"),
                bf16=(_g("compute_type") == "bf16"),
                pure_bf16=(_g("compute_type") == "pure_bf16"),
                plot_loss=True,
                trust_remote_code=True,
                ddp_timeout=180000000,
                include_num_input_tokens_seen=True,
            )

            # Extra args override
            extra_args = _g("extra_args")
            if extra_args:
                if isinstance(extra_args, str):
                    args.update(json.loads(extra_args))
                elif isinstance(extra_args, dict):
                    args.update(extra_args)

            # Checkpoints
            checkpoint_path = _g("checkpoint_path")
            finetuning_type = _g("finetuning_type")
            model_name = _g("model_name", "unknown")
            if checkpoint_path:
                if finetuning_type in PEFT_METHODS:
                    if isinstance(checkpoint_path, list):
                        args["adapter_name_or_path"] = ",".join(
                            [get_save_dir(model_name, finetuning_type, cp) for cp in checkpoint_path]
                        )
                    else:
                        args["adapter_name_or_path"] = get_save_dir(model_name, finetuning_type, checkpoint_path)
                else:
                    if isinstance(checkpoint_path, list):
                        args["model_name_or_path"] = get_save_dir(model_name, finetuning_type, checkpoint_path[0])
                    else:
                        args["model_name_or_path"] = get_save_dir(model_name, finetuning_type, checkpoint_path)

            # Quantization
            if _g("quantization_bit") and _g("quantization_bit") != "none":
                args["quantization_bit"] = int(_g("quantization_bit"))
                args["quantization_method"] = _g("quantization_method")
                args["double_quantization"] = not is_torch_npu_available()

            # Freeze config
            if args["finetuning_type"] == "freeze":
                args["freeze_trainable_layers"] = _g("freeze_trainable_layers")
                args["freeze_trainable_modules"] = _g("freeze_trainable_modules")
                args["freeze_extra_modules"] = _g("freeze_extra_modules") or None

            # LoRA config
            if args["finetuning_type"] == "lora":
                args["lora_rank"] = _g("lora_rank", 8)
                args["lora_alpha"] = _g("lora_alpha", 16)
                args["lora_dropout"] = _g("lora_dropout", 0.0)
                args["loraplus_lr_ratio"] = _g("loraplus_lr_ratio") or None
                args["create_new_adapter"] = _g("create_new_adapter", False)
                args["use_rslora"] = _g("use_rslora", False)
                args["use_dora"] = _g("use_dora", False)
                args["pissa_init"] = _g("use_pissa", False)
                args["pissa_convert"] = _g("use_pissa", False)
                args["lora_target"] = _g("lora_target") or "all"
                args["additional_target"] = _g("additional_target") or None

                if args["use_llama_pro"]:
                    args["freeze_trainable_layers"] = _g("freeze_trainable_layers")

            # RLHF config
            if args["stage"] == "ppo":
                reward_model = _g("reward_model")
                if finetuning_type in PEFT_METHODS:
                    if isinstance(reward_model, list):
                        args["reward_model"] = ",".join(
                            [get_save_dir(model_name, finetuning_type, rm) for rm in reward_model]
                        )
                    else:
                        args["reward_model"] = get_save_dir(model_name, finetuning_type, reward_model)
                else:
                    args["reward_model"] = get_save_dir(model_name, finetuning_type, reward_model)

                args["reward_model_type"] = "lora" if finetuning_type == "lora" else "full"
                args["ppo_score_norm"] = _g("ppo_score_norm", True)
                args["ppo_whiten_rewards"] = _g("ppo_whiten_rewards", True)
            elif args["stage"] in ["dpo", "kto"]:
                args["pref_beta"] = _g("pref_beta", 0.1)
                args["pref_ftx"] = _g("pref_ftx", 0.0)
                args["pref_loss"] = _g("pref_loss", "sigmoid")

            # Multimodal config
            if _g("model_name", "") in MULTIMODAL_SUPPORTED_MODELS:
                args["freeze_vision_tower"] = _g("freeze_vision_tower", True)
                args["freeze_multi_modal_projector"] = _g("freeze_multi_modal_projector", True)
                args["freeze_language_model"] = _g("freeze_language_model", False)
                args["image_max_pixels"] = calculate_pixels(_g("image_max_pixels", "768*768"))
                args["image_min_pixels"] = calculate_pixels(_g("image_min_pixels", "32*32"))
                args["video_max_pixels"] = calculate_pixels(_g("video_max_pixels", "256*256"))
                args["video_min_pixels"] = calculate_pixels(_g("video_min_pixels", "16*16"))

            # Galore config
            if args["use_galore"]:
                args["galore_rank"] = _g("galore_rank", 128)
                args["galore_update_interval"] = _g("galore_update_interval", 200)
                args["galore_scale"] = _g("galore_scale", 0.25)
                args["galore_target"] = _g("galore_target", "all")

            # Apollo config
            if args["use_apollo"]:
                args["apollo_rank"] = _g("apollo_rank", 128)
                args["apollo_update_interval"] = _g("apollo_update_interval", 200)
                args["apollo_scale"] = _g("apollo_scale", 0.25)
                args["apollo_target"] = _g("apollo_target", "all")

            # BAdam config
            if args["use_badam"]:
                args["badam_mode"] = _g("badam_mode", "layer")
                args["badam_switch_mode"] = _g("badam_switch_mode", "fixed")
                args["badam_switch_interval"] = _g("badam_switch_interval", 50)
                args["badam_update_ratio"] = _g("badam_update_ratio", 0.05)

            # SwanLab config
            if _g("use_swanlab"):
                args["swanlab_project"] = _g("swanlab_project", "llamafactory")
                args["swanlab_run_name"] = _g("swanlab_run_name", "")
                args["swanlab_workspace"] = _g("swanlab_workspace", "")
                args["swanlab_api_key"] = _g("swanlab_api_key", "")
                args["swanlab_mode"] = _g("swanlab_mode", "cloud")

            # Eval during training
            if _g("val_size", 0) > 1e-6 and args["stage"] != "ppo":
                args["val_size"] = _g("val_size")
                args["eval_strategy"] = "steps"
                args["eval_steps"] = args["save_steps"]
                args["per_device_eval_batch_size"] = args["per_device_train_batch_size"]

            # DeepSpeed config
            if _g("ds_stage") and _g("ds_stage") != "none":
                ds_stage = _g("ds_stage")
                ds_offload = "offload_" if _g("ds_offload") else ""
                args["deepspeed"] = os.path.join(DEFAULT_CACHE_DIR, f"ds_z{ds_stage}_{ds_offload}config.json")

        else:
            # Evaluation args
            args = dict(
                stage="sft",
                model_name_or_path=_g("model_path"),
                cache_dir=_g("cache_dir") or load_config().get("cache_dir"),
                preprocessing_num_workers=16,
                finetuning_type=_g("finetuning_type"),
                quantization_method=_g("quantization_method"),
                template=_g("template"),
                rope_scaling=_g("rope_scaling") if _g("rope_scaling") and _g("rope_scaling") != "none" else None,
                flash_attn="fa2" if _g("booster") == "flashattn2" else "auto",
                use_unsloth=(_g("booster") == "unsloth"),
                dataset_dir=_g("dataset_dir"),
                eval_dataset=",".join(_g("dataset", [])),
                cutoff_len=_g("cutoff_len", 1024),
                max_samples=int(_g("max_samples", 0)),
                per_device_eval_batch_size=_g("batch_size", 2),
                predict_with_generate=True,
                report_to="none",
                max_new_tokens=_g("max_new_tokens", 512),
                top_p=_g("top_p", 0.9),
                temperature=_g("temperature", 0.6),
                output_dir=get_save_dir(
                    _g("model_name", "unknown"),
                    _g("finetuning_type", "full"),
                    _g("output_dir", "eval_default"),
                ),
                trust_remote_code=True,
                ddp_timeout=180000000,
            )

            if _g("predict"):
                args["do_predict"] = True
            else:
                args["do_eval"] = True

            # Checkpoints
            checkpoint_path = _g("checkpoint_path")
            finetuning_type = _g("finetuning_type")
            model_name = _g("model_name", "unknown")
            if checkpoint_path:
                if finetuning_type in PEFT_METHODS:
                    if isinstance(checkpoint_path, list):
                        args["adapter_name_or_path"] = ",".join(
                            [get_save_dir(model_name, finetuning_type, cp) for cp in checkpoint_path]
                        )
                    else:
                        args["adapter_name_or_path"] = get_save_dir(model_name, finetuning_type, checkpoint_path)
                else:
                    if isinstance(checkpoint_path, list):
                        args["model_name_or_path"] = get_save_dir(model_name, finetuning_type, checkpoint_path[0])
                    else:
                        args["model_name_or_path"] = get_save_dir(model_name, finetuning_type, checkpoint_path)

            # Quantization
            if _g("quantization_bit") and _g("quantization_bit") != "none":
                args["quantization_bit"] = int(_g("quantization_bit"))
                args["quantization_method"] = _g("quantization_method")
                args["double_quantization"] = not is_torch_npu_available()

        return args

    @staticmethod
    def _build_config_dict(params: dict[str, Any]) -> dict[str, Any]:
        r"""Build a dict of UI-level config for saving alongside the run (resume support)."""
        skip_keys = {"lang", "model_path", "output_dir", "config_path"}
        return {k: v for k, v in params.items() if k not in skip_keys}

    def start(self, params: dict[str, Any], do_train: bool) -> str:
        r"""Start a training or evaluation run. Returns the output_dir."""
        args = self.build_args(params, do_train)
        self.do_train = do_train
        self.aborted = False
        self.running = True
        output_dir = args["output_dir"]

        os.makedirs(output_dir, exist_ok=True)
        self._output_path = output_dir

        # Save full UI config for resume / output-dir check
        config_dict = self._build_config_dict(params)
        save_args(os.path.join(output_dir, LLAMABOARD_CONFIG), config_dict)

        env = deepcopy(os.environ)
        env["LLAMABOARD_ENABLED"] = "1"
        env["LLAMABOARD_WORKDIR"] = output_dir
        if args.get("deepspeed") is not None:
            env["FORCE_TORCHRUN"] = "1"

        args_path = save_cmd(args)
        self.trainer = Popen(["llamafactory-cli", "train", args_path], env=env, stderr=PIPE, text=True)
        self.current_run_id = os.path.basename(output_dir)
        return output_dir

    def preview(self, params: dict[str, Any], do_train: bool) -> str:
        r"""Preview the training command without running it."""
        args = self.build_args(params, do_train)
        return gen_cmd(args)

    async def monitor(self) -> None:
        r"""Monitor the running process and push progress via WebSocket queues."""
        if self.trainer is None or self._output_path is None:
            return

        output_path = self._output_path
        last_log_len = 0
        last_trainer_log_len = 0
        stderr_lines: list[str] = []
        loop = asyncio.get_running_loop()

        while True:
            if self.trainer is None:
                break

            if self.aborted:
                # Already flagged — skip stderr reading, just wait for exit
                pass
            else:
                # Collect any new stderr output (non-blocking via thread executor)
                if self.trainer.stderr and not self.trainer.stderr.closed:
                    try:
                        line = await loop.run_in_executor(None, self.trainer.stderr.readline)
                        count = 0
                        while line and count < 100:
                            stderr_lines.append(line)
                            count += 1
                            line = await loop.run_in_executor(None, self.trainer.stderr.readline)
                    except Exception:
                        pass

            return_code = self.trainer.poll()
            if return_code is not None:
                # Read remaining stderr (non-blocking)
                remaining_stderr = ""
                if self.trainer.stderr and not self.trainer.stderr.closed:
                    try:
                        remaining_stderr = await loop.run_in_executor(None, self.trainer.stderr.read)
                    except Exception:
                        pass

                stderr_output = "".join(stderr_lines) + remaining_stderr

                # Push remaining log
                running_log = _read_running_log(output_path)
                if running_log:
                    await self._broadcast({"type": "log", "text": running_log})

                if return_code == 0 and not self.aborted:
                    await self._broadcast({
                        "type": "train:complete",
                        "status": "success",
                        "message": "Training completed successfully.",
                    })
                elif self.aborted:
                    await self._broadcast({
                        "type": "train:complete",
                        "status": "aborted",
                        "message": "Training aborted.",
                    })
                else:
                    await self._broadcast({
                        "type": "train:complete",
                        "status": "error",
                        "message": f"Training failed. Exit code: {return_code}\n{stderr_output[:5000]}",
                    })
                break

            # Read running log (new content)
            running_log = _read_running_log(output_path)
            if len(running_log) != last_log_len:
                last_log_len = len(running_log)
                await self._broadcast({"type": "log", "text": running_log})

            # Read trainer log for progress/loss
            trainer_records = _read_trainer_log(output_path)
            if len(trainer_records) > last_trainer_log_len:
                for record in trainer_records[last_trainer_log_len:]:
                    await self._broadcast({
                        "type": "progress",
                        "percentage": record.get("percentage", 0),
                        "current": record.get("current_steps", 0),
                        "total": record.get("total_steps", 0),
                        "remaining_secs": record.get("remaining_time", 0),
                        "elapsed_secs": record.get("elapsed_time", 0),
                    })
                    if "loss" in record:
                        await self._broadcast({
                            "type": "loss",
                            "step": record.get("current_steps", 0),
                            "value": record["loss"],
                        })
                last_trainer_log_len = len(trainer_records)

            await asyncio.sleep(2 if not self.aborted else 1)

        self._cleanup()

    def check_output_dir(self, model_name: str, finetuning_type: str, output_dir: str) -> dict[str, Any]:
        r"""Check if output_dir exists and return saved config if available."""
        from yaml import safe_load

        result: dict[str, Any] = {"exists": False, "warning": "", "config": None}
        if not model_name or not output_dir:
            return result

        save_dir = get_save_dir(model_name, finetuning_type, output_dir)
        if os.path.isdir(save_dir):
            result["exists"] = True
            result["warning"] = "Output directory already exists."
            config_path = os.path.join(save_dir, LLAMABOARD_CONFIG)
            if os.path.isfile(config_path):
                try:
                    with open(config_path, encoding="utf-8") as f:
                        result["config"] = safe_load(f)
                except Exception:
                    pass
        return result

    def get_train_status(self) -> dict[str, Any]:
        r"""Get current training/eval status without Gradio components."""
        if not self.running or self._output_path is None:
            return {"running": False, "current_step": 0, "total_steps": 0, "loss": None, "progress": 0, "run_id": self.current_run_id}

        records = _read_trainer_log(self._output_path)
        if records:
            latest = records[-1]
            return {
                "running": self.running,
                "current_step": latest.get("current_steps", 0),
                "total_steps": latest.get("total_steps", 0),
                "loss": latest.get("loss"),
                "progress": latest.get("percentage", 0),
                "run_id": self.current_run_id,
            }
        return {"running": self.running, "current_step": 0, "total_steps": 0, "loss": None, "progress": 0, "run_id": self.current_run_id}

    @staticmethod
    def _build_export_args(params: dict[str, Any]) -> dict[str, Any]:
        r"""Build export args from params dict (mirrors old Gradio save_model)."""
        _g = lambda key, default=None: params.get(key) if params.get(key) not in (None, "") else default

        model_name = _g("model_name", "unknown")
        finetuning_type = _g("finetuning_type", "full")

        args = dict(
            stage="sft",
            do_export=True,
            model_name_or_path=_g("model_path"),
            finetuning_type=finetuning_type,
            template=_g("template", "default"),
            export_dir=_g("export_dir", ""),
            export_size=_g("export_size", 1),
            export_device=_g("export_device", "cpu"),
            export_legacy_format=_g("export_legacy_format", False),
            trust_remote_code=True,
        )

        if _g("export_quantization_bit") and _g("export_quantization_bit") != "none":
            args["export_quantization_bit"] = int(_g("export_quantization_bit"))
            args["export_quantization_dataset"] = _g("export_quantization_dataset") or "data"

        if _g("export_hub_model_id"):
            args["export_hub_model_id"] = _g("export_hub_model_id")

        # Checkpoints
        checkpoint_path = _g("checkpoint_path")
        if checkpoint_path:
            if finetuning_type in PEFT_METHODS:
                if isinstance(checkpoint_path, list):
                    args["adapter_name_or_path"] = ",".join(
                        [get_save_dir(model_name, finetuning_type, cp) for cp in checkpoint_path]
                    )
                else:
                    args["adapter_name_or_path"] = get_save_dir(model_name, finetuning_type, checkpoint_path)
            else:
                if isinstance(checkpoint_path, list):
                    args["model_name_or_path"] = get_save_dir(model_name, finetuning_type, checkpoint_path[0])
                else:
                    args["model_name_or_path"] = get_save_dir(model_name, finetuning_type, checkpoint_path)

        # Extra args override
        extra_args = _g("extra_args")
        if extra_args:
            if isinstance(extra_args, str):
                args.update(json.loads(extra_args))
            elif isinstance(extra_args, dict):
                args.update(extra_args)

        return args

    def start_export(self, params: dict[str, Any]) -> str:
        r"""Start an export run. Returns the output_dir."""
        args = self._build_export_args(params)
        self.do_train = False
        self.aborted = False
        self.running = True
        output_dir = args.get("export_dir", "") or os.path.dirname(args.get("model_name_or_path", "."))

        os.makedirs(output_dir, exist_ok=True)
        self._output_path = output_dir

        env = deepcopy(os.environ)
        env["LLAMABOARD_ENABLED"] = "1"

        args_path = save_cmd(args)
        self.trainer = Popen(["llamafactory-cli", "export", args_path], env=env, stderr=PIPE, text=True)
        self.current_run_id = os.path.basename(output_dir)
        return output_dir

    def _cleanup(self) -> None:
        self.trainer = None
        self.aborted = False
        self.running = False
        self.current_run_id = None
        self._output_path = None
        torch_gc()


class EngineHolder:
    r"""Singleton holding all state for the API layer."""

    def __init__(self) -> None:
        self.runner = ApiRunner()
        self.chat_model: ChatModel | None = None
        self.current_model_info: dict[str, Any] = {}

    @property
    def is_training(self) -> bool:
        return self.runner.running

    @property
    def is_model_loaded(self) -> bool:
        return self.chat_model is not None

    def get_status(self) -> dict[str, Any]:
        model_info = self.current_model_info if self.is_model_loaded else {}
        if self.is_training:
            state = EngineState.TRAINING if self.runner.do_train else EngineState.EVALUATING
        elif self.is_model_loaded:
            state = EngineState.MODEL_LOADED
        else:
            state = EngineState.IDLE

        return {
            "status": state.value,
            "model_name": model_info.get("model_name", ""),
            "model_path": model_info.get("model_path", ""),
            "finetuning_type": model_info.get("finetuning_type", ""),
            "template": model_info.get("template", ""),
            "quantized_bit": model_info.get("quantized_bit", ""),
            "checkpoint_path": model_info.get("checkpoint_path", ""),
            "output_dir": self.runner.current_run_id or "",
        }

    def load_chat_model(self, params: dict[str, Any]) -> None:
        r"""Load a model for chat/inference."""
        args = dict(
            model_name_or_path=params.get("model_path") or params.get("model_name_or_path"),
            cache_dir=params.get("cache_dir") or load_config().get("cache_dir"),
            finetuning_type=params.get("finetuning_type"),
            template=params.get("template"),
            rope_scaling=(
                params.get("rope_scaling")
                if params.get("rope_scaling") and params.get("rope_scaling") != "none"
                else None
            ),
            flash_attn="fa2" if params.get("booster") == "flashattn2" else "auto",
            use_unsloth=(params.get("booster") == "unsloth"),
            enable_liger_kernel=(params.get("booster") == "liger_kernel"),
            infer_backend=params.get("infer_backend", "huggingface"),
            infer_dtype=params.get("infer_dtype", "auto"),
            trust_remote_code=True,
        )

        # Extra args
        extra_args = params.get("extra_args")
        if extra_args:
            if isinstance(extra_args, str):
                args.update(json.loads(extra_args))
            elif isinstance(extra_args, dict):
                args.update(extra_args)

        # Checkpoints
        checkpoint_path = params.get("checkpoint_path")
        finetuning_type = params.get("finetuning_type")
        model_name = params.get("model_name", "unknown")
        if checkpoint_path:
            if finetuning_type in PEFT_METHODS:
                if isinstance(checkpoint_path, list):
                    args["adapter_name_or_path"] = ",".join(
                        [get_save_dir(model_name, finetuning_type, cp) for cp in checkpoint_path]
                    )
                else:
                    args["adapter_name_or_path"] = get_save_dir(model_name, finetuning_type, checkpoint_path)
            else:
                if isinstance(checkpoint_path, list):
                    args["model_name_or_path"] = get_save_dir(model_name, finetuning_type, checkpoint_path[0])
                else:
                    args["model_name_or_path"] = get_save_dir(model_name, finetuning_type, checkpoint_path)

        # Quantization
        if params.get("quantization_bit") and params.get("quantization_bit") != "none":
            args["quantization_bit"] = int(params["quantization_bit"])
            args["quantization_method"] = params.get("quantization_method", "bnb")
            args["double_quantization"] = not is_torch_npu_available()

        self.chat_model = ChatModel(args)
        self.current_model_info = {
            "model_name": params.get("model_name", ""),
            "model_path": params.get("model_path", ""),
            "finetuning_type": params.get("finetuning_type", ""),
            "template": params.get("template", ""),
            "quantized_bit": params.get("quantization_bit", ""),
            "checkpoint_path": params.get("checkpoint_path", ""),
        }

    def unload_chat_model(self) -> None:
        r"""Unload the chat model and free GPU memory."""
        self.chat_model = None
        self.current_model_info = {}
        torch_gc()

    async def stream_chat(
        self,
        messages: list[dict[str, str]],
        system: str | None = None,
        tools: str | None = None,
        max_new_tokens: int = 2048,
        top_p: float = 0.9,
        temperature: float = 0.6,
    ) -> AsyncGenerator[str, None]:
        r"""Stream chat responses from the loaded model."""
        if self.chat_model is None:
            raise RuntimeError("No model loaded")

        async for new_token in self.chat_model.astream_chat(
            messages,
            system,
            tools,
            max_new_tokens=max_new_tokens,
            top_p=top_p,
            temperature=temperature,
        ):
            yield new_token

    def reset(self) -> None:
        self.runner = ApiRunner()
        self.chat_model = None
        self.current_model_info = {}
        torch_gc()


# Global singleton
_engine_holder: EngineHolder | None = None


def get_engine_holder() -> EngineHolder:
    global _engine_holder
    if _engine_holder is None:
        _engine_holder = EngineHolder()
    return _engine_holder
