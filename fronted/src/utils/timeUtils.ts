import dayjs from 'dayjs';

// 时间格式处理
export const formateTime = (val: string, type = 'YYYY-MM-DD') => {
    if (!val) {
        return '';
    }
    let time = new Date(new Date(val).getTime() + new Date(val).getTimezoneOffset()*60*1000)
    return dayjs(`${time}`).format(type);
};
