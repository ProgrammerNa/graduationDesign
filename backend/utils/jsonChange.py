from config import cursor
class change_json:
    @staticmethod
    def obj_to_json(obj):
        '''
        将获取的数据库对象转化成json数据传给前端
        '''
        # 获取字段名
        data_dict = []
        for filed in cursor.description:
            data_dict.append(filed[0])
        #  转化为json
        res = [dict(zip(data_dict, i)) for i in obj]
        return res

    @staticmethod
    def dict_slice_data(data,start,end):
        '''分页切片'''
        key=data.keys()
        dict_slice = {}
        for k in list(key)[start:end]:
            dict_slice[k] = data[k]
        return dict_slice