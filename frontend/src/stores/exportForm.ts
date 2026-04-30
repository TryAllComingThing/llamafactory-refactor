import { defineStore } from "pinia";
import { reactive } from "vue";

export interface ExportFormState {
  export_size: number;
  export_quantization_bit: string;
  export_quantization_dataset: string;
  export_device: string;
  export_legacy_format: boolean;
  export_dir: string;
  export_hub_model_id: string;
  extra_args: string;
}

export const DEFAULT_EXPORT_FORM: ExportFormState = {
  export_size: 5,
  export_quantization_bit: "none",
  export_quantization_dataset: "data/c4_demo.jsonl",
  export_device: "auto",
  export_legacy_format: false,
  export_dir: "",
  export_hub_model_id: "",
  extra_args: "{}",
};

export const useExportFormStore = defineStore("exportForm", () => {
  const form = reactive<ExportFormState>({ ...DEFAULT_EXPORT_FORM });

  function reset(): void {
    Object.assign(form, { ...DEFAULT_EXPORT_FORM });
  }

  function toParams(): Record<string, unknown> {
    return { ...form };
  }

  return { form, reset, toParams };
});
