// Заполнение текстовых полей при запуске
window.onload = function() {
    let getUrl = new XMLHttpRequest();
    getUrl.open("GET", "http://127.0.0.1/getPageForParse", true);
    getUrl.onload = function ()
    {
        document.getElementById('input-url').value = getUrl.responseText;
    }
    getUrl.send(null);

    getWord(); 
}

// Выгрузка поискового слова
function getWord() {
    let getFindWord = new XMLHttpRequest();
    getFindWord.open("GET", "http://127.0.0.1/getFindWord", true);
    getFindWord.onload = function ()
    {
        document.getElementById('change-word').placeholder  = "Current search phrase: " + getFindWord.responseText;
        document.getElementById('change-word').value = "";
    }

    getFindWord.send(null);
}

// Заргузка нового поискового слова
function loadNewWord() {
    let newWord = document.getElementById('change-word').value;
    let loadFindWord = new XMLHttpRequest();
    loadFindWord.open("GET", "http://127.0.0.1/newFindWord/" + newWord, true);
    loadFindWord.onload = function ()
    {
        console.log("new word loaded");
        getWord();
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
    document.body.append(timeline);
}

// Запрос обработки резюме по ссылке
function reqForParse() {
    let url = document.getElementById('input-url').value;
    let id = url.split('/')[4]

    console.log(id)
    console.log("http://127.0.0.1/reqForParse/" + id.toString());

    let reqPage = new XMLHttpRequest();
    reqPage.open("GET", "http://127.0.0.1/reqForParse/" + id.toString(), true);
    reqPage.onload = function ()
    {
        addFrame(id);
        addTimeLine();
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