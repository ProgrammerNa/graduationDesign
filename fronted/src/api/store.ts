import { get, post } from '../utils/http';
export const getStoreList = (data:any) => {
    return post('/store/getStoreList',data)
}