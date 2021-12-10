var domane = 'https://colak.eu.pythonanywhere.com/';

if(window.location.hostname == '127.0.0.1'){
    domane = 'http://localhost:8000/';
}

$(document).ready(function () {
    echart_ticker_info_base();


});

function echart_ticker_info_base() {
    var $stockChart = document.querySelector('.echart-test');
    if($stockChart){
        url = domane + 'data_hub/historical_daily_price_full/'+ticker
        $.getJSON(url, function(data) {
            data=data['historical']
            var arr = data.reverse();
            var score_arr = [];
            arr = get_data_by_period(arr, 3);
            dateList = arr.map(function (item) {
                return item.date;
            });
            valueList = arr.map(function (item) {
                return item.close.toFixed(2);
            });

            if(jQuery.type(hist_data) === "string"){
                 hist_data=jQuery.parseJSON(hist_data);
            }

            hist_data = get_data_by_period(hist_data, 3);

            hist_dateList = hist_data.map(function (item) {
                return item[0];
            });
            hist_valueList = hist_data.map(function (item) {
                return item[1].toFixed(2);
            });

            var chart = window.echarts.init($stockChart);
            var options = {
                color:[utils.getColors().primary, utils.getColors().warning],
                tooltip: {
                    trigger: 'axis',
                    position: function (pt) {
                        return [pt[0], '10%'];
                    },
                },
                toolbox: {
                    feature: {
                        dataZoom: {show: true},
                        dataView: { show: true, readOnly: true },
                        restore: { show: true },
                        saveAsImage: { show: true }
                    },
                    orient: 'vertical',
                    top: '20%',
                    right: '3%',
                },
                xAxis: [
                    {
                        type: 'category',
                        data: dateList,
                        boundaryGap: false
                    },
                    {
                        type: 'category',
                        data: hist_dateList,
                        boundaryGap: false,
                        show: false
                    }
                ],
                yAxis: [
                    {
                        type: 'value',
                        name: 'Close Price',
                        min: function (value) {
                            return (value.min - 20).toFixed(0);
                        },
                        interval: 30,
                        axisLabel: {
                            formatter: '{value} $'
                        },
                        axisLine: {
                            lineStyle: {
                                color: utils.getColors().primary
                            }
                        }
                    },
                    {
                        type: 'value',
                        name: 'Stock Score',
                        min: function (value) {
                            return (value.min - 1).toFixed(0);
                        },
                        interval: 3,
                        axisLabel: {
                            formatter: '{value}'
                        },
                        axisLine: {
                            lineStyle: {
                                color: utils.getColors().warning
                            }
                        }
                    }
                ],
                dataZoom: [
                    {
                        type: 'inside',
                        start: 0,
                        end: 100
                    },
                    {
                        start: 0,
                        end: 100
                    }
                ],
                series: [
                    {
                        type: 'line',
                        name: 'Close Price',
                        data: valueList,
                        symbol: 'none',
                        smooth: true,
                        hoverAnimation: true,
                        areaStyle: {
                            color: {
                                type: 'linear',
                                x: 0,
                                y: 0,
                                x2: 0,
                                y2: 1,
                                colorStops: [{
                                        offset: 0,
                                        color: utils.rgbaColor(utils.getColors().primary, 0.5)
                                    }, {
                                        offset: 1,
                                        color: utils.rgbaColor(utils.getColors().primary, 0)
                                }]
                            }
                        }
                    },
                    {
                        type: 'line',
                        name: 'Stock Score',
                        yAxisIndex: 1,
                        xAxisIndex: 1,
                        data: hist_valueList,
                        symbol: 'none',
                        smooth: true,
                        hoverAnimation: true,
                        areaStyle: {
                            color: {
                                type: 'linear',
                                x: 0,
                                y: 0,
                                x2: 0,
                                y2: 1,
                                colorStops: [{
                                        offset: 0,
                                        color: utils.rgbaColor(utils.getColors().warning, 0.5)
                                    }, {
                                        offset: 1,
                                        color: utils.rgbaColor(utils.getColors().warning, 0)
                                }]
                            }
                        }
                    }
                ]
            };

            chart.setOption(options);
        })
    }
};

