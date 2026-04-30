<template>
  <div class="dataset-preview">
    <n-space vertical size="small">
      <n-space justify="space-between" align="center">
        <n-form-item :label="$t('dataset')">
          <n-select
            v-model:value="selectedDataset"
            :options="datasetOptions"
            filterable
          :placeholder="$t('dataset_select_placeholder')"
            style="min-width: 240px"
            @update:value="handleDatasetChange"
          />
        </n-form-item>
        <n-button size="small" @click="handleRefresh" :loading="loading">
          {{ $t('dataset_refresh') }}
        </n-button>
      </n-space>

      <n-data-table
        v-if="samples.length > 0"
        :columns="columns"
        :data="samples"
        :pagination="pagination"
        :bordered="false"
        :single-line="false"
        size="small"
      />

      <n-empty v-else :description="$t('dataset_empty_desc')" />
    </n-space>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive } from "vue";
import { useI18n } from "vue-i18n";
import type { DataTableColumn } from "naive-ui";

const { t } = useI18n();

const selectedDataset = ref<string | null>(null);
const loading = ref(false);
const samples = ref<Record<string, unknown>[]>([]);

const datasetOptions = [
  { label: "alpaca_zh", value: "alpaca_zh" },
  { label: "alpaca_en", value: "alpaca_en" },
  { label: "identity", value: "identity" },
];

const pagination = reactive({
  page: 1,
  pageSize: 10,
  pageSizes: [5, 10, 20, 50],
  showSizePicker: true,
});

const columns: DataTableColumn[] = [
  { title: t("dataset_col_index"), key: "index", width: 60 },
  { title: t("dataset_col_instruction"), key: "instruction", ellipsis: { tooltip: true } },
  { title: t("dataset_col_input"), key: "input", ellipsis: { tooltip: true } },
  { title: t("dataset_col_output"), key: "output", ellipsis: { tooltip: true } },
];

async function handleDatasetChange(_value: string): Promise<void> {
  loading.value = true;
  try {
    // TODO: 接入真实数据集 API，当前为 mock 数据
    const mockData = generateMockData(_value);
    samples.value = mockData;
  } finally {
    loading.value = false;
  }
}

function handleRefresh(): void {
  if (selectedDataset.value) {
    handleDatasetChange(selectedDataset.value);
  }
}

function generateMockData(dataset: string): Record<string, unknown>[] {
  const result: Record<string, unknown>[] = [];
  for (let i = 0; i < 46; i++) {
    result.push({
      index: i + 1,
      instruction: `${dataset} 样本 ${i + 1} 的指令内容`,
      input: i % 3 === 0 ? `输入参数示例 #${i + 1}` : "",
      output: `这是数据集 ${dataset} 的第 ${i + 1} 条生成结果`,
    });
  }
  return result;
}
</script>

<style scoped>
.dataset-preview {
  padding: var(--spacing-3) 0;
}
</style>
