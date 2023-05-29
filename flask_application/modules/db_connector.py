# -*- coding: utf-8 -*-


import uuid
import datetime
import os
from pymongo import MongoClient
from .user_db import User


class DatabaseConnector:
    __instance = None

    def __init__(self):
        if not DatabaseConnector.__instance:
            self.client = MongoClient(f'mongodb://root:example@{os.getenv("MONGO_MODE")}', 27017)
            self.db = self.client['DPM']
            self.client.server_info()
            self.collection_users = self.db['users']
            self.collection_dataset = self.db['Datasets']
            self.collection_skills_dataset = self.db['SkillsDataset']
            self.collection_feedback = self.db['Feedback']
            self.collection_admin_panel = self.db['AdminPanel']
            self.collection_analytics = self.db['Analytics']



    @classmethod
    def get_instance(cls):
        if not cls.__instance:
            cls.__instance = DatabaseConnector()
        return cls.__instance

    def update_record(self, findKey, findValue, key, value):
        self.collection_users.find_one_and_update({findKey: findValue},
                                                  {'$set': {key: value}})

    def create_record(self, name, email, password):
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

        self.collection_users.insert_one({
            'id': str(uuid.uuid4()),
            'language': 'en',
            'name': name,
            'email': email,
            'password': password,
            'jsondata': [json_data],
            'rchillidata': rchilli_data,
            'timelineEvents': timeline_events,
            'avatar': 'user_tmp_example.png',
            'recommendationClickCounter': 0
        })

        new_user = self.find_record("email", email)
        print(new_user)
        return new_user

    def find_record(self, key, value):
        user = self.collection_users.find_one({key: value})
        if user is not None:
            return User(id=user['id'],
                         language=user['language'],
                         name=user['name'],
                         email=user['email'],
                         password=user['password'],
                         json_data=user['jsondata'],
                         rchilli_data=user['rchillidata'],
                         timeline_events=user['timelineEvents'],
                         avatar=user['avatar'],
                         recommendation_click_counter=user['recommendationClickCounter'])
        else:
            return None

    def disable_skill(self, curUserId, skillName):
        user = self.find_record('id', curUserId)
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

        self.update_record('id', curUserId, 'jsondata', [data])
        return user

    def add_timeline_evidence_event(self, user_id, job_name, job_deadline):
        user = self.find_record('id', user_id)

        event = {
            'startDate': job_deadline,
            'endDate': '',
            'position': job_name,
            'employer': '',
            'id': len(user.timeline_events['experienceEvents'])
        }

        user.timeline_events['experienceEvents'].append(event)

        self.update_record('id', user_id, 'timelineEvents', user.timeline_events)

    def add_certificate_event(self, user_id, name, date, url, user_name):
        user = self.find_record('id', user_id)

        event = {
            'date': date,
            'name': name,
            'url': url,
            'userName': user_name,
            'id': len(user.timeline_events['certifications'])
        }

        user.timeline_events['certifications'].append(event)

        self.update_record('id', user_id, 'timelineEvents', user.timeline_events)

    def get_owned_skills(self, user_id):
        user_data = self.find_record('id', user_id).json_data[0]['children']
        skills = []

        for lvl1 in user_data:
            for lvl2 in lvl1['children']:
                for lvl3 in lvl2['children']:
                    skills.append(lvl3['name'])

        return skills

    def get_courses(self, req_skills):
        courses = []

        for course in self.collection_dataset.find():
            course_skills = set(course['skills'])
            skills_union = course_skills & req_skills

            if len(skills_union):
                # print(len(skills_union), skills_union, course['name'], course['url'])
                courses.append({'courseData': course,
                                'gapLength': len(skills_union),
                                'gapSkills': skills_union})
        return sorted(courses, key=lambda d: d['gapLength'], reverse=True)

    def add_skill_to_dataset(self, skill_name, jobs, courses, id):
        self.collection_skills_dataset.insert_one({
            'id': id,
            'skill': skill_name,
            'relatedJobs': jobs,
            'relatedCourses': courses
        })

    def get_skill_from_dataset(self, skill_name):
        return self.collection_skills_dataset.find_one({'skill': skill_name})

    def update_recommendation_clicks(self, user_id):
        count = self.collection_users.find_one({'id': user_id})['recommendationClickCounter']
        self.collection_users.find_one_and_update({'id': user_id}, {'$set': {"recommendationClickCounter": count + 1}})

    def get_admin_panel(self):
        # print(dict(collection_admin_panel.find()))
        cur = self.collection_admin_panel.find()
        documents = [doc for doc in cur]

        return documents

