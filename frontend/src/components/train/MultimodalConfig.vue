<template>
  <n-collapse-item :title="$t('mm_tab')" name="multimodal">
    <n-grid :cols="2" :x-gap="16" :y-gap="12">
      <n-grid-item>
        <n-form-item :label="$t('freeze_vision_tower')">
          <n-switch v-model:value="store.form.freeze_vision_tower" />
        </n-form-item>
      </n-grid-item>
      <n-grid-item>
        <n-form-item :label="$t('freeze_multi_modal_projector')">
          <n-switch v-model:value="store.form.freeze_multi_modal_projector" />
        </n-form-item>
      </n-grid-item>
      <n-grid-item>
        <n-form-item :label="$t('freeze_language_model')">
          <n-switch v-model:value="store.form.freeze_language_model" />
        </n-form-item>
      </n-grid-item>
      <n-grid-item />
      <n-grid-item>
        <n-form-item :label="$t('image_max_pixels')">
          <n-input v-model:value="store.form.image_max_pixels" />
        </n-form-item>
      </n-grid-item>
      <n-grid-item>
        <n-form-item :label="$t('image_min_pixels')">
          <n-input v-model:value="store.form.image_min_pixels" />
        </n-form-item>
      </n-grid-item>
      <n-grid-item>
        <n-form-item :label="$t('video_max_pixels')">
          <n-input v-model:value="store.form.video_max_pixels" />
        </n-form-item>
      </n-grid-item>
      <n-grid-item>
        <n-form-item :label="$t('video_min_pixels')">
          <n-input v-model:value="store.form.video_min_pixels" />
        </n-form-item>
      </n-grid-item>
    </n-grid>
  </n-collapse-item>
</template>

<script setup lang="ts">
import { useTrainFormStore } from "@/stores/trainForm";

const store = useTrainFormStore();
</script>
