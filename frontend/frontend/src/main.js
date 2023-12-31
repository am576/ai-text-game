import { createApp } from "vue";
import App from "./App.vue";
import router from "./router";
import MainChat from "./components/MainChat"

const app = createApp(App).use(router);

app.component("main-chat", MainChat)

app.mount("#app")
