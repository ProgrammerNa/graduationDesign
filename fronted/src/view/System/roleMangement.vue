<script setup lang="ts">
    import {getRoleList, changeUserActivate} from "../../api/systemApi";
    import {ref, onMounted, defineExpose} from 'vue'
    import {useUserStore} from "../../store/user";
    import pinia from "../../plugins/pinia";
    import editRole from './add.vue'

    const tableData = ref<any[]>([])
    const searchValue = ref<any>('')
    const currentId = ref(useUserStore(pinia).userInfo)
    const currentPage = ref(1)
    const pageSize = ref(5)
    const total = ref(0)
    const loading = ref(false)
    const handleSizeChange = (val: any) => {
        pageSize.value = val
        currentPage.value = val = 1
        getList()
    }
    const handleCurrentChange = (val: any) => {
        currentPage.value = val
        getList()
    }
    const search = () => {
        getList()
        console.log(searchValue.value)
    }
    const reset = () => {
        searchValue.value = ''
        getList()
        console.log(searchValue.value)
    }
    const getList = () => {
        tableData.value = []
        getRoleList({
            pageSize: pageSize.value,
            currentPage: currentPage.value,
            search: searchValue.value
        }).then((res) => {
            if (res.status === 200) {
                total.value = res.data.total
                tableData.value = res.data.data
            }
        })

    };
    const changeRoleActivate = (data:any) => {
        console.log(data)
    }
    const edit = ref()
    const editor = (data:any) => {
        edit.value.open(data)
    }
    onMounted(() => {
        getList()
    })
</script>


<template>
    <div class="container">
        <div class="search">
            <div class="title">角色名:</div>
            <div class="search-input">
                <el-input v-model="searchValue" placeholder="请输入角色名查询">
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
        <div class="user-table">
            <div class="user-table-head">
                <div class="user-table-title">
                    <div class="table-border"></div>
                    <div class="table-title">
                        角色列表
                    </div>
                </div>
            </div>
            <el-table :data="tableData" style="width: 100%" stripe border max-height="600px"
                      :header-cell-style="{
        'background': 'rgb(250,250,250)',
        'color':'black'
      }">
                <el-table-column prop="role_id" label="ID" align="center"/>
                <el-table-column prop="role" label="角色名称" align="center"/>
                <el-table-column prop="menuName" label="菜单权限" align="center"/>
                <el-table-column prop="option" label="操作" align="center">
                    <template #default="scope">
                        <el-button @click="editor(scope.row)">编辑</el-button>
                    </template>
                </el-table-column>

            </el-table>
            <el-pagination
                    background layout="->,total,sizes,prev,pager,next,jumper"
                    :current-page="currentPage"
                    :page-size="pageSize"
                    :total="total"
                    :page-sizes="[5,10, 20, 30, 40, 50]"
                    @size-change="handleSizeChange"
                    @current-change="handleCurrentChange"

            />
        </div>
        <editRole ref="edit" :getList="getList"></editRole>
    </div>
</template>


<style lang="scss" scoped>
    .search {
        height: 70px;
        background-color: white;
        display: flex;
        align-items: center;
        justify-items: center;
        border: 1px solid #eaeaea;
        border-radius: 5px;

        .title {
            margin-left: 10px;
        }

        .search-input {
            width: 300px;
            margin-left: 5px;
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

     .user-table {
        margin-top: 20px;
        background-color: white;
        height: calc(100vh - 210px);

        .user-table-head {
            display: flex;
            align-items: center;
            justify-content: space-between;

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
</style>