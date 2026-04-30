import { getJson, postJson } from "./client";

export async function startEval(params: Record<string, unknown>): Promise<{ run_id: string }> {
  return postJson<{ run_id: string }>("/eval/start", params);
}

export async function fetchEvalStatus(): Promise<{
  running: boolean;
  progress: number;
}> {
  return getJson<{ running: boolean; progress: number }>("/eval/status");
}
