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

const colors = [
    ['rgba(255, 99, 132, 0.2)', 'rgba(255, 99, 132)'],
    ['rgba(255, 159, 64, 0.2)', 'rgba(255, 159, 64)'],
    ['rgba(255, 205, 86, 0.2)', 'rgba(255, 205, 86)'],
    ['rgba(75, 192, 192, 0.2)', 'rgba(75, 192, 192)'],
    ['rgba(54, 162, 235, 0.2)', 'rgba(54, 162, 235)']
];

function getColor(idx) {
    return colors[idx % colors.length];
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
    mockData: [
        {
            step_name: "DNS Lookup",
            time: 0.45,
            status: 'OK',
        }, {
            step_name: "Connection",
            time: 0.59,
            status: 'OK',
        }, {
            step_name: "SSL Handshake",
            time: 0.31,
            status: 'OK',
        }, {
            step_name: "First Byte",
            time: 1.07,
            status: 'OK',
        }, {
            step_name: "Content Transfer",
            time: 1.18,
            status: 'ERR',
        },
    ],
    init: function(canvasId, dataset) {
        console.log(dataset);

        if (dataset === undefined) {
            dataset = steprunbarchart.mockData;
        }

        const labels = dataset.map(({step_name}) => step_name);

        const data = {
          labels: labels,
          datasets: [
            {
              label: 'Время выполнения шагов транзакции, с',
              data: dataset.map(({time}) => time),
                backgroundColor: dataset.map(({status}) => (status == 'OK' ? 'rgba(75, 192, 192, 0.2)' : 'rgba(255, 99, 132, 0.2)')),
                borderColor: dataset.map(({status}) => (status == 'OK' ? 'rgb(75, 192, 192)' : 'rgb(255, 99, 132)')),
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

        var ctx = document.getElementById(canvasId).getContext("2d");
        var floatingChart = new Chart(ctx, config);
    },
    initFromApiByTransactionRunId: function(canvasId, transactionRunId) {
        axios.get("/charts/step_run", {params: {"transaction_run_id": transactionRunId}}).then((r) => {
            const data = r.data;
            console.log(r);
            console.log(data);

            steprunbarchart.init(canvasId, data);
        });
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

    init: function(element_id, perf_data) {

        const labels = perf_data.map(day => day["date"]);
        const all_num = perf_data.map(day => day["all_num"]);
        const err_num = perf_data.map(day => day["err_num"]);

        const data = {
          labels: labels,
          datasets: [
            {
              label: 'Количество транзакций за сутки',
              data: all_num,
                backgroundColor: 'rgba(255, 159, 64, 0.2)',
                borderColor: 'rgb(255, 159, 64)',
                yAxisID: 'y'
            },
            {
              label: 'Количество ошибок выполнения',
              data: err_num,
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

        var ctx = document.getElementById(element_id).getContext("2d");
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
    init: function(element_id, services_data) {

        const labels = services_data.map(service => service.service_name);
        const data_average_time = services_data.map(service => service.average_time);
        const data_err_percentage = services_data.map(service => service.err_percentage);

        const data = {
          labels: labels,
          datasets: [
            {
              label: 'Среднее время выполнения транзакций, с',
              data: data_average_time,
                backgroundColor: 'rgba(75, 192, 192, 0.2)',
                borderColor: 'rgb(75, 192, 192)',
                order: 1,
                yAxisID: 'y'
            },
            {
              label: 'Процент ошибок выполнения',
              data: data_err_percentage,
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

        var ctx = document.getElementById(element_id).getContext("2d");
        var floatingChart = new Chart(ctx, config);
    }
}

transactionrunbarchart = {
    mockData: [
        {
            name: 'Робот "Москва"',
            stats: {
                "0-30": 150,
                "30-60": 400,
                "60-120": 320,
                "120-300": 840,
                "300+": 30,
            },
        }, {
            name: 'Робот "Волгоград"',
            stats: {
                "0-30": 50,
                "30-60": 120,
                "60-120": 40,
                "120-300": 310,
                "300+": 50,
            },
        }
    ],
    init: function(canvasId, dataset) {
        if (dataset === undefined) {
            dataset = transactionrunbarchart.mockData;
        }

        const labels = ["< 30 c", "30-60 c", "60-120 c", "120-300 c", "> 300 c"]

        const data = {
          labels: labels,
          datasets: dataset.map(({name, stats}, idx) => {
              return {
                  label: `Робот "${name}", количество транзакций`,
                  data: [stats["0-30"], stats["30-60"], stats["60-120"], stats["120-300"], stats["300+"]],
                  backgroundColor: getColor(idx)[0],
                  borderColor: getColor(idx)[1],
              }
          }),
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

        var ctx = document.getElementById(canvasId).getContext("2d");
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
    mockData: [
        {
            name: 'Робот "Москва"',
            stats: {
                ok: 1578,
                failed: 315
            },
        }, {
            name: 'Робот "Волгоград"',
            stats: {
                ok: 215,
                failed: 56
            },
        }
    ],
    init: function(canvasId, dataset) {
        if (dataset === undefined) {
            dataset = transactionrunhorizontalchart.mockData;
        }

        const labels = ["OK", "Failed"]

        const data = {
          labels: labels,
          datasets: dataset.map(({name, stats: {ok, failed}}, idx) => {
              return {
                  label: name,
                  data: [ok, failed],
                  backgroundColor: getColor(idx)[0],
                  borderColor: getColor(idx)[1],
              };
          }),
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

        var ctx = document.getElementById(canvasId).getContext("2d");
        var floatingChart = new Chart(ctx, config);
    }
}

const defaultScatterData = {
  "OK": [
    {
      x: "2024-01-01",
      y: 0
    },
    {
      x: "2024-01-02",
      y: 10
    },
    {
      x: "2024-01-03",
      y: 5
    },
    {
      x: "2024-01-04",
      y: 5.5
    }
  ],
  "Failed": [
    {
      x: "2024-02-01",
      y: 2
    },
    {
      x: "2024-02-02",
      y: 17
    },
    {
      x: "2024-02-03",
      y: 1
    },
    {
      x: "2024-02-04",
      y: 4
    }
  ]
}

scatterstatuschart = {
    init: function(element_id, transaction_data) {
        if (transaction_data === undefined) {
          transaction_data = defaultScatterData
        }
        const data = {
          datasets: [
          {
            label: 'OK',
            data: transaction_data["OK"],
            backgroundColor: 'rgb(75, 140, 60)'
          },
          {
            label: 'Failed',
            data: transaction_data["Failed"],
            backgroundColor: 'rgb(255, 99, 132)'
          }
        ],
        };

        const options = {
          scales: {
              x: {
                type: "time",
                title: {
                    text: "Transaction time",
                    display: true,
                },
                position: 'bottom',

              },
              y: {
                type: 'linear',
                title: {
                    text: "Response time, microseconds",
                    display: true,
                },
                position: "left"
              }
            }
        }

        const config = {
          type: 'scatter',
          data: data,
          options: options
        };

        var ctx = document.getElementById(element_id).getContext("2d");
        var scatterChart = new Chart(ctx, config);
    },
    initFromApiByService(element_id, service_id) {
        axios.get("/charts/runs", {params: {"service_id": service_id}}).then((response) => {
            const data = response.data;

            scatterstatuschart.init(element_id, data);
        });
    }
}
