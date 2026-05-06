import { getJson } from "./client";

export interface ModelInfo {
  model_name: string;
  model_path: string;
  template: string;
}

export interface ModelDetail extends ModelInfo {
  finetuning_type: string;
  quantized_bit: string;
}

export async function fetchModelInfo(modelName: string): Promise<ModelInfo> {
  return getJson<ModelInfo>(`/models/${encodeURIComponent(modelName)}`);
}

export async function fetchCheckpoints(
  modelName: string,
  finetuningType: string,
): Promise<string[]> {
  return getJson<string[]>("/checkpoints", { model: modelName, ft: finetuningType });
}

export async function fetchDatasets(dir?: string, stage?: string): Promise<string[]> {
  return getJson<string[]>("/datasets", { dir, stage });
}

export async function fetchOutputDirs(
  modelName: string,
  finetuningType: string,
): Promise<string[]> {
  return getJson<string[]>("/output-dirs", { model: modelName, ft: finetuningType });
}

export async function fetchFullModelList(): Promise<ModelInfo[]> {
  return getJson<ModelInfo[]>("/models");
}

export async function fetchTemplates(): Promise<string[]> {
  return getJson<string[]>("/templates");
}

export async function fetchConfigPaths(): Promise<string[]> {
  return getJson<string[]>("/configs");
}
