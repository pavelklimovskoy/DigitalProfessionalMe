# -*- coding: utf-8 -*-

from modules.certificate_parser import parse_coursera_url, parse_stepik_url
from modules.blueprints.languages.ru_lang_version import ru_version
from modules.blueprints.languages.en_lang_version import en_version
from modules.blueprints.core.core_routes import core_route
from modules.blueprints.rchilli.routes import rchilli_routes
from modules.blueprints.skills.routes import skills_routes

from bson import json_util
from flask_login import LoginManager, login_required, current_user
from flask import Flask, request, jsonify
from flask_cors import CORS

from modules.db_connector import DatabaseConnector
from modules.service import ServiceContainer
from modules.rchilli import RchilliConnector

import os
import json
from waitress import serve

# Проверка версии интерпретатора перед созданием Flask приложения
# check_python_version()

# Создание и конфигурация Flask приложения
app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('FLASK_SECRET_KEY')
app.config['JSON_AS_ASCII'] = False
app.config['UPLOAD_FOLDER'] = './static/data/cv/'
app.config['UPLOAD_IMAGE_FOLDER'] = './static/data/img/'
app.config['SECURITY_UNAUTHORIZED_VIEW'] = '/auth'
app.config.from_object(__name__)
CORS(app)

# Регистрация блюпринтов во Flask приложении
app.register_blueprint(ru_version)
app.register_blueprint(en_version)
app.register_blueprint(core_route)
app.register_blueprint(rchilli_routes)
app.register_blueprint(skills_routes)


login_manager = LoginManager(app)
login_manager.login_view = 'core_routes.select_language'

@login_manager.user_loader
def load_user(user_id):
    return DatabaseConnector.get_instance().find_record('id', user_id)


@app.after_request
def apply_caching(response):
    response.headers['X-Frame-Options'] = 'ALLOW'
    return response



@app.route('/getChartJson', methods=['GET', 'POST'])
@login_required
def get_chart_json():
    """
    Json для Sunburst Chart
    :return:
    """
    return jsonify(current_user.json_data)


# Json для Timeline
@app.route('/getTimelineJson', methods=['GET', 'POST'])
@login_required
def get_timeline_json():
    return jsonify(current_user.timeline_events)


@app.route('/translatedSkillInputAutocomplete', methods=['POST'])
def show_translated_input_options():
    translated = RchilliConnector.get_instance().get_translate_text(request.get_json()['skillName'])
    return RchilliConnector.get_instance().skill_autocomplete(translated)


@app.route('/translatedJobInputAutocomplete', methods=['POST'])
def show_translated_jobs():
    translated = RchilliConnector.get_instance().get_translate_text(request.get_json()['jobName'])
    print(translated)
    return RchilliConnector.get_instance().job_autocomplete(translated)


@app.route('/jobInputAutocomplete', methods=['POST'])
def show_jobs():
    return RchilliConnector.get_instance().job_autocomplete(request.get_json()['jobName'])


@app.route('/findJob', methods=['POST'])
def find_jobs():
    job_name = request.get_json()['jobName']
    job_deadline = request.get_json()['deadline']
    # print(job_name)
    DatabaseConnector.get_instance().add_timeline_evidence_event(current_user.id, job_name, job_deadline)
    resp = RchilliConnector.get_instance().job_search(RchilliConnector.get_instance().job_autocomplete(job_name))['Skills']

    # print(resp)

    owned_skills = DatabaseConnector.get_instance().get_owned_skills(current_user.id)
    req_skills = []

    for skill in resp:
        req_skills.append(skill['Skill'])

    set_owned_skills = set(owned_skills)
    set_req_skills = set(req_skills)
    print('owned skills', set_owned_skills)
    print('required skills', set_req_skills)

    set_different = set_req_skills - set_owned_skills
    # print('skillGap', set_different)

    courses = DatabaseConnector.get_instance().get_courses(set_different)
    print(courses)

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

    DatabaseConnector.get_instance().add_certificate_event(current_user.id, resp['courseName'], resp['date'], resp['url'], resp['userName'])
    return resp





@app.route('/getAdminPanelData', methods=['GET', 'POST'])
def get_admin_panel_data():
    resp = DatabaseConnector.get_instance().get_admin_panel()
    res = []
    for i in resp:
        i.pop('_id')
        res.append(i)
    print(res)
    return jsonify(res)


if __name__ == '__main__':

    if __debug__:
        app.run(debug=True, port=5000, host='0.0.0.0')
    else:
        from werkzeug.middleware.proxy_fix import ProxyFix

        app.wsgi_app = ProxyFix(app.wsgi_app)
        serve(app, port=5000, host="0.0.0.0")
