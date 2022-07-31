let cookieId = document.cookie.match('(^|;)\\s*' + 'id' + '\\s*=\\s*([^;]+)')?.pop() || '',
    skillBlock = document.querySelector('#skillsBlock');

// Смена состояний скиллов
function changeSkillState(skillId) {
    const skill = document.querySelector(`#${skillId}`),
        ask = confirm(`Change state of the skill: ${skill.textContent}?`);

    if (ask && skill) {
        skill.remove();

        let classId = '';
        for (let i = 0; i < skill.classList.length; i++) {
            if (skill.classList[i].includes('skill')) {
                classId = skill.classList[i];
                break;
            }
        }
        console.log(skill.textContent);
        fetch(`http://digitalprofessional.me:5000/changeSkillState?skillName=${skill.textContent}`, {mode: 'no-cors'})
            .then(() => {
                if (classId != 'disabled-skill') {
                    skill.classList.remove(classId);
                    skill.classList.add('disabled-skill');
                    skillBlock.append(skill);
                }
                else {
                    skill.classList.remove('disabled-skill');
                    
                    if (skill.id.includes('SoftSkill')) {
                        skill.classList.add('soft-skill');
                    } else if (skill.id.includes('OperationalSkill')) {
                        skill.classList.add('hard-skill');
                    }
                    
                    skillBlock.append(skill);
                }
            });
            // .then(setTimeout(() => {
            //     chart.draw();
            //     console.log('TIMER');
            // }, 5000));
    }
}

function loadSkills(skillList, redrawChart, filteringData) {
    skillList.forEach(
        (skill, i) => {
            let skillDiv = document.createElement("div");

            if (skill.enabled == false) {
                skillDiv.className = "badge bg-primary text-wrap disabled-skill";
                skillDiv.textContent = skill.name;
            }
            else if (skill.id == "SoftSkill") {
                skillDiv.className = "badge bg-primary text-wrap soft-skill";
                skillDiv.textContent = skill.name;
            }
            else if (skill.id == "OperationalSkill") {
                skillDiv.className = "badge bg-primary text-wrap hard-skill";
                skillDiv.textContent = skill.name;
            }

            skillDiv.id = `${skill.id}-${i}`;

            // Создание иконки удаления
            let iconButton = document.createElement("i");
            iconButton.className = "fa fa-close";

            // Создание кнопки удаления
            let delButton = document.createElement("button");
            delButton.className = "btn";
            delButton.id = i;

            delButton.addEventListener("mouseover", (e) => {
                e.currentTarget.setAttribute("style", "background-color: red");
            });

            delButton.addEventListener("mouseout", (e) => {
                e.currentTarget.setAttribute("style", "");
            });

            // Удаление по клику по кнопке
            delButton.addEventListener("click", () => {
                filteringData.push(skill);
                changeSkillState(`${skill.id}-${delButton.id}`);
                redrawChart(filteringData);
            });

            // Добавление иконки к кнопке
            delButton.appendChild(iconButton);
            skillDiv.appendChild(delButton);
            skillBlock.appendChild(skillDiv);
        }
    );
}

// Добавления скиллов
// function addSkiilButton() {
//     let skillName = prompt("Enter skill name", "Python");

//     let skillBlock = document.getElementById("skillsBlock");

//     let skillDiv = document.createElement("div");

//     skillDiv.className = "badge bg-primary text-wrap";
//     skillDiv.id = "skills-" + skillId;
//     skillDiv.title = skillName;

//     // Создание иконки удаления
//     let iconButton = document.createElement("i");
//     iconButton.className = "fa fa-close";

//     // Создание кнопки удаленич
//     let delButton = document.createElement("button");
//     delButton.className = "btn";
//     delButton.id = skillId;

//     // Удаление по клику по кнопке
//     delButton.addEventListener("click", () => changeSkillState(`skills-${delButton.id}`));

//     // Добавление иконки к кнопке
//     delButton.appendChild(iconButton);
//     skillDiv.innerHTML = skillName;
//     skillDiv.appendChild(delButton);
//     skillBlock.appendChild(skillDiv);
// }