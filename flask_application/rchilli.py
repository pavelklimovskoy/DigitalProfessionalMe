import base64
import requests
import json
import os

# Rchilli API config
API_PARSE_RESUME_URL = 'https://rest.rchilli.com/RChilliParser/Rchilli/parseResumeBinary'
API_SKILL_SEARCH_URL = 'https://taxonomy3.rchilli.com/taxonomy/skillsearch'
API_JOB_SEARCH_URL = 'https://taxonomy3.rchilli.com/taxonomy/jobprofilesearch'
API_SKILL_AUTOCOMPLETE_URL = 'https://taxonomy3.rchilli.com/taxonomy/autocompleteskill'
API_JOB_AUTOCOMPLETE_URL = 'https://taxonomy3.rchilli.com/taxonomy/autocompletejobprofile'
API_RESUME_VERSION = '8.0.0'
API_TAXONOMY_VERSION = '3.0'
USER_KEY = os.getenv('RCHILLI_API_KEY')
USER_NAME = 'Alexander Fedorov'

def get_translate_text(text):
    url = "https://google-translate1.p.rapidapi.com/language/translate/v2"

    payload = "q=Hello%2C%20world!&target=es&source=en"
    headers = {
        "content-type": "application/x-www-form-urlencoded",
        "Accept-Encoding": "application/gzip",
        "X-RapidAPI-Key": "aa9a8aab23mshd0bac0de361bd74p19ca38jsn50395001c991",
        "X-RapidAPI-Host": "google-translate1.p.rapidapi.com"
    }

    response = requests.request("POST", url, data=payload, headers=headers)

    return response.text


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

    resp['ResumeParserData'].pop('DetailResume')
    resp['ResumeParserData'].pop('HtmlResume')
    resp['ResumeParserData'].pop('TemplateOutput')

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
    skill_type = str(resp['SkillType']).split('/')
    skill_data = {
        'ontology': resp['SkillOntology'],
        'type': skill_type[0],
        'searchWord': skill_name,
        'jobs': resp['RelatedJobProfile']
    }

    return skill_data


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


def job_search(job_name):
    payload = json.dumps({
        "ApiKey": USER_KEY,
        "Version": API_TAXONOMY_VERSION,
        "Language": "ENG",
        "Locale": "US",
        "CustomValues": "",
        "Keyword": job_name
    })

    headers = {
        'Content-Type': 'application/json'
    }

    response = requests.request("POST", API_JOB_SEARCH_URL, headers=headers, data=payload)
    resp = response.json()['JobProfile']['JobProfileData']

    return resp


def job_autocomplete(job_name):
    payload = json.dumps({
        "ApiKey": USER_KEY,
        "Version": API_TAXONOMY_VERSION,
        "Language": "ENG",
        "Locale": "US",
        "CustomValues": "",
        "Keyword": job_name
    })

    headers = {
        'Content-Type': 'application/json'
    }

    try:
        response = requests.request("POST", API_JOB_AUTOCOMPLETE_URL, headers=headers, data=payload)
        resp = response.json()
        return {'options': resp['JobProfileAutoComplete']}
    except Exception as e:
        print(e)
