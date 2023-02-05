/*
 ** 防抖函数 n秒内重复出发，在n秒后执行最后一次触发
 ** 思路：
        （1）事件函数，创建定时器
        （2）将逻辑代码放入定时器中
        （3）函数再次触发，清除定时器
        （4）创建一个新的定时器
 */
export function debounce(fn: () => void) {
    // //保存定时器
    let timer: number | undefined;
    return function () {
        // n秒内重复触发清楚定时器
        if (timer) {
            clearTimeout(timer);
        }
        timer = setTimeout(() => {
            fn();
        }, 300);
    };
}
