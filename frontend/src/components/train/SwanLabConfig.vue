<template>
  <n-form-item :label="$t('use_swanlab')" label-placement="top" size="tiny">
    <n-switch v-model:value="store.form.use_swanlab" size="small" />
  </n-form-item>
  <n-grid :cols="5" :x-gap="8" :y-gap="6">
    <n-grid-item>
      <n-form-item :label="$t('swanlab_project')" label-placement="top" size="tiny">
        <n-input v-model:value="store.form.swanlab_project" placeholder="llamafactory" size="tiny" />
      </n-form-item>
    </n-grid-item>
    <n-grid-item>
      <n-form-item :label="$t('swanlab_run_name')" label-placement="top" size="tiny">
        <n-input v-model:value="store.form.swanlab_run_name" :placeholder="$t('optional')" size="tiny" />
      </n-form-item>
    </n-grid-item>
    <n-grid-item>
      <n-form-item :label="$t('swanlab_workspace')" label-placement="top" size="tiny">
        <n-input v-model:value="store.form.swanlab_workspace" :placeholder="$t('optional')" size="tiny" />
      </n-form-item>
    </n-grid-item>
    <n-grid-item>
      <n-form-item :label="$t('swanlab_api_key')" label-placement="top" size="tiny">
        <n-input
          v-model:value="store.form.swanlab_api_key"
          type="password"
          :placeholder="$t('input_api_key')"
          show-password-on="click"
          size="tiny"
        />
      </n-form-item>
    </n-grid-item>
    <n-grid-item>
      <n-form-item :label="$t('swanlab_mode')" label-placement="top" size="tiny">
        <n-select
          v-model:value="store.form.swanlab_mode"
          :options="modeOptions"
          size="tiny"
        />
      </n-form-item>
    </n-grid-item>
  </n-grid>
</template>

<script setup lang="ts">
import { useTrainFormStore } from "@/stores/trainForm";

const store = useTrainFormStore();

const modeOptions = [
  { label: "Cloud", value: "cloud" },
  { label: "Local", value: "local" },
  { label: "Disabled", value: "disabled" },
];
</script>
