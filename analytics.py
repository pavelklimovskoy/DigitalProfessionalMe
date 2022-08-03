"""



"""

from pymongo import MongoClient

client = MongoClient('localhost', 27017)
db = client['DPM']
collection = db['Analytics']


class Analytics:
    image_count: int = 0
    users_count: int = 0
    cv_count: int = 0
    type_of_record: str = ""
    info: str = ""

    def __init__(self, image_count=0, users_count=0, cv_count=0, type_of_record="record", info=""):
        self.image_count = image_count
        self.users_count = users_count
        self.cv_count = cv_count
        self.type_of_record = type_of_record
        self.info = info

    def to_json(self):
        return {
            "image_count": self.image_count,
            "users_count": self.users_count,
            "cv_count": self.cv_count,
            "type_of_record": self.type_of_record,
            "info": self.info
        }


def summary_info_is_exist() -> bool:
    if collection.find_one({"type_of_record": "summary"}) is None:
        collection.insert_one(Analytics(type_of_record="summary").to_json())

    return True


def summary_image_count() -> int:
    if summary_info_is_exist() is True:
        return collection.find_one({"type_of_record": "summary"})["image_count"]

    return -1


def increment_image_count():
    if summary_info_is_exist() is True:
        count = collection.find_one({"type_of_record": "summary"})["image_count"]
        collection.find_one_and_update({"type_of_record": "summary"}, {'$set': {"image_count": count + 1}})


def summary_cv_count() -> int:
    if summary_info_is_exist() is True:
        return collection.find_one({"type_of_record": "summary"})["cv_count"]

    return -1


def increment_cv_count():
    if summary_info_is_exist() is True:
        count = collection.find_one({"type_of_record": "summary"})["cv_count"]
        collection.find_one_and_update({"type_of_record": "summary"}, {'$set': {"cv_count": count + 1}})