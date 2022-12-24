let skillBlock = document.querySelector('#skillsBlock');

// Смена состояний скиллов
function changeSkillState(skillId) {
    const skill = document.querySelector(`#${skillId}`);
    let state;

    if (skill) {
        let skillClass;

        for (let i = 0; i < skill.classList.length; i++) {
            if (skill.classList[i].includes('skill')) {
                skillClass = skill.classList[i];
                break;
            }
        }

        if (skillClass != 'disabled-skill') {
            skill.remove();

            skill.classList.remove(skillClass);
            skill.classList.add('disabled-skill');

            console.log(skill);
            skill.childNodes[1].childNodes[0].src = '../static/icons/button-off.png';

            if (localStorage.getItem('hideDisabledSkills') == 'false') {
                skillBlock.append(skill);
            }

            state = 0;
        }
        else {
            skill.classList.remove('disabled-skill');

            if (skill.id.includes('SoftSkill') || skill.id.includes('Soft') || skill.id.includes('Knowledge') || skill.id.includes('BehaviorSkills')) {
                skill.classList.add('soft-skill');
            } else {
                skill.classList.add('hard-skill');
            }

            console.log(skill);
            try {
                skill.remove();
                skill.childNodes[1].childNodes[0].src = '../static/icons/button-on.png';
                document.querySelectorAll('.disabled-skill')[0].before(skill);
            }
            catch {
                skill.childNodes[1].childNodes[0].src = '../static/icons/button-on.png';
                skillBlock.append(skill);
            }

            state = 1;
        }

        // Переключение состояния скилла в БД
        postData(`${baseUrl}/changeSkillState`, { skill: skill.textContent });
    }

    return state;
}

// Добавление скилла
function addSkill(skill, i) {
    let skillDiv = document.createElement('div');

    if (skill.enabled == false) {
        skillDiv.className = 'badge bg-primary text-wrap disabled-skill';
    }
    else if (skill.id.includes('SoftSkill') || skill.id.includes('Knowledge') || skill.id.includes('BehaviorSkills')) {
        skillDiv.className = 'badge bg-primary text-wrap soft-skill';
    }
    else {//if (skill.id == "OperationalSkill") {
        skillDiv.className = 'badge bg-primary text-wrap hard-skill';
    }
    // } else {
    //     skillDiv.className = "badge bg-primary text-wrap unknown-skill";
    // }

    skillDiv.textContent = skill.name;

    skillDiv.id = `${skill.id}-${i}`;

    // skillDiv.addEventListener('mouseenter', (e) => {
    //     // Создание иконки переключения
    //     let iconButton = document.createElement("i");
    //     iconButton.className = "fa fa-close";

    //     // Создание кнопки переключения
    //     let delButton = document.createElement("button");
    //     delButton.className = "btn";
    //     delButton.id = i;


    //     // Кнопка становится красной при наведении мыши
    //     delButton.addEventListener("mouseover", (e) => {
    //         e.currentTarget.setAttribute("style", "background-color: red");
    //     });

    //     // Кнопка становится прозрачной при отведении мыши или нажатия на неё 
    //     delButton.addEventListener("mouseout", (e) => {
    //         e.currentTarget.setAttribute("style", "");
    //     });

    //     // Переключение состояния скиллов
    //     delButton.addEventListener("click", (e) => {
    //         e.currentTarget.setAttribute("style", "");

    //         let state = changeSkillState(`${skill.id}-${i}`);
    //         console.log('st: ', state);
    //         if (state == 0) {
    //             skill.enabled = false;
    //             disabledSkills.push(skill);
    //             disableSkill(skill.name)
    //         } else {
    //             skill.enabled = true;
    //             disabledSkills.pop(skill);
    //             enableSkill(skill);
    //         }
    //     });

    //     delButton.appendChild(iconButton);
    //     skillDiv.appendChild(delButton);    

    //     skillDiv.addEventListener('mouseleave', (e) => {
    //         skillDiv.removeChild(delButton);
    //     });
    // });


    // Создание иконки переключения
    let iconButton;
    iconButton = document.createElement('img');
    if (skill.enabled) {
        iconButton.src = '../static/icons/button-on.png';
    }
    else {
        iconButton.src = '../static/icons/button-off.png';
    }
    iconButton.style.height = '1rem';
    //let iconButton = document.createElement('i');
    //iconButton.className = 'fa fa-refresh';
    //iconButton.style = 'color:white!important';

    // Создание кнопки переключения
    let delButton = document.createElement('button');
    delButton.className = 'btn';
    delButton.id = i;

    // Кнопка становится красной при наведении мыши
    delButton.addEventListener('mouseover', (e) => {
        e.currentTarget.setAttribute('style', 'background-color: red');
    });

    // Кнопка становится прозрачной при отведении мыши или нажатия на неё 
    delButton.addEventListener('mouseout', (e) => {
        e.currentTarget.setAttribute('style', '');
    });

    // Переключение состояния скиллов
    delButton.addEventListener('click', (e) => {
        e.currentTarget.setAttribute('style', '');

        let state = changeSkillState(`${skill.id}-${i}`);

        if (state == 0) {
            skill.enabled = false;
            disabledSkills.push(skill);
            disableSkill(skill.name);
        } else {
            skill.enabled = true;
            disabledSkills.pop(skill);
            enableSkill(skill);
        }
    });

    // Добавление иконки к кнопке
    delButton.appendChild(iconButton);
    skillDiv.appendChild(delButton);
    skillBlock.appendChild(skillDiv);
}

// Загрузка скиллов
function loadSkills(topSkills = '') {
    console.log(skillList);

    let enabled = skillList.filter(skill => skill.enabled),
        disabled = skillList.filter(skill => (skill.enabled === false));

    console.log(disabled);

    console.log(enabled);
    console.log(topSkills);

    if (topSkills && localStorage.getItem('isCVUploadedFirstly') == 'true') {
        topSkills.forEach(skill => {
            if (skill) {
                const elemE = enabled.find(skillObj => skillObj.name == skill[0]);
                const elemD = disabled.find(skillObj => skillObj.name == skill[0]);
                //console.log(elemD);

                if (!elemE && elemD) {
                    disabled.pop(elemD);
                    elemD.enabled = true;
                    enabled.push(elemD);
                    enableSkill(elemD);
                    // Переключение состояния скилла в БД
                    postData(`${baseUrl}/changeSkillState`, { skill: skill[0] });
                }
            }
        });
        localStorage.setItem('isCVUploadedFirstly', 'false');
    }

    enabled.sort();
    disabled.sort();

    let i = 0;

    enabled.forEach(skill => { addSkill(skill, i); i++; });

    if (localStorage.getItem('hideDisabledSkills') == 'false') {
        showDisabledSkills();
    }
}


// Просчет веса скиллов
function calcSkillsWeightAndShowIt() {
    const urlRequest = `${baseUrl}/getRchilliSkills`;
    postData(urlRequest)
        .then(response => {
            return response.json();
        })
        .then(data => {
            console.log(data);
            if (data != 404) {
                let skillsSize = data.length;
                let skillsWeights = {};
                let skillsIn = {};
                let skillsLastUsed = {};
                let skillsExp = {};

                data.map(skill => {
                    const skillName = skill.FormattedName;
                    if (skillName != '') {
                        if (skillName in skillsIn) {
                            skillsIn[skillName] += 1;
                        }
                        else {
                            skillsIn[skillName] = 1;
                        }
                    }
                });

                console.log('Количество вхождений: ', skillsIn);

                data.map(skill => {
                    const skillName = skill.FormattedName;
                    if (skillName != '') {
                        if (skillName in skillsWeights) {
                            skillsWeights[skillName] += (1 / skillsSize);
                        }
                        else {
                            skillsWeights[skillName] = (1 / skillsSize);
                        }

                        const n = +skill.ExperienceInMonths;
                        if (n) {
                            // switch (true) {
                            //     case (n <= 6):
                            //         skillsWeights[skillName] += 0.1;
                            //         break;
                            //     case (n <= 12):
                            //         skillsWeights[skillName] += 0.25;
                            //         break;
                            //     case (n > 12):
                            //         skillsWeights[skillName] += 0.5;
                            //         break;
                            // }

                            if (skillName in skillsExp) {
                                skillsExp[skillName] = Math.max(skillsExp[skillName], n);
                            }
                            else {
                                skillsExp[skillName] = n;
                            }
                        }
                        if (skill.LastUsed != "") {
                            const nowDate = new Date();
                            const m = skill.LastUsed.slice(3, 5),
                                d = skill.LastUsed.slice(0, 2),
                                y = skill.LastUsed.slice(-4);

                            const endDate = new Date(`${m}.${d}.${y}`);
                            const diff = nowDate - endDate;

                            const hours = Math.floor(diff / 3.6e6);
                            const mDiff = Math.trunc(hours / 730);

                            // if (mDiff <= 12) {
                            //     skillsWeights[skillName] += 0.25;
                            // }
                            if (skillName in skillsLastUsed) {
                                skillsLastUsed[skillName] = Math.min(skillsLastUsed[skillName], mDiff);
                            }
                            else {
                                skillsLastUsed[skillName] = mDiff;
                            }
                        }
                    }
                });

                for (let key in skillsLastUsed) {
                    if (skillsLastUsed[key] <= 12) {
                        skillsWeights[key] += 0.25;
                    }
                }

                for (let key in skillsExp) {
                    switch (true) {
                        case (skillsExp[key] <= 6):
                            skillsWeights[key] += 0.1;
                            break;
                        case (skillsExp[key] <= 12):
                            skillsWeights[key] += 0.25;
                            break;
                        case (skillsExp[key] > 12):
                            skillsWeights[key] += 0.5;
                            break;
                    }
                }

                console.log('Минимальная разница текущей даты и последней даты использования скилла: ', skillsLastUsed);
                console.log('Максимальное количество месяцев использования скилла: ', skillsExp);
                console.log('Веса: ', skillsWeights);

                let topSkills = Object.keys(skillsWeights).map(function (key) {
                    return [key, skillsWeights[key]];
                });

                topSkills.sort(function (first, second) {
                    return second[1] - first[1];
                });

                loadSkills(topSkills.slice(0, Math.min(10, topSkills.length)));

                //console.log(topSkills.slice(0, 10));
                //console.log(topSkills[0][0]);
            }
        });
}