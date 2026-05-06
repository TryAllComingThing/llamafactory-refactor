import { defineStore } from "pinia";
import { ref, watch } from "vue";
import { getJson } from "@/api/client";
import { useTrainFormStore } from "@/stores/trainForm";

const CACHE_KEY = "session_cache";

interface SystemStatus {
  status: "idle" | "training" | "evaluating" | "model_loaded";
  model_name: string;
  model_path: string;
  finetuning_type: string;
  template: string;
  quantized_bit: string;
  checkpoint_path: string;
  output_dir: string;
}

export const useSessionStore = defineStore("session", () => {
  const darkMode = ref(false);
  const sidebarCollapsed = ref(false);
  const lang = ref("zh");
  const modelName = ref("");
  const modelPath = ref("");
  const hubName = ref("huggingface");
  const finetuningType = ref("lora");
  const checkpointPath = ref<string[]>([]);
  const quantizationBit = ref("none");
  const quantizationMethod = ref("bnb");
  const template = ref("default");
  const ropeScaling = ref("none");
  const booster = ref("auto");
  const trainRunId = ref("");

  function restoreFromCache(): void {
    try {
      const cached = localStorage.getItem(CACHE_KEY);
      if (cached) {
        const data = JSON.parse(cached);
        modelName.value = data.model_name || "";
        modelPath.value = data.model_path || "";
        hubName.value = data.hub_name || "huggingface";
        finetuningType.value = data.finetuning_type || "lora";
        checkpointPath.value = data.checkpoint_path || [];
        quantizationBit.value = data.quantized_bit || "none";
        quantizationMethod.value = data.quantization_method || "bnb";
        template.value = data.template || "default";
        ropeScaling.value = data.rope_scaling || "none";
        booster.value = data.booster || "auto";
        lang.value = data.lang ?? "zh";
        sidebarCollapsed.value = data.sidebar_collapsed ?? false;
        trainRunId.value = data.train_run_id ?? "";
      }
    } catch {
      localStorage.removeItem(CACHE_KEY);
    }
  }

  function persistToCache(): void {
    const data = {
      model_name: modelName.value,
      model_path: modelPath.value,
      hub_name: hubName.value,
      finetuning_type: finetuningType.value,
      checkpoint_path: checkpointPath.value,
      quantization_bit: quantizationBit.value,
      quantization_method: quantizationMethod.value,
      template: template.value,
      rope_scaling: ropeScaling.value,
      booster: booster.value,
      lang: lang.value,
      sidebar_collapsed: sidebarCollapsed.value,
      train_run_id: trainRunId.value,
    };
    try {
      localStorage.setItem(CACHE_KEY, JSON.stringify(data));
    } catch {
      // localStorage full or unavailable
    }
  }

  async function recoverFromServer(): Promise<void> {
    try {
      const status = await getJson<SystemStatus>("/status");
      modelName.value = status.model_name || "";
      modelPath.value = status.model_path || "";
      finetuningType.value = status.finetuning_type || "lora";
      template.value = status.template || "";
      quantizationBit.value = status.quantized_bit || "none";
      checkpointPath.value = status.checkpoint_path ? [status.checkpoint_path] : [];

      if (status.output_dir) {
        const trainForm = useTrainFormStore();
        trainForm.updateField("output_dir", status.output_dir);
      }

      persistToCache();
    } catch {
      // API not available, keep cached values
    }
  }

  restoreFromCache();

  if (typeof window !== "undefined") {
    setTimeout(() => recoverFromServer(), 0);
  }

  function toggleDarkMode(): void {
    darkMode.value = !darkMode.value;
  }

  function toggleSidebar(): void {
    sidebarCollapsed.value = !sidebarCollapsed.value;
    persistToCache();
  }

  function setModel(info: {
    model_name: string;
    model_path: string;
    template: string;
    finetuning_type: string;
    quantized_bit: string;
  }): void {
    modelName.value = info.model_name;
    modelPath.value = info.model_path;
    template.value = info.template;
    finetuningType.value = info.finetuning_type;
    quantizationBit.value = info.quantized_bit;
    persistToCache();
  }

  watch(modelName, async (name) => {
    if (!name) return;
    try {
      const data = await getJson<{
        model_path: string;
        template: string;
        checkpoints: string[];
        quantization_available: string;
        output_dirs: string[];
      }>("/on-model-change", { model_name: name, finetuning_type: finetuningType.value });

      modelPath.value = data.model_path;
      template.value = data.template;
      if (data.checkpoints?.length) {
        checkpointPath.value = data.checkpoints;
      }

      const trainForm = useTrainFormStore();
      if (data.output_dirs?.[0]) {
        trainForm.updateField("output_dir", data.output_dirs[0]);
      }

      persistToCache();
    } catch {
      // API not available yet
    }
  });

  return {
    darkMode,
    sidebarCollapsed,
    lang,
    modelName,
    modelPath,
    hubName,
    finetuningType,
    checkpointPath,
    quantizationBit,
    quantizationMethod,
    template,
    ropeScaling,
    booster,
    trainRunId,
    toggleDarkMode,
    toggleSidebar,
    setModel,
    recoverFromServer,
    persistToCache,
  };
});
