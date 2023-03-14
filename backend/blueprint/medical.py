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
    print(data)
    for i in data['data']:
        print(i['time'][0])
        sql = """insert into ru_save_medical (save_medical_num,medical_name,medical_type_id,medical_price,save_store_id,medical_standards,save_time,count,save_price,producat_time,medical_out_time,drug_barcode)
                    values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"""
        cursor.execute(sql, (i['saveMedicalNum'],
                             i['medicalName'], i['medicalType'], i['medicalOutPrice'], data['storeId'],
                             i['medicalStandards'],
                             data['saveTime'], i['count'], i['medicalInPrice'], i['time'][0], i['time'][1],
                             i['drugBarcode']))
        db.commit()
        sql2 = """insert into ru_save_medical_copy (save_medical_num,medical_name,medical_type_id,medical_price,save_store_id,medical_standards,save_time,count,save_price,producat_time,medical_out_time,drug_barcode)
                           values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"""
        cursor.execute(sql2, (i['saveMedicalNum'],
                              i['medicalName'], i['medicalType'], i['medicalOutPrice'], data['storeId'],
                              i['medicalStandards'],
                              data['saveTime'], i['count'], i['medicalInPrice'], i['time'][0], i['time'][1],
                              i['drugBarcode']))
        db.commit()

    return 'true'


# 获取库存记录列表
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


# 获取销售列表信息
@medical_blueprint.route('/sellMedicalList', methods=['POST'])
def sell_medical_list():
    data = request.get_json(silent=True)
    sql = """
           select * from sell where sell_store_id = %s
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


# 根据批号,药品名称查询药品
@medical_blueprint.route('/getMedicalInfoByDrugBarcode', methods=['POST'])
def get_medical_info_by_drug_barcode():
    data = request.get_json(silent=True)
    sql = """
     select * from ru_save_medical_copy m INNER JOIN (select * from medical_type) mt on m.medical_type_id = mt.type_id 
    where save_store_id = %s and drug_barcode = %s or medical_name=%s
                       """
    cursor.execute(sql, (data['storeId'], data['search'],data['search']))
    result = cursor.fetchall()
    data1 = change_json.obj_to_json(result)
    return jsonify(data1)
