import { ref, onMounted, onUnmounted } from "vue";
import { wsManager } from "@/api/ws-manager";
import type { WsStatus } from "@/api/ws-manager";

export function useWsStatus() {
  const status = ref<WsStatus>("disconnected");
  let cleanup: (() => void) | null = null;

  onMounted(() => {
    status.value = wsManager.getStatus();
    cleanup = wsManager.onStatusChange((newStatus) => {
      status.value = newStatus;
    });
  });

  onUnmounted(() => {
    cleanup?.();
  });

  return { status };
}
