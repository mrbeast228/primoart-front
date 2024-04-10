// Heatmap data is a list of {time: <UTC Timestamp in ms>, value: <Value>, trxId: <transaction id>} objects.
const heatmapTestData = [];

const start = new Date() * 1;
for (let i = 0; i < 7 * 24; i++) {
    heatmapTestData.push({
        time: start + 1000 * 60 * 60 * i,
        value: 0.1 + Math.random() * 99.9,
        // trxId: i,
    });
}

const dayNames = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"];

function convertData(raw) {
    const adapter = new Chart._adapters._date();

    return raw.map(({time, value, trxId}) => {
        const dt = adapter.startOf(new Date(time));
        return {
            x: dt.getHours(),
            y: dayNames[(dt.getDay() + 6) % 7],
            d: dt,
            v: value,
            // trxId: trxId,
        };
    });
}

heatmapchart = {
    init: function(canvasId, dataset) {
        if (dataset === undefined) {
            dataset = heatmapTestData;
        }

        const scales = {
            y: {
                type: 'category',
                labels: dayNames.reverse(),
                position: "right",
                offset: true,
                grid: { display: false },
            },
            x: {
                type: 'linear',
                title: {
                    text: "Hour of the day",
                    display: true,
                },
                min: 0,
                max: 23,
                position: 'bottom',
                offset: true,
                ticks: { stepSize: 1, },
                grid: { display: false },
            }
        };

        const data = {
            datasets: [{
                data: convertData(dataset),
                backgroundColor(c) {
                    const value = c.dataset.data[c.dataIndex].v;
                    const alpha = value / 100;
                    return Chart.helpers.color('green').alpha(alpha).rgbString();
                },
                borderColor(c) {
                    const value = c.dataset.data[c.dataIndex].v;
                    const alpha = value / 100;
                    return Chart.helpers.color('green').alpha(alpha).darken(0.3).rgbString();
                },
                borderWidth: 1,
                hoverBackgroundColor: 'yellow',
                hoverBorderColor: 'yellowgreen',
                height(c) {
                    const a = c.chart.chartArea || {};
                    return (a.bottom - a.top) / 7 - 1;
                },
                width(c) {
                    const a = c.chart.chartArea || {};
                    return (a.right - a.left) / 24 - 1;
                }
            }]
        };

        const options = {
            plugins: {
                legend: false,
                tooltip: {
                    displayColors: false,
                    callbacks: {
                        title() {
                            return '';
                        },
                        label(context) {
                            const v = context.dataset.data[context.dataIndex];
                            return [
                                "Дата: " + v.d,
                                "Время выполнения, с: " + v.v.toFixed(2),
                            ];
                        }
                    }
                },
            },
            scales: scales,
            layout: {
                padding: {
                    top: 10
                }
            }
        };

        const config = {
            type: 'matrix',
            data: data,
            options: options,
        };

        var canvas = document.getElementById(canvasId);
        var ctx = canvas.getContext("2d");
        var heatmapChart = new Chart(ctx, config);

        // canvas.onclick = function(e) {
        //     var block = heatmapChart.getElementsAtEventForMode(e, 'nearest', {intersect: true}, true);
        //     if (!block.length) return;
        //     var blockData = data.datasets[block[0].datasetIndex].data[block[0].index];
        //     window.open("/mvp-transaction.html?transaction_id=" + blockData.trxId);
        // }

        return heatmapChart;
    }
}
