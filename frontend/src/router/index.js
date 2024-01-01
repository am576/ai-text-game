import { createRouter, createWebHistory } from "vue-router";
import MainChat from "../components/MainChat"

const routes = [
  {
    path: "/prompt",
    name: "prompt",
    component: MainChat
  }
];
const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes,
});

export default router;
