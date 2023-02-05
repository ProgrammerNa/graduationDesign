import { get, post } from '../utils/http';
export const getTest = () => {
    return get('/getMsg1');
};

export const postData = (data:any) => {
    console.log(data)
    return post('/getFontData',data);
};

export const getData = () => {
    return get('/getData');
};

export const add  = (data:any) => {
    return post('/add',data)
}
 export const addMore = (data:any) => {
    return post('/addMore',data)
 }

 export const getData1 = (data:any) => {
     return post('/get',data)
 }