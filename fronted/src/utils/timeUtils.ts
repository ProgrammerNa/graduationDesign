import dayjs from 'dayjs';

// 时间格式处理
export const formateTime = (time: string, type = 'YYYY-MM-DD') => {
    if (!time) {
        return '';
    }
    return dayjs(`${time}`).format(type);
};
