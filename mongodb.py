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
    avatar = ''


    def __init__(self, Id, name, email, password, jsondata, rchillidata, avatar):
        self.Id = Id
        self.name = name
        self.email = email
        self.password = password
        self.jsondata = jsondata
        self.rchillidata = rchillidata
        self.avatar = avatar


    def to_json(self):
        return {
            "Id": self.Id,
            "name": self.name,
            "email": self.email,
            "password": self.password,
            "jsondata": self.jsondata,
            "rchillidata": self.rchillidata,
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
                     avatar=user['avatar'])
    else:
        return None

# class Users(db.Document, UserMixin):
#     _id = db.ObjectId()
#     #Id = db.StringField(primary_key=True)
#     jsondata = db.DictField()
#     rchillidata = db.DictField()
#     name = db.StringField()
#     email = db.StringField()
#     password = db.StringField()
#
#     def __init__(self, name, email, password):
#         self.name = name
#         self.email = email
#         self.password = password
#
#     def to_json(self):
#         return {
#             "Id": self._id,
#             "name": self.name,
#             "email": self.email,
#             "password": self.password,
#             "jsondata": self.jsondata,
#             "rchillidata": self.rchillidata
#         }
#
#     def get_id(self):
#         return self._id
#
#     def is_authenticated(self):
#         return True
#
#     def is_active(self):
#         return True
#
#     def is_anonymous(self):
#         return False


# def find_user_byemail(userEmail):
#     user = mongo.db.users.find_one({"username": username})
#     if not user:
#         return None
#     return User(user["username"], user["email"], user["date_created"])
#
#
#     #try:
#     users = Users.objects(email=str(userEmail)).first()
#     print("Hello from byemail", users)
#     #except:
#     #    user = None
#     return users
#
# def find_user_byid(userId):
#     #try:
#     users = Users.objects(Id=str(userId)).first()
#     print("Hello from byid", users.Id)
#     #except:
#         #user = None
#     return users
#
#
# def create_record(CurRequest):
#     #try:
#     users = Users(
#         Id=str(uuid.uuid4()),
#         name=CurRequest.form['name'],
#         email=CurRequest.form['email'],
#         password=CurRequest.form['password']
#     )
#
#     print("Hello from creating", users.str(users.Id))
#     print("Hello from creating", users.name)
#     users.save()
#
#     #except:
#     #    users = None
#
# def update_record(users, jsonData, rchilliData):
#     if users == None:
#         return False
#     else:
#         #Users().reload()
#         #user.save()
#         users.update(jsondata=jsonData)
#         users.update(rchillidata=rchilliData)
#
#         users.save()
#         print("Hello from updating", users)
#         return True
#
# def delete_record(self):
#     record = json.loads(request.data)
#     users = self.objects(name=record['name']).first()
#
#     if not users or users == None:
#         users = None
#         print('Error! User not found!')
#         return False
#     else:
#         users.delete()
#         return True
