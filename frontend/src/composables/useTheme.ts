import { watch } from "vue";
import { useSessionStore } from "@/stores/session";

export function useTheme(): void {
  const session = useSessionStore();

  function applyTheme(isDark: boolean): void {
    document.documentElement.setAttribute("data-theme", isDark ? "dark" : "light");
  }

  applyTheme(session.darkMode);

  watch(
    () => session.darkMode,
    (val) => {
      applyTheme(val);
    },
  );
}
