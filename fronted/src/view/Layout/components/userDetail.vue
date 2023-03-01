<script setup lang="ts">
    import {ref, onMounted, defineProps, reactive} from 'vue'
    import {checkPassword} from "../../../api/user";
    import {useRouter} from 'vue-router'

    const title = ref('')
    const userId = ref()
    const roleId = ref()
    const userInfo = ref([])
    const route = useRouter()
    const ruleForm = reactive({
        username: '',
        password: '',
        repassword: '',
        name: '',
        storeName: '',
        storePhone: '',
        storeAddress: ''
    })
    const show = ref(false)
    //点击详情该行的用户id
    const open = (data: any) => {
        title.value = data.title
        userId.value = data.data.user_id
        roleId.value = data.data.role_id
        if (data.title === '修改信息') {
            ruleForm.username = data.data.username;
            ruleForm.name = data.data.store_responsible;
            ruleForm.storeName = data.data.store_name;
            ruleForm.storePhone = data.data.phone;
            ruleForm.storeAddress = data.data.store_address;
        }
        show.value = true
    }
    const ruleFormRef = ref()
    const validatePhone = (rule: any, value: any, callback: any) => {
        if (value === '') {
            callback(new Error('请填写联系方式'))
        } else {
            if (!(/^1[0123456789]\d{9}$/.test(ruleForm.staffPhone))) {
                callback(new Error("联系方式格式有误"))
            } else {
                callback()
            }
        }
    }
    const validatePass = (rule: any, value: any, callback: any) => {
        if (value === '') {
            callback(new Error('请输入密码'))
        } else {
            if (ruleForm.repassword !== '') {
                if (!ruleFormRef.value) return
                ruleFormRef.value.validateField('repassword', () => null)
            }
            callback()
        }
    }
    const validatePass2 = (rule: any, value: any, callback: any) => {
        if (value === '') {
            callback(new Error('请再次输入密码'))
        } else if (value !== ruleForm.password) {
            callback(new Error("俩次密码不一致"))
        } else {
            callback()
        }
    }
    const rules = reactive({
        password: [{required: true, validator: validatePass, trigger: 'blur'}],
        repassword: [{required: true, validator: validatePass2, trigger: 'blur'}],
        storePhone: [{required: true, validator: validatePhone, trigger: 'blur'}],
    })
    const confirm = () => {
        ruleFormRef.value.validate((valid: any) => {
            if (valid) {
                if (title.value === '修改密码') {
                    checkPassword({
                        id: userId.value,
                        password: ruleForm.password
                    }).then((res) => {
                        if (res.status === 200) {
                            // @ts-ignore
                            ElMessage({
                                message: '修改密码成功',
                                type: 'success',
                            })
                            setTimeout(() => {
                                route.push('/')
                            },2000)
                        } else {
                             // @ts-ignore
                            ElMessage({
                                message: '修改密码失败',
                                type: 'error',
                            })
                        }
                    }).catch(err => {
                           // @ts-ignore
                            ElMessage({
                                message: '网络异常',
                                type: 'error',
                            })
                    })

                }
            } else {
                console.log('验证出错')
            }
        })


    }
    const cancel = () => {
        show.value = false;
        ruleForm.storePhone = '';
        ruleForm.storeAddress = '';
        ruleForm.storeName
        ruleForm.name = '';
        ruleForm.repassword = '';
        ruleForm.password = '';
        ruleForm.username = ''
    }

    defineExpose({
        open,
    })

</script>


<template>
    <el-dialog
            v-model="show"
            :title=title
            width="50%"
            @open="init"
            ref="dialogs"
    >
        <div class="container">
            <el-form
                    :model="ruleForm" ref="ruleFormRef" :rules="rules" label-width="120">
                <el-form-item label="登录用户名" prop="username" v-if="title=== '修改信息'">
                    <el-input v-model="ruleForm.username" disabled="true"></el-input>
                </el-form-item>
                <el-form-item label="门店名称" prop="storeName" v-if="title=== '修改信息' && roleId !== 1">
                    <el-input v-model="ruleForm.storeName" disabled="true"></el-input>
                </el-form-item>
                <el-form-item label="门店地址" prop="storeAddress" v-if="title=== '修改信息'  && roleId !== 1">
                    <el-input v-model="ruleForm.storeAddress" disabled="true"></el-input>
                </el-form-item>
                <el-form-item label="密码" prop="password" v-if="title=== '修改密码'">
                    <el-input type="password" v-model="ruleForm.password" show-password="true"
                              placeholder="请输入密码"></el-input>
                </el-form-item>
                <el-form-item label="重复密码" prop="repassword" v-if="title=== '修改密码'">
                    <el-input type="password" v-model="ruleForm.repassword" show-password="true"
                              placeholder="请确认密码"></el-input>
                </el-form-item>
                <el-form-item label="姓名" prop="name" v-if="title=== '修改信息'  && roleId !== 1">
                    <el-input v-model="ruleForm.name" disabled="true"></el-input>
                </el-form-item>
                <el-form-item label="联系方式" prop="storePhone" v-if="title=== '修改信息'  && roleId !== 1">
                    <el-input v-model="ruleForm.storePhone"></el-input>
                </el-form-item>
                <el-form-item>
                    <el-button @click="cancel">取消</el-button>
                    <el-button type="primary" @click="confirm">
                        确认
                    </el-button>
                </el-form-item>
            </el-form>
        </div>
    </el-dialog>
</template>


<style scoped>

</style>