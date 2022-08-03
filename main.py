import os
from flask import Flask, jsonify, request, send_from_directory, render_template, json, make_response, redirect, \
    url_for, flash, send_file, Response, session
from pymongo import MongoClient
from flask_cors import CORS, cross_origin
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
import codecs
from jsonConvert import json_convert
from rchilli import rchilli_parse, skill_search, skill_autocomplete
from mongodb import *
from analytics import *
import pdfkit
from werkzeug.utils import secure_filename
import os

# Flask config
app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('FLASK_SECRET_KEY')
app.config['JSON_AS_ASCII'] = False
app.config['UPLOAD_FOLDER'] = './static/data/cv/'
app.config['UPLOAD_IMAGE_FOLDER'] = './static/data/img/'
app.config.from_object(__name__)
CORS(app)

client = MongoClient('localhost', 27017)
db = client['DPM']
collection = db['users']

login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message = 'Please log in to access the site'
login_manager.login_message_category = 'success'


@login_manager.user_loader
def load_user(userId):
    return find_record('Id', userId)


@app.after_request
def apply_caching(response):
    response.headers['X-Frame-Options'] = 'ALLOW'
    return response


# Загрузка аватара на сервер
@app.route('/upload_avatar', methods=['GET', 'POST'])
@login_required
def upload_avatar():
    # curUserId = str(request.cookies.get('id'))
    curUserId = session['id']
    curUser = find_record('Id', curUserId)
    avatar = request.files['avatar']
    avatarName = avatar.filename
    image_id = summary_image_count()

    if request.method == 'POST':
        if avatar is not None:
            if avatarName[-3:] in ["jpg", "png"]:
                file_name = f"{avatarName[:-4]}-id-{image_id}.{avatarName[-3:]}"

                # Локально сохраняем аватар
                avatar.save(os.path.join(app.config['UPLOAD_IMAGE_FOLDER'], file_name))

                increment_image_count()
                update_record('Id', curUserId, 'avatar', file_name)

    return render_template('index.html', title='Digital Professional Me', userName=curUser.name)


# Загрузка CV на сервер
@app.route('/uploader', methods=['GET', 'POST'])
def upload_file():
    global fname, curUser
    if request.method == 'POST':
        cvLink = request.form['link']

        if cvLink != '':
            try:
                fname = f'hhCv_{summary_cv_count()}.pdf'
                save_pdf(cvLink, fileName=fname)

                increment_cv_count()
            except:
                print("Error")
        else:
            file = request.files['file']
            fname = secure_filename(file.filename)
            # Локально сохраняем копию CV
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], fname))
        # print(fname)

        # curUserId = str(request.cookies.get('id'))
        curUserId = session['id']

        # print("Hello from updating + CurUsId= ", curUserId)
        curUser = find_record('Id', curUserId)
        # print("Hello from updating + CurUs= ", curUser)
        if curUser is not None:
            rchilliData = rchilli_parse(fileName=fname)
            jsonData = json_convert(data=rchilliData)

            # print(rchilliData)
            # print(jsonData)

            update_record('Id', curUserId, 'jsondata', jsonData)
            update_record('Id', curUserId, 'rchillidata', rchilliData)

            # update_record(curUser, jsonData, rchilliData)

    # print(request.cookies.get('id'))
    return render_template('index.html', title='Digital Professional Me', userName=curUser.name)


# Основная страница
@app.route('/')
@app.route('/me')
@login_required
def index():
    if session is None or 'id' not in session.keys():
        logout_user()
        return render_template('login.html')

    cur_user_id = session['id']

    cur_user = find_record('Id', cur_user_id)

    return render_template('index.html', title='Digital Professional Me', userName=cur_user.name)


# Avatar
@app.route('/getAvatar', methods=['GET', 'POST'])
@login_required
def get_avatar():
    cur_user_id = str(request.args.get('id'))
    cur_user = find_record('Id', cur_user_id)

    return cur_user.avatar


# Json для Sunburst Chart
@app.route('/getChartJson', methods=['GET', 'POST'])
# @login_required
def get_chart_json():
    cur_user_id = str(request.args.get('id'))
    cur_user = find_record('Id', cur_user_id)

    return jsonify(cur_user.jsondata)


# Rchilli Json
@app.route('/getRchilliJson', methods=['GET', 'POST'])
def get_rchilli_json():
    cur_user_id = str(request.args.get('id'))
    cur_user = find_record('Id', cur_user_id)

    return jsonify(cur_user.rchillidata)


# Cтраница с информацией
@app.route('/about')
def about_us():
    return render_template('aboutus.html', title='About us')


# Регистрация
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        if len(request.form['name']) > 4 and len(request.form['email']) > 2 \
                and 20 >= len(request.form['password']) >= 6 and request.form['password'] == request.form['password2']:
            # hash = generate_password_hash(request.form['password'])
            # res = dbase.addUser(request.form['name'], request.form['email'], request.form['password'])

            # Проверка на существование пользователя в БД
            curUser = find_record('email', str(request.form['email']))
            if curUser is None:
                create_record(request)

                flash("You have successfully registered", category='success')
                return redirect(url_for('login'))
            else:
                # print("Уже есть в базе ", curUser.Id)
                flash("Error adding to the database", category='error')
        else:
            # print("Не совпали данные")
            flash("The fields are filled in incorrectly", category='error')
    return render_template('register.html')


# Авторизация
@app.route('/login', methods=['POST', 'GET'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))

    if request.method == 'POST':
        curUser = find_record('email', str(request.form['email']))

        if curUser is not None and curUser.password == request.form['password']:
            rm = True if request.form.get('remainme') else False

            resp = make_response(render_template('index.html', userName=curUser.name))

            resp.set_cookie(key='id', value=str(curUser.Id))
            session['id'] = curUser.Id

            login_user(curUser, remember=rm)
            # return redirect(request.args.get('next') or url_for('index'))
            return resp

        flash("Wrong password or login", 'error')

    return render_template('login.html')


# Деавторизация
@app.route('/logout')
@login_required
def logout():
    logout_user()

    resp = make_response(render_template('login.html'))

    resp.delete_cookie(key='id')
    session.pop('id', default=None)

    flash("You logged out of the profile", 'success')
    return resp


def save_pdf(url, file_name):
    pdfkit.from_url(url, f'./static/data/cv/{file_name}')


@app.route('/changeSkillState')
def change_skill_state():
    cur_user_id = session['id']
    skill_name = str(request.args.get('skillName'))
    cur_user = disable_skill(cur_user_id, skill_name)

    return render_template('index.html', title='Digital Professional Me', userName=cur_user.name)


@app.route('/InputAutocomplete')
def show_input_options():
    skill_name = str(request.args.get('skillName'))
    return skill_autocomplete(skill_name)


@app.route('/findSkill')
def find_skill():
    skill_name = str(request.args.get('skillName'))

    return skill_search(skill_name)


if __name__ == "__main__":
    app.run(debug=True, port=5000, host="0.0.0.0")
