import { createRouter, createWebHistory } from "vue-router";
import MainChat from "../components/MainChat"
import HomeView from "../components/HomeView"

const routes = [
  {
    path: "/adventure",
    name: "adventure",
    component: MainChat
  },
  {
    path: "/",
    name: "home",
    component: HomeView
  }
];
const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes,
});

export default router;
