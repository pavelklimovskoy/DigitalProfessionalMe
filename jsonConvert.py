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
    secondType = []

    for skill in data['ResumeParserData']['SegregatedSkill']:
        ontology = str(skill['Ontology']).split('>')

        if len(ontology) == 3:
            if ontology[0] not in first_type:
                first_type.append(ontology[0])

            if ontology[1] not in secondType:
                secondType.append(ontology[1])

    # Заполнение типов умений
    for typeSkill in first_type:
        childMain = {
            'name': typeSkill, 'id': '', 'fill': '',
            'parent': 'Me', 'children': []
        }  # Второй уровень

        # Заполнение дочернего массива скиллов
        for skill in data['ResumeParserData']['SegregatedSkill']:
            ontologyMain = str(skill['Ontology']).split('>')

            if ontologyMain[0] == typeSkill:
                childMain['id'] = skill['Type']

                tmp = {
                    'name': ontologyMain[1], 'id': childMain['id'],
                    'value': '1', 'fill': '', 'parent': typeSkill,
                    'children': []
                }

                for skillName in data['ResumeParserData']['SegregatedSkill']:
                    ontology = str(skillName['Ontology']).split('>')
                    if len(ontology) == 3:
                        shortName = ontology[2]

                        if len(shortName) > 5:
                            shortName = f'{ontology[2][:6]}...'

                        skillSelf = {
                            'name': ontology[2], 'id': childMain['id'], 'value': '1',
                            'enabled': True, 'shortName': shortName, 'fill': '',
                            'grandParent': typeSkill, 'parent': ontologyMain[1]
                        }

                        if ontology[1] == ontologyMain[1] and ontology[2] not in skills_array:
                            tmp['children'].append(skillSelf)
                            skills_array.append(ontology[2])

                if tmp not in childMain['children'] and len(tmp['children']) > 0:
                    childMain['children'].append(tmp)

        if len(childMain['children']) > 0:
            main_dict['children'].append(childMain)

    for type in main_dict['children']:
        skillCounter = 0

        for subType in type['children']:
            filling = color_calc(len(subType['children']), subType['id'])

            subType['fill'] = filling

            for skill in subType['children']:
                skillCounter += 1

                if skill['id'] in soft_types:
                    filling = '#FFB240'
                else:
                    filling = '#4188D2'
                skill['fill'] = filling

        filling = color_calc(skillCounter, type['id'])

        type['fill'] = filling

    return [main_dict]
