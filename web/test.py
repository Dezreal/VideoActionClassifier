# coding=utf-8
import os
import sys

from flask import Flask, render_template, request, session, redirect, jsonify
from werkzeug.utils import secure_filename

from web.db.mysqlpool import Mysql
from web.eval_thread import EvalThread
from web.login import login_api, getLastDate

reload(sys)
sys.setdefaultencoding('utf-8')

app = Flask(__name__, static_url_path='')
app.register_blueprint(login_api)
app.secret_key = 'random string'


class ThreadPool:

    def __init__(self):
        self.index = -1
        self.threads = []

    def add(self, thread):
        self.threads.append(thread)
        self.index = self.index + 1

    def get_thread(self):
        return self.threads[self.index]


thread_pool = ThreadPool()
mysql = Mysql()


@app.route('/')
def index():
    if len(session) == 0:
        name = "登录"
    else:
        name = "Hello! " + session['username']
    return render_template('index.html', username=name)


@app.route('/upload')
def upload():
    if 'username' in session:
        return redirect('/upload/upload.html')
    else:
        return redirect('/login')


@app.route('/uploader', methods=['POST'])
def upload_file():
    if 'username' in session:
        username = session['username']
        f = request.files['file']
        filename = secure_filename(f.filename)
        f.save(filename)
        abs_path = os.path.abspath('.') + "/"
        eval_thread = EvalThread()
        eval_thread.set_path(abs_path, filename)
        eval_thread.set_username(username)
        eval_thread.start()
        thread_pool.add(eval_thread)

        return redirect('/widget/analysis.html')
    else:
        return redirect('/login')


@app.route('/analysis')
def info():
    rst = thread_pool.get_thread().get_info()
    alive = thread_pool.get_thread().is_alive()
    detail = thread_pool.get_thread().get_info_detail()

    t = {
        'alive': alive,
        'result': rst,
        'filename': thread_pool.get_thread().get_video_name(),
        'detail': detail,
        'summary': thread_pool.get_thread().analysis_result()
    }
    return jsonify(t)


@app.route('/stop', methods=['post'])
def stop():
    thread_pool.get_thread().stop()
    return 'stop'


@app.route('/user')
def user():
    if len(session) == 0:
        return redirect('/login')
    return redirect('/widget/account.html')


if __name__ == '__main__':
    app.run()
