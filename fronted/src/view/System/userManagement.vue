<script setup lang="ts">
    import {getUserList, changeUserActivate} from "../../api/systemApi";
    import {ref, onMounted} from 'vue'
    import {useUserStore} from "../../store/user";
    import pinia from "../../plugins/pinia";

    const tableData = ref<any[]>([])
    const currentId = ref(useUserStore(pinia).userInfo)
    const loading= ref(false)
    const getListUser = () => {
        getUserList().then((res) => {
            if (res.status === 200) {
                res.data.forEach((val) => {
                    if (val.flag === 1) {
                        tableData.value.push({
                            id: val.user_id,
                            show: true,
                            username: val.username,
                            roleName: val.role,
                        })
                    } else {
                        tableData.value.push({
                            id: val.user_id,
                            show: false,
                            username: val.username,
                            roleName: val.role,
                        })
                    }
                })
            }
        })

    };
    const changeUserActivite = (data: any) => {
        loading.value = true
        if (data.show === false) {
            changeUserActivate({
                flag: 0,
                id: data.id
            }).then((res) => {
                if (res.status === 200) {
                    // @ts-ignore
                    ElMessage({
                        message: '禁用成功',
                        type: 'success',
                    })
                    setTimeout(() =>{
                        loading.value=false
                    },2000)
                }
            }).catch((err) => {
                  // @ts-ignore
                    ElMessage({
                        message: '禁用失败',
                        type: 'error',
                    })
            })
        } else {
            changeUserActivate({
                flag: 1,
                id: data.id
            }).then((res) => {
                if (res.status === 200) {
                    // @ts-ignore
                    ElMessage({
                        message: '启用成功',
                        type: 'success',
                    })
                     setTimeout(() =>{
                        loading.value=false
                    },2000)
                }
            }).catch((err) => {
                  // @ts-ignore
                    ElMessage({
                        message: '启用失败',
                        type: 'error',
                    })
            })
        }

    }
    onMounted(() => {
        getListUser()
    })
</script>


<template>
    <div class="container">
        <el-table :data="tableData" style="width: 100%" stripe border
                  :header-cell-style="{
        'background': 'rgb(250,250,250)',
        'color':'black'
      }">
            <el-table-column prop="username" label="用户名" align="center"/>
            <el-table-column prop="roleName" label="角色" align="center"/>
            <el-table-column prop="flag" label="启用禁用" align="center">
                <template #default="scope">
                    <el-switch
                            v-model="scope.row.show"
                            inline-prompt
                            active-text="启用"
                            inactive-text="禁用"
                            :disabled="currentId.id === scope.row.id?true:false"
                            @change="changeUserActivite(scope.row)"
                            :loading="loading"
                    />
                </template>
            </el-table-column>
            <el-table-column prop="option" label="操作" align="center">
                <template #default>
                    <el-button>详情</el-button>
                </template>
            </el-table-column>
        </el-table>
    </div>
</template>


<style lang="scss" scoped>

</style>