<template>
  <n-space>
    <n-button
      size="tiny"
      :type="chat.modelLoaded ? 'warning' : 'primary'"
      :loading="loading"
      @click="handleToggle"
    >
      {{ chat.modelLoaded ? $t('unload_model') : $t('load_model') }}
    </n-button>
  </n-space>
</template>

<script setup lang="ts">
import { ref } from "vue";
import { useI18n } from "vue-i18n";
import { useMessage } from "naive-ui";
import { useChatStore } from "@/stores/chatStore";
import { useSessionStore } from "@/stores/session";
import { loadModel as apiLoadModel, unloadModel as apiUnloadModel } from "@/api/chat";

const { t } = useI18n();
const chat = useChatStore();
const session = useSessionStore();
const message = useMessage();
const loading = ref(false);

async function handleToggle(): Promise<void> {
  loading.value = true;
  try {
    if (chat.modelLoaded) {
      await apiUnloadModel();
      chat.setModelLoaded(false);
      chat.clearMessages();
      message.success(t("model_unloaded"));
    } else {
      await apiLoadModel({
        model_name: session.modelName,
        model_path: session.modelPath,
        finetuning_type: session.finetuningType,
        template: session.template,
        quantized_bit: session.quantizationBit,
        checkpoint_path: session.checkpointPath,
      });
      chat.setModelLoaded(true);
      message.success(t("model_loaded_success"));
    }
  } catch (err) {
    message.error(t("operation_failed"));
  } finally {
    loading.value = false;
  }
}
</script>
