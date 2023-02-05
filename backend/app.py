from flask import Flask
from test import test_t
from userLogin import login_blueprint

app = Flask(__name__)
# 注册蓝图
app.register_blueprint(test_t)
app.register_blueprint(login_blueprint)
@app.route('/')
def hello_world():
    return 'json'


if __name__ == '__main__':
    app.run()
