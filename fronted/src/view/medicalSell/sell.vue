<script setup lang="ts">
    import {onMounted, ref} from "vue";
    import {getMedicalTree} from "../../api/medical";
    import {tree} from "../../utils/treeUtilr";
    const searchValue = ref('')
    const treeData = ref([])
    const tableData = ref([
        {id:1}
    ])
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
    const handleNodeClick = (data:any) => {
        searchValue.value = data.type_name
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
                <el-table-column prop="staffId" label="药品编号" align="center"></el-table-column>
                <el-table-column prop="staffName" label="药品名称" align="center"></el-table-column>
                <el-table-column prop="staffName" label="药品类型" align="center"></el-table-column>
                <el-table-column prop="username" label="服用方式" align="center"></el-table-column>
                <el-table-column prop="username" label="服用剂量" align="center"></el-table-column>
                <el-table-column prop="staffPhone" label="药品备注" align="center"></el-table-column>
                <el-table-column prop="status" label="药品售价(元)" align="center"></el-table-column>
                <el-table-column prop="ruzhiTime" label="药品库存数量" align="center"></el-table-column>
                <el-table-column prop="option" label="操作" align="center" width="200">
                    <template #default="scope">
                        <el-button>售出</el-button>
                        <el-button>身份登记</el-button>
                    </template>
                </el-table-column>
            </el-table>
        </div>
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
        }


    }


</style>