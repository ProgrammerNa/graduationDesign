<script setup lang="ts">
import { RouterView } from 'vue-router';
import zhCn from 'element-plus/lib/locale/lang/zh-cn';
</script>

<template>
  <!-- 表格分页汉化处理 -->
    <el-config-provider :locale="zhCn">
        <router-view></router-view>
    </el-config-provider>
</template>

<style lang="scss" scoped>
    html,body,#app{
  height: 100%;
}
</style>
