# -*- coding: utf-8 -*-

from flask_login import UserMixin


class User(UserMixin):
    id = str()
    json_data = dict()
    rchilli_data = dict()
    name = str()
    language = str()
    email = str()
    password = str()
    timeline_events = dict()
    avatar = str()
    recommendation_click_counter = 0

    def __init__(
        self,
        id,
        language,
        name,
        email,
        password,
        json_data,
        rchilli_data,
        timeline_events,
        avatar,
        recommendation_click_counter,
    ):
        self.id = id
        self.name = name
        self.email = email
        self.password = password
        self.json_data = json_data
        self.rchilli_data = rchilli_data
        self.timeline_events = timeline_events
        self.avatar = avatar
        self.language = language
        self.recommendation_click_counter = recommendation_click_counter

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
            "avatar": self.avatar,
            "recommendationClickCounter": self.recommendation_click_counter,
        }

    def get_id(self):
        return self.id

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False
