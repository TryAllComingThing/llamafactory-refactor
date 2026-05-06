<template>
  <div class="train-view">
    <div class="train-layout">
      <!-- Left: Form Area -->
      <div class="train-form">
        <!-- Section: Data -->
        <div class="form-section">
          <span class="section-label">{{ $t('data') }}</span>
          <n-grid :cols="4" :x-gap="8" :y-gap="6">
            <n-grid-item>
              <n-form-item :label="$t('training_stage')" label-placement="top" size="tiny">
                <n-select v-model:value="store.form.training_stage" :options="stageOptions" size="tiny" />
              </n-form-item>
            </n-grid-item>
            <n-grid-item>
              <n-form-item :label="$t('dataset_dir')" label-placement="top" size="tiny">
                <n-input v-model:value="store.form.dataset_dir" size="tiny" />
              </n-form-item>
            </n-grid-item>
            <n-grid-item span="2">
              <n-form-item :label="$t('dataset')" label-placement="top" size="tiny">
                <div class="dataset-row">
                  <n-select
                    v-model:value="store.form.dataset"
                    multiple
                    filterable
                    :placeholder="$t('dataset_select_placeholder')"
                    :options="store.datasetOptions"
                    class="dataset-select"
                    size="tiny"
                  />
                  <n-button size="tiny" :disabled="!store.form.dataset.length" @click="showPreview = true">{{ $t('data_preview_btn') }}</n-button>
                </div>
              </n-form-item>
            </n-grid-item>
          </n-grid>
        </div>

        <!-- Section: Hyperparameters -->
        <div class="form-section">
          <span class="section-label">{{ $t('hyperparameters') }}</span>
          <n-grid :cols="5" :x-gap="8" :y-gap="6">
            <n-grid-item>
              <n-form-item :label="$t('learning_rate')" label-placement="top" size="tiny">
                <n-input v-model:value="store.form.learning_rate" placeholder="5e-5" size="tiny" />
              </n-form-item>
            </n-grid-item>
            <n-grid-item>
              <n-form-item :label="$t('num_train_epochs')" label-placement="top" size="tiny">
                <n-input v-model:value="store.form.num_train_epochs" placeholder="3" size="tiny" />
              </n-form-item>
            </n-grid-item>
            <n-grid-item>
              <n-form-item :label="$t('max_grad_norm')" label-placement="top" size="tiny">
                <n-input v-model:value="store.form.max_grad_norm" placeholder="1.0" size="tiny" />
              </n-form-item>
            </n-grid-item>
            <n-grid-item>
              <n-form-item :label="$t('max_samples')" label-placement="top" size="tiny">
                <n-input v-model:value="store.form.max_samples" :placeholder="$t('all_samples')" size="tiny" />
              </n-form-item>
            </n-grid-item>
            <n-grid-item>
              <n-form-item :label="$t('compute_type')" label-placement="top" size="tiny">
                <n-select v-model:value="store.form.compute_type" :options="computeOptions" size="tiny" />
              </n-form-item>
            </n-grid-item>
          </n-grid>
          <n-grid :cols="5" :x-gap="8" :y-gap="6" style="margin-top:6px">
            <n-grid-item>
              <n-form-item :label="$t('cutoff_len')" label-placement="top" size="tiny">
                <n-input-number v-model:value="store.form.cutoff_len" :min="4" :max="131072" :step="64" size="tiny" />
              </n-form-item>
            </n-grid-item>
            <n-grid-item>
              <n-form-item :label="$t('batch_size')" label-placement="top" size="tiny">
                <n-input-number v-model:value="batchSize" :min="1" :max="128" size="tiny" />
              </n-form-item>
            </n-grid-item>
            <n-grid-item>
              <n-form-item :label="$t('gradient_accumulation_steps')" label-placement="top" size="tiny">
                <n-input-number v-model:value="gradAccum" :min="1" :max="1024" size="tiny" />
              </n-form-item>
            </n-grid-item>
            <n-grid-item>
              <n-form-item :label="$t('val_size')" label-placement="top" size="tiny">
                <n-input-number v-model:value="store.form.val_size" :min="0" :max="1" :step="0.001" size="tiny" />
              </n-form-item>
            </n-grid-item>
            <n-grid-item>
              <n-form-item :label="$t('lr_scheduler_type')" label-placement="top" size="tiny">
                <n-select v-model:value="store.form.lr_scheduler_type" :options="schedulerOptions" size="tiny" />
              </n-form-item>
            </n-grid-item>
          </n-grid>
        </div>

        <!-- Collapse Panels -->
        <n-collapse class="train-collapse" :default-expanded-names="[]">
          <!-- Extra Settings -->
          <n-collapse-item :title="$t('extra_tab')" name="extra">
            <n-grid :cols="5" :x-gap="8" :y-gap="6">
              <n-grid-item>
                <n-form-item :label="$t('logging_steps')" label-placement="top" size="tiny">
                  <n-input-number v-model:value="store.form.logging_steps" :min="1" :max="1000" :step="5" size="tiny" />
                </n-form-item>
              </n-grid-item>
              <n-grid-item>
                <n-form-item :label="$t('save_steps')" label-placement="top" size="tiny">
                  <n-input-number v-model:value="store.form.save_steps" :min="10" :max="5000" :step="10" size="tiny" />
                </n-form-item>
              </n-grid-item>
              <n-grid-item>
                <n-form-item :label="$t('warmup_steps')" label-placement="top" size="tiny">
                  <n-input-number v-model:value="store.form.warmup_steps" :min="0" :max="5000" size="tiny" />
                </n-form-item>
              </n-grid-item>
              <n-grid-item>
                <n-form-item :label="$t('neoftune_alpha')" label-placement="top" size="tiny">
                  <n-input-number v-model:value="store.form.neftune_alpha" :min="0" :max="10" :step="0.1" size="tiny" />
                </n-form-item>
              </n-grid-item>
              <n-grid-item :span="3">
                <n-form-item :label="$t('extra_args')" label-placement="top" size="tiny">
                  <n-input v-model:value="store.form.extra_args" placeholder='{"optim": "adamw_torch"}' size="tiny" />
                </n-form-item>
              </n-grid-item>
            </n-grid>
            <n-grid :cols="5" :x-gap="8" :y-gap="6" style="margin-top:6px">
              <n-grid-item>
                <n-checkbox v-model:checked="store.form.packing">{{ $t('packing') }}</n-checkbox>
              </n-grid-item>
              <n-grid-item>
                <n-checkbox v-model:checked="store.form.neat_packing">{{ $t('neat_packing') }}</n-checkbox>
              </n-grid-item>
              <n-grid-item>
                <n-checkbox v-model:checked="store.form.train_on_prompt">{{ $t('train_on_prompt') }}</n-checkbox>
              </n-grid-item>
              <n-grid-item>
                <n-checkbox v-model:checked="store.form.mask_history">{{ $t('mask_history') }}</n-checkbox>
              </n-grid-item>
              <n-grid-item>
                <n-checkbox v-model:checked="store.form.resize_vocab">{{ $t('resize_vocab') }}</n-checkbox>
              </n-grid-item>
            </n-grid>
          </n-collapse-item>

          <!-- Freeze Settings -->
          <n-collapse-item :title="$t('freeze_tab')" name="freeze">
            <n-grid :cols="3" :x-gap="8" :y-gap="6">
              <n-grid-item>
                <n-form-item :label="$t('freeze_trainable_layers')" label-placement="top" size="tiny">
                  <n-input-number v-model:value="store.form.freeze_trainable_layers" :min="-128" :max="128" size="tiny" />
                </n-form-item>
              </n-grid-item>
              <n-grid-item>
                <n-form-item :label="$t('freeze_trainable_modules')" label-placement="top" size="tiny">
                  <n-input v-model:value="store.form.freeze_trainable_modules" size="tiny" />
                </n-form-item>
              </n-grid-item>
              <n-grid-item>
                <n-form-item :label="$t('freeze_extra_modules')" label-placement="top" size="tiny">
                  <n-input v-model:value="store.form.freeze_extra_modules" :placeholder="$t('optional')" size="tiny" />
                </n-form-item>
              </n-grid-item>
            </n-grid>
          </n-collapse-item>

          <!-- LoRA Settings -->
          <n-collapse-item :title="$t('lora_tab')" name="lora">
            <n-grid :cols="5" :x-gap="8" :y-gap="6">
              <n-grid-item>
                <n-form-item :label="$t('lora_rank')" label-placement="top" size="tiny">
                  <n-input-number v-model:value="store.form.lora_rank" :min="1" :max="1024" size="tiny" />
                </n-form-item>
              </n-grid-item>
              <n-grid-item>
                <n-form-item :label="$t('lora_alpha')" label-placement="top" size="tiny">
                  <n-input-number v-model:value="store.form.lora_alpha" :min="1" :max="2048" size="tiny" />
                </n-form-item>
              </n-grid-item>
              <n-grid-item>
                <n-form-item :label="$t('lora_dropout')" label-placement="top" size="tiny">
                  <n-input-number v-model:value="store.form.lora_dropout" :min="0" :max="1" :step="0.01" size="tiny" />
                </n-form-item>
              </n-grid-item>
              <n-grid-item>
                <n-form-item :label="$t('loraplus_lr_ratio')" label-placement="top" size="tiny">
                  <n-input-number v-model:value="store.form.loraplus_lr_ratio" :min="0" :max="64" :step="0.01" size="tiny" />
                </n-form-item>
              </n-grid-item>
              <n-grid-item :span="3">
                <n-form-item :label="$t('lora_target')" label-placement="top" size="tiny">
                  <n-input v-model:value="store.form.lora_target" placeholder="q_proj,v_proj" size="tiny" />
                </n-form-item>
              </n-grid-item>
            </n-grid>
            <n-grid :cols="4" :x-gap="8" :y-gap="6" style="margin-top:6px">
              <n-grid-item>
                <n-checkbox v-model:checked="store.form.use_rslora">{{ $t('use_rslora') }}</n-checkbox>
              </n-grid-item>
              <n-grid-item>
                <n-checkbox v-model:checked="store.form.use_dora">{{ $t('use_dora') }}</n-checkbox>
              </n-grid-item>
              <n-grid-item>
                <n-checkbox v-model:checked="store.form.use_pissa">{{ $t('use_pissa') }}</n-checkbox>
              </n-grid-item>
              <n-grid-item>
                <n-checkbox v-model:checked="store.form.create_new_adapter">{{ $t('create_new_adapter') }}</n-checkbox>
              </n-grid-item>
            </n-grid>
          </n-collapse-item>

          <!-- RLHF Settings -->
          <n-collapse-item :title="$t('rlhf_tab')" name="rlhf">
            <RlhfConfig />
          </n-collapse-item>

          <!-- Multimodal Settings -->
          <n-collapse-item :title="$t('mm_tab')" name="multimodal">
            <MultimodalConfig />
          </n-collapse-item>

          <!-- GaLore Settings -->
          <n-collapse-item :title="$t('galore_tab')" name="galore">
            <n-grid :cols="5" :x-gap="8" :y-gap="6">
              <n-grid-item>
                <n-form-item label-placement="top" size="tiny">
                  <n-checkbox v-model:checked="store.form.use_galore">{{ $t('use_galore') }}</n-checkbox>
                </n-form-item>
              </n-grid-item>
              <n-grid-item>
                <n-form-item :label="$t('galore_rank')" label-placement="top" size="tiny">
                  <n-input-number v-model:value="store.form.galore_rank" :min="1" :max="128" size="tiny" />
                </n-form-item>
              </n-grid-item>
              <n-grid-item>
                <n-form-item :label="$t('galore_update_interval')" label-placement="top" size="tiny">
                  <n-input-number v-model:value="store.form.galore_update_interval" :min="1" :max="1000" size="tiny" />
                </n-form-item>
              </n-grid-item>
              <n-grid-item>
                <n-form-item :label="$t('galore_scale')" label-placement="top" size="tiny">
                  <n-input-number v-model:value="store.form.galore_scale" :min="0" :max="1" :step="0.01" size="tiny" />
                </n-form-item>
              </n-grid-item>
              <n-grid-item :span="3">
                <n-form-item :label="$t('galore_target')" label-placement="top" size="tiny">
                  <n-input v-model:value="store.form.galore_target" size="tiny" />
                </n-form-item>
              </n-grid-item>
            </n-grid>
          </n-collapse-item>

          <!-- APOLLO Settings -->
          <n-collapse-item :title="$t('apollo_tab')" name="apollo">
            <n-grid :cols="5" :x-gap="8" :y-gap="6">
              <n-grid-item>
                <n-form-item label-placement="top" size="tiny">
                  <n-checkbox v-model:checked="store.form.use_apollo">{{ $t('use_apollo') }}</n-checkbox>
                </n-form-item>
              </n-grid-item>
              <n-grid-item>
                <n-form-item :label="$t('apollo_rank')" label-placement="top" size="tiny">
                  <n-input-number v-model:value="store.form.apollo_rank" :min="1" :max="128" size="tiny" />
                </n-form-item>
              </n-grid-item>
              <n-grid-item>
                <n-form-item :label="$t('apollo_update_interval')" label-placement="top" size="tiny">
                  <n-input-number v-model:value="store.form.apollo_update_interval" :min="1" :max="1000" size="tiny" />
                </n-form-item>
              </n-grid-item>
              <n-grid-item>
                <n-form-item :label="$t('apollo_scale')" label-placement="top" size="tiny">
                  <n-input-number v-model:value="store.form.apollo_scale" :min="0" :max="1" :step="0.01" size="tiny" />
                </n-form-item>
              </n-grid-item>
              <n-grid-item :span="3">
                <n-form-item :label="$t('apollo_target')" label-placement="top" size="tiny">
                  <n-input v-model:value="store.form.apollo_target" size="tiny" />
                </n-form-item>
              </n-grid-item>
            </n-grid>
          </n-collapse-item>

          <!-- BAdam Settings -->
          <n-collapse-item :title="$t('badam_tab')" name="badam">
            <n-grid :cols="5" :x-gap="8" :y-gap="6">
              <n-grid-item>
                <n-form-item label-placement="top" size="tiny">
                  <n-checkbox v-model:checked="store.form.use_badam">{{ $t('use_badam') }}</n-checkbox>
                </n-form-item>
              </n-grid-item>
              <n-grid-item>
                <n-form-item :label="$t('badam_mode')" label-placement="top" size="tiny">
                  <n-select v-model:value="store.form.badam_mode" :options="badamModeOptions" size="tiny" />
                </n-form-item>
              </n-grid-item>
              <n-grid-item>
                <n-form-item :label="$t('badam_switch_mode')" label-placement="top" size="tiny">
                  <n-select v-model:value="store.form.badam_switch_mode" :options="badamSwitchModeOptions" size="tiny" />
                </n-form-item>
              </n-grid-item>
              <n-grid-item>
                <n-form-item :label="$t('badam_switch_interval')" label-placement="top" size="tiny">
                  <n-input-number v-model:value="store.form.badam_switch_interval" :min="1" :max="1000" size="tiny" />
                </n-form-item>
              </n-grid-item>
              <n-grid-item>
                <n-form-item :label="$t('badam_update_ratio')" label-placement="top" size="tiny">
                  <n-input-number v-model:value="store.form.badam_update_ratio" :min="0.01" :max="1" :step="0.01" size="tiny" />
                </n-form-item>
              </n-grid-item>
            </n-grid>
          </n-collapse-item>

          <!-- SwanLab Settings -->
          <n-collapse-item :title="$t('swanlab_track')" name="swanlab">
            <SwanLabConfig />
          </n-collapse-item>
        </n-collapse>

        <!-- Action Buttons Row -->
        <div class="action-row">
          <n-space size="small">
            <n-button size="tiny" @click="handlePreview">{{ $t('cmd_preview_btn') }}</n-button>
            <n-button size="tiny" @click="handleSave">{{ $t('arg_save_btn') }}</n-button>
            <n-button size="tiny" @click="handleLoad">{{ $t('arg_load_btn') }}</n-button>
            <n-button v-if="runId" size="tiny" type="error" @click="handleAbort">{{ $t('stop_btn') }}</n-button>
            <n-button v-if="!runId && session.trainRunId" size="tiny" @click="handleResume">{{ $t('resume_btn') }}</n-button>
            <n-button v-if="!runId" size="tiny" type="primary" @click="handleStart">{{ $t('start_btn') }}</n-button>
          </n-space>
        </div>

        <!-- Output Section -->
        <div class="form-section output-section">
          <span class="section-label">{{ $t('output') }}</span>
          <n-grid :cols="5" :x-gap="8" :y-gap="6">
            <n-grid-item>
              <n-form-item :label="$t('output_dir')" label-placement="top" size="tiny">
                <n-auto-complete
                  v-model:value="outputDir"
                  :options="outputDirOptions"
                  :placeholder="$t('output_dir')"
                  size="tiny"
                />
              </n-form-item>
            </n-grid-item>
            <n-grid-item>
              <n-form-item :label="$t('config_path')" label-placement="top" size="tiny">
                <n-auto-complete
                  v-model:value="configPath"
                  :options="configPathOptions"
                  :placeholder="$t('config_path')"
                  @focus="loadConfigPaths"
                  size="tiny"
                />
              </n-form-item>
            </n-grid-item>
            <n-grid-item>
              <n-form-item :label="$t('device_count')" label-placement="top" size="tiny">
                <n-input-number v-model:value="store.form.device_count" :min="1" :max="64" placeholder="1" size="tiny" />
              </n-form-item>
            </n-grid-item>
            <n-grid-item>
              <n-form-item :label="$t('ds_stage')" label-placement="top" size="tiny">
                <n-select v-model:value="store.form.ds_stage" :options="dsStageOptions" size="tiny" />
              </n-form-item>
            </n-grid-item>
            <n-grid-item>
              <n-form-item :label="$t('ds_offload')" label-placement="top" size="tiny">
                <n-checkbox v-model:checked="store.form.ds_offload">offload</n-checkbox>
              </n-form-item>
            </n-grid-item>
          </n-grid>
        </div>
      </div>

      <!-- Right: Loss Chart -->
      <div class="train-chart">
        <n-tabs type="line" animated>
          <n-tab-pane name="loss" :tab="$t('loss_viewer')">
            <TrainMonitor :run-id="runId" />
          </n-tab-pane>
        </n-tabs>
      </div>
    </div>

    <!-- Dataset Preview Modal -->
    <n-modal v-model:show="showPreview" :title="$t('data_preview_btn')" preset="card" style="width:900px">
      <DatasetPreview
        :dataset="store.form.dataset"
        :dataset-dir="store.form.dataset_dir"
        @close="showPreview = false"
      />
    </n-modal>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, watch, onMounted } from "vue";
import { useI18n } from "vue-i18n";
import { useMessage } from "naive-ui";
import { useTrainFormStore } from "@/stores/trainForm";
import { useSessionStore } from "@/stores/session";
import { getJson, postJson } from "@/api/client";
import { previewTrain, startTrain, abortTrain } from "@/api/train";
import TrainMonitor from "@/components/train/TrainMonitor.vue";
import DatasetPreview from "@/components/common/DatasetPreview.vue";
import RlhfConfig from "@/components/train/RlhfConfig.vue";
import MultimodalConfig from "@/components/train/MultimodalConfig.vue";
import SwanLabConfig from "@/components/train/SwanLabConfig.vue";

const { t } = useI18n();
const store = useTrainFormStore();
const session = useSessionStore();
const message = useMessage();
const runId = ref("");
const showPreview = ref(false);
const configPath = ref("");
const outputDir = ref("");
const statusText = ref(t("status_ready_short"));
const configPathOptions = ref<{ label: string; value: string }[]>([]);
const outputDirOptions = ref<{ label: string; value: string }[]>([]);
const checkingOutputDir = ref(false);

async function loadConfigPaths(): Promise<void> {
  try {
    const data = await getJson<string[]>("/configs");
    configPathOptions.value = data.map((f: string) => ({ label: f, value: f }));
    if (!configPath.value && data.length > 0) {
      configPath.value = data[0];
    }
  } catch {
    configPathOptions.value = [];
  }
}

async function loadOutputDirs(): Promise<void> {
  try {
    const data = await getJson<string[]>("/output-dirs", {
      model: session.modelName,
      finetuning_type: session.finetuningType,
      prefix: "train",
    });
    outputDirOptions.value = data.map((d: string) => ({ label: d, value: d }));
    if (!outputDir.value && data.length > 0) {
      outputDir.value = data[0];
    }
  } catch {
    outputDirOptions.value = [];
  }
}

const batchSize = computed({
  get: () => store.form.batch_size,
  set: (val: number) => { store.form.batch_size = val; },
});

const gradAccum = computed({
  get: () => store.form.gradient_accumulation_steps,
  set: (val: number) => { store.form.gradient_accumulation_steps = val; },
});

const stageOptions = [
  { label: "Supervised Fine-Tuning", value: "sft" },
  { label: "Reward Modeling", value: "rm" },
  { label: "PPO", value: "ppo" },
  { label: "DPO", value: "dpo" },
  { label: "Pre-Training", value: "pt" },
];

const computeOptions = [
  { label: "bf16", value: "bf16" },
  { label: "fp16", value: "fp16" },
  { label: "fp32", value: "fp32" },
  { label: "pure_bf16", value: "pure_bf16" },
];

const schedulerOptions = [
  { label: "linear", value: "linear" },
  { label: "cosine", value: "cosine" },
  { label: "cosine_with_restarts", value: "cosine_with_restarts" },
  { label: "polynomial", value: "polynomial" },
  { label: "constant", value: "constant" },
  { label: "constant_with_warmup", value: "constant_with_warmup" },
];

const badamModeOptions = [
  { label: "layer", value: "layer" },
  { label: "block", value: "block" },
];

const badamSwitchModeOptions = [
  { label: "ascending", value: "ascending" },
  { label: "descending", value: "descending" },
  { label: "random", value: "random" },
];

const dsStageOptions = [
  { label: "none", value: "none" },
  { label: "stage1", value: "stage1" },
  { label: "stage2", value: "stage2" },
  { label: "stage3", value: "stage3" },
];

function buildTrainParams(): Record<string, unknown> {
  return {
    ...store.toParams(),
    model_name: session.modelName,
    model_path: session.modelPath,
    finetuning_type: session.finetuningType,
    template: session.template,
    quantized_bit: session.quantizationBit,
    quantization_method: session.quantizationMethod,
    rope_scaling: session.ropeScaling,
    booster: session.booster,
    checkpoint_path: session.checkpointPath,
    hub_name: session.hubName,
  };
}

async function handleStart(): Promise<void> {
  try {
    const params = buildTrainParams();
    const result = await startTrain(params);
    runId.value = result.run_id;
    session.trainRunId = result.run_id;
    session.persistToCache();
    statusText.value = t("training_started");
    message.success(t("training_started"));
  } catch {
    statusText.value = t("training_failed");
    message.error(t("operation_failed"));
  }
}

async function handleResume(): Promise<void> {
  if (!session.trainRunId) return;
  // Try to reconnect to the persisted run
  try {
    const status = await getJson<{ running: boolean; run_id: string }>("/train/status");
    if (status.running && status.run_id === session.trainRunId) {
      runId.value = session.trainRunId;
      message.success(t("resume_btn"));
    } else {
      message.warning(t("training_completed"));
      session.trainRunId = "";
      session.persistToCache();
    }
  } catch {
    message.error(t("operation_failed"));
  }
}

async function handlePreview(): Promise<void> {
  try {
    const params = buildTrainParams();
    const result = await previewTrain(params);
    message.info(result.command.join("\n"));
  } catch {
    message.error(t("operation_failed"));
  }
}

async function handleAbort(): Promise<void> {
  try {
    await abortTrain();
    runId.value = "";
    session.trainRunId = "";
    session.persistToCache();
    statusText.value = t("training_aborted");
    message.info(t("abort_sent"));
  } catch {
    message.error(t("operation_failed"));
  }
}

async function handleSave(): Promise<void> {
  if (!configPath.value) {
    message.warning(t("arg_save_empty"));
    return;
  }
  try {
    const params = { ...store.toParams(), ...sessionToParams() };
    await postJson("/configs/" + encodeURIComponent(configPath.value), params as Record<string, unknown>);
    loadConfigPaths();
    message.success(t("arg_saved"));
  } catch {
    message.error(t("operation_failed"));
  }
}

function sessionToParams(): Record<string, unknown> {
  return {
    model_name: session.modelName,
    model_path: session.modelPath,
    finetuning_type: session.finetuningType,
    template: session.template,
    quantization_bit: session.quantizationBit,
    quantization_method: session.quantizationMethod,
    rope_scaling: session.ropeScaling,
    booster: session.booster,
    checkpoint_path: session.checkpointPath,
    hub_name: session.hubName,
  };
}

async function handleLoad(): Promise<void> {
  if (!configPath.value) {
    message.warning(t("optional"));
    return;
  }
  try {
    const data = await getJson<Record<string, unknown>>("/configs/" + encodeURIComponent(configPath.value));

    // Restore session (Top Bar) fields from loaded config
    if (data.model_name) session.modelName = data.model_name as string;
    if (data.model_path) session.modelPath = data.model_path as string;
    if (data.finetuning_type) session.finetuningType = data.finetuning_type as string;
    if (data.template) session.template = data.template as string;
    if (data.quantization_bit) session.quantizationBit = data.quantization_bit as string;
    if (data.quantization_method) session.quantizationMethod = data.quantization_method as string;
    if (data.rope_scaling) session.ropeScaling = data.rope_scaling as string;
    if (data.booster) session.booster = data.booster as string;
    if (data.checkpoint_path) {
      session.checkpointPath = Array.isArray(data.checkpoint_path)
        ? (data.checkpoint_path as string[])
        : [data.checkpoint_path as string];
    }
    session.persistToCache();

    store.updateFields(data as Partial<typeof store.form>);
    message.success(t("arg_loaded"));
  } catch {
    message.error(t("operation_failed"));
  }
}

// Watch output_dir changes for auto-detection
// Refresh output dirs when model or finetuning method changes (matches Gradio behavior)
watch(() => [session.modelName, session.finetuningType], () => {
  loadOutputDirs();
});

watch(outputDir, async (newDir) => {
  if (!newDir || !session.modelName || checkingOutputDir.value) return;
  checkingOutputDir.value = true;
  try {
    const result = await getJson<{
      exists: boolean;
      warning: string;
      config: Record<string, unknown> | null;
    }>("/output-dir/check", {
      model_name: session.modelName,
      finetuning_type: session.finetuningType,
      output_dir: newDir,
    });
    if (result.exists) {
      message.warning(result.warning);
      if (result.config) {
        store.updateFields(result.config as Partial<typeof store.form>);
        // Also restore session fields from saved config
        if (result.config.model_name) session.modelName = result.config.model_name as string;
        if (result.config.finetuning_type) session.finetuningType = result.config.finetuning_type as string;
        if (result.config.template) session.template = result.config.template as string;
      }
    }
  } catch {
    // Silently ignore - dir check is optional
  } finally {
    checkingOutputDir.value = false;
  }
});

onMounted(async () => {
  loadConfigPaths();
  loadOutputDirs();

  // Check if training is running (for resume after page reload)
  try {
    const status = await getJson<{ running: boolean; run_id: string }>("/train/status");
    if (status.running && status.run_id) {
      runId.value = status.run_id;
      session.trainRunId = status.run_id;
      session.persistToCache();
    }
  } catch {
    // API not available - use cached runId if any
    if (session.trainRunId) {
      try {
        const status = await getJson<{ running: boolean; run_id: string }>("/train/status");
        if (status.running && status.run_id === session.trainRunId) {
          runId.value = session.trainRunId;
        }
      } catch {
        // Keep cached value, show resume option
      }
    }
  }
});
</script>

<style scoped>
.train-view {
  max-width: none;
  padding: 0 var(--spacing-6);
}

.train-layout {
  display: grid;
  grid-template-columns: 1fr 400px;
  gap: var(--spacing-4);
}

.train-form {
  min-width: 0;
}

.train-chart {
  position: sticky;
  top: var(--spacing-3);
  height: fit-content;
  background: var(--bg-surface);
  border: 1px solid var(--border-default);
  border-radius: var(--radius-md);
  padding: var(--spacing-3);
}

.form-section {
  margin-bottom: var(--spacing-3);
  padding: var(--spacing-3);
  background: var(--bg-surface);
  border: 1px solid var(--border-default);
  border-radius: var(--radius-sm);
}

.section-label {
  font-size: var(--font-size-sm);
  font-weight: var(--font-weight-medium);
  color: var(--text-primary);
  display: block;
  margin-bottom: var(--spacing-2);
}

.dataset-row {
  display: flex;
  gap: var(--spacing-2);
  align-items: center;
}

.dataset-row .dataset-select {
  flex: 1;
}

.train-collapse {
  margin-bottom: var(--spacing-3);
}

.train-collapse :deep(.n-collapse-item__header) {
  font-size: var(--font-size-sm);
  font-weight: var(--font-weight-medium);
  padding: var(--spacing-2) var(--spacing-3);
  background: var(--bg-elevated);
  border-radius: var(--radius-sm);
  margin-bottom: var(--spacing-1);
  cursor: pointer;
}

.train-collapse :deep(.n-collapse-item__content) {
  padding: var(--spacing-3);
  background: var(--bg-surface);
  border: 1px solid var(--border-default);
  border-radius: var(--radius-sm);
  margin-top: var(--spacing-1);
}

.output-section {
  margin-top: var(--spacing-4);
  background: var(--bg-surface);
  border: 1px solid var(--border-default);
  border-radius: var(--radius-sm);
}

.action-row {
  display: flex;
  align-items: center;
  justify-content: flex-start;
  margin-top: var(--spacing-3);
  padding-top: var(--spacing-3);
  border-top: 1px solid var(--border-default);
}


@media (max-width: 1400px) {
  .train-layout {
    grid-template-columns: 1fr;
  }

  .train-chart {
    position: static;
    margin-top: var(--spacing-4);
  }
}
</style>
