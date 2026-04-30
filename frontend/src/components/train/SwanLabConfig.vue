<template>
  <n-collapse-item :title="$t('swanlab_track')" name="swanlab">
    <n-space vertical size="small">
      <n-form-item :label="$t('use_swanlab')">
        <n-switch v-model:value="store.form.use_swanlab" />
      </n-form-item>
      <n-grid :cols="2" :x-gap="16" :y-gap="12">
        <n-grid-item>
          <n-form-item :label="$t('swanlab_project')">
            <n-input v-model:value="store.form.swanlab_project" placeholder="llamafactory" />
          </n-form-item>
        </n-grid-item>
        <n-grid-item>
          <n-form-item :label="$t('swanlab_run_name')">
            <n-input v-model:value="store.form.swanlab_run_name" placeholder="可选" />
          </n-form-item>
        </n-grid-item>
        <n-grid-item>
          <n-form-item :label="$t('swanlab_workspace')">
            <n-input v-model:value="store.form.swanlab_workspace" placeholder="可选" />
          </n-form-item>
        </n-grid-item>
        <n-grid-item>
          <n-form-item :label="$t('swanlab_api_key')">
            <n-input
              v-model:value="store.form.swanlab_api_key"
              type="password"
              placeholder="输入 API Key"
              show-password-on="click"
            />
          </n-form-item>
        </n-grid-item>
        <n-grid-item>
          <n-form-item :label="$t('swanlab_mode')">
            <n-select
              v-model:value="store.form.swanlab_mode"
              :options="modeOptions"
            />
          </n-form-item>
        </n-grid-item>
      </n-grid>
    </n-space>
  </n-collapse-item>
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
