<script setup lang="ts">
    import {ref, onMounted} from 'vue'
    import {getRoleName} from "../../api/systemApi";

    const ruleForm = ref({
        username: '',
        password: '',
        repassword: '',
        permission: ''
    })
    const roleValue = ref('')
    const roleOptions = ref([])
    const show = ref(false)
    //点击详情该行的用户id
    const open = () => {
        show.value = true
    }
    const getRoleList = () => {
        getRoleName().then((res) => {
            if (res.status === 200) {
                res.data.forEach((item) => {
                    roleOptions.value.push({
                        value: item.id,
                        label: item.role,
                    })
                })
                console.log(roleOption.value)
            }
        })
    }
    const init = () => {
        getRoleList()
    }
    defineExpose({
        open
    })

</script>


<template>
    <el-dialog
            v-model="show"
            title="新增用户"
            width="50%"
            align-center
            @open="init"
    >
        <div class="container">
            <el-form ref="ruleFormRef"
                     :model="ruleForm"
                     :rules="rules"
                     label-width="120px">
                <el-form-item label="用户名" prop="username">
                    <el-input v-model="ruleForm.username" placeholder="请输入用户名"></el-input>
                </el-form-item>
                <el-form-item label="密码" prop="password">
                    <el-input v-model="ruleForm.password" placeholder="请输入密码"></el-input>
                </el-form-item>
                <el-form-item label="重复密码" prop="repassword">
                    <el-input v-model="ruleForm.repassword" placeholder="请确认密码"></el-input>
                </el-form-item>
                <el-form-item label="用户权限" prop="permission">
                    <el-select v-model="roleValue" placeholder="请选择用户角色">
                        <el-option
                                v-for="item in roleOptions"
                                :key="item.value"
                                :label="item.label"
                                :value="item.value"
                        />
                    </el-select>
                </el-form-item>

            </el-form>

        </div>
    </el-dialog>
</template>


<style scoped>

</style>