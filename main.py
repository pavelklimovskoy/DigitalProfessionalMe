import sqlite3
import os
from flask import Flask, jsonify, request, send_from_directory, render_template, abort, json, make_response, flash, \
    session, redirect, url_for, g
from flask_cors import CORS, cross_origin
import codecs
from ParseModulesHH import *
from FDataBase import FDataBase
from LoadModules import loadPage
from Logger import log
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from UserLogin import UserLogin


# Конфигурация
DATABASE = 'main.db'
#DEBUG = True
#SECRET_KEY = '1498b405c48e5daf56eef86bec68f8d9ed627376'

app = Flask(__name__)
app.config['SECRET_KEY'] = '1a2d5a33a7f02c888ff796a9f5f422bf96f4eb1c '
app.config['JSON_AS_ASCII'] = False
app.config.from_object(__name__)
#app.config.update(dict(DATABASE=os.path.join(app.root_path, 'main.db')))
CORS(app)

login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message = "Log in to access private pages"
login_manager.login_message_category = 'success'

dbase = None


@login_manager.user_loader
def load_user(user_id):
    print("load_user")
    return UserLogin().fromDB(user_id, dbase)


# Установка соединения с БД перед выполнением запросов
@app.before_request
def before_request():
    global dbase
    db = get_db()
    dbase = FDataBase(db)


# Получение загруженной страницы по id
@app.route('/templates/<id>')
def pageFormHH(id):
    filename = id + ".html"
    #print(filename)
    return render_template(filename)


@app.after_request
def apply_caching(response):
    response.headers['X-Frame-Options'] = 'ALLOW'
    return response


# Основная страница
@app.route('/')
@login_required
def index():
    return render_template('index.html', title='Timeline')


# Выдача скриптов
# @app.route('/script')
# def renderJS():
#    return render_template('script.js')


# Профиль
# @app.route('/profile/<username>')
# def profile(username):
#    if 'userLogged' not in session or session['userLogged'] != username:
#        abort(401)
#    return f"Профиль пользователя {username}!"


# Смена поискового слова
@app.route('/newFindWord/<newWord>', methods=['GET'])
def changeFindWord(newWord):
    if request.method == 'GET':
        file = open("FindWord.txt", "w")
        file.write(newWord)
        file.close()
        return "Word changed"


# Получение поискового слова
@app.route('/getFindWord', methods=['GET'])
def getFindWord():
    if request.method == 'GET':
        file = open("FindWord.txt")
        word = file.read()
        file.close()
        return word


# Получение старницы для парсинга
@app.route('/getPageForParse/<findWord>', methods=['GET'])
def pageForParse(findWord):
    if request.method == 'GET':
        resList = parseList(findWord)
        return resList


# Получение старницы для парсинга
@app.route('/reqForParse/<id>', methods=['GET'])
def reqForParse(id):
    if request.method == 'GET':
        filename = "templates/" + id + ".html"

        url = "https://hh.ru/resume/" + id

        response = urllib.request.urlopen(url)
        webContent = response.read().decode('utf-8')

        f = codecs.open(filename, "w", 'utf-8')
        f.write(webContent)
        f.close()

        return "https://hh.ru/resume/" + id + " загружено"


# Выдача иконки
@app.route("/favicon.ico")
def favicon():
    log('favicon')
    return send_from_directory(os.path.join(app.root_path, 'static'), 'jpg/favicon.ico',
                               mimetype='image/vnd.microsoft.icon')


# Получение Json-файла
@app.route('/jsonData/<id>', methods=['GET'])
def jsonData(id):
    if request.method == 'GET':
        return jsonify(dictFromUrl(id))


# Обработка несуществующих страниц
@app.errorhandler(404)
def pageNotFound(error):
    return render_template('page404.html', title='Page not found'), 404


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


# Регистрация
@app.route('/register', methods=['GET', 'POST'])
def register():
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
    if current_user.is_authenticated:
        return redirect(url_for('profile'))

    if request.method == 'POST':
        user = dbase.getUserByEmail(request.form['email'])
        if user and check_password_hash(user['password'], request.form['password']):
            userlogin = UserLogin().create(user)
            rm = True if request.form.get('remainme') else False
            login_user(userlogin, remember=rm)
            return redirect(request.args.get('next') or url_for('profile'))

        flash("Неверная пара логин/пароль", 'error')

    return render_template('login.html', title='Authorization')


# Деавторизация
@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash("Вы вышли из аккаунта", 'success')
    return redirect(url_for('login'))


# Профиль авторизованного пользователя
@app.route('/profile')
@login_required
def profile():
    return f"""<p><a href = "{url_for('logout')}"> Выйти из профиля</a> <p> user info: {current_user.get_id()} <p><a href="http://127.0.0.1/">Тестирование</a></p>"""


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


if __name__ == '__main__':
    app.run(debug=False, port=80)