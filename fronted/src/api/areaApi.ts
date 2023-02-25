import { get, post } from '../utils/http';
export const getAreaList = () => {
    return post('/area/getAreaList')
}