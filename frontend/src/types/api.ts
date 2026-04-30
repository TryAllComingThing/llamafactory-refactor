export interface ApiResponse<T> {
  success: boolean;
  data: T;
  message?: string;
}

export interface ApiError {
  success: false;
  message: string;
  code?: string;
}

export interface PaginatedData<T> {
  items: T[];
  total: number;
  page: number;
  limit: number;
}

export interface WsMessage {
  type: string;
  [key: string]: unknown;
}

export interface WsTrainProgress extends WsMessage {
  type: "train:progress";
  progress: number;
  current_step: number;
  total_steps: number;
  loss: number;
  log: string;
}

export interface WsTrainMonitorProgress extends WsMessage {
  type: "progress";
  percentage: number;
  current: number;
  total: number;
  remaining_secs: number;
  elapsed_secs: number;
}

export interface WsTrainMonitorLog extends WsMessage {
  type: "log";
  text: string;
}

export interface WsTrainMonitorLoss extends WsMessage {
  type: "loss";
  step: number;
  value: number;
}

export interface WsTrainComplete extends WsMessage {
  type: "train:complete";
  status: "success" | "error" | "aborted";
  message?: string;
}

export interface WsChatToken extends WsMessage {
  type: "chat:token";
  text: string;
}

export interface WsChatDone extends WsMessage {
  type: "chat:done";
  full_text: string;
}
