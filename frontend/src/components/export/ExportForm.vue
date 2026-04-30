<template>
  <n-card :title="$t('export_title')" size="small">
    <n-grid :cols="2" :x-gap="16" :y-gap="12">
      <n-grid-item>
        <n-form-item :label="$t('export_size')">
          <n-slider
            v-model:value="form.export_size"
            :min="1"
            :max="100"
            :step="1"
          />
        </n-form-item>
      </n-grid-item>
      <n-grid-item>
        <n-form-item :label="$t('export_quantization_bit')">
          <n-select v-model:value="form.export_quantization_bit" :options="quantOptions" />
        </n-form-item>
      </n-grid-item>
      <n-grid-item>
        <n-form-item :label="$t('export_quantization_dataset')">
          <n-input v-model:value="form.export_quantization_dataset" placeholder="data/c4_demo.jsonl" />
        </n-form-item>
      </n-grid-item>
      <n-grid-item>
        <n-form-item :label="$t('export_device')">
          <n-radio-group v-model:value="form.export_device">
            <n-radio value="cpu">CPU</n-radio>
            <n-radio value="auto">Auto</n-radio>
          </n-radio-group>
        </n-form-item>
      </n-grid-item>
      <n-grid-item>
        <n-form-item :label="$t('export_legacy_format')">
          <n-switch v-model:value="form.export_legacy_format" />
        </n-form-item>
      </n-grid-item>
      <n-grid-item>
        <n-form-item :label="$t('export_dir')">
          <n-input v-model:value="form.export_dir" :placeholder="$t('export_placeholder')" />
        </n-form-item>
      </n-grid-item>
      <n-grid-item span="2">
        <n-form-item :label="$t('export_hub_model_id')">
          <n-input v-model:value="form.export_hub_model_id" :placeholder="$t('export_hub_placeholder')" />
        </n-form-item>
      </n-grid-item>
      <n-grid-item span="2">
        <n-form-item :label="$t('extra_args')">
          <n-input v-model:value="form.extra_args" type="textarea" :rows="2" placeholder='{}' />
        </n-form-item>
      </n-grid-item>
    </n-grid>

    <n-space justify="center" size="large" class="export-actions">
      <n-button type="primary" size="large" @click="handleExport">
        {{ $t("export_btn") }}
      </n-button>
      <n-button size="large" @click="handlePreview">
        {{ $t("cmd_preview_btn") }}
      </n-button>
    </n-space>
  </n-card>
</template>

<script setup lang="ts">
import { useI18n } from "vue-i18n";
import { useMessage } from "naive-ui";
import { useExportFormStore } from "@/stores/exportForm";

const { t } = useI18n();
const message = useMessage();
const form = useExportFormStore().form;

const quantOptions = [
  { label: "None", value: "none" },
  { label: "8bit", value: "8" },
  { label: "4bit", value: "4" },
  { label: "3bit", value: "3" },
  { label: "2bit", value: "2" },
];

function handleExport(): void {
  message.info(t("export_started"));
}

function handlePreview(): void {
  message.info(t("cmd_preview_pending"));
}
</script>

<style scoped>
.export-actions {
  margin-top: var(--spacing-6);
}
</style>
