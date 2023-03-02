<script setup lang="ts">
    import {onMounted, ref} from "vue";
    import {getMedicalTree} from "../../api/medical";
    import {tree} from "../../utils/treeUtilr";
    import addSave from "./addSave.vue"

    const searchValue = ref('')
    const treeData = ref([])
    const defaultProps = {
        children: 'children',
        label: 'type_name',
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
    const add = ref()
    const addMedical = () => {
        add.value.open()
    }
    onMounted(() => {
        getTree()
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
                <div class="add-btn">
                    <el-button type="danger" @click="addMedical">新增入库</el-button>
                </div>
            </div>
            <el-table :data="tableData" style="width: 100%" stripe border max-height="600px"
                      :header-cell-style="{
        'background': 'rgb(250,250,250)',
        'color':'black'
      }">
                <el-table-column prop="staffId" label="库存编号" align="center"></el-table-column>
                <el-table-column prop="staffName" label="药品名称" align="center"></el-table-column>
                <el-table-column prop="staffName" label="药品类型" align="center"></el-table-column>
                <el-table-column prop="username" label="服用方式" align="center"></el-table-column>
                <el-table-column prop="username" label="服用剂量" align="center"></el-table-column>
                <el-table-column prop="staffPhone" label="药品备注" align="center"></el-table-column>
                <el-table-column prop="staffPhone" label="入库时间" align="center"></el-table-column>
                <el-table-column prop="status" label="药品进价(元)" align="center"></el-table-column>
                 <el-table-column prop="status" label="药品售价(元)" align="center"></el-table-column>
                 <el-table-column prop="status" label="购买是否需要身份登记" align="center"></el-table-column>
                <el-table-column prop="ruzhiTime" label="药品库存数量" align="center"></el-table-column>
                <el-table-column prop="option" label="操作" align="center" width="250">
                    <template #default="scope">
                        <el-button>药品出库</el-button>
                        <el-button>库存盘点</el-button>
                    </template>
                </el-table-column>
            </el-table>
        </div>
        <addSave ref="add"></addSave>
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

        }
    }


</style>