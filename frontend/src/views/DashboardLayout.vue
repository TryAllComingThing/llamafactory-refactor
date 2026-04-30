<template>
  <div class="narrow-screen-hint">
    <p>{{ $t('narrow_screen_hint') }}</p>
  </div>

  <div class="app-container">
    <AppSidebar />
    <div class="content-area">
      <main class="main-content">
        <AppHeader />
        <router-view />
      </main>
      <AppFooter />
    </div>
  </div>
</template>

<script setup lang="ts">
import AppSidebar from "@/components/layout/AppSidebar.vue";
import AppHeader from "@/components/layout/AppHeader.vue";
import AppFooter from "@/components/layout/AppFooter.vue";
</script>

<style scoped>
.app-container {
  display: flex;
  min-height: 100vh;
}

.content-area {
  flex: 1;
  display: flex;
  flex-direction: column;
  min-width: 0;
}

.main-content {
  flex: 1;
  padding: var(--spacing-6);
  overflow-y: auto;
  max-width: calc(100vw - 280px);
}

@media (min-width: 1440px) {
  .main-content {
    max-width: 960px;
  }
}

@media (max-width: 1023px) {
  .app-container {
    display: none;
  }
}
</style>
