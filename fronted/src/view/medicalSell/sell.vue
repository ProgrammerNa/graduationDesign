<script setup lang="ts">
    import {onMounted, ref} from "vue";
    import {getMedicalTree} from "../../api/medical";
    import {tree} from "../../utils/treeUtilr";
    import {sellMedicalList} from '../../api/medical'
    import {useUserStore} from "../../store/user";
    import pinia from '../../plugins/pinia'
    import sellInfo from './sellInfo.vue'
    import {formateTime} from "../../utils/timeUtils";

    const currentStoreId = ref(useUserStore(pinia).userInfo.store_id)
    const searchValue = ref('')
    const treeData = ref([])
    const defaultProps = {
        children: 'children',
        label: 'type_name',
    }
    const currentPage = ref(1)
    const pageSize = ref(10)
    const tableData = ref([])
    const total = ref(0)
    const sell = ref()
    const getTree = () => {
        getMedicalTree().then(res => {
            if (res.status === 200) {
                treeData.value = tree(res.data)
            }
        })
    }
    const handleSizeChange = (val: any) => {
        pageSize.value = val
        currentPage.value = val = 1
        getSellList()
    }
    const handleCurrentChange = (val: any) => {
        currentPage.value = val
        getSellList()
    }
    const handleNodeClick = (data: any) => {
        searchValue.value = data.type_name
    }
    const search = () => {
        getSellList()
        console.log(searchValue.value)
    }
    const reset = () => {
        searchValue.value = ''
        getSellList()
    }
    const getSellList = () => {
        sellMedicalList
        ({
            storeId: currentStoreId.value,
            search: searchValue.value,
            currentPage: currentPage.value,
            pageSize: pageSize.value
        }).then((res) => {
            if (res.status === 200) {
                tableData.value = res.data.data
                total.value = res.data.total
            }
        })
    }
    const sellMedical = () => {
        sell.value.open()
    }
    onMounted(() => {
        getTree()
        getSellList()
    })
</script>


<template>
    <div class="container">
        <div class="medical-tree">
            <el-tree :data="treeData" :props="defaultProps" @node-click="handleNodeClick"/>
        </div>
        <div class="medical-table">
            <div class="search">
                <div class="search-form">
                    <div class="search-input">
                        <el-input v-model="searchValue" placeholder="请选择药品名称/类型/批号">
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
                <div class="sell-btn">
                    <el-button @click="sellMedical" type="danger">售出</el-button>
                </div>
            </div>
            <div class="user-table-head">
                <div class="user-table-title">
                    <div class="table-border"></div>
                    <div class="table-title">
                        销售记录
                    </div>
                </div>
            </div>
            <el-table :data="tableData" style="width: 100%" stripe border max-height="600px"
                      :header-cell-style="{
        'background': 'rgb(250,250,250)',
        'color':'black'
      }">
                <el-table-column prop="sell_id" label="销售单号" align="center"></el-table-column>
                <el-table-column prop="sell_medical_name" label="药品名称" align="center"></el-table-column>
                <el-table-column prop="sell_num" label="售出数量" align="center"></el-table-column>
                <el-table-column prop="receive_money" label="应收金额" align="center"></el-table-column>
                <el-table-column prop="sell_time" label="售出时间" align="center"></el-table-column>
                <el-table-column prop="count" label="药品现有数量" align="center"></el-table-column>
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
            <div class="user-table-head">
                <div class="user-table-title">
                    <div class="table-border"></div>
                    <div class="table-title">
                        需身份登记药品销售记录
                    </div>
                </div>
            </div>
            <div style="height: 550px">
                <el-table :data="tableData" style="width: 100%" stripe border max-height="600px"
                          :header-cell-style="{
        'background': 'rgb(250,250,250)',
        'color':'black'
      }">
                    <el-table-column prop="sell_id" label="销售单号" align="center"></el-table-column>
                    <el-table-column prop="sell_medical_name" label="药品名称" align="center"></el-table-column>
                    <el-table-column prop="sell_num" label="售出数量" align="center"></el-table-column>
                    <el-table-column prop="receive_money" label="应收金额" align="center"></el-table-column>
                    <el-table-column prop="sell_time" label="售出时间" align="center"></el-table-column>
                    <el-table-column prop="count" label="药品现有数量" align="center"></el-table-column>
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
        <sellInfo ref="sell"></sellInfo>
    </div>
</template>


<style lang="scss" scoped>
    .container {
        width: 100%;
        background-color: white;
        display: flex;
        height: auto;
        border: 1px solid #eaeaea;
        border-radius: 5px;

    }

    .user-table-head {
        display: flex;
        align-items: center;
        justify-content: space-between;
        margin-left: 5px;


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

    .medical-tree {
        width: 300px;
        box-shadow: 4px 5px 10px 0px #e8ebef;

    }

    .medical-table {
        width: 100%;

        .search {
            height: 70px;
            background-color: white;
            display: flex;
            align-items: center;
            justify-content: space-between;
            border: 1px solid #eaeaea;
            border-radius: 5px;

            .sell-btn {
                margin-right: 20px;
            }

            .search-form {
                display: flex;
                align-items: center;
            }

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

        .el-pagination {
            margin-top: 20px;
            margin-right: 20px
        }
    }


</style>