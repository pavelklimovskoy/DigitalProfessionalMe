import sys
from bs4 import BeautifulSoup
from urllib.request import urlopen
from urllib.error import HTTPError
import random
import main
import re
import json
import urllib.parse

def openHTML(url):
    url = url.encode('ascii', 'ignore').decode('ascii')
    try:
        html = urlopen(url)
        bsObj = BeautifulSoup(html.read(), "html.parser")
        return bsObj
    except HTTPError as e:
        print("Page not found")

#def getInfAbout(url):
#    about = bsObj.findAll("div", {"data-qa": "resume-block-skills"})
#    for line in about:
#        print("About Me: ", line.get_text(' '))

#def getExperience(url):
#    exp = bsObj.findAll("div", {"data-qa": "resume-block-experience"})
#    for line in exp:
#        print("Experience: ", line.get_text(' '))

#def getLanguages(url):
#    lang = bsObj.findAll("div", {"data-qa": "resume-block-additional"})
#    for line in lang:
#        print("Additional: ", line.get_text(' '))

resumeList = []

def getParseList(url):
    resumes = bsObj.findAll("div", {"class": "resume-serps"})
    for line in resumes[0]:
        try:
            link = "https://rostov.hh.ru" + line.find('a', class_='resume-search-item__name').get('href')
            resumeList.append(link)
        except:
            pass

def getParsePage():
    getParseList(urlList)
    url = resumeList[random.randint(0, len(resumeList))]
    return url

if __name__ == "__main__":
    dict = {}

    url = "https://rostov.hh.ru/resume/87f32e4d000339c37e0039ed1f4d496b635065"
    bsObj = openHTML(url)

    # Название профессии
    titles = bsObj.findAll("div", {"class": "resume-block__title-text-wrapper"})
    for title in titles[0]:
        dict["Title"] = title.get_text(' ')

    # Получение навыков
    try:
        skillsBlock = bsObj.findAll("div", {"class": "bloko-tag-list"})
        for skill in skillsBlock[0]:
            skills = skillsBlock[0].get_text(',').split(',')
            dict["Skills"] = skills
    except:
        dict["Skills"] = None

    # Получение образования
    try:
        eduBlock = bsObj.find('div', {'data-qa': 'resume-block-education'}).find("div", class_="resume-block-item-gap").\
            find("div", class_="bloko-columns-row")
        for line in eduBlock:
            print("Education: ", line.get_text('\n').split('\n'))
            edu = eduBlock.get_text('\n').split('\n')
            dict["Education"] = edu
    except:
        dict["Education"] = None

    # Получение компетенций
    try:
        competenceBlock = bsObj.find("div", {"class": "resume-block-item-gap"}).find("div", {"class": "bloko-columns-row"}).\
            find("div", {"class": "bloko-column bloko-column_xs-4 bloko-column_s-8 bloko-column_m-9 bloko-column_l-12"}).\
            find("div", {"class": "resume-block-container"}).find("div", {"bloko-gap bloko-gap_bottom"})
        for line in competenceBlock:
            #print("Competence: ", line.get_text(',').split(','))
            comp = competenceBlock.get_text(',').split(',')
            dict["Competence"] = comp
    except:
        dict["Competence"] = None

    #Получение опыта работы
    try:
        wholeTime = ""
        expBlockWhole = bsObj.find("div", {"data-qa": "resume-block-experience"})\
            .find('span', class_='resume-block__title-text resume-block__title-text_sub')
        for line in expBlockWhole:
            wholeTime += line.get_text().replace('\xa0', ' ')
        #print(wholeTime)
        dict["Experience"] = wholeTime
        #...
    except:
        dict["Experience"] = None

    print(dict)

    #json_object = json.dumps(dict)
    #print(json_object)