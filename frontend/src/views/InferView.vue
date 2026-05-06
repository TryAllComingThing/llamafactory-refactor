<template>
  <div class="infer-view">
    <!-- Section: Infer Settings -->
    <div class="form-section">
      <n-grid :cols="3" :x-gap="8" :y-gap="6">
        <n-grid-item>
          <n-form-item :label="$t('infer_backend')" label-placement="top" size="tiny">
            <n-select v-model:value="chat.inferBackend" :options="backendOptions" size="tiny" />
          </n-form-item>
        </n-grid-item>
        <n-grid-item>
          <n-form-item :label="$t('infer_dtype')" label-placement="top" size="tiny">
            <n-select v-model:value="chat.inferDtype" :options="dtypeOptions" size="tiny" />
          </n-form-item>
        </n-grid-item>
        <n-grid-item>
          <n-form-item :label="$t('extra_args')" label-placement="top" size="tiny">
            <n-input v-model:value="chat.extraArgs" placeholder='{"vllm_enforce_eager": true}' size="tiny" />
          </n-form-item>
        </n-grid-item>
      </n-grid>
    </div>

    <!-- Section: Load/Unload Model Button -->
    <div class="model-control-section">
      <n-space :size="8" style="width: 100%">
        <n-button
          :type="chat.modelLoaded ? 'warning' : 'primary'"
          :loading="loading"
          @click="handleToggleModel"
          style="flex: 1"
          size="large"
        >
          {{ chat.modelLoaded ? $t('unload_model') : $t('load_model') }}
        </n-button>
      </n-space>
    </div>

    <!-- Section: Chat Area -->
    <div class="chat-wrapper">
      <div class="chat-left">
        <ChatBox ref="chatBoxRef" />
      </div>
      <div class="chat-params">
        <span class="section-label">{{ $t('infer_config') }}</span>
        <n-form-item :label="$t('max_new_tokens')" label-placement="top" size="tiny">
          <n-input-number v-model:value="chat.maxNewTokens" :min="1" :max="32768" :step="1" size="tiny" />
        </n-form-item>
        <n-form-item :label="$t('top_p')" label-placement="top" size="tiny">
          <n-slider v-model:value="chat.topP" :min="0" :max="1" :step="0.01" style="width: 100%" />
          <span class="slider-value">{{ chat.topP.toFixed(2) }}</span>
        </n-form-item>
        <n-form-item :label="$t('temperature')" label-placement="top" size="tiny">
          <n-slider v-model:value="chat.temperature" :min="0" :max="2" :step="0.01" style="width: 100%" />
          <span class="slider-value">{{ chat.temperature.toFixed(2) }}</span>
        </n-form-item>
        <n-form-item :label="$t('skip_special_tokens')" label-placement="top" size="tiny">
          <n-switch v-model:value="chat.skipSpecialTokens" size="small" />
        </n-form-item>
        <n-form-item :label="$t('escape_html')" label-placement="top" size="tiny">
          <n-switch v-model:value="chat.escapeHtml" size="small" />
        </n-form-item>
        <n-form-item :label="$t('enable_thinking')" label-placement="top" size="tiny">
          <n-switch v-model:value="chat.enableThinking" size="small" />
        </n-form-item>
        <n-button
          size="tiny"
          :disabled="!chat.modelLoaded"
          @click="chatBoxRef?.handleClear()"
          style="width: 100%"
        >
          {{ $t('clear_btn') }}
        </n-button>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref } from "vue";
import { useI18n } from "vue-i18n";
import { useMessage } from "naive-ui";
import { useChatStore } from "@/stores/chatStore";
import { useSessionStore } from "@/stores/session";
import { loadModel as apiLoadModel, unloadModel as apiUnloadModel } from "@/api/chat";
import ChatBox from "@/components/chat/ChatBox.vue";

const { t } = useI18n();
const chat = useChatStore();
const session = useSessionStore();
const message = useMessage();
const chatBoxRef = ref<InstanceType<typeof ChatBox> | null>(null);
const loading = ref(false);

const backendOptions = [
  { label: "HuggingFace", value: "huggingface" },
  { label: "vLLM", value: "vllm" },
  { label: "SGLang", value: "sglang" },
];

const dtypeOptions = [
  { label: "Auto", value: "auto" },
  { label: "Float16", value: "float16" },
  { label: "BFloat16", value: "bfloat16" },
  { label: "Float32", value: "float32" },
];

async function handleToggleModel(): Promise<void> {
  loading.value = true;
  try {
    if (chat.modelLoaded) {
      await apiUnloadModel();
      chat.setModelLoaded(false);
      chatBoxRef.value?.handleClear();
      message.success(t("model_unloaded"));
    } else {
      await apiLoadModel({
        model_name: session.modelName,
        model_path: session.modelPath,
        finetuning_type: session.finetuningType,
        template: session.template,
        quantized_bit: session.quantizationBit,
        checkpoint_path: session.checkpointPath,
        infer_backend: chat.inferBackend,
        infer_dtype: chat.inferDtype,
        extra_args: chat.extraArgs,
      });
      chat.setModelLoaded(true);
      message.success(t("model_loaded_success"));
    }
  } catch {
    message.error(t("operation_failed"));
  } finally {
    loading.value = false;
  }
}
</script>

<style scoped>
.infer-view {
  max-width: none;
  padding: 0 var(--spacing-6);
}

.form-section {
  margin-bottom: var(--spacing-4);
}

.model-control-section {
  margin-bottom: var(--spacing-4);
}

.model-control-section :deep(.n-button) {
  height: 48px;
  font-size: var(--font-size-base);
  font-weight: var(--font-weight-medium);
}

.chat-wrapper {
  margin-top: var(--spacing-4);
  display: flex;
  gap: var(--spacing-4);
  align-items: flex-start;
}

.chat-left {
  flex: 1;
  min-width: 0;
}

.chat-params {
  width: 240px;
  flex-shrink: 0;
  border: 1px solid var(--border-default);
  border-radius: var(--radius-md);
  background: var(--bg-surface);
  padding: var(--spacing-3);
  display: flex;
  flex-direction: column;
  gap: var(--spacing-2);
}

.section-label {
  font-size: var(--font-size-sm);
  font-weight: var(--font-weight-medium);
  color: var(--text-secondary);
  margin-bottom: var(--spacing-1);
}

.slider-value {
  font-size: var(--font-size-xs);
  color: var(--text-tertiary);
  margin-left: var(--spacing-2);
}
</style>
