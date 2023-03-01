<script setup lang="ts">
    import {ref, reactive} from 'vue';
    import {userLogin} from "../../api/loginApi";
    import pinia from '../../plugins/pinia'
    import {useSystemStore} from "../../store/system";
    import {useUserStore} from "../../store/user";
    import router from "../../router/index";
    import {getMenuLsit} from "../../api/menu";
    import {tree} from '../../utils/treeUtilr'

    const roleId = ref(0)
    const formData = reactive({
        username: '',
        password: ''
    })
    const menuList = ref(<any>[]);
    const rules = reactive({
        username: [
            {required: true, message: '请输入用户名', trigger: 'blur'},
        ],
        password: [
            {
                required: true,
                message: '请输入密码',
                trigger: 'blur',
            },
        ],
    })
    const ruleFormRef = ref();
    const sumbit = () => {
        ruleFormRef.value.validate((valid: any) => {
            if (valid) {
                console.log(valid)
                userLogin({
                    username: formData.username,
                    password: formData.password
                }).then((res) => {
                    if (res.status === 200) {
                        console.log(res.data.length)
                        if (res.data[0].flag === 0) {
                            // @ts-ignore
                            ElMessage({
                                message: '账号已被禁用，联系管理员进行处理',
                                type: 'warning',
                            })
                        } else {
                            if (formData.username === res.data[0].username && formData.password === res.data[0].password) {
                                roleId.value = res.data[0].role_id
                                useUserStore(pinia).setUserInfo(res.data[0])
                                // @ts-ignore
                                ElMessage({
                                    message: '登录成功',
                                    type: 'success',
                                })
                                getMenu()
                                router.push('/main')
                            }
                        }
                    }
                }).catch((err) => {
                    // @ts-ignore
                    ElMessage({
                        message: '账户或密码填写错误，请重新填写',
                        type: 'error',
                    })
                })
            } else {
                console.log(valid)
                return false
            }
        })
    }
    const getMenu = () => {
        getMenuLsit({
            roleId: roleId.value
        }).then(res => {
            if (res.status === 200) {
                useSystemStore(pinia).setRoleMenuList(tree(res.data))
            }
        })
    }
</script>
<template>
    <div class="container">
        <div class="login-container">
            <div class="title">桂湖大药房连锁药房管理系统</div>
            <div class="login-form">
                <el-form :model="formData" ref="ruleFormRef" :rules="rules">
                    <el-form-item required prop="username">
                        <template #label>
                            用户名
                        </template>
                        <el-input placeholder="请输入用户名" v-model="formData.username"></el-input>
                    </el-form-item>
                    <el-form-item required prop="password">
                        <template #label>
                            密&nbsp;&nbsp;&nbsp;码
                        </template>
                        <el-input placeholder="请输入密码" v-model="formData.password"></el-input>
                    </el-form-item>
                    <el-form-item>
                        <el-button @click="sumbit" type="primary">登录</el-button>
                    </el-form-item>
                </el-form>
            </div>
        </div>
    </div>
</template>


<style lang="scss" scoped>
    .container {
        height: 100%;
        width: 100%;
        display: flex;
        align-items: center;
        justify-content: center;
        background-color: aliceblue;
        background-repeat: no-repeat;
        background-position-y: 50%;
        background-image: url("https://img1.baidu.com/it/u=1499999492,3493837702&fm=253&fmt=auto&app=138&f=PNG?w=857&h=500");

        .login-container {
            margin-left: 40%;
            width: 500px;
            height: 500px;
            flex-direction: column;
            display: flex;
            align-items: center;
            justify-content: flex-start;
            box-shadow: 2px 3px 10px 1px lightgray;

            .title {
                margin-top: 25%;
                font-size: 30px;
                font-family: YouYuan;
            }

            .login-form {
                margin-top: 10%;

                .el-button {
                    width: 300px;
                }
            }

        }
    }
</style>