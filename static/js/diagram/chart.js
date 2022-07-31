function filterSkills(data) {
  let disabledSkills = [];

  data[0].children.forEach(item => {
    item.children.forEach(item => {
      item.children.forEach(item => {
        if (!item.enabled) {
          disabledSkills.push(item);
        }
      });
    });
  });

  return disabledSkills;
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
    urlRequest = `http://localhost:5000/getChartJson?id=${cookieId}`;

  anychart.data.loadJsonFile(urlRequest,
    function (data) {
      let dataTree = anychart.data.tree(data);

      let redrawChart = (disabledSkills, skill = '') => {
        console.log('disabledSkills: ', disabledSkills);
        console.log('skill: ', skill);

        // Выключение скилла
        if (!skill) {
          disabledSkills.forEach(item => {
            let child = dataTree.search('name', item.name);

            if (child) {
              let parent = child.getParent(),
                grandParent = parent.getParent();
              parent.removeChild(child);
              if (parent.numChildren() == 0) {
                grandParent.removeChild(parent);
              }
            }
          });
          chart.autoRedraw(true);
        }
        else {  // Включение скилла
          let treeParent = dataTree.search('name', skill.parent),
            treeGrandParent = dataTree.search('name', skill.grandParent);

          if (treeGrandParent) {
            if (treeParent) {
              treeParent.addChild(skill);
            } else {
              let parent = {
                'name': skill.parent,
                'id': skill.id,
                'value': '1',
                'fill': skill.fill,
                'parent': skill.grandParent
              };

              treeGrandParent.addChild(parent).addChild(skill);
            }
          } else {
            let grandParent = {
              'name': skill.grandParent,
              'id': skill.id,
              'value': '1',
              'fill': skill.fill
            };

            let parent = {
              'name': skill.parent,
              'id': skill.id,
              'value': '1',
              'fill': skill.fill,
              'parent': skill.grandParent
            };

            dataTree.addChild(grandParent).addChild(parent).addChild(skill);
          }
        }
      };

      let chart = anychart.sunburst(dataTree);
      chart.calculationMode('parent-independent');
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

      chart.labels().useHtml(true);
      chart.tooltip().useHtml(true);
      chart.labels().useHtml(true);

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

      chart
        .tooltip()
        .fontFamily("Verdana, sans-serif")
        .format("<h5 style='font-size:16px; margin: 0.25rem 0;'>{%name}</h5><h6 style='font-size:14px; font-weight:400; margin: 0.2rem 0;'>Level: <b>{%value}{groupsSeparator:\\,}</b></h6><h6 style='font-size:14px; font-weight:400; margin: 0.2rem 0;'></b></h6>");

      // Set avatar
      fetch(`http://localhost:5000/getAvatar?id=${cookieId}`)
        .then(data => data.text())
        .then(data => chart.fill({
          src: `../static/data/img/${data}`,
          mode: 'fit'
        }));

      chart.labels().format("<span style='font-size: 10px; word-break: normal; word-wrap: break-word;'>{%shortName}</span>");
      chart.labels().position("circular");

      chart.container('chartid');

      chart.draw();
      chart.autoRedraw(true);

      redrawChart(filterSkills(data), 0);

      createTimeline();
      loadSkills(unfilteringSkills(data), redrawChart, filterSkills(data));
    });
});