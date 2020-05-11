import datetime
import hashlib
from flask import Blueprint, session, request, url_for, render_template, jsonify
from werkzeug.utils import redirect
from db.mysqlpool import Mysql

login_api = Blueprint('login_api', __name__)

mysql = Mysql()


@login_api.route('/login', methods=['GET', 'POST'])
def login():
    return redirect('/login/index.html')


@login_api.route('/signin', methods=['POST'])
def sign_in():
    name = request.form['username']
    pwd = md5(request.form['pwd'])
    result = mysql.getOne('select pwd from user_login where username = %s', [name])
    if not result:
        return '103'
    expected = result['pwd']
    if pwd == expected:
        session['username'] = name
        return '0'
    else:
        return '102'


@login_api.route('/signup', methods=['POST'])
def sign_up():
    name = request.form['username']
    pwd = md5(request.form['pwd'])
    email = request.form['email']
    date = getLastDate()
    try:
        mysql.insertOne('insert into user_login (username,pwd,email,date) values (%s,%s,%s,%s)', [name, pwd, email, date])
        mysql.end()
        return "1"
    except Exception:
        return "2"


@login_api.route('/c_user')
def get_current_user():
    if 'username' in session:
        return session['username']
    return False


@login_api.route('/signout')
def sign_out():
    session.pop('username', None)
    return redirect('/')


@login_api.route('/account')
def get_account_data():
    if 'username' not in session:
        return redirect('/login')
    sql = 'select filename as f, result as t from user_files where username = %s;'
    username = session['username']
    files = mysql.getAll(sql, [username])
    sql = 'select * from user_last_file where username = %s;'
    last = mysql.getOne(sql, [username])
    sql = 'select count(*) as count, date from user_files where username = %s group by date;'
    group_date = mysql.getAll(sql, [username])
    _2020 = datetime.date(2020, 1, 1)
    if group_date:
        for i in range(len(group_date)):
            group_date[i]["days"] = (group_date[i]["date"] - _2020).days
    t = {
        'username': username,
        'files': files,
        'last_file': last,
        'group_date': group_date
    }
    sql = "select result from user_files where username = %s and filename in ( " \
          "select filename from user_last_file where username = %s);"

    last_result = mysql.getOne(sql, [username, username])
    if last_result:
        t['last_file']['result'] = last_result["result"]
    return jsonify(t)


def md5(string):
    return hashlib.new('md5', string).hexdigest()


def getLastDate():
    return datetime.datetime.now().strftime('%Y%m%d')