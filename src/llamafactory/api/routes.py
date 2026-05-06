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

r"""REST API routes for the LLaMA Factory backend."""

import json
import os
from typing import Any, NoReturn

from fastapi import APIRouter, HTTPException, Query, status

from ..extras.constants import (
    CHECKPOINT_NAMES,
    SUPPORTED_MODELS,
    TRAINING_STAGES,
    DownloadSource,
)
from ..extras.misc import use_modelscope, use_openmind
from ..webui.common import (
    DEFAULT_CONFIG_DIR,
    DEFAULT_DATA_DIR,
    get_model_path,
    get_save_dir,
    get_template,
    get_time,
    load_args,
    load_config,
    load_dataset_info,
    save_args,
)
from .deps import EngineHolderDep

router = APIRouter()

# Generated once at server startup — mirrors Gradio engine.resume() behavior
_START_TIME = get_time()


def _success(data: Any, message: str | None = None) -> dict[str, Any]:
    r"""Wrap a successful response."""
    result: dict[str, Any] = {"success": True, "data": data}
    if message:
        result["message"] = message
    return result


def _error(message: str, status_code: int = status.HTTP_400_BAD_REQUEST) -> NoReturn:
    r"""Raise an HTTPException with the standard error format."""
    raise HTTPException(status_code=status_code, detail={"success": False, "message": message})


# ---------------------------------------------------------------------------
# A. System Status
# ---------------------------------------------------------------------------


@router.get("/status")
async def get_status(engine_holder: EngineHolderDep):
    r"""Get the current system status."""
    return _success(engine_holder.get_status())


@router.get("/on-model-change")
async def on_model_change(
    engine_holder: EngineHolderDep,
    model_name: str = Query(default=""),
    finetuning_type: str = Query(default="lora"),
):
    r"""Get model info when model selection changes."""
    model_path = get_model_path(model_name) if model_name else ""
    template = get_template(model_name) if model_name else "default"

    # List checkpoints
    checkpoints: list[str] = []
    if model_name:
        save_dir = get_save_dir(model_name, finetuning_type)
        if save_dir and os.path.isdir(save_dir):
            for checkpoint in os.listdir(save_dir):
                checkpoint_dir = os.path.join(save_dir, checkpoint)
                if os.path.isdir(checkpoint_dir) and any(
                    os.path.isfile(os.path.join(checkpoint_dir, name)) for name in CHECKPOINT_NAMES
                ):
                    checkpoints.append(checkpoint)

    # Quantization availability
    quantization_available = "none"
    if finetuning_type in {"lora", "oft"}:
        import torch

        if torch.cuda.is_available():
            quantization_available = "none,8,4"
        else:
            quantization_available = "none,8"

    # Output dirs
    output_dirs: list[str] = []
    if model_name:
        save_dir = get_save_dir(model_name, finetuning_type)
        if save_dir and os.path.isdir(save_dir):
            from transformers.trainer_utils import get_last_checkpoint

            for folder in os.listdir(save_dir):
                output_dir_path = os.path.join(save_dir, folder)
                if os.path.isdir(output_dir_path) and get_last_checkpoint(output_dir_path) is not None:
                    output_dirs.append(folder)

    return _success({
        "model_path": model_path,
        "template": template,
        "checkpoints": checkpoints,
        "quantization_available": quantization_available,
        "output_dirs": output_dirs,
    })


# ---------------------------------------------------------------------------
# B. Resource Queries
# ---------------------------------------------------------------------------


@router.get("/models")
async def list_models(
    engine_holder: EngineHolderDep,  # noqa: ARG001
):
    r"""List all supported models."""
    user_config = load_config()
    path_dict = user_config.get("path_dict", {})
    models = []
    seen = set()
    for model_name in SUPPORTED_MODELS:
        if model_name not in seen:
            seen.add(model_name)
            model_entry = SUPPORTED_MODELS[model_name]
            model_path = path_dict.get(model_name) or model_entry.get(DownloadSource.DEFAULT, "")
            if use_modelscope() and model_entry.get(DownloadSource.MODELSCOPE) and not path_dict.get(model_name):
                model_path = model_entry[DownloadSource.MODELSCOPE]
            if use_openmind() and model_entry.get(DownloadSource.OPENMIND) and not path_dict.get(model_name):
                model_path = model_entry[DownloadSource.OPENMIND]

            models.append({
                "model_name": model_name,
                "model_path": model_path,
                "template": get_template(model_name),
            })
    return _success(models)


@router.get("/models/{model_name:path}")
async def get_model_detail(model_name: str):
    r"""Get details of a specific model."""
    if model_name not in SUPPORTED_MODELS:
        _error(f"Model '{model_name}' not found", status.HTTP_404_NOT_FOUND)

    model_path = get_model_path(model_name)
    template = get_template(model_name)
    return _success({
        "model_name": model_name,
        "model_path": model_path,
        "template": template,
        "finetuning_type": "lora",
        "quantized_bit": "none",
    })


@router.get("/checkpoints")
async def list_checkpoints(
    model: str = Query(default=""),
    ft: str = Query(default="lora", alias="finetuning_type"),
):
    r"""List available checkpoints for a model."""
    checkpoints: list[str] = []
    if not model:
        return _success(checkpoints)

    save_dir = get_save_dir(model, ft)
    if save_dir and os.path.isdir(save_dir):
        for checkpoint in os.listdir(save_dir):
            checkpoint_dir = os.path.join(save_dir, checkpoint)
            if os.path.isdir(checkpoint_dir) and any(
                os.path.isfile(os.path.join(checkpoint_dir, name)) for name in CHECKPOINT_NAMES
            ):
                checkpoints.append(checkpoint)

    return _success(checkpoints)


@router.get("/datasets")
async def list_datasets(
    dir: str | None = Query(default=None),
    stage: str = Query(default="Supervised Fine-Tuning"),
    format: str = Query(default="array", alias="format"),
):
    r"""List available datasets.

    Supports two formats:
    - "array": returns a plain list of dataset names
    - "select": returns a list of {label, value} objects
    """
    from ..extras.constants import STAGES_USE_PAIR_DATA

    # Resolve dir: if relative or not given, use DEFAULT_DATA_DIR (now absolute)
    dataset_dir = dir if (dir and os.path.isabs(dir)) else DEFAULT_DATA_DIR
    dataset_info = load_dataset_info(dataset_dir)
    training_stage_key = TRAINING_STAGES.get(stage, "sft")
    ranking = training_stage_key in STAGES_USE_PAIR_DATA
    datasets = [k for k, v in dataset_info.items() if v.get("ranking", False) == ranking]

    if format == "select":
        return _success([{"label": d, "value": d} for d in datasets])
    else:
        return _success(datasets)


@router.get("/output-dirs")
async def list_output_dirs(
    model: str = Query(default=""),
    ft: str = Query(default="lora", alias="finetuning_type"),
    prefix: str = Query(default="train"),
):
    r"""List available output directories for resume."""
    from transformers.trainer_utils import get_last_checkpoint

    # Always include the auto-generated default name (mirrors Gradio list_output_dirs)
    output_dirs: list[str] = [f"{prefix}_{_START_TIME}"]
    if model:
        save_dir = get_save_dir(model, ft)
        if save_dir and os.path.isdir(save_dir):
            for folder in os.listdir(save_dir):
                output_dir_path = os.path.join(save_dir, folder)
                if os.path.isdir(output_dir_path) and get_last_checkpoint(output_dir_path) is not None:
                    if folder not in output_dirs:
                        output_dirs.append(folder)

    return _success(output_dirs)


@router.get("/output-dir/check")
async def check_output_dir(
    engine_holder: EngineHolderDep,
    model_name: str = Query(...),
    finetuning_type: str = Query("full"),
    output_dir: str = Query(...),
):
    r"""Check if output_dir already exists on disk and return saved config if available."""
    result = engine_holder.runner.check_output_dir(model_name, finetuning_type, output_dir)
    return _success(result)


@router.get("/configs")
async def list_configs():
    r"""List saved training configuration files."""
    # Always include the auto-generated default name (mirrors Gradio list_config_paths)
    default_name = f"{_START_TIME}.yaml"
    config_files: list[str] = [default_name]
    if os.path.isdir(DEFAULT_CONFIG_DIR):
        for file_name in os.listdir(DEFAULT_CONFIG_DIR):
            if file_name.endswith(".yaml") and file_name != default_name:
                config_files.append(file_name)
    return _success(sorted(config_files))


@router.get("/configs/{config_name:path}")
async def get_config(config_name: str):
    r"""Load a saved training configuration file."""
    config_path = os.path.realpath(os.path.join(DEFAULT_CONFIG_DIR, config_name))
    if not config_path.startswith(os.path.realpath(DEFAULT_CONFIG_DIR) + os.sep):
        _error("Invalid config path.", status.HTTP_400_BAD_REQUEST)
    if not os.path.isfile(config_path):
        _error(f"Config '{config_name}' not found.", status.HTTP_404_NOT_FOUND)
    config = load_args(config_path)
    if config is None:
        _error(f"Failed to load config '{config_name}'.", status.HTTP_500_INTERNAL_SERVER_ERROR)
    return _success(config)


@router.post("/configs/{config_name:path}")
async def save_config(config_name: str, body: dict[str, Any]):
    r"""Save a training configuration file."""
    config_path = os.path.realpath(os.path.join(DEFAULT_CONFIG_DIR, config_name))
    if not config_path.startswith(os.path.realpath(DEFAULT_CONFIG_DIR) + os.sep):
        _error("Invalid config path.", status.HTTP_400_BAD_REQUEST)
    os.makedirs(DEFAULT_CONFIG_DIR, exist_ok=True)
    if not config_path.endswith(".yaml"):
        config_path += ".yaml"
    save_args(config_path, body)
    return _success({}, "Config saved.")


@router.get("/templates")
async def list_templates():
    r"""List all available chat templates."""
    # Lazily import to avoid heavy data module loading at startup
    from ..data import TEMPLATES

    template_names = sorted(TEMPLATES.keys())
    return _success(template_names)


# ---------------------------------------------------------------------------
# C. Training Operations
# ---------------------------------------------------------------------------


def _validate_train(params: dict[str, Any]) -> None:
    r"""Validate training parameters before starting (mirrors old _initialize)."""
    if not params.get("model_name"):
        _error("Please select a model.")
    if not params.get("model_path"):
        _error("Model not found.")
    dataset = params.get("dataset")
    if not dataset or (isinstance(dataset, list) and not any(dataset)):
        _error("Please choose a dataset.")
    if not params.get("output_dir"):
        _error("Please provide output dir.")
    extra_args = params.get("extra_args", "{}")
    if isinstance(extra_args, str):
        try:
            json.loads(extra_args)
        except json.JSONDecodeError:
            _error("Invalid JSON schema for extra_args.")
    stage = TRAINING_STAGES.get(params.get("training_stage", "sft"), "sft")
    if stage == "ppo" and not params.get("reward_model"):
        _error("Please select a reward model.")


def _validate_eval(params: dict[str, Any]) -> None:
    r"""Validate evaluation parameters before starting."""
    if not params.get("model_name"):
        _error("Please select a model.")
    if not params.get("model_path"):
        _error("Model not found.")
    dataset = params.get("dataset")
    if not dataset or (isinstance(dataset, list) and not any(dataset)):
        _error("Please choose a dataset.")
    if not params.get("output_dir"):
        _error("Please provide output dir.")


@router.post("/train/preview")
async def preview_train(params: dict[str, Any], engine_holder: EngineHolderDep):
    r"""Preview training command without starting it."""
    do_train = params.get("do_train", True)
    cmd_text = engine_holder.runner.preview(params, do_train=do_train)
    args = engine_holder.runner.build_args(params, do_train=do_train)
    return _success({
        "command": cmd_text.split("\n"),
        "output_dir": args.get("output_dir", ""),
    })


@router.post("/train/start")
async def start_train(params: dict[str, Any], engine_holder: EngineHolderDep):
    r"""Start a training run."""
    if engine_holder.is_training:
        _error("A training or evaluation run is already in progress.", status.HTTP_409_CONFLICT)

    _validate_train(params)

    output_dir = engine_holder.runner.start(params, do_train=True)
    run_id = os.path.basename(output_dir)

    # Start background monitor
    import asyncio
    asyncio.ensure_future(engine_holder.runner.monitor())

    return _success({"run_id": run_id})


@router.post("/train/abort")
async def abort_train(engine_holder: EngineHolderDep):
    r"""Abort the current training run."""
    if not engine_holder.is_training:
        return _success(None, "No training or evaluation run in progress.")
    engine_holder.runner.set_abort()
    return _success(None, "Training aborted.")


@router.get("/train/status")
async def train_status(engine_holder: EngineHolderDep):
    r"""Get the current training status."""
    return _success(engine_holder.runner.get_train_status())


# ---------------------------------------------------------------------------
# D. Evaluation Operations
# ---------------------------------------------------------------------------


@router.post("/eval/start")
async def start_eval(params: dict[str, Any], engine_holder: EngineHolderDep):
    r"""Start an evaluation run."""
    if engine_holder.is_training:
        _error("A training or evaluation run is already in progress.", status.HTTP_409_CONFLICT)

    _validate_eval(params)

    output_dir = engine_holder.runner.start(params, do_train=False)
    run_id = os.path.basename(output_dir)

    # Start background monitor
    import asyncio
    asyncio.ensure_future(engine_holder.runner.monitor())

    return _success({"run_id": run_id})


@router.get("/eval/status")
async def eval_status(engine_holder: EngineHolderDep):
    r"""Get the current evaluation status."""
    return _success(engine_holder.runner.get_train_status())


# ---------------------------------------------------------------------------
# E. Chat Model Management
# ---------------------------------------------------------------------------


@router.post("/model/load")
async def load_model(params: dict[str, Any], engine_holder: EngineHolderDep):
    r"""Load a model for chat/inference."""
    if engine_holder.is_model_loaded:
        _error("A model is already loaded. Unload it first.", status.HTTP_409_CONFLICT)

    try:
        engine_holder.load_chat_model(params)
    except Exception as e:
        _error(f"Failed to load model: {str(e)}", status.HTTP_500_INTERNAL_SERVER_ERROR)

    return _success(None, "Model loaded successfully.")


@router.post("/model/unload")
async def unload_model(engine_holder: EngineHolderDep):
    r"""Unload the current chat model."""
    if not engine_holder.is_model_loaded:
        _error("No model is currently loaded.", status.HTTP_409_CONFLICT)

    engine_holder.unload_chat_model()
    return _success(None, "Model unloaded successfully.")


# ---------------------------------------------------------------------------
# F. Model Export
# ---------------------------------------------------------------------------


@router.post("/export/start")
async def start_export(params: dict[str, Any], engine_holder: EngineHolderDep):
    r"""Start a model export run."""
    if engine_holder.is_training:
        _error("A training or evaluation run is already in progress.", status.HTTP_409_CONFLICT)

    if not params.get("model_name"):
        _error("Please select a model.")
    if not params.get("model_path"):
        _error("Model not found.")
    if not params.get("export_dir"):
        _error("Please provide export dir.")

    output_dir = engine_holder.runner.start_export(params)
    import asyncio
    asyncio.ensure_future(engine_holder.runner.monitor())

    return _success({"run_id": os.path.basename(output_dir), "output_dir": output_dir})


@router.get("/export/status")
async def export_status(engine_holder: EngineHolderDep):
    r"""Get the current export status."""
    return _success(engine_holder.runner.get_train_status())


@router.post("/export/abort")
async def abort_export(engine_holder: EngineHolderDep):
    r"""Abort the current export run."""
    if not engine_holder.is_training:
        _error("No export run in progress.", status.HTTP_409_CONFLICT)
    engine_holder.runner.set_abort()
    return _success(None, "Export aborted.")


# ---------------------------------------------------------------------------
# G. GPU Memory & Dataset Preview
# ---------------------------------------------------------------------------


@router.get("/gpu-memory")
async def get_gpu_memory():
    r"""Get GPU memory usage."""
    try:
        import torch

        if not torch.cuda.is_available():
            return _success({"used": 0, "total": 0}, "No GPU available.")

        used = 0
        total = 0
        for i in range(torch.cuda.device_count()):
            total_mem = torch.cuda.get_device_properties(i).total_mem
            allocated = torch.cuda.memory_allocated(i)
            total += total_mem
            used += allocated

        # Convert bytes to GB
        def to_gb(b):
            return round(b / (1024**3), 2)

        return _success({
            "used": to_gb(used),
            "total": to_gb(total),
            "utilization": round(used / total * 100, 1) if total > 0 else 0,
            "device_count": torch.cuda.device_count(),
        })
    except ImportError:
        return _success({"used": 0, "total": 0}, "PyTorch not available.")


@router.get("/datasets/preview")
async def preview_dataset(
    dataset: str = Query(...),
    dataset_dir: str | None = Query(default=None),
    page: int = Query(default=1, ge=1),
    page_size: int = Query(default=10, ge=1, le=100),
):
    r"""Preview a dataset's samples."""
    data_dir = dataset_dir if (dataset_dir and os.path.isabs(dataset_dir)) else DEFAULT_DATA_DIR

    # Try loading from dataset_info.json first
    dataset_info = load_dataset_info(data_dir)
    if dataset not in dataset_info:
        _error(f"Dataset '{dataset}' not found in {data_dir}/dataset_info.json")

    from datasets import load_dataset as hf_load_dataset

    ds_path = dataset_info[dataset].get("file_name", dataset)
    full_path = os.path.join(data_dir, ds_path)

    if not os.path.isfile(full_path):
        _error(f"Dataset file not found: {full_path}")

    try:
        hf_ds = hf_load_dataset(
            "json",
            data_files=full_path,
            split="train",
        )
    except Exception:
        try:
            hf_ds = hf_load_dataset(
                "csv",
                data_files=full_path,
                split="train",
            )
        except Exception:
            _error(f"Unable to load dataset file: {full_path}")

    total = len(hf_ds)
    start_idx = (page - 1) * page_size
    end_idx = min(start_idx + page_size, total)
    samples = [hf_ds[i] for i in range(start_idx, end_idx)]

    return _success({
        "total": total,
        "page": page,
        "page_size": page_size,
        "samples": samples,
    })
