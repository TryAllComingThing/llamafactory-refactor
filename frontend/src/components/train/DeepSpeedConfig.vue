<template>
  <n-collapse-item :title="$t('deepspeed_tab')" name="deepspeed">
    <n-grid :cols="2" :x-gap="16" :y-gap="12">
      <n-grid-item>
        <n-form-item :label="$t('config_path')">
          <n-input v-model:value="store.form.deepspeed" placeholder="可选" />
        </n-form-item>
      </n-grid-item>
      <n-grid-item>
        <n-form-item :label="$t('ds_stage')">
          <n-select v-model:value="store.form.ds_stage" :options="stageOptions" />
        </n-form-item>
      </n-grid-item>
      <n-grid-item>
        <n-form-item :label="$t('ds_offload')">
          <n-switch v-model:value="store.form.ds_offload" />
        </n-form-item>
      </n-grid-item>
      <n-grid-item>
        <n-form-item :label="$t('device_count')">
          <n-input-number v-model:value="store.form.device_count" :min="1" :max="64" />
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
