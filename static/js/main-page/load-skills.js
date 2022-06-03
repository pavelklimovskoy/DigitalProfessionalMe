let skillId = 0;

function deleteSkill(skillId)
{
    let elem = document.getElementById(skillId);


    let ask = confirm("Delete skill: " + elem.textContent + "?");

    if(ask == true)
    {
        if(elem != null)
        {
            elem.remove();
        }
    }
}

function loadSkills()
{
    let skillList = new Map();

    let jsonWithSkills = null;

    fetch("http://digitalprofessional.me:5000/getJson")
    .then((response) => {
        return response.json();
    })
    .then((data) => {
        jsonWithSkills = data;

        skillsData = jsonWithSkills["ResumeParserData"]["SegregatedSkill"];

        skillsData.forEach(skill => {

            if(skill["Ontology"] != "")
            {
                let skillName = skill["Ontology"].split('>')[2];
                let skillType = skill["Type"];

                skillList.set(skillName, skillType);
            }
        });

        let skillBlock = document.getElementById("skillsBlock");

    skillList.forEach(
        (type, name) => {
            let skillDiv = document.createElement("div");

            if(type == "SoftSkill")
            {
                skillDiv.className = "badge bg-primary text-wrap soft-skill";
            }
            if(type == "OperationalSkill")
            {
                skillDiv.className = "badge bg-primary text-wrap hard-skill";
            }



            skillDiv.id = "skills-" + skillId;
            skillDiv.title = name;

            //skillDiv.onclick = ()=> {skillDiv.remove()};


            let skillText = name;

            // if(skill.length <= 10) {
            //     skillText = skill;
            // }
            // else{
            //     skillText = skill.slice(0, 7) + "...";
            // }

            // Создание иконки удаления
            let iconButton = document.createElement("i");
            iconButton.className = "fa fa-close";

            // Создание кнопки удаленич
            let delButton = document.createElement("button");
            delButton.className = "btn";
            delButton.id = skillId;

            // Удаление по клику по кнопке
            delButton.onclick = () => deleteSkill("skills-" + delButton.id);

            // Добавление иконки к кнопке
            delButton.appendChild(iconButton);

            skillDiv.innerHTML = skillText

            skillDiv.appendChild(delButton);

            skillBlock.appendChild(skillDiv);

            skillId++;
        }
    );

    });

}

function addSkiilButton()
{
    let skillName = prompt("Enter skill name", "Python");

    let skillBlock = document.getElementById("skillsBlock");

    let skillDiv = document.createElement("div");

    skillDiv.className = "badge bg-primary text-wrap";
    skillDiv.id = "skills-" + skillId;
    skillDiv.title = skillName;



    // Создание иконки удаления
    let iconButton = document.createElement("i");
    iconButton.className = "fa fa-close";

    // Создание кнопки удаленич
    let delButton = document.createElement("button");
    delButton.className = "btn";
    delButton.id = skillId;

    // Удаление по клику по кнопке
    delButton.onclick = () => deleteSkill("skills-" + delButton.id);

    // Добавление иконки к кнопке
    delButton.appendChild(iconButton);

    skillDiv.innerHTML = skillName;

    skillDiv.appendChild(delButton);

    skillBlock.appendChild(skillDiv);

    skillId++;
}