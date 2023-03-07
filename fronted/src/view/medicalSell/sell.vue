<script setup lang="ts">
    import {onMounted, ref} from "vue";
    import {getMedicalTree} from "../../api/medical";
    import {tree} from "../../utils/treeUtilr";
    import {sellMedicalList} from '../../api/medical'
    import {useUserStore} from "../../store/user";
    import pinia from '../../plugins/pinia'
    import sellInfo from './sellInfo.vue'

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
        sellMedicalList({
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
    const sellMedical = (data: any) => {
        sell.value.open(data)
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
                <div class="search-input">
                    <el-input v-model="searchValue" placeholder="请选择药品名称/类型">
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
            <el-table :data="tableData" style="width: 100%" stripe border max-height="600px"
                      :header-cell-style="{
        'background': 'rgb(250,250,250)',
        'color':'black'
      }">
                <el-table-column prop="medical_name" label="药品名称" align="center"></el-table-column>
                <el-table-column prop="type_name" label="药品类型" align="center"></el-table-column>
                <el-table-column prop="medical_use_methods" label="服用方式" align="center"></el-table-column>
                <el-table-column prop="medical_use_num" label="用法用量" align="center"></el-table-column>
                <el-table-column prop="details" label="药品备注" align="center"></el-table-column>
                <el-table-column prop="medical_price" label="药品售价(元)" align="center"></el-table-column>
                <el-table-column prop="save_medical_count" label="药品库存数量" align="center"></el-table-column>
                <el-table-column prop="buy_isId" label="购买是否需要登记" align="center">
                    <template #default="scope">
                        <div v-if="scope.row.buy_isId === 0">否</div>
                        <div v-if="scope.row.buy_isId === 1">是</div>
                    </template>
                </el-table-column>
                <el-table-column prop="option" label="操作" align="center" width="200">
                    <template #default="scope">
                        <el-button @click="sellMedical(scope.row)">售出</el-button>
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
        <sellInfo ref="sell"></sellInfo>
    </div>
</template>


<style lang="scss" scoped>
    .container {
        display: flex;
        background-color: white;
        min-height: calc(100vh - 250px);
        border: 1px solid #eaeaea;
        border-radius: 5px;

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

            .el-pagination {
                margin-top: 20px;
                margin-right: 20px
            }
        }


    }


</style>