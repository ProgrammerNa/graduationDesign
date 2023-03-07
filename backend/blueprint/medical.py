from flask import Blueprint, jsonify, request
#  获取操作数据的从操作游标
from config import cursor
from config import db
from jsonChange import change_json
from pagination import Pagination
import threading

medical_blueprint = Blueprint('medical', __name__, url_prefix='/medical')

lock = threading.Lock()


@medical_blueprint.route('/getMedicalTree', methods=['POST'])
def get_medical_tree():
    sql = "select type_id as id,type_name,parent_id from medical_type"
    # 互斥锁
    lock.acquire()
    cursor.execute(sql)
    result = cursor.fetchall()
    # 释放锁
    lock.release()
    data = change_json.obj_to_json(result)
    return jsonify(data)


# 入库新增
@medical_blueprint.route('/addMedicalSave', methods=['POST'])
def add_medical_save():
    data = request.get_json(silent=True)
    sql = """insert into ru_save_medical (medical_name,medical_type_id,medical_price,save_store_id,medical_use_methods,medical_use_num,buy_isId,save_time,count,save_price,details)
                values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"""
    cursor.execute(sql, (
        data['medicalName'], data['medicalType'], data['medicalOutPrice'], data['storeId'], data['eatMethods'],
        data['eatMedicalCount'], data['buyIdBool'], data['time'], data['count'], data['medicalInPrice'],
        data['medicalDetail']))
    db.commit()
    sql2 = """select `save_medical_name`  from save"""
    cursor.execute(sql2)
    name = cursor.fetchall()
    sql3 = """select sum(count) from ru_save_medical where medical_name=%s"""
    cursor.execute(sql3, (data['medicalName']))
    count = cursor.fetchall()
    if name[0][0] == data['medicalName']:
        sql4 = """update save set save_medical_count = %s where `save_medical_name` = %s"""
        cursor.execute(sql4, (count, data['medicalName']))
        db.commit()
    else:
        sql5 = """
        insert into save (save_medical_name,save_medical_count,save_store_id) values (%s,%s,%s)
        """
        cursor.execute(sql5, (data['medicalName'], count, data['storeId']))
        db.commit()

    return 'true'


# 获取入库列表
@medical_blueprint.route('/getMedicalInSaveList', methods=['POST'])
def get_medical_in_save_list():
    data = request.get_json(silent=True)
    if data['search']:
        sql = """
        select * from ru_save_medical m INNER JOIN (select * from medical_type) mt on m.medical_type_id = mt.type_id 
        where save_store_id = %s and medical_name = %s or type_name = %s
        """
        lock.acquire()
        cursor.execute(sql, (data['storeId'], data['search'], data['search']))
        result = cursor.fetchall()
        lock.release()
        res = Pagination.get_pagination(data, result)
        data1 = change_json.obj_to_json(res)
        return jsonify({
            'data': data1,
            'total': len(result)
        })
    else:
        sql = """
                select * from ru_save_medical m INNER JOIN (select * from medical_type) mt on m.medical_type_id = mt.type_id 
                where save_store_id = %s
                """
        lock.acquire()
        cursor.execute(sql, (data['storeId']))
        result = cursor.fetchall()
        lock.release()
        res = Pagination.get_pagination(data, result)
        data1 = change_json.obj_to_json(res)
        return jsonify({
            'data': data1,
            'total': len(result)
        })


# 获取可销售药品库存列表
@medical_blueprint.route('/sellMedicalList', methods=['POST'])
def sell_medical_list():
    data = request.get_json(silent=True)
    if data['search']:

        sql = """
        select * from medical_type mt INNER JOIN(SELECT * from(select * FROM save s LEFT JOIN (select * from(select medical_name,medical_type_id,save_store_id as id,medical_price,medical_use_methods,medical_use_num,buy_isId,details from ru_save_medical
     GROUP BY medical_name) as rm) t1 on s.save_store_id = t1.id and t1.medical_name = s.save_medical_name ) t3 )t4 on mt.type_id = t4.medical_type_id where save_store_id = %s and medical_name = %s or type_name = %s
        """
        lock.acquire()
        cursor.execute(sql, (data['storeId'], data['search'], data['search']))
        result = cursor.fetchall()
        lock.release()
        res = Pagination.get_pagination(data, result)
        data1 = change_json.obj_to_json(res)
        return jsonify({
            'data': data1,
            'total': len(result)
        })

    else:
        sql = """
               select * from medical_type mt INNER JOIN(SELECT * from(select * FROM save s LEFT JOIN (select * from(select medical_name,medical_type_id,save_store_id as id,medical_price,medical_use_methods,medical_use_num,buy_isId,details from ru_save_medical
            GROUP BY medical_name) as rm) t1 on s.save_store_id = t1.id and t1.medical_name = s.save_medical_name ) t3 )t4 on mt.type_id = t4.medical_type_id where save_store_id = %s 
               """
        lock.acquire()
        cursor.execute(sql, (data['storeId']))
        result = cursor.fetchall()
        lock.release()
        res = Pagination.get_pagination(data, result)
        data1 = change_json.obj_to_json(res)
        return jsonify({
            'data': data1,
            'total': len(result)
        })
