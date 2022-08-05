import base64
import requests
import json
import os

# Rchilli API config
API_PARSE_RESUME_URL = 'https://rest.rchilli.com/RChilliParser/Rchilli/parseResumeBinary'
API_SKILL_SEARCH_URL = 'https://taxonomy3.rchilli.com/taxonomy/skillsearch'
API_SKILL_AUTOCOMPLETE_URL = 'https://taxonomy3.rchilli.com/taxonomy/autocompleteskill'
API_RESUME_VERSION = '8.0.0'
API_TAXONOMY_VERSION = '3.0'
USER_KEY = os.getenv('RCHILLI_API_KEY')
USER_NAME = 'Alexander Fedorov'


def rchilli_parse(file_name):
    file_path = f'./static/data/cv/{file_name}'

    with open(file_path, "rb") as filePath:
        encoded_string = base64.b64encode(filePath.read())

    data64 = encoded_string.decode('unicode_escape')
    headers = {'content-type': 'application/json'}
    body = """{"filedata":\"""" + data64 + """\","filename":\"""" + file_name + """\","userkey":\"""" + \
           USER_KEY + """\",\"version\":\"""" + API_RESUME_VERSION + """\",\"subuserid\":\"""" + USER_NAME + """\"}"""
    response = requests.post(API_PARSE_RESUME_URL, data=body, headers=headers)
    resp = json.loads(response.text)

    return resp


def skill_search(skill_name):
    payload = json.dumps({
        "ApiKey": USER_KEY,
        "Version": API_TAXONOMY_VERSION,
        "Language": "ENG",
        "Locale": "US",
        "CustomValues": "",
        "Keyword": skill_name
    })
    headers = {
        'Content-Type': 'application/json'
    }

    response = requests.request("POST", API_SKILL_SEARCH_URL, headers=headers, data=payload)
    resp = response.json()['Skill']['SkillData']
    print(resp)
    skill_type = str(resp['SkillType']).split('/')
    print(skill_type)
    skill_data = {
        'ontology': resp['SkillOntology'],
        'type': skill_type[0],
        'searchWord': skill_name
    }

    return skill_data

    # resp = json.loads(response.text)
    # print(resp)
    # return resp


def skill_autocomplete(skill_name):
    payload = json.dumps({
        "ApiKey": USER_KEY,
        "Version": API_TAXONOMY_VERSION,
        "Language": "ENG",
        "Locale": "US",
        "CustomValues": "",
        "Keyword": skill_name
    })
    headers = {
        'Content-Type': 'application/json'
    }

    try:
        response = requests.request("POST", API_SKILL_AUTOCOMPLETE_URL, headers=headers, data=payload)
        resp = response.json()['SkillAutoComplete']
        return {'options': resp}
    except Exception as e:
        print(e)
