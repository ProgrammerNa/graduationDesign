import { get, post } from '../utils/http';

export const getStaffListByStoreId = (data:any) => {
    return post('/staff/getStaffListByStoreId',data)
}
export const changeStaffStatus = (data:any) => {
    return post('/staff/changeStaffStatus',data)
}