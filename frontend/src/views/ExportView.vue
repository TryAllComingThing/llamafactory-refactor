<template>
  <div class="export-view">
    <ModelConfig />
    <ExportForm />
  </div>
</template>

<script setup lang="ts">
import ModelConfig from "@/components/common/ModelConfig.vue";
import ExportForm from "@/components/export/ExportForm.vue";
</script>

<style scoped>
.export-view {
  max-width: 960px;
}
</style>
