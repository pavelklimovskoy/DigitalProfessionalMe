import json

# Soft Types of skills
soft_types = ['SoftSkill', 'Knowledge', 'Soft', 'Tool']

# Colors for skills
hard_colors = ['#4188D2', '#3272B5', '#235C97', '#144679', '#05305B']  # 1-2, 3-4, 5-6, 7-8, >= 9
soft_colors = ['#FFB240', '#D99632', '#B27923', '#8C5C14', '#653F05']  # 1-2, 3-4, 5-6, 7-8, >= 9


# Определение цвета для сектора
def color_calc(check, skill_type):
    if skill_type in soft_types:
        if check == 1:
            filling = soft_colors[0]
        elif 2 <= check <= 4:
            filling = soft_colors[1]
        elif 5 <= check <= 6:
            filling = soft_colors[2]
        elif 7 <= check <= 8:
            filling = soft_colors[3]
        else:
            filling = soft_colors[4]
    else:  # HardSkill
        if check == 1:
            filling = hard_colors[0]
        elif 2 <= check <= 4:
            filling = hard_colors[1]
        elif 5 <= check <= 6:
            filling = hard_colors[2]
        elif 7 <= check <= 8:
            filling = hard_colors[3]
        else:
            filling = hard_colors[4]

    return filling


# Конвертация Json
def json_convert(data):
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
                            'enabled': True, 'shortName': short_name, 'fill': '',
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
            filling = color_calc(len(sub_type['children']), sub_type['id'])

            sub_type['fill'] = filling

            for skill in sub_type['children']:
                skill_counter += 1

                if skill['id'] in soft_types:
                    filling = '#FFB240'
                else:
                    filling = '#4188D2'
                skill['fill'] = filling

        filling = color_calc(skill_counter, type['id'])

        type['fill'] = filling

    return [main_dict], skills_array


def timeline_parse(data):
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
