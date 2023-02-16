from flask import Blueprint, jsonify, request
#  获取操作数据的从操作游标
from config import cursor
from config import db
from jsonChange import change_json

sys_blueprint = Blueprint('system', __name__, url_prefix='/system')


@sys_blueprint.route('/getUserList', methods=['POST'])
def get_user_list():
    data = request.get_json(silent=True)
    print(data['search'])
    if data['search']:
        sql = " select * from user u INNER JOIN (select * from role r INNER JOIN (select * FROM userRole) ur ON ur.role_id=r.id) r1 on u.id = r1.user_id where username=%s "
        # 执行sql语句
        cursor.execute(sql, (data['search']))
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
        sql = " select * from user u INNER JOIN (select * from role r INNER JOIN (select * FROM userRole) ur ON ur.role_id=r.id) r1 on u.id = r1.user_id "
        # 执行sql语句
        cursor.execute(sql)
        result = cursor.fetchall()
        start = (data['currentPage'] - 1) * data['pageSize']
        end = data['currentPage'] * data['pageSize']
        res = result[start:end]
        data1 = change_json.obj_to_json(res)
        return jsonify({
            'data': data1,
            'total': len(result)
        })


@sys_blueprint.route('/changeUserActivate', methods=['POST'])
def change_user_activate():
    data = request.get_json(silent=True)
    sql = "UPDATE user SET flag=%s where id = %s"
    cursor.execute(sql, (data['flag'], data['id']))
    print(data['flag'])
    print(data['id'])
    db.commit()
    return 'true'

@sys_blueprint.route('/getUserDetailByUserId',methods=['POST'])
def get_user_detail_by_user_id():
    data = request.get_json(silent=True)
    sql = """UPDATE user SET password='123456' where id = %s"""
    # 执行sql语句
    cursor.execute(sql, (data['id']))
    db.commit()
    return 'true'

