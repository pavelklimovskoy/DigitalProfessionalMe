let debugTimeline = false;

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
  let urlRequest = `${baseUrl}/getRchilliJson?id=${cookieId}`;


  fetch(urlRequest)
    .then(response => {
      return response.json();
    })
    .then(data => {
      // Обработка опыта работы
      data["ResumeParserData"]["SegregatedExperience"].forEach(job => {

        let endDate = job["EndDate"].split('/').reverse().join('-');
        let startDate = job["StartDate"].split('/').reverse().join('-');
        let position = job["JobProfile"]["FormattedName"];
        let employer = job["Employer"]["EmployerName"];

        let itemContent = "<b>" + employer + "</b>" + "<br>" + position;
        let tooltip = itemContent

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
      data["ResumeParserData"]["SegregatedQualification"].forEach(study => {

        let itemIcon = '<div><img id="111"src="../static/data/img/university.png"></div>';
        let period = study["FormattedDegreePeriod"];
        let place = "<div>" + study["Institution"]["Name"] + "</div>" + itemIcon;
        let tooltip = study["Institution"]["Name"]

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
          content: "<b>Experience</b>"
        },
        {
          id: 2,
          content: '<b>Courses</b>'
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

      let timeline = new vis.Timeline(container, items, groups, options);

      let updateEditOptions = function (e) {
        let changedOption = e.target.name;
        let options = { editable: {} };
        options.editable[changedOption] = e.target.checked;
        timeline.setOptions(options);
      };

      let cbs = document.getElementsByTagName("input");
      [].forEach.call(cbs, function (cb) {
        cb.onchange = updateEditOptions;
      });

    });
}