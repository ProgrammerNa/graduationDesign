class Pagination:
    @staticmethod
    def get_pagination(data,result):
        start = (data['currentPage'] - 1) * data['pageSize']
        end = data['currentPage'] * data['pageSize']
        res = result[start:end]
        return res


