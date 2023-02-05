import { createApp } from 'vue'
import './style.css'
import App from './App.vue'
import router from './router';
import service from './utils/http';
const app = createApp(App);
app.config.globalProperties.$service = service;
app.use(router,service).mount('#app');
