import { defineStore } from "pinia";
import { ref } from "vue";
import type { ChatMessage } from "@/api/chat";

export const useChatStore = defineStore("chat", () => {
  const messages = ref<ChatMessage[]>([]);
  const streamingResponse = ref("");
  const modelLoaded = ref(false);

  // Inference config
  const inferBackend = ref("huggingface");
  const inferDtype = ref("auto");
  const extraArgs = ref('{"vllm_enforce_eager": true}');
  const infoText = ref("");

  // Chat parameters
  const maxNewTokens = ref(1024);
  const topP = ref(0.7);
  const temperature = ref(0.95);
  const skipSpecialTokens = ref(true);
  const escapeHtml = ref(true);
  const enableThinking = ref(true);

  // Role / system / tools
  const role = ref("user");
  const systemPrompt = ref("");
  const tools = ref("");

  function addMessage(msg: ChatMessage): void {
    messages.value.push(msg);
  }

  function appendToken(token: string): void {
    streamingResponse.value += token;
  }

  function finalizeResponse(): void {
    if (streamingResponse.value) {
      messages.value.push({
        role: "assistant",
        content: streamingResponse.value,
      });
      streamingResponse.value = "";
    }
  }

  function clearMessages(): void {
    messages.value = [];
    streamingResponse.value = "";
  }

  function setModelLoaded(loaded: boolean): void {
    modelLoaded.value = loaded;
  }

  return {
    messages,
    streamingResponse,
    modelLoaded,
    inferBackend,
    inferDtype,
    extraArgs,
    infoText,
    maxNewTokens,
    topP,
    temperature,
    skipSpecialTokens,
    escapeHtml,
    enableThinking,
    role,
    systemPrompt,
    tools,
    addMessage,
    appendToken,
    finalizeResponse,
    clearMessages,
    setModelLoaded,
  };
});
