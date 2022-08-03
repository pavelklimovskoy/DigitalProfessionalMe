from flask_login import LoginManager, login_user, login_required, logout_user, current_user
import codecs
from jsonConvert import json_convert, color_calc
from flask import render_template, make_response, redirect, url_for, flash, session
from flask_cors import CORS
from jsonConvert import json_convert
from rchilli import rchilli_parse, skill_search, skill_autocomplete
from mongodb import *
from analytics import *
import pdfkit
from werkzeug.utils import secure_filename
import os
import re

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
def load_user(user_id):
    return find_record('Id', user_id)


@app.after_request
def apply_caching(response):
    response.headers['X-Frame-Options'] = 'ALLOW'
    return response


# Загрузка аватара на сервер
@app.route('/upload_avatar', methods=['GET', 'POST'])
@login_required
def upload_avatar():
    cur_user_id = session['id']
    cur_user = find_record('Id', cur_user_id)
    avatar = request.files['avatar']
    avatar_name = avatar.filename
    image_id = summary_image_count()

    if request.method == 'POST':
        if avatar is not None:
            if avatar_name[-3:] in ["jpg", "png"]:
                file_name = f"{avatar_name[:-4]}-id-{image_id}.{avatar_name[-3:]}"

                # Локально сохраняем аватар
                avatar.save(os.path.join(app.config['UPLOAD_IMAGE_FOLDER'], file_name))

                increment_image_count()
                update_record('Id', cur_user_id, 'avatar', file_name)

    return render_template('index.html', title='Digital Professional Me', userName=cur_user.name)


# Uploading CV in storage
@app.route('/uploader', methods=['GET', 'POST'])
def upload_file():
    file_name, cur_user = "", ""

    if request.method == 'POST':
        cv_link = request.form['link']

        if cv_link != '':
            try:
                file_name = f'hhCv_{summary_cv_count()}.pdf'
                save_pdf(cv_link, file_name=file_name)

                increment_cv_count()
            except Exception as e:
                print(e)
        else:
            file = request.files['file']
            file_name = secure_filename(file.filename)

            # Локально сохраняем копию CV
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], file_name))

        cur_user_id = session['id']

        cur_user = find_record('Id', cur_user_id)

        if cur_user is not None:
            rchilli_data = rchilli_parse(fileName=file_name)
            json_data = json_convert(data=rchilli_data)

            update_record('Id', cur_user_id, 'jsondata', json_data)
            update_record('Id', cur_user_id, 'rchillidata', rchilli_data)

    # Переписать на редирект
    return render_template('index.html', title='Digital Professional Me', userName=cur_user.name)


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


# About page
@app.route('/about')
def about_us():
    return render_template('aboutus.html', title='About us')


# Password validation with regEx
def password_correct(data: str) -> bool:
    """
    Conditions for a valid password are:
        Should have at least one number.
        Should have at least one uppercase and one lowercase character.
        Should have at least one special symbol.
        Should be between 6 to 20 characters long.
    :param data:
    :return:
    """
    regex = "^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*#?&])[A-Za-z\d@$!#%*?&]{6,20}$"
    pat = re.compile(regex)

    if re.search(pat, data):
        return True
    else:
        flash("Wrong password format", category='error')
        return False


# Email validation
def email_correct(email: str) -> bool:
    """
    Validation email with regEx
    :param email:
    :return:
    """
    regex = '^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$'

    if re.search(regex, email):
        return True
    else:
        flash("Wrong email format", category='error')
        return False


# User's fullname validation
def name_correct(data: str) -> bool:
    fullname = data.split()

    check_count = len(fullname) == 2
    check_name = 2 <= len(fullname[0]) <= 35
    check_surname = 2 <= len(fullname[1]) <= 35

    if check_name and check_surname and check_count:
        return True
    else:
        flash("Wrong fullname format", category='error')
        return False


def password_equal(str1, str2) -> bool:
    if str1 == str2:
        return True
    else:
        flash("Passwords not equal", category='error')
        return False


def input_form_correct(input_form) -> bool:

    res = name_correct(input_form['name'])
    res &= password_correct(input_form['password'])
    res &= email_correct(input_form['email'])
    res &= password_equal(input_form['password'], input_form['password2'])

    return res


# Registration
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        if input_form_correct(request.form):

            # Проверка на существование пользователя в БД
            cur_user = find_record('email', str(request.form['email']))
            if cur_user is None:
                create_record(request)

                flash("You have successfully registered", category='success')
                return redirect(url_for('login'))
            else:
                flash("Error adding to the database", category='error')
        else:
            flash("The fields are filled in incorrectly", category='error')
    return render_template('register.html')


# Авторизация
@app.route('/login', methods=['POST', 'GET'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))

    if request.method == 'POST':
        cur_user = find_record('email', str(request.form['email']))

        if cur_user is not None and cur_user.password == request.form['password']:
            rm = True if request.form.get('remainme') else False

            resp = make_response(render_template('index.html', userName=cur_user.name))

            resp.set_cookie(key='id', value=str(cur_user.Id))
            session['id'] = cur_user.Id

            login_user(cur_user, remember=rm)

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
    return skill_autocomplete(f"{request.args.get('skillName')}")


@app.route('/findSkill')
def find_skill():
    return skill_search(f"{request.args.get('skillName')}")
    skill_name = str(request.args.get('skillName'))
    cur_user_id = session['id']
    cur_user_data = find_record('Id', cur_user_id).jsondata[0]

    resp = skill_search(skill_name)

    ontoloty = resp['ontology']

    flag1 = False
    flag2 = False

    for grandParentSkillType in cur_user_data['children']:
        if ontoloty.split('>')[0] == grandParentSkillType['name']:
            flag1 = True

            for parentSkillType in grandParentSkillType['children']:
                if ontoloty.split('>')[1] == parentSkillType['name']: # Найден Parent, GrandParent
                    flag2 = True

                    shortName = ontoloty.split('>')[-1]
                    if len(shortName) > 6:
                        shortName = f'{ontoloty.split(">")[-1][:6]}...'

                    if resp['type'] == 'SoftSkill':
                        filling = '#FFB240'
                    else:
                        filling = '#4188D2'

                    skill = {
                        'name': ontoloty.split('>')[-1],
                        'id': resp['type'],
                        'value': '1',
                        'enabled': True,
                        'shortName': shortName,
                        'fill': filling,
                        'grandParent': grandParentSkillType['name'],
                        'parent': parentSkillType['name']
                    }
                    parentSkillType['children'].append(skill)
                    break

            if flag2 is False:  # Parent не найден, только GrandParent
                parentSkillType = {
                    'name': ontoloty.split('>')[1],
                    'id': resp['type'],
                    'value': '1',
                    'fill': color_calc(1, resp['type']),
                    'parent': grandParentSkillType['name'],
                    'children': []
                }

                shortName = ontoloty.split('>')[-1]
                if len(shortName) > 6:
                    shortName = f'{ontoloty.split(">")[-1][:6]}...'

                if resp['type'] == 'SoftSkill':
                    filling = '#FFB240'
                else:
                    filling = '#4188D2'

                skill = {
                    'name': ontoloty.split('>')[-1],
                    'id': resp['type'],
                    'value': '1',
                    'enabled': True,
                    'shortName': shortName,
                    'fill': filling,
                    'grandParent': grandParentSkillType['name'],
                    'parent': parentSkillType['name']
                }
                parentSkillType['children'].append(skill)
                grandParentSkillType['children'].append(parentSkillType)

    if flag1 is False:  # Не найдено ни GrandParent, ни Parent
        grandParentSkillType = {
            'name': ontoloty.split('>')[0],
            'id': resp['type'],
            'value': '1',
            'fill': color_calc(1, resp['type']),
            'parent': 'Me',
            'children': []
        }

        parentSkillType = {
            'name': ontoloty.split('>')[1],
            'id': resp['type'],
            'value': '1',
            'fill': color_calc(1, resp['type']),
            'parent': grandParentSkillType['name'],
            'children': []
        }

        shortName = ontoloty.split('>')[-1]
        if len(shortName) > 6:
            shortName = f'{ontoloty.split(">")[-1][:6]}...'

        if resp['type'] == 'SoftSkill':
            filling = '#FFB240'
        else:
            filling = '#4188D2'

        skill = {
            'name': ontoloty.split('>')[-1],
            'id': resp['type'],
            'value': '1',
            'enabled': True,
            'shortName': shortName,
            'fill': filling,
            'grandParent': grandParentSkillType['name'],
            'parent': parentSkillType['name']
        }
        parentSkillType['children'].append(skill)
        grandParentSkillType['children'].append(parentSkillType)
        cur_user_data['children'].append(grandParentSkillType)

    update_record('Id', cur_user_id, 'jsondata', [cur_user_data])

    return resp


if __name__ == "__main__":
    app.run(debug=True, port=5000, host="0.0.0.0")
