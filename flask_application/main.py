from certificateParser import parse_coursera_url, parse_stepik_url
from bson import json_util
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from jsonConvert import json_convert, color_calc, timeline_parse
from flask import Flask, request, jsonify, render_template, make_response, redirect, url_for, flash, session
from flask_cors import CORS
from flask import send_from_directory
from rchilli import rchilli_parse, skill_search, skill_autocomplete, job_autocomplete, job_search
from mongodb import *
from analytics import *
import pdfkit
from werkzeug.utils import secure_filename
import os
import json
import re
from forms import FormRegister, FormLogin
from waitress import serve

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
collection_users = db['users']
collection_dataset = db['Datasets']
collection_skills_dataset = db['SkillsDataset']
collection_feedback = db['Feedback']

login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message = 'Please log in to access the site'
login_manager.login_message_category = 'success'


@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static/image'),
                               'favicon.ico', mimetype='image/vnd.microsoft.icon')

@app.errorhandler(404)
@app.errorhandler(401)
def page_not_found(error):
    return render_template('notfound.html')


@login_manager.user_loader
def load_user(user_id):
    return find_record('id', user_id)


@app.after_request
def apply_caching(response):
    response.headers['X-Frame-Options'] = 'ALLOW'
    return response


# Загрузка аватара на сервер
@app.route('/upload_avatar', methods=['GET', 'POST'])
@login_required  #
def upload_avatar():
    avatar = request.files['avatar']
    avatar_name = avatar.filename
    image_id = summary_image_count()

    if request.method == 'POST':
        if avatar is not None:
            if avatar_name[-3:] in ['jpg', 'png']:
                file_name = f'{avatar_name[:-4]}-id-{image_id}.{avatar_name[-3:]}'

                # Локально сохраняем аватар
                avatar.save(os.path.join(app.config['UPLOAD_IMAGE_FOLDER'], file_name))

                increment_image_count()
                update_record('id', current_user.id, 'avatar', file_name)

    return redirect(url_for('index'))


# Uploading CV in storage
@app.route('/uploader', methods=['GET', 'POST'])
@login_required
def upload_file():
    if request.method == 'POST':
        try:
            cv_link = request.form['link']
            file_name = ''
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

            cur_user = find_record('id', current_user.id)

            if cur_user is not None:
                rchilli_data = rchilli_parse(file_name)
                json_data, skills_array = json_convert(rchilli_data)
                timeline_events = timeline_parse(rchilli_data)

                update_record('id', current_user.id, 'language',
                              rchilli_data['ResumeParserData']['ResumeLanguage']['LanguageCode'])
                update_record('id', current_user.id, 'jsondata', json_data)
                update_record('id', current_user.id, 'rchillidata', rchilli_data)
                update_record('id', current_user.id, 'timelineEvents', timeline_events)
                return '200'
        except Exception as e:
            print(e)

    return redirect(url_for('index'))

# Новая страница логинки
@app.route('/newlogin')
def newLogin():
    return render_template('login_new.html', title='Digital Professional Me')


# Основная страница
@app.route('/')
@app.route('/me')
@login_required
def index():
    if session is None or 'id' not in session.keys():
        logout_user()
        return redirect(url_for('login'))

    return render_template('index.html', title='Digital Professional Me', userName=current_user.name)


# Avatar
@app.route('/getAvatar', methods=['GET', 'POST'])
@login_required
def get_avatar():
    return current_user.avatar


# Json для Sunburst Chart
@app.route('/getChartJson', methods=['GET', 'POST'])
@login_required
def get_chart_json():
    #print(current_user.language)
    return jsonify(current_user.json_data)


# Json для Timeline
@app.route('/getTimelineJson', methods=['GET', 'POST'])
@login_required
def get_timeline_json():
    return jsonify(current_user.timeline_events)


# Get Rchilli Json
@app.route('/getRchilliJson', methods=['GET', 'POST'])
@login_required
def get_rchilli_json():
    return jsonify(current_user.rchilli_data)


# Get Skills from Rchilli Json
@app.route('/getRchilliSkills', methods=['GET', 'POST'])
@login_required
def get_rchilli_skills():
    try:
        return jsonify(current_user.rchilli_data['ResumeParserData']['SegregatedSkill'])
    except Exception as e:
        print(e)
        return '404'

# About page
@app.route('/about', methods=['POST', 'GET'])
def about_us():
    #return redirect('http://digitalprofessional.me')
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

            resp.set_cookie(key='id', value=user_db.id)
            session['id'] = user_db.id

            checkbox = True if form.remember.data else False

            login_user(user_db, remember=checkbox)
            return resp

        flash('Wrong password or login', 'error')

    return render_template('login.html', form=form)


# Деавторизация
@app.route('/logout')
@login_required
def logout():
    logout_user()
    resp = make_response(redirect(url_for('login')))

    resp.delete_cookie(key='id')
    session.pop('id', default=None)

    flash('You logged out of the profile', 'success')

    return resp


def save_pdf(url, file_name):
    pdfkit.from_url(url, f'static/data/cv/{file_name}')


@app.route('/changeSkillState', methods=['POST', 'GET'])
def change_skill_state():
    skill_name = request.get_json()['skill']
    disable_skill(current_user.id, skill_name)
    return '200'


@app.route('/skillInputAutocomplete', methods=['POST'])
def show_input_options():
    return skill_autocomplete(request.get_json()['skillName'])


@app.route('/jobInputAutocomplete', methods=['POST'])
def show_jobs():
    return job_autocomplete(request.get_json()['jobName'])


@app.route('/findJob', methods=['POST'])
def find_jobs():
    job_name = request.get_json()['jobName']
    job_deadline = request.get_json()['deadline']
    #print(job_name)
    add_timeline_evidence_event(current_user.id, job_name, job_deadline)
    resp = job_search(job_autocomplete(job_name))['Skills']

    #print(resp)

    owned_skills = get_owned_skills(current_user.id)
    req_skills = []

    for skill in resp:
        req_skills.append(skill['Skill'])

    set_owned_skills = set(owned_skills)
    set_req_skills = set(req_skills)
    #print('owned skills', set_owned_skills)
    #print('required skills', set_req_skills)

    set_different = set_req_skills - set_owned_skills
    #print('skillGap', set_different)

    courses = get_courses(set_different)
    #print(courses)

    return json.loads(json_util.dumps({
        'offeredCourses': courses,
        'gapSkills': set_different,
        'deadline': job_deadline
    }))


@app.route('/parseCertificate', methods=['POST'])
def parse_certificate():
    url = request.get_json()['url']
    resp = dict()

    if 'coursera.org' in url:
        resp = parse_coursera_url(url)
    elif 'stepik.org' in url:
        resp = parse_stepik_url(url)

    add_certificate_event(current_user.id, resp['courseName'], resp['date'], resp['url'], resp['userName'])
    return resp


@app.route('/findSkill', methods=['POST'])
def find_skill():
    soft_types = ['SoftSkill', 'Knowledge', 'Soft', 'BehaviorSkills']

    skill_name = request.get_json()['skill']
    cur_user_data = find_record('id', current_user.id).json_data[0]

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

                    if resp['type'] in soft_types:
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

                if resp['type'] in soft_types:
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

        if resp['type'] in soft_types:
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

    update_record('id', current_user.id, 'jsondata', [cur_user_data])

    return resp


@app.route('/findJobsOptions', methods=['GET'])
@login_required
def find_jobs_by_skills():
    set_owned_skills = set(get_owned_skills(current_user.id))
    related_jobs = dict()
    matched_job = str()
    mx = 0

    for skill in set_owned_skills:
        skill_data = get_skill_from_dataset(skill)
        if skill_data is not None:
            for job in skill_data['relatedJobs']:
                if job in related_jobs.keys():
                    related_jobs[job] += 1
                else:
                    related_jobs[job] = 1

                if related_jobs[job] > mx:
                    mx = related_jobs[job]
                    matched_job = job

    job_data = job_search(job_autocomplete(matched_job))['Skills']
    set_req_skills = set()

    for skill in job_data:
        set_req_skills.add(skill['Skill'])

    #set_different = set_req_skills - set_owned_skills
    set_different = set_owned_skills - set_req_skills

    courses = get_courses(set_different)

    #print(courses)
    #print(set_owned_skills)
    #print(set_req_skills)
    #print(set_different)

    return json.loads(json_util.dumps({
        'offeredCourses': courses,
        'gapSkills': set_different,
        'matchedJob': matched_job
    }))


@app.route('/handleRecommendationClick', methods=['GET', 'POST'])
@login_required
def handleRecommendationClick():
    update_recommendation_clicks(current_user.id)
    return '200'

if __name__ == '__main__':

    if __debug__:
        app.run(debug=True, port=5000, host='0.0.0.0')
    else:
        serve(app, port=5000, host="0.0.0.0")