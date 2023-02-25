from flask import Blueprint, jsonify, request
#  获取操作数据的从操作游标
from config import cursor
from config import db
from pagination import Pagination
from jsonChange import change_json

store_blueprint = Blueprint('store', __name__, url_prefix='/store')


@store_blueprint.route('/getStoreList', methods=['POST'])
def get_store_list():
    data = request.get_json(silent=True)
    if data['search']:
        sql = "select * from store st right JOIN(select * FROM(select * from user u INNER JOIN  (select role,user_id,role_id from (select * from role r INNER JOIN (select * FROM userRole) ur ON ur.role_id=r.id) as r1) rr  on u.id = rr.user_id) as t1) t2 on t2.store = st.store_id WHERE role_id = 3 and  parent_id = %s and store_name = %s or phone = %s or store_responsible = %s"
        cursor.execute(sql, (data['id'], data['search'], data['search'], data['search']))
        result = cursor.fetchall()
        res = Pagination.get_pagination(data, result)
        data1 = change_json.obj_to_json(res)
        return jsonify({
            'data': data1,
            'total': len(result)
        })
    else:
        sql = "select * from store st right JOIN(select * FROM(select * from user u INNER JOIN  (select role,user_id,role_id from (select * from role r INNER JOIN (select * FROM userRole) ur ON ur.role_id=r.id) as r1) rr  on u.id = rr.user_id) as t1) t2 on t2.store = st.store_id WHERE role_id = 3 and parent_id = %s"
        cursor.execute(sql, (data['id']))
        result = cursor.fetchall()
        res = Pagination.get_pagination(data, result)
        data1 = change_json.obj_to_json(res)
        return jsonify({
            'data': data1,
            'total': len(result)
        })


@store_blueprint.route('/addStore', methods=['POST'])
def add_store():
    data = request.get_json(silent=True)
    sql = "insert into store (store_name,store_address,store_responsible,phone,parent_id) values (%s,%s,%s,%s,%s)"
    cursor.execute(sql,
                   (data['storeName'], data['storeAddress'], data['storeResponsible'], data['phone'], data['parentId']))
    new_store_id = cursor.lastrowid
    print(new_store_id)
    db.commit()
    sql1 = "insert into user (username,password,store) values (%s,%s,%s)"
    cursor.execute(sql1, (data['username'], data['password'], new_store_id))
    new_user_id = cursor.lastrowid
    print(new_user_id)
    db.commit()
    sql2 = "insert into userRole (user_id,role_id) values  (%s,3)"
    cursor.execute(sql2, (new_user_id))
    db.commit()
    return 'true'


@store_blueprint.route('/updateStoreInfo', methods=['POST'])
def update_store_info():
    data = request.get_json(silent=True)
    sql = "update store set store_name = %s,store_address=%s,store_responsible=%s,phone=%s where store_id = %s"
    cursor.execute(sql, (data['storeName'], data['storeAddress'], data['storeResponsibleName'], data['storePhone'],data['storeId']))
    db.commit()
    return 'true'
