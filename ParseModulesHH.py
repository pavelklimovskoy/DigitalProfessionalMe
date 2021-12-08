import sys
from bs4 import BeautifulSoup
from urllib.request import urlopen, Request
from urllib.error import HTTPError
import random
import re
import json
import requests
import urllib.parse
from main import *


# Открытие веб-страницы
#def openHTML(url):
#    url = url.encode('ascii', 'ignore').decode('ascii')
#    try:
#        html = urlopen(url)
#        bsObj = BeautifulSoup(html.read(), "html.parser")
#        return bsObj
#    except HTTPError as e:
#        print("Page not found")


def openHTML(url):
    url = url.encode('ascii', 'ignore').decode('ascii')
    bsObj = ""
    try:
        req = Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        html = urlopen(req)
        bsObj = BeautifulSoup(html.read(), "html.parser")
    except HTTPError as e:
        print("Page not found")
    return bsObj


dict = {}


# Получение названия профессии
def getTitle(bsObj):
    try:
        title = bsObj.find('div', {'data-qa': 'resume-block-position'})
        title = title.find('span', class_='resume-block__title-text')
        dict['Title'] = title.get_text()
    except:
        dict['Title'] = ""

# Получение ключевых навыков
def getSkills(bsObj):
    try:
        skillsBlock = bsObj.findAll('div', {'class': 'bloko-tag-list'})
        skills = skillsBlock[0].get_text(',').split(',')
        dict['Skills'] = skills
    except:
        dict['Skills'] = ""

# Получение образования
def getEdu(bsObj):
    try:
        eduBlock = bsObj.find('div', {'data-qa': 'resume-block-education'})
        eduBlock = eduBlock.find('div', class_='resume-block-item-gap')
        eduBlock = eduBlock.find('div', class_='bloko-columns-row')
        eduBlock = eduBlock.find_all('div', class_='resume-block-item-gap')
        years = []
        orgs = []
        specs = []
        for i in range(len(eduBlock)):
            year = eduBlock[i].find('div', class_='bloko-column bloko-column_xs-4 bloko-column_s-2 bloko-column_m-2 bloko-column_l-2')
            year = year.get_text().split('\n')
            years.append(year)

            org = eduBlock[i].find('div', {'data-qa': 'resume-block-education-name'}).get_text().split('\n')
            orgs.append(org)

            spec = eduBlock[i].find('div', {'data-qa': 'resume-block-education-organization'}).get_text().split('\n')
            specs.append(spec)
        dict['Education'] = [{'Year': years}, {'Organization': orgs}, {'Specialization': specs}]
    except:
        dict['Education'] = ""


# Получение компетенций
def getComptenece(bsObj):
    try:
        competenceBlock = bsObj.find('div', {'data-qa': 'resume-block-position'})
        competenceBlock = competenceBlock.find('div', class_='resume-block-item-gap')
        competenceBlock = competenceBlock.find('div', class_='bloko-gap bloko-gap_bottom')
        comp = competenceBlock.get_text(' ')
        dict['Competence'] = comp
    except:
        dict['Competence'] = ""


# Получение опыта работы
def getExperience(bsObj):
    try:
        # Получение общего времени работы
        totalTimeBlock = bsObj.find('div', {'data-qa': 'resume-block-experience'})
        totalTimeBlock = totalTimeBlock.find('div',
                                             class_='bloko-column bloko-column_xs-4 bloko-column_s-8 bloko-column_m-9 bloko-column_l-12')
        totalTimeBlock = totalTimeBlock.find('span', class_='resume-block__title-text resume-block__title-text_sub')
        totalTime = totalTimeBlock.get_text('').replace('Опыт работы ', '')

        # Получение опыта по каждому месту работы
        expBlock = bsObj.find('div', {'data-qa': 'resume-block-experience'})
        expBlock = expBlock.find('div', class_='resume-block-item-gap')
        expBlock = expBlock.find('div', class_='bloko-columns-row')
        expBlock = expBlock.find_all('div', class_='resume-block-item-gap')

        begins = []
        ends = []
        totalOnes = []
        orgs = []
        positions = []
        posDescs = []

        for i in range(len(expBlock)):
            expBlockDates = expBlock[i].find('div',
                                             class_='bloko-column bloko-column_xs-4 bloko-column_s-2 bloko-column_m-2 bloko-column_l-2')
            totalOne = expBlockDates.find('div', class_='bloko-text bloko-text_tertiary').get_text()
            totalOnes.append(totalOne)

            expBlockDates.find('div', class_='bloko-text bloko-text_tertiary').extract()
            dates = expBlockDates.get_text()

            dates.split('—')
            begins.append(dates.split(' — ')[0])
            ends.append(dates.split(' — ')[1])

            org = expBlock[i].find('div', class_='resume-block-container')
            org = org.find('div', class_='bloko-text bloko-text_strong').get_text().replace('\"', '')
            orgs.append(org)

            position = expBlock[i].find('div', class_='resume-block-container')
            position = position.find('div', {'data-qa': 'resume-block-experience-position'}).get_text()
            positions.append(position)

            posDesc = expBlock[i].find('div', class_='resume-block-container')
            posDesc = posDesc.find('div', {'data-qa': 'resume-block-experience-description'}).get_text(' ').replace('\n',
                                                                                                                    ' ')
            posDescs.append(posDesc)
        dict['Work Experience'] = [{'start_date': begins}, {'end_date': ends},
                                   {'Total Work-Time on the organization': totalOnes},
                                   {'Organization': orgs}, {'Position': positions}, {'Position Describe': posDescs},
                                   {'Total Experience': totalTime}]
    except:
        dict['Work Experience'] = ""


# Получение информации "обо мне"
def getInfAbout(bsObj):
    try:
        aboutBlock = bsObj.find('div', {'data-qa': 'resume-block-skills'}, class_='resume-block')
        aboutBlock = aboutBlock.find('div', class_='resume-block-item-gap')
        dict['About me'] = aboutBlock.get_text(' ').replace('\n', ' ')
    except:
        dict['About me'] = ""

def parseList(findWord):
    resumes = "https://hh.ru/search/resume?area=76&isDefaultArea=true&exp_period=all_time&logic=normal&pos=full_text&fromSearchLine=true&clusters=True&ored_clusters=True&order_by=relevance&text=" + urllib.parse.quote_plus(findWord)
    bsObjResumesList = openHTML(resumes)

    resumeBlock = bsObjResumesList.find('div', class_='resume-serp')
    resumeBlock = resumeBlock.find('div', class_='bloko-column bloko-column_s-8 bloko-column_m-9 bloko-column_l-13')
    resumeBlock = resumeBlock.find('div', class_='resume-serps')
    resumeBlock = resumeBlock.find_all('div', {'data-qa': 'resume-serp__resume'})

    resList = []
    resDict = {}
    for i in range(len(resumeBlock)):
        link = resumeBlock[i].find('a', class_='resume-search-item__name').get('href')
        resList.append(link)
    resDict['Links'] = resList
    return resDict


def dictFromUrl(id):
    url = "https://hh.ru/resume/" + id
    bsObj = openHTML(url)

    getTitle(bsObj)
    getSkills(bsObj)
    getEdu(bsObj)
    getComptenece(bsObj)
    getExperience(bsObj)
    getInfAbout(bsObj)

    return dict


if __name__ == "__main__":
    pass
    #dictFromUrl("f176b5f600061272f10047b466656f47506741")