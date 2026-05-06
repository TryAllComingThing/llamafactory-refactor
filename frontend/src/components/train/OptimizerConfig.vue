<template>
  <n-collapse-item :title="$t('optimizer_tab')" name="optimizer">
    <template #header-extra>
      <n-tag v-if="store.form.use_galore" size="tiny" type="info">GaLore</n-tag>
      <n-tag v-if="store.form.use_apollo" size="tiny" type="info">Apollo</n-tag>
      <n-tag v-if="store.form.use_badam" size="tiny" type="info">BAdam</n-tag>
    </template>

    <n-divider>GaLore</n-divider>
    <n-form-item :label="$t('use_galore')" label-placement="top" size="tiny">
      <n-switch v-model:value="store.form.use_galore" size="small" />
    </n-form-item>
    <n-grid :cols="5" :x-gap="8" :y-gap="6">
      <n-grid-item>
        <n-form-item :label="$t('galore_rank')" label-placement="top" size="tiny">
          <n-input-number v-model:value="store.form.galore_rank" :min="1" :max="1024" size="tiny" />
        </n-form-item>
      </n-grid-item>
      <n-grid-item>
        <n-form-item :label="$t('galore_update_interval')" label-placement="top" size="tiny">
          <n-input-number v-model:value="store.form.galore_update_interval" :min="1" :max="1000" size="tiny" />
        </n-form-item>
      </n-grid-item>
      <n-grid-item>
        <n-form-item :label="$t('galore_scale')" label-placement="top" size="tiny">
          <n-input-number v-model:value="store.form.galore_scale" :min="0.0" :max="10.0" :step="0.1" size="tiny" />
        </n-form-item>
      </n-grid-item>
      <n-grid-item>
        <n-form-item :label="$t('galore_target')" label-placement="top" size="tiny">
          <n-input v-model:value="store.form.galore_target" placeholder="all" size="tiny" />
        </n-form-item>
      </n-grid-item>
    </n-grid>

    <n-divider>Apollo</n-divider>
    <n-form-item :label="$t('use_apollo')" label-placement="top" size="tiny">
      <n-switch v-model:value="store.form.use_apollo" size="small" />
    </n-form-item>
    <n-grid :cols="5" :x-gap="8" :y-gap="6">
      <n-grid-item>
        <n-form-item :label="$t('apollo_rank')" label-placement="top" size="tiny">
          <n-input-number v-model:value="store.form.apollo_rank" :min="1" :max="1024" size="tiny" />
        </n-form-item>
      </n-grid-item>
      <n-grid-item>
        <n-form-item :label="$t('apollo_update_interval')" label-placement="top" size="tiny">
          <n-input-number v-model:value="store.form.apollo_update_interval" :min="1" :max="1000" size="tiny" />
        </n-form-item>
      </n-grid-item>
      <n-grid-item>
        <n-form-item :label="$t('apollo_scale')" label-placement="top" size="tiny">
          <n-input-number v-model:value="store.form.apollo_scale" :min="0.0" :max="100.0" :step="0.1" size="tiny" />
        </n-form-item>
      </n-grid-item>
      <n-grid-item>
        <n-form-item :label="$t('apollo_target')" label-placement="top" size="tiny">
          <n-input v-model:value="store.form.apollo_target" placeholder="all" size="tiny" />
        </n-form-item>
      </n-grid-item>
    </n-grid>

    <n-divider>BAdam</n-divider>
    <n-form-item :label="$t('use_badam')" label-placement="top" size="tiny">
      <n-switch v-model:value="store.form.use_badam" size="small" />
    </n-form-item>
    <n-grid :cols="5" :x-gap="8" :y-gap="6">
      <n-grid-item>
        <n-form-item :label="$t('badam_mode')" label-placement="top" size="tiny">
          <n-select v-model:value="store.form.badam_mode" :options="badamModeOptions" size="tiny" />
        </n-form-item>
      </n-grid-item>
      <n-grid-item>
        <n-form-item :label="$t('badam_switch_mode')" label-placement="top" size="tiny">
          <n-select v-model:value="store.form.badam_switch_mode" :options="switchModeOptions" size="tiny" />
        </n-form-item>
      </n-grid-item>
      <n-grid-item>
        <n-form-item :label="$t('badam_switch_interval')" label-placement="top" size="tiny">
          <n-input-number v-model:value="store.form.badam_switch_interval" :min="1" :max="1000" size="tiny" />
        </n-form-item>
      </n-grid-item>
      <n-grid-item>
        <n-form-item :label="$t('badam_update_ratio')" label-placement="top" size="tiny">
          <n-input-number v-model:value="store.form.badam_update_ratio" :min="0.0" :max="1.0" :step="0.01" size="tiny" />
        </n-form-item>
      </n-grid-item>
    </n-grid>
  </n-collapse-item>
</template>

<script setup lang="ts">
import { useTrainFormStore } from "@/stores/trainForm";

const store = useTrainFormStore();

const badamModeOptions = [
  { label: "Layer", value: "layer" },
  { label: "Ratio", value: "ratio" },
];

const switchModeOptions = [
  { label: "Ascending", value: "ascending" },
  { label: "Descending", value: "descending" },
  { label: "Random", value: "random" },
  { label: "Fixed", value: "fixed" },
];
</script>
