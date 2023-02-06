<script setup lang="ts">
    import headerVue from './components/header.vue'
    import sildeBarVue from './components/sildeBar.vue'
import { RouterView } from 'vue-router';
</script>
<template>
    <div class="container">
        <el-container>
            <el-header class="layout-head">
                <headerVue></headerVue>
            </el-header>
            <el-container>
                <el-aside class="layout-aside">
                    <sildeBarVue></sildeBarVue>
                </el-aside>
                <el-container class="layout-container">
                    <el-main class="layout-main">
                        <RouterView></RouterView>
                    </el-main>
                </el-container>
            </el-container>
        </el-container>
    </div>
</template>
<style lang="scss" scoped>
.container {
    height: 100%;
    .layout-head {
        padding: 0;
    }
    .layout-aside {
        width: 240px;
        overflow: hidden;
        background: #eef2f5;
        margin-top: 1px;
    }
    .el-main {
        background-color: #eef2f5;
        overflow-x: hidden;
    }
    .layout-main {
        background-color: #eef2f5;
        overflow-y: auto;
        height: calc(100vh - 122px);
    }
}
</style>
