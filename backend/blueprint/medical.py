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
    sql = """insert into medical (medical_name,medical_type_id,medical_price,save_store_id,medical_use_methods,medical_use_num,buy_isId,save_time,count,save_price,details)
                values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"""
    lock.acquire()
    cursor.execute(sql, (
    data['medicalName'], data['medicalType'], data['medicalOutPrice'], data['storeId'], data['eatMethods'],
    data['eatMedicalCount'], data['buyIdBool'], data['time'], data['count'], data['medicalInPrice'],
    data['medicalDetail']))
    db.commit()
    lock.release()
    return 'true'


# 获取入库列表
@medical_blueprint.route('/getMedicalInSaveList', methods=['POST'])
def get_medical_in_save_list():
    data = request.get_json(silent=True)
    if data['search']:
        sql = """
        select * from medical m INNER JOIN (select * from medical_type) mt on m.medical_type_id = mt.type_id 
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
                select * from medical m INNER JOIN (select * from medical_type) mt on m.medical_type_id = mt.type_id 
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
