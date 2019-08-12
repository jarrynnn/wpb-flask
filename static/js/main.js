        
$(function() {
  var barChart = $('#bar-chart');

  
  var myChart;
  createChart(myChart, barChart, [0, 0, 0]);

}); 




$('.refresh').click(function() {
    alert('refreshed');

    $.get("/data/" + $(this).text(), function(result) {
        createChart(myChart, barChart, result.data);
      });
    });
  
  });
    
  function createChart(chart, canvas, data) {

    if (chart) chart.destroy();
    chart = new Chart(canvas, {
      type: 'bar',
      data: {
        labels: ['UK', 'Ireland', 'France'],
        datasets: [
          {
            label: "Total prison population",
            backgroundColor: ['#000000', '#FFFF00', '#009900'],
            data: data
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