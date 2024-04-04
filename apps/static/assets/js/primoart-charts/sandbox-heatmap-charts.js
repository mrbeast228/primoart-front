// Heatmap data is a list of {time: <UTC Timestamp in ms>, value: <Value>} objects.
const heatmapTestData = [];

const start = new Date() * 1;
for (let i = 0; i < 7 * 24; i++) {
    heatmapTestData.push({
        time: start + 1000 * 60 * 60 * i,
        value: 0.1 + Math.random() * 99.9,
    });
}

const dayNames = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"];

function convertData(raw) {
    const adapter = new Chart._adapters._date();

    return raw.map(({time, value}) => {
        const dt = adapter.startOf(new Date(time));
        return {
            x: dt.getHours(),
            y: dayNames[(dt.getDay() + 6) % 7],
            d: dt,
            v: value
        };
    });
}

heatmapchart = {
    init: function() {
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
                data: convertData(heatmapTestData),
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
                            return ['d: ' + v.d, 'v: ' + v.v.toFixed(2)];
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

        var ctx = document.getElementById("chartHeatmap01").getContext("2d");
        var heatmapChart = new Chart(ctx, config);
    }
}
