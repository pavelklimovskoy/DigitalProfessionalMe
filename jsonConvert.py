import json

# Определение цвета для сектора
def color_calc(check, skillType):
    # Массив цветов
    hardColors = ['#4188D2', '#3272B5', '#235C97', '#144679', '#05305B']  # 1-2, 3-4, 5-6, 7-8, >= 9
    softColors = ['#FFB240', '#D99632', '#B27923', '#8C5C14', '#653F05']  # 1-2, 3-4, 5-6, 7-8, >= 9

    if skillType == 'SoftSkill':
        if check == 1:
            filling = softColors[0]
        elif 2 <= check <= 4:
            filling = softColors[1]
        elif 5 <= check <= 6:
            filling = softColors[2]
        elif 7 <= check <= 8:
            filling = softColors[3]
        else:
            filling = softColors[4]
    else:  # HardSkill
        if check == 1:
            filling = hardColors[0]
        elif 2 <= check <= 4:
            filling = hardColors[1]
        elif 5 <= check <= 6:
            filling = hardColors[2]
        elif 7 <= check <= 8:
            filling = hardColors[3]
        else:
            filling = hardColors[4]

    return filling


# Конвертация Json
def json_convert(data):
    #jsonName = './static/data/cv/' + 'rchilli.json'

    #with open(jsonName, encoding='utf-8') as rchilliJson:
    #    data = json.load(rchilliJson)

    # Массив названий навыков для удаления дублей
    skillsArray = []

    # Структура Json
    mainArray = []
    mainDict = {'name': 'Me', 'children': []}  # Первый уровень

    # Массив типов умений
    firstType = []
    secondType = []

    for skill in data['ResumeParserData']['SegregatedSkill']:
        ontology = str(skill['Ontology']).split('>')

        if len(ontology) == 3:
            if ontology[0] not in firstType:
                firstType.append(ontology[0])

            if ontology[1] not in secondType:
                secondType.append(ontology[1])

    # Заполнение типов умений
    for typeSkill in firstType:
        childMain = {'name': typeSkill, 'id': '', 'fill': '', 'children': []}  # Второй уровень

        # Заполнение дочернего массива скиллов
        for skill in data['ResumeParserData']['SegregatedSkill']:
            ontologyMain = str(skill['Ontology']).split('>')

            if skill['Type'] == 'SoftSkill':
                typeIdFill = 'SoftSkill'
            else:
                typeIdFill = 'OperationalSkill'

            if ontologyMain[0] == typeSkill:
                childMain['id'] = typeIdFill

                tmp = {'name': ontologyMain[1], 'id': childMain['id'], 'value': '1', 'fill': '', 'children': []}

                for skillName in data['ResumeParserData']['SegregatedSkill']:
                    ontology = str(skillName['Ontology']).split('>')
                    if len(ontology) == 3:

                        skillSelf = {'name': ontology[2], 'id': childMain['id'], 'value': '1', 'fill': ''}

                        if ontology[1] == ontologyMain[1] and ontology[2] not in skillsArray:
                            tmp['children'].append(skillSelf)
                            skillsArray.append(ontology[2])

                if tmp not in childMain['children'] and len(tmp['children']) > 0:
                    childMain['children'].append(tmp)

        if len(childMain['children']) > 0:
            mainDict['children'].append(childMain)

    for type in mainDict['children']:
        skillCounter = 0

        for subType in type['children']:
            if subType['id'] == 'SoftSkill':  # SoftSkill
                filling = color_calc(len(subType['children']), 'SoftSkill')
            else:  # HardSkill
                filling = color_calc(len(subType['children']), 'OperationalSkill')

            subType['fill'] = filling

            for skill in subType['children']:
                skillCounter += 1

                if skill['id'] == 'SoftSkill':
                    filling = '#FFB240'
                else:
                    filling = '#4188D2'
                skill['fill'] = filling

        if type['id'] == 'SoftSkill':  # SoftSkill
            filling = color_calc(skillCounter, 'SoftSkill')
        else:  # HardSkill
            filling = color_calc(skillCounter, 'OperationalSkill')

        type['fill'] = filling

    mainArray.append(mainDict)

    # Запись нового Json файла
    #with open('./static/data/cv/sunburstDataUpdated.json', 'w') as chartJson:
    #    json.dump(mainArray, chartJson, sort_keys=False, indent=2)

    return mainArray