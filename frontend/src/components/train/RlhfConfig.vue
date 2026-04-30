<template>
  <n-collapse-item :title="$t('rlhf_tab')" name="rlhf">
    <n-grid :cols="2" :x-gap="16" :y-gap="12">
      <n-grid-item>
        <n-form-item :label="$t('pref_beta')">
          <n-input-number
            v-model:value="store.form.pref_beta"
            :min="0.0"
            :max="1.0"
            :step="0.01"
          />
        </n-form-item>
      </n-grid-item>
      <n-grid-item>
        <n-form-item :label="$t('pref_ftx')">
          <n-input-number
            v-model:value="store.form.pref_ftx"
            :min="0.0"
            :max="10.0"
            :step="0.1"
          />
        </n-form-item>
      </n-grid-item>
      <n-grid-item>
        <n-form-item :label="$t('pref_loss')">
          <n-select
            v-model:value="store.form.pref_loss"
            :options="lossOptions"
          />
        </n-form-item>
      </n-grid-item>
      <n-grid-item>
        <n-form-item :label="$t('ppo_score_norm')">
          <n-switch v-model:value="store.form.ppo_score_norm" />
        </n-form-item>
      </n-grid-item>
      <n-grid-item>
        <n-form-item :label="$t('ppo_whiten_rewards')">
          <n-switch v-model:value="store.form.ppo_whiten_rewards" />
        </n-form-item>
      </n-grid-item>
      <n-grid-item>
        <n-form-item :label="$t('reward_model')">
          <n-select
            v-model:value="store.form.reward_model"
            multiple
            filterable
            :placeholder="$t('reward_model_placeholder')"
          />
        </n-form-item>
      </n-grid-item>
    </n-grid>
  </n-collapse-item>
</template>

<script setup lang="ts">
import { useTrainFormStore } from "@/stores/trainForm";

const store = useTrainFormStore();

const lossOptions = [
  { label: "Sigmoid", value: "sigmoid" },
  { label: "IPO", value: "ipo" },
  { label: "KTO", value: "kto" },
  { label: "CPO", value: "cpo" },
  { label: "SimPO", value: "simpo" },
  { label: "ORPO", value: "orpo" },
];
</script>
