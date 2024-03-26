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

    initFloatingChart: function() {

        const labels = ["DNS Lookup", "Connection", "SSL Handshake", "First Byte", "Content Transfer"]

        const data = {
          labels: labels,
          datasets: [
            {
              label: 'Время выполнения шагов транзакции, с',
              data: [
                [0, 0.45],
                [0.45, 0.59],
                [0.59, 0.81],
                [0.81, 1.07],
                [1.07, 1.18]
              ],
                backgroundColor: [
                  'rgba(255, 99, 132, 0.2)',
                  'rgba(255, 159, 64, 0.2)',
                  'rgba(255, 205, 86, 0.2)',
                  'rgba(75, 192, 192, 0.2)',
                  'rgba(54, 162, 235, 0.2)'
                ],
                borderColor: [
                  'rgb(255, 99, 132)',
                  'rgb(255, 159, 64)',
                  'rgb(255, 205, 86)',
                  'rgb(75, 192, 192)',
                  'rgb(54, 162, 235)'
                ]
            }
          ]
        };

        console.log(data);

        const config = {
          type: 'bar',
          data: data,
          options: {
            responsive: true,
            plugins: {
              legend: {
                position: 'top',
              },
              title: {
                display: false,
                text: ''
              }
            }
          }
        };

        var ctx = document.getElementById("chartTransactionFloationg01").getContext("2d");
        var floatingChart = new Chart(ctx, config);
    }
}