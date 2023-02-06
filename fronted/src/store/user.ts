import { ref } from 'vue';
import { defineStore } from 'pinia';
import * as piniaStorage from '../utils/piniaStorage';

export const useUserStore = defineStore('user', () => {
    const userInfo = ref<any>(piniaStorage.getUserInfo() || {});
    function setUserInfo(value: any) {
        piniaStorage.setUserInfo(value);
        userInfo.value = value;
    }
    function removeUserInfo() {
        piniaStorage.removeUserInfo();
        userInfo.value = {};
    }

    return {
        userInfo,
        setUserInfo,
        removeUserInfo,
    };
});