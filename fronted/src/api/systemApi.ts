import {get, post} from '../utils/http';

export const getUserList = (data:any) => {
    return post('/system/getUserList',data)
}

export const changeUserActivate = (data: any) => {
    return post('/system/changeUserActivate', data)
}

export const getUserDetailByUserId = (data:any) => {
    return post('/system/getUserDetailByUserId', data)
}