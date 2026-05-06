import { createRouter, createWebHistory } from "vue-router";
import DashboardLayout from "@/views/DashboardLayout.vue";

const router = createRouter({
  history: createWebHistory(),
  routes: [
    {
      path: "/",
      component: DashboardLayout,
      redirect: "/train",
      children: [
        {
          path: "train",
          name: "train",
          component: () => import("@/views/TrainView.vue"),
          meta: { title: "nav_train", desc: "train_desc" },
        },
        {
          path: "eval",
          name: "eval",
          component: () => import("@/views/EvalView.vue"),
          meta: { title: "nav_eval", desc: "eval_desc" },
        },
        {
          path: "infer",
          name: "infer",
          component: () => import("@/views/InferView.vue"),
          meta: { title: "nav_infer", desc: "infer_desc" },
        },
        {
          path: "export",
          name: "export",
          component: () => import("@/views/ExportView.vue"),
          meta: { title: "nav_export", desc: "export_desc" },
        },
      ],
    },
  ],
});

export default router;
