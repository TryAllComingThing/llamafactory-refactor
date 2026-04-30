<template>
  <footer class="app-footer">
    <div class="footer-left">
      <span class="footer-link" @click="handleOpenDocs">{{ $t('docs') }}</span>
      <span class="footer-separator">|</span>
      <span class="footer-link" @click="handleOpenGithub">GitHub</span>
    </div>

    <div class="footer-center">
      <span class="footer-label">{{ $t('memory_usage') }}</span>
      <div class="memory-bar">
        <div
          class="memory-bar-fill"
          :style="{ width: memoryPercent + '%' }"
          :class="memoryBarClass"
        />
      </div>
      <span class="footer-value">{{ memoryUsed }}GB / {{ memoryTotal }}GB</span>
    </div>

    <div class="footer-right">
      <WsStatusIndicator />
      <span class="footer-separator">|</span>
      <span class="footer-label">{{ sysInfo || $t('sys_ready') }}</span>
    </div>
  </footer>
</template>

<script setup lang="ts">
import { ref, computed, onMounted, onUnmounted } from "vue";
import { useI18n } from "vue-i18n";
import WsStatusIndicator from "@/components/common/WsStatusIndicator.vue";

const { t } = useI18n();
const memoryUsed = ref(0);
const memoryTotal = ref(16);
const sysInfo = ref("");

let timer: ReturnType<typeof setInterval> | null = null;

const memoryPercent = computed(() => {
  if (memoryTotal.value === 0) return 0;
  return Math.min(100, Math.round((memoryUsed.value / memoryTotal.value) * 100));
});

const memoryBarClass = computed(() => {
  if (memoryPercent.value >= 90) return "memory-bar--critical";
  if (memoryPercent.value >= 70) return "memory-bar--warning";
  return "";
});

function fetchMemoryStatus(): void {
  // TODO: 接入真实 GPU 显存 API，当前为 mock 数据
  memoryUsed.value = Math.round((Math.random() * 8 + 0.5) * 10) / 10;
  sysInfo.value = memoryUsed.value > 6 ? t("gpu_memory_critical") : t("gpu_memory_normal");
}

function handleOpenDocs(): void {
  window.open("https://github.com/hiyouga/LLaMA-Factory/wiki", "_blank");
}

function handleOpenGithub(): void {
  window.open("https://github.com/hiyouga/LLaMA-Factory", "_blank");
}

onMounted(() => {
  fetchMemoryStatus();
  timer = setInterval(fetchMemoryStatus, 5000);
});

onUnmounted(() => {
  if (timer) clearInterval(timer);
});
</script>

<style scoped>
.app-footer {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: var(--spacing-2) var(--spacing-5);
  border-top: 1px solid var(--border-default);
  background: var(--bg-surface);
  font-size: var(--font-size-xs);
  color: var(--text-tertiary);
  flex-shrink: 0;
}

.footer-left {
  display: flex;
  align-items: center;
  gap: var(--spacing-2);
}

.footer-link {
  cursor: pointer;
  transition: color var(--transition-fast);
}

.footer-link:hover {
  color: var(--color-brand);
}

.footer-separator {
  color: var(--border-default);
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
  min-width: 80px;
  text-align: right;
}

.footer-right {
  display: flex;
  align-items: center;
}

.memory-bar {
  width: 100px;
  height: 8px;
  background: var(--bg-elevated);
  border-radius: var(--radius-sm);
  overflow: hidden;
}

.memory-bar-fill {
  height: 100%;
  background: var(--color-brand);
  border-radius: var(--radius-sm);
  transition: width 0.5s ease, background 0.5s ease;
}

.memory-bar--warning {
  background: var(--color-warning);
}

.memory-bar--critical {
  background: var(--color-error);
}
</style>
