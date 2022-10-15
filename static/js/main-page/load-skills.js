let cookieId = document.cookie.match('(^|;)\\s*' + 'id' + '\\s*=\\s*([^;]+)')?.pop() || '',
    skillBlock = document.querySelector('#skillsBlock');

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

            if (localStorage.getItem('showDisabledSkills') == 'false') {
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
            disableSkill(skill.name)
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
function loadSkills() {
    let enabled = skillList.filter(skill => skill.enabled),
        disabled = skillList.filter(skill => !skill.enabled),
        i = 0;

    enabled.sort();
    disabled.sort();

    enabled.forEach(
        (skill) => { addSkill(skill, i); i++ });

    if (localStorage.getItem('showDisabledSkills') == 'false') {
        disabled.forEach(
            (skill) => { addSkill(skill, i); i++ });
    }
}