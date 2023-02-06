import { createApp } from 'vue'
import './style.css'
import App from './App.vue'
import router from './router';
import pinia from './plugins/pinia';
import service from './utils/http';
const app = createApp(App);
app.config.globalProperties.$service = service;
app.use(router,pinia,service).mount('#app');
