<script setup lang="ts">
    import {ref, onMounted, defineProps, reactive} from 'vue'
    import {useUserStore} from "../../store/user";
    import pinia from '../../plugins/pinia'
    import {getMedicalTree} from "../../api/medical";
    import {selectCascader} from "../../utils/treeUtilr";
    import {addMedicalSave} from "../../api/medical";
    import {formateTime} from "../../utils/timeUtils";

    const props = defineProps({
        getMedicalList: {
            type: Function,
            default: () => {
            }
        }
    })
    const currentStoreId = ref(useUserStore(pinia).userInfo.store_id)
    const currentRoleId = ref(useUserStore(pinia).userInfo.role_id)
    const show = ref(false)
    const ruleForm = ref({
        medicalName: '',
        drugBarcode: '',
        medicalType: '',
        selectOption: [],
        medicalInPrice: '',
        medicalOutPrice: '',
        count: 0,
        saveMedicalNum: '',
        time: '',
        medicalStandards: '',
        medicalSupply: ''

    })
    //点击详情该行的用户id
    const open = () => {
        show.value = true
    }
    const ruleFormRef = ref()
    const cancel =() => {
        show.value = false
        ruleFormRef.value.resetFields()
    }
    const tableData = ref([])
    const validateMedicalOutPrice = (rule: any, value: any, callback: any) => {
        if (value <= 0 || isNaN(value)) {
            callback(new Error('药品售价大于0且必须为数字'))
        } else {
            callback()

        }
    }
    const validateMedicalInPrice = (rule: any, value: any, callback: any) => {
        if (value <= 0 || isNaN(value)) {
            callback(new Error('药品进价大于0且必须为数字'))
        } else {
            callback()

        }
    }
    const validateCount = (rule: any, value: any, callback: any) => {
        if (value <= 0) {
            callback(new Error('入库药品数量需要大于0'))
        } else {
            callback()

        }
    }
    const rules = reactive({
        saveMedicalNum: [
            {required: true, message: '入库单号不能为空', trigger: 'blur'},
        ],
        medicalStandards: [
            {required: true, message: '药品规格不能为空', trigger: 'blur'},
        ],
        medicalType: [
            {required: true, message: '药品类型不能为空', trigger: 'blur'},
        ],
        drugBarcode: [
            {required: true, message: '药品编码不能为空', trigger: 'blur'},
        ],
        medicalName: [
            {required: true, message: '药品名称不能为空', trigger: 'blur'},
        ],
        medicalSupply: [
            {required: true, message: '供应商家不能为空', trigger: 'blur'},
        ],
        time: [
            {required: true, message: '有效日期不能为空', trigger: 'blur'},
        ],
        count: [
            {required: true, validator: validateCount, trigger: 'blur'},
        ],
        medicalInPrice: [
            {required: true, validator: validateMedicalInPrice, trigger: 'blur'},
        ],
        medicalOutPrice: [
            {required: true, validator: validateMedicalOutPrice, trigger: 'blur'},
        ],

    })
    //添加新增入库表格记录
    const add = () => {
        ruleFormRef.value.validate((valid) => {
            if (valid) {
                //进行深拷贝，防止改变数据
                const data = JSON.parse(JSON.stringify(ruleForm.value))
                tableData.value.push(data)
            } else {
                console.log('error submit!')
            }
        })
    }
    //删除新增入库表格记录
    const remove = (data: any) => {
        tableData.value.splice(data, 1)
    }
    const getMedicalTreeList = () => {
        getMedicalTree().then((res) => {
            if (res.status === 200) {
                res.data.forEach((val) => {
                    ruleForm.value.selectOption.push({
                        value: val.id,
                        label: val.type_name,
                        parent_id: val.parent_id
                    })
                })
                console.log(ruleForm.value.selectOption)
            }
        })
    }
    const changeMedicalType = (data: any) => {
        ruleForm.value.medicalType = data[data.length - 1]
    }
    const init = () => {
        ruleForm.value.selectOption = []
        getMedicalTreeList()
        tableData.value = []
    }

    defineExpose({
        open,
    })

</script>


<template>
    <el-dialog
            v-model="show"
            title="新增入库"
            width="60%"
            @open="init"
            ref="dialogs"
            :show-close="false"
            :close-on-click-modal="false"
    >
        <div class="container">
            <el-form ref="ruleFormRef"
                     :model="ruleForm"
                     :rules="rules">
                <div class="form-content">
                    <div class="content">
                        <el-form-item label="库存单号:" prop="saveMedicalNum">
                            <el-input placeholder="请填写入库单号" v-model="ruleForm.saveMedicalNum"></el-input>
                        </el-form-item>
                        <el-form-item label="药品名称:" prop="medicalName">
                            <el-input placeholder="请填写药品名称" v-model="ruleForm.medicalName"></el-input>
                        </el-form-item>
                        <el-form-item label="药品编号:" prop="drugBarcode">
                            <el-input placeholder="请填写药品编号" v-model="ruleForm.drugBarcode"></el-input>
                        </el-form-item>
                        <el-form-item label="药品类型:" prop="medicalType">
                            <el-cascader :options="selectCascader( ruleForm.selectOption)"
                                         :show-all-levels="false" clearable @change="changeMedicalType"
                                         style="margin-left: 5px;width:190px"></el-cascader>
                        </el-form-item>
                    </div>
                    <div class="content">
                        <el-form-item label="药品进价:" prop="medicalInPrice">
                            <el-input placeholder="请填写药品进价" v-model="ruleForm.medicalInPrice"></el-input>
                        </el-form-item>
                        <el-form-item label="药品售价:" prop="medicalOutPrice">
                            <el-input placeholder="请填写药品进价" v-model="ruleForm.medicalOutPrice"></el-input>
                        </el-form-item>
                        <el-form-item label="药品规格:" prop="medicalStandards">
                            <el-input placeholder="请填写药品规格" v-model="ruleForm.medicalStandards"></el-input>
                        </el-form-item>
                        <el-form-item label="供应商家:" prop="medicalSupply">
                            <el-input placeholder="请填写供应商" v-model="ruleForm.medicalSupply"></el-input>
                        </el-form-item>
                    </div>
                    <div class="content">
                        <el-form-item label="入库数量:" prop="count">
                            <el-input placeholder="请填写入库数量" v-model="ruleForm.count"></el-input>
                        </el-form-item>
                        <el-form-item label="有效日期:" prop="time">
                            <el-date-picker
                                    v-model="ruleForm.time"
                                    type="daterange"
                                    range-separator="至"
                                    start-placeholder="生产时间"
                                    end-placeholder="过期时间"
                                    style="width: 580px;margin-left: 5px"
                            />
                        </el-form-item>
                        <el-form-item>
                            <el-button @click="add" type="primary">添加</el-button>
                            <el-button @click="reset">重置</el-button>
                        </el-form-item>

                    </div>
                </div>
            </el-form>
        </div>
        <el-divider/>
        <div class="table">
            <el-table :data="tableData" style="width: 100%" stripe :max-height="400">
                <el-table-column prop="saveMedicalNum" label="库存单号"/>
                <el-table-column prop="drugBarcode" label="药品编号"/>
                <el-table-column prop="medicalName" label="药品名称"/>
                <el-table-column prop="medicalType" label="药品类型"/>
                <el-table-column prop="medicalStandards" label="药品规格"/>
                <el-table-column prop="medicalInPrice" label="药品进价(元)"/>
                <el-table-column prop="medicalOutPrice" label="药品售价(元)"/>
                <el-table-column prop="count" label="入库数量"/>
                <el-table-column prop="medicalSupply" label="供应商家"/>
                <el-table-column prop="time" label="有效日期" width="200">
                    <template #default="scope">
                        <div>{{formateTime(scope.row.time.join('-').split('-')[0])}}至
                            {{formateTime(scope.row.time.join('-').split('-')[1])}}
                        </div>
                    </template>
                </el-table-column>
                <el-table-column prop="option" label="操作">
                    <template #default="scope">
                        <el-button type="danger" @click="remove(scope.$index)">删除</el-button>
                    </template>
                </el-table-column>
            </el-table>
        </div>
        <div class="option-btn">
             <el-button @click="cancel">取消</el-button>
            <el-button @click="save" type="primary">入库</el-button>
        </div>
    </el-dialog>
</template>


<style lang="scss" scoped>
    .form-content {
        display: flex;
        flex-direction: column;
        justify-content: center;

        .content {
            display: flex;
            align-items: center;
            margin-top: 5px;
            justify-content: space-between;

            .input-content {
                display: flex;
                align-items: center;


                .el-button {
                    margin-left: 10px;
                }
            }
        }
    }
    .option-btn{
        display: flex;
        align-items: center;
        justify-content: space-around;
        margin-top: 10px;
        .el-button{
            margin-left: 15px;
        }
    }
</style>