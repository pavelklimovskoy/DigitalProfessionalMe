import json
from flask import Flask, request, jsonify
from flask_pymongo import PyMongo
from main import collection
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
