import sqlite3
import os
from flask import Flask, render_template, request, g, flash, make_response, redirect, url_for
from FDataBase import FDataBase
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import LoginManager, login_user, login_required
from UserLogin import UserLogin

# Конфигурация
DATABASE = '/tmp/main.db'
DEBUG = True
SECRET_KEY = '1498b405c48e5daf56eef86bec68f8d9ed627376'

app = Flask(__name__)
app.config.from_object(__name__)
app.config.update(dict(DATABASE=os.path.join(app.root_path, 'main.db')))

login_manager = LoginManager(app)


@login_manager.user_loader
def load_user(user_id):
    print("load_user")
    return UserLogin().fromDB(user_id, dbase)


dbase = None


# Установка соединения с БД перед выполнением запросов
@app.before_request
def before_request():
    global dbase
    db = get_db()
    dbase = FDataBase(db)


# Разрыв соединения с БД, если оно было установлено
@app.teardown_appcontext
def close_db(error):
    if hasattr(g, 'link_db'):
        g.link_db.close()


# Соединение с БД
def connect_db():
    conn = sqlite3.connect(app.config['DATABASE'])
    conn.row_factory = sqlite3.Row
    return conn


# Создание БД
def create_db():
    db = connect_db()
    with app.open_resource('sq_db.sql', mode="r") as f:
        db.cursor().executescript(f.read())
    db.commit()
    db.close()


# Соединение с БД, если оно еще не было установлено
def get_db():
    if not hasattr(g, 'link_db'):
        g.link_db = connect_db()
    return g.link_db


#@app.route('/')
#@login_required
#def index():
#    # return render_template('index.html')
#    return "Main Page"


# Регистрация
@app.route('/register', methods=['GET', 'POST'])
def addUser():
    if request.method == 'POST':
        if len(request.form['name']) > 4 and len(request.form['email']) > 2 \
                and 20 >= len(request.form['password']) >= 6 and request.form['password'] == request.form['password2']:
            hash = generate_password_hash(request.form['password'])
            res = dbase.addUser(request.form['name'], request.form['email'], hash)
            if res:
                flash("Вы успешно зарегистрировались", category='success')
                return redirect(url_for('login'))
            else:
                flash("Ошибка добавления в БД", category='error')
        else:
            flash("Неверно заполнены поля", category='error')

    return render_template('register.html', title='Registration')


# Авторизация
@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        user = dbase.getUserByEmail(request.form['email'])
        if user and check_password_hash(user['password'], request.form['password']):
            userlogin = UserLogin().create(user)
            login_user(userlogin)
            return redirect(url_for('index'))

        flash("Неверная пара логин/пароль", 'error')

    return render_template('login.html', title='Authorization')


# Авторизация
# @app.route('/login')
# def login():
#    log = ""
#    if request.cookies.get('logged'):
#        log = request.cookies.get('logged')
#    res = make_response(f"<h1>Форма авторизации</h1><p>logged: {log}")
#    res.set_cookie('logged', 'yes', 30 * 24 * 3600)
#    return res


# Дезавторизация
# @app.route('/logout')
# def logout():
#    res = make_response('<p> Вы больше не авторизованы!</p>')
#    res.set_cookie('logged', "", 0)
#    return res

# create_db()

#if __name__ == '__main__':
#    app.run(debug=True, port=80)
