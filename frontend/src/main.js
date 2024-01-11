import { createApp } from "vue";
import App from "./App.vue";
import router from "./router";
import MainChat from "./components/MainChat"
import AdventuresList from "./components/AdventuresList"
import { library } from '@fortawesome/fontawesome-svg-core'
import { FontAwesomeIcon } from '@fortawesome/vue-fontawesome'
import "./assets/style.css";
import '@fortawesome/fontawesome-svg-core/styles.css'

import { faAngleLeft, faRotateRight, faPenToSquare } from '@fortawesome/free-solid-svg-icons'

library.add(faAngleLeft)
library.add(faRotateRight)
library.add(faPenToSquare)


import 'vuetify/styles'
import { createVuetify } from 'vuetify'
import * as components from 'vuetify/components'
import * as directives from 'vuetify/directives'

const vuetify = createVuetify({
  components,
  directives,
  theme: {
    defaultTheme: 'dark'
  }
})

const app = createApp(App).use(router);

app.component("main-chat", MainChat)
app.component("adventures-list", AdventuresList)
app.component('font-awesome-icon', FontAwesomeIcon)
app.use(vuetify)
app.mount("#app")
