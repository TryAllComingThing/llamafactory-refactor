<template>
  <div class="eval-view">
    <ModelConfig />

    <n-card title="评估参数" size="small">
      <n-grid :cols="2" :x-gap="16" :y-gap="12">
        <n-grid-item>
          <n-form-item :label="$t('dataset')">
            <n-select
              v-model:value="store.form.dataset"
              multiple
              filterable
              placeholder="选择评估数据集"
              :options="store.datasetOptions"
            />
          </n-form-item>
        </n-grid-item>
        <n-grid-item>
          <n-form-item :label="$t('cutoff_len')">
            <n-input-number v-model:value="store.form.cutoff_len" :min="64" :max="8192" :step="64" />
          </n-form-item>
        </n-grid-item>
        <n-grid-item>
          <n-form-item :label="$t('max_samples')">
            <n-input v-model:value="store.form.max_samples" placeholder="全部" />
          </n-form-item>
        </n-grid-item>
        <n-grid-item>
          <n-form-item :label="$t('batch_size')">
            <n-input-number v-model:value="store.form.batch_size" :min="1" :max="128" />
          </n-form-item>
        </n-grid-item>
        <n-grid-item>
          <n-form-item :label="$t('compute_type')">
            <n-select v-model:value="store.form.compute_type" :options="computeOptions" />
          </n-form-item>
        </n-grid-item>
        <n-grid-item>
          <n-form-item :label="$t('predict')">
            <n-switch v-model:value="store.form.predict" />
          </n-form-item>
        </n-grid-item>
        <n-grid-item span="2">
          <n-form-item :label="$t('output_dir')">
            <n-input v-model:value="store.form.output_dir" placeholder="默认输出路径" />
          </n-form-item>
        </n-grid-item>
      </n-grid>

      <n-space justify="center" size="large" class="eval-actions">
        <n-button type="primary" size="large" @click="handleStart">
          {{ $t("start_btn") }}
        </n-button>
        <n-button size="large" @click="handlePreview">
          {{ $t("cmd_preview_btn") }}
        </n-button>
      </n-space>
    </n-card>
  </div>
</template>

<script setup lang="ts">
import { useMessage } from "naive-ui";
import { useEvalFormStore } from "@/stores/evalForm";
import ModelConfig from "@/components/common/ModelConfig.vue";

const store = useEvalFormStore();
const message = useMessage();

const computeOptions = [
  { label: "bf16", value: "bf16" },
  { label: "fp16", value: "fp16" },
  { label: "fp32", value: "fp32" },
  { label: "auto", value: "auto" },
];

function handleStart(): void {
  message.info("评估启动（待 API 接入）");
}

function handlePreview(): void {
  message.info("命令预览（待 API 接入）");
}
</script>

<style scoped>
.eval-view {
  max-width: 960px;
}

.eval-actions {
  margin-top: var(--spacing-6);
}
</style>
