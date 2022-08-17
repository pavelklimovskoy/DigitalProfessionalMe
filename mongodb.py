import json
from flask import Flask, request, jsonify
from flask_pymongo import PyMongo
from main import collection, collection_dataset
from pymongo import MongoClient
from flask_login import UserMixin
import uuid


class Users(UserMixin):
    Id = ''
    jsondata = {}
    rchillidata = {}
    name = ''
    email = ''
    password = ''
    timeline_events = {}
    avatar = ''

    def __init__(self, Id, name, email, password, jsondata, rchillidata, timeline_events, avatar):
        self.Id = Id
        self.name = name
        self.email = email
        self.password = password
        self.jsondata = jsondata
        self.rchillidata = rchillidata
        self.timeline_events = timeline_events
        self.avatar = avatar

    def to_json(self):
        return {
            "Id": self.Id,
            "name": self.name,
            "email": self.email,
            "password": self.password,
            "jsondata": self.jsondata,
            "rchillidata": self.rchillidata,
            "timelineEvents": self.timeline_events,
            "avatar": self.avatar
        }

    def get_id(self):
        return self.Id

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False


def update_record(findKey, findValue, key, value):
    collection.find_one_and_update({findKey: findValue},
                                   {'$set': {key: value}})


def create_record(CurRequest):
    collection.insert_one({'Id': str(uuid.uuid4()),
                           'name': CurRequest.form['name'],
                           'email': CurRequest.form['email'],
                           'password': CurRequest.form['password'],
                           'jsondata': {},
                           'rchillidata': {},
                           'timelineEvents': {},
                           'avatar': 'user_tmp_example.png'
                           })


def find_record(key, value):
    user = collection.find_one({key: value})
    if user is not None:
        return Users(Id=user['Id'],
                     name=user['name'],
                     email=user['email'],
                     password=user['password'],
                     jsondata=user['jsondata'],
                     rchillidata=user['rchillidata'],
                     timeline_events=user['timelineEvents'],
                     avatar=user['avatar'])
    else:
        return None


def disable_skill(curUserId, skillName):
    user = find_record('Id', curUserId)
    data = user.jsondata[0]
    for i in data['children']:
        for j in i['children']:
            for k in j['children']:
                if k['name'] == skillName:
                    if k['enabled'] is True:
                        k['enabled'] = False
                    else:
                        k['enabled'] = True
                    break

    update_record('Id', curUserId, 'jsondata', [data])
    return user


def add_timeline_evidence_event(cur_user_id, job_name, job_deadline):
    user = find_record('Id', cur_user_id)

    event = {
        'startDate': job_deadline,
        'endDate': '',
        'position': job_name,
        'employer': '',
        'id': len(user.timeline_events['experienceEvents'])
    }

    user.timeline_events['experienceEvents'].append(event)

    update_record('Id', cur_user_id, 'timelineEvents', user.timeline_events)


def add_cerificate_event(cur_user_id, name, date, url, user_name):
    user = find_record('Id', cur_user_id)

    event = {
        'date': date,
        'name': name,
        'url': url,
        'userName': user_name,
        'id': len(user.timeline_events['certifications'])
    }

    user.timeline_events['certifications'].append(event)

    update_record('Id', cur_user_id, 'timelineEvents', user.timeline_events)


def get_owned_skills(cur_user_id):
    user_data = find_record('Id', cur_user_id).jsondata[0]['children']
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
            print(len(skills_union), skills_union)
            courses.append({'courseName': course,
                            'gap': len(skills_union)})
    # dict_courses.sort(key=lambda x: x[0])
    #
    # courses = []
    # for course in dict_courses:
    #     print(course[1])
    #courses = sorted(courses, key=lambda d: d['gap'])
    return sorted(courses, key=lambda d: d['gap'], reverse=True)
