<template>
  <n-collapse-item :title="$t('deepspeed_tab')" name="deepspeed">
    <n-grid :cols="5" :x-gap="8" :y-gap="6">
      <n-grid-item>
        <n-form-item :label="$t('config_path')" label-placement="top" size="tiny">
          <n-input v-model:value="store.form.deepspeed" :placeholder="$t('optional')" size="tiny" />
        </n-form-item>
      </n-grid-item>
      <n-grid-item>
        <n-form-item :label="$t('ds_stage')" label-placement="top" size="tiny">
          <n-select v-model:value="store.form.ds_stage" :options="stageOptions" size="tiny" />
        </n-form-item>
      </n-grid-item>
      <n-grid-item>
        <n-form-item :label="$t('ds_offload')" label-placement="top" size="tiny">
          <n-switch v-model:value="store.form.ds_offload" size="small" />
        </n-form-item>
      </n-grid-item>
      <n-grid-item>
        <n-form-item :label="$t('device_count')" label-placement="top" size="tiny">
          <n-input-number v-model:value="store.form.device_count" :min="1" :max="64" size="tiny" />
        </n-form-item>
      </n-grid-item>
    </n-grid>
  </n-collapse-item>
</template>

<script setup lang="ts">
import { useTrainFormStore } from "@/stores/trainForm";

const store = useTrainFormStore();

const stageOptions = [
  { label: "None", value: "none" },
  { label: "Stage 1 (ZeRO-1)", value: "stage1" },
  { label: "Stage 2 (ZeRO-2)", value: "stage2" },
  { label: "Stage 3 (ZeRO-3)", value: "stage3" },
];
</script>
