from flask import Blueprint, jsonify, request
#  获取操作数据的从操作游标
from config import cursor
from config import db
from jsonChange import change_json

menu_blueprint = Blueprint('menu', __name__, url_prefix='/menu')


@menu_blueprint.route('/getMenuList', methods=['POST'])
def get_menu_list():
    data = request.get_json(silent=True)
    sql = """
    select menu_id as id,menu,pre_level as parent_id,flag,path,rid from (
    select * from menu m inner JOIN (select menu_id as mid,role_id as rid from role_menu) rm on  m.menu_id=rm.mid ) as t1 where t1.rid = %s"""
    cursor.execute(sql, data['roleId'])
    temp = cursor.fetchall()
    result = change_json.obj_to_json(temp)
    print(data['roleId'])
    return jsonify(result)


@menu_blueprint.route('/getAllMenuList', methods=['POST'])
def get_all_menu_list():
    sql = """select * from menu"""
    cursor.execute(sql)
    result = cursor.fetchall()
    data = change_json.obj_to_json(result)
    return jsonify(data)
