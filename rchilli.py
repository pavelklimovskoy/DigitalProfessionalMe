import base64
import requests
import json

# Rchilli API config
apiParseResumeUrl = 'https://rest.rchilli.com/RChilliParser/Rchilli/parseResumeBinary'
apiSkillSearchUrl = 'https://taxonomy3.rchilli.com/taxonomy/skillsearch'
apiSkillAutocompleteUrl = 'https://taxonomy3.rchilli.com/taxonomy/autocompleteskill'
apiResumeVersion = '8.0.0'
apiTaxonomyVersion = '3.0'
userkey = '00SLQQL6'
subUserId = 'Alexander Fedorov'


def rchilli_parse(fileName):
    filePath = './static/data/cv/' + fileName
    # service url- provided by RChilli

    with open(filePath, "rb") as filePath:
        encoded_string = base64.b64encode(filePath.read())

    data64 = encoded_string.decode('unicode_escape')
    headers = {'content-type': 'application/json'}
    body = """{"filedata":\"""" + data64 + """\","filename":\"""" + fileName + """\","userkey":\"""" + userkey + """\",\"version\":\"""" + apiResumeVersion + """\",\"subuserid\":\"""" + subUserId + """\"}"""
    response = requests.post(apiParseResumeUrl, data=body, headers=headers)
    resp = json.loads(response.text)

    # please handle error too

    #Resume = resp["ResumeParserData"]
    # read values from response

    # jsonName = './static/data/cv/' + 'rchilli.json'

    # with open(jsonName, 'w', encoding='utf-8') as outfile:
    #    json.dump(resp, outfile, sort_keys=True, indent=2, ensure_ascii=False)

    return resp


def skill_search(skillName):
    payload = json.dumps({
        "ApiKey": userkey,
        "Version": apiTaxonomyVersion,
        "Language": "ENG",
        "Locale": "US",
        "CustomValues": "",
        "Keyword": skillName
    })
    headers = {
        'Content-Type': 'application/json'
    }

    response = requests.request("POST", apiSkillSearchUrl, headers=headers, data=payload)
    resp = response.json()['Skill']['SkillData']

    skillData = {
        'ontology': resp['SkillOntology'],
        'type': resp['SkillType']
    }

    print(skillData)
    return skillData


    #resp = json.loads(response.text)
    #print(resp)
    #return resp

def skill_autocomplete(skillName):
    payload = json.dumps({
        "ApiKey": userkey,
        "Version": apiTaxonomyVersion,
        "Language": "ENG",
        "Locale": "US",
        "CustomValues": "",
        "Keyword": skillName
    })
    headers = {
        'Content-Type': 'application/json'
    }

    response = requests.request("POST", apiSkillAutocompleteUrl, headers=headers, data=payload)

    resp = response.json()['SkillAutoComplete']
    return {'options': resp}