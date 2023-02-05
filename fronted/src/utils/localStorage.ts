import { DEFAULT_LOCAL_STORAGE_KEY_PREFIX } from './const';

function isLocalStorageUsable() {
    const localStorageTestKey = '__localStorage_support_test';
    const localStorageTestValue = 'test';
    let isSupport = false;

    try {
        localStorage.setItem(localStorageTestKey, localStorageTestValue);
        if (
            localStorage.getItem(localStorageTestKey) === localStorageTestValue
        ) {
            isSupport = true;
        }
        localStorage.removeItem(localStorageTestKey);
        return isSupport;
    } catch (e: any) {
        if (
            e.name === 'QuotaExceededError' ||
            e.name === 'NS_ERROR_DOM_QUOTA_REACHED'
        ) {
            console.warn('localStorage 存储已达上限！');
        } else {
            console.warn('当前浏览器不支持 localStorage！');
        }
        return isSupport;
    }
}

function normalizeKey(key: string) {
    if (typeof key !== 'string') {
        console.warn(`${key} used as a key, but it is not a string.`);
        key = String(key);
    }
    return key;
}

function serialize(value: string | number, callback: any) {
    try {
        const valueString = JSON.stringify(value);
        callback(null, valueString);
    } catch (e) {
        callback(e);
    }
}

class StorageHandler {
    private isSupport: boolean | undefined;
    private KEY_PREFIX: string = DEFAULT_LOCAL_STORAGE_KEY_PREFIX;
    static instance: StorageHandler;

    constructor() {
        this.KEY_PREFIX = `${DEFAULT_LOCAL_STORAGE_KEY_PREFIX}`;
    }

    static getInstance() {
        if (!StorageHandler.instance) {
            StorageHandler.instance = new StorageHandler();
        }
        return StorageHandler.instance;
    }

    private ready() {
        if (this.isSupport == null) {
            this.isSupport = isLocalStorageUsable();
        }
        return this.isSupport;
    }

    setItem(key: string, value: any) {
        key = normalizeKey(key);
        if (this.ready()) {
            if (value === undefined) {
                value = null;
            }
            serialize(value, (error: any, valueString: string) => {
                if (error) {
                    return;
                }
                try {
                    const FINAL_KEY = `${this.KEY_PREFIX}${key}`;
                    localStorage.setItem(FINAL_KEY, valueString);
                } catch (e) {
                    console.log('e', e);
                }
            });
        }
    }

    getItem(key: string) {
        key = normalizeKey(key);
        const FINAL_KEY = `${this.KEY_PREFIX}${key}`;
        const result = localStorage.getItem(FINAL_KEY);
        if (result) {
            return JSON.parse(result);
        }
    }

    removeItem(key: string) {
        key = normalizeKey(key);
        const FINAL_KEY = `${this.KEY_PREFIX}${key}`;
        localStorage.removeItem(FINAL_KEY);
    }

    hasItem(key: string) {
        key = normalizeKey(key);
        const FINAL_KEY = `${this.KEY_PREFIX}${key}`;
        return Object.prototype.hasOwnProperty.call(localStorage, FINAL_KEY);
    }

    getAllKeys() {
        return Object.keys(localStorage);
    }

    clearAll() {
        localStorage.clear();
    }
}

export default StorageHandler;
