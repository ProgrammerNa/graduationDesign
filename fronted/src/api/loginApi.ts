import { get, post } from '../utils/http';
export const userLogin = (data:any) => {
    console.log(data)
    return post('/userlogin/login',data)
}
