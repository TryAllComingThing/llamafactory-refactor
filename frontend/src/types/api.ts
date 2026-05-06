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

export interface WsChatError extends WsMessage {
  type: "chat:error";
  message: string;
}

export interface WsChatSend extends WsMessage {
  type: "chat:send";
  messages: { role: string; content: string }[];
  system?: string;
  tools?: string;
  max_new_tokens?: number;
  top_p?: number;
  temperature?: number;
  skip_special_tokens?: boolean;
  escape_html?: boolean;
  enable_thinking?: boolean;
}

export interface WsPing extends WsMessage {
  type: "ping";
}
