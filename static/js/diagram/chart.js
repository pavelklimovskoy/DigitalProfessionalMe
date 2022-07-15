anychart.onDocumentReady(function () {
 
  let cookieId = document.cookie.match('(^|;)\\s*' + 'id' + '\\s*=\\s*([^;]+)')?.pop() || '';
  //let xhr = new XMLHttpRequest();

  //xhr.responseType = 'text'; // or json

  let urlRequest = 'http://digitalprofessional.me:5000/getChartJson?id='+cookieId;
  
  // xhr.open(
  //   'GET',
  //   urlRequest,
  //   true
  // );
  // xhr.send();

  // xhr.onload = function() {
  //   data = xhr.response;
  // };
   
  anychart.data.loadJsonFile(urlRequest,
    function (data) {
        // create a data tree from the dataset
        let dataTree = anychart.data.tree(data);
        
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
          .level(1)
          .labels()
          .fontFamily("Verdana, sans-serif")
          .format("<span style='font-size:16px'>{%name}</span>");
        chart
          .level(0)
          .labels()
          .fontFamily("Verdana, sans-serif")
          .fontWeight(500)
          .format("<span style='font-size:16px'></span><br><br><span style='font-size:16px'></span>");

        // enable HTML in tooltips
        chart.tooltip().useHtml(true);

        // customize the format of the sunburst chart tooltip
        chart
          .tooltip()
          .fontFamily("Verdana, sans-serif")
          .format("<h5 style='font-size:16px; margin: 0.25rem 0;'>{%name}</h5><h6 style='font-size:14px; font-weight:400; margin: 0.2rem 0;'>Level: <b>{%value}{groupsSeparator:\\,}</b></h6><h6 style='font-size:14px; font-weight:400; margin: 0.2rem 0;'></b></h6>");

        // Set chart fill.
        let avatarName = new XMLHttpRequest();
        avatarName.open("GET", "http://digitalprofessional.me:5000/getAvatar", true);
        avatarName.onload = function () {
                chart.fill({
            src: '../static/data/img/' + avatarName.responseText,
            mode: 'fit'
            });
        }
        avatarName.send(null);

        chart.labels().useHtml(true);
        chart.labels().format("<span style='font-size: 8px; word-break: normal; word-wrap: break-word;'>{%name}</span>");

        // set the position of labels
        chart.labels().position("circular");

        // set the chart container element id
        chart.container('chartid');

        // initiate chart drawing
        chart.draw();
      });
    });