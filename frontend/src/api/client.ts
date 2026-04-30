import { ofetch } from "ofetch";
import type { ApiResponse } from "@/types/api";

export const apiClient = ofetch.create({
  baseURL: "/api",
  headers: { "Content-Type": "application/json" },
  parseResponse: JSON.parse,
  onResponseError({ response }) {
    const message = response?._data?.message || response?.statusText || "请求失败";
    console.error("[API Error]", response?.status, message);
  },
});

function unwrapData<T>(res: ApiResponse<T>, url: string): T {
  if (res.data === undefined) {
    throw new Error(`API response missing data field: ${url}`);
  }
  return res.data as T;
}

export async function getJson<T>(url: string, params?: Record<string, unknown>): Promise<T> {
  return apiClient<ApiResponse<T>>(url, { params }).then((res) => unwrapData(res, url));
}

export async function postJson<T>(
  url: string,
  body?: Record<string, unknown>,
): Promise<T> {
  return apiClient<ApiResponse<T>>(url, { method: "POST", body }).then(
    (res) => unwrapData(res, url),
  );
}

export async function putJson<T>(
  url: string,
  body?: Record<string, unknown>,
): Promise<T> {
  return apiClient<ApiResponse<T>>(url, { method: "PUT", body }).then(
    (res) => unwrapData(res, url),
  );
}

export async function delJson<T>(url: string): Promise<T> {
  return apiClient<ApiResponse<T>>(url, { method: "DELETE" }).then(
    (res) => unwrapData(res, url),
  );
}
