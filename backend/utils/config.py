import pymysql
# 打开数据库连接
db = pymysql.connect(host="localhost",user="root",password="root",database="graduationdesign")
# 使用cursor()获取数据库操作游标
cursor = db.cursor()