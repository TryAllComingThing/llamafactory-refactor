import { getJson, postJson } from "./client";

export interface TrainPreview {
  command: string[];
  output_dir: string;
}

export interface TrainStatus {
  running: boolean;
  current_step: number;
  total_steps: number;
  loss: number | null;
  progress: number;
}

export async function previewTrain(params: Record<string, unknown>): Promise<TrainPreview> {
  return postJson<TrainPreview>("/train/preview", params);
}

export async function startTrain(params: Record<string, unknown>): Promise<{ run_id: string }> {
  return postJson<{ run_id: string }>("/train/start", params);
}

export async function abortTrain(): Promise<void> {
  return postJson<void>("/train/abort");
}

export async function fetchTrainStatus(): Promise<TrainStatus> {
  return getJson<TrainStatus>("/train/status");
}
