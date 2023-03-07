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
    console.log(props.getMedicalList)
    const currentStoreId = ref(useUserStore(pinia).userInfo.store_id)
    const show = ref(false)
    const ruleForm = reactive({
        medicalName: '',
        buyIdBool: '',
        medicalType: '',
        selectOption: [],
        eatMethods: '',
        eatMedicalCount: '',
        medicalInPrice: '',
        medicalOutPrice: '',
        medicalDetail: '',
        count: 0

    })
    //点击详情该行的用户id
    const open = () => {
        show.value = true
    }
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
        medicalName:[
           {required: true, message: '请填入药品名称', trigger: 'blur'},
        ],
        eatMethods:[
           {required: true, message: '请填写服用方式', trigger: 'blur'},
        ],
        eatMedicalCount:[
           {required: true, message: '请填写服用剂量', trigger: 'blur'},
        ],
        count:[
           {required: true,  validator: validateCount, trigger: 'blur'},
        ],
        medicalInPrice:[
           {required: true,  validator: validateMedicalInPrice, trigger: 'blur'},
        ],
        medicalOutPrice:[
           {required: true,  validator: validateMedicalOutPrice, trigger: 'blur'},
        ],
        buyIdBool:[
           {required: true,  message: '请选择购买限制', trigger: 'blur'},
        ],
        medicalType:[
           {required: true,  message: '请选择药品类型', trigger: 'blur'},
        ],

    })
    const getMedicalTreeList = () => {
        getMedicalTree().then((res) => {
            if (res.status === 200) {
                res.data.forEach((val) => {
                    ruleForm.selectOption.push({
                        value: val.id,
                        label: val.type_name,
                        parent_id: val.parent_id
                    })
                })
                console.log(ruleForm.selectOption)
            }
        })
    }
    const ruleFormRef = ref()
    const cancel = () => {
        show.value = false
        ruleForm.medicalName = '';
        ruleForm.medicalName = '';
        ruleForm.buyIdBool = '';
        ruleForm.medicalType = '';
        ruleForm.selectOption = [];
        ruleForm.eatMethods = '';
        ruleForm.eatMedicalCount = '';
        ruleForm.medicalInPrice = '';
        ruleForm.medicalOutPrice = '';
        ruleForm.medicalDetail = '';
        ruleForm.count = 0
    }
    const confirm = () => {
        ruleFormRef.value.validate((valid: any) => {
            if (valid) {
                addMedicalSave({
                    medicalName: ruleForm.medicalName,
                    medicalType: parseInt(ruleForm.medicalType),
                    medicalOutPrice: parseFloat(ruleForm.medicalOutPrice),
                    storeId: currentStoreId.value,
                    eatMethods: ruleForm.eatMethods,
                    eatMedicalCount: ruleForm.eatMedicalCount,
                    buyIdBool: ruleForm.buyIdBool,
                    time: formateTime(new Date()),
                    count: ruleForm.count,
                    medicalInPrice: parseFloat(ruleForm.medicalOutPrice),
                    medicalDetail: ruleForm.medicalDetail
                }).then((res) => {
                    if (res.status === 200) {
                        // @ts-ignore
                        ElMessage({
                            message: '入库成功',
                            type: 'success',
                        })
                        props.getMedicalList()
                        cancel()
                    }else{
                         // @ts-ignore
                        ElMessage({
                            message: '入库失败',
                            type: 'error',
                        })
                    }
                }).catch(err => {
                     // @ts-ignore
                        ElMessage({
                            message: '网络异常',
                            type: 'error',
                        })
                })
            } else {
                console.log('验证出错')
            }
        })


    }
    const changeMedicalType = (data: any) => {
        ruleForm.medicalType = data[data.length - 1]
    }
    const changeBuyIdBool = (data: any) => {
        ruleForm.buyIdBool = data
    }
    const init = () => {
        ruleForm.selectOption = []
        getMedicalTreeList()
    }

    defineExpose({
        open,
    })

</script>


<template>
    <el-dialog
            v-model="show"
            title="新增入库"
            width="50%"
            align-center
            @open="init"
            ref="dialogs"
            :show-close="false"
            :close-on-click-modal="false"
    >
        <div class="container">
            <el-form :model="ruleForm" ref="ruleFormRef" :rules="rules" label-width="120">
                <el-form-item label="药品名称" prop="medicalName">
                    <el-input v-model="ruleForm.medicalName" placeholder="请输入药品名称"></el-input>
                </el-form-item>
                <el-form-item label="药品类型" prop="medicalType">
                    <el-cascader :options="selectCascader( ruleForm.selectOption)"
                                 :show-all-levels="false" clearable @change="changeMedicalType"></el-cascader>
                </el-form-item>
                <el-form-item label="服用方式" prop="eatMethods">
                    <el-input v-model="ruleForm.eatMethods" placeholder="请填写服用方式"></el-input>
                </el-form-item>
                <el-form-item label="用法用量" prop="eatMedicalCount">
                    <el-input v-model="ruleForm.eatMedicalCount" placeholder="请填写服用剂量"></el-input>
                </el-form-item>
                <el-form-item label="药品进价(元)" prop="medicalInPrice">
                    <el-input v-model="ruleForm.medicalInPrice"></el-input>
                </el-form-item>
                <el-form-item label="药品售价(元)" prop="medicalOutPrice">
                    <el-input v-model="ruleForm.medicalOutPrice"></el-input>
                </el-form-item>
                <el-form-item label="入库数量(盒)" prop="count">
                    <el-input v-model="ruleForm.count" type="number" min="0"></el-input>
                </el-form-item>
                <el-form-item label="顾客购买是否需登记" prop="buyIdBool">
                    <el-radio-group v-model="ruleForm.buyIdBool" class="ml-4" @change="changeBuyIdBool">
                        <el-radio label="1" size="large">是</el-radio>
                        <el-radio label="0" size="large">否</el-radio>
                    </el-radio-group>
                </el-form-item>
                <el-form-item label="药品备注" prop="medicalDetail">
                    <el-input v-model="ruleForm.medicalDetail" type="textarea"></el-input>
                </el-form-item>
                <el-form-item>
                    <el-button @click="cancel">取消</el-button>
                    <el-button @click="confirm" type="primary">入库</el-button>
                </el-form-item>
            </el-form>
        </div>
    </el-dialog>
</template>


<style scoped>

</style>