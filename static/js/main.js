        
$(function() {
    var barChart = $('#bar-chart');

  
    var myChart = createChart(barChart, [0, 0, 0]);


    $('.refresh').click(function() {
            
    $.get("/data/" + $(this).data('key'), function(result) {
        myChart.destroy();  
        myChart = createChart(barChart, result.data);
      });
    });

    $('.refreshmetric').click(function() {
            
    $.get("/data/1/" + $(this).data('key'), function(result) {
          myChart.destroy();  
          myChart = createChart(barChart, result.data);
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
            }
      }
    });
  } 

