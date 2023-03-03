<script setup lang="ts">
    import {ref, onMounted, defineProps, reactive} from 'vue'
    import {useUserStore} from "../../store/user";
    import pinia from '../../plugins/pinia'
    import {addStore, updateStoreInfo} from "../../api/store";
    import {getCity} from "../../api/areaApi";

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
        storeAddress: [],
        storeId: ''
    })
    //loading加载
    const loading = ref(true)
    const show = ref(false)
    //点击详情该行的用户id
    const title = ref('')
    const cityOptions = ref([])
    const selectOptions = ref('')
    const cityProps = ref({
        value: 'name',
        label: 'name',
        children: 'districts',
    })
    const open = (data: any) => {
        show.value = true
        loading.value = true
        title.value = data.title
        if (data.title === '编辑门店') {
            ruleForm.storeId = data.rowData.store_id
            ruleForm.username = data.rowData.username;
            ruleForm.storeName = data.rowData.store_name;
            ruleForm.storeResponsibleName = data.rowData.store_responsible;
            ruleForm.storePhone = data.rowData.phone;
            selectOptions.value = data.rowData.store_address.split(',');
        }
    }
    const getAreaList = () => {
        getCity().then(res => {
            if (res.status === 200) {
                cityOptions.value = getTreeData(
                    res.data.districts[0].districts
                )
                loading.value = false
            }
        })
    }
    /* 递归处理末尾项district为0的空项 */
    const getTreeData = (data: any) => {
        // 循环遍历返回的数据
        for (var i = 0; i < data.length; i++) {
            if (data[i].districts.length < 1) {
                // districts若为空数组，则将districts设为undefined
                data[i].districts = undefined
            } else {
                // districts若不为空数组，则继续 递归调用 本方法
                getTreeData(data[i].districts)
            }
        }
        return data
    }
    const ruleFormRef = ref()
    const validateAddress = (rule: any, value: any, callback: any) => {
        value = selectOptions.value
        if (selectOptions.value === '') {
            callback(new Error('请选择门店地址'))
        } else {
            callback()

        }
    }
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
            {required: true, validator: validateAddress, trigger: 'blur'},
        ],
        password: [{required: true, validator: validatePass, trigger: 'blur'}],
        repassword: [{required: true, validator: validatePass2, trigger: 'blur'}],
        storePhone: [{required: true, validator: validatePhone, trigger: 'blur'}],
    })
    const addStoreForm = () => {
        addStore({
            username: ruleForm.username,
            password: ruleForm.password,
            storeName: ruleForm.storeName,
            storeAddress: selectOptions.value.toString(),
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
    }
    const updateStore = () => {
        updateStoreInfo({
            storeId: ruleForm.storeId,
            storeName: ruleForm.storeName,
            storeAddress: selectOptions.value.toString(),
            storeResponsibleName: ruleForm.storeResponsibleName,
            storePhone: ruleForm.storePhone,
        }).then((res) => {
            if (res.status === 200) {
                // @ts-ignore
                ElMessage({
                    message: '修改成功',
                    type: 'success',
                })
                props.getStoreList()
                show.value = false
            } else {
                // @ts-ignore
                ElMessage({
                    message: '修改失败',
                    type: 'error',
                })
            }
        }).catch(err => {
            // @ts-ignore
            ElMessage({
                message: '修改失败',
                type: 'error',
            })
        })
    }
    const confirm = () => {
        ruleFormRef.value.validate((valid: any) => {
            if (valid) {
                if (title.value === '新增门店') {
                    addStoreForm()
                } else {
                    updateStore()
                }
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
        ruleForm.storeAddress = []
        selectOptions.value = ''
    };
    const change = (data: any) => {
        selectOptions.value = data
    }
    onMounted(() => {
        getAreaList()
    })
    defineExpose({
        open,
    })

</script>


<template>
    <el-dialog
            v-model="show"
            v-loading="loading"
            :title="title"
            width="50%"
            align-center
            @open="init"
            :show-close="false"
            :close-on-click-modal="false"
    >
        <div class="container">
            <el-form
                    :model="ruleForm" ref="ruleFormRef" :rules="rules" label-width="120">
                <el-form-item label="登录用户名" prop="username">
                    <el-input v-model="ruleForm.username" placeholder="请输入登录用户名" v-if="title === '新增门店'"></el-input>
                    <el-input v-model="ruleForm.username" v-if="title === '编辑门店'" disabled></el-input>
                </el-form-item>
                <el-form-item label="密码" prop="password" v-if="title === '新增门店'">
                    <el-input type="password" v-model="ruleForm.password" show-password="true"
                              placeholder="请输入密码"></el-input>
                </el-form-item>
                <el-form-item label="重复密码" prop="repassword" v-if="title === '新增门店'">
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
                    <el-cascader
                            filterable
                            placeholder="请选择"
                            ref="addPoint"
                            :props="cityProps"
                            :options="cityOptions"
                            clearable
                            v-model="selectOptions"
                            @change="change"
                            style="width: 800px"
                    ></el-cascader>
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