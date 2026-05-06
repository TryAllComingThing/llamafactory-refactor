<template>
  <div class="chat-container">
    <!-- Role / System / Tools / Multimodal inputs -->
    <div class="chat-config">
      <n-grid :cols="4" :x-gap="8" :y-gap="6">
        <n-grid-item>
          <n-form-item :label="$t('role')" label-placement="top" size="tiny">
            <n-select v-model:value="chat.role" :options="roleOptions" size="tiny" />
          </n-form-item>
        </n-grid-item>
        <n-grid-item>
          <n-form-item :label="$t('system')" label-placement="top" size="tiny">
            <n-input v-model:value="chat.systemPrompt" :placeholder="$t('optional')" size="tiny" />
          </n-form-item>
        </n-grid-item>
        <n-grid-item>
          <n-form-item :label="$t('tools')" label-placement="top" size="tiny">
            <n-input v-model:value="chat.tools" type="textarea" :rows="2" :placeholder="$t('optional')" size="tiny" />
          </n-form-item>
        </n-grid-item>
        <n-grid-item>
          <n-form-item :label="$t('mm_box')" label-placement="top" size="tiny">
            <n-tabs size="tiny" type="segment" default-value="image">
              <n-tab-pane name="image" :tab="$t('image')">
                <n-button size="tiny" :disabled="!chat.modelLoaded" @click="handleUploadImage">
                  {{ $t('upload_image') }}
                </n-button>
              </n-tab-pane>
              <n-tab-pane name="video" :tab="$t('video')">
                <span class="pending-label">{{ $t('video') }} (API pending)</span>
              </n-tab-pane>
            </n-tabs>
          </n-form-item>
        </n-grid-item>
      </n-grid>
    </div>

    <!-- Messages -->
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
        <div class="message-content" v-html="msg.content"></div>
      </div>

      <div v-if="chat.streamingResponse" class="message message--assistant">
        <div class="message-label">{{ $t('chat_assistant') }}</div>
        <div class="message-content streaming" v-html="chat.streamingResponse"></div>
      </div>
    </div>

    <!-- Input area -->
    <div class="input-area">
      <div v-if="previewImages.length" class="image-preview-bar">
        <div v-for="(url, i) in previewImages" :key="i" class="image-preview-item">
          <img :src="url" :alt="$t('upload_image')" />
          <n-button size="tiny" circle quaternary class="image-remove" @click="removeImage(i)">✕</n-button>
        </div>
      </div>
      <n-input-group>
        <n-input
          v-model:value="inputText"
          type="textarea"
          :rows="3"
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
  </div>
</template>

<script setup lang="ts">
import { ref, onUnmounted } from "vue";
import { useI18n } from "vue-i18n";
import { useMessage } from "naive-ui";
import { useChatStore } from "@/stores/chatStore";
import { streamChat } from "@/api/chat";
import type { ChatMessage } from "@/api/chat";

const { t } = useI18n();
const chat = useChatStore();
const message = useMessage();
const inputText = ref("");
const messagesRef = ref<HTMLElement | null>(null);
const previewImages = ref<string[]>([]);
let closeWs: (() => void) | null = null;

const roleOptions = [
  { label: "User", value: "user" },
  { label: "Observation", value: "observation" },
];

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
  if (!inputText.value.trim() || !chat.modelLoaded) return;

  // Cancel previous stream if active
  if (closeWs !== null) {
    closeWs();
    closeWs = null;
    chat.finalizeResponse();
  }

  const content = inputText.value;
  inputText.value = "";

  chat.addMessage({
    role: "user",
    content,
    files: previewImages.value.length > 0 ? [...previewImages.value] : undefined,
  });
  previewImages.value = [];

  const apiMessages: ChatMessage[] = chat.messages.map((m) => ({
    role: m.role === "user" ? "user" : "assistant",
    content: m.content,
  }));
  // Before the last user message was added, we need to use the role from config
  const lastIdx = apiMessages.length - 1;
  if (lastIdx >= 0) {
    apiMessages[lastIdx] = { role: chat.role as "user" | "assistant", content };
  }

  closeWs = streamChat(
    {
      messages: apiMessages,
      system: chat.systemPrompt || undefined,
      tools: chat.tools || undefined,
      max_new_tokens: chat.maxNewTokens,
      top_p: chat.topP,
      temperature: chat.temperature,
    },
    {
      onToken: (text: string) => {
        chat.appendToken(text);
      },
      onDone: () => {
        closeWs = null;
        chat.finalizeResponse();
      },
      onError: (err: string) => {
        closeWs = null;
        chat.finalizeResponse();
        message.error(err);
      },
    },
  );
}

function handleClear(): void {
  if (closeWs !== null) {
    closeWs();
    closeWs = null;
  }
  chat.clearMessages();
}

onUnmounted(() => {
  if (closeWs) closeWs();
});

defineExpose({
  handleClear,
});
</script>

<style scoped>
.chat-container {
  border: 1px solid var(--border-default);
  border-radius: var(--radius-md);
  overflow: hidden;
  background: var(--bg-surface);
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
  padding: var(--spacing-3);
  background: var(--bg-elevated);
  border-top: 1px solid var(--border-default);
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
