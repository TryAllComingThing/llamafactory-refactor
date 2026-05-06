import { defineStore } from "pinia";
import { reactive, ref, watch } from "vue";
import { getJson } from "@/api/client";

export interface EvalFormState {
  model_name: string;
  finetuning_type: string;
  dataset: string[];
  dataset_dir: string;
  template: string;
  cutoff_len: number;
  max_samples: string;
  batch_size: number;
  compute_type: string;
  output_dir: string;
  predict: boolean;
  max_new_tokens: number;
  top_p: number;
  temperature: number;
}

export const useEvalFormStore = defineStore("evalForm", () => {
  const form = reactive<EvalFormState>({
    model_name: "",
    finetuning_type: "lora",
    dataset: [],
    dataset_dir: "data",
    template: "",
    cutoff_len: 2048,
    max_samples: "",
    batch_size: 4,
    compute_type: "bf16",
    output_dir: "",
    predict: true,
    max_new_tokens: 512,
    top_p: 0.7,
    temperature: 0.95,
  });

  const FALLBACK_DATASETS = [
    { label: "alpaca_zh_demo", value: "alpaca_zh_demo" },
    { label: "alpaca_en_demo", value: "alpaca_en_demo" },
    { label: "identity", value: "identity" },
  ];

  const datasetOptions = ref<{ label: string; value: string }[]>([...FALLBACK_DATASETS]);

  async function fetchDatasets(dir?: string): Promise<void> {
    try {
      const params: Record<string, string> = { format: "select" };
      if (dir) params.dir = dir;
      const data = await getJson<{ label: string; value: string }[]>("/datasets", params);
      if (data.length > 0) {
        datasetOptions.value = data;
      }
    } catch {
      // keep fallback values
    }
  }

  // dataset_dir 变化 → 重新加载数据集
  watch(
    () => form.dataset_dir,
    (dir) => {
      fetchDatasets(dir);
    },
    { immediate: true },
  );

  function updateFields(fields: Partial<EvalFormState>): void {
    Object.assign(form, fields);
  }

  function reset(): void {
    Object.assign(form, {
      model_name: "",
      finetuning_type: "lora",
      dataset: [],
      dataset_dir: "data",
      template: "",
      cutoff_len: 2048,
      max_samples: "",
      batch_size: 4,
      compute_type: "bf16",
      output_dir: "",
      predict: true,
      max_new_tokens: 512,
      top_p: 0.7,
      temperature: 0.95,
    });
  }

  function toParams(): Record<string, unknown> {
    return { ...form };
  }

  return { form, updateFields, reset, toParams, datasetOptions, fetchDatasets };
});
