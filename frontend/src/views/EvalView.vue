<template>
  <div class="eval-view">
    <!-- Section: Data -->
    <div class="form-section">
      <span class="section-label">{{ $t('data') }}</span>
      <n-grid :cols="5" :x-gap="8" :y-gap="6">
        <n-grid-item span="2">
          <n-form-item :label="$t('dataset_dir')" label-placement="top" size="tiny">
            <n-input v-model:value="store.form.dataset_dir" size="tiny" />
          </n-form-item>
        </n-grid-item>
        <n-grid-item span="3">
          <n-form-item :label="$t('dataset')" label-placement="top" size="tiny">
            <div class="dataset-row">
              <n-select
                v-model:value="store.form.dataset"
                multiple
                filterable
                :placeholder="$t('dataset_select_placeholder')"
                :options="store.datasetOptions"
                class="dataset-select"
                size="tiny"
              />
              <n-button size="tiny" :disabled="!store.form.dataset.length" @click="showPreview = true">{{ $t('data_preview_btn') }}</n-button>
            </div>
          </n-form-item>
        </n-grid-item>
      </n-grid>
    </div>

    <!-- Section: Parameters -->
    <div class="form-section">
      <span class="section-label">{{ $t('eval_params') }}</span>
      <n-grid :cols="4" :x-gap="8" :y-gap="6">
        <n-grid-item>
          <n-form-item :label="$t('cutoff_len')" label-placement="top" size="tiny">
            <n-input-number v-model:value="store.form.cutoff_len" :min="4" :max="131072" :step="64" size="tiny" />
          </n-form-item>
        </n-grid-item>
        <n-grid-item>
          <n-form-item :label="$t('max_samples')" label-placement="top" size="tiny">
            <n-input v-model:value="store.form.max_samples" :placeholder="$t('all_samples')" size="tiny" />
          </n-form-item>
        </n-grid-item>
        <n-grid-item>
          <n-form-item :label="$t('batch_size')" label-placement="top" size="tiny">
            <n-input-number v-model:value="store.form.batch_size" :min="1" :max="128" size="tiny" />
          </n-form-item>
        </n-grid-item>
        <n-grid-item>
          <n-form-item :label="$t('predict')" label-placement="top" size="tiny">
            <n-switch v-model:value="store.form.predict" />
          </n-form-item>
        </n-grid-item>
      </n-grid>

      <n-grid :cols="4" :x-gap="8" :y-gap="6" style="margin-top:6px">
        <n-grid-item>
          <n-form-item :label="$t('max_new_tokens')" label-placement="top" size="tiny">
            <n-input-number v-model:value="store.form.max_new_tokens" :min="8" :max="4096" :step="16" size="tiny" />
          </n-form-item>
        </n-grid-item>
        <n-grid-item>
          <n-form-item :label="$t('top_p')" label-placement="top" size="tiny">
            <n-input-number v-model:value="store.form.top_p" :min="0.01" :max="1" :step="0.01" size="tiny" />
          </n-form-item>
        </n-grid-item>
        <n-grid-item>
          <n-form-item :label="$t('temperature')" label-placement="top" size="tiny">
            <n-input-number v-model:value="store.form.temperature" :min="0.01" :max="1.5" :step="0.01" size="tiny" />
          </n-form-item>
        </n-grid-item>
      </n-grid>
    </div>

    <!-- Section: Output -->
    <div class="form-section">
      <span class="section-label">{{ $t('output') }}</span>
      <n-grid :cols="2" :x-gap="8" :y-gap="6">
        <n-grid-item>
          <n-form-item :label="$t('output_dir')" label-placement="top" size="tiny">
            <n-input v-model:value="store.form.output_dir" :placeholder="$t('export_placeholder')" size="tiny" />
          </n-form-item>
        </n-grid-item>
      </n-grid>

      <div class="action-bar">
        <n-space size="small">
          <n-button size="tiny" @click="handlePreview">{{ $t('cmd_preview_btn') }}</n-button>
        </n-space>
        <n-space size="small">
          <n-button v-if="evalRunId" size="tiny" type="error" @click="handleStop">{{ $t('stop_btn') }}</n-button>
          <n-button size="tiny" type="primary" @click="handleStart">{{ $t('start_btn') }}</n-button>
        </n-space>
      </div>

      <div v-if="evalRunId" class="eval-monitor">
        <n-progress
          v-if="progress > 0"
          type="line"
          :percentage="progress"
          :indicator-placement="'inside'"
          processing
        />
        <div v-if="outputText" class="eval-output">{{ outputText }}</div>
      </div>
    </div>

    <!-- Dataset Preview Modal -->
    <n-modal v-model:show="showPreview" :title="$t('data_preview_btn')" preset="card" style="width:900px">
      <DatasetPreview
        :dataset="store.form.dataset"
        :dataset-dir="store.form.dataset_dir"
        @close="showPreview = false"
      />
    </n-modal>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from "vue";
import { useI18n } from "vue-i18n";
import { useMessage } from "naive-ui";
import { useEvalFormStore } from "@/stores/evalForm";
import { useSessionStore } from "@/stores/session";
import { startEval } from "@/api/eval";
import { previewTrain } from "@/api/train";
import { abortTrain } from "@/api/train";
import DatasetPreview from "@/components/common/DatasetPreview.vue";

const { t } = useI18n();
const store = useEvalFormStore();
const session = useSessionStore();
const message = useMessage();
const evalRunId = ref("");
const showPreview = ref(false);
const progress = ref(0);
const outputText = ref("");

function buildEvalParams(): Record<string, unknown> {
  return {
    ...store.toParams(),
    model_name: session.modelName,
    model_path: session.modelPath,
    finetuning_type: session.finetuningType,
    template: session.template,
    quantized_bit: session.quantizationBit,
    checkpoint_path: session.checkpointPath,
  };
}

async function handleStart(): Promise<void> {
  try {
    const result = await startEval(buildEvalParams());
    evalRunId.value = result.run_id;
    outputText.value = "";
    progress.value = 0;
    message.success(t("eval_started"));
  } catch {
    message.error(t("operation_failed"));
  }
}

async function handlePreview(): Promise<void> {
  try {
    const params = buildEvalParams();
    const result = await previewTrain({ ...params, do_train: false });
    message.info(result.command.join("\n"));
  } catch {
    message.error(t("operation_failed"));
  }
}

onMounted(() => {
  store.fetchDatasets();
});

async function handleStop(): Promise<void> {
  try {
    await abortTrain();
    evalRunId.value = "";
    message.info(t("abort_sent"));
  } catch {
    message.error(t("operation_failed"));
  }
}
</script>

<style scoped>
.eval-view {
  max-width: none;
  padding: 0 var(--spacing-6);
}

.form-section {
  margin-bottom: var(--spacing-4);
}

.action-bar {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-top: var(--spacing-3);
  padding-top: var(--spacing-3);
  border-top: 1px solid var(--border-default);
}

.eval-monitor {
  margin-top: var(--spacing-4);
}

.eval-output {
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
