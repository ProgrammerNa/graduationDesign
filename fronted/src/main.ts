import {createApp} from 'vue'
import './style.css'
import App from './App.vue'
import router from './router';
import pinia from './plugins/pinia';
import service from './utils/http';
import * as ElementPlusIconsVue from '@element-plus/icons-vue';

const app = createApp(App);
for (const [key, component] of Object.entries(ElementPlusIconsVue)) {
    app.component(key, component);
}
app.config.globalProperties.$service = service;
app.use(router, pinia, service).mount('#app');
