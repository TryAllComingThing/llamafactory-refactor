<template>
  <n-tooltip trigger="hover">
    <template #trigger>
      <span class="ws-status" :class="`ws-status--${status}`">
        <span class="ws-dot" />
        <span class="ws-label">{{ label }}</span>
      </span>
    </template>
    <span>{{ tooltip }}</span>
  </n-tooltip>
</template>

<script setup lang="ts">
import { computed } from "vue";
import { useI18n } from "vue-i18n";
import { useWsStatus } from "@/composables/useWsStatus";

const { t } = useI18n();
const { status } = useWsStatus();

const label = computed(() => {
  switch (status.value) {
    case "connected": return t("ws_connected");
    case "connecting": return t("ws_connecting");
    case "reconnecting": return t("ws_reconnecting");
    default: return t("ws_disconnected");
  }
});

const tooltip = computed(() => {
  switch (status.value) {
    case "connected": return t("ws_connected_tip");
    case "connecting": return t("ws_connecting_tip");
    case "reconnecting": return t("ws_reconnecting_tip");
    default: return t("ws_disconnected_tip");
  }
});
</script>

<style scoped>
.ws-status {
  display: inline-flex;
  align-items: center;
  gap: 4px;
  font-size: var(--font-size-xs);
  cursor: default;
}

.ws-dot {
  width: 6px;
  height: 6px;
  border-radius: 50%;
  background: var(--text-tertiary);
}

.ws-status--connected .ws-dot {
  background: var(--color-success);
}

.ws-status--connected .ws-label {
  color: var(--color-success);
}

.ws-status--connecting .ws-dot,
.ws-status--reconnecting .ws-dot {
  background: var(--color-warning);
  animation: pulse 1s ease-in-out infinite;
}

.ws-status--connecting .ws-label,
.ws-status--reconnecting .ws-label {
  color: var(--color-warning);
}

.ws-status--disconnected .ws-dot {
  background: var(--color-error);
}

.ws-status--disconnected .ws-label {
  color: var(--color-error);
}

@keyframes pulse {
  0%, 100% { opacity: 0.4; }
  50% { opacity: 1; }
}
</style>
