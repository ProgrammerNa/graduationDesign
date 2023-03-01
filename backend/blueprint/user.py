from flask import Blueprint, jsonify, request
#  获取操作数据的从操作游标
from config import cursor
from config import db
from jsonChange import change_json

user_blueprint = Blueprint('user', __name__, url_prefix='/user')


@user_blueprint.route('/checkPassword', methods=['POST'])
def check_password():
    data = request.get_json(silent=True)
    sql = """UPDATE user SET password=%s where id = %s"""
    # 执行sql语句
    cursor.execute(sql, (data['password'], data['id']))
    db.commit()
    return 'true'
