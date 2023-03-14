<script setup lang="ts">
    import {ref, onMounted, defineProps, reactive, computed} from 'vue'
    import {useUserStore} from "../../store/user";
    import pinia from '../../plugins/pinia'
    import {getMedicalInfoByDrugBarcode} from "../../api/medical";

    const currentStoreId = ref(useUserStore(pinia).userInfo.store_id)
    const show = ref(false)
    const open = () => {
        show.value = true
    }
    const ruleForm = ref({
        searchValue: ''
    })
    const ruleSellForm = ref({
        sellCount: null,
        buyUserName: '',
        recordId: '',
        buyPhone: '',
        buyAddress: ''
    })
    // 确认售出弹窗
    const dialogVisible = ref(false)
    const sellTableData = ref([])
    const sellMedicalData = ref(null)
    const searchTableData = ref([])
    const getSearchList = () => {
        getMedicalInfoByDrugBarcode({
            storeId: currentStoreId.value,
            search: ruleForm.value.searchValue,
        }).then((res) => {
            if (res.status === 200) {
                searchTableData.value = res.data
                console.log(res)
            }
        })
    }
    const sellSearch = () => {
        getSearchList()
    }
    const cancel = () => {
        show.value = false
    }
    const confirmSell = (data: any) => {
        sellMedicalData.value = data
        dialogVisible.value = true
    }
    const totalMoney = computed (() => {
        let total =0 ;
        sellTableData.value.forEach((val) => {
            total = total+val.reveive_money
        })
        return total
    });
    const confirmMedical = () => {
        dialogVisible.value = false
        sellTableData.value.push({
            sellCount:ruleSellForm.value.sellCount,
            buyUserName:ruleSellForm.value.buyUserName,
            buyPhone:ruleSellForm.value.buyPhone,
            buyAddress:ruleSellForm.value.buyAddress,
            medical_name:sellMedicalData.value.medical_name,
            medical_price:sellMedicalData.value.medical_price,
            reveive_money:sellMedicalData.value.medical_price*ruleSellForm.value.sellCount,
            recordId:ruleSellForm.value.recordId
        })
        console.log(sellTableData.value)
    }
    const remove = (data:any) => {
        sellTableData.value.splice(data,1)
    }
    const settleAccounts = () => {
        if(sellTableData.value.length<=0){
             // @ts-ignore
                ElMessage({
                    message: '没有可结算的数据',
                    type: 'error',
                })
        } else{

        }
    }

    defineExpose({
        open,
    })

</script>


<template>
    <el-dialog
            v-model="show"
            title="药品销售"
            width="60%"
            @open="init"
            ref="dialogs"
            :close-on-click-modal="false"
    >
        <div class="container">

            <el-form ref="ruleFormRef"
                     :model="ruleForm"
                     :rules="rules"
            >
                <div style="display: flex">
                    <el-form-item label="批号/药品名称">
                        <el-input placeholder="请输入药品批号进行查询" v-model="ruleForm.searchValue"></el-input>
                    </el-form-item>
                    <el-form-item>
                        <el-button @click="sellSearch">查询</el-button>
                    </el-form-item>
                </div>
            </el-form>
            <div class="search-table">
                <div class="user-table-head">
                <div class="user-table-title">
                    <div class="table-border"></div>
                    <div class="table-title">
                        查询结果列表
                    </div>
                </div>
            </div>
                <el-table :data="searchTableData" stripe style="width: 100%">
                    <el-table-column prop="drug_barcode" label="药品批号"/>
                    <el-table-column prop="medical_name" label="药品名称"/>
                    <el-table-column prop="medical_standards" label="药品规格"/>
                    <el-table-column prop="count" label="药品数量"/>
                    <el-table-column prop="medical_price" label="药品售价"/>
                    <el-table-column prop="record" label="购买是否需要登记">
                        <template #default="scope">
                            <div v-if="scope.row.record">是</div>
                            <div v-else>否</div>
                        </template>
                    </el-table-column>
                    <el-table-column prop="option" label="操作">
                        <template #default="scope">
                            <el-button type="danger" @click="confirmSell(scope.row)">确认售出</el-button>
                        </template>
                    </el-table-column>
                </el-table>
                <el-dialog
                        v-model="dialogVisible"
                        title="确认售出"
                        width="40%"
                >
                    <div>
                        <el-form ref="ruleFormRef"
                                 :model="ruleSellForm"
                                 :rules="ruleSell"
                        >
                            <el-form-item label="售出数量">
                                <el-input placeholder="请输入药品售出数量" v-model="ruleSellForm.sellCount" type="number" min="1"></el-input>
                            </el-form-item>
                            <div v-if="sellMedicalData.record === 1">
                                <el-form-item label="购买者姓名:" prop="buyUserName">
                                    <el-input v-model="ruleSellForm.buyUserName" placeholder="请登记购买者姓名"></el-input>
                                </el-form-item>
                                <el-form-item label="购买者身份登记:" prop="recordId">
                                    <el-input v-model="ruleSellForm.recordId" placeholder="请登记购买者身份证信息"></el-input>
                                </el-form-item>
                                <el-form-item label="购买者联系方式:" prop="buyPhone">
                                    <el-input v-model="ruleSellForm.buyPhone" placeholder="请登记购买者联系方式"></el-input>
                                </el-form-item>
                                <el-form-item label="购买者居住地址:" prop="buyAddress">
                                    <el-input v-model="ruleSellForm.buyAddress" placeholder="请登记购买者居住地址"></el-input>
                                </el-form-item>
                            </div>
                            <el-form-item>
                               <el-button @click="confirmMedical">确认</el-button>
                                 <el-button @click="cancelMedical">取消</el-button>
                            </el-form-item>
                        </el-form>
                    </div>
                </el-dialog>
            </div>
            <div class="search-table">
                <div class="user-table-head">
                <div class="user-table-title">
                    <div class="table-border"></div>
                    <div class="table-title">
                        待结算列表
                    </div>
                </div>
            </div>
                <el-table :data="sellTableData" stripe style="width: 100%" :max-height="400">
                    <el-table-column prop="medical_name" label="药品名称" />
                    <el-table-column prop="medical_price" label="药品单价"/>
                    <el-table-column prop="sellCount" label="售出总数"/>
                    <el-table-column prop="reveive_money" label="金额"/>
                    <el-table-column prop="buyUserName" label="购买者姓名"/>
                    <el-table-column prop="buyPhone" label="购买者联系方式"/>
                    <el-table-column prop="recordId" label="购买者身份证号码"/>
                    <el-table-column prop="buyAddress" label="购买者居住地址"/>
                     <el-table-column prop="option" label="操作">
                          <template #default="scope">
                            <el-button type="primary" @click="remove(scope.$index)">删除</el-button>
                        </template>
                     </el-table-column>

                </el-table>
            </div>
            <div style="display: flex; justify-content: flex-end;margin-top: 10px">
                <el-button type="danger" @click="settleAccounts">结算({{totalMoney}})</el-button>
            </div>
        </div>

    </el-dialog>

</template>


<style lang="scss" scoped>
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
                height: 15px;
                margin-left: 10px;
                margin-right: 5px;
            }

            .table-title {
                height: 50px;
                margin-left: 5px;
                font-size: 15px;
                line-height: 50px;
            }

        }

    }

</style>