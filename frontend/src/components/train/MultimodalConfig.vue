<template>
  <n-grid :cols="5" :x-gap="8" :y-gap="6">
    <n-grid-item>
      <n-form-item :label="$t('freeze_vision_tower')" label-placement="top" size="tiny">
        <n-switch v-model:value="store.form.freeze_vision_tower" size="small" />
      </n-form-item>
    </n-grid-item>
    <n-grid-item>
      <n-form-item :label="$t('freeze_multi_modal_projector')" label-placement="top" size="tiny">
        <n-switch v-model:value="store.form.freeze_multi_modal_projector" size="small" />
      </n-form-item>
    </n-grid-item>
    <n-grid-item>
      <n-form-item :label="$t('freeze_language_model')" label-placement="top" size="tiny">
        <n-switch v-model:value="store.form.freeze_language_model" size="small" />
      </n-form-item>
    </n-grid-item>
    <n-grid-item>
      <n-form-item :label="$t('image_max_pixels')" label-placement="top" size="tiny">
        <n-input v-model:value="store.form.image_max_pixels" size="tiny" />
      </n-form-item>
    </n-grid-item>
    <n-grid-item>
      <n-form-item :label="$t('image_min_pixels')" label-placement="top" size="tiny">
        <n-input v-model:value="store.form.image_min_pixels" size="tiny" />
      </n-form-item>
    </n-grid-item>
    <n-grid-item>
      <n-form-item :label="$t('video_max_pixels')" label-placement="top" size="tiny">
        <n-input v-model:value="store.form.video_max_pixels" size="tiny" />
      </n-form-item>
    </n-grid-item>
    <n-grid-item>
      <n-form-item :label="$t('video_min_pixels')" label-placement="top" size="tiny">
        <n-input v-model:value="store.form.video_min_pixels" size="tiny" />
      </n-form-item>
    </n-grid-item>
  </n-grid>
</template>

<script setup lang="ts">
import { useTrainFormStore } from "@/stores/trainForm";

const store = useTrainFormStore();
</script>
