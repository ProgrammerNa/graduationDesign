import { get, post } from '../utils/http';
export const getMenuLsit = (data:any) => {
    console.log(data)
    return post('/menu/getMenuList',data)
}