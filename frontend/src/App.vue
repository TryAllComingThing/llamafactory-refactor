<template>
  <n-config-provider :theme="naiveTheme" :locale="zhCN" :date-locale="dateZhCN">
    <n-message-provider>
      <n-notification-provider>
        <n-loading-bar-provider>
          <router-view />
        </n-loading-bar-provider>
      </n-notification-provider>
    </n-message-provider>
  </n-config-provider>
</template>

<script setup lang="ts">
import { computed } from "vue";
import { zhCN, dateZhCN } from "naive-ui";
import { darkTheme } from "naive-ui";
import { useSessionStore } from "@/stores/session";

import { useTheme } from "@/composables/useTheme";

const session = useSessionStore();

useTheme();

const naiveTheme = computed(() => (session.darkMode ? darkTheme : null));
</script>
