import {createRouter, createWebHistory} from 'vue-router';
import Example from '../view/example/example.vue'
import Login from '../view/Login/Login.vue'
import Layout from '../view/Layout/index.vue'
import UserMangement from '../view/System/userManagement.vue'
import RoleMangement from '../view/System/roleMangement.vue'
import FenMangement from '../view/fen/fenMangement.vue'
import Sell from '../view/medicalSell/sell.vue'
import Staff from '../view/staff/staff.vue'
import FenStaff from '../view/fen/fenStaff.vue'
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
            path: '/system',
            component: Layout,
            meta: {
                title: '系统管理'
            },
            children: [
                {
                    path: '/userMangement',
                    component: UserMangement,
                    meta: {
                        title: '用户管理'
                    }
                },
                {
                    path: '/roleMangement',
                    component: RoleMangement,
                    meta: {
                        title: '角色管理'
                    }
                }
            ]
        },
        {
            path: '/medicalSell',
            component: Layout,
            meta: {
                title: '药品销售'
            },
            children: [
                {
                    path: '/sell',
                    component: Sell,
                    meta: {
                        title: '药品销售'
                    }
                },
            ]
        },
        {
            path: '/dianlMangement',
            component: Layout,
            meta: {
                title: '分店管理'
            },
            children: [
                {
                    path: '/fendianMangement',
                    component: FenMangement,
                    meta: {
                        title: '分店管理'
                    }
                },
                {
                     path: '/fenStaffDetail',
                    component: FenStaff,
                    meta: {
                        title: '人员详情'
                    }
                }
            ]
        },
        {
            path: '/yuangongMangement',
            component: Layout,
            meta: {
                title: '员工管理'
            },
            children: [
                {
                    path: '/yuangongMangement',
                    component: Staff,
                    meta: {
                        title: '员工管理'
                    }
                },
            ]
        }

    ],
});

export default router;
