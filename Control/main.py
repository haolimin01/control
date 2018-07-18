from flask import abort, redirect, url_for, request, Flask, g, render_template
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
    author = 'HaoLimin'
    emial = '15029182243@163.com'
    about = 'This is a small Flask App with sqlite3 developed by me :)'
    return send_index(author=author, email=emial, about=about)


@app.route('/post/status/', methods=['GET', 'POST'])
def post_status():
    if request.method == 'GET':
        error = True
        detail = 'Please use POST method and upload the device info of mac,name,task,status,limitation,maxup and maxdown.'
        return send_msg(error=error, detail=detail)
    elif request.method == 'POST':
        success = post_status_data(request.json)
        if success:
            error = False
            detail = 'Post data success.'
        else:
            error = True
            detail = 'Post data failed.'
        return send_msg(error=error, detail=detail)





# @app.route('/update/task/')
#
# @app.route('/update/network/')
#
# 指定查询设备设备或是全部数据
@app.route('/status/', methods=['POST', 'GET'])
def get_status():
    if request.method == 'POST':
        error = True
        detail = "Please use GET method with or without the device's mac address."
        return send_msg(error=error, detail=detail)
    elif request.method == 'GET':
        mac = request.args.get('mac', None)
        if mac:
            result = show(mac=mac)
        else:
            result = show_all()
        if result is False:
            error = True
            detail = 'Table or mac address is not exist'
            return send_msg(error=error, detail=detail)
        else:
            result = json.loads(result)
            if type(result) is list:
                return render_template('show_status.html', result=result, type='list')
            elif type(result) is dict:
                return render_template('show_status.html', result=result, type='dict')


# @app.route('/email/')

@app.route('/update/task', methods=['GET', 'POST'])
def update_task():
    if request.method == 'GET':
        error = True
        detail = "Please use POST method and upload the device's mac and task"
        return send_msg(error=error, detail=detail)
    elif request.method == 'POST':
        return 'post'


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


def show(mac=None):
    if mac is None:
        return False
    elif not g.db.mac_exist(mac=mac):
        return False
    else:
        result = g.db.query(mac=mac)
        if request is None:
            return False
        else:
            return result


def show_all():
    if not g.db.table_exist():
        return False
    else:
        result = g.db.display_all()
        return result


if __name__ == '__main__':
    app.run(debug=True)
