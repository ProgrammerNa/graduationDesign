from flask import Blueprint, jsonify, request
#  获取操作数据的从操作游标
from config import cursor
from config import db
from jsonChange import change_json

medical_blueprint = Blueprint('medical', __name__, url_prefix='/medical')

@medical_blueprint.route('/getMedicalTree',methods=['POST'])
def get_medical_tree():
    sql = "select * from medical_type"
    cursor.execute(sql)
    result = cursor.fetchall()
    data = change_json.obj_to_json(result)
    return jsonify(data)

