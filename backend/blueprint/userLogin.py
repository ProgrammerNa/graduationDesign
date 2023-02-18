# 示例使用，写一个蓝图均需在app.py中注册，方法名不能重复
from flask import Blueprint,jsonify,request
#  获取操作数据的从操作游标
from config import cursor
from config import db
from jsonChange import change_json
login_blueprint = Blueprint('login',__name__,url_prefix='/userlogin')


@login_blueprint.route('/login', methods=['POST'])
def loginUser():
    data = request.get_json(silent=True)
    print( data['username'])
    sql="select * from store st right JOIN(select * FROM(select * from user u INNER JOIN  (select role,user_id,role_id from (select * from role r INNER JOIN (select * FROM userRole) ur ON ur.role_id=r.id) as r1) rr  on u.id = rr.user_id) as t1) t2 on t2.store = st.store_id where username = %s and password = %s"
    # 执行sql语句
    cursor.execute(sql, (data['username'], data['password']))
    result = cursor.fetchall()
    print(result)
    data1 = change_json.obj_to_json(result)
    return jsonify(data1)
