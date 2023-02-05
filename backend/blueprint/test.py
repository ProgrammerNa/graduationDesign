# 示例使用，写一个蓝图均需在app.py中注册，方法名不能重复
from flask import Blueprint,jsonify,request
#  获取操作数据的从操作游标
from config import cursor
from config import db
from jsonChange import change_json
test_t = Blueprint('test',__name__,url_prefix='/')
# 获取所有数据示例，返回给前端
@test_t.route('/getMsg1', methods=['GET'])
def home():
    return 'teur'
# 获取前端传给后端数据的示例
@test_t.route('/getFontData', methods=['POST'])
def home1():
    result = request.get_json(silent=True)
    print(result)
    return result

# 使用常规sql查询示例(查询所有)
@test_t.route('/getData',methods=['GET'])
def getData():
    sql="select * from test"
    # 执行sql语句
    cursor.execute(sql)
    # 查询所有记录
    result = cursor.fetchall()
    # 转化成json
    data = change_json.obj_to_json(result)
    return jsonify(data)

# 查询指定条件数据
@test_t.route('/get',methods=['POST'])
def getData1():
    data = request.get_json(silent=True)
    print(data['id'])
    sql  = """select * from test where id= %s;"""
    # 执行sql语句
    cursor.execute(sql,data['id'])
    result = cursor.fetchall()
    data1 = change_json.obj_to_json(result)
    return jsonify(data1)

# 插入一条数据
@test_t.route('/add',methods=['POST'])
def add1():
    result = request.get_json(silent=True)
    # sql 语句
    sql = "insert into test(name) values (%s)"
    # 执行sql语句
    cursor.execute(sql,(result['name']))
    # 提交事务
    db.commit()
    return 'true'

# 插入多条数据 进行循环插入
@test_t.route('/addMore',methods=['POST'])
def addMore():
    data = request.get_json(silent=True)
    for i in data:
        for x in i:
            # sql 语句
            sql = "insert into test(name) values (%s)"
            # 执行sql语句
            cursor.execute(sql, (i[x]))
        # 提交事务
    db.commit()
    print(data)
    return 'sss'

#

