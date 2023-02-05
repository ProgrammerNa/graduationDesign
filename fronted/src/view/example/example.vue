<script setup lang="ts">
import {getTest ,postData,getData,add,addMore,getData1} from '../../api/testApi'
const test = () => {
    getTest().then((res) => {
        console.log(res)
    })
}
const test1 = () => {
    postData({
        "id":3,
        "name":"fghghjhhg"
    }).then(res => {
        console.log(res)
    })
}
const test2 = () => {
    getData().then((res) => {
        console.log(res)
    })
}
const addTest = () => {
    add({
        name:'test'
    }).then((res) => {
        console.log(res)
    })
}
const addMoreTest = () => {
    addMore([
        {
            name:'aaaa'
        },
        {
            name:'bbb'
        }
        ]).then((res) => {
            console.log(res)
    })
}
const get = () => {
    getData1({
        id:3
    }).then((res) => {
        console.log(res)
    })
}
</script>
<template>
    <el-button @click="test">测试</el-button>
    <el-button @click="test1">post</el-button>
    <el-button @click="test2">getData</el-button>
    <el-button @click="addTest">add</el-button>
    <el-button @click="addMoreTest">addMore</el-button>
    <el-button @click="get">获取指定数据</el-button>
</template>


<style scoped>

</style>