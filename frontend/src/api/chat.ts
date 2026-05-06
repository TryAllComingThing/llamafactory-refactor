import { apiClient } from "./client";
import type { ApiResponse } from "@/types/api";

export interface ChatMessage {
  role: "user" | "assistant" | "observation";
  content: string;
  files?: string[];
}

export interface ChatSendParams {
  messages: ChatMessage[];
  system?: string;
  tools?: string;
  max_new_tokens: number;
  top_p: number;
  temperature: number;
}

export interface ChatStreamCallbacks {
  onToken: (text: string) => void;
  onDone: (fullText: string) => void;
  onError: (message: string) => void;
}

export function streamChat(
  params: ChatSendParams,
  callbacks: ChatStreamCallbacks,
): () => void {
  const protocol = window.location.protocol === "https:" ? "wss:" : "ws:";
  const wsUrl = `${protocol}//${window.location.host}/ws/chat`;
  const ws = new WebSocket(wsUrl);

  ws.onopen = () => {
    ws.send(JSON.stringify({ type: "chat:send", ...params }));
  };

  ws.onmessage = (event: MessageEvent) => {
    const data = JSON.parse(event.data);
    if (data.type === "chat:token") {
      callbacks.onToken(data.text);
    } else if (data.type === "chat:done") {
      callbacks.onDone(data.full_text);
      ws.close();
    } else if (data.type === "chat:error") {
      callbacks.onError(data.message);
      ws.close();
    }
  };

  ws.onerror = () => {
    callbacks.onError("WebSocket connection failed");
  };

  return () => ws.close();
}

export async function loadModel(params: Record<string, unknown>): Promise<string> {
  const res = await apiClient<ApiResponse<null>>("/model/load", { method: "POST", body: params });
  return res.message ?? "";
}

export async function unloadModel(): Promise<string> {
  const res = await apiClient<ApiResponse<null>>("/model/unload", { method: "POST" });
  return res.message ?? "";
}
