<script setup lang="ts">
    import {ref,reactive} from 'vue';
    import {userLogin} from "../../api/loginApi";
    import router from "../../router/index";

    const formData = reactive({
        username:'',
        password:''
    })
    const sumbit = () => {
        userLogin({
            username:formData.username,
            password:formData.password
        }).then((res) => {
            if( res.status === 200){
                console.log(res.data.length)
                if(formData.username === res.data[0].username && formData.password === res.data[0].password) {
                    // @ts-ignore
                    ElMessage({
                        message: '登录成功',
                        type: 'success',
                    })
                    router.push('/main')
                }
            }
        }).catch((err) =>{
            // @ts-ignore
            ElMessage({
                message: '账户或密码填写错误，请重新填写',
                type: 'error',
            })
        })
    }
</script>
<template>
    <div class="container">
        <div class="login-container">
            <el-form :model="formData">
                <el-form-item required>
                    <template #label>
                        用户名
                    </template>
                    <el-input placeholder="请输入用户名" v-model="formData.username"></el-input>
            </el-form-item>
                <el-form-item required>
                    <template #label>
                     密&nbsp;&nbsp;&nbsp;码
                    </template>
                    <el-input placeholder="请输入密码" v-model="formData.password"></el-input>
                </el-form-item>
                <el-button @click="sumbit">登录</el-button>
            </el-form>
        </div>
    </div>
</template>


<style lang="scss" scoped>
.container{
    height: 100%;
    width: 100%;
    display: flex;
    align-items: center;
    justify-content: center;
    background-image: linear-gradient(to top, #1c9cf9,#0082fa);
}
</style>