<template>
  <div class="export-view">
    <!-- Section: Export Settings -->
    <div class="form-section">
      <span class="section-label">{{ $t('export_title') }}</span>
      <n-grid :cols="5" :x-gap="8" :y-gap="6">
        <n-grid-item>
          <n-form-item :label="$t('export_size')" label-placement="top" size="tiny">
            <n-input-number v-model:value="form.export_size" :min="1" :max="100" size="tiny" />
            <n-slider v-model:value="form.export_size" :min="1" :max="100" :step="1" :tooltip="false" />
          </n-form-item>
        </n-grid-item>
        <n-grid-item>
          <n-form-item :label="$t('export_quantization_bit')" label-placement="top" size="tiny">
            <n-select v-model:value="form.export_quantization_bit" :options="quantOptions" size="tiny" />
          </n-form-item>
        </n-grid-item>
        <n-grid-item>
          <n-form-item :label="$t('export_quantization_dataset')" label-placement="top" size="tiny">
            <n-input v-model:value="form.export_quantization_dataset" placeholder="data/c4_demo.jsonl" size="tiny" />
          </n-form-item>
        </n-grid-item>
        <n-grid-item>
          <n-form-item :label="$t('export_device')" label-placement="top" size="tiny">
            <n-radio-group v-model:value="form.export_device">
              <n-radio value="cpu">cpu</n-radio>
              <n-radio value="auto">auto</n-radio>
            </n-radio-group>
          </n-form-item>
        </n-grid-item>
        <n-grid-item>
          <n-form-item :label="$t('export_legacy_format')" label-placement="top" size="tiny">
            <n-checkbox v-model:checked="form.export_legacy_format" />
          </n-form-item>
        </n-grid-item>
      </n-grid>
    </div>

    <!-- Section: Output -->
    <div class="form-section">
      <span class="section-label">{{ $t('output') }}</span>
      <n-grid :cols="3" :x-gap="8" :y-gap="6">
        <n-grid-item>
          <n-form-item :label="$t('export_dir')" label-placement="top" size="tiny">
            <n-input v-model:value="form.export_dir" :placeholder="$t('export_placeholder')" size="tiny" />
          </n-form-item>
        </n-grid-item>
        <n-grid-item>
          <n-form-item :label="$t('export_hub_model_id')" label-placement="top" size="tiny">
            <n-input v-model:value="form.export_hub_model_id" :placeholder="$t('export_hub_placeholder')" size="tiny" />
          </n-form-item>
        </n-grid-item>
        <n-grid-item>
          <n-form-item :label="$t('extra_args')" label-placement="top" size="tiny">
            <n-input v-model:value="form.extra_args" placeholder='{}' size="tiny" />
          </n-form-item>
        </n-grid-item>
      </n-grid>
    </div>

    <!-- Export Button -->
    <div class="button-section">
      <n-space style="width: 100%">
        <n-button
          type="primary"
          size="large"
          @click="handleExport"
          style="flex: 1"
        >
          {{ $t('export_btn') }}
        </n-button>
        <n-button
          v-if="exportRunId"
          type="error"
          size="large"
          @click="handleAbort"
        >
          {{ $t('stop_btn') }}
        </n-button>
      </n-space>
    </div>

    <!-- Output Log -->
    <div v-if="exporting || exportOutput" class="form-section">
      <div v-if="exporting" class="export-monitor">
        <n-progress
          type="line"
          :percentage="exportProgress"
          :indicator-placement="'inside'"
          processing
        />
      </div>
      <div v-if="exportOutput" class="export-output">{{ exportOutput }}</div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onBeforeUnmount } from "vue";
import { useI18n } from "vue-i18n";
import { useMessage } from "naive-ui";
import { useExportFormStore } from "@/stores/exportForm";
import { useSessionStore } from "@/stores/session";
import { startExport, abortExport } from "@/api/export";

const { t } = useI18n();
const message = useMessage();
const form = useExportFormStore().form;
const session = useSessionStore();

const exporting = ref(false);
const exportRunId = ref("");
const exportProgress = ref(0);
const exportOutput = ref("");
let closeWs: (() => void) | null = null;

const quantOptions = [
  { label: "None", value: "none" },
  { label: "8bit", value: "8" },
  { label: "4bit", value: "4" },
  { label: "3bit", value: "3" },
  { label: "2bit", value: "2" },
];

function connectExportWs(runId: string): void {
  const protocol = window.location.protocol === "https:" ? "wss:" : "ws:";
  const wsUrl = `${protocol}//${window.location.host}/ws/train/${runId}`;
  const ws = new WebSocket(wsUrl);
  ws.onmessage = (event) => {
    const data = JSON.parse(event.data);
    if (data.type === "log") {
      exportOutput.value = data.text;
    } else if (data.type === "progress") {
      exportProgress.value = data.percentage ?? exportProgress.value;
    } else if (data.type === "train:complete") {
      exporting.value = false;
      exportProgress.value = data.status === "success" ? 100 : exportProgress.value;
      ws.close();
    }
  };
  ws.onerror = () => {
    exporting.value = false;
  };
  closeWs = () => ws.close();
}

async function handleExport(): Promise<void> {
  exporting.value = true;
  exportProgress.value = 0;
  exportOutput.value = "";

  try {
    const params: Record<string, unknown> = {
      model_name: session.modelName,
      model_path: session.modelPath,
      finetuning_type: session.finetuningType,
      template: session.template,
      checkpoint_path: session.checkpointPath,
      export_size: form.export_size,
      export_quantization_bit: form.export_quantization_bit,
      export_quantization_dataset: form.export_quantization_dataset,
      export_device: form.export_device,
      export_legacy_format: form.export_legacy_format,
      export_dir: form.export_dir,
      export_hub_model_id: form.export_hub_model_id,
      ...JSON.parse(form.extra_args || "{}"),
    };

    const result = await startExport(params);
    exportRunId.value = result.run_id;
    exportProgress.value = 10;
    message.success(t("export_started"));
    connectExportWs(result.run_id);
  } catch {
    message.error(t("operation_failed"));
    exporting.value = false;
  }
}

async function handleAbort(): Promise<void> {
  try {
    await abortExport();
    closeWs?.();
    exportRunId.value = "";
    exporting.value = false;
    message.info(t("abort_sent"));
  } catch {
    message.error(t("operation_failed"));
  }
}

onBeforeUnmount(() => {
  closeWs?.();
});
</script>

<style scoped>
.export-view {
  max-width: none;
  padding: 0 var(--spacing-6);
}

.form-section {
  margin-bottom: var(--spacing-4);
}

.section-label {
  font-size: var(--font-size-sm);
  font-weight: var(--font-weight-medium);
  color: var(--text-primary);
  display: block;
  margin-bottom: var(--spacing-3);
}

.button-section {
  margin-bottom: var(--spacing-4);
}

.export-monitor {
  margin-top: var(--spacing-3);
}

.export-output {
  margin-top: var(--spacing-3);
  padding: var(--spacing-3);
  background: var(--bg-elevated);
  border-radius: var(--radius-sm);
  font-family: var(--font-mono);
  font-size: var(--font-size-sm);
  white-space: pre-wrap;
  max-height: 300px;
  overflow-y: auto;
}
</style>
