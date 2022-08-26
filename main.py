from certificateParser import parse_coursera_url, parse_stepik_url
from bson import json_util
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from jsonConvert import json_convert, color_calc, timeline_parse
from flask import render_template, make_response, redirect, url_for, flash, session
from flask_cors import CORS
from rchilli import rchilli_parse, skill_search, skill_autocomplete, job_autocomplete, job_search
from mongodb import *
from analytics import *
import pdfkit
from werkzeug.utils import secure_filename
import os
import re
from forms import FormRegister, FormLogin

# Flask config
app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('FLASK_SECRET_KEY')
app.config['JSON_AS_ASCII'] = False
app.config['UPLOAD_FOLDER'] = './static/data/cv/'
app.config['UPLOAD_IMAGE_FOLDER'] = './static/data/img/'
app.config['SECURITY_UNAUTHORIZED_VIEW'] = '/login'
app.config.from_object(__name__)
CORS(app)

client = MongoClient('localhost', 27017)
db = client['DPM']
collection = db['users']
collection_dataset = db['Datasets']

login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message = 'Please log in to access the site'
login_manager.login_message_category = 'success'


@app.errorhandler(404)
@app.errorhandler(401)
def page_not_found(error):
    return render_template('notfound.html')


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

    return redirect(url_for('index'))


# Uploading CV in storage
@app.route('/uploader', methods=['GET', 'POST'])
def upload_file():
    file_name, cur_user = "", ""

    if request.method == 'POST':
        try:
            cv_link = request.form['link']

            if cv_link != '':
                try:
                    file_name = f'hhCv_{summary_cv_count()}.pdf'
                    save_pdf(cv_link, file_name)

                    increment_cv_count()
                except Exception as e:
                    print(e)
            else:
                file = request.files['file']
                file_name = secure_filename(file.filename)

                # Локально сохраняем копию CV
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], file_name))

                increment_cv_count()

            cur_user_id = session['id']

            cur_user = find_record('Id', cur_user_id)

            if cur_user is not None:
                rchilli_data = rchilli_parse(file_name)
                json_data = json_convert(rchilli_data)
                timeline_events = timeline_parse(rchilli_data)

                update_record('Id', cur_user_id, 'jsondata', json_data)
                update_record('Id', cur_user_id, 'rchillidata', rchilli_data)
                update_record('Id', cur_user_id, 'timelineEvents', timeline_events)



        except Exception as e:
            print(e)    

    return redirect(url_for('index'))

# Основная страница
@app.route('/')
@app.route('/me')
@login_required
def index():
    if session is None or 'id' not in session.keys():
        logout_user()
        return redirect(url_for('login'))

    # cur_user_id = session['id']
    # cur_user = find_record('Id', cur_user_id)

    return render_template('index.html', title='Digital Professional Me', userName=current_user.name)


# Avatar
@app.route('/getAvatar', methods=['GET', 'POST'])
# @login_required
def get_avatar():
    # print(current_user)
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


# Json для Timeline
@app.route('/getTimelineJson', methods=['GET', 'POST'])
# @login_required
def get_timeline_json():
    cur_user_id = str(request.args.get('id'))
    cur_user = find_record('Id', cur_user_id)

    return jsonify(cur_user.timeline_events)


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

# Registration
@app.route('/register', methods=['GET', 'POST'])
def register():
    form = FormRegister()

    if form.validate_on_submit():
        user_db = find_record('email', form.email.data)

        if user_db is None:
            create_record(form)
            flash('You have successfully registered', 'success')
            return redirect(url_for('login'))
        else:
            flash('User with such email is already exists', 'error')

    return render_template('register.html', form=form)


# Авторизация
@app.route('/login', methods=['POST', 'GET'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))

    form = FormLogin()
    if form.validate_on_submit():
        user_db = find_record('email', form.email.data)

        if user_db is not None and user_db.password == form.password.data:
            resp = make_response(redirect(url_for('index')))

            resp.set_cookie(key='id', value=user_db.Id)
            session['id'] = user_db.Id

            checkbox = True if form.remember.data else False

            login_user(user_db, remember=checkbox)
            return resp

        flash("Wrong password or login", 'error')

    return render_template('login.html', form=form)


# Деавторизация
@app.route('/logout')
@login_required
def logout():
    logout_user()
    resp = make_response(redirect(url_for('login')))

    resp.delete_cookie(key='id')
    session.pop('id', default=None)

    flash("You logged out of the profile", 'success')

    return resp


def save_pdf(url, file_name):
    pdfkit.from_url(url, f'./static/data/cv/{file_name}')


@app.route('/changeSkillState', methods=['POST', 'GET'])
def change_skill_state():
    cur_user_id = session['id']
    #skill_name = str(request.args.get('skillName'))

    skill_name = request.get_json()['skill']
    disable_skill(cur_user_id, skill_name)
    return '200'
    #return redirect(url_for('index'))


@app.route('/skillInputAutocomplete')
def show_input_options():
    return skill_autocomplete(f"{request.args.get('skillName')}")


@app.route('/jobInputAutocomplete')
def show_jobs():
    return job_autocomplete(f"{request.args.get('jobName')}")


@app.route('/findJob')
def find_jobs():
    cur_user_id = session['id']

    job_name = str(request.args.get('jobName'))
    job_deadline = str(request.args.get('deadline'))

    add_timeline_evidence_event(cur_user_id, job_name, job_deadline)
    resp = job_search(job_autocomplete(job_name))

    ownend_skills = get_owned_skills(cur_user_id)
    req_skills = []

    for skill in resp:
        req_skills.append(skill['Skill'])

    set_owned_skills = set(ownend_skills)
    set_req_skills = set(req_skills)
    print('ow', set_owned_skills)
    print('req', set_req_skills)

    set_different = set_req_skills - set_owned_skills
    print(set_different)

    courses = get_courses(set_different)

    return json.loads(json_util.dumps({
        'offeredCourses': courses,
        'gapSkills': set_different
    }))


@app.route('/parseCertificate')
def parse_certificate():
    url = str(request.args.get('url'))
    resp = {}
    if 'coursera.org' in url:
        resp = parse_coursera_url(url)
    elif 'stepik.org' in url:
        resp = parse_stepik_url(url)
    #elif 'ude.my' in url or 'udemy.com' in url:
    #    resp = parse_udemy_url(url)

    add_cerificate_event(current_user.Id, resp['courseName'], resp['date'], resp['url'], resp['userName'])
    return resp


@app.route('/findSkill')
def find_skill():
    skill_name = str(request.args.get('skillName'))
    cur_user_id = session['id']
    cur_user_data = find_record('Id', cur_user_id).jsondata[0]

    resp = skill_search(skill_name)

    ontoloty = resp['ontology']

    flag1 = False
    flag2 = False
    filling = ''

    for grandParentSkillType in cur_user_data['children']:
        if ontoloty.split('>')[0] == grandParentSkillType['name']:
            flag1 = True

            for parentSkillType in grandParentSkillType['children']:
                if ontoloty.split('>')[1] == parentSkillType['name']:  # Найден Parent, GrandParent
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

    if filling != '':
        resp['filling'] = filling
    else:
        resp['filling'] = '#4188D2'

    update_record('Id', cur_user_id, 'jsondata', [cur_user_data])

    return resp


#@app.route('/saveCertificate')
#def save_certificate():
    #cur_user_id = session['id']
    #date = str(request.args.get('date'))
    #name = str(request.args.get('name'))
    #add_cerificate_event(cur_user_id, name, date)
    #return '200'


if __name__ == "__main__":
    app.run(debug=True, port=5000, host="0.0.0.0")
    #parse_udemy_url('https://www.udemy.com/certificate/UC-7PDXUTCH/')

    # print(parse_coursera_url('https://www.coursera.org/account/accomplishments/verify/5B8JXGAHLS2Y'))
    # dataset = collection_dataset.find()
    # skill_set_res = set()
    # for skill_set in dataset:
    #
    #     for skill in skill_set['skills']:
    #         skill_set_res.add(skill)
    # #
    # print(skill_set_res)
