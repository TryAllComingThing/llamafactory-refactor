<template>
  <div class="dataset-preview">
    <div class="preview-toolbar">
      <n-select
        v-model:value="selectedDataset"
        :options="datasetOptions"
        filterable
        :placeholder="$t('dataset_select_placeholder')"
        size="tiny"
        class="toolbar-select"
        @update:value="handleDatasetChange"
      />
      <span class="preview-count">{{ $t('dataset') }}: {{ totalSamples }}</span>
      <n-button size="tiny" @click="handlePrev" :disabled="currentPage <= 1">
        {{ $t('prev_btn') }}
      </n-button>
      <n-button size="tiny" @click="handleNext" :disabled="currentPage * pageSize >= totalSamples">
        {{ $t('next_btn') }}
      </n-button>
      <n-button size="tiny" @click="handleRefresh" :loading="loading">
        {{ $t('dataset_refresh') }}
      </n-button>
      <n-button size="tiny" @click="$emit('close')">
        {{ $t('close_btn') }}
      </n-button>
    </div>

    <n-data-table
      v-if="samples.length > 0"
      :columns="columns"
      :data="samples"
      :bordered="false"
      :single-line="false"
      size="tiny"
      max-height="400"
      class="preview-table"
    />

    <n-empty v-else :description="$t('dataset_empty_desc')" size="tiny" />
  </div>
</template>

<script setup lang="ts">
import { ref, computed, watch } from "vue";
import { useI18n } from "vue-i18n";
import { getJson } from "@/api/client";
import type { DataTableColumn } from "naive-ui";

const { t } = useI18n();

const props = defineProps<{
  dataset: string[];
  datasetDir: string;
}>();

defineEmits<{
  close: [];
}>();

interface PreviewResult {
  total: number;
  page: number;
  page_size: number;
  samples: Record<string, unknown>[];
}

const selectedDataset = ref<string | null>(null);
const loading = ref(false);
const samples = ref<Record<string, unknown>[]>([]);
const totalSamples = ref(0);
const currentPage = ref(1);
const pageSize = ref(10);

const datasetOptions = computed(() =>
  props.dataset.map((d) => ({ label: d, value: d }))
);

// Auto-select first dataset and load preview on mount
watch(datasetOptions, (opts) => {
  if (opts.length > 0 && !selectedDataset.value) {
    selectedDataset.value = opts[0].value;
    fetchData();
  }
}, { immediate: true });

const columns: DataTableColumn[] = [
  { title: t("dataset_col_index"), key: "index", width: 60 },
  { title: t("dataset_col_instruction"), key: "instruction", ellipsis: { tooltip: true } },
  { title: t("dataset_col_input"), key: "input", ellipsis: { tooltip: true } },
  { title: t("dataset_col_output"), key: "output", ellipsis: { tooltip: true } },
];

async function fetchData(): Promise<void> {
  if (!selectedDataset.value) return;
  loading.value = true;
  try {
    const data = await getJson<PreviewResult>("/datasets/preview", {
      dataset: selectedDataset.value,
      dataset_dir: props.datasetDir,
      page: currentPage.value,
      page_size: pageSize.value,
    });
    totalSamples.value = data.total;
    samples.value = data.samples.map((s: Record<string, unknown>, i: number) => ({
      index: (currentPage.value - 1) * pageSize.value + i + 1,
      ...s,
    }));
  } catch {
    samples.value = [];
    totalSamples.value = 0;
  } finally {
    loading.value = false;
  }
}

function handleDatasetChange(_dataset: string): void {
  currentPage.value = 1;
  fetchData();
}

function handleRefresh(): void {
  fetchData();
}

function handlePrev(): void {
  if (currentPage.value > 1) {
    currentPage.value--;
    fetchData();
  }
}

function handleNext(): void {
  if (currentPage.value * pageSize.value < totalSamples.value) {
    currentPage.value++;
    fetchData();
  }
}
</script>

<style scoped>
.dataset-preview {
  background: var(--bg-surface);
  border-radius: var(--radius-md);
  padding: var(--spacing-4);
}

.preview-toolbar {
  display: flex;
  align-items: center;
  gap: 8px;
  margin-bottom: var(--spacing-3);
}

.toolbar-select {
  flex: 1;
}

.preview-count {
  font-size: 11px;
  color: var(--text-tertiary);
  white-space: nowrap;
}

.preview-table {
  margin-top: var(--spacing-3);
}

.preview-table :deep(.n-ellipsis) {
  font-size: var(--font-size-base);
}
</style>
