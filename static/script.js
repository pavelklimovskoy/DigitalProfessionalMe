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
    getUrl.open("GET", "http://127.0.0.1/getPageForParse/" + findWord, true);
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
    getFindWord.open("GET", "http://127.0.0.1/getFindWord", false);
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
    loadFindWord.open("GET", "http://127.0.0.1/newFindWord/" + newWord, false);
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
    frame.setAttribute("src", "http://127.0.0.1/templates/" + id);
    frame.style.width = "100%";
    frame.style.height = "480px";
    document.body.append(frame);
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
    timeline.setAttribute("src", "https://cdn.knightlab.com/libs/timeline3/latest/embed/index.html?source=1xuY4upIooEeszZ_lCmeNx24eSFWe0rHe9ZdqH2xqVNk&font=Default&lang=en&initial_zoom=2&height=100%");
    timeline.style.width = "100%";
    timeline.style.height = "600px";
    document.body.append(timeline);
}

// Вывод тестового JSON в консоль
function jsonToConsole()
{
    console.log(jsonRespons);
}

// Запрос обработки резюме по ссылке
function reqForParse() {
    let showFrame = document.getElementById("showIframe").checked;
    let showTimeline = document.getElementById("showTimeline").checked;
    let showJSON = document.getElementById("showJSON").checked;

    let url = document.getElementById('input-url').value;
    let id = url.split('/')[4]

    console.log(id)
    console.log("http://127.0.0.1/reqForParse/" + id.toString());

    let reqPage = new XMLHttpRequest();
    reqPage.open("GET", "http://127.0.0.1/reqForParse/" + id.toString(), true);
    reqPage.onload = function ()
    {
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