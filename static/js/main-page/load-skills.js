let skillId = 0;

// Удаление скиллов
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
    

    let cookieId = document.cookie.match('(^|;)\\s*' + 'id' + '\\s*=\\s*([^;]+)')?.pop() || '';
    let urlRequest = 'http://digitalprofessional.me:5000/getRchilliJson?id='+cookieId;

    fetch(urlRequest)
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
            delButton.addEventListener("mouseover", function( event ) {
                event.currentTarget.setAttribute("style", "background-color:red");
              }, false);

            delButton.addEventListener("mouseout", function( event ) {
                event.currentTarget.setAttribute("style", "");
              }, false);


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

// Добавления скиллов
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