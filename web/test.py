# coding=utf-8
import sys
import os
import torch
from torch.nn import functional as F
from flask import Flask, render_template, flash, request
from werkzeug.utils import secure_filename

from data.sliding import sliding
from st_gcn.utils import get_action_name

from model import gcn
from web.eval_thread import EvalThread

reload(sys)
sys.setdefaultencoding('utf-8')

app = Flask(__name__, static_url_path='')
app.secret_key = 'random string'

eval_thread = EvalThread()


@app.route('/')
def index():
    flash('info')
    return render_template('index.html')


@app.route('/upload')
def upload():
    return render_template('upload.html')


@app.route('/uploader', methods = ['POST'])
def upload_file():
    f = request.files['file']
    filename = secure_filename(f.filename)
    f.save(filename)
    abs_path = os.path.abspath('.') + "/" + filename
    eval_thread.set_path(abs_path)
    eval_thread.start()
    return render_template("uploader.html", content=abs_path)


@app.route('/info')
def info():
    info = eval_thread.get_info()
    alive = eval_thread.is_alive()
    return render_template("fresh.html", content=info, fresh=alive)


@app.route('/stop', methods = ['post'])
def stop():
    eval_thread.stop()
    return 'stop'

@app.route('/user/<user>')
def hello_world(user):
    print user
    return '<h1>Hello World</h1>'


if __name__ == '__main__':
    app.run()
