import { createApp } from 'vue'
import App from './App.vue'
import router from './router'

import 'vuetify/styles'
import { createVuetify } from 'vuetify'
import * as components from 'vuetify/components'
import * as directives from 'vuetify/directives'

import '@/assets/mycss.css'
import '@/assets/Interfont/inter.css'
import axios from "axios";

const vuetify = createVuetify({
  components,
  directives,
})

axios.defaults.baseURL = 'http://192.168.1.100:9090'
axios.defaults.timeout = 30000

const app = createApp(App)

app.use(router)
app.use(vuetify)

app.mount('#app')
