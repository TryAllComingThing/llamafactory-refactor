import { postJson } from "./client";

export interface ExportStartResult {
  run_id: string;
  output_dir: string;
}

export async function startExport(params: Record<string, unknown>): Promise<ExportStartResult> {
  return postJson<ExportStartResult>("/export/start", params);
}

export async function abortExport(): Promise<void> {
  return postJson<void>("/export/abort");
}
