import { ref } from 'vue';
import { defineStore } from 'pinia';
import * as piniaStorage from '../utils/piniaStorage';

export const useSystemStore = defineStore('system', () => {

    // 调用 piniaStorage中的getRoleMenuList方法，获取角色菜单列表
    const roleMenuList = ref<any>(piniaStorage.getRoleMenuList() || []);

    const setRoleMenuList = (list: any[]) => {
        //  login.vue中调用了该方法，该方法接收到了roleMenuList
        piniaStorage.setRoleMenuList(list); //调用piniaStroage 设置角色菜单列表
        roleMenuList.value = list;
    };
    return {
        roleMenuList,
        setRoleMenuList,
    };
});
