import { get, post } from '../utils/http';

export const getMedicalTree = () => {
    return post('/medical/getMedicalTree')
}