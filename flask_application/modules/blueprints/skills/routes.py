# -*- coding: utf-8 -*-

"""
    Фйал с роутаами для работы со скиллами

"""

from flask import Blueprint
from flask_login import login_required,  current_user
from flask import request




from bson import json_util
import json


skills_routes = Blueprint('skills_routes', __name__, template_folder='templates')


@skills_routes.route('/skillInputAutocomplete', methods=['POST'])
def show_input_options():
    from ...rchilli import RchilliConnector
    return RchilliConnector.get_instance().skill_autocomplete(request.get_json()['skillName'])


@skills_routes.route('/translatedSkillInputAutocomplete', methods=['POST'])
def show_translated_input_options():
    from ...rchilli import RchilliConnector
    # print(request.get_json()['skillName'])
    translated = RchilliConnector.get_instance().get_translate_text(request.get_json()['skillName'])
    # print(translated)
    return RchilliConnector.get_instance().skill_autocomplete(translated)


@skills_routes.route('/changeSkillState', methods=['POST', 'GET'])
def change_skill_state():
    from ...rchilli import RchilliConnector
    from ...db_connector import DatabaseConnector
    skill_name = request.get_json()['skill']
    DatabaseConnector.get_instance().disable_skill(current_user.id, skill_name)
    return '200'


@skills_routes.route('/findSkill', methods=['POST'])
def find_skill():
    from ...rchilli import RchilliConnector
    from ...db_connector import DatabaseConnector
    from ...service import ServiceContainer
    soft_types = ['SoftSkill', 'Knowledge', 'Soft', 'BehaviorSkills']

    skill_name = request.get_json()['skill']
    cur_user_data = DatabaseConnector.get_instance().find_record('id', current_user.id).json_data[0]

    resp = RchilliConnector.get_instance().skill_search(skill_name)
    ontoloty = resp['ontology']

    flag1 = False
    flag2 = False
    filling = ''

    for grand_parent_skill_type in cur_user_data['children']:
        if ontoloty.split('>')[0] == grand_parent_skill_type['name']:
            flag1 = True

            for parent_skill_type in grand_parent_skill_type['children']:
                if ontoloty.split('>')[1] == parent_skill_type['name']:  # Найден Parent, GrandParent
                    flag2 = True

                    short_name = ontoloty.split('>')[-1]
                    if len(short_name) > 6:
                        short_name = f'{ontoloty.split(">")[-1][:6]}...'

                    if resp['type'] in soft_types:
                        filling = '#FFB240'
                    else:
                        filling = '#4188D2'

                    skill = {
                        'name': ontoloty.split('>')[-1],
                        'id': resp['type'],
                        'value': '1',
                        'enabled': True,
                        'short_name': short_name,
                        'fill': filling,
                        'grandParent': grand_parent_skill_type['name'],
                        'parent': parent_skill_type['name']
                    }
                    parent_skill_type['children'].append(skill)
                    break

            if flag2 is False:  # Parent не найден, только GrandParent
                parent_skill_type = {
                    'name': ontoloty.split('>')[1],
                    'id': resp['type'],
                    'value': '1',
                    'fill': ServiceContainer.get_instance().color_calc(1, resp['type']),
                    'parent': grand_parent_skill_type['name'],
                    'children': []
                }

                short_name = ontoloty.split('>')[-1]
                if len(short_name) > 6:
                    short_name = f'{ontoloty.split(">")[-1][:6]}...'

                if resp['type'] in soft_types:
                    filling = '#FFB240'
                else:
                    filling = '#4188D2'

                skill = {
                    'name': ontoloty.split('>')[-1],
                    'id': resp['type'],
                    'value': '1',
                    'enabled': True,
                    'short_name': short_name,
                    'fill': filling,
                    'grandParent': grand_parent_skill_type['name'],
                    'parent': parent_skill_type['name']
                }
                parent_skill_type['children'].append(skill)
                grand_parent_skill_type['children'].append(parent_skill_type)

    if flag1 is False:  # Не найдено ни GrandParent, ни Parent
        grand_parent_skill_type = {
            'name': ontoloty.split('>')[0],
            'id': resp['type'],
            'value': '1',
            'fill': ServiceContainer.get_instance().color_calc(1, resp['type']),
            'parent': 'Me',
            'children': []
        }

        parent_skill_type = {
            'name': ontoloty.split('>')[1],
            'id': resp['type'],
            'value': '1',
            'fill': ServiceContainer.get_instance().color_calc(1, resp['type']),
            'parent': grand_parent_skill_type['name'],
            'children': []
        }

        short_name = ontoloty.split('>')[-1]
        if len(short_name) > 6:
            short_name = f'{ontoloty.split(">")[-1][:6]}...'

        if resp['type'] in soft_types:
            filling = '#FFB240'
        else:
            filling = '#4188D2'

        skill = {
            'name': ontoloty.split('>')[-1],
            'id': resp['type'],
            'value': '1',
            'enabled': True,
            'short_name': short_name,
            'fill': filling,
            'grandParent': grand_parent_skill_type['name'],
            'parent': parent_skill_type['name']
        }

        parent_skill_type['children'].append(skill)
        grand_parent_skill_type['children'].append(parent_skill_type)
        cur_user_data['children'].append(grand_parent_skill_type)

    if filling != '':
        resp['filling'] = filling
    else:
        resp['filling'] = '#4188D2'

    DatabaseConnector.get_instance().update_record('id', current_user.id, 'jsondata', [cur_user_data])

    return resp


# @skills_routes.route('/findJobsOptions', methods=['GET'])
# @login_required
# def find_jobs_by_skills():
#     """
#     Метод для рекомендации работы по навыками пользователся
#     :return:
#     """
#     from ...rchilli import RchilliConnector
#     from ...db_connector import DatabaseConnector
#     from collections import defaultdict
#     import operator
#
#     # Получение экземпляров одиночек
#     db_instance = DatabaseConnector.get_instance()
#     rchilli_instance = RchilliConnector.get_instance()
#
#     skills_current_user = db_instance.get_owned_skills(current_user.id)
#     user_skills_set = set(skills_current_user)
#
#     related_jobs = defaultdict(lambda: 1)
#
#     matched_job = str()
#     mx = 0
#
#
#     # Перебираем все умения пользователя
#     for current_skill in user_skills_set:
#         # Получение списка работ и курсов для отдельного навыка
#         skill_data = db_instance.skill_in_dataset(current_skill)
#         if skill_data is None:
#             continue
#
#         # Перебираем все работы для конкретного навыка и считаем их упоминания
#         for job in skill_data['relatedJobs']:
#             related_jobs[job] += 1
#
#             if related_jobs[job] > mx:
#                 mx = related_jobs[job]
#                 matched_job = job
#
#     # matched_job = max(related_jobs, key=related_jobs.get)
#
#     job_data = rchilli_instance.job_search(rchilli_instance.job_autocomplete(matched_job))['Skills']
#     set_req_skills = set()
#
#     for skill in job_data:
#         set_req_skills.add(skill['Skill'])
#
#     # set_different = set_req_skills - set_owned_skills
#     set_different = user_skills_set - set_req_skills
#
#     courses = db_instance.get_courses(set_different)
#
#     return json.loads(json_util.dumps({
#         'offeredCourses': courses,
#         'gapSkills': set_different,
#         'matchedJob': matched_job
#     }))


@skills_routes.route('/findJobsOptions', methods=['GET'])
@login_required
def find_jobs_by_skills():
    from ...rchilli import RchilliConnector
    from ...db_connector import DatabaseConnector

    set_owned_skills = set(DatabaseConnector.get_instance().get_owned_skills(current_user.id))
    related_jobs = dict()
    matched_job = str()
    mx = 0

    for skill in set_owned_skills:
        skill_data = DatabaseConnector.get_instance().get_skill_from_dataset(skill)
        if skill_data is not None:
            for job in skill_data['relatedJobs']:
                if job in related_jobs.keys():
                    related_jobs[job] += 1
                else:
                    related_jobs[job] = 1

                if related_jobs[job] > mx:
                    mx = related_jobs[job]
                    matched_job = job

    job_data = RchilliConnector.get_instance().job_search(RchilliConnector.get_instance().job_autocomplete(matched_job))['Skills']
    set_req_skills = set()

    for skill in job_data:
        set_req_skills.add(skill['Skill'])

    # set_different = set_req_skills - set_owned_skills
    set_different = set_owned_skills - set_req_skills

    courses = DatabaseConnector.get_instance().get_courses(set_different)

    return json.loads(json_util.dumps({
        'offeredCourses': courses,
        'gapSkills': set_different,
        'matchedJob': matched_job
    }))
