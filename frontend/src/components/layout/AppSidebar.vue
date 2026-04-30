<template>
  <aside class="sidebar">
    <div class="sidebar-header">
      <h1 class="sidebar-title">LLaMA Factory</h1>
      <p class="sidebar-subtitle">{{ $t('system_subtitle') }}</p>
    </div>

    <nav class="sidebar-nav">
      <router-link
        v-for="tab in tabs"
        :key="tab.name"
        :to="tab.path"
        class="nav-item"
        active-class="nav-item--active"
      >
        <span class="nav-icon">{{ tab.icon }}</span>
        <span class="nav-label">{{ $t(tab.labelKey) }}</span>
      </router-link>
    </nav>

    <div class="sidebar-footer">
      <label class="theme-toggle">
        <span class="theme-label">{{ darkMode ? $t('theme_dark') : $t('theme_light') }}</span>
        <n-switch :value="darkMode" @update:value="session.toggleDarkMode" size="small" />
      </label>
    </div>
  </aside>
</template>

<script setup lang="ts">
import { computed } from "vue";
import { useSessionStore } from "@/stores/session";

const session = useSessionStore();
const darkMode = computed(() => session.darkMode);

const tabs = [
  { name: "train", path: "/train", labelKey: "nav.train", icon: "⚙" },
  { name: "eval", path: "/eval", labelKey: "nav.eval", icon: "📊" },
  { name: "infer", path: "/infer", labelKey: "nav.infer", icon: "💬" },
  { name: "export", path: "/export", labelKey: "nav.export", icon: "📦" },
];
</script>

<style scoped>
.sidebar {
  width: 280px;
  flex-shrink: 0;
  background: var(--bg-surface);
  border-right: 1px solid var(--border-default);
  display: flex;
  flex-direction: column;
  padding: var(--spacing-6) 0;
}

.sidebar-header {
  padding: 0 var(--spacing-5) var(--spacing-6);
  border-bottom: 1px solid var(--border-default);
  margin-bottom: var(--spacing-4);
}

.sidebar-title {
  font-size: var(--font-size-xl);
  font-weight: var(--font-weight-bold);
  color: var(--color-brand);
  margin: 0;
}

.sidebar-subtitle {
  font-size: var(--font-size-xs);
  color: var(--text-tertiary);
  margin-top: var(--spacing-1);
}

.sidebar-nav {
  flex: 1;
  display: flex;
  flex-direction: column;
  gap: var(--spacing-1);
  padding: 0 var(--spacing-3);
}

.nav-item {
  display: flex;
  align-items: center;
  gap: var(--spacing-3);
  padding: var(--spacing-2) var(--spacing-3);
  border-radius: var(--radius-sm);
  color: var(--text-secondary);
  font-weight: var(--font-weight-medium);
  transition: background var(--transition-fast), color var(--transition-fast);
  text-decoration: none;
}

.nav-item:hover {
  background: var(--color-brand-bg);
  color: var(--text-primary);
}

.nav-item--active {
  background: var(--color-brand-bg);
  color: var(--color-brand);
}

.nav-icon {
  font-size: var(--font-size-md);
  width: 20px;
  text-align: center;
}

.nav-label {
  font-size: var(--font-size-base);
}

.sidebar-footer {
  padding: var(--spacing-4) var(--spacing-5);
  border-top: 1px solid var(--border-default);
}

.theme-toggle {
  display: flex;
  align-items: center;
  justify-content: space-between;
  cursor: pointer;
}

.theme-label {
  font-size: var(--font-size-sm);
  color: var(--text-secondary);
}
</style>
