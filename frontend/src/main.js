import { createApp } from 'vue'
import { createPinia } from 'pinia'
import '@/tailwind/main.css'
import App from './App.vue'
import router from './router'
import 'animate.css'
import Toast from "vue-toastification"
import "vue-toastification/dist/index.css"

const app = createApp(App)

app.use(createPinia())
app.use(router)
app.use(Toast, {
  transition: "Vue-Toastification__fade",
  maxToasts: 20,
  newestOnTop: true
})
app.mount('#app')
