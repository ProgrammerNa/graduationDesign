<script setup lang="ts">
    import {ref, onMounted, defineProps, reactive} from 'vue'
    import {useUserStore} from "../../store/user";
    import pinia from '../../plugins/pinia'
    import {addStore} from "../../api/store";

    const props = defineProps({
        getStoreList: {
            type: Function,
            default: () => {
            }
        }
    })
    const currentStoreId = ref(useUserStore(pinia).userInfo.store_id)
    const ruleForm = reactive({
        username: '',
        password: '',
        repassword: '',
        storeName: '',
        storeResponsibleName: '',
        storePhone: '',
        storeAddress: ''
    })
    const show = ref(false)
    //点击详情该行的用户id
    const open = () => {
        show.value = true
    }
    const ruleFormRef = ref()
    const validatePhone = (rule: any, value: any, callback: any) => {
        if (value === '') {
            callback(new Error('请填写联系方式'))
        } else {
            if (!(/^1[0123456789]\d{9}$/.test(ruleForm.storePhone))) {
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
            {required: true, message: '请输入登录用户名', trigger: 'blur'},
        ],
        storeName: [
            {required: true, message: '请输入新增门店名称', trigger: 'blur'},
        ],
        storeResponsibleName: [
            {required: true, message: '请选择新增门店负责人', trigger: 'blur'},
        ],
        storeAddress: [
            {required: true, message: '请选择新增门店地址', trigger: 'blur'},
        ],
        password: [{required: true, validator: validatePass, trigger: 'blur'}],
        repassword: [{required: true, validator: validatePass2, trigger: 'blur'}],
        storePhone: [{required: true, validator: validatePhone, trigger: 'blur'}],
    })
    const confirm = () => {
        ruleFormRef.value.validate((valid: any) => {
            if (valid) {
                addStore({
                    username: ruleForm.username,
                    password: ruleForm.password,
                    storeName: ruleForm.storeName,
                    storeAddress: ruleForm.storeAddress,
                    storeResponsible: ruleForm.storeResponsibleName,
                    phone: ruleForm.storePhone,
                    parentId: currentStoreId.value
                }).then((res) => {
                    if (res.status === 200) {
                        // @ts-ignore
                        ElMessage({
                            message: '新增成功',
                            type: 'success',
                        })
                        props.getStoreList()
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
            }
        })
    };
    const cancel = () => {
        show.value = false;
        ruleForm.username = '';
        ruleForm.password = '';
        ruleForm.repassword = '';
        ruleForm.storeName = '';
        ruleForm.storeResponsibleName = '';
        ruleForm.storePhone = '';
        ruleForm.storeAddress = ''
    };
    defineExpose({
        open,
    })

</script>


<template>
    <el-dialog
            v-model="show"
            title="新增门店"
            width="50%"
            align-center
            @open="init"
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
                <el-form-item label="门店名称" prop="storeName">
                    <el-input v-model="ruleForm.storeName" placeholder="请输入新增门店名称"></el-input>
                </el-form-item>
                <el-form-item label="门店负责人" prop="storeName">
                    <el-input v-model="ruleForm.storeResponsibleName" placeholder="请输入新增门店负责人"></el-input>
                </el-form-item>
                <el-form-item label="联系方式" prop="storePhone">
                    <el-input v-model="ruleForm.storePhone" placeholder="请输入负责人联系方式"></el-input>
                </el-form-item>
                <el-form-item label="门店地址" prop="storeAddress">
                    <el-input v-model="ruleForm.storeAddress" placeholder="请输入新增门店地址"></el-input>
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