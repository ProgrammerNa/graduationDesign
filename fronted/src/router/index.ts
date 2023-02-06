import { createRouter, createWebHistory } from 'vue-router';
import Example from '../view/example/example.vue'
import Login from '../view/Login/Login.vue'
import Layout from '../view/Layout/index.vue'
import UserMangement from '../view/System/userManagement.vue'
import RoleMangement from '../view/System/roleMangement.vue'
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
        {
            path:'/system',
            component:Layout,
            meta:{
                title:'系统管理'
            },
            children:[
                {
                    path:'/userMangement',
                    component:UserMangement,
                    meta:{
                        title:'用户管理'
                    }
                },
                {
                    path:'/roleMangement',
                    component:RoleMangement,
                    meta:{
                        title:'角色管理'
                    }
                }
            ]
        }
    ],
});

export default router;
