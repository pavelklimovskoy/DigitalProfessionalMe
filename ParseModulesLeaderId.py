import sys
from bs4 import BeautifulSoup
from urllib.request import urlopen, Request
from urllib.error import HTTPError
import random
import main
import re
import socks
import socket
import json
import requests
import urllib.parse
import fake_useragent


if __name__ == "__main__":
    authdata = json.dumps({"email": "rasmygens@gmail.com", "password": "qbU-9kR-eZe-Ve6"})
    mysession = requests.session()
    response = mysession.post('https://leader-id.ru/api/v4/auth/login', data=authdata, headers={'User-Agent': 'Mozilla/5.0'})
    parsedata = mysession.post('https://leader-id.ru/profile', headers={'User-Agent': 'Mozilla/5.0'})
    #print(response)
    print(parsedata.text)