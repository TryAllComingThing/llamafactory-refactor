<template>
  <n-collapse-item :title="$t('optimizer_tab')" name="optimizer">
    <template #header-extra>
      <n-tag v-if="store.form.use_galore" size="tiny" type="info">GaLore</n-tag>
      <n-tag v-if="store.form.use_apollo" size="tiny" type="info">Apollo</n-tag>
      <n-tag v-if="store.form.use_badam" size="tiny" type="info">BAdam</n-tag>
    </template>

    <n-divider>GaLore</n-divider>
    <n-space vertical size="small">
      <n-form-item :label="$t('use_galore')">
        <n-switch v-model:value="store.form.use_galore" />
      </n-form-item>
      <n-grid :cols="2" :x-gap="16" :y-gap="12">
        <n-grid-item>
          <n-form-item :label="$t('galore_rank')">
            <n-input-number v-model:value="store.form.galore_rank" :min="1" :max="1024" />
          </n-form-item>
        </n-grid-item>
        <n-grid-item>
          <n-form-item :label="$t('galore_update_interval')">
            <n-input-number v-model:value="store.form.galore_update_interval" :min="1" :max="1000" />
          </n-form-item>
        </n-grid-item>
        <n-grid-item>
          <n-form-item :label="$t('galore_scale')">
            <n-input-number v-model:value="store.form.galore_scale" :min="0.0" :max="10.0" :step="0.1" />
          </n-form-item>
        </n-grid-item>
        <n-grid-item>
          <n-form-item :label="$t('galore_target')">
            <n-input v-model:value="store.form.galore_target" placeholder="all" />
          </n-form-item>
        </n-grid-item>
      </n-grid>
    </n-space>

    <n-divider>Apollo</n-divider>
    <n-space vertical size="small">
      <n-form-item :label="$t('use_apollo')">
        <n-switch v-model:value="store.form.use_apollo" />
      </n-form-item>
      <n-grid :cols="2" :x-gap="16" :y-gap="12">
        <n-grid-item>
          <n-form-item :label="$t('apollo_rank')">
            <n-input-number v-model:value="store.form.apollo_rank" :min="1" :max="1024" />
          </n-form-item>
        </n-grid-item>
        <n-grid-item>
          <n-form-item :label="$t('apollo_update_interval')">
            <n-input-number v-model:value="store.form.apollo_update_interval" :min="1" :max="1000" />
          </n-form-item>
        </n-grid-item>
        <n-grid-item>
          <n-form-item :label="$t('apollo_scale')">
            <n-input-number v-model:value="store.form.apollo_scale" :min="0.0" :max="100.0" :step="0.1" />
          </n-form-item>
        </n-grid-item>
        <n-grid-item>
          <n-form-item :label="$t('apollo_target')">
            <n-input v-model:value="store.form.apollo_target" placeholder="all" />
          </n-form-item>
        </n-grid-item>
      </n-grid>
    </n-space>

    <n-divider>BAdam</n-divider>
    <n-space vertical size="small">
      <n-form-item :label="$t('use_badam')">
        <n-switch v-model:value="store.form.use_badam" />
      </n-form-item>
      <n-grid :cols="2" :x-gap="16" :y-gap="12">
        <n-grid-item>
          <n-form-item :label="$t('badam_mode')">
            <n-select v-model:value="store.form.badam_mode" :options="badamModeOptions" />
          </n-form-item>
        </n-grid-item>
        <n-grid-item>
          <n-form-item :label="$t('badam_switch_mode')">
            <n-select v-model:value="store.form.badam_switch_mode" :options="switchModeOptions" />
          </n-form-item>
        </n-grid-item>
        <n-grid-item>
          <n-form-item :label="$t('badam_switch_interval')">
            <n-input-number v-model:value="store.form.badam_switch_interval" :min="1" :max="1000" />
          </n-form-item>
        </n-grid-item>
        <n-grid-item>
          <n-form-item :label="$t('badam_update_ratio')">
            <n-input-number v-model:value="store.form.badam_update_ratio" :min="0.0" :max="1.0" :step="0.01" />
          </n-form-item>
        </n-grid-item>
      </n-grid>
    </n-space>
  </n-collapse-item>
</template>

<script setup lang="ts">
import { useTrainFormStore } from "@/stores/trainForm";

const store = useTrainFormStore();

const badamModeOptions = [
  { label: "Layer", value: "layer" },
  { label: "Adapter", value: "adapter" },
];

const switchModeOptions = [
  { label: "Ascending", value: "ascending" },
  { label: "Descending", value: "descending" },
  { label: "Random", value: "random" },
  { label: "Fixed", value: "fixed" },
];
</script>
