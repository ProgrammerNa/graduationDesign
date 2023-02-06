import StorageHandler from './localStorage';
const stroageHandler = StorageHandler.getInstance();
export const setUserInfo = (userInfo: any) => {
    StorageHandler.getInstance().setItem('userInfo', userInfo);
};

export const getUserInfo = () => {
    return StorageHandler.getInstance().getItem('userInfo');
};

export const removeUserInfo = () => {
    StorageHandler.getInstance().removeItem('userInfo');
};

export const setRoleMenuList = (roleMenuList: any[]) => {
	// 调用本地存储中setItem方法，存储值，将key值设置为roleMenuList
   StorageHandler.getInstance().setItem('roleMenuList', roleMenuList);
};

export const getRoleMenuList = () => {
	// 调用本地存储getItem方法，获取key为roleMenuList的值
    return StorageHandler.getInstance().getItem('roleMenuList');
};

export const removeRoleMenuList = () => {
    StorageHandler.getInstance().removeItem('roleMenuList');
};
