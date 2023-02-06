from flask import Flask
from test import test_t
from userLogin import login_blueprint
from menu import menu_blueprint
from user import  user_blueprint

app = Flask(__name__)
# 注册蓝图
app.register_blueprint(test_t)
app.register_blueprint(login_blueprint)
app.register_blueprint(menu_blueprint)
app.register_blueprint(user_blueprint)
@app.route('/')
def hello_world():
    return 'json'


if __name__ == '__main__':
    app.run()
