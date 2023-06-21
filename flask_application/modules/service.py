# -*- coding: utf-8 -*-

"""
    Служебные модули для поддержания работы сервера

    28.05.2023
"""

import sys

import pdfkit


class ServiceContainer:
    __instance = None

    def __init__(self):
        if not ServiceContainer.__instance:
            # Soft Types of skills
            self.soft_types = ['SoftSkill', 'Knowledge', 'Soft']

            # Colors for skills
            self.hard_colors = ['#4188D2', '#3272B5', '#235C97', '#144679', '#05305B']  # 1-2, 3-4, 5-6, 7-8, >= 9
            self.soft_colors = ['#FFB240', '#D99632', '#B27923', '#8C5C14', '#653F05']  # 1-2, 3-4, 5-6, 7-8, >= 9

    @classmethod
    def get_instance(cls):
        if not cls.__instance:
            cls.__instance = ServiceContainer()
        return cls.__instance

    def color_calc(self, check, skill_type):
        """
        Определение цвета для сектора

        :param check:
        :param skill_type:
        :return:
        """
        if skill_type in self.soft_types:
            if check == 1:
                filling = self.soft_colors[0]
            elif 2 <= check <= 4:
                filling = self.soft_colors[1]
            elif 5 <= check <= 6:
                filling = self.soft_colors[2]
            elif 7 <= check <= 8:
                filling = self.soft_colors[3]
            else:
                filling = self.soft_colors[4]
        else:  # HardSkill
            if check == 1:
                filling = self.hard_colors[0]
            elif 2 <= check <= 4:
                filling = self.hard_colors[1]
            elif 5 <= check <= 6:
                filling = self.hard_colors[2]
            elif 7 <= check <= 8:
                filling = self.hard_colors[3]
            else:
                filling = self.hard_colors[4]

        return filling

    def json_convert(self, data):
        """
        Конвертация Json
        :param data:
        :return:
        """
        # Массив названий навыков для удаления дублей
        skills_array = []

        main_dict = {'name': 'Me', 'children': []}  # Первый уровень

        # Массив типов умений
        first_type = []
        second_type = []

        for skill in data['ResumeParserData']['SegregatedSkill']:
            ontology = str(skill['Ontology']).split('>')

            if len(ontology) == 3:
                if ontology[0] not in first_type:
                    first_type.append(ontology[0])

                if ontology[1] not in second_type:
                    second_type.append(ontology[1])

        # Заполнение типов умений
        for type_skill in first_type:
            child_main = {
                'name': type_skill, 'id': '', 'fill': '',
                'parent': 'Me', 'children': []
            }  # Второй уровень

            # Заполнение дочернего массива скиллов
            for skill in data['ResumeParserData']['SegregatedSkill']:
                ontology_main = str(skill['Ontology']).split('>')

                if ontology_main[0] == type_skill:
                    child_main['id'] = skill['Type']

                    tmp = {
                        'name': ontology_main[1], 'id': child_main['id'],
                        'value': '1', 'fill': '', 'parent': type_skill,
                        'children': []
                    }

                    for skillName in data['ResumeParserData']['SegregatedSkill']:
                        ontology = str(skillName['Ontology']).split('>')
                        if len(ontology) == 3:
                            short_name = skillName['FormattedName']

                            if len(short_name) > 5:
                                short_name = f'{short_name[:6]}...'

                            skill_self = {
                                'name': skillName['FormattedName'], 'id': child_main['id'], 'value': '1',
                                'enabled': False, 'shortName': short_name, 'fill': '',
                                'grandParent': type_skill, 'parent': ontology_main[1]
                            }

                            if ontology[1] == ontology_main[1] and skillName['FormattedName'] not in skills_array:
                                tmp['children'].append(skill_self)
                                skills_array.append(skillName['FormattedName'])

                    if tmp not in child_main['children'] and len(tmp['children']) > 0:
                        child_main['children'].append(tmp)

            if len(child_main['children']) > 0:
                main_dict['children'].append(child_main)

        for type in main_dict['children']:
            skill_counter = 0

            for sub_type in type['children']:
                filling = self.color_calc(len(sub_type['children']), sub_type['id'])

                sub_type['fill'] = filling

                for skill in sub_type['children']:
                    skill_counter += 1

                    if skill['id'] in self.soft_types:
                        filling = '#FFB240'
                    else:
                        filling = '#4188D2'
                    skill['fill'] = filling

            filling = self.color_calc(skill_counter, type['id'])

            type['fill'] = filling

        return [main_dict], skills_array

    def timeline_parse(self, data):
        qualification_events = []
        experience_events = []
        certifications = []

        counter = 0
        for study in data['ResumeParserData']['SegregatedQualification']:
            event = {'period': study['FormattedDegreePeriod'],
                     'name': study['Institution']['Name'],
                     'id': counter}
            qualification_events.append(event)
            counter += 1

        counter = 0
        for job in data['ResumeParserData']['SegregatedExperience']:
            event = {'endDate': job['EndDate'],
                     'startDate': job['StartDate'],
                     'position': job['JobProfile']['FormattedName'],
                     'employer': job['Employer']['EmployerName'],
                     'id': counter}

            experience_events.append(event)
            counter += 1

        main = {
            'qualificationEvents': qualification_events,
            'experienceEvents': experience_events,
            'certifications': certifications
        }

        return main

    def check_python_version(self) -> None:
        """
        Функция для проверки версии интерпретатора Python
        :return:
        """
        major = sys.version_info.major
        minor = sys.version_info.minor

        if major < 3 or minor < 10:
            raise Exception("Неверная версия Python, необходима версия старше 3.10")

    def save_pdf(self, url: str, file_name: str) -> None:
        """
        Сохранение pdf
        :param url:
        :param file_name:
        :return:
        """
        pdfkit.from_url(url, f'static/data/cv/{file_name}')
