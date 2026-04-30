import { postJson } from "./client";

export interface ChatMessage {
  role: "user" | "assistant";
  content: string;
  files?: string[];
}

export async function loadModel(modelName: string): Promise<void> {
  if (!modelName || !modelName.trim()) {
    throw new Error("modelName must be non-empty");
  }
  return postJson<void>("/model/load", { model_name: modelName });
}

export async function unloadModel(): Promise<void> {
  return postJson<void>("/model/unload");
}
