import { createApp } from "vue";
import App from "./App.vue";
import router from "./router";
import MainChat from "./components/MainChat"
import { library } from '@fortawesome/fontawesome-svg-core'
import { FontAwesomeIcon } from '@fortawesome/vue-fontawesome'
import "./assets/style.css";
import '@fortawesome/fontawesome-svg-core/styles.css'

import { faAngleLeft } from '@fortawesome/free-solid-svg-icons'

library.add(faAngleLeft)

const app = createApp(App).use(router);

app.component("main-chat", MainChat)
app.component('font-awesome-icon', FontAwesomeIcon)

app.mount("#app")
