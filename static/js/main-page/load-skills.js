let cookieId = document.cookie.match('(^|;)\\s*' + 'id' + '\\s*=\\s*([^;]+)')?.pop() || '',
    skillBlock = document.querySelector('#skillsBlock');

// Смена состояний скиллов
function changeSkillState(skillId) {
    const skill = document.querySelector(`#${skillId}`);
    console.log(skill);
    let state;

    if (skill) {
        skill.remove();

        let skillClass;
        for (let i = 0; i < skill.classList.length; i++) {
            if (skill.classList[i].includes('skill')) {
                skillClass = skill.classList[i];
                break;
            }
        }

        if (skillClass != 'disabled-skill') {
            skill.classList.remove(skillClass);
            skill.classList.add('disabled-skill');

            skillBlock.append(skill);
            state = 0;
        }
        else {
            skill.classList.remove('disabled-skill');

            if (skill.id.includes('SoftSkill')) {
                skill.classList.add('soft-skill');
            } else {
                skill.classList.add('hard-skill');
            } 

            skillBlock.append(skill);
            state = 1;
        }

        let xhr = new XMLHttpRequest();
        xhr.open(
            'GET',
            `http://localhost:5000/changeSkillState?skillName=${skill.textContent}`,
            true
        );
        xhr.send();
    }

    return state;
}

// Добавление скилла
function addSkill(skill, i)
{
    let skillDiv = document.createElement("div");

    if (skill.enabled == false) {
        skillDiv.className = "badge bg-primary text-wrap disabled-skill";
    }
    else if (skill.id == "SoftSkill") {
        skillDiv.className = "badge bg-primary text-wrap soft-skill";
    }
    else {//if (skill.id == "OperationalSkill") {
        skillDiv.className = "badge bg-primary text-wrap hard-skill";
    }
    // } else {
    //     skillDiv.className = "badge bg-primary text-wrap unknown-skill";
    // }

    skillDiv.textContent = skill.name;

    skillDiv.id = `${skill.id}-${i}`;

    // Создание иконки переключения
    let iconButton = document.createElement("i");
    iconButton.className = "fa fa-close";

    // Создание кнопки переключения
    let delButton = document.createElement("button");
    delButton.className = "btn";
    delButton.id = i;

    // Кнопка становится красной при наведении мыши
    delButton.addEventListener("mouseover", (e) => {
        e.currentTarget.setAttribute("style", "background-color: red");
    });

    // Кнопка становится прозрачной при отведении мыши или нажатия на неё 
    delButton.addEventListener("mouseout", (e) => {
        e.currentTarget.setAttribute("style", "");
    });

    // Переключение состояния скиллов
    delButton.addEventListener("click", (e) => {
        e.currentTarget.setAttribute("style", "");

        let state = changeSkillState(`${skill.id}-${i}`);
        console.log('st: ', state);
        if (state == 0) {
            skill.enabled = false;
            disabledSkills.push(skill);
            redrawChart();
        } else {
            skill.enabled = true;
            disabledSkills.pop(skill);
            redrawChart(skill);
        }

    });

    // Добавление иконки к кнопке
    delButton.appendChild(iconButton);
    skillDiv.appendChild(delButton);
    skillBlock.appendChild(skillDiv);
}

// Загрузка скиллов
function loadSkills() {
    skillList.forEach(
        (skill, i) => addSkill(skill, i));
}