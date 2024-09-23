# -*- coding: utf-8 -*-
"""



"""

from .db_connector import DatabaseConnector


class Analytics:
    __instance = None

    def __init__(
        self, image_count=0, users_count=0, cv_count=0, type_of_record="record", info=""
    ):
        if not Analytics.__instance:
            self.image_count = image_count
            self.users_count = users_count
            self.cv_count = cv_count
            self.type_of_record = type_of_record
            self.info = info

    @classmethod
    def get_instance(cls):
        if not cls.__instance:
            cls.__instance = Analytics()
        return cls.__instance

    def to_json(self):
        return {
            "image_count": self.image_count,
            "users_count": self.users_count,
            "cv_count": self.cv_count,
            "type_of_record": self.type_of_record,
            "info": self.info,
        }

    def summary_info_is_exist(self) -> bool:
        # db_instance = DatabaseConnector.get_instance()
        if (
            DatabaseConnector.get_instance().collection_analytics.find_one(
                {"type_of_record": "summary"}
            )
            is None
        ):
            DatabaseConnector.get_instance().collection_analytics.insert_one(
                Analytics(type_of_record="summary").to_json()
            )

        return True

    def summary_image_count(self) -> int:
        # db_instance = DatabaseConnector.get_instance()
        if self.summary_info_is_exist() is True:
            return DatabaseConnector.get_instance().collection_analytics.find_one(
                {"type_of_record": "summary"}
            )["image_count"]

        return -1

    def increment_image_count(self):
        # db_instance = DatabaseConnector.get_instance()
        if self.summary_info_is_exist() is True:
            count = DatabaseConnector.get_instance().collection_analytics.find_one(
                {"type_of_record": "summary"}
            )["image_count"]
            DatabaseConnector.get_instance().collection_analytics.find_one_and_update(
                {"type_of_record": "summary"}, {"$set": {"image_count": count + 1}}
            )

    def summary_cv_count(self) -> int:
        # db_instance = DatabaseConnector.get_instance()
        if self.summary_info_is_exist() is True:
            return DatabaseConnector.get_instance().collection_analytics.find_one(
                {"type_of_record": "summary"}
            )["cv_count"]

        return -1

    def increment_cv_count(self):
        if self.summary_info_is_exist() is True:
            count = DatabaseConnector.get_instance().collection_analytics.find_one(
                {"type_of_record": "summary"}
            )["cv_count"]
            DatabaseConnector.get_instance().collection_analytics.find_one_and_update(
                {"type_of_record": "summary"}, {"$set": {"cv_count": count + 1}}
            )
