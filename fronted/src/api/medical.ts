import { get, post } from '../utils/http';

export const getMedicalTree = () => {
    return post('/medical/getMedicalTree')
}

export const addMedicalSave = (data:any) => {
    return post('/medical/addMedicalSave',data)
}

export const getMedicalInSaveList = (data:any) => {
    return post('/medical/getMedicalInSaveList',data)
}

export const sellMedicalList = (data:any) => {
    return post('/medical/sellMedicalList',data)
}

export const getMedicalInfoByDrugBarcode = (data:any) => {
    return post('/medical/getMedicalInfoByDrugBarcode',data)
}