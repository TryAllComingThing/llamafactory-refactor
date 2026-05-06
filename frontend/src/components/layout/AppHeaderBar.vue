<template>
  <header class="header-bar">
    <div class="header-left">
      <span class="brand-mark" />
      <span class="brand-text">LLaMA Factory</span>
    </div>

    <div class="header-right">
      <button class="header-btn" @click="session.toggleDarkMode" :title="darkMode ? $t('theme_light') : $t('theme_dark')">
        {{ darkMode ? '☽' : '☀' }}
      </button>

      <n-select
        v-model:value="session.lang"
        :options="langOptions"
        size="tiny"
        class="header-lang"
        @update:value="handleLangChange"
      />

      <a class="header-btn" href="https://github.com/hiyouga/LLaMA-Factory/wiki" target="_blank" rel="noopener">{{ $t('docs') }}</a>
      <a class="header-btn" href="https://github.com/hiyouga/LLaMA-Factory" target="_blank" rel="noopener">GitHub</a>
    </div>
  </header>
</template>

<script setup lang="ts">
import { computed } from "vue";
import { useI18n } from "vue-i18n";
import { useSessionStore } from "@/stores/session";

const { locale } = useI18n();
const session = useSessionStore();
const darkMode = computed(() => session.darkMode);

const langOptions = [
  { label: "EN", value: "en" },
  { label: "ZH", value: "zh" },
  { label: "RU", value: "ru" },
  { label: "KO", value: "ko" },
  { label: "JA", value: "ja" },
];

function handleLangChange(val: string): void {
  locale.value = val;
}
</script>

<style scoped>
.header-bar {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: var(--spacing-2) var(--spacing-5);
  background: var(--bg-surface);
  border-bottom: 1px solid var(--border-default);
  flex-shrink: 0;
  min-height: 36px;
}

.header-left {
  display: flex;
  align-items: center;
  gap: var(--spacing-2);
}

.brand-mark {
  width: 8px;
  height: 8px;
  border-radius: 2px;
  background: var(--color-brand);
  flex-shrink: 0;
}

.brand-text {
  font-size: var(--font-size-sm);
  font-weight: var(--font-weight-bold);
  color: var(--text-primary);
  letter-spacing: -0.01em;
}

.header-right {
  display: flex;
  align-items: center;
  gap: var(--spacing-2);
}

.header-btn {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  width: 66px;
  height: 28px;
  padding: 0 6px;
  border: 1px solid var(--border-default);
  border-radius: var(--radius-sm);
  background: transparent;
  color: var(--text-secondary);
  font-size: 12px;
  font-family: inherit;
  text-decoration: none;
  cursor: pointer;
  transition: border-color var(--transition-fast), color var(--transition-fast);
  white-space: nowrap;
  overflow: hidden;
}

.header-btn:hover {
  border-color: var(--text-tertiary);
  color: var(--text-primary);
}

.header-lang {
  width: 66px;
}

.header-lang :deep(.n-base-selection) {
  height: 28px;
  border: 1px solid var(--border-default);
  border-radius: var(--radius-sm);
  background: transparent;
}

.header-lang :deep(.n-base-selection:hover) {
  border-color: var(--text-tertiary);
}
</style>
