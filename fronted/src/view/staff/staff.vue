<script setup lang="ts">
    import {useUserStore} from "../../store/user";
    import pinia from '../../plugins/pinia'
    import {ref, onMounted,defineEmits,defineExpose} from 'vue'
    import {getStaffListByStoreId,changeStaffStatus} from "../../api/staffApi";
    import {formateTime} from '../../utils/timeUtils'
     import {resetUserPassword} from '../../api/systemApi'
    import addStaffVue from './add.vue'
    const currentStoreId = ref(useUserStore(pinia).userInfo.store_id)
    const currentPage = ref(1)
    const pageSize = ref(10)
    const tableData = ref([])
    const total = ref(0)
    const searchValue = ref('')
    const statusValue = ref()
    const statusOption = ref([{
        value: 1,
        label: '在职'
    }, {
        value: 0,
        label: '离职'
    }])

    const handleSizeChange = (val: any) => {
        pageSize.value = val
        currentPage.value = val = 1
        getList()
    }
    const handleCurrentChange = (val: any) => {
        currentPage.value = val
        getList()
    }
    const getList = () => {
        tableData.value = []
        getStaffListByStoreId({
            id: currentStoreId.value,
            currentPage: currentPage.value,
            pageSize: pageSize.value,
            search: searchValue.value
        }).then((res) => {
            if (res.status === 200) {
                res.data.data.forEach((val) => {
                    tableData.value.push({
                        userId:val.id,
                        staffId: val.yuan_id,
                        staffName: val.name,
                        username: val.username,
                        staffPhone: val.y_phone,
                        status: val.type === 1 ? true :false,
                        ruzhiTime: formateTime(val.ruzhi_time),
                        lizhiTime: val.type === 0 ? formateTime(val.lizhi_time) : '-'
                    })

                })
                total.value = res.data.total
            }
        })
    }
    const search = () => {
        getList()
        console.log(searchValue.value)
    }
    const reset = () => {
        searchValue.value = ''
        getList()
    }
    const changeStatus = (data:any) => {
       if(data.status === true){
           changeStaffStatus({
               id:data.userId,
               flag:1,type:1
           }).then(res => {
               if(res.status === 200){
                   tableData.value = []
                    // @ts-ignore
                ElMessage({
                    message: '更改成功',
                    type: 'success',
                })
                   getList()
               }else{
                    // @ts-ignore
                ElMessage({
                    message: '更改失败',
                    type: 'error',
                })
               }
           }).catch(err => {
                // @ts-ignore
                ElMessage({
                    message: '更改失败',
                    type: 'error',
                })
           })
       }else{
           changeStaffStatus({
               id:data.userId,
               flag:0,type: 0
           }).then(res => {
               if(res.status === 200){
                   tableData.value = []
                    getList()
                    // @ts-ignore
                ElMessage({
                    message: '更改成功',
                    type: 'success',
                })
               }else{
                    // @ts-ignore
                ElMessage({
                    message: '更改失败',
                    type: 'error',
                })
               }
           })
       }
    }
    const centerDialogVisible = ref(false)
    const rowInfo = ref([])
     const restPassword = (data: any) => {
        centerDialogVisible.value = true
        rowInfo.value = data
        console.log(rowInfo.value)

    }
    const cancel = () => {
        centerDialogVisible.value = false
    }
    const confirm = () => {
        centerDialogVisible.value = false
        resetUserPassword({
            id: rowInfo.value.userId
        }).then((res) => {
            if (res.status === 200) {
                // @ts-ignore
                ElMessage({
                    message: '密码重置成功',
                    type: 'success',
                })
            }
        }).catch((err) => {
            // @ts-ignore
            ElMessage({
                message: '密码重置失败',
                type: 'error',
            })
        })
    }
    const text = ref('sdsds')
    const add = ref()
    const addStaff = () => {
        add.value.open()
    }
    onMounted(() => {
        getList()
    })
    defineExpose({

    })
</script>

<template>
    <div class="container">
        <div class="search">
            <div class="search-input">
                <el-input v-model="searchValue" placeholder="请输入员工姓名查询">
                </el-input>
            </div>
            <div class="option-btn">
                <div class="search-bnt">
                    <el-button type="primary" @click="search">查询</el-button>
                </div>
                <div class="reset-bnt">
                    <el-button type="info" @click="reset">重置</el-button>
                </div>
            </div>
        </div>
        <div class="store_table_container">
            <div class="user-table-head">
                <div class="user-table-title">
                    <div class="table-border"></div>
                    <div class="table-title">
                        员工信息
                    </div>
                </div>
                <div class="add-btn">
                    <el-button type="danger" @click="addStaff">新增员工</el-button>
                </div>
            </div>
            <el-table :data="tableData" style="width: 100%" stripe border max-height="600px"
                      :header-cell-style="{
        'background': 'rgb(250,250,250)',
        'color':'black'
      }">
                <el-table-column prop="staffId" label="员工编号" align="center"></el-table-column>
                <el-table-column prop="staffName" label="员工姓名" align="center"></el-table-column>
                <el-table-column prop="username" label="登录账户" align="center"></el-table-column>
                <el-table-column prop="staffPhone" label="联系方式" align="center"></el-table-column>
                <el-table-column prop="status" label="员工状态" align="center">
                    <template #default="scope">
                        <el-switch
                                v-model="scope.row.status"
                                active-text="在职"
                                inactive-text="离职"
                                @change="changeStatus(scope.row)"
                        />
                    </template>

                </el-table-column>
                <el-table-column prop="ruzhiTime" label="入职时间" align="center">
                </el-table-column>
                <el-table-column prop="lizhiTime" label="离职时间" align="center">
                </el-table-column>
                <el-table-column prop="option" label="操作" align="center">
                    <template #default="scope">
                        <el-button @click="restPassword(scope.row)">重置密码
                        </el-button>
                    </template>
                </el-table-column>
            </el-table>
            <el-pagination
                    background layout="->,total,sizes,prev,pager,next,jumper"
                    :current-page="currentPage"
                    :page-size="pageSize"
                    :total="total"
                    :page-sizes="[10, 20, 30, 40, 50]"
                    @size-change="handleSizeChange"
                    @current-change="handleCurrentChange"

            />
        </div>
        <el-dialog v-model="centerDialogVisible" title="提示" width="30%" center>
            <span>
                确定要将{{rowInfo.staffName}}员工的密码重置为123456嘛？
            </span>
            <template #footer>
                <span class="dialog-footer">
                    <el-button @click="cancel">取消</el-button>
                    <el-button type="primary" @click="confirm">
                        确认
                    </el-button>
                </span>
            </template>
        </el-dialog>
        <addStaffVue ref="add" :getstaffList="getList" ></addStaffVue>
    </div>

</template>


<style lang="scss" scoped>
    .container {
        .search {
            height: 70px;
            background-color: white;
            display: flex;
            align-items: center;
            border: 1px solid #eaeaea;
            border-radius: 5px;


            .search-input {
                width: 300px;
                margin-left: 10px;
            }

            .option-btn {
                margin-left: 50px;
                display: flex;
                align-items: center;
                justify-items: center;

                .search-bnt {
                    margin-right: 20px;
                }
            }
        }

        .store_table_container {
            margin-top: 20px;
            background-color: white;
            height: calc(100vh - 210px);

            .user-table-head {
                display: flex;
                align-items: center;
                justify-content: space-between;
                margin-left: 5px;

                .add-btn {
                    margin-right: 10px;
                }

                .user-table-title {
                    display: flex;
                    align-items: center;

                    .table-border {
                        border: 2px solid #d1d1d1;
                        height: 25px;
                        margin-left: 10px;
                        margin-right: 5px;
                    }

                    .table-title {
                        height: 50px;
                        margin-left: 5px;
                        font-size: 25px;
                        line-height: 50px;
                    }

                }

            }

            .el-pagination {
                margin-top: 20px;
                margin-right: 20px
            }
        }
    }
</style>