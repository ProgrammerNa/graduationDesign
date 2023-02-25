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
        sql = "select * from( select bool, role_id,role,GROUP_CONCAT(menu_id SEPARATOR ',') as menu_id from (select * from role r  inner JOIN (select * from  role_menu) rm on rm.role_id = r.id) as rrm GROUP BY role_id ) as t1 INNER JOIN(select * from (select role_id,GROUP_CONCAT(menu SEPARATOR ',') as menuName,GROUP_CONCAT(path SEPARATOR ',') as menuPath from(select * from menu m inner join (select menu_id as rm_id,role_id from role_menu) rm on m.menu_id  = rm.rm_id) as ti group by role_id) as t2 ) t3 on t1.role_id = t3.role_id  where role = %s "
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
        sql = " select * from( select bool, role_id,role,GROUP_CONCAT(menu_id SEPARATOR ',') as menu_id from (select * from role r  inner JOIN (select * from  role_menu) rm on rm.role_id = r.id) as rrm GROUP BY role_id ) as t1 INNER JOIN(select * from (select role_id,GROUP_CONCAT(menu SEPARATOR ',') as menuName,GROUP_CONCAT(path SEPARATOR ',') as menuPath from(select * from menu m inner join (select menu_id as rm_id,role_id from role_menu) rm on m.menu_id  = rm.rm_id) as ti group by role_id) as t2 ) t3 on t1.role_id = t3.role_id "
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
@sys_blueprint.route('/role', methods=['GET'])
def get_role():
    sql = "select * from role"
    cursor.execute(sql)
    result = cursor.fetchall()
    data = change_json.obj_to_json(result)
    return jsonify(data)


@sys_blueprint.route('/changeRoleMenu', methods=['POST'])
def change_role_menu():
    data = request.get_json(silent=True)
    sql1 = """ select role_id,GROUP_CONCAT(menu_id SEPARATOR ',') as menu_id from role_menu where role_id = %s GROUP BY role_id"""
    cursor.execute(sql1, data['roleId'])
    print(data['menuId'])
    sqlResult = cursor.fetchall()
    data1 = change_json.obj_to_json(sqlResult)
    menuArray = []
    for i in data1:
        menuArray = i['menu_id'].split(',')
    # 判断是否已经拥有菜单权限，进行相应的添加删除操作
    if len(data['menuId']) > len(menuArray):
        # 添加新增的菜单权限
        for id in data['menuId']:
            if id not in menuArray:
                sql2 = " insert into role_menu(menu_id,role_id) values (%s, %s)"
                cursor.execute(sql2, (id, data['roleId']))
                db.commit()
        for id in menuArray:
            if id not in data['menuId']:
                sql3 = "delete from role_menu where menu_id = %s and role_id=%s"
                cursor.execute(sql3, (id,data['roleId']))
                db.commit()
    elif len(data['menuId']) < len(menuArray) and len(data['menuId']) > 0:
        for id in menuArray:
            if id not in data['menuId']:
                sql3 = "delete from role_menu where menu_id = %s and role_id=%s"
                cursor.execute(sql3, (id,data['roleId']))
                db.commit()
        for i in data['menuId']:
            if i not in menuArray:
                sql2 = " insert into role_menu(menu_id,role_id) values (%s, %s)"
                cursor.execute(sql2, (i, data['roleId']))
                db.commit()
    elif len(data['menuId']) == len(menuArray):
        if len(data['menuId']) == 1:
            sql4 = "update role_menu set menu_id = %s where role_id = %s and menu_id = %s"
            cursor.execute(sql4,(data['menuId'][0],data['roleId'],menuArray[0]))
            db.commit()
        else:
            for i in data['menuId']:
                if i not in menuArray:
                    sql2 = " insert into role_menu(menu_id,role_id) values (%s, %s)"
                    cursor.execute(sql2, (i, data['roleId']))
                    db.commit()
            for id in menuArray:
                if id not in data['menuId']:
                    sql3 = "delete from role_menu where menu_id = %s and role_id=%s"
                    cursor.execute(sql3, (id, data['roleId']))
                    db.commit()



    else:
        print('kkkkkk')
    return 'true'

