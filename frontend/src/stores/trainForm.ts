import { defineStore } from "pinia";
import { reactive, ref, watch } from "vue";
import { getJson } from "@/api/client";

export interface TrainFormState {
  training_stage: string;
  dataset_dir: string;
  dataset: string[];
  learning_rate: string;
  num_train_epochs: string;
  max_samples: string;
  max_grad_norm: string;
  compute_type: string;
  cutoff_len: number;
  batch_size: number;
  gradient_accumulation_steps: number;
  val_size: number;
  lr_scheduler_type: string;
  warmup_steps: number;
  warmup_ratio: string;
  neftune_alpha: number;
  logging_steps: number;
  save_steps: number;
  output_dir: string;
  packing: boolean;
  neat_packing: boolean;
  train_on_prompt: boolean;
  mask_history: boolean;
  resize_vocab: boolean;
  use_llama_pro: boolean;
  enable_thinking: boolean;
  report_to: string;
  extra_args: string;

  lora_rank: number;
  lora_alpha: number;
  lora_dropout: number;
  lora_target: string;
  loraplus_lr_ratio: number;
  additional_target: string;
  create_new_adapter: boolean;
  use_rslora: boolean;
  use_dora: boolean;
  use_pissa: boolean;

  freeze_trainable_layers: number;
  freeze_trainable_modules: string;
  freeze_extra_modules: string;

  pref_beta: number;
  pref_ftx: number;
  pref_loss: string;
  reward_model: string[];
  ppo_score_norm: boolean;
  ppo_whiten_rewards: boolean;

  freeze_vision_tower: boolean;
  freeze_multi_modal_projector: boolean;
  freeze_language_model: boolean;
  image_max_pixels: string;
  image_min_pixels: string;
  video_max_pixels: string;
  video_min_pixels: string;

  use_galore: boolean;
  galore_rank: number;
  galore_update_interval: number;
  galore_scale: number;
  galore_target: string;
  use_apollo: boolean;
  apollo_rank: number;
  apollo_update_interval: number;
  apollo_scale: number;
  apollo_target: string;
  use_badam: boolean;
  badam_mode: string;
  badam_switch_mode: string;
  badam_switch_interval: number;
  badam_update_ratio: number;

  use_swanlab: boolean;
  swanlab_project: string;
  swanlab_run_name: string;
  swanlab_workspace: string;
  swanlab_api_key: string;
  swanlab_mode: string;
  swanlab_logdir: string;

  project: string;
  trackio_space_id: string;
  hub_private_repo: boolean;

  deepspeed: string;
  ds_stage: string;
  ds_offload: boolean;
  device_count: number;
}

export const DEFAULT_TRAIN_FORM: TrainFormState = {
  training_stage: "sft",
  dataset_dir: "data",
  dataset: [],
  learning_rate: "5e-5",
  num_train_epochs: "3",
  max_samples: "",
  max_grad_norm: "1.0",
  compute_type: "bf16",
  cutoff_len: 2048,
  batch_size: 2,
  gradient_accumulation_steps: 8,
  val_size: 0.0,
  lr_scheduler_type: "cosine",
  warmup_steps: 0,
  warmup_ratio: "0.03",
  neftune_alpha: 0.0,
  logging_steps: 5,
  save_steps: 100,
  output_dir: "",
  packing: false,
  neat_packing: false,
  train_on_prompt: false,
  mask_history: false,
  resize_vocab: false,
  use_llama_pro: false,
  enable_thinking: true,
  report_to: "none",
  extra_args: "{}",

  lora_rank: 8,
  lora_alpha: 16,
  lora_dropout: 0.0,
  lora_target: "q_proj,v_proj",
  loraplus_lr_ratio: 0.0,
  additional_target: "",
  create_new_adapter: false,
  use_rslora: false,
  use_dora: false,
  use_pissa: false,

  freeze_trainable_layers: 2,
  freeze_trainable_modules: "all",
  freeze_extra_modules: "",

  pref_beta: 0.1,
  pref_ftx: 0.0,
  pref_loss: "sigmoid",
  reward_model: [],
  ppo_score_norm: false,
  ppo_whiten_rewards: false,

  freeze_vision_tower: true,
  freeze_multi_modal_projector: true,
  freeze_language_model: false,
  image_max_pixels: "768*768",
  image_min_pixels: "32*32",
  video_max_pixels: "256*256",
  video_min_pixels: "16*16",

  use_galore: false,
  galore_rank: 16,
  galore_update_interval: 200,
  galore_scale: 2.0,
  galore_target: "all",
  use_apollo: false,
  apollo_rank: 16,
  apollo_update_interval: 200,
  apollo_scale: 32.0,
  apollo_target: "all",
  use_badam: false,
  badam_mode: "layer",
  badam_switch_mode: "ascending",
  badam_switch_interval: 50,
  badam_update_ratio: 0.05,

  use_swanlab: false,
  swanlab_project: "llamafactory",
  swanlab_run_name: "",
  swanlab_workspace: "",
  swanlab_api_key: "",
  swanlab_mode: "cloud",
  swanlab_logdir: "",

  project: "huggingface",
  trackio_space_id: "trackio",
  hub_private_repo: false,

  deepspeed: "",
  ds_stage: "none",
  ds_offload: false,
  device_count: 1,
};

export const useTrainFormStore = defineStore("trainForm", () => {
  const form = reactive<TrainFormState>({ ...DEFAULT_TRAIN_FORM });

  const FALLBACK_DATASETS = [
    { label: "alpaca_zh_demo", value: "alpaca_zh_demo" },
    { label: "alpaca_en_demo", value: "alpaca_en_demo" },
    { label: "identity", value: "identity" },
  ];

  const datasetOptions = ref<{ label: string; value: string }[]>([...FALLBACK_DATASETS]);

  async function fetchDatasets(stage: string, dir?: string): Promise<void> {
    form.dataset = [];
    try {
      const params: Record<string, string> = { stage, format: "select" };
      if (dir) params.dir = dir;
      const data = await getJson<{ label: string; value: string }[]>("/datasets", params);
      if (data.length > 0) {
        datasetOptions.value = data;
      }
    } catch {
      // keep fallback values
    }
  }

  // 级联：training_stage 变化 → 过滤可用数据集
  watch(
    () => form.training_stage,
    (stage) => {
      fetchDatasets(stage, form.dataset_dir);
    },
    { immediate: true },
  );

  // 级联：dataset_dir 变化 → 重新加载数据集
  watch(
    () => form.dataset_dir,
    (dir) => {
      fetchDatasets(form.training_stage, dir);
    },
  );

  function updateFields(fields: Partial<TrainFormState>): void {
    Object.assign(form, fields);
  }

  function reset(): void {
    Object.assign(form, { ...DEFAULT_TRAIN_FORM });
  }

  function toParams(): Record<string, unknown> {
    return { ...form };
  }

  function updateField<K extends keyof TrainFormState>(field: K, value: TrainFormState[K]): void {
    form[field] = value;
  }

  return { form, updateField, updateFields, reset, toParams, datasetOptions };
});
