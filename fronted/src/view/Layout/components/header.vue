<script setup lang="ts">
    import {ref} from 'vue'
    import router from '../../../router';
    import {useUserStore} from "../../../store/user";
    import pinia from "../../../plugins/pinia";
    import userDetail from './userDetail.vue'
    const currentUserInfo = ref(useUserStore(pinia).userInfo)
    const user = ref()
    const rePassword = () => {
        user.value.open({
            title:'修改密码',
            data:currentUserInfo.value
        })
    }
     const editUser = () => {
        user.value.open({
            title:'修改信息',
            data:currentUserInfo.value
        })
    }
    const logout = () => {
        router.push({
            path: '/',
        });
    };
</script>
<template>
    <div class="header">
        <div class="header-title">
            <div class="title">桂湖大药房连锁药房管理系统</div>
            <div class="username">
                <el-tooltip class="box-item" effect="light" placement="bottom">
                    <template #content>
                        <div style="border-bottom: 1px solid #d1d1d1" @click="rePassword">修改密码</div>
                        <div @click="logout">退出登录</div>
                    </template>
                    <div class="login-name">{{currentUserInfo.username}}</div>
                </el-tooltip>
            </div>
        </div>
        <userDetail ref="user"></userDetail>
    </div>
</template>

<style lang="scss" scoped>
    .header-title {
        display: flex;
        align-items: center;
        justify-content: space-between;

        .title {
            margin-top: 10px;
            margin-left: 10px;
            font-size: 30px;
            font-family: YouYuan;
        }

        .username {
            margin-right: 20px;
            margin-top: 10px;
            font-size: 20px;
        }
    }
</style>
