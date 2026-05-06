<template>
  <header class="app-header">
    <div class="header-left">
      <div class="header-accent" />
      <div>
        <h2 class="header-title">{{ pageTitle }}</h2>
        <p class="header-desc">{{ pageDesc }}</p>
      </div>
    </div>

    <div class="header-right">
      <span v-if="session.modelName" class="chip chip--model">
        <span class="chip-dot" />
        {{ session.modelName }}
      </span>

      <span v-if="chat.modelLoaded" class="chip chip--loaded">
        <span class="chip-dot" />
        {{ $t('model_loaded') }}
      </span>

      <n-tooltip trigger="hover">
        <template #trigger>
          <n-button quaternary circle size="tiny" @click="handleRefresh">
            <template #icon>
              <RotateCw :size="14" />
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
import { RotateCw } from "lucide-vue-next";

const { t } = useI18n();
const route = useRoute();
const message = useMessage();
const session = useSessionStore();
const chat = useChatStore();

const pageTitle = computed(() => {
  const key = route.meta?.title as string;
  return key ? t(key) : "";
});

const pageDesc = computed(() => {
  const key = route.meta?.desc as string;
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
  padding: 0 0 var(--spacing-3) 0;
  border-bottom: 1px solid var(--border-default);
  margin-bottom: var(--spacing-5);
}

.header-left {
  display: flex;
  align-items: center;
  gap: var(--spacing-3);
}

.header-accent {
  width: 3px;
  height: 28px;
  background: var(--color-brand);
  border-radius: 2px;
  flex-shrink: 0;
}

.header-title {
  font-size: var(--font-size-md);
  font-weight: var(--font-weight-bold);
  color: var(--text-primary);
  margin: 0;
  line-height: 1.3;
}

.header-desc {
  font-size: 12px;
  color: var(--text-tertiary);
  margin: 0;
  line-height: 1.3;
}

.header-right {
  display: flex;
  align-items: center;
  gap: var(--spacing-3);
}

.chip {
  display: inline-flex;
  align-items: center;
  gap: 5px;
  padding: 2px 8px;
  border-radius: var(--radius-full);
  font-size: 12px;
  font-weight: var(--font-weight-medium);
}

.chip--model {
  background: var(--color-brand-bg);
  color: var(--color-brand);
}

.chip--loaded {
  background: var(--color-success);
  color: #fff;
}

.chip-dot {
  width: 5px;
  height: 5px;
  border-radius: 50%;
  background: currentColor;
  opacity: 0.6;
}
</style>
