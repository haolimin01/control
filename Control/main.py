from flask import abort, redirect, url_for, request, Flask, g
import json
from Database.DB import DB
from utils.utils import *
app = Flask(__name__)

# post/status/ (task, network)
# update/task/
# update/network/
# status/ (user)
# email/
@app.route('/')
def redirect_index():
    return redirect(url_for('index'))


@app.route('/index/')
def index():
    data = {
        'author': 'HaoLimin',
        'email': 'haolimin01@baidu.com',
        'about': 'This is a small Flask App with sqlite3 developed by me :)'
    }
    return json.dumps(data, ensure_ascii=False) + '\n'


@app.route('/post/status/', methods=['GET', 'POST'])
def post_status():
    if request.method == 'GET':
        error = True
        detail = 'Please use POST method and upload the device info of mac,name,task,status,limitation,maxup and maxdown.'
        data = {
            'error': error,
            'detail': detail
        }
        return json.dumps(data, ensure_ascii=False) + '\n'
    elif request.method == 'POST':
        success = post_status_data(request.json)
        if success:
            error = False
            detail = 'Post data success.'
        else:
            error = True
            detail = 'Post data failed.'
        data = {
            'error': error,
            'detail': detail
        }
        return json.dumps(data, ensure_ascii=False) + '\n'





# @app.route('/update/task/')
#
# @app.route('/update/network/')
#
# 指定查询设备设备或是全部数据
@app.route('/status/', methods=['GET'])
def get_status():
    

# @app.route('/email/')


@app.route('/limit/', methods=['POST', 'GET'])
def limit():
    if request.method == 'GET':
        return 'Please upload limit info.'
    elif request.method == 'POST':
        content = request.json
        mac = content['ma']
        print(mac)
        return 'done\n'
    return 'error ...'


@app.before_request
def before_request():
    db = getattr(g, 'db', None)
    if db is None:
        db = DB(table='status')
        g.db = db
    print('before_request')


@app.teardown_request
def teardown_request(exception=None):
    db = hasattr(g, 'db')
    if db is not None:
        g.db.close()
    print('teardown_request')


def post_status_data(content):
    mac = get_value(content, 'mac')
    name = get_value(content, 'name')
    task = get_value(content, 'task')
    status = get_value(content, 'status', default='working')
    limitation = get_value(content, 'limitation', default=0)
    maxup = get_value(content, 'maxup', default=0)
    maxdown = get_value(content, 'maxdown', default=0)
    if mac and name and task:
        success = g.db.insert(mac=mac, name=name, task=task, status=status, limitation=limitation, maxup=maxup, maxdown=maxdown)
        return success
    else:
        return False




if __name__ == '__main__':
    app.run(debug=True)