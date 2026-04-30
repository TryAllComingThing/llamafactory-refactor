import { createApp } from "vue";
import { createPinia } from "pinia";
import { createI18n } from "vue-i18n";
import zh from "./i18n/zh.json";
import en from "./i18n/en.json";
import router from "./router";
import App from "./App.vue";
import "./styles/global.css";

const i18n = createI18n({
  locale: "zh",
  fallbackLocale: "en",
  messages: { zh, en },
});

const app = createApp(App);
app.use(createPinia());
app.use(router);
app.use(i18n);
app.mount("#app");
