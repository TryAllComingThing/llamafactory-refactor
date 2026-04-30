<template>
  <n-card :title="$t('chat_title')" class="chat-card">
    <template #header-extra>
      <n-space>
        <ModelControl />
        <n-button size="small" @click="handleClear">
          {{ $t('clear_chat') }}
        </n-button>
      </n-space>
    </template>

    <div class="chat-messages" ref="messagesRef">
      <div
        v-for="(msg, i) in chat.messages"
        :key="i"
        :class="['message', msg.role === 'user' ? 'message--user' : 'message--assistant']"
      >
        <div class="message-label">
          {{ msg.role === "user" ? $t('chat_user') : $t('chat_assistant') }}
        </div>
        <div v-if="msg.files" class="message-files">
          <img
            v-for="(file, fi) in msg.files"
            :key="fi"
            :src="file"
            class="message-image"
            :alt="$t('upload_image')"
          />
        </div>
        <div class="message-content">{{ msg.content }}</div>
      </div>

      <div v-if="chat.streamingResponse" class="message message--assistant">
        <div class="message-label">{{ $t('chat_assistant') }}</div>
        <div class="message-content streaming">{{ chat.streamingResponse }}</div>
      </div>
    </div>

    <template #footer>
      <div class="input-area">
        <div v-if="previewImages.length" class="image-preview-bar">
          <div v-for="(url, i) in previewImages" :key="i" class="image-preview-item">
            <img :src="url" :alt="$t('upload_image')" />
            <n-button
              size="tiny"
              circle
              quaternary
              class="image-remove"
              @click="removeImage(i)"
            >
              ✕
            </n-button>
          </div>
        </div>
        <n-input-group>
          <n-button :disabled="!chat.modelLoaded" @click="handleUploadImage">
            <template #icon>
              <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <rect x="3" y="3" width="18" height="18" rx="2" ry="2" />
                <circle cx="8.5" cy="8.5" r="1.5" />
                <polyline points="21 15 16 10 5 21" />
              </svg>
            </template>
          </n-button>
          <n-input
            v-model:value="inputText"
            type="textarea"
            :rows="2"
            :placeholder="$t('chat_input_placeholder')"
            :disabled="!chat.modelLoaded"
            @keydown.ctrl.enter="handleSend"
          />
          <n-button
            type="primary"
            :disabled="!chat.modelLoaded || !inputText.trim()"
            @click="handleSend"
          >
            {{ $t('send') }}
          </n-button>
        </n-input-group>
      </div>
    </template>
  </n-card>
</template>

<script setup lang="ts">
import { ref, onUnmounted } from "vue";
import { useI18n } from "vue-i18n";
import { useMessage } from "naive-ui";
import { useChatStore } from "@/stores/chatStore";
import ModelControl from "@/components/chat/ModelControl.vue";

const { t } = useI18n();
const chat = useChatStore();
const message = useMessage();
const inputText = ref("");
const messagesRef = ref<HTMLElement | null>(null);
const previewImages = ref<string[]>([]);
let intervalId: ReturnType<typeof setInterval> | null = null;

function handleUploadImage(): void {
  if (previewImages.value.length >= 5) {
    message.warning(t("upload_image_limit"));
    return;
  }
  message.info(t("image_upload_pending"));
  previewImages.value.push("data:image/svg+xml,%3Csvg%20xmlns%3D%22http%3A%2F%2Fwww.w3.org%2F2000%2Fsvg%22%20width%3D%22100%22%20height%3D%22100%22%3E%3Crect%20width%3D%22100%22%20height%3D%22100%22%20fill%3D%22%23eee%22%2F%3E%3Ctext%20x%3D%2220%22%20y%3D%2255%22%20font-size%3D%2212%22%20fill%3D%22%23999%22%3Eimage%3C%2Ftext%3E%3C%2Fsvg%3E");
}

function removeImage(index: number): void {
  previewImages.value = previewImages.value.filter((_, i) => i !== index);
}

function handleSend(): void {
  if (!inputText.value.trim()) return;

  // 清除前一次未完成的流式回复
  if (intervalId !== null) {
    clearInterval(intervalId);
    intervalId = null;
  }

  chat.addMessage({
    role: "user",
    content: inputText.value,
    files: previewImages.value.length > 0 ? [...previewImages.value] : undefined,
  });
  previewImages.value = [];
  const text = inputText.value;
  inputText.value = "";

  chat.setModelLoaded(true);
  // TODO: 接入 WebSocket 流式回复，当前为 mock 逐字输出
  const response = `这是对"${text}"的模拟回复。待 WebSocket 流式接入后，此处将显示实时生成的回复内容。`;
  let i = 0;
  intervalId = setInterval(() => {
    if (i < response.length) {
      chat.appendToken(response[i]);
      i++;
    } else {
      clearInterval(intervalId!);
      intervalId = null;
      chat.finalizeResponse();
    }
  }, 30);
}

function handleClear(): void {
  if (intervalId !== null) {
    clearInterval(intervalId);
    intervalId = null;
  }
  chat.clearMessages();
}

onUnmounted(() => {
  if (intervalId) clearInterval(intervalId);
});
</script>

<style scoped>
.chat-card {
  min-height: 500px;
}

.chat-messages {
  height: 400px;
  overflow-y: auto;
  padding: var(--spacing-3);
  display: flex;
  flex-direction: column;
  gap: var(--spacing-3);
}

.message {
  max-width: 80%;
  padding: var(--spacing-3);
  border-radius: var(--radius-md);
}

.message--user {
  align-self: flex-end;
  background: var(--color-brand-bg);
}

.message--assistant {
  align-self: flex-start;
  background: var(--bg-elevated);
}

.message-label {
  font-size: var(--font-size-xs);
  color: var(--text-tertiary);
  margin-bottom: var(--spacing-1);
}

.message-files {
  display: flex;
  flex-wrap: wrap;
  gap: var(--spacing-2);
  margin-bottom: var(--spacing-2);
}

.message-image {
  max-width: 200px;
  max-height: 200px;
  border-radius: var(--radius-sm);
}

.message-content {
  font-size: var(--font-size-base);
  color: var(--text-primary);
  white-space: pre-wrap;
  word-break: break-word;
}

.message-content.streaming::after {
  content: "\258A";
  animation: blink 1s step-end infinite;
}

@keyframes blink {
  50% {
    opacity: 0;
  }
}

.input-area {
  display: flex;
  flex-direction: column;
  gap: var(--spacing-2);
}

.image-preview-bar {
  display: flex;
  gap: var(--spacing-2);
  padding: var(--spacing-2) 0;
  overflow-x: auto;
}

.image-preview-item {
  position: relative;
  width: 60px;
  height: 60px;
  flex-shrink: 0;
}

.image-preview-item img {
  width: 100%;
  height: 100%;
  object-fit: cover;
  border-radius: var(--radius-sm);
}

.image-remove {
  position: absolute;
  top: -4px;
  right: -4px;
}
</style>
