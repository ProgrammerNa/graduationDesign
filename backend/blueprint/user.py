from flask import Blueprint,jsonify,request
#  获取操作数据的从操作游标
from config import cursor
from config import db
from jsonChange import change_json
user_blueprint = Blueprint('user',__name__,url_prefix='/user')