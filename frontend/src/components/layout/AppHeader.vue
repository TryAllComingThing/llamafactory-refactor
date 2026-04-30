<template>
  <header class="app-header">
    <div class="header-left">
      <h2 class="header-title">{{ pageTitle }}</h2>
    </div>

    <div class="header-right">
      <div v-if="session.modelName" class="status-item">
        <span class="status-dot status-dot--active" />
        <span class="status-label">{{ session.modelName }}</span>
      </div>

      <div v-if="chat.modelLoaded" class="status-item">
        <span class="status-dot status-dot--active" />
        <span class="status-label">{{ $t('model_loaded') }}</span>
      </div>

      <n-tooltip trigger="hover">
        <template #trigger>
          <n-button quaternary circle size="small" @click="handleRefresh">
            <template #icon>
              <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                <polyline points="23 4 23 10 17 10" />
                <polyline points="1 20 1 14 7 14" />
                <path d="M3.51 9a9 9 0 0 1 14.85-3.36L23 10M1 14l4.64 4.36A9 9 0 0 0 20.49 15" />
              </svg>
            </template>
          </n-button>
        </template>
        {{ $t('refresh_status') }}
      </n-tooltip>
    </div>
  </header>
</template>

<script setup lang="ts">
import { computed } from "vue";
import { useI18n } from "vue-i18n";
import { useRoute } from "vue-router";
import { useMessage } from "naive-ui";
import { useSessionStore } from "@/stores/session";
import { useChatStore } from "@/stores/chatStore";

const { t } = useI18n();
const route = useRoute();
const message = useMessage();
const session = useSessionStore();
const chat = useChatStore();

const pageTitle = computed(() => {
  const key = route.meta?.title as string;
  return key ? t(key) : "";
});

function handleRefresh(): void {
  message.info(t("status_refreshed"));
}
</script>

<style scoped>
.app-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 0 0 var(--spacing-4) 0;
  border-bottom: 1px solid var(--border-default);
  margin-bottom: var(--spacing-6);
}

.header-left {
  display: flex;
  align-items: center;
}

.header-title {
  font-size: var(--font-size-2xl);
  font-weight: var(--font-weight-bold);
  color: var(--text-primary);
  margin: 0;
}

.header-right {
  display: flex;
  align-items: center;
  gap: var(--spacing-4);
}

.status-item {
  display: flex;
  align-items: center;
  gap: var(--spacing-2);
}

.status-dot {
  width: 8px;
  height: 8px;
  border-radius: 50%;
  background: var(--text-tertiary);
}

.status-dot--active {
  background: var(--color-success);
}

.status-label {
  font-size: var(--font-size-sm);
  color: var(--text-secondary);
}
</style>
