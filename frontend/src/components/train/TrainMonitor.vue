<template>
  <n-card :title="$t('train_monitor_title')" class="train-monitor-card">
    <n-space vertical size="medium">
      <!-- Status bar -->
      <n-space justify="space-between" align="center">
        <n-tag :type="statusTagType" size="small">{{ statusText }}</n-tag>
        <n-space size="small">
          <n-button
            v-if="isRunning"
            size="small"
            type="warning"
            @click="handleAbort"
          >
            {{ $t('abort_btn') }}
          </n-button>
          <n-button
            v-if="hasData"
            size="small"
            @click="handleClear"
          >
            {{ $t('clear_btn') }}
          </n-button>
        </n-space>
      </n-space>

      <!-- Progress bar -->
      <div class="progress-section">
        <n-progress
          v-if="total > 0"
          type="line"
          :percentage="percentage"
          :indicator-placement="'inside'"
          processing
        />
        <div class="progress-info">
          <span>{{ $t('step_label') }} {{ current }} / {{ total }}</span>
          <span v-if="remainingSecs > 0">
            {{ $t('remaining') }} {{ formatTime(remainingSecs) }}
          </span>
          <span v-if="elapsedSecs > 0">
            {{ $t('elapsed') }} {{ formatTime(elapsedSecs) }}
          </span>
        </div>
      </div>

      <!-- Current loss -->
      <div v-if="currentLoss > 0" class="loss-display">
        <span class="loss-label">Current Loss:</span>
        <span class="loss-value">{{ currentLoss.toFixed(6) }}</span>
      </div>

      <!-- Loss chart -->
      <LossChart :data="lossData" />

      <!-- Log output -->
      <div class="log-section">
        <div class="log-header">
          <span>{{ $t('train_log') }}</span>
          <n-button size="tiny" quaternary @click="scrollToBottom">
            {{ $t('scroll_bottom') }}
          </n-button>
        </div>
        <div ref="logRef" class="log-content">
          <div v-if="logLines.length === 0" class="log-empty">
            {{ $t('waiting_log') }}
          </div>
          <div v-for="(line, i) in logLines" :key="i" class="log-line">
            {{ line }}
          </div>
        </div>
      </div>
    </n-space>
  </n-card>
</template>

<script setup lang="ts">
import { ref, computed, nextTick } from "vue";
import { useI18n } from "vue-i18n";
import LossChart from "@/components/common/LossChart.vue";

const { t } = useI18n();

// TODO: 接入 WebSocket 训练监控消息，当前 expose 方法等待外部调用

interface LossPoint {
  step: number;
  value: number;
}

const logLines = ref<string[]>([]);
const lossData = ref<LossPoint[]>([]);
const isRunning = ref(false);
const percentage = ref(0);
const current = ref(0);
const total = ref(0);
const elapsedSecs = ref(0);
const remainingSecs = ref(0);
const currentLoss = ref(0);
const logRef = ref<HTMLElement | null>(null);

const hasData = computed(() => logLines.value.length > 0);

const statusText = computed(() => {
  if (isRunning.value) return t("status_training");
  if (hasData.value) return t("status_completed");
  return t("status_ready_short");
});

const statusTagType = computed<"warning" | "success" | "default">(() => {
  if (isRunning.value) return "warning";
  if (hasData.value) return "success";
  return "default";
});

function formatTime(seconds: number): string {
  const m = Math.floor(seconds / 60);
  const s = seconds % 60;
  return `${m.toString().padStart(2, "0")}:${s.toString().padStart(2, "0")}`;
}

function scrollToBottom(): void {
  nextTick(() => {
    if (logRef.value) {
      logRef.value.scrollTop = logRef.value.scrollHeight;
    }
  });
}

function handleAbort(): void {
  isRunning.value = false;
}

function handleClear(): void {
  logLines.value = [];
  lossData.value = [];
  percentage.value = 0;
  current.value = 0;
  total.value = 0;
  currentLoss.value = 0;
  elapsedSecs.value = 0;
  remainingSecs.value = 0;
}

defineExpose({
  setStatus(running: boolean): void {
    isRunning.value = running;
  },
  updateProgress(fraction: number, cur: number, tot: number, elapsed: number, remaining: number): void {
    percentage.value = Math.round(fraction * 100);
    current.value = cur;
    total.value = tot;
    elapsedSecs.value = elapsed;
    remainingSecs.value = remaining;
  },
  appendLog(text: string): void {
    logLines.value.push(text);
    if (logLines.value.length > 1000) {
      logLines.value = logLines.value.slice(-500);
    }
    scrollToBottom();
  },
  appendLoss(step: number, value: number): void {
    currentLoss.value = value;
    lossData.value.push({ step, value });
    if (lossData.value.length > 10000) {
      lossData.value = lossData.value.slice(-5000);
    }
  },
  reset(): void {
    handleClear();
  },
});
</script>

<style scoped>
.train-monitor-card {
  margin-top: var(--spacing-5);
}

.progress-section {
  padding: var(--spacing-3) 0;
}

.progress-info {
  display: flex;
  justify-content: space-between;
  font-size: var(--font-size-sm);
  color: var(--text-secondary);
  margin-top: var(--spacing-2);
}

.loss-display {
  display: flex;
  align-items: center;
  gap: var(--spacing-2);
  padding: var(--spacing-2) 0;
}

.loss-label {
  font-size: var(--font-size-sm);
  color: var(--text-secondary);
}

.loss-value {
  font-size: var(--font-size-lg);
  font-weight: var(--font-weight-bold);
  font-family: var(--font-mono);
  color: var(--color-brand);
}

.log-section {
  border: 1px solid var(--border-default);
  border-radius: var(--radius-sm);
}

.log-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: var(--spacing-2) var(--spacing-3);
  border-bottom: 1px solid var(--border-default);
  font-size: var(--font-size-sm);
  color: var(--text-secondary);
}

.log-content {
  height: 200px;
  overflow-y: auto;
  padding: var(--spacing-2) var(--spacing-3);
  font-family: var(--font-mono);
  font-size: var(--font-size-xs);
  line-height: 1.6;
}

.log-line {
  white-space: pre-wrap;
  word-break: break-all;
  color: var(--text-secondary);
}

.log-empty {
  color: var(--text-tertiary);
  font-style: italic;
}
</style>
