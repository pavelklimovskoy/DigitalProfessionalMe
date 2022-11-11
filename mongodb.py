import datetime
from main import collection_users, collection_dataset, collection_skills_dataset
from flask_login import UserMixin
import uuid


class Users(UserMixin):
    id = str()
    json_data = dict()
    rchilli_data = dict()
    name = str()
    language = str()
    email = str()
    password = str()
    timeline_events = dict()
    avatar = str()

    def __init__(self, id, language, name, email, password, json_data, rchilli_data, timeline_events, avatar):
        self.id = id
        self.name = name
        self.email = email
        self.password = password
        self.json_data = json_data
        self.rchilli_data = rchilli_data
        self.timeline_events = timeline_events
        self.avatar = avatar
        self.language = language

    def to_json(self):
        return {
            "id": self.id,
            "name": self.name,
            "language": self.language,
            "email": self.email,
            "password": self.password,
            "jsondata": self.json_data,
            "rchillidata": self.rchilli_data,
            "timelineEvents": self.timeline_events,
            "avatar": self.avatar
        }

    def get_id(self):
        return self.id

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False


def update_record(findKey, findValue, key, value):
    collection_users.find_one_and_update({findKey: findValue},
                                         {'$set': {key: value}})


def create_record(form):
    json_data = dict()

    json_data['name'] = 'Me'
    json_data['children'] = []

    timeline_events = dict()
    timeline_events['qualificationEvents'] = []
    timeline_events['experienceEvents'] = []
    timeline_events['certifications'] = [{
        'date': datetime.datetime.now(),
        'name': 'Digital Professional Me registration',
        'id': 0
    }]

    rchilli_data = dict()
    rchilli_data['ResumeParserData'] = {}
    rchilli_data['ResumeParserData']['SegregatedSkill'] = [{
        'Type': 'OperationalSkill',
        'Skill': 'Skills Profiling',
        'FormattedName': 'Skills Profiling',
        'Alias': '',
        'Ontology': 'Information>Skills>Skills Profiling',
        'Evidence': 'ExperienceSection',
        'LastUsed': '',
        'ExperienceInMonths': 1
    }]

    json_data['children'] = [
        {
            'name': 'Information',
            'id': 'OperationalSkill',
            'fill': '#4188D2',
            'parent': 'Me',
            'children': [
                {
                    'name': 'Skills',
                    'id': 'OperationalSkill',
                    'value': '1',
                    'fill': '#4188D2',
                    'parent': 'Information',
                    'children': [
                        {
                            'name': 'Skills Profiling',
                            'id': 'OperationalSkill',
                            'value': '1',
                            'enabled': True,
                            'shortName': 'Skills Profiling',
                            'fill': '#4188D2',
                            'grandParent': 'Information',
                            'parent': 'Skills'
                        }
                    ]
                }
            ]
        }
    ]

    collection_users.insert_one({
        'id': str(uuid.uuid4()),
        'language': 'en',
        'name': form.name.data,
        'email': form.email.data,
        'password': form.password.data,
        'jsondata': [json_data],
        'rchillidata': rchilli_data,
        'timelineEvents': timeline_events,
        'avatar': 'user_tmp_example.png'
    })


def find_record(key, value):
    user = collection_users.find_one({key: value})
    if user is not None:
        return Users(id=user['id'],
                     language=user['language'],
                     name=user['name'],
                     email=user['email'],
                     password=user['password'],
                     json_data=user['jsondata'],
                     rchilli_data=user['rchillidata'],
                     timeline_events=user['timelineEvents'],
                     avatar=user['avatar'])
    else:
        return None


def disable_skill(curUserId, skillName):
    user = find_record('id', curUserId)
    data = user.json_data[0]
    for i in data['children']:
        for j in i['children']:
            for k in j['children']:
                if k['name'] == skillName:
                    if k['enabled'] is True:
                        k['enabled'] = False
                    else:
                        k['enabled'] = True
                    break

    update_record('id', curUserId, 'jsondata', [data])
    return user


def add_timeline_evidence_event(user_id, job_name, job_deadline):
    user = find_record('id', user_id)

    event = {
        'startDate': job_deadline,
        'endDate': '',
        'position': job_name,
        'employer': '',
        'id': len(user.timeline_events['experienceEvents'])
    }

    user.timeline_events['experienceEvents'].append(event)

    update_record('id', user_id, 'timelineEvents', user.timeline_events)


def add_certificate_event(user_id, name, date, url, user_name):
    user = find_record('id', user_id)

    event = {
        'date': date,
        'name': name,
        'url': url,
        'userName': user_name,
        'id': len(user.timeline_events['certifications'])
    }

    user.timeline_events['certifications'].append(event)

    update_record('id', user_id, 'timelineEvents', user.timeline_events)


def get_owned_skills(user_id):
    user_data = find_record('id', user_id).json_data[0]['children']
    skills = []

    for lvl1 in user_data:
        for lvl2 in lvl1['children']:
            for lvl3 in lvl2['children']:
                skills.append(lvl3['name'])

    return skills


def get_courses(req_skills):
    courses = []

    for course in collection_dataset.find():
        course_skills = set(course['skills'])
        skills_union = course_skills & req_skills

        if len(skills_union):
            # print(len(skills_union), skills_union, course['name'], course['url'])
            courses.append({'courseData': course,
                            'gapLength': len(skills_union),
                            'gapSkills': skills_union})
    return sorted(courses, key=lambda d: d['gapLength'], reverse=True)


def add_skill_to_dataset(skill_name, jobs, courses, id):
    collection_skills_dataset.insert_one({
        'id': id,
        'skill': skill_name,
        'relatedJobs': jobs,
        'relatedCourses': courses
    })


def get_skill_from_dataset(skill_name):
    return collection_skills_dataset.find_one({'skill': skill_name})
