from flask import Blueprint, jsonify, request
#  获取操作数据的从操作游标
from config import cursor
from config import db
from jsonChange import change_json

menu_blueprint = Blueprint('menu', __name__, url_prefix='/menu')


@menu_blueprint.route('/getMenuList', methods=['POST'])
def get_menu_list():
    data = request.get_json(silent=True)
    sql = """select * FROM (select * from menu m LEFT JOIN( select pre_level as parent_id,GROUP_CONCAT(menu,path SEPARATOR ',') as menu_path from menu GROUP BY pre_level) m1 on m.menu_id = m1.parent_id where m.pre_level = 0) as c1 INNER JOIN (select menu_id as id,GROUP_CONCAT(role_id SEPARATOR ',') as role_id from role_menu rm  GROUP BY menu_id ) c2 ON c2.id = c1.menu_id where c2.role_id LIKE  '%%%s%%'"""
    cursor.execute(sql, data['roleId'])
    temp = cursor.fetchall()
    result = change_json.obj_to_json(temp)
    print(data['roleId'])
    return jsonify(result)


@menu_blueprint.route('/getAllMenuList', methods=['POST'])
def get_all_menu_list():
    sql = """
    select * FROM (select * from menu m LEFT JOIN( select pre_level as parent_id,GROUP_CONCAT(menu,path SEPARATOR ',') as menu_path from menu GROUP BY pre_level) m1 on m.menu_id = m1.parent_id where m.pre_level = 0) as c1 INNER JOIN (select menu_id as id,GROUP_CONCAT(role_id SEPARATOR ',') as role_id from role_menu rm  GROUP BY menu_id ) c2 ON c2.id = c1.menu_id 
    """
    cursor.execute(sql)
    result = cursor.fetchall()
    data = change_json.obj_to_json(result)
    return jsonify(data)
