<script setup lang="ts">
    import {getUserList, changeUserActivate} from "../../api/systemApi";
    import {ref, onMounted, defineExpose} from 'vue'
    import {useUserStore} from "../../store/user";
    import pinia from "../../plugins/pinia";
    import {resetUserPassword} from '../../api/systemApi'
    import addVue from './add.vue'

    const tableData = ref<any[]>([]);
    const searchValue = ref<any>('');
    const currentId = ref(useUserStore(pinia).userInfo);
    const userDiaglos = ref();
    const currentPage = ref(1);
    const pageSize = ref(5);
    const total = ref(0);
    const loading = ref(false);
    const btnLoading = ref(false);
    const handleSizeChange = (val: any) => {
        pageSize.value = val
        currentPage.value = val = 1;
        getListUser()
    }
    const handleCurrentChange = (val: any) => {
        currentPage.value = val;
        getListUser()
    }
    const search = () => {
        getListUser();
        console.log(searchValue.value)
    }
    const reset = () => {
        searchValue.value = '';
        getListUser();
        console.log(searchValue.value)
    }
    const getListUser = () => {
        tableData.value = [];
        getUserList({
            pageSize: pageSize.value,
            currentPage: currentPage.value,
            search: searchValue.value
        }).then((res) => {
            if (res.status === 200) {
                total.value = res.data.total
                res.data.data.forEach((val) => {
                    if (val.flag === 1) {
                        tableData.value.push({
                            id: val.user_id,
                            show: true,
                            username: val.username,
                            roleName: val.role,
                            storeName: val.store_name
                        })
                    } else {
                        tableData.value.push({
                            id: val.user_id,
                            show: false,
                            username: val.username,
                            roleName: val.role,
                            storeName: val.store_name
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
                        message: '????????????',
                        type: 'success',
                    })
                    setTimeout(() => {
                        loading.value = false
                    }, 2000)
                }
            }).catch((err) => {
                // @ts-ignore
                ElMessage({
                    message: '????????????',
                    type: 'error',
                })
                setTimeout(() => {
                    loading.value = false
                }, 2000)
            })
        } else {
            changeUserActivate({
                flag: 1,
                id: data.id
            }).then((res) => {
                if (res.status === 200) {
                    // @ts-ignore
                    ElMessage({
                        message: '????????????',
                        type: 'success',
                    })
                    setTimeout(() => {
                        loading.value = false
                    }, 2000)
                }
            }).catch((err) => {
                // @ts-ignore
                ElMessage({
                    message: '????????????',
                    type: 'error',
                })
                setTimeout(() => {
                    loading.value = false
                }, 2000)
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
        btnLoading.value = true
        resetUserPassword({
            id: rowInfo.value.id
        }).then((res) => {
            if (res.status === 200) {
                // @ts-ignore
                ElMessage({
                    message: '??????????????????',
                    type: 'success',
                })
                setTimeout(() => {
                    btnLoading.value = false
                }, 2000)
            }
        }).catch((err) => {
            // @ts-ignore
            ElMessage({
                message: '??????????????????',
                type: 'error',
            })
            setTimeout(() => {
                btnLoading.value = false
            }, 2000)
        })
    }
    const add = ref()
    const addUser = () => {
        add.value.open()
    }
    onMounted(() => {
        getListUser()
    })
</script>


<template>
    <div class="container">
        <div class="search">
            <div class="title">?????????:</div>
            <div class="search-input">
                <el-input v-model="searchValue" placeholder="????????????????????????">
                </el-input>
            </div>
            <div class="option-btn">
                <div class="search-bnt">
                    <el-button type="primary" @click="search">??????</el-button>
                </div>
                <div class="reset-bnt">
                    <el-button type="info" @click="reset">??????</el-button>
                </div>
            </div>
        </div>
        <div class="user-table">
            <div class="user-table-head">
                <div class="user-table-title">
                    <div class="table-border"></div>
                    <div class="table-title">
                        ????????????
                    </div>
                </div>
            </div>
            <el-table :data="tableData" style="width: 100%" stripe border max-height="600px"
                      :header-cell-style="{
        'background': 'rgb(250,250,250)',
        'color':'black'
      }">
                <el-table-column prop="username" label="?????????" align="center"/>
                <el-table-column prop="roleName" label="??????" align="center"/>
                <el-table-column prop="flag" label="????????????" align="center">
                    <template #default="scope">
                        <el-switch
                                v-model="scope.row.show"
                                inline-prompt
                                active-text="??????"
                                inactive-text="??????"
                                :disabled="currentId.id === scope.row.id?true:false"
                                @change="changeUserActivite(scope.row)"
                                :loading="loading"
                        />
                    </template>
                </el-table-column>
                <el-table-column prop="storeName" label="????????????" align="center"></el-table-column>
                <el-table-column prop="option" label="??????" align="center">
                    <template #default="scope">
                        <el-button @click="restPassword(scope.row)" :disabled="currentId.id === scope.row.id?true:false"
                                   :loading="btnLoading">????????????
                        </el-button>
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
        <el-dialog v-model="centerDialogVisible" title="??????" width="30%" align-center :show-close="false"
                   :close-on-click-modal="false">
            <span>
                ????????????{{rowInfo.username}}????????????????????????123456??????
            </span>
            <template #footer>
                <span class="dialog-footer">
                    <el-button @click="cancel">??????</el-button>
                    <el-button type="primary" @click="confirm">
                        ??????
                    </el-button>
                </span>
            </template>
        </el-dialog>
        <addVue ref="add"></addVue>
    </div>
</template>


<style lang="scss" scoped>
    .search {
        height: 70px;
        background-color: white;
        display: flex;
        align-items: center;
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