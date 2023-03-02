<script setup lang="ts">
    import {ref, onMounted, defineProps, reactive} from 'vue'
    import {useUserStore} from "../../store/user";
    import pinia from '../../plugins/pinia'
    import {getMedicalTree} from "../../api/medical";
    import {selectCascader} from "../../utils/treeUtilr";

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
        ruleForm.medicalName= '';
        ruleForm.buyIdBool= '';
        ruleForm.medicalType= '';
        ruleForm.selectOption= [];
        ruleForm.eatMethods= '';
        ruleForm.eatMedicalCount= '';
        ruleForm.medicalInPrice='';
        ruleForm.medicalOutPrice= '';
        ruleForm.medicalDetail= '';
        ruleForm.count= 0
    }
    const confirm = () => {
        ruleFormRef.value.validate((valid: any) => {
            if (valid) {
            } else {
                console.log('验证出错')
            }
        })


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
                    <el-input v-model="ruleForm.username" placeholder="请输入药品名称"></el-input>
                </el-form-item>
                <el-form-item label="药品类型" prop="medicalType">
                    <el-cascader :options="selectCascader( ruleForm.selectOption)"
                                 :show-all-levels="false"></el-cascader>
                </el-form-item>
                <el-form-item label="服用方式" prop="eatMethods">
                    <el-input v-model="ruleForm.eatMethods" placeholder="请填写服用方式"></el-input>
                </el-form-item>
                <el-form-item label="服用剂量" prop="eatMedicalCount">
                    <el-input v-model="ruleForm.eatMedicalCount" placeholder="请填写服用剂量"></el-input>
                </el-form-item>
                <el-form-item label="药品进价" prop="medicalInPrice">
                    <el-input v-model="ruleForm.medicalInPrice"></el-input>
                </el-form-item>
                <el-form-item label="药品售价" prop="medicalOutPrice">
                    <el-input v-model="ruleForm.medicalOutPrice"></el-input>
                </el-form-item>
                <el-form-item label="入库数量" prop="count">
                    <el-input v-model="ruleForm.count" type="number" min="0"></el-input>
                </el-form-item>
                <el-form-item label="顾客购买是否需登记" prop="sex">
                    <el-radio-group v-model="ruleForm.buyIdBool" class="ml-4" @change="change">
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