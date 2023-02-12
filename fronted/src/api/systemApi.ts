import {get, post} from '../utils/http';

export const getUserList = () => {
    return post('/system/getUserList')
}

export const changeUserActivate = (data: any) => {
    return post('/system/changeUserActivate', data)
}