<template>
  <footer class="app-footer">
    <div class="footer-center">
      <span class="footer-label">{{ $t('memory_usage') }}</span>
      <div class="memory-bar">
        <div
          class="memory-bar-fill"
          :style="{ width: memoryPercent + '%' }"
          :class="memoryBarClass"
        />
      </div>
      <span class="footer-value">{{ memoryUsed }} / {{ memoryTotal }} GB</span>
    </div>

    <div class="footer-right">
      <span class="ws-dot" :class="wsConnected ? 'ws-dot--ok' : 'ws-dot--off'" />
      <span class="footer-label">{{ wsConnected ? $t('ws_connected') : $t('ws_disconnected') }}</span>
      <span class="footer-sep" />
      <span class="footer-sys">{{ sysText }}</span>
    </div>
  </footer>
</template>

<script setup lang="ts">
import { ref, computed, onMounted, onUnmounted } from "vue";
import { useI18n } from "vue-i18n";
import { getJson } from "@/api/client";
import { wsManager } from "@/api/ws-manager";
import type { WsStatus } from "@/api/ws-manager";

const { t } = useI18n();
const memoryUsed = ref(0);
const memoryTotal = ref(0);
const sysText = ref("");
const wsConnected = ref(false);

let memoryTimer: ReturnType<typeof setInterval> | null = null;
let unsubWs: (() => void) | null = null;

const memoryPercent = computed(() => {
  if (memoryTotal.value === 0) return 0;
  return Math.min(100, Math.round((memoryUsed.value / memoryTotal.value) * 100));
});

const memoryBarClass = computed(() => {
  if (memoryPercent.value >= 90) return "memory-bar--critical";
  if (memoryPercent.value >= 70) return "memory-bar--warning";
  return "";
});

interface GpuMemory { used: number; total: number; utilization: number; device_count: number }

async function fetchMemoryStatus(): Promise<void> {
  try {
    const data = await getJson<GpuMemory>("/gpu-memory");
    memoryUsed.value = data.used;
    memoryTotal.value = data.total;
    if (data.device_count === 0) {
      sysText.value = t("no_gpu_available");
    } else {
      sysText.value = `${data.device_count} GPU · ${data.utilization}%`;
    }
  } catch {
    sysText.value = "";
  }
}

onMounted(() => {
  fetchMemoryStatus();
  memoryTimer = setInterval(fetchMemoryStatus, 8000);
  wsConnected.value = wsManager.getStatus() === "connected";
  unsubWs = wsManager.onStatusChange((status: WsStatus) => {
    wsConnected.value = status === "connected";
  });
});

onUnmounted(() => {
  if (memoryTimer) clearInterval(memoryTimer);
  unsubWs?.();
});
</script>

<style scoped>
.app-footer {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 5px var(--spacing-4);
  border-top: 1px solid var(--border-default);
  background: var(--bg-surface);
  font-size: 10px;
  color: var(--text-tertiary);
  flex-shrink: 0;
}

.footer-center {
  display: flex;
  align-items: center;
  gap: var(--spacing-2);
}

.footer-label {
  color: var(--text-tertiary);
}

.footer-value {
  color: var(--text-secondary);
  font-family: var(--font-mono);
  font-size: 10px;
}

.footer-right {
  display: flex;
  align-items: center;
  gap: var(--spacing-2);
}

.footer-sys {
  color: var(--text-secondary);
  font-family: var(--font-mono);
  font-size: 10px;
}

.ws-dot {
  width: 6px;
  height: 6px;
  border-radius: 50%;
  background: var(--text-tertiary);
  flex-shrink: 0;
}

.ws-dot--ok {
  background: var(--color-success);
}

.ws-dot--off {
  background: var(--text-tertiary);
}

.memory-bar {
  width: 80px;
  height: 4px;
  background: var(--bg-elevated);
  border-radius: var(--radius-full);
  overflow: hidden;
}

.memory-bar-fill {
  height: 100%;
  background: var(--color-brand);
  border-radius: var(--radius-full);
  transition: width 0.5s ease, background 0.5s ease;
}

.memory-bar--warning {
  background: var(--color-warning);
}

.memory-bar--critical {
  background: var(--color-error);
}
</style>
