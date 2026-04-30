<template>
  <n-card :title="$t('model_config')" class="model-config-card" size="small">
    <n-grid :cols="3" :x-gap="12" :y-gap="8">
      <n-grid-item>
        <n-form-item :label="$t('model_name')">
          <n-select
            v-model:value="session.modelName"
            filterable
            :placeholder="$t('choose_model')"
            :options="[]"
            clearable
          />
        </n-form-item>
      </n-grid-item>
      <n-grid-item>
        <n-form-item :label="$t('model_path')">
          <n-input v-model:value="session.modelPath" :placeholder="$t('model_path_placeholder')" />
        </n-form-item>
      </n-grid-item>
      <n-grid-item>
        <n-form-item :label="$t('finetuning_type')">
          <n-select
            v-model:value="session.finetuningType"
            :options="ftOptions"
          />
        </n-form-item>
      </n-grid-item>
      <n-grid-item>
        <n-form-item :label="$t('template')">
          <n-select
            v-model:value="session.template"
            :options="[]"
            :placeholder="$t('auto_detect')"
            clearable
          />
        </n-form-item>
      </n-grid-item>
      <n-grid-item>
        <n-form-item :label="$t('quantization_bit')">
          <n-select
            v-model:value="session.quantizedBit"
            :options="quantOptions"
          />
        </n-form-item>
      </n-grid-item>
      <n-grid-item>
        <n-form-item :label="$t('checkpoint_path')">
          <n-select
            v-model:value="session.checkpointPath"
            :options="[]"
            :placeholder="$t('optional')"
            clearable
          />
        </n-form-item>
      </n-grid-item>
    </n-grid>
  </n-card>
</template>

<script setup lang="ts">
import { useSessionStore } from "@/stores/session";

const session = useSessionStore();

const ftOptions = [
  { label: "LoRA", value: "lora" },
  { label: "QLoRA", value: "qlora" },
  { label: "Freeze", value: "freeze" },
  { label: "Full", value: "full" },
  { label: "BAdam", value: "badam" },
];

const quantOptions = [
  { label: "无", value: "none" },
  { label: "4bit", value: "4bit" },
  { label: "8bit", value: "8bit" },
];
</script>

<style scoped>
.model-config-card {
  margin-bottom: var(--spacing-5);
}
</style>
