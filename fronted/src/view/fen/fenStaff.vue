<script setup lang="ts">
    import {ref,onMounted} from 'vue'
    import {useRoute,useRouter} from 'vue-router'
    import {getStaffListByStoreId} from "../../api/staffApi";
    import {formateTime} from "../../utils/timeUtils";

    const route  = useRoute()
    const router = useRouter()
     const currentPage = ref(1)
    const pageSize = ref(10)
    const tableData = ref([])
    const total = ref(0)
    const searchValue = ref('')
    const back  = () => {
        router.push('/fendianMangement')
    }
     const getList = () => {
        tableData.value = []
        getStaffListByStoreId({
            id:route.query.storeId,
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
    }
    onMounted(() =>{
        getList()
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
                    <el-button type="danger" @click="back">返回</el-button>
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
                                disabled
                        />
                    </template>

                </el-table-column>
                <el-table-column prop="ruzhiTime" label="入职时间" align="center">
                </el-table-column>
                <el-table-column prop="lizhiTime" label="离职时间" align="center">
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