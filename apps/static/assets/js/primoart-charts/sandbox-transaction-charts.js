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

function generateData() {
  const adapter = new helpers._adapters._date();
  const data = [];
  let dt = adapter.startOf(new Date(), 'month');
  const end = adapter.endOf(dt, 'month');
  while (dt <= end) {
    const iso = adapter.format(dt, 'yyyy-MM-dd');
    data.push({
      x: Utils.isoDayOfWeek(dt),
      y: iso,
      d: iso,
      v: Math.random() * 50
    });
    dt = new Date(dt.setDate(dt.getDate() + 1));
  }
  return data;
}

steprunfloatchart = {

    init: function() {

        const labels = ["DNS Lookup", "Connection", "SSL Handshake", "First Byte", "Content Transfer", "TestTestTest", "TestTestTest", "TestTestTest", "TestTestTest", "TestTestTest", "TestTestTest", "TestTestTest", "TestTestTest", "TestTestTest", "TestTestTest", "TestTestTest", "TestTestTest", "TestTestTest", "TestTestTest", "TestTestTest", "TestTestTest"]

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
                [0.59, 0.81],
                [0.81, 0.1],
                [1, 2],
                [3, 4],
                [5, 6],
                [7, 8],
                [9, 10],
                [11, 12],
                [13, 14],
                [0.59, 0.81],
                [0.59, 0.81],
                [0.59, 0.81],
                [0.59, 0.81],
                [0.59, 0.81],
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

steprunbarchart = {

    init: function() {

        const labels = ["DNS Lookup", "Connection", "SSL Handshake", "First Byte", "Content Transfer"]

        const data = {
          labels: labels,
          datasets: [
            {
              label: 'Время выполнения шагов транзакции, с',
              data: [0.45, 0.59, 0.31, 1.07, 1.18],
                backgroundColor: [
                  'rgba(75, 192, 192, 0.2)',
                  'rgba(75, 192, 192, 0.2)',
                  'rgba(75, 192, 192, 0.2)',
                  'rgba(75, 192, 192, 0.2)',
                  'rgba(255, 99, 132, 0.2)'
                ],
                borderColor: [
                  'rgb(75, 192, 192)',
                  'rgb(75, 192, 192)',
                  'rgb(75, 192, 192)',
                  'rgb(75, 192, 192)',
                  'rgb(255, 99, 132)'
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
            scales: {
              y: {
                beginAtZero: true
              }
            },

            // Elements options apply to all of the options unless overridden in a dataset
            // In this case, we are setting the border of each horizontal bar to be 2px wide
            elements: {
              bar: {
                borderWidth: 2,
              }
            },
            plugins: {
              legend: {
                position: 'top',
                display: false
              },
              title: {
                display: false,
                text: ''
              }
            }
          }
        };

        var ctx = document.getElementById("stepRunBarChart01").getContext("2d");
        var floatingChart = new Chart(ctx, config);
    }
}

steprunfailchart = {

    init: function() {

        const labels = ["DNS Lookup", "Connection", "SSL Handshake", "First Byte", "Content Transfer"]

        const data = {
          labels: labels,
          datasets: [
            {
              label: 'Количество ошибок шага транзакции',
              data: [1, 4, 3, 12,45],
                backgroundColor: [
                  'rgba(255, 99, 132, 0.2)',
                  'rgba(255, 99, 132, 0.2)',
                  'rgba(255, 99, 132, 0.2)',
                  'rgba(255, 99, 132, 0.2)',
                  'rgba(255, 99, 132, 0.2)'
                ],
                borderColor: [
                  'rgb(255, 99, 132)',
                  'rgb(255, 99, 132)',
                  'rgb(255, 99, 132)',
                  'rgb(255, 99, 132)',
                  'rgb(255, 99, 132)'
                ]
            }
          ]
        };

        console.log(data);

        const config = {
          type: 'bar',
          data: data,
          options: {
            indexAxis: 'y',
            // Elements options apply to all of the options unless overridden in a dataset
            // In this case, we are setting the border of each horizontal bar to be 2px wide
            elements: {
              bar: {
                borderWidth: 2,
              }
            },
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
          },
        };

        var ctx = document.getElementById("transactionStepFailChart01").getContext("2d");
        var floatingChart = new Chart(ctx, config);
    }
}

performancechart = {

    init: function() {

        const labels = ["18.03.2024", "19.03.2024", "20.03.2024", "21.03.2024", "22.03.2024", "23.03.2024", "24.03.2024", "25.03.2024"];

        const data = {
          labels: labels,
          datasets: [
            {
              label: 'Количество транзакций за сутки',
              data: [1285, 1175, 2357, 1245, 1624, 476, 328, 1134],
                backgroundColor: 'rgba(255, 159, 64, 0.2)',
                borderColor: 'rgb(255, 159, 64)',
                yAxisID: 'y'
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

heatmapchart2 = {

    init: function() {

        const chart = new Chart('chartheatmap01', {
          type: 'matrix',
          data: {
            datasets: [{
              label: 'Basic matrix',
              data: [{x: 1, y: 1}, {x: 2, y: 1}, {x: 1, y: 2}, {x: 2, y: 2}],
              borderWidth: 1,
              borderColor: 'rgba(0,0,0,0.5)',
              backgroundColor: 'rgba(200,200,0,0.3)',
              width: ({chart}) => (chart.chartArea || {}).width / 2 - 1,
              height: ({chart}) => (chart.chartArea || {}).height / 2 - 1,
            }],
          },
          options: {
            scales: {
              x: {
                display: false,
                min: 0.5,
                max: 2.5,
                offset: false
              },
              y: {
                display: false,
                min: 0.5,
                max: 2.5
              }
            }
          }
        });

    }
}

servicetimevserrchart = {
    init: function() {

        const labels = ["Управление кассовыми операциями", "Оценка кредитоспособности", "Управление корпоративными счетами", "Управление инвестиционными портфелями", "Анализ кредитных заявок"]

        const data = {
          labels: labels,
          datasets: [
            {
              label: 'Среднее время выполнения транзакций, с',
              data: [150, 400, 320, 840, 500],
                backgroundColor: 'rgba(75, 192, 192, 0.2)',
                borderColor: 'rgb(75, 192, 192)',
                order: 1,
                yAxisID: 'y'
            },
            {
              label: 'Процент ошибок выполнения',
              data: [5, 24, 37, 5, 30],
                backgroundColor: 'rgba(75, 192, 192, 0.2)',
                borderColor: 'rgb(75, 192, 192)',
                type: 'line',
                order: 0,
                yAxisID: 'y1'
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
                display: true
              },
              title: {
                display: false,
                text: ''
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
                min: 0,
                max: 100,
                // grid line settings
                grid: {
                  drawOnChartArea: false, // only want the grid lines for one axis to show up
                },
              }
            }
          }
        };

        var ctx = document.getElementById("transactionTimeVsErrsChart01").getContext("2d");
        var floatingChart = new Chart(ctx, config);
    }
}

transactionrunbarchart = {
    init: function() {

        const labels = ["< 30 c", "30-60 c", "60-120 c", "120-300 c", "> 300 c"]

        const data = {
          labels: labels,
          datasets: [
            {
              label: 'Робот "Москва", количество транзакций',
              data: [150, 400, 320, 840, 30],
                backgroundColor: 'rgba(75, 192, 192, 0.2)',
                borderColor: 'rgb(75, 192, 192)'
            },
            {
              label: 'Робот "Волгоград", количество транзакций',
              data: [50, 120, 40, 310, 50],
                backgroundColor: 'rgba(255, 205, 86, 0.2)',
                borderColor: 'rgb(255, 205, 86)'
            }
          ]
        };

        console.log(data);

        const config = {
          type: 'bar',
          data: data,
          options: {
            responsive: true,
            scales: {
              x: {
                stacked: true,
              },
              y: {
                stacked: true,
                beginAtZero: true
              }
            },

            // Elements options apply to all of the options unless overridden in a dataset
            // In this case, we are setting the border of each horizontal bar to be 2px wide
            elements: {
              bar: {
                borderWidth: 2,
              }
            },
            plugins: {
              legend: {
                position: 'top',
                display: true
              },
              title: {
                display: false,
                text: ''
              }
            }
          }
        };

        var ctx = document.getElementById("transactionRunBarChart01").getContext("2d");
        var floatingChart = new Chart(ctx, config);
    }
}

transactionrundonutchart = {
    init: function() {

        const labels = ["< 30 c", "30-60 c", "60-120 c", "120-300 c", "> 300 c"]

        const data = {
          labels: ['OK', 'Warning', 'Failed'],
          datasets: [
            {
              label: 'Dataset 1',
              data: [1578, 315, 17],
              backgroundColor: ['red', 'yellow', 'green'],
            }
          ]
        };

        console.log(data);

        const config = {
          type: 'doughnut',
          data: data,
          options: {
            responsive: true,
            plugins: {
              legend: {
                position: 'top',
              },
              title: {
                display: true,
                text: 'Chart.js Doughnut Chart'
              }
            }
          },
        };

        var ctx = document.getElementById("transactionRunDonutChart01").getContext("2d");
        var floatingChart = new Chart(ctx, config);
    }
}

transactionrunhorizontalchart = {
    init: function() {

        const labels = ["OK", "Failed"]

        const data = {
          labels: labels,
          datasets: [
            {
              label: 'Робот "Москва"',
              data: [1578, 315],
                backgroundColor: 'rgba(75, 192, 192, 0.2)',
                borderColor: 'rgb(75, 192, 192)'
            },
            {
              label: 'Робот "Волгоград"',
              data: [215, 56],
                backgroundColor: 'rgba(255, 205, 86, 0.2)',
                borderColor: 'rgb(255, 205, 86)'
            }
          ]
        };

        console.log(data);

        const config = {
          type: 'bar',
          data: data,
          options: {
            indexAxis: 'y',
            // Elements options apply to all of the options unless overridden in a dataset
            // In this case, we are setting the border of each horizontal bar to be 2px wide
            elements: {
              bar: {
                borderWidth: 2,
              }
            },
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
          },
        };

        var ctx = document.getElementById("transactionRunHorizontalChart01").getContext("2d");
        var floatingChart = new Chart(ctx, config);
    }
}

scatterstatuschart = {
    init: function() {

        const data = {
          datasets: [
          {
            label: 'OK',
            data: [{
              x: -10,
              y: 0
            }, {
              x: 0,
              y: 10
            }, {
              x: 10,
              y: 5
            }, {
              x: 0.5,
              y: 5.5
            }],
            backgroundColor: 'rgb(255, 99, 132)'
          },
          {
            label: 'Failed',
            data: [{
              x: -15,
              y: 2
            }, {
              x: 3,
              y: 17
            }, {
              x: 27,
              y: 1
            }, {
              x: 16,
              y: 4
            }],
            backgroundColor: 'rgb(75, 140, 60)'
          }
        ],
        };

        const config = {
          type: 'scatter',
          data: data,
          options: {
            scales: {
              x: {
                type: 'linear',
                position: 'bottom'
              }
            }
          }
        };

        var ctx = document.getElementById("transactionScatterChart01").getContext("2d");
        var scatterChart = new Chart(ctx, config);
    }
}