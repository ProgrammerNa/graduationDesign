import { get, post } from '../utils/http';
export const getAreaList = () => {
    return post('/area/getAreaList')
}

export  const getCity = () => {
    return get('https://restapi.amap.com/v3/config/district?subdistrict=5&key=0acd16d73f18df580f5181cc18137852')
}