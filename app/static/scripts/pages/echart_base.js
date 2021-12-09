var domane = 'https://colak.eu.pythonanywhere.com/';

if(window.location.hostname == '127.0.0.1'){
    domane = 'http://localhost:8000/';
}

var TICKER_INFO_DATA = [];
var TICKER_INFO_HIST_DATA = [];

$(document).ready(function () {
    $('.echart-btn').on('click',function(){
        var period = parseInt($(this).data('period'));
        var function_name = $(this).data('function-name');
        change_period(period, function_name);
    })

    echart_ticker_info_base();

});

//************ BASE FUNCTIONS ************//
function get_data_by_period(arr, month_period){
    if(month_period > 0){
        var now = new Date();
        now.setMonth(now.getMonth()-month_period);
        var period = now.getFullYear() + '-' + (now.getMonth()+1) + '-' + now.getDate();
        if(jQuery.type(arr[0])==='object'){
            return arr.filter(x => new Date(x.date) >= new Date(period));
        }
        else return arr.filter(x => new Date(x[0]) >= new Date(period));
    }
    else return arr;
}

function change_period(period, function_name){
    if(function_name == 'ticker_info'){
        var base_arr = get_data_by_period(TICKER_INFO_DATA, period);
        var hist_data = get_data_by_period(TICKER_INFO_HIST_DATA, period);
        var dates = base_arr.filter(x => new Date(x.date) < new Date(hist_data[0][0]));
        if(dates.length > 0){
            hist_data = hist_data.reverse();
            dates = dates.reverse();
            $.each(dates, function( index, d ){
                hist_data.push([d.date, 0]);
            })
            hist_data = hist_data.reverse();
        }
        var $stockChart = document.querySelector('.echart-test');
        draw_echart_ticker_info_base(base_arr, hist_data, $stockChart);
    }
}

function echart_xAxis(data, is_show){
    return {
                type: 'category',
                data: data,
                boundaryGap: false,
                show: is_show
            };
}

function echart_yAxis(name, diff, interval, label, color){
    return {
        type: 'value',
        name: name,
        min: function (value) {
            return (value.min - diff).toFixed(0);
        },
        interval: interval,
        axisLabel: {
            formatter: label
        },
        axisLine: {
            lineStyle: {
                color: color
            }
        }
    };
}

function echart_series(name, axis_index, data, color){
    return {
                type: 'line',
                name: name,
                yAxisIndex: axis_index,
                xAxisIndex: axis_index,
                data: data,
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
                                color: utils.rgbaColor(color, 0.5)
                            }, {
                                offset: 1,
                                color: utils.rgbaColor(color, 0)
                        }]
                    }
                }
            };
}

function echart_default_options(){
    return {
                color:[],
                tooltip: {
                    trigger: 'axis',
                    axisPointer: {
                        animation: false,
                        type: 'cross',
                        lineStyle: {
                            color: '#376df4',
                            width: 2,
                            opacity: 1
                        }
                    }
                },
                toolbox: {
                    feature: {
                        dataZoom: {show: true},
                        dataView: {
                            show: true,
                            readOnly: true,
                            optionToContent: function(opt) {
                                var axisData = opt.xAxis[0].data;
                                var series = opt.series;
                                var table = '<table class="table table-striped overflow-hidden">'
                                             +'<thead><tr class="btn-reveal-trigger">'
                                             +'<th scope="col">Date</th>'
                                             +'<th scope="col">' + series[0].name + '</th>'
                                             +'<th class="text-end" scope="col">' + series[1].name + '</th>'
                                             +'</tr></thead>'
                                             +'<tbody>';
                                for (var i = 0, l = axisData.length; i < l; i++) {
                                    table += '<tr class="btn-reveal-trigger">'
                                             + '<td>' + axisData[i] + '</td>'
                                             + '<td>' + series[0].data[i] + '</td>'
                                             + '<td class="text-end">' + series[1].data[i] + '</td>'
                                             + '</tr>';
                                }
                                table += '</tbody></table>';
                                return table;
                            }
                        },
                        restore: { show: true },
                        saveAsImage: { show: true }
                    },
                    orient: 'vertical',
                    top: '20%',
                    right: '3%',
                },
                xAxis: [],
                yAxis: [],
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
                series: [],
                legend: {
                    data: [],
                    inactiveColor: '#777',
                    show: false
                }
            };
}


//********** END BASE FUNCTIONS **********//



//***** TICKER INFO *****//
function echart_ticker_info_base() {
    var $stockChart = document.querySelector('.echart-test');
    if($stockChart){
        url = domane + 'data_hub/historical_daily_price_full/'+ticker
        $.getJSON(url, function(data) {
            data=data['historical']
            TICKER_INFO_DATA = data.reverse();
            var arr = get_data_by_period(TICKER_INFO_DATA, 3);

            if(jQuery.type(hist_data) === "string"){
                 TICKER_INFO_HIST_DATA = jQuery.parseJSON(hist_data);
            }
            else{
                TICKER_INFO_HIST_DATA = hist_data;
            }
            hist_data = get_data_by_period(TICKER_INFO_HIST_DATA, 3);
            draw_echart_ticker_info_base(arr, hist_data, $stockChart);
        })
    }
};

function echart_ticker_info_base_options(dateList, hist_dateList, valueList, hist_valueList){
    var options = echart_default_options();
    options.color.push(utils.getColors().primary);
    options.color.push(utils.getColors().warning);
    options.xAxis.push(echart_xAxis(dateList, true));
    options.xAxis.push(echart_xAxis(hist_dateList, false));
    options.yAxis.push(echart_yAxis('Close Price',20, 30, '{value} $', utils.getColors().primary));
    options.yAxis.push(echart_yAxis('Stock Score',1, 3, '{value}', utils.getColors().warning));
    options.series.push(echart_series('Close Price', 0, valueList, utils.getColors().primary));
    options.series.push(echart_series('Stock Score', 1, hist_valueList, utils.getColors().warning));
    options.legend.data.push('Close Price');
    options.legend.data.push('Stock Score');
//    options.legend.show = true;
    return options;
}

function draw_echart_ticker_info_base(base_arr, hist_data, $stockChart){
    dateList = base_arr.map(function (item) {
        return item.date;
    });
    valueList = base_arr.map(function (item) {
        return item.close.toFixed(2);
    });
    hist_dateList = hist_data.map(function (item) {
        return item[0];
    });
    hist_valueList = hist_data.map(function (item) {
        return item[1].toFixed(2);
    });
    var chart = window.echarts.init($stockChart);
    var options = echart_ticker_info_base_options(dateList, hist_dateList, valueList, hist_valueList);
    chart.setOption(options);
}


