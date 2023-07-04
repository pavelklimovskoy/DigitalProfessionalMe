let debugTimeline = false;
var timeline;
var itemId = 0;

// Вывод отладочной информации
function showControllers() {
  fetch('../templates/snippets/debug-form-timeline.html')
    .then(response => response.text())
    .then(text => {
      let divControl = document.getElementById("debugTimeline");

      if (divControl != null) {
        divControl.innerHTML = text;
      }
    });
}

// Содание Timeline
function createTimeline() {
  if (debugTimeline == true) {
    showControllers();
  }

  let arrItems = [];

  itemId = 0;

  let urlRequest = `${baseUrl}/getTimelineJson`;


  fetch(urlRequest)
    .then(response => {
      return response.json();
    })
    .then(data => {
      // Обработка опыта работы
      data["experienceEvents"].forEach(job => {

        if (job["endDate"]) {
          let endDate = job["endDate"].split('/').reverse().join('-');
          let startDate = job["startDate"].split('/').reverse().join('-');
          let position = job["position"];
          let employer = job["employer"];

          let itemContent = "<b>" + employer + "</b>" + "<br>" + position;
          let tooltip = employer + "<br>" + position

          arrItems.push(
            {
              id: itemId,
              content: itemContent,
              editable: false,
              start: startDate,
              end: endDate,
              group: 1,
              title: tooltip,
            });

          //console.log(itemId);
          itemId++;

        } else {
          //let startDate = job["startDate"].split('/').reverse().join('-');
          let dateEntered = new Date(job["startDate"]);
          let planeName = job["position"];

          arrItems.push({
            id: itemId,
            start: dateEntered,
            editable: false,
            group: 1,
            content: '<b>' + planeName + '</b>',
            title: planeName
          });

          //timeline.itemsData.add(newItem);
          //console.log(itemId);

          itemId++;
        }
      });

      // Обработка образования
      data["qualificationEvents"].forEach(study => {

        let itemIcon = '<div><img id="111"src="../static/data/img/university.png"></div>';
        let period = study["period"];
        let place = "<div>" + study["name"] + "</div>" + itemIcon;
        let tooltip = study["name"]

        if (period.includes("to") == true) {
          period = period.replace(/\s/g, '');

          let startDate = period.split("to")[0];
          let endDate = period.split("to")[1];

          arrItems.push({
            id: itemId,
            content: place,
            editable: false,
            start: new Date(startDate),
            end: new Date(endDate),
            group: 3,
            title: tooltip
          });
        }
        else {
          period = period.split('/').reverse().join('-');

          arrItems.push({
            id: itemId,
            content: place,
            editable: false,
            start: new Date(period),
            group: 3,
            title: tooltip
          });
        }
        //console.log(itemId);

        itemId++;
      });

      // Обработка сертификатов
      data["certifications"].forEach(certificate => {
        let date = certificate["date"],
          name = certificate["name"];

        console.log(date);
        console.log(name);
        console.log(new Date(date));

        arrItems.push({
          id: itemId,
          start: new Date(date),
          editable: false,
          group: 2,
          content: '<b>' + name + '</b>',
          title: name
        });

        itemId++;
      });
      let items = new vis.DataSet(arrItems);

      // Группы событий
      let groups = [
        {
          id: 1,
          content: "<b>Experience</b><span> &#128188;</span>"
        },
        {
          id: 2,
          content: '<b>Courses </b><span> &#128211;</span>'
        },
        {
          id: 3,
          content: '<b>Education</b><span> &#127891;</span>'
        }
      ]

      // HTML div для размещения Timeline
      let container = document.getElementById('visualization');

      // Параметры для Timeline
      let options = {
        zoomMax: 900000000000,
        zoomMin: 80000000000,

        autoResize: false,
        editable: {
          add: false,
          remove: false,
          updateGroup: false,
          updateTime: false,
          overrideItems: false
        }
      };

      timeline = new vis.Timeline(container, items, groups, options);
      timeline.setOptions({ height: "400px" })
  

      timeline.redraw()

      timeline.zoomIn(0.01)


    }).finally(() => {
      timeline.redraw()
    });
}

// Ожидание загрузки DOM
function waitForDOM() {
  if (timeline != null) {
    timeline._redraw();
    let view_date = new Date()
    view_date.setFullYear(view_date.getFullYear() - 2);
    timeline.moveTo(view_date);
  } else {
    setTimeout(waitForDOM, 300);
  }
}

// При полной заргрузки страницы происходит обновление Timeline
document.addEventListener('DOMContentLoaded', function () {
  setTimeout(waitForDOM, 300);
});

// Перерисовка при изменение размеров окна
window.addEventListener('resize', function (event) {
  if (timeline != null) {
    timeline._redraw()
  }
}, true);

// Добавление нового ивента
function addLifeGoal() {
  let inputDate = document.getElementById("goalDateInput").value;
  let dateEntered = new Date(inputDate);
  //console.log(dateEntered);
  let planeName = document.getElementById("goalJDInput").value;

  itemId++;

  let newItem = {
    id: itemId,
    start: dateEntered,
    editable: false,
    group: 1,
    content: '<b>' + planeName + '</b>',
    title: planeName
  };

  timeline.itemsData.add(newItem);
  //console.log(itemId);
}

// Добавление нового Сертификата
function addCerificate(ceritificateData) {
  const courseDate = ceritificateData.date,
    //courseSkills = ceritificateData.skills,
    dateEntered = new Date(courseDate),
    courseName = ceritificateData.courseName;
  console.log(dateEntered);

  itemId++;

  let newItem = {
    id: itemId,
    start: courseDate,
    editable: false,
    group: 2,
    content: '<b>' + courseName + '</b>',
    title: courseName
  };


  timeline.itemsData.add(newItem);
  //console.log(itemId);

  //closeModal();
}

// courseSkills.forEach(skill => {
//   const skillArr = skill.split(' ');
//   for (let i = 0; i < skillArr.length; i++)
//     if (skillArr[i].length > 3) {
//       console.log(skillArr[i]);
//       fetch(`${baseUrl}/skillInputAutocomplete?skillName=${skillArr[i]}`)
//         .then(response => await response.json())
//         .then(data => {
//           console.log(data);
//           if (data[0]) {
//             const urlRequest = `${baseUrl}/findSkill?skillName=${data[0]}`;
//             await fetch(urlRequest)
//               .then(response => response.json())
//               .then(skillData => {
//                 console.log(skillData);
//                 const ontology = skillData.ontology.split(',')[0].split('>');
//                 let skill = addSkillToChart(skillData.searchWord, ontology[1], ontology[0], skillData.type, skillData.filling);

//                 addSkill(skill, skillList.length);
//               });
//           }
//         });
//       break;
//     }
// });