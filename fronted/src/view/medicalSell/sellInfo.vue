<script setup lang="ts">
    import {ref, onMounted, defineProps, reactive} from 'vue'
    import {useUserStore} from "../../store/user";
    import pinia from '../../plugins/pinia'

    const currentStoreId = ref(useUserStore(pinia).userInfo.store_id)
    const show = ref(false)
    //售出药品信息
    const rowInfo = ref(null)
    const open = (data: any) => {
        show.value = true
        rowInfo.value = data
    }
    const ruleForm = reactive({
        recordId: '',
        sellCount: 1,
        buyUserName:'',
        buyPhone:'',
        buyAddress:''
    })

    const IdCodeValid = (code) => {
        //身份证号合法性验证
        //支持15位和18位身份证号
        //支持地址编码、出生日期、校验位验证
        var city = {
            11: "北京",
            12: "天津",
            13: "河北",
            14: "山西",
            15: "内蒙古",
            21: "辽宁",
            22: "吉林",
            23: "黑龙江 ",
            31: "上海",
            32: "江苏",
            33: "浙江",
            34: "安徽",
            35: "福建",
            36: "江西",
            37: "山东",
            41: "河南",
            42: "湖北 ",
            43: "湖南",
            44: "广东",
            45: "广西",
            46: "海南",
            50: "重庆",
            51: "四川",
            52: "贵州",
            53: "云南",
            54: "西藏 ",
            61: "陕西",
            62: "甘肃",
            63: "青海",
            64: "宁夏",
            65: "新疆",
            71: "台湾",
            81: "香港",
            82: "澳门",
            91: "国外 "
        };
        var msg = '';
        if (!code || !/^\d{6}(18|19|20)?\d{2}(0[1-9]|1[012])(0[1-9]|[12]\d|3[01])\d{3}(\d|[xX])$/.test(code)) {
            msg = "身份证号格式错误";
        } else if (!city[code.substr(0, 2)]) {
            msg = "身份证号地址编码错误";
        } else {
            //18位身份证需要验证最后一位校验位
            if (code.length == 18) {
                code = code.split('');
                //∑(ai×Wi)(mod 11)
                //加权因子
                var factor = [7, 9, 10, 5, 8, 4, 2, 1, 6, 3, 7, 9, 10, 5, 8, 4, 2];
                //校验位
                var parity = [1, 0, 'X', 9, 8, 7, 6, 5, 4, 3, 2];
                var sum = 0;
                var ai = 0;
                var wi = 0;
                for (var i = 0; i < 17; i++) {
                    ai = code[i];
                    wi = factor[i];
                    sum += ai * wi;
                }
                if (parity[sum % 11] != code[17].toUpperCase()) {
                        msg = "身份证号校验位错误";
                }
            }
        }
        return msg;
    }
      const validatePhone = (rule: any, value: any, callback: any) => {
        if (value === '') {
            callback(new Error('请填写购买者联系方式'))
        } else {
            if (!(/^1[0123456789]\d{9}$/.test(ruleForm.buyPhone))) {
                callback(new Error("联系方式格式有误"))
            } else {
                callback()
            }
        }
    }
    const validateSellCount = (rule: any, value: any, callback: any) => {
        if (value < 1) {
            callback(new Error('售卖数量最低为1'))
        } else if (value > rowInfo.value.save_medical_count) {
            callback(new Error('售出数量不得超过库存数量'))
        } else {
            callback()
        }
    }
    const validateIdCard = (rule: any, value: any, callback: any) => {
        if (value === '') {
            callback(new Error('身份证信息不能为空'))
        } else {
            if (value !== '') {
                let error = IdCodeValid(value)
                if (error === '') {
                    callback()
                } else {
                    callback(new Error(error))
                }
            } else {
                callback()
            }

        }
    }
    const rules = reactive({
        sellCount: [
            {required: true, validator: validateSellCount, trigger: 'blur'},
        ],
        recordId: [
            {required: true, validator: validateIdCard, trigger: 'blur'},
        ],
         buyUserName:[
           {required: true, message: '请填写购买者姓名', trigger: 'blur'},
        ],
          buyPhone:[
           {required: true, validator: validatePhone, trigger: 'blur'},
        ],
         buyAddress:[
           {required: true, message: '请填写购买者居住地址', trigger: 'blur'},
        ],
    })

    const cancel = () => {
        show.value = false
    }

    defineExpose({
        open,
    })

</script>


<template>
    <el-dialog
            v-model="show"
            title="药品销售信息"
            width="50%"
            align-center
            @open="init"
            ref="dialogs"
            :show-close="false"
            :close-on-click-modal="false"
    >
        <div class="container">
            <el-form :model="ruleForm" ref="ruleFormRef" :rules="rules" label-width="120">
                <el-form-item label="药品名称:">
                    <span>{{rowInfo.medical_name}}</span>
                </el-form-item>
                <el-form-item label="药品售价:">
                    <span>￥{{rowInfo.medical_price}}</span>
                </el-form-item>
                <el-form-item label="售卖数量:" prop="sellCount">
                    <el-input v-model="ruleForm.sellCount" placeholder="请输入药品名称" type="number" min="1"></el-input>
                </el-form-item>
                <el-form-item label="购买者姓名:" prop="buyUserName" v-if="rowInfo.buy_isId===1">
                    <el-input v-model="ruleForm.buyUserName" placeholder="请登记购买者姓名"></el-input>
                </el-form-item>
                <el-form-item label="购买者身份登记:" prop="recordId" v-if="rowInfo.buy_isId===1">
                    <el-input v-model="ruleForm.recordId" placeholder="请登记购买者身份证信息"></el-input>
                </el-form-item>
                 <el-form-item label="购买者联系方式:" prop="buyPhone" v-if="rowInfo.buy_isId===1">
                    <el-input v-model="ruleForm.buyPhone" placeholder="请登记购买者联系方式"></el-input>
                </el-form-item>
                <el-form-item label="购买者居住地址:" prop="buyAddress" v-if="rowInfo.buy_isId===1">
                    <el-input v-model="ruleForm.buyAddress" placeholder="请登记购买者居住地址"></el-input>
                </el-form-item>
                <el-form-item>
                    <el-button @click="cancel">取消</el-button>
                    <el-button @click="confirm" type="primary">售出</el-button>
                </el-form-item>
            </el-form>
        </div>
    </el-dialog>
</template>


<style scoped>

</style>