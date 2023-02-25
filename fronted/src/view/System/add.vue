<script setup lang="ts">
    import {ref, reactive} from 'vue'
    import {changeRoleMenu} from "../../api/systemApi";
    import {useUserStore} from "../../store/user";
    import pinia from "../../plugins/pinia";
    import {getAllMenuList} from "../../api/menu";
    import {useRouter} from 'vue-router'

     const props = defineProps({
        getList: {
            type: Function,
            default: () => {
            }
        }
    })
    const currentRoleId = ref(useUserStore(pinia).userInfo.role_id)
    const route = useRouter()
    const ruleForm = ref({
        roleId: '',
        roleName: '',
        roleValue: [],
    })
    const editRowInfo = ref()
    const roleValue = ref([])
    const roleOptions = ref([])
    const show = ref(false)
    //点击详情该行的用户id
    const open = (data: any) => {
        show.value = true;
        editRowInfo.value = data
        roleValue.value = data.menu_id.split(',')
    }
    const getMenu = () => {
        roleOptions.value = []
        getAllMenuList().then((res) => {
            if (res.status === 200) {
                res.data.forEach((val) => {
                    roleOptions.value.push({
                        value: String(val.id),
                        label: val.menu
                    })
                })

            }
        })
    }
    const chagRolePermission = (data: any) => {
         ruleForm.value.roleValue = []
         ruleForm.value.roleValue= data
    }
    const cancel = () => {
        show.value = false
    }
    const ruleFormRef = ref()
    const changeRolePermission = () => {
        ruleFormRef.value.validate((valid: any) => {
            if (valid) {
                changeRoleMenu({
                    menuId: ruleForm.value.roleValue,
                    roleId: editRowInfo.value.role_id
                }).then((res) => {
                    if (res.status === 200) {
                        show.value = false
                        props.getList()
                        if (editRowInfo.value.role_id === currentRoleId.value) {
                            setTimeout(() => {
                                  route.push('/')
                            },2000)

                        }
                        // @ts-ignore
                        ElMessage({
                            message: '修改角色权限成功',
                            type: 'success',
                        })
                    } else {
                        // @ts-ignore
                        ElMessage({
                            message: '修改角色权限失败',
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
    const centerDialogVisible = ref(false)
    const confirmChange = () => {
        centerDialogVisible.value = false
        changeRolePermission()
    }
    const confirm = () => {
        if (editRowInfo.value.role_id === currentRoleId.value) {
            centerDialogVisible.value = true
        }else{
            changeRolePermission()
        }
    }
    const cancelChange = () =>{
        centerDialogVisible.value = false
    }
    const rules = reactive({
        roleValue: [
            {required: true, message: '请选择要更改的菜单权限', trigger: 'change'},
        ],
    })
    const init = () => {
        getMenu()
    }
    defineExpose({
        open
    })

</script>


<template>
    <el-dialog
            v-model="show"
            title="编辑角色"
            width="50%"
            align-center
            @open="init"
    >
        <div class="container">
            <el-form ref="ruleFormRef"
                     :model="ruleForm"
                     :rules="rules"
                     label-width="120px">
                <el-form-item label="角色ID" prop="roleId">
                    <div>{{editRowInfo.role_id}}</div>
                </el-form-item>
                <el-form-item label="角色名称" prop="roleName">
                    <div>{{editRowInfo.role}}</div>
                </el-form-item>
                <el-form-item label="菜单权限" prop="roleValue">
                    <el-select v-model="roleValue" placeholder="请选择用户角色" collapse-tags multiple
                               @change="chagRolePermission">
                        <el-option
                                v-for="item in roleOptions"
                                :key="item.value"
                                :label="item.label"
                                :value="item.value"
                        />
                    </el-select>
                </el-form-item>
                <el-form-item>
                    <el-button @click="confirm">确认</el-button>
                    <el-button @click="cancel">关闭</el-button>
                </el-form-item>
            </el-form>
            <el-dialog v-model="centerDialogVisible" title="提示" width="30%" center>
            <span>
               您修改的角色权限是当前用户，是否确认修改？
            </span>
                <template #footer>
                <span class="dialog-footer">
                    <el-button @click="cancelChange">取消</el-button>
                    <el-button type="primary" @click="confirmChange">
                        确认
                    </el-button>
                </span>
                </template>
            </el-dialog>
        </div>
    </el-dialog>
</template>


<style scoped>

</style>