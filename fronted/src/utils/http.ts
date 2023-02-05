import axios from 'axios';
import QS from 'qs';
axios.defaults.timeout = 30000;
axios.defaults.headers["Content-Type"]="application/json; charset=utf-8"
// 创建axios实例
const service = axios.create({
    baseURL: '/api',
});

// 添加请求拦截器 后进先执行  ===》 前端给后端的参数，但后端还未响应
service.interceptors.request.use(
    // congig是配置对象，可以对其进行更改
    function (config) {
        // 此处是做登录的判断，如果用户是登陆状态，会在headers中把用户的token传递给后端
        // 在发送请求之前做些什么
        console.log('请求拦截器成功');
        return config;
    },
    function (error) {
        // 对请求错误做些什么
        console.log('请求拦截器失败');
        return Promise.reject(error);
    }
);

// 添加响应拦截器 先进先执行 ===》 后端给前端的数据 ，后端返回给前端的东西
service.interceptors.response.use(
    function (response) {
        // 2xx 范围内的状态码都会触发该函数。
        // 对响应数据做点什么
        console.log('请求响应拦截器成功');
        return response;
    },
    function (error) {
        // 超出 2xx 范围的状态码都会触发该函数。
        // 对响应错误做点什么
        console.log('请求响应拦截器失败');
        return Promise.reject(error);
    }
);

// 封装get方法
export function get(url: any, params?: any) {
    return new Promise((resolve, reject) => {
        service
            .get(url, {
                params: params,
            })
            .then((res) => {
                resolve(res);
            })
            .catch((err) => {
                reject(err);
            });
    });
}

// 封装post方法
export function post(url: any, params?: any,) {
    return new Promise((resolve, reject) => {
        service
            .post(
                url,
                params)
            .then((res) => {
                console.log(res)
                resolve(res);
            })
            .catch((err) => {
                reject(err);
            });
    });
}
// 最终返回，将其暴露出去
export default service;
