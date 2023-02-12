from flask import Blueprint,jsonify,request
#  获取操作数据的从操作游标
from config import cursor
from config import db
from jsonChange import change_json
sys_blueprint = Blueprint('system',__name__,url_prefix='/system')


@sys_blueprint.route('/getUserList', methods=['POST'])
def get_user_list():
    sql=" select * from user u INNER JOIN (select * from role r INNER JOIN (select * FROM userRole) ur ON ur.role_id=r.id) r1 on u.id = r1.user_id "
    # 执行sql语句
    cursor.execute(sql)
    result = cursor.fetchall()
    print(result)
    data1 = change_json.obj_to_json(result)
    return jsonify(data1)


@sys_blueprint.route('/changeUserActivate', methods=['POST'])
def change_user_activate():
    data = request.get_json(silent=True)
    sql = "UPDATE user SET flag=%s where id = %s"
    cursor.execute(sql,(data['flag'],data['id']))
    print(data['flag'])
    print(data['id'])
    db.commit()
    return 'true'