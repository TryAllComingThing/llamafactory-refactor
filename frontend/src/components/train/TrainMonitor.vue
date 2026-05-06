<template>
  <div class="train-monitor">
    <div class="monitor-header">
      <n-space justify="space-between" align="center">
        <n-tag :type="statusTagType" size="small">{{ statusText }}</n-tag>
        <n-space size="small">
          <n-button
            v-if="isRunning"
            size="tiny"
            type="warning"
            @click="handleAbort"
          >
            {{ $t('abort_btn') }}
          </n-button>
          <n-button
            v-if="hasData"
            size="tiny"
            @click="handleClear"
          >
            {{ $t('clear_btn') }}
          </n-button>
        </n-space>
      </n-space>
    </div>

    <div class="monitor-content">
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
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, watch, onUnmounted, nextTick } from "vue";
import { useI18n } from "vue-i18n";
import { useMessage } from "naive-ui";
import { wsManager } from "@/api/ws-manager";
import { abortTrain } from "@/api/train";
import type {
  WsTrainMonitorProgress,
  WsTrainMonitorLog,
  WsTrainMonitorLoss,
  WsTrainComplete,
} from "@/types/api";
import LossChart from "@/components/common/LossChart.vue";

const { t } = useI18n();
const message = useMessage();

interface LossPoint {
  step: number;
  value: number;
}

const props = defineProps<{
  runId?: string;
}>();

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

let unsubProgress: (() => void) | null = null;
let unsubLog: (() => void) | null = null;
let unsubLoss: (() => void) | null = null;
let unsubComplete: (() => void) | null = null;

function connectWs(runId: string): void {
  disconnectWs();
  wsManager.connect(`/ws/train/${encodeURIComponent(runId)}`);

  unsubProgress = wsManager.on("progress", (data) => {
    const msg = data as unknown as WsTrainMonitorProgress;
    percentage.value = msg.percentage;
    current.value = msg.current;
    total.value = msg.total;
    elapsedSecs.value = msg.elapsed_secs;
    remainingSecs.value = msg.remaining_secs;
    isRunning.value = true;
  });

  unsubLog = wsManager.on("log", (data) => {
    const msg = data as unknown as WsTrainMonitorLog;
    logLines.value.push(msg.text);
    if (logLines.value.length > 1000) {
      logLines.value = logLines.value.slice(-500);
    }
    scrollToBottom();
  });

  unsubLoss = wsManager.on("loss", (data) => {
    const msg = data as unknown as WsTrainMonitorLoss;
    currentLoss.value = msg.value;
    lossData.value.push({ step: msg.step, value: msg.value });
    if (lossData.value.length > 10000) {
      lossData.value = lossData.value.slice(-5000);
    }
  });

  unsubComplete = wsManager.on("train:complete", (data) => {
    const msg = data as unknown as WsTrainComplete;
    isRunning.value = false;
    if (msg.status === "success") {
      message.success(t("training_completed"));
    } else if (msg.status === "aborted") {
      message.warning(t("training_aborted"));
    } else {
      message.error(msg.message || t("training_failed"));
    }
  });
}

function disconnectWs(): void {
  unsubProgress?.();
  unsubLog?.();
  unsubLoss?.();
  unsubComplete?.();
  unsubProgress = null;
  unsubLog = null;
  unsubLoss = null;
  unsubComplete = null;
  wsManager.disconnect();
}

watch(
  () => props.runId,
  (newId) => {
    if (newId) {
      isRunning.value = true;
      connectWs(newId);
    } else {
      disconnectWs();
    }
  },
);

onUnmounted(() => {
  disconnectWs();
});

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

async function handleAbort(): Promise<void> {
  try {
    await abortTrain();
    isRunning.value = false;
    message.info(t("abort_sent"));
  } catch {
    message.error(t("operation_failed"));
  }
}

function handleClear(): void {
  disconnectWs();
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
  reset(): void {
    handleClear();
  },
});
</script>

<style scoped>
.train-monitor {
  height: 100%;
  display: flex;
  flex-direction: column;
}

.monitor-header {
  padding-bottom: var(--spacing-3);
  border-bottom: 1px solid var(--border-default);
  margin-bottom: var(--spacing-3);
}

.monitor-content {
  flex: 1;
  display: flex;
  flex-direction: column;
  gap: var(--spacing-3);
  overflow-y: auto;
}

.progress-section {
  padding: var(--spacing-2) 0;
}

.progress-info {
  display: flex;
  justify-content: space-between;
  font-size: var(--font-size-xs);
  color: var(--text-secondary);
  margin-top: var(--spacing-1);
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
  font-size: var(--font-size-base);
  font-weight: var(--font-weight-medium);
  font-family: var(--font-mono);
  color: var(--color-brand);
}

.log-section {
  flex: 1;
  min-height: 200px;
  border: 1px solid var(--border-default);
  border-radius: var(--radius-sm);
  overflow: hidden;
  display: flex;
  flex-direction: column;
}

.log-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: var(--spacing-2) var(--spacing-3);
  border-bottom: 1px solid var(--border-default);
  font-size: var(--font-size-xs);
  color: var(--text-secondary);
  background: var(--bg-elevated);
}

.log-content {
  flex: 1;
  min-height: 150px;
  max-height: 300px;
  overflow-y: auto;
  padding: var(--spacing-2) var(--spacing-3);
  font-family: var(--font-mono);
  font-size: var(--font-size-xs);
  line-height: 1.6;
  background: var(--bg-surface);
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
