// Заполнение текстовых полей при запуске
let findWord = "1";
let jsonRespons;

// Действия при открытии страницы
window.onload = function() {
    // Полчение поискового слова
    getWord();

    // Получение 20 ссылок по ключевому слову
    loadURLs();
}

// Выгразка 20 ссылок по поисковому слову
function loadURLs()
{
    // Удаление дочерних элементов
    let linksBlock = document.getElementById("resumes-links");
    while (linksBlock.firstChild)
    {
        linksBlock.removeChild(linksBlock.firstChild);
    }


    document.getElementById("input-url").value = "";

    let getUrl = new XMLHttpRequest();
    getUrl.open("GET", "/getPageForParse/" + findWord, true);
    getUrl.responseType = 'json';
    getUrl.onload = function ()
    {
        jsonRespons = getUrl.response;

        var options = '';
        for(let i = 0; i < getUrl.response["Links"].length; i++)
        {
            options += "<option value=https://hh.ru" +  getUrl.response["Links"][i] + " />"
        }
        document.getElementById('resumes-links').innerHTML = options;
    }
    getUrl.send(null); 
}

// Выгрузка поискового слова
function getWord() {
    let getFindWord = new XMLHttpRequest();
    getFindWord.open("GET", "/getFindWord", false);
    getFindWord.onload = function ()
    {
        document.getElementById('change-word').placeholder = "Current search phrase: " + getFindWord.responseText;
        document.getElementById('change-word').value = "";
        findWord = getFindWord.responseText;
    }

    getFindWord.send(null);
}


// Заргузка нового поискового слова
function loadNewWord() {
    let newWord = document.getElementById('change-word').value;
    let loadFindWord = new XMLHttpRequest();
    loadFindWord.open("GET", "/newFindWord/" + newWord, false);
    loadFindWord.onload = function ()
    {
        console.log("new word loaded");
        getWord();

        loadURLs();
    }
    
    loadFindWord.send(null);
}

// Добавление iframe с резюме
function addFrame(id) {
    try {
        document.getElementById("frame-id").remove();
    }
    catch (e) {
        console.log("Frame ещё не создан");
    }

    let frame = document.createElement("iframe");
    frame.id = "frame-id";
    frame.setAttribute("src", "/templates/" + id);
    frame.style.width = "100%";
    frame.style.height = "480px";

    let container = document.getElementById("iframe-cont");
    container.appendChild(frame);
}

// Нанесение Timeline
function addTimeLine()
{
    try {
        document.getElementById("timeline").remove();
     }
     catch (e) {
        console.log("timeline ещё не создан");
     }
     
    let timeline = document.createElement("iframe");
    timeline.id = "timeline";
    timeline.setAttribute("src", "https://cdn.knightlab.com/libs/timeline3/latest/embed/index.html?source=15KJzDYah5reYpr65uq_m2E_NvbV_yXlFs5sgyIEy-jY&font=Default&lang=en&initial_zoom=2&height=650");
    timeline.style.width = "100%";
    timeline.style.height = "600px";

    let container = document.getElementById("timeline-cont");
    container.appendChild(timeline);
}

// Очистка блока умений
function clearSkillsBlock()
{
    // Удаление дочерних элементов
    let skillsBlock = document.getElementById("skills-block");
    while (skillsBlock.firstChild)
    {
        skillsBlock.removeChild(skillsBlock.firstChild);
    }
}

// Получение навыков по id
function getSkills(id)
{
    let skillsReq = new XMLHttpRequest();
    skillsReq.open("GET", "/jsonData/" + id, true);
    skillsReq.responseType = 'json';
    skillsReq.onload = function ()
    {
        jsonRespons = skillsReq.response;

        for(let i = 0; i < skillsReq.response["Skills"].length; i++)
        {
            let p = document.createElement('p');
            p.id = "skills";
            p.innerHTML = skillsReq.response["Skills"][i];
            document.getElementById('skills-block').appendChild(p);

            //console.log(skillsReq.response["Skills"][i]);
        }
    }
    skillsReq.send(null); 
}

// Вывод тестового JSON в консоль
function jsonToConsole()
{
    console.log(jsonRespons);
}

// Запрос данных из Leader Id
function reqFromLeaderId()
{
    let leaderId = document.getElementById('input-leader-id').value;

    if(leaderId != "")
    {
        let leadReq = new XMLHttpRequest();
        leadReq.open("GET", "/ParseLeader/" + leaderId, true);
        leadReq.responseType = 'json';
        leadReq.onload = function ()
        {
            var data = {
                labels: [],
                series: []
            };

            let size = leadReq.response["Skills"][0]["Skill Title"].length;
            for(let i = 0; i < size; i++)
            {
                console.log(leadReq.response["Skills"][0]["Skill Title"][i]+ " " + leadReq.response["Skills"][1]["Skill Rate"][i]);
                
                data["labels"].push(leadReq.response["Skills"][0]["Skill Title"][i]);
                data["series"].push(leadReq.response["Skills"][1]["Skill Rate"][i]);
            }

            var options = {
                labelInterpolationFnc: function(value) {
                    return value[0]
                }
            };
    
            var responsiveOptions = [
                ['screen and (min-width: 640px)', {
                    chartPadding: 30,
                    labelOffset: 100,
                    labelDirection: 'explode',
                    labelInterpolationFnc: function(value) {
                    return value;
                    }
                }],
                ['screen and (min-width: 1024px)', {
                    labelOffset: 80,
                    chartPadding: 20
                }]
            ];
    
            new Chartist.Pie('.ct-chart', data, options, responsiveOptions);
        }
        leadReq.send(null); 
    }
}

// Запрос обработки резюме по ссылке
function reqForParse() {

    reqFromLeaderId();

    let showFrame = document.getElementById("showIframe").checked;
    let showTimeline = document.getElementById("showTimeline").checked;
    let showJSON = document.getElementById("showJSON").checked;

    let url = document.getElementById('input-url').value;
    let id = url.split('/')[4]

    console.log(id)
    console.log("/reqForParse/" + id.toString());

    let reqPage = new XMLHttpRequest();
    reqPage.open("GET", "/reqForParse/" + id.toString(), true);
    reqPage.onload = function ()
    {
        clearSkillsBlock();
        getSkills(id)

        if(showFrame)
        {
            addFrame(id);
        }
        else
        {
            try {
                document.getElementById("frame-id").remove();
             }
             catch (e) {
                console.log("Frame ещё не создан");
             }
        }
        
        if(showTimeline)
        {
            addTimeLine();
        }
        else 
        {
            try {
                document.getElementById("timeline").remove();
            }
             catch (e) {
                console.log("timeline ещё не создан");
            }
        }

        if(showJSON)
        {
            jsonToConsole()
        }
    }

    reqPage.send(null);

    //setTimeout(() => { addFrame(id); }, 1500);
}

// Отлеживание нажатия клавиши Enter
function chengeWordPress(event) {
    if (event.keyCode == 13) {
        loadNewWord();
    }
}

function parsePress(event) {
    if (event.keyCode == 13) {
        reqForParse();
    }
}

// Выпадающий чеклист
var checkList = document.getElementById('list1');
checkList.getElementsByClassName('anchor')[0].onclick = function(evt) {
  if (checkList.classList.contains('visible'))
    checkList.classList.remove('visible');
  else
    checkList.classList.add('visible');
}