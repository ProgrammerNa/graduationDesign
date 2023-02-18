from flask import Blueprint, jsonify, request
#  获取操作数据的从操作游标
from config import cursor
from config import db
from jsonChange import change_json

sys_blueprint = Blueprint('system', __name__, url_prefix='/system')

# 获取用户列表
@sys_blueprint.route('/getUserList', methods=['POST'])
def get_user_list():
    data = request.get_json(silent=True)
    print(data['search'])
    if data['search']:
        sql = " select * from store st right JOIN(select * FROM(select * from user u INNER JOIN  (select role,user_id,role_id from (select * from role r INNER JOIN (select * FROM userRole) ur ON ur.role_id=r.id) as r1) rr  on u.id = rr.user_id) as t1) t2 on t2.store = st.store_id where username=%s "
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
        sql = "select * from store st right JOIN(select * FROM(select * from user u INNER JOIN  (select role,user_id,role_id from (select * from role r INNER JOIN (select * FROM userRole) ur ON ur.role_id=r.id) as r1) rr  on u.id = rr.user_id) as t1) t2 on t2.store = st.store_id "
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


# 改变用户启用禁用状态
@sys_blueprint.route('/changeUserActivate', methods=['POST'])
def change_user_activate():
    data = request.get_json(silent=True)
    sql = "UPDATE user SET flag=%s where id = %s"
    cursor.execute(sql, (data['flag'], data['id']))
    print(data['flag'])
    print(data['id'])
    db.commit()
    return 'true'

# 重置用户密码
@sys_blueprint.route('/resetUserPassword', methods=['POST'])
def reset_user_password():
    data = request.get_json(silent=True)
    sql = """UPDATE user SET password='123456' where id = %s"""
    # 执行sql语句
    cursor.execute(sql, (data['id']))
    db.commit()
    return 'true'

# 获取角色列表分页
@sys_blueprint.route('/getRoleList', methods=['POST'])
def get_role_list():
    data = request.get_json(silent=True)
    print(data['search'])
    if data['search']:
        sql = " select * from role where role = %s "
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
        sql = " select * from role "
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

#    获取角色
@sys_blueprint.route('/role',methods=['GET'])
def get_role():
    sql = "select * from role"
    cursor.execute(sql)
    result = cursor.fetchall()
    data = change_json.obj_to_json(result)
    return jsonify(data)
