from flask import Blueprint, jsonify, request
#  获取操作数据的从操作游标
from config import cursor
from config import db
from jsonChange import change_json

staff_blueprint = Blueprint('staff', __name__, url_prefix='/staff')


@staff_blueprint.route('/getStaffListByStoreId', methods=['POST'])
def get_staff_list_by_store_id():
    data = request.get_json(silent=True)
    if data['search']:
        sql = "select * from store st INNER JOIN ( select * from (SELECT * FROM yuangong yg INNER JOIN (select * FROM user) u on u.id = yg.zhanghao) as uy) uyg ON uyg.store = st.store_id where store_id = %s and name = %s"
        cursor.execute(sql, (data['id'], data['search']))
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
        sql = "select * from store st INNER JOIN ( select * from (SELECT * FROM yuangong yg INNER JOIN (select * FROM user) u on u.id = yg.zhanghao) as uy) uyg ON uyg.store = st.store_id where store_id = %s"
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


@staff_blueprint.route('/changeStaffStatus', methods=['POST'])
def change_staff_status():
    data = request.get_json(silent=True)
    sql = "UPDATE yuangong yg INNER JOIN user u on yg.zhanghao = u.id SET yg.type =%s,u.flag = %s WHERE yg.zhanghao = u.id  and u.id = %s"
    cursor.execute(sql, (data['type'],data['flag'],data['id']))
    cursor.fetchone()
    db.commit()
    return 'true'
