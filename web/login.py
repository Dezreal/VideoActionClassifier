import datetime
import hashlib
from flask import Blueprint, session, request, url_for, render_template, abort
from werkzeug.utils import redirect
from db.mysqlpool import Mysql

login_api = Blueprint('login_api', __name__)

mysql = Mysql()


@login_api.route('/login', methods=['GET', 'POST'])
def login():
    return render_template('login.html')
   #  if request.method == 'POST':
   #      session['username'] = request.form['username']
   #      return redirect(url_for('login_api.users'))
   #  return '''
   #
   # <form action = "" method = "post">
   #    <p><input type = text name = username></p>
   #    <p><input type = submit value = Login></p>
   # </form>
   #
   # '''


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
        count = mysql.insertOne('insert into user_login (username,pwd,email,date) values (%s,%s,%s,%s)', [name, pwd, email, date])
        mysql.end()
        return "1"
    except Exception as e:
        abort(400)


@login_api.route('/c_user')
def get_current_user():
    if 'username' in session:
        return session['username']
    return ""


@login_api.route('/signout')
def sign_out():
    session.pop('username', None)
    return redirect('/')


@login_api.route('/users')
def users():
    if 'username' in session:
        username = session['username']
        return 'Logged in as '+        username + '<br>' + "<b><a href = '/logout'>click here to log out</a></b>"


    return "You are not logged in <br><a href = '/login'></b>" +            "click here to log in</b></a>"


def md5(string):
    return hashlib.new('md5', string).hexdigest()


def getLastDate():
    return datetime.datetime.now().strftime('%Y%m%d')