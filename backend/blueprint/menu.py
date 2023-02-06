from flask import Blueprint,jsonify,request
#  获取操作数据的从操作游标
from config import cursor
from config import db
from jsonChange import change_json
menu_blueprint = Blueprint('menu',__name__,url_prefix='/menu')

@menu_blueprint.route('/getMenuList',methods=['POST'])
def get_menu_list():
    data = request.get_json(silent=True)
    sql="select * from menu where role_menu_id = %s"
    cursor.execute(sql,(data['roleId']))
    temp = cursor.fetchall()
    result = change_json.obj_to_json(temp)
    print(data['roleId'])
    return jsonify(result)