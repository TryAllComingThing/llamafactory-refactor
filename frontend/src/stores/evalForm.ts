import { defineStore } from "pinia";
import { reactive } from "vue";

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
  });

  const datasetOptions = reactive<{ label: string; value: string }[]>([
    { label: "alpaca_zh", value: "alpaca_zh" },
    { label: "alpaca_en", value: "alpaca_en" },
    { label: "identity", value: "identity" },
  ]);

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
    });
  }

  function toParams(): Record<string, unknown> {
    return { ...form };
  }

  return { form, updateFields, reset, toParams, datasetOptions };
});
