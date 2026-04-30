import { defineStore } from "pinia";
import { ref } from "vue";
import type { ChatMessage } from "@/api/chat";

export const useChatStore = defineStore("chat", () => {
  const messages = ref<ChatMessage[]>([]);
  const streamingResponse = ref("");
  const modelLoaded = ref(false);

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
    addMessage,
    appendToken,
    finalizeResponse,
    clearMessages,
    setModelLoaded,
  };
});
