import { createApp } from "vue";
import App from "./App.vue";
import router from "./router";
import { MainChat, AdventuresList } from "./components"
import { library } from '@fortawesome/fontawesome-svg-core'
import { FontAwesomeIcon } from '@fortawesome/vue-fontawesome'
import "./assets/style.css";
import '@fortawesome/fontawesome-svg-core/styles.css'
import '@mdi/font/css/materialdesignicons.css'

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
  },
  iconfont: 'mdi'
})

const app = createApp(App).use(router);

app.component("main-chat", MainChat)
app.component("adventures-list", AdventuresList)
app.component('font-awesome-icon', FontAwesomeIcon)
app.use(vuetify)
app.mount("#app")
