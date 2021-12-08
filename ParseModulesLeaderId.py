import codecs
import sys
from bs4 import BeautifulSoup
from urllib.request import urlopen, Request
from urllib.error import HTTPError
import random
import main
import re
import socket
import json
import requests
import urllib.parse
from urllib.request import urlopen
from selenium import webdriver
from selenium.webdriver import ActionChains, Keys
from selenium.webdriver.remote.webelement import WebElement
from bs4 import BeautifulSoup
import codecs
import time




def openTXT(name):
    f = codecs.open(name, "r", "utf_8_sig")
    data = f.read()
    bsObj = BeautifulSoup(data, "html.parser")
    f.close()
    return bsObj

dict = {}


def ParseData(id):
  driver = webdriver.Chrome('chromedriver')
  driver.get("https://leader-id.ru/users/" + str(id))

  driver.find_elements_by_class_name('login-button')[0].click()

  driver.find_elements_by_class_name('app-input__inner')[1].send_keys("rasmygens@gmail.com")
  driver.find_elements_by_class_name('app-input__inner')[2].send_keys("qbU-9kR-eZe-Ve6")

  driver.find_elements_by_class_name('app-input__inner')[2].send_keys(Keys.ENTER)

  time.sleep(1)
  driver.get("https://leader-id.ru/users/" + str(id))

  saveHtml = codecs.open(str(id) + ".html", 'w', "utf-8-sig")
  saveHtml.write(driver.page_source)
  saveHtml.close()
  driver.quit()


# Получение ключевых навыков
def getSkills(bsObj):
    skillsBlock = bsObj.find_all('div', {'class': '_1J3TOxrxEyk0'})

    skillTitle = []
    skillRate = []

    for i in range(len(skillsBlock)):
        title = skillsBlock[i].find('h4', class_='app-heading-4').get_text().replace("\r\n", "")
        title = title[6:-4]
        skillTitle.append(title)

        rate = skillsBlock[i].find('div', class_='UHAx9ui7_NpV').get_text()
        rate = rate[1:-1]
        skillRate.append(rate)

    dict['Skills'] = [{'Skill Title': skillTitle}, {'Skill Rate': skillRate}]

# Получение данных Leader Id
def LIDParse(id):
    #url = "https://leader-id.ru/users/" + id

    ParseData(id)

    name = str(id) + ".html"
    bsObj = openTXT(name)

    getSkills(bsObj)

    return dict

if __name__ == "__main__":
    pass
    #authdata = json.dumps({"email": "rasmygens@gmail.com", "password": "qbU-9kR-eZe-Ve6"})
    #headers = {
    #    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.85 YaBrowser/21.11.2.773 Yowser/2.5 Safari/537.36'
    #}
    #session = requests.Session()
    #session.headers.update(headers)
    #response = session.post('https://leader-id.ru/api/v4/auth/login', data=authdata)
    #pdata = session.get('https://leader-id.ru/users')
    #parsedata = session.post('https://leader-id.ru/profile', headers = {
    #'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 11_2_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.90 Safari/537.36'}, params=None)
    #print(response.json())
    #print(pdata.text)