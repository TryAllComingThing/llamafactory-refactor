<template>
  <div class="narrow-screen-hint">
    <p>{{ $t('narrow_screen_hint') }}</p>
  </div>

  <div class="app-container">
    <AppHeaderBar />
    <ModelConfig />

    <n-tabs
      :value="activeTab"
      size="medium"
      type="line"
      class="nav-tabs"
      @update:value="handleTabChange"
    >
      <n-tab-pane v-for="tab in tabs" :key="tab.name" :name="tab.name" :tab="$t(tab.labelKey)">
        <template #tab>
          <span class="tab-label">
            <component :is="tab.icon" :size="14" />
            <span>{{ $t(tab.labelKey) }}</span>
          </span>
        </template>
      </n-tab-pane>
    </n-tabs>

    <main class="main-content">
      <router-view v-slot="{ Component }">
        <transition name="page-fade" mode="out-in">
          <component :is="Component" />
        </transition>
      </router-view>
    </main>

    <AppFooter />
  </div>
</template>

<script setup lang="ts">
import { computed } from "vue";
import { useRouter, useRoute } from "vue-router";
import { useI18n } from "vue-i18n";
import { Cog, BarChart3, MessageCircle, Download } from "lucide-vue-next";
import AppHeaderBar from "@/components/layout/AppHeaderBar.vue";
import AppFooter from "@/components/layout/AppFooter.vue";
import ModelConfig from "@/components/common/ModelConfig.vue";

const { t } = useI18n();
const router = useRouter();
const route = useRoute();

const tabs = [
  { name: "train", labelKey: "nav_train", icon: Cog },
  { name: "eval", labelKey: "nav_eval", icon: BarChart3 },
  { name: "infer", labelKey: "nav_infer", icon: MessageCircle },
  { name: "export", labelKey: "nav_export", icon: Download },
];

const activeTab = computed(() => {
  const name = route.name as string;
  return tabs.find((t) => t.name === name) ? name : "train";
});

function handleTabChange(name: string): void {
  router.push({ name });
}
</script>

<style scoped>
.app-container {
  display: flex;
  flex-direction: column;
  min-height: 100vh;
}

.nav-tabs {
  padding: 0 var(--spacing-5);
  background: var(--bg-surface);
  border-bottom: 1px solid var(--border-default);
  flex-shrink: 0;
}

.nav-tabs :deep(.n-tabs-nav) {
  --n-tab-font-size: 12px;
}

.tab-label {
  display: inline-flex;
  align-items: center;
  gap: 6px;
}

.main-content {
  flex: 1;
  padding: var(--spacing-5) var(--spacing-6);
  overflow-y: auto;
}

.page-fade-enter-active,
.page-fade-leave-active {
  transition: opacity 120ms ease;
}

.page-fade-enter-from,
.page-fade-leave-to {
  opacity: 0;
}

@media (max-width: 1023px) {
  .app-container {
    display: none;
  }
}
</style>
