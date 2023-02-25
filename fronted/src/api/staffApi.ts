import { get, post } from '../utils/http';

export const getStaffListByStoreId = (data:any) => {
    console.log(data)
    return post('/staff/getStaffListByStoreId',data)
}
export const changeStaffStatus = (data:any) => {
    return post('/staff/changeStaffStatus',data)
}

export const addNewStaff = (data:any) => {
    return post('/staff/addStaff',data)
}