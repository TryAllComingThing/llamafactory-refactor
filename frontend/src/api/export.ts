import { postJson } from "./client";

export async function exportModel(params: Record<string, unknown>): Promise<{ run_id: string }> {
  return postJson<{ run_id: string }>("/export", params);
}
