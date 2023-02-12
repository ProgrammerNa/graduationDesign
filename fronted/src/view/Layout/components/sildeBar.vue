<script setup lang="ts">
    import pinia from '../../../plugins/pinia'
    import {storeToRefs} from 'pinia'
    import {useSystemStore} from "../../../store/system";
    const {roleMenuList} = storeToRefs(useSystemStore(pinia))
</script>
<template>
   <div class="sild-menu">
        <el-menu
            class="el-menu-vertical-demo"
            text-color="#8090A6"
            active-text-color=" #f3f6f8"
            unique-opened="true"
            collapse-transition="false"
            router
        >
            <template v-for="(item, index) of roleMenuList" :key="item.menu">
                <template v-if="item.children">
                    <el-sub-menu :index="item.path">
                        <template #title>
                            <span>{{ item.menu }}</span>
                        </template>
                        <template
                            v-for="(childItem, chileIndex) of item.childrenMenu"
                            :key="childItem.menu"
                        >
                            <el-menu-item :index="childItem.path">
                                <template #title>
                                    <span>{{ childItem.menu }}</span>
                                </template>
                            </el-menu-item>
                        </template>
                    </el-sub-menu>
                </template>
                <template v-if="!item.children">
                    <el-menu-item :index="item.path">
                        <template #title>
                            <span>{{ item.menu }}</span>
                        </template>
                    </el-menu-item>
                </template>
            </template>
        </el-menu>
   </div>
</template>
<style lang="scss" scoped>
.sild-menu {
    width: 100%;
    height: 100%;
    background: #ffffff;
    border: 1px solid #e6eaee;
}
.el-menu {
    .el-menu-item {
        background-color: #ffffff;
    }
    .el-menu-item {
        &.is-active,
        &:hover {
            background-color: #1d517e;
            color: #ffffff;
        }
    }
    .el-sub-menu {
        --el-menu-hover-bg-color: #f3f6f8;
        &.is-opened {
            background: #f3f6f8;
        }
    }
}
</style>
