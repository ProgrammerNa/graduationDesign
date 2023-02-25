import { get, post } from '../utils/http';
export const getStoreList = (data:any) => {
    return post('/store/getStoreList',data)
}
export const addStore = (data:any) => {
    console.log(data)
    return post('/store/addStore',data)
}

export const updateStoreInfo = (data:any) => {
    return post('/store/updateStoreInfo',data)
}