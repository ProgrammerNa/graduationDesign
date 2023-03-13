<script setup lang="ts">
    import {ref, onMounted, defineProps, reactive} from 'vue'
    import {useUserStore} from "../../store/user";
    import pinia from '../../plugins/pinia'
    import {addNewStaff} from '../../api/staffApi'

    const props = defineProps({
        getstaffList: {
            type: Function,
            default: () => {
            }
        }
    })
    const currentStoreId = ref(useUserStore(pinia).userInfo.store_id)
    const dialogs = ref()
    const ruleForm = reactive({
        username: '',
        password: '',
        repassword: '',
        name: '',
        sex: '',
        staffPhone: ''
    })
    const show = ref(false)
    //点击详情该行的用户id
    const open = () => {
        show.value = true
    }
    const changeSex = (data: any) => {
        ruleForm.sex = data

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
        username: [
            {required: true, message: '请输入用户名', trigger: 'blur'},
        ],
        name: [
            {required: true, message: '请输入员姓名', trigger: 'blur'},
        ],
        sex: [
            {required: true, message: '请选择员工性别', trigger: 'blur'},
        ],
        password: [{required: true, validator: validatePass, trigger: 'blur'}],
        repassword: [{required: true, validator: validatePass2, trigger: 'blur'}],
        staffPhone: [{required: true, validator: validatePhone, trigger: 'blur'}],
    })
    const confirm = () => {
        ruleFormRef.value.validate((valid: any) => {
            if (valid) {
                addNewStaff({
                    store: currentStoreId.value,
                    username: ruleForm.username,
                    password: ruleForm.password,
                    repassword: ruleForm.repassword,
                    name: ruleForm.name,
                    y_phone: ruleForm.staffPhone,
                    sex: parseInt(ruleForm.sex)
                }).then((res) => {
                    if (res.status === 200) {
                        // @ts-ignore
                        ElMessage({
                            message: '新增成功',
                            type: 'success',
                        })
                        props.getstaffList()
                        show.value = false
                    } else {
                        // @ts-ignore
                        ElMessage({
                            message: '新增失败',
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
            } else {
                console.log('验证出错')
            }
        })


    }
    const cancel = () => {
        show.value = false;
        ruleFormRef.value.resetFields()
    }

    defineExpose({
        open,
    })

</script>


<template>
    <el-dialog
            v-model="show"
            title="新增员工"
            width="50%"
            align-center
            @open="init"
            ref="dialogs"
            :show-close="false"
            :close-on-click-modal="false"
    >
        <div class="container">
            <el-form
                    :model="ruleForm" ref="ruleFormRef" :rules="rules" label-width="120">
                <el-form-item label="登录用户名" prop="username">
                    <el-input v-model="ruleForm.username" placeholder="请输入登录用户名"></el-input>
                </el-form-item>
                <el-form-item label="密码" prop="password">
                    <el-input type="password" v-model="ruleForm.password" show-password="true"
                              placeholder="请输入密码"></el-input>
                </el-form-item>
                <el-form-item label="重复密码" prop="repassword">
                    <el-input type="password" v-model="ruleForm.repassword" show-password="true"
                              placeholder="请确认密码"></el-input>
                </el-form-item>
                <el-form-item label="真实姓名" prop="name">
                    <el-input v-model="ruleForm.name" placeholder="请输入员工真实姓名"></el-input>
                </el-form-item>
                <el-form-item label="性别" prop="sex">
                    <el-radio-group v-model="ruleForm.sex" class="ml-4" @change="changeSex">
                        <el-radio label="1" size="large">男</el-radio>
                        <el-radio label="2" size="large">女</el-radio>
                    </el-radio-group>
                </el-form-item>
                <el-form-item label="联系方式" prop="staffPhone">
                    <el-input v-model="ruleForm.staffPhone" placeholder="请输入员工联系方式"></el-input>
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