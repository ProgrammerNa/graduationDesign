from flask import Blueprint,jsonify,request
#  获取操作数据的从操作游标
from config import cursor
from config import db
from jsonChange import change_json
store_blueprint = Blueprint('store',__name__,url_prefix='/store')

@store_blueprint.route('/getStoreList',methods=['POST'])
def get_store_list():
    data = request.get_json(silent=True)
    if data['search']:
        sql = "select * from store where parent_id = %s and store_name = %s or phone = %s or store_responsible = %s"
        cursor.execute(sql,(data['id'],data['search'],data['search'],data['search']))
        result = cursor.fetchall()
        start = (data['currentPage'] - 1) * data['pageSize']
        end = data['currentPage'] * data['pageSize']
        res = result[start:end]
        data1 = change_json.obj_to_json(res)
        return jsonify({
            'data': data1,
            'total': len(result)
        })
    else:
        sql = "select * from store where parent_id = %s"
        cursor.execute(sql, (data['id']))
        result = cursor.fetchall()
        start = (data['currentPage'] - 1) * data['pageSize']
        end = data['currentPage'] * data['pageSize']
        res = result[start:end]
        data1 = change_json.obj_to_json(res)
        return jsonify({
            'data': data1,
            'total': len(result)
        })
