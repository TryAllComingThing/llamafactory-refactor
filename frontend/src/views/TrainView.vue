<template>
  <div class="train-view">
    <!-- Model config panel -->
    <ModelConfig />

    <!-- Train form -->
    <n-collapse class="train-form-collapse">
      <n-collapse-item title="基础配置" name="basic">
        <n-space vertical size="medium">
          <n-grid :cols="2" :x-gap="16" :y-gap="12">
            <n-grid-item>
              <n-form-item :label="$t('training_stage')">
                <n-select
                  v-model:value="store.form.training_stage"
                  :options="stageOptions"
                />
              </n-form-item>
            </n-grid-item>
            <n-grid-item>
              <n-form-item :label="$t('dataset')">
                <n-select
                  v-model:value="store.form.dataset"
                  multiple
                  filterable
                  placeholder="选择数据集"
                  :options="store.datasetOptions"
                />
              </n-form-item>
            </n-grid-item>
            <n-grid-item>
              <n-form-item :label="$t('learning_rate')">
                <n-input v-model:value="store.form.learning_rate" placeholder="5e-5" />
              </n-form-item>
            </n-grid-item>
            <n-grid-item>
              <n-form-item :label="$t('num_train_epochs')">
                <n-input v-model:value="store.form.num_train_epochs" placeholder="3" />
              </n-form-item>
            </n-grid-item>
          </n-grid>
        </n-space>
      </n-collapse-item>

      <n-collapse-item :title="$t('extra_tab')" name="advanced">
        <n-grid :cols="2" :x-gap="16" :y-gap="12">
          <n-grid-item>
            <n-form-item :label="$t('max_samples')">
              <n-input v-model:value="store.form.max_samples" placeholder="可选" />
            </n-form-item>
          </n-grid-item>
          <n-grid-item>
            <n-form-item :label="$t('batch_size')">
              <n-input-number
                v-model:value="batchSize"
                :min="1"
                :max="128"
              />
            </n-form-item>
          </n-grid-item>
          <n-grid-item>
            <n-form-item :label="$t('gradient_accumulation_steps')">
              <n-input-number
                v-model:value="gradAccum"
                :min="1"
                :max="64"
              />
            </n-form-item>
          </n-grid-item>
          <n-grid-item>
            <n-form-item :label="$t('lr_scheduler_type')">
              <n-select
                v-model:value="store.form.lr_scheduler_type"
                :options="schedulerOptions"
              />
            </n-form-item>
          </n-grid-item>
        </n-grid>
      </n-collapse-item>

      <n-collapse-item :title="$t('lora_tab')" name="lora">
        <n-grid :cols="2" :x-gap="16" :y-gap="12">
          <n-grid-item>
            <n-form-item :label="$t('lora_rank')">
              <n-input-number v-model:value="store.form.lora_rank" :min="1" :max="512" />
            </n-form-item>
          </n-grid-item>
          <n-grid-item>
            <n-form-item :label="$t('lora_alpha')">
              <n-input-number v-model:value="store.form.lora_alpha" :min="1" :max="512" />
            </n-form-item>
          </n-grid-item>
          <n-grid-item span="2">
            <n-form-item :label="$t('lora_target')">
              <n-input v-model:value="store.form.lora_target" placeholder="q_proj,v_proj" />
            </n-form-item>
          </n-grid-item>
        </n-grid>
      </n-collapse-item>

      <RlhfConfig />
      <MultimodalConfig />
      <OptimizerConfig />
      <SwanLabConfig />
      <DeepSpeedConfig />
    </n-collapse>

    <TrainMonitor />

    <!-- Actions -->
    <n-space class="train-actions" justify="center" size="large">
      <n-button type="primary" size="large" @click="handleStart">
        {{ $t("start_btn") }}
      </n-button>
      <n-button size="large" @click="handlePreview">
        {{ $t("cmd_preview_btn") }}
      </n-button>
      <n-button size="large" @click="handleSave">
        {{ $t("arg_save_btn") }}
      </n-button>
    </n-space>
  </div>
</template>

<script setup lang="ts">
import { computed } from "vue";
import { useMessage } from "naive-ui";
import { useTrainFormStore } from "@/stores/trainForm";
import RlhfConfig from "@/components/train/RlhfConfig.vue";
import MultimodalConfig from "@/components/train/MultimodalConfig.vue";
import OptimizerConfig from "@/components/train/OptimizerConfig.vue";
import SwanLabConfig from "@/components/train/SwanLabConfig.vue";
import DeepSpeedConfig from "@/components/train/DeepSpeedConfig.vue";
import TrainMonitor from "@/components/train/TrainMonitor.vue";

const store = useTrainFormStore();
const message = useMessage();

const batchSize = computed({
  get: () => store.form.per_device_train_batch_size,
  set: (val: number) => {
    store.form.per_device_train_batch_size = val;
  },
});

const gradAccum = computed({
  get: () => store.form.gradient_accumulation_steps,
  set: (val: number) => {
    store.form.gradient_accumulation_steps = val;
  },
});

const stageOptions = [
  { label: "Supervised Fine-Tuning (SFT)", value: "sft" },
  { label: "Reward Modeling", value: "rm" },
  { label: "PPO", value: "ppo" },
  { label: "DPO", value: "dpo" },
  { label: "Pre-Training", value: "pt" },
];

const schedulerOptions = [
  { label: "线性", value: "linear" },
  { label: "余弦", value: "cosine" },
  { label: "余弦重启", value: "cosine_with_restarts" },
  { label: "多项式", value: "polynomial" },
  { label: "常数", value: "constant" },
  { label: "常数预热", value: "constant_with_warmup" },
];

function handleStart(): void {
  message.info("训练启动（待 API 接入）");
}

function handlePreview(): void {
  message.info("命令预览（待 API 接入）");
}

function handleSave(): void {
  message.info("参数保存（待 API 接入）");
}
</script>

<style scoped>
.train-view {
  max-width: 960px;
}

.train-form-collapse {
  margin-bottom: var(--spacing-6);
}

.train-actions {
  margin-top: var(--spacing-4);
}
</style>
