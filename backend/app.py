from flask import Flask
from test import test_t
from userLogin import login_blueprint
from menu import menu_blueprint
from store import  store_blueprint
from system import sys_blueprint
from staff import staff_blueprint
from area import area_blueprint
from medical import medical_blueprint

app = Flask(__name__)
# 注册蓝图
app.register_blueprint(test_t)
app.register_blueprint(login_blueprint)
app.register_blueprint(menu_blueprint)
app.register_blueprint(store_blueprint)
app.register_blueprint(sys_blueprint)
app.register_blueprint(staff_blueprint)
app.register_blueprint(area_blueprint)
app.register_blueprint(medical_blueprint)
@app.route('/')
def hello_world():
    return 'json'


if __name__ == '__main__':
    app.run()
