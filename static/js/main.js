        
$(function() {
  var barChart = $('#bar-chart');
  new Chart(barChart, {
      type: 'bar',
      data: {
        labels: ['UK', 'Ireland'],
        datasets: [
          {
            label: "Total prison population",
            backgroundColor: ['#33ccdd', '#FFFF00'],
            data: [123, 28890]
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




$('#refresh').click(function() {
    alert('refreshed');
    });
});

