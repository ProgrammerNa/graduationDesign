import { get, post } from '../utils/http';

export const checkPassword = (data:any) => {
    return post('/user/checkPassword',data)
}
