<script setup lang="ts">
    import {onMounted, ref} from "vue";
    import {getMedicalTree} from "../../api/medical";
    import {tree} from "../../utils/treeUtilr";
    import addSave from "./addSave.vue"
    import {getMedicalInSaveList} from "../../api/medical";
    import {useUserStore} from "../../store/user";
    import pinia from '../../plugins/pinia'
    import {formateTime} from "../../utils/timeUtils";

    const searchValue = ref('')
    const loading = ref(true)
    const treeData = ref([])
    const currentStoreId = ref(useUserStore(pinia).userInfo.store_id)
    const currentPage = ref(1)
    const pageSize = ref(10)
    const tableData = ref([])
    const total = ref(0)
    const defaultProps = {
        children: 'children',
        label: 'type_name',
    }
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
        getMedicalInSaveList({
            storeId: currentStoreId.value,
            currentPage: currentPage.value,
            pageSize: pageSize.value,
            search: searchValue.value
        }).then((res) => {
            if (res.status === 200) {
                tableData.value = res.data.data
                total.value = res.data.total
                setTimeout(() => {
                    loading.value = false
                },2000)
            }else{
                loading.value = false
            }
        }).catch(err => {
            console.log(err)
            loading.value=false
        })
    }
    const getTree = () => {
        getMedicalTree().then(res => {
            if (res.status === 200) {
                treeData.value = tree(res.data)
            }
        })
    }
    const handleNodeClick = (data: any) => {
        searchValue.value = data.type_name
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
    const addMedical = () => {
        add.value.open()
    }
    onMounted(() => {
        getTree()
        getList()
    })
</script>


<template>
    <div class="container">
        <div class="medical-tree">
            <el-tree :data="treeData" :props="defaultProps" @node-click="handleNodeClick"/>
        </div>
        <div class="medical-table">
            <div class="search">
                <div class="search-box">
                    <div class="search-input">
                        <el-input v-model="searchValue" placeholder="?????????????????????/??????">
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
                <div class="add-btn">
                    <el-button type="danger" @click="addMedical">????????????</el-button>
                </div>
            </div>
            <el-table
                    v-loading="loading"
                    :data="tableData" style="width: 100%" stripe border max-height="600px"
                      :header-cell-style="{
        'background': 'rgb(250,250,250)',
        'color':'black'
      }">
                <el-table-column prop="save_medical_num" label="????????????" align="center"></el-table-column>
                <el-table-column prop="medical_name" label="????????????" align="center"></el-table-column>
                <el-table-column prop="drug_barcode" label="????????????" align="center"></el-table-column>
                <el-table-column prop="type_name" label="????????????" align="center"></el-table-column>
                <el-table-column prop="medical_standards" label="????????????" align="center"></el-table-column>
                <el-table-column prop="save_time" label="????????????" align="center" width="110">
                    <template #default="scope">
                        <div>{{formateTime(scope.row.save_time)}}</div>
                    </template>
                </el-table-column>
                <el-table-column prop="save_price" label="????????????(???)" align="center"></el-table-column>
                <el-table-column prop="medical_price" label="????????????(???)" align="center"></el-table-column>
                <el-table-column prop="count" label="????????????" align="center"></el-table-column>
                <el-table-column prop="medical_supply" label="????????????" align="center"></el-table-column>
                 <el-table-column prop="producat_time" label="????????????" align="center" width="110">
                      <template #default="scope">
                       <div>{{formateTime(scope.row.producat_time)}}</div>
                    </template>
                 </el-table-column>
                <el-table-column prop="medical_out_time" label="????????????" align="center" width="110">
                      <template #default="scope">
                       <div>{{formateTime(scope.row.medical_out_time)}}</div>
                    </template>
                </el-table-column>
                <el-table-column prop="option" label="??????" align="center" width="250">
                    <template #default="scope">
                        <el-button>????????????</el-button>
                        <el-button>????????????</el-button>
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
        <addSave ref="add" :getMedicalList="getList"></addSave>
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
            width: 200px;
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

                .add-btn {
                    margin-right: 20px;
                }

                .search-box {
                    display: flex;

                    .search-input {
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
            }
             .el-pagination {
                margin-top: 20px;
                margin-right: 20px
            }

        }
    }


</style>