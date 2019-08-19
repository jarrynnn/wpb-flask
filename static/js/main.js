        
//barchart
$(function() {

    var barChart = $('#bar-chart');
 
    var myChart = createChart(barChart, [0, 0, 0]);
    var selectedCountries = []


    $(".js-countries-multiple").on("select2:select select2:unselect", function (e) {

      //this returns all the selected item
      var items= $(this).val();       
  
      //Gets the last selected item
      var lastSelectedItem = e.params.data.id;

      $.get("/data/" + items('key'), function(result) {
        myChart.destroy();  
        myChart = createChart(barChart, result.data);
      });
  
  })


    $('.refresh').click(function() {
            
    $.get("/data/" + $(this).data('key'), function(result) {
        myChart.destroy();  
        myChart = createChart(barChart, result.data);
      });
    });

    $('.refreshmetric').click(function() {
            
    $.get("/data/1/" + $(this).data('key'), function(result) {
    //need to work out how to pass through the selected countries here (fixed at UK)

          myChart.destroy();  
          myChart = createChart(barChart, result.data);
        });
    });

    // Onclick event to retrieve all active countries
    $('.chartdiv').click(function() {
          
    $.get($(this).data('key'), function(result) {
        selectedCountries.destroy();  
        selectedCountries = event.target.dataItem.dataContext.id;
        alert(selectedCountries);

        });
    });

  });
    


 

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






