from urllib.request import urlopen
import requests
from bs4 import BeautifulSoup


def parse_coursera_url(url):
    try:
        html = urlopen(url)
        bs = BeautifulSoup(html.read(), 'html.parser')
        div_skills = bs.find_all("ul", {"class": "css-uqope5"})
        div_course_name = bs.find_all("h2", {"class": "course-name"})
        div_date = bs.find_all("div", {"class": "course-details"})
        # div_company_name = bs.find_all("div", {"h3": "course-name-header"})

        response = dict()

        if div_skills:
            children = div_skills[0].find_all("li")
            if children:
                skills = [child.get_text() for child in children]
                response['skills'] = skills

        if div_course_name:
            course_name = div_course_name[0].get_text()
            if course_name:
                response['courseName'] = course_name

        if div_date:
            date = div_date[0].find_all('p')[0].get_text()
            if date:
                response['date'] = date

        response['url'] = ''
        response['userName'] = ''
        return response
    except Exception as e:
        print(e)


def parse_stepik_url(url):
    try:
        certificate_id = url.split('/')[-1]
        req_url = f'https://stepik.org/api/certificates/{certificate_id}'
        headers = {
            'Content-Type': 'application/json'
        }
        response = requests.request("GET", req_url, headers=headers).json()['certificates'][0]
        resp = {'date': response['issue_date'], 'url': response['url'], 'userName': response['saved_fullname'],
                'courseName': response['course_title']}
        return resp
    except Exception as e:
        print(e)


# def parse_udemy_url(url):
#     try:
#         html = urlopen(url)
#         bs = BeautifulSoup(html.read(), 'html.parser')
#         print(bs)
#         url = bs.find_all("img", {"data-purpose": "certificate-img"})
#         print(url)
#
#
#         #return response
#     except Exception as e:
#         print(e)