import { createRouter, createWebHistory } from 'vue-router';
import Example from '../view/example/example.vue'
import Login from '../view/Login/Login.vue'
import Layout from '../view/Layout/index.vue'
// 定义路由规则
const router = createRouter({
    history: createWebHistory('dist'),
    routes: [
        {
            path: '/',
            name: 'login',
            component: Login,
            meta: {
                title: '登录'
            },
        },
        {
            path: '/main',
            component: Layout,
        },
    ],
});

export default router;
