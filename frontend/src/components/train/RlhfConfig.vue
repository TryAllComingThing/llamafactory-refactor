<template>
  <n-grid :cols="5" :x-gap="8" :y-gap="6">
    <n-grid-item>
      <n-form-item :label="$t('pref_beta')" label-placement="top" size="tiny">
        <n-input-number
          v-model:value="store.form.pref_beta"
          :min="0.0"
          :max="1.0"
          :step="0.01"
          size="tiny"
        />
      </n-form-item>
    </n-grid-item>
    <n-grid-item>
      <n-form-item :label="$t('pref_ftx')" label-placement="top" size="tiny">
        <n-input-number
          v-model:value="store.form.pref_ftx"
          :min="0.0"
          :max="10.0"
          :step="0.1"
          size="tiny"
        />
      </n-form-item>
    </n-grid-item>
    <n-grid-item>
      <n-form-item :label="$t('pref_loss')" label-placement="top" size="tiny">
        <n-select
          v-model:value="store.form.pref_loss"
          :options="lossOptions"
          size="tiny"
        />
      </n-form-item>
    </n-grid-item>
    <n-grid-item>
      <n-form-item :label="$t('ppo_score_norm')" label-placement="top" size="tiny">
        <n-switch v-model:value="store.form.ppo_score_norm" size="small" />
      </n-form-item>
    </n-grid-item>
    <n-grid-item>
      <n-form-item :label="$t('ppo_whiten_rewards')" label-placement="top" size="tiny">
        <n-switch v-model:value="store.form.ppo_whiten_rewards" size="small" />
      </n-form-item>
    </n-grid-item>
    <n-grid-item>
      <n-form-item :label="$t('reward_model')" label-placement="top" size="tiny">
        <n-select
          v-model:value="store.form.reward_model"
          multiple
          filterable
          :placeholder="$t('reward_model_placeholder')"
          size="tiny"
        />
      </n-form-item>
    </n-grid-item>
  </n-grid>
</template>

<script setup lang="ts">
import { useTrainFormStore } from "@/stores/trainForm";

const store = useTrainFormStore();

const lossOptions = [
  { label: "Sigmoid", value: "sigmoid" },
  { label: "Hinge", value: "hinge" },
  { label: "IPO", value: "ipo" },
  { label: "KTO Pair", value: "kto_pair" },
  { label: "ORPO", value: "orpo" },
  { label: "SimPO", value: "simpo" },
];
</script>
