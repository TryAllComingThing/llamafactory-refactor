<template>
  <div class="model-config">
    <!-- Row 1: 模型名称、模型路径、模型下载源 -->
    <n-grid :cols="7" :x-gap="8" :y-gap="6">
      <n-grid-item :span="2">
        <n-form-item :label="$t('model_name')" label-placement="top" size="tiny">
          <n-select
            v-model:value="session.modelName"
            :options="modelOptions"
            :placeholder="$t('model_name_placeholder')"
            filterable
            size="tiny"
            clearable
          />
        </n-form-item>
      </n-grid-item>
      <n-grid-item :span="3">
        <n-form-item :label="$t('model_path')" label-placement="top" size="tiny">
          <n-input v-model:value="session.modelPath" :placeholder="$t('model_path_placeholder')" size="tiny" />
        </n-form-item>
      </n-grid-item>
      <n-grid-item :span="2">
        <n-form-item :label="$t('hub_name')" label-placement="top" size="tiny">
          <n-select v-model:value="session.hubName" :options="hubOptions" size="tiny" />
        </n-form-item>
      </n-grid-item>
    </n-grid>

    <!-- Row 2: 微调方法、检查点路径 -->
    <n-grid :cols="5" :x-gap="8" :y-gap="6" style="margin-top:6px">
      <n-grid-item :span="2">
        <n-form-item :label="$t('finetuning_type')" label-placement="top" size="tiny">
          <n-select v-model:value="session.finetuningType" :options="ftOptions" size="tiny" />
        </n-form-item>
      </n-grid-item>
      <n-grid-item :span="3">
        <n-form-item :label="$t('checkpoint_path')" label-placement="top" size="tiny">
          <n-select
            v-model:value="session.checkpointPath"
            :options="checkpointOptions"
            multiple
            filterable
            :placeholder="$t('optional')"
            clearable
            size="tiny"
            @focus="loadCheckpoints"
          />
        </n-form-item>
      </n-grid-item>
    </n-grid>

    <!-- Row 3: 量化等级、量化方法、对话模板、RoPE 插值方法、加速方式 -->
    <n-grid :cols="5" :x-gap="8" :y-gap="6" style="margin-top:6px">
      <n-grid-item>
        <n-form-item :label="$t('quantization_bit')" label-placement="top" size="tiny">
          <n-select v-model:value="session.quantizationBit" :options="quantBitOptions" size="tiny" />
        </n-form-item>
      </n-grid-item>
      <n-grid-item>
        <n-form-item :label="$t('quantization_method')" label-placement="top" size="tiny">
          <n-select v-model:value="session.quantizationMethod" :options="quantMethodOptions" size="tiny" />
        </n-form-item>
      </n-grid-item>
      <n-grid-item>
        <n-form-item :label="$t('template')" label-placement="top" size="tiny">
          <n-select
            v-model:value="session.template"
            :options="templateOptions"
            :placeholder="$t('auto_detect')"
            clearable
            size="tiny"
          />
        </n-form-item>
      </n-grid-item>
      <n-grid-item>
        <n-form-item :label="$t('rope_scaling')" label-placement="top" size="tiny">
          <n-select v-model:value="session.ropeScaling" :options="ropeOptions" size="tiny" />
        </n-form-item>
      </n-grid-item>
      <n-grid-item>
        <n-form-item :label="$t('booster')" label-placement="top" size="tiny">
          <n-select v-model:value="session.booster" :options="boosterOptions" size="tiny" />
        </n-form-item>
      </n-grid-item>
    </n-grid>
  </div>
</template>

<script setup lang="ts">
import { ref, watch, onMounted } from "vue";
import { useSessionStore } from "@/stores/session";
import { getJson } from "@/api/client";

const session = useSessionStore();

interface OptionItem { label: string; value: string }

const modelOptions = ref<OptionItem[]>([]);
const templateOptions = ref<OptionItem[]>([]);
const checkpointOptions = ref<OptionItem[]>([]);
const allModels = ref<OptionItem[]>([]);

const hubOptions: OptionItem[] = [
  { label: "Hugging Face", value: "huggingface" },
  { label: "ModelScope", value: "modelscope" },
  { label: "OpenMind", value: "openmind" },
];

const ftOptions: OptionItem[] = [
  { label: "LoRA", value: "lora" },
  { label: "QLoRA", value: "qlora" },
  { label: "Freeze", value: "freeze" },
  { label: "Full", value: "full" },
  { label: "BAdam", value: "badam" },
];

const quantBitOptions: OptionItem[] = [
  { label: "None", value: "none" },
  { label: "8bit", value: "8" },
  { label: "4bit", value: "4" },
];

const quantMethodOptions: OptionItem[] = [
  { label: "bnb", value: "bnb" },
  { label: "hqq", value: "hqq" },
  { label: "eetq", value: "eetq" },
];

const ropeOptions: OptionItem[] = [
  { label: "None", value: "none" },
  { label: "Linear", value: "linear" },
  { label: "Dynamic", value: "dynamic" },
  { label: "YaRN", value: "yarn" },
  { label: "LLaMA3", value: "llama3" },
];

const boosterOptions: OptionItem[] = [
  { label: "Auto", value: "auto" },
  { label: "FlashAttn2", value: "flashattn2" },
  { label: "Unsloth", value: "unsloth" },
  { label: "Liger Kernel", value: "liger_kernel" },
];

async function loadModels(): Promise<void> {
  try {
    const data = await getJson<{ model_name: string; model_path: string; template: string }[]>("/models");
    allModels.value = data.map((m) => ({
      label: m.model_name,
      value: m.model_name,
    }));
    modelOptions.value = allModels.value;
    if (!session.modelName && allModels.value.length > 0) {
      session.modelName = allModels.value[0].value;
    }
  } catch {
    modelOptions.value = allModels.value;
  }
}

async function loadTemplates(): Promise<void> {
  try {
    const data = await getJson<string[]>("/templates");
    templateOptions.value = data.map((t) => ({ label: t, value: t }));
  } catch {
    templateOptions.value = [];
  }
}

async function loadCheckpoints(): Promise<void> {
  if (!session.modelName) {
    checkpointOptions.value = [];
    return;
  }
  try {
    const data = await getJson<string[]>("/checkpoints", {
      model: session.modelName,
      ft: session.finetuningType,
    });
    checkpointOptions.value = data.map((c) => ({ label: c, value: c }));
  } catch {
    checkpointOptions.value = [];
  }
}

watch(() => session.modelName, async (name) => {
  if (!name) return;
  try {
    const data = await getJson<{
      model_path: string;
      template: string;
      checkpoints: string[];
    }>("/on-model-change", {
      model_name: name,
      finetuning_type: session.finetuningType,
    });

    session.modelPath = data.model_path ?? "";
    session.template = data.template ?? "";
    if (data.checkpoints?.length) {
      checkpointOptions.value = data.checkpoints.map((c) => ({ label: c, value: c }));
    }
  } catch {
    // API not available yet
  }
});

watch(() => session.finetuningType, () => {
  loadCheckpoints();
});

onMounted(() => {
  loadModels();
  loadTemplates();
  loadCheckpoints();
});
</script>

<style scoped>
.model-config {
  margin: var(--spacing-4) var(--spacing-6);
  padding: var(--spacing-6) var(--spacing-6) var(--spacing-5);
  border-bottom: 1px solid var(--border-default);
}
</style>
