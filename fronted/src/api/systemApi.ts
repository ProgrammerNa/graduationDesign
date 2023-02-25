import {get, post} from '../utils/http';

export const getUserList = (data:any) => {
    return post('/system/getUserList',data)
}

export const changeUserActivate = (data: any) => {
    return post('/system/changeUserActivate', data)
}

export const resetUserPassword = (data:any) => {
    return post('/system/resetUserPassword', data)
}
export const getRoleList = (data:any) => {
    return post('/system/getRoleList',data)
}
//获取角色名称
export const getRoleName = () => {
    return get('/system/role')
}

export const changeRoleMenu = (data:any) => {
    return post('system/changeRoleMenu',data)
}