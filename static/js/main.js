
//barchart
am4core.ready(
$(function() {

    var barChart = $('#bar-chart');
 
    var myChart = createChart(barChart, [0, 0, 0]);
    var map = $('#chartdiv');
    var myMap = createMap(map, [{
      "id": "US",
      "value": 0
    }, {
      "id": "FR",
      "value": 0
    }]);  



    $(".js-countries-multiple").on("select2:select select2:unselect", function (e) {
      //this returns all the selected items
    var items= $(this).val(); 

    $.get("/data/" + items, function(result) {
        myChart.destroy();  
        myChart = createChart(barChart, result.data);
        myMap.destroy();
        var mapdata = [{
          "id": "US",
          "value": 100
        }, {
          "id": "FR",
          "value": 50
        }]
        myMap = createMap(map, mapdata);
      });
    })


    $('.refreshmetric').click(function() {
            
    $.get("/data/" + $(".js-countries-multiple").val() + "/" + $(this).data('key'), function(result) {
    //need to work out how to pass through the selected countries here (fixed at UK)

          myChart.destroy();  
          myChart = createChart(barChart, result.data);
          createMap(mapdata);
        });
    });

  }));
    


 

function createChart(canvas, data) {  
  
    return new Chart(canvas, {
      
      type: 'bar',
      data: {
        labels: data["countryname"],
        datasets: [
          {
            label: data["metric"],
            //change this so it just shows one? Showing undefinded?
            backgroundColor: data["countrycolour"],
            data: data["value"]
          }
        ]
      },
      options: {
        legend: { display: false },
        title: { 
          display: true,
            text: 'Total prison population'
            },
        scales: {
            yAxes: [{
              display: true,
              ticks: {
                suggestedMin: 0,
              }
            }]
        }
      }
    });
}

function createMap(map, data) {
  alert(data);  

  // Themes begin
  am4core.useTheme(am4themes_animated);
  // Themes end
  
  // Create map instance
  var chart = am4core.create("chartdiv", am4maps.MapChart);
  
  // Set map definition
  chart.geodata = am4geodata_worldLow;
  
  // Set projection
  chart.projection = new am4maps.projections.NaturalEarth1();
  
  // Create map polygon series
  var polygonSeries = chart.series.push(new am4maps.MapPolygonSeries());
  
  polygonSeries.mapPolygons.template.strokeWidth = 0.5;
  
  // Exclude Antartica
  polygonSeries.exclude = ["AQ"];
  
  // Make map load polygon (like country names) data from GeoJSON
  polygonSeries.useGeodata = true;
  
  polygonSeries.data = data;
  
  polygonSeries.heatRules.push({
    "property": "fill",
    "target": polygonSeries.mapPolygons.template,
    "min": am4core.color("#BBBBBB"),
    "max": am4core.color("#AAAAAA")
  });
  
  // Configure series
  var polygonTemplate = polygonSeries.mapPolygons.template;
  polygonTemplate.tooltipText = "{name} [bold]{value}[/]";
  
  // Create hover state and set alternative fill color
  var hs = polygonTemplate.states.create("hover");
  hs.properties.stroke = am4core.color("#666666");
  hs.properties.strokeWidth = 1;
  
  // Create active state
  var activeState = polygonTemplate.states.create("active");
  activeState.properties.stroke = am4core.color("#999999");
  activeState.properties.strokeWidth = 1;
  
  // Create an event to toggle "active" state
  polygonTemplate.events.on("hit", function(ev) {
    ev.target.isActive = !ev.target.isActive;
  })
  
  chart.events.on("hit", function(ev) {
    var activeIds = Array.from(polygonSeries.mapPolygons)
      .filter(p => p.isActive)
      .map(p => p.dataItem.dataContext.id);
    
    alert(activeIds);
  })
  
  function setState(country, active) {
    polygonSeries.mapPolygons.each(function(polygon) {
      if (polygon.dataItem.dataContext.id == country) polygon.setState(active ? "active" : "default");
    });
  }
  
  var graticuleSeries = chart.series.push(new am4maps.GraticuleSeries());
  
  setState("GB", true);
  setState("US", true);
  setState("US", false);

  return (chart)
  }; 

    

  

