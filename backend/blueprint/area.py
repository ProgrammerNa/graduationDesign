from flask import Blueprint, jsonify, request
#  获取操作数据的从操作游标
from config import cursor
from config import db
from jsonChange import change_json

area_blueprint = Blueprint('area', __name__, url_prefix='/area')


@area_blueprint.route('/getAreaList', methods=['POST'])
def get_area_list():
    sql = """select province,city,area,street from 
    (select * from (
            SELECT AREA_CODE as aco,GROUP_CONCAT(STREET_NAME SEPARATOR ',') AS street FROM bs_street GROUP BY AREA_CODE) as sta INNER JOIN (select * from (SELECT * FROM (select CITY_CODE AS CO,AREA_CODE,GROUP_CONCAT(AREA_NAME SEPARATOR ',') AS area from bs_area GROUP BY CO) AS AC INNER JOIN
                (SELECT * FROM  (
                    select * from (select PROVINCE_CODE AS PC_CODE,CITY_CODE,GROUP_CONCAT(CITY_NAME SEPARATOR ',') as city from  bs_city GROUP BY PC_CODE) as pc INNER JOIN (select PROVINCE_CODE,PROVINCE_NAME as province from bs_province )bp on bp.PROVINCE_CODE=pc.PC_CODE
                    ) AS T1) T2 ON T2.CITY_CODE = AC.CO) as t4) t5 ON t5.AREA_CODE = sta.aco) as t6"""
    cursor.execute(sql)
    result = cursor.fetchall()
    data = change_json.obj_to_json(result)
    return jsonify(data)
