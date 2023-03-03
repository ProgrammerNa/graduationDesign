<script setup lang="ts">
    import {useUserStore} from "../../store/user";
    import pinia from '../../plugins/pinia'
    import {ref, onMounted} from 'vue'
    import {getStoreList} from "../../api/store";
    import {resetUserPassword} from "../../api/systemApi";
    import addStore from './add.vue'
    import {useRouter} from 'vue-router'

    const currentStoreId = ref(useUserStore(pinia).userInfo.store_id)
    const currentPage = ref(1)
    const pageSize = ref(10)
    const tableData = ref([])
    const total = ref(0)
    const searchValue = ref('')
    const route = useRouter()
    const loading = ref(true)
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
        getStoreList({
            id: currentStoreId.value,
            currentPage: currentPage.value,
            pageSize: pageSize.value,
            search: searchValue.value
        }).then((res) => {
            if (res.status === 200) {
                tableData.value = res.data.data
                total.value = res.data.total
                setTimeout(() => {
                     loading.value = false
                },1000)
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
    const add = ref()
    const addNewStore = () => {
        add.value.open({
            title: '新增门店'
        })
    }
    const editor = (data: any) => {
        add.value.open({
            title: '编辑门店',
            rowData: data
        })
    }
    const centerDialogVisible = ref(false)
    const rowInfo = ref([])
    const restPassword = (data: any) => {
        centerDialogVisible.value = true
        rowInfo.value = data
    }
    const cancel = () => {
        centerDialogVisible.value = false
    }
    const confirm = () => {
        centerDialogVisible.value = false
        resetUserPassword({
            id: rowInfo.value.user_id
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
    const checkFenStaff = (data: any) => {
        console.log(data)
        route.push({path: "/fenStaffDetail", query: {storeId: data.store_id}})
    }
    onMounted(() => {
        getList()
    })
</script>

<template>
    <div class="container">
        <div class="search">
            <div class="search-input">
                <el-input v-model="searchValue" placeholder="请输入门店名称/负责人/联系方式查询">
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
                        门店信息
                    </div>
                </div>
                <div class="add-btn">
                    <el-button type="danger" @click="addNewStore">新增门店</el-button>
                </div>
            </div>
            <el-table v-loading="loading" :data="tableData" style="width: 100%" stripe border max-height="600px"
                      :header-cell-style="{
        'background': 'rgb(250,250,250)',
        'color':'black'
      }">
                <el-table-column prop="store_id" label="门店编号" align="center"></el-table-column>
                <el-table-column prop="store_name" label="门店名称" align="center"></el-table-column>
                <el-table-column prop="username" label="登陆账号" align="center"></el-table-column>
                <el-table-column prop="store_responsible" label="门店负责人" align="center"></el-table-column>
                <el-table-column prop="phone" label="联系方式" align="center"></el-table-column>
                <el-table-column prop="store_address" label="门店地址" align="center"></el-table-column>
                <el-table-column prop="option" label="操作" align="center" width="450">
                    <template #default="scope">
                        <el-button @click="editor(scope.row)">门店编辑
                        </el-button>
                        <el-button @click="restPassword(scope.row)">重置密码
                        </el-button>
                        <el-button>数据查看
                        </el-button>
                        <el-button @click="checkFenStaff(scope.row)">人员详情
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
        <el-dialog v-model="centerDialogVisible" title="提示" width="30%" align-center :show-close="false"
                   :close-on-click-modal="false">
            <span>
                确定要将{{rowInfo.username}}用户的密码重置为123456嘛？
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
        <addStore ref="add" :getStoreList="getList"></addStore>
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