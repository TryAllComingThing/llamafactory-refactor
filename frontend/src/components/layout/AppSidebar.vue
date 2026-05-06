<template>
  <aside class="sidebar" :class="{ 'sidebar--folded': session.sidebarCollapsed }">
    <div class="sidebar-header">
      <div class="brand-row">
        <span class="brand-mark" />
        <transition name="fade-text">
          <h1 v-if="!session.sidebarCollapsed" class="sidebar-title">LLaMA Factory</h1>
        </transition>
      </div>
      <transition name="fade-text">
        <p v-if="!session.sidebarCollapsed" class="sidebar-subtitle">{{ $t('system_subtitle') }}</p>
      </transition>
    </div>

    <div class="sidebar-nav-wrap">
      <transition name="fade-text">
        <span v-if="!session.sidebarCollapsed" class="nav-section-label">{{ $t('nav_section') }}</span>
      </transition>
      <nav class="sidebar-nav">
        <router-link
          v-for="tab in tabs"
          :key="tab.name"
          :to="tab.path"
          class="nav-item"
          active-class="nav-item--active"
          :title="session.sidebarCollapsed ? $t(tab.labelKey) : ''"
        >
          <span class="nav-indicator" />
          <span class="nav-icon">
            <component :is="tab.icon" :size="16" />
          </span>
          <transition name="fade-text">
            <span v-if="!session.sidebarCollapsed" class="nav-label">{{ $t(tab.labelKey) }}</span>
          </transition>
        </router-link>
      </nav>
    </div>

    <div class="sidebar-footer">
      <transition name="fade-text">
        <span v-if="!session.sidebarCollapsed" class="version-text">v0.9.0</span>
      </transition>
    </div>

    <button class="fold-toggle" @click="session.toggleSidebar" :title="session.sidebarCollapsed ? '展开' : '折叠'">
      <ChevronRight v-if="session.sidebarCollapsed" :size="12" />
      <ChevronLeft v-else :size="12" />
    </button>
  </aside>
</template>

<script setup lang="ts">
import { useSessionStore } from "@/stores/session";
import { Cog, BarChart3, MessageCircle, Download, ChevronLeft, ChevronRight } from "lucide-vue-next";

const session = useSessionStore();

const tabs = [
  { name: "train", path: "/train", labelKey: "nav_train", icon: Cog },
  { name: "eval", path: "/eval", labelKey: "nav_eval", icon: BarChart3 },
  { name: "infer", path: "/infer", labelKey: "nav_infer", icon: MessageCircle },
  { name: "export", path: "/export", labelKey: "nav_export", icon: Download },
];
</script>

<style scoped>
.sidebar {
  width: 200px;
  flex-shrink: 0;
  background: var(--bg-surface);
  border-right: 1px solid var(--border-default);
  display: flex;
  flex-direction: column;
  user-select: none;
  position: relative;
  transition: width var(--transition-base);
  overflow: hidden;
}

.sidebar--folded {
  width: 52px;
}

.sidebar-header {
  padding: var(--spacing-4) var(--spacing-3);
  border-bottom: 1px solid var(--border-default);
  min-height: 48px;
  display: flex;
  flex-direction: column;
  justify-content: center;
}

.brand-row {
  display: flex;
  align-items: center;
  gap: var(--spacing-2);
  white-space: nowrap;
}

.brand-mark {
  width: 8px;
  height: 8px;
  border-radius: 2px;
  background: var(--color-brand);
  flex-shrink: 0;
}

.sidebar--folded .brand-row {
  justify-content: center;
}

.sidebar-title {
  font-size: var(--font-size-md);
  font-weight: var(--font-weight-bold);
  color: var(--text-primary);
  margin: 0;
  letter-spacing: -0.01em;
  white-space: nowrap;
}

.sidebar-subtitle {
  font-size: 11px;
  color: var(--text-tertiary);
  margin: 2px 0 0 16px;
  white-space: nowrap;
}

.sidebar-nav-wrap {
  flex: 1;
  display: flex;
  flex-direction: column;
  padding: var(--spacing-3) var(--spacing-2);
}

.nav-section-label {
  font-size: 11px;
  font-weight: var(--font-weight-bold);
  color: var(--text-tertiary);
  text-transform: uppercase;
  letter-spacing: 0.08em;
  padding: 0 var(--spacing-3) var(--spacing-1);
  white-space: nowrap;
}

.sidebar-nav {
  display: flex;
  flex-direction: column;
  gap: 1px;
}

.nav-item {
  display: flex;
  align-items: center;
  gap: var(--spacing-2);
  padding: 7px var(--spacing-2);
  border-radius: var(--radius-md);
  color: var(--text-secondary);
  font-size: 13px;
  font-weight: var(--font-weight-medium);
  transition: background var(--transition-fast), color var(--transition-fast);
  text-decoration: none;
  position: relative;
  white-space: nowrap;
}

.sidebar--folded .nav-item {
  justify-content: center;
  padding: 7px 0;
}

.nav-indicator {
  position: absolute;
  left: 0;
  top: 50%;
  transform: translateY(-50%);
  width: 3px;
  height: 0;
  background: var(--color-brand);
  border-radius: 0 2px 2px 0;
  transition: height var(--transition-fast);
}

.sidebar--folded .nav-indicator {
  left: 0;
  border-radius: 0 2px 2px 0;
}

.nav-item:hover {
  background: var(--bg-elevated);
  color: var(--text-primary);
}

.nav-item:hover .nav-indicator {
  height: 16px;
}

.nav-item--active {
  background: var(--color-brand-bg);
  color: var(--color-brand);
}

.nav-item--active .nav-indicator {
  height: 20px;
}

.nav-icon {
  width: 16px;
  height: 16px;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
}

.nav-label {
  font-size: 13px;
}

.sidebar-footer {
  padding: var(--spacing-3);
  border-top: 1px solid var(--border-default);
  display: flex;
  flex-direction: column;
  align-items: stretch;
}

.version-text {
  font-size: 10px;
  color: var(--text-tertiary);
  text-align: center;
}

/* Fold toggle button */
.fold-toggle {
  position: absolute;
  bottom: 60px;
  right: -10px;
  width: 20px;
  height: 20px;
  border-radius: 50%;
  border: 1px solid var(--border-default);
  background: var(--bg-surface);
  color: var(--text-tertiary);
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 0;
  transition: color var(--transition-fast), background var(--transition-fast), right var(--transition-base);
  z-index: 2;
}

.fold-toggle:hover {
  color: var(--color-brand);
  background: var(--bg-elevated);
}

.sidebar--folded .fold-toggle {
  right: -10px;
}

/* Text fade transition */
.fade-text-enter-active,
.fade-text-leave-active {
  transition: opacity 120ms ease;
}

.fade-text-enter-from,
.fade-text-leave-to {
  opacity: 0;
}
</style>
