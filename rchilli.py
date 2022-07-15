import base64
import requests
import json

# Rchilli API config
APIURL = "https://rest.rchilli.com/RChilliParser/Rchilli/parseResumeBinary"
USERKEY = '00SLQQL6'
VERSION = '8.0.0'
subUserId = 'Alexander Fedorov'

def rchilli_parse(fileName):
    filePath = './static/data/cv/'+fileName
    # service url- provided by RChilli

    with open(filePath, "rb") as filePath:
        encoded_string = base64.b64encode(filePath.read())
        
    data64 = encoded_string.decode('unicode_escape')
    headers = {'content-type': 'application/json'}
    body = """{"filedata":\"""" + data64 + """\","filename":\"""" + fileName + """\","userkey":\"""" + USERKEY + """\",\"version\":\"""" + VERSION + """\",\"subuserid\":\"""" + subUserId + """\"}"""
    response = requests.post(APIURL, data=body, headers=headers)
    resp = json.loads(response.text)

    # please handle error too

    Resume = resp["ResumeParserData"]
    # read values from response

    #jsonName = './static/data/cv/' + 'rchilli.json'

    #with open(jsonName, 'w', encoding='utf-8') as outfile:
    #    json.dump(resp, outfile, sort_keys=True, indent=2, ensure_ascii=False)

    return resp