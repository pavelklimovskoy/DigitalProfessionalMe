let debugTimeline = false;
var timeline;

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

  let itemId = 0;

  let cookieId = document.cookie.match('(^|;)\\s*' + 'id' + '\\s*=\\s*([^;]+)')?.pop() || '';
  let urlRequest = `${baseUrl}/getTimelineJson?id=${cookieId}`;


  fetch(urlRequest)
    .then(response => {
      return response.json();
    })
    .then(data => {
      // Обработка опыта работы
      data["experienceEvents"].forEach(job => {

        let endDate = job["endDate"].split('/').reverse().join('-');
        let startDate = job["startDate"].split('/').reverse().join('-');
        let position = job["position"];
        let employer = job["employer"];

        let itemContent = "<b>" + employer + "</b>" + "<br>" + position;
        let tooltip = employer + "<br>" + position

        arrItems.push(
          { id: itemId, 
            content: itemContent, 
            editable: false,
            start: startDate, 
            end: endDate,
            group: 1,
            title: tooltip,
          });

        itemId++;
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
      timeline.setOptions({height:"400px"})

      timeline.redraw()

      timeline.zoomIn(0.01)


    }).finally(() => {
      timeline.redraw()
      });
}


function waitForDOM () {
  if (timeline != null) {
    timeline._redraw()
    let view_date = new Date()
    view_date.setFullYear(view_date.getFullYear() - 2);
    timeline.moveTo(view_date);
  } else {
    setTimeout(waitForDOM, 300);
  }
}

// При полной заргрузки страницы происходит обновление Timeline
document.addEventListener('DOMContentLoaded', function() {
  setTimeout(waitForDOM, 300);
});

// Перерисовка при изменение размеров окна
window.addEventListener('resize', function(event) {
  if (timeline != null) {
    timeline._redraw()
  }
}, true);