// https://quickchart.io/sandbox

var _seed = Date.now();

function valueOrDefault(value, defaultValue) {
  return typeof value === 'undefined' ? defaultValue : value;
}

function srand(seed) {
  _seed = seed;
}

function rand(min, max) {
  min = valueOrDefault(min, 0);
  max = valueOrDefault(max, 0);
  _seed = (_seed * 9301 + 49297) % 233280;
  return min + (_seed / 233280) * (max - min);
}

transactioncharts = {

    initPerformanceChart: function() {

        const labels = ["18.03.2024", "19.03.2024", "20.03.2024", "21.03.2024", "22.03.2024", "23.03.2024", "24.03.2024", "25.03.2024"];

        const data = {
          labels: labels,
          datasets: [
            {
              label: 'Среднее время выполнения транзакций, с',
              data: [13.1, 15.2, 9.5, 7.8, 18.9, 3.1, 2.7, 11.4],
                backgroundColor: 'rgba(255, 99, 132, 0.2)',
                borderColor: 'rgb(255, 99, 132)',
                yAxisID: 'y'
            },
            {
              label: 'Количество транзакций за сутки',
              data: [1285, 1175, 2357, 1245, 1624, 476, 328, 1134],
                backgroundColor: 'rgba(255, 159, 64, 0.2)',
                borderColor: 'rgb(255, 159, 64)',
                yAxisID: 'y1'
            },
            {
              label: 'Количество ошибок выполнения',
              data: [125, 208, 56, 178, 73, 12, 43, 250],
                backgroundColor: 'rgba(75, 192, 192, 0.2)',
                borderColor: 'rgb(75, 192, 192)',
                yAxisID: 'y1'
            }
          ]
        };

        console.log(data);

        const config = {
          type: 'line',
          data: data,
          options: {
            responsive: true,
            interaction: {
              mode: 'index',
              intersect: false,
            },
            stacked: false,
            plugins: {
              title: {
                display: false,
                text: 'Chart.js Line Chart - Multi Axis'
              }
            },
            scales: {
              y: {
                type: 'linear',
                display: true,
                position: 'left',
              },
              y1: {
                type: 'linear',
                display: true,
                position: 'right',

                // grid line settings
                grid: {
                  drawOnChartArea: false, // only want the grid lines for one axis to show up
                },
              }
            }
          },
        };

        var ctx = document.getElementById("chartTransactionPerf01").getContext("2d");
        var floatingChart = new Chart(ctx, config);
    }
}