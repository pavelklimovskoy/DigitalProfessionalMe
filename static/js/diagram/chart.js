anychart.onDocumentReady(renderChart);
let dataTree, skillList = [], disabledSkills = [];

function filterSkills(data) {
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
  data[0].children.forEach(item => {
    item.children.forEach(item => {
      item.children.forEach(item => {
        skillList.push(item);
      });
    });
  });

  return skillList;
}

function disableSkill(skillName) {
  let child = dataTree.search('name', skillName),
    root = dataTree.search('name', 'Me');
  if (child) {
    let parent = child.getParent(),
      grandParent = parent.getParent();

    parent.removeChild(child);

    if (!parent.numChildren()) {
      grandParent.removeChild(parent);
      if (!grandParent.numChildren()) {
        root.removeChild(grandParent);
      }
    }
  }
}

function enableSkill(skill) {
  let treeParent = dataTree.search('name', skill.parent),
    treeGrandParent = dataTree.search('name', skill.grandParent),
    root = dataTree.search('name', 'Me');

  if (treeGrandParent) {
    if (treeParent) {
      treeParent.addChild(skill);
    } else {
      let parent = {
        'name': skill.parent,
        'id': skill.id,
        'value': '1',
        'fill': skill.fill,
        'parent': skill.grandParent,
        'children': []
      };

      treeGrandParent.addChild(parent).addChild(skill);
    }
  } else {

    let grandParent = {
      'name': skill.grandParent,
      'id': skill.id,
      'fill': skill.fill,
      'parent': 'Me',
      'children': []
    };

    let parent = {
      'name': skill.parent,
      'id': skill.id,
      'value': '1',
      'fill': skill.fill,
      'parent': skill.grandParent,
      'children': []
    };

    root.addChild(grandParent).addChild(parent).addChild(skill);
  }
}

function addSkillToChart(skillName, skillParentName, skillGrandParentName, skillType, skillFilling) {
  let treeChild = dataTree.search('name', skillName),
    treeParent = dataTree.search('name', skillParentName),
    treeGrandParent = dataTree.search('name', skillGrandParentName);


  if (!treeChild) {
    let shortName = skillName;
    // if (skillName.length > 6) {
    //   shortName = `${skillName.slice(0, 6)}...`;
    // } else {
    //   shortName = skillName;
    // }

    let grandParent = {
      'name': skillGrandParentName,
      'id': skillType,
      'fill': skillFilling,
      'parent': 'Me',
      'children': []
    };

    let parent = {
      'name': skillParentName,
      'id': skillType,
      'value': '1',
      'fill': skillFilling,
      'parent': skillGrandParentName,
      'children': []
    };

    let skill = {
      'name': skillName,
      'id': skillType,
      'value': '1',
      'enabled': true,
      'shortName': shortName,
      'fill': skillFilling,
      'grandParent': skillGrandParentName,
      'parent': skillParentName
    };

    skillList.push(skill);

    if (treeGrandParent) {
      if (treeParent) {
        treeParent.addChild(skill);
      } else {
        treeGrandParent.addChild(parent).addChild(skill);
      }
    } else {
      dataTree.addChild(grandParent).addChild(parent).addChild(skill);
    }
    return skill;
  }
}

function renderChart() {
  let cookieId = document.cookie.match('(^|;)\\s*' + 'id' + '\\s*=\\s*([^;]+)')?.pop() || '',
    urlRequest = `${baseUrl}/getChartJson?id=${cookieId}`;

  anychart.data.loadJsonFile(urlRequest,
    function (data) {
      dataTree = anychart.data.tree(data);
      disabledSkills = filterSkills(data);
      skillList = unfilteringSkills(data);
      let chart = anychart.sunburst(dataTree);

      chart.calculationMode('parent-independent');
      chart.sort('asc');

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
      fetch(`${baseUrl}/getAvatar?id=${cookieId}`)
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

      createTimeline();
      loadSkills();

      disabledSkills.forEach(skill => disableSkill(skill.name));
    });
}
