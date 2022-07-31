function filterSkills(data) {
  let filteringData = [];

  data[0].children.forEach(item => {
    item.children.forEach(item => {
      item.children.forEach(item => {
        if (!item.enabled) {
          filteringData.push(item);
        }
      });
    });
  });

  return filteringData;
}

function unfilteringSkills(data) {
  let unfilteringData = [];

  data[0].children.forEach(item => {
    item.children.forEach(item => {
      item.children.forEach(item => {
        unfilteringData.push(item);
      });
    });
  });

  return unfilteringData;
}

anychart.onDocumentReady(function () {
  let cookieId = document.cookie.match('(^|;)\\s*' + 'id' + '\\s*=\\s*([^;]+)')?.pop() || '',
    urlRequest = `http://digitalprofessional.me:5000/getChartJson?id=${cookieId}`;

  anychart.data.loadJsonFile(urlRequest,
    function (data) {

      // create a data tree from the dataset
      let dataTree = anychart.data.tree(data);

      let redrawChart = (filteringData) => {
        //let filteringData = filterSkills(data);
        console.log(filteringData);
        filteringData.forEach(item => {
          console.log(dataTree);
          let child = dataTree.search('name', item.name);
          if (child) {
            let parent = child.getParent();
            let grandParent = parent.getParent();

            parent.removeChild(child);
            if (parent.numChildren() == 0) {
              grandParent.removeChild(parent);
            }
          }
        });
        chart.autoRedraw(true);
      };

      // create a sunburst chart
      let chart = anychart.sunburst(dataTree);

      // set the calculation mode
      chart.calculationMode('parent-independent');

      // set the ascending sort order
      chart.sort('asc');

      // set the chart title
      //chart.title("Title");

      // var label = anychart.standalones.label();
      // label.enabled(true);
      // label.text('Activities');
      // label.width('100%');
      // label.height('100%');
      // label.fontSize(30);
      // label.fontColor('#60727b');
      // label.hAlign('center');
      // label.vAlign('middle');

      // enable HTML in labels
      chart.labels().useHtml(true);

      // customize the format of the sunburst chart labels
      chart
        .level(0)
        .labels()
        .fontFamily("Verdana, sans-serif")
        .fontWeight(500)
        .format("<span style='font-size:16px'></span><br><br><span style='font-size:16px'></span>");

      chart
        .level(1)
        .labels()
        .fontFamily("Verdana, sans-serif")
        .format("<span style='font-size:16px'>{%name}</span>");

      chart
        .level(2)
        .labels()
        .fontFamily("Verdana, sans-serif")
        .format("<span style='font-size:8px'>{%name}</span>");

      // enable HTML in tooltips
      chart.tooltip().useHtml(true);

      // customize the format of the sunburst chart tooltip
      chart
        .tooltip()
        .fontFamily("Verdana, sans-serif")
        .format("<h5 style='font-size:16px; margin: 0.25rem 0;'>{%name}</h5><h6 style='font-size:14px; font-weight:400; margin: 0.2rem 0;'>Level: <b>{%value}{groupsSeparator:\\,}</b></h6><h6 style='font-size:14px; font-weight:400; margin: 0.2rem 0;'></b></h6>");

      // Set chart fill.
      fetch(`http://digitalprofessional.me:5000/getAvatar?id=${cookieId}`)
        .then(data => data.text())
        .then(data => chart.fill({
          src: `../static/data/img/${data}`,
          mode: 'fit'
        }));

      chart.labels().useHtml(true);
      chart.labels().format("<span style='font-size: 10px; word-break: normal; word-wrap: break-word;'>{%shortName}</span>");

      // set the position of labels
      chart.labels().position("circular");

      // set the chart container element id
      chart.container('chartid');

      chart.draw();
      chart.autoRedraw(true);

      redrawChart(filterSkills(data));

      // setTimeout(() => {
      //   var dad = dataTree.search('name', 'Information');
      //   var parent = dataTree.search('name', 'Software Developers and Programmers');
      //   var child = dataTree.search('name', 'Язык');
      //   parent.removeChild(child);

      //   let ask = confirm(`Redraw?`);
      //   if (ask) { chart.autoRedraw(true); }
      // }, 4000);

      // chart.autoRedraw(false);

      // setTimeout(() => {
      //   var dad = dataTree.search('name', 'Management of Companies and Enterprises');
      //   var parent = dataTree.search('name', 'Managers, All Other');
      //   var child = dataTree.search('name', 'работа в команде');
      //   parent.removeChild(child);

      //   let ask = confirm(`Redraw?`);
      //   if (ask) { chart.autoRedraw(true); }
      // }, 10000);

      createTimeline();
      loadSkills(unfilteringSkills(data), redrawChart, filterSkills(data));
    });
});