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
