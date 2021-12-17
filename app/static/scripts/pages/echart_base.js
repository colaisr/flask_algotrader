var domane = 'https://colak.eu.pythonanywhere.com/';

if(window.location.hostname == '127.0.0.1'){
    domane = 'http://localhost:8000/';
}

var TICKER_INFO_DATA = [];
var TICKER_INFO_HIST_DATA = [];
var TICKER_INFO_TECHNICAL_SMA = []
var TICKER_INFO_TECHNICAL_EMA = []
var TICKER_INFO_TECHNICAL_WMA = []
var TICKER_INFO_TECHNICAL_DEMA = []
var TICKER_INFO_TECHNICAL_TEMA = []
var TICKER_INFO_TECHNICAL_WILLIAMS = []
var TICKER_INFO_TECHNICAL_RSI = []
var TICKER_INFO_TECHNICAL_ADX = []
var TICKER_INFO_TECHNICAL_STANDARD_DEVIATION = []
//*********************************
var TODAY_SNP = []
var TODAY_EMOTION = []
//*********************************

$(document).ready(function () {
    $('.echart-btn').on('click',function(){
        var period = parseInt($(this).data('period'));
        var function_name = $(this).data('function-name');
        change_period(period, function_name);
    })

    $('.echart-legend').on('change',function(){
        draw_graph_by_legends();
    })

    get_technical_data();
    echart_ticker_info_base();
    echart_ticker_info_technical();

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
        var $stockChart = document.querySelector('.echart-icker-info');
        draw_echart_ticker_info_base(base_arr, hist_data, $stockChart);
    }
    else if(function_name == 'ticker_info_technical'){
        draw_graph_by_legends();
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

function echart_series(name, data, axis_index=0, color=utils.getColors().primary, lineWidth=2){
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
                },
                lineStyle:{
                    width: lineWidth
                }
            };
}

function echart_legend(selected){
    return {
        inactiveColor: '#777',
        show: true,
        type: "plain",
        selected: selected,
//        tooltip:
    };
}

function echart_default_options(){
    return {
                title: {
                    show: false,
                    text: '',
                    textStyle: {
                        fontWeight: 'bold'
                    }
                },
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
//                toolbox: {
//                    feature: {
//                        dataZoom: {show: true},
//                        dataView: {
//                            show: true,
//                            readOnly: true,
//                            optionToContent: function(opt) {
//                                var axisData = opt.xAxis[0].data;
//                                var series = opt.series;
//                                var table = '<table class="table table-striped overflow-hidden">'
//                                             +'<thead><tr class="btn-reveal-trigger">'
//                                             +'<th scope="col">Date</th>'
//                                             +'<th scope="col">' + series[0].name + '</th>'
//                                             +'<th class="text-end" scope="col">' + series[1].name + '</th>'
//                                             +'</tr></thead>'
//                                             +'<tbody>';
//                                for (var i = 0, l = axisData.length; i < l; i++) {
//                                    table += '<tr class="btn-reveal-trigger">'
//                                             + '<td>' + axisData[i] + '</td>'
//                                             + '<td>' + series[0].data[i] + '</td>'
//                                             + '<td class="text-end">' + series[1].data[i] + '</td>'
//                                             + '</tr>';
//                                }
//                                table += '</tbody></table>';
//                                return table;
//                            }
//                        },
////                        restore: { show: true },
//                        saveAsImage: { show: true }
//                    },
//                    orient: 'vertical',
//                    top: '20%',
//                    right: '3%',
//                },
                xAxis: [],
                yAxis: [],
                dataZoom: [
                    {
                        textStyle: {
                            color: '#8392A5'
                        },
                        handleIcon: 'path://M10.7,11.9v-1.3H9.3v1.3c-4.9,0.3-8.8,4.4-8.8,9.4c0,5,3.9,9.1,8.8,9.4v1.3h1.3v-1.3c4.9-0.3,8.8-4.4,8.8-9.4C19.5,16.3,15.6,12.2,10.7,11.9z M13.3,24.4H6.7V23h6.6V24.4z M13.3,19.6H6.7v-1.4h6.6V19.6z',
                        dataBackground: {
                            areaStyle: {
                                color: '#8392A5'
                            },
                            lineStyle: {
                                opacity: 0.8,
                                color: '#8392A5'
                            }
                        },
                        brushSelect: true
                    },
                    {
                        type: 'inside'
                    }
                ],
                series: [],
                legend: {
                    show: false
                }
            };
}


//********** END BASE FUNCTIONS **********//



//***** TICKER INFO *****//
function echart_ticker_info_base() {
    var $stockChart = document.querySelector('.echart-icker-info');
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
    options.series.push(echart_series('Close Price', valueList));
    options.series.push(echart_series('Stock Score', hist_valueList, 1, utils.getColors().light, 0.7));
    options.legend = echart_legend({'Stock Score': false});
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

//***** TICKER INFO TECHNICAL ****//

function get_technical_data(){
    var $stockChart = document.querySelector('.echart-ticker-info-technical');
    if($stockChart){
        var url_ema = domane + 'data_hub/technical_indicators?ticker=' + ticker + '&type=ema';
        var url_wma = domane + 'data_hub/technical_indicators?ticker=' + ticker + '&type=wma';
        var url_dema = domane + 'data_hub/technical_indicators?ticker=' + ticker + '&type=dema';
        var url_tema = domane + 'data_hub/technical_indicators?ticker=' + ticker + '&type=tema';
        var url_williams = domane + 'data_hub/technical_indicators?ticker=' + ticker + '&type=williams';
        var url_rsi = domane + 'data_hub/technical_indicators?ticker=' + ticker + '&type=rsi';
        var url_adx = domane + 'data_hub/technical_indicators?ticker=' + ticker + '&type=adx';
        var url_standard_deviation = domane + 'data_hub/technical_indicators?ticker=' + ticker + '&type=standardDeviation';

        Promise.all([
                $.ajax({ url: url_ema }),
                $.ajax({ url: url_wma }),
                $.ajax({ url: url_dema }),
                $.ajax({ url: url_tema }),
                $.ajax({ url: url_williams }),
                $.ajax({ url: url_rsi }),
                $.ajax({ url: url_adx }),
                $.ajax({ url: url_standard_deviation })
            ])
            .then(([ema, wma, dema, tema, williams, rsi, adx, standard_deviation]) => {
                TICKER_INFO_TECHNICAL_EMA = ema.reverse();
                TICKER_INFO_TECHNICAL_WMA = wma.reverse();
                TICKER_INFO_TECHNICAL_DEMA = dema.reverse();
                TICKER_INFO_TECHNICAL_TEMA = tema.reverse();
                TICKER_INFO_TECHNICAL_WILLIAMS = williams.reverse();
                TICKER_INFO_TECHNICAL_RSI = rsi.reverse();
                TICKER_INFO_TECHNICAL_ADX = adx.reverse();
                TICKER_INFO_TECHNICAL_STANDARD_DEVIATION = standard_deviation.reverse();
            });
    }
}

function echart_ticker_info_technical() {
    var $stockChart = document.querySelector('.echart-ticker-info-technical');
    if($stockChart){
        var url_sma = domane + 'data_hub/technical_indicators?ticker=' + ticker + '&type=sma';

        $.getJSON(url_sma, function(data) {
            TICKER_INFO_TECHNICAL_SMA = data.reverse();
            draw_graph_by_legends();
        })
    }
};

function echart_ticker_info_technical_options(dateList){
    var options = {
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
            },
            formatter: _tooltipFormatter
        },
//        toolbox: {
//            feature: {
//                dataZoom: {show: true},
//                dataView: {
//                    show: true,
//                    readOnly: true,
//                    optionToContent: function(opt) {
//                        var axisData = opt.xAxis[0].data;
//                        var series = opt.series;
//                        var table = '<table class="table table-striped overflow-hidden">'
//                                     +'<thead><tr class="btn-reveal-trigger">'
//                                     +'<th scope="col">Date</th>';
//                        for (var i = 0, l = series.length-1; i < l; i++) {
//                            table += '<th scope="col">' + series[i].name + '</th>';
//                        }
//                        table += '<th class="text-end" scope="col">' + series[series.length-1].name + '</th>'
//                                +'</tr></thead>'
//                                +'<tbody>';
//                        for (var i = 0, l = axisData.length; i < l; i++) {
//                            table += '<tr class="btn-reveal-trigger">'
//                                     + '<td>' + axisData[i] + '</td>';
//                            for (var k = 0, s = series.length-1; k < s; k++) {
//                                table += '<td>' + series[k].data[i] + '</td>';
//                            }
//                            table += '<td class="text-end">' + series[series.length-1].data[i] + '</td></tr>';
//                        }
//                        table += '</tbody></table>';
//                        return table;
//                    }
//                },
//                saveAsImage: { show: true }
//            }
//        },
        grid: [
            {
                left: '5%',
                right: '5%',
                bottom: 200,
                height: 200
            },
            {
                left: '5%',
                right: '5%',
                height: 80,
                bottom: 80
            }
        ],
        xAxis: [
            {
                type: 'category',
                scale: true,
                data: dateList,
                boundaryGap: false
            },
            {
                type: 'category',
                gridIndex: 1,
                data: dateList,
                axisLine: { onZero: false },
                axisTick: { show: false },
                splitLine: { show: false },
                axisLabel: { show: false },
                scale: true,
                boundaryGap: false
            }
        ],
        yAxis: [
            {
                type: 'value',
                name: name,
                min: function (value) {
                    return (value.min - 5).toFixed(0);
                },
                interval: 20,
                axisLabel: {
                    formatter: '{value} $'
                }
            },
            {
                scale: true,
                gridIndex: 1,
                splitNumber: 2,
                axisLabel: { show: false },
                axisLine: { show: false },
                axisTick: { show: false },
                splitLine: { show: false }
            }
        ],
        dataZoom: [
            {
                textStyle: {
                    color: '#8392A5'
                },
                handleIcon: 'path://M10.7,11.9v-1.3H9.3v1.3c-4.9,0.3-8.8,4.4-8.8,9.4c0,5,3.9,9.1,8.8,9.4v1.3h1.3v-1.3c4.9-0.3,8.8-4.4,8.8-9.4C19.5,16.3,15.6,12.2,10.7,11.9z M13.3,24.4H6.7V23h6.6V24.4z M13.3,19.6H6.7v-1.4h6.6V19.6z',
                dataBackground: {
                    areaStyle: {
                        color: '#8392A5'
                    },
                    lineStyle: {
                        opacity: 0.8,
                        color: '#8392A5'
                    }
                },
                brushSelect: true
            },
            {
                type: 'inside'
            }
        ],
        series: [],
//        legend: {
//            data: ['SMA', 'EMA','WMA','DEMA','TEMA','WILLIAMS','RSI','ADX','Standart Deviation'],
//            inactiveColor: '#777',
//            selected: {
//                'EMA': false,
//                'WMA': false,
//                'DEMA': false,
//                'TEMA': false,
//                'WILLIAMS': false,
//                'RSI': false,
//                'ADX': false,
//                'Standart Deviation': false
//            },
//            orient: 'vertical',
//            right: 0,
//            top: 100,
//            tooltip: {
//                show: true,
//                formatter: _tooltipFormatter,
//                triggerOn: "mousemove|click",
//
//                appendToBody: true,
//                trigger: "item"
//            }
//        }
    };
    return options;
}

var _tooltipFormatter = function _tooltipFormatter(params) {
    var content = '<div><h6 class="mb-2 text-700">' + window.dayjs(params[0].axisValue).format('MMM DD, YYYY')
                +'</h6><div>';
    var i = 0;
    if(params[0].axisIndex == 0){
        i = 1;
        content += '<div class="fs--1 text-700 d-flex">'
                + '<span class="fas fa-circle fa-xs align-self-center" style="color:' + params[0].color + '"></span><span class="ps-1">'
                + 'open</span><span class="ps-3 ws-bold ms-auto">' + params[0].value[1] + '</span></div>'
                + '<div class="fs--1 text-700 d-flex">'
                + '<span class="fas fa-circle fa-xs align-self-center" style="color:' + params[0].color + '"></span><span class="ps-1">'
                + 'close</span><span class="ps-3 ws-bold ms-auto">' + params[0].value[2] + '</span></div>'
                + '<div class="fs--1 text-700 d-flex">'
                + '<span class="fas fa-circle fa-xs align-self-center" style="color:' + params[0].color + '"></span><span class="ps-1">'
                + 'lowest</span><span class="ps-3 ws-bold ms-auto">' + params[0].value[3] + '</span></div>'
                + '<div class="fs--1 text-700 d-flex">'
                + '<span class="fas fa-circle fa-xs align-self-center" style="color:' + params[0].color + '"></span><span class="ps-1">'
                + 'highest</span><span class="ps-3 ws-bold ms-auto">' + params[0].value[4] + '</span></div>';
    }

    for (i, l = params.length; i < l; i++) {
        content += '<div class="fs--1 text-700 d-flex">'
                   + '<span class="fas fa-circle align-self-center" style="color: ' + get_color(params[i].seriesName) + '"></span><span class="ps-1">'
                   + params[i].seriesName + '</span><span class="ps-3 ws-bold ms-auto">' + params[i].value + '</span></div>';
    }
    content += '</div></div>';
    return content;
};

function draw_graph_by_legends(){
    var period = $('.echart-technical:checked').data('period');
    var arr = get_data_by_period(TICKER_INFO_TECHNICAL_SMA, period);
    var obj = get_date_and_value_lists(arr);
    var options = echart_ticker_info_technical_options(obj.dateList);
    var series = [{
            type: 'candlestick',
            name: 'Day',
            data: obj.valueList,
            itemStyle: {
                color: '#FD1050',
                color0: '#0CF49B',
                borderColor: '#FD1050',
                borderColor0: '#0CF49B'
            }
        }];
    $.each($('.echart-legend:checked'), function(i, item)
    {
        series.push(get_series(item.id, period));
    })
    options.series = series;
    var $stockChart = document.querySelector('.echart-ticker-info-technical');
    window.echarts.dispose($stockChart);
    var chart = window.echarts.init($stockChart);
    chart.setOption(options);
}

function get_date_and_value_lists(arr){
    dateList = arr.map(function (item) {
        return item.date;
    });
    valueList = arr.map(function (item) {
        return [+item.open.toFixed(2), +item.close.toFixed(2), +item.low.toFixed(2), +item.high.toFixed(2)];
    });
    return {dateList: dateList, valueList: valueList};
}

function get_series(seria_name, period){
    if(seria_name == 'sma'){
        var arr_sma = get_data_by_period(TICKER_INFO_TECHNICAL_SMA, period);
        var sma = arr_sma.map(function (item) {
            return item.sma.toFixed(2);
        });
        return {
            name: 'SMA',
            type: 'line',
            data: sma,
            smooth: true,
            showSymbol: false,
            lineStyle: {
                width: 1,
                color: '#5470c6'
            }
        };
    }
    if(seria_name == 'ema'){
        var arr_ema = get_data_by_period(TICKER_INFO_TECHNICAL_EMA, period);
        var ema = arr_ema.map(function (item) {
            return item.ema.toFixed(2);
        });
        return {
            name: 'EMA',
            type: 'line',
            data: ema,
            smooth: true,
            showSymbol: false,
            lineStyle: {
                width: 1,
                color: '#91cc75'
            }
        };
    }
    if(seria_name == 'wma'){
        var arr_wma = get_data_by_period(TICKER_INFO_TECHNICAL_WMA, period);
        var wma = arr_wma.map(function (item) {
            return item.wma.toFixed(2);
        });
        return {
            name: 'WMA',
            type: 'line',
            data: wma,
            smooth: true,
            showSymbol: false,
            lineStyle: {
                width: 1,
                color: '#fac858'
            }
        };
    }
    if(seria_name == 'dema'){
        var arr_dema = get_data_by_period(TICKER_INFO_TECHNICAL_DEMA, period);
        var dema = arr_dema.map(function (item) {
            return item.dema.toFixed(2);
        });
        return {
            name: 'DEMA',
            type: 'line',
            data: dema,
            smooth: true,
            showSymbol: false,
            lineStyle: {
                width: 1,
                color: '#ee6666'
            }
        };
    }
    if(seria_name == 'tema'){
        var arr_tema = get_data_by_period(TICKER_INFO_TECHNICAL_TEMA, period);
        var tema = arr_tema.map(function (item) {
            return item.tema.toFixed(2);
        });
        return {
            name: 'TEMA',
            type: 'line',
            data: tema,
            smooth: true,
            showSymbol: false,
            lineStyle: {
                width: 1,
                color: '#73c0de'
            }
        };
    }
    if(seria_name == 'williams'){
        var arr_williams = get_data_by_period(TICKER_INFO_TECHNICAL_WILLIAMS, period);
        var williams = arr_williams.map(function (item) {
            return item.williams.toFixed(2);
        });
        return {
            name: 'WILLIAMS',
            type: 'line',
            xAxisIndex: 1,
            yAxisIndex: 1,
            data: williams,
            smooth: true,
            showSymbol: false,
            lineStyle: {
                width: 1,
                color: '#3ba272'
            }
        };
    }
    if(seria_name == 'rsi'){
        var arr_rsi = get_data_by_period(TICKER_INFO_TECHNICAL_RSI, period);
        var rsi = arr_rsi.map(function (item) {
            return item.rsi.toFixed(2);
        });
        return {
            name: 'RSI',
            type: 'line',
            xAxisIndex: 1,
            yAxisIndex: 1,
            data: rsi,
            smooth: true,
            showSymbol: false,
            lineStyle: {
                width: 1,
                color: '#fc8452'
            }
        };
    }
    if(seria_name == 'adx'){
        var arr_adx = get_data_by_period(TICKER_INFO_TECHNICAL_ADX, period);
        var adx = arr_adx.map(function (item) {
            return item.adx.toFixed(2);
        });
        return {
            name: 'ADX',
            type: 'line',
            xAxisIndex: 1,
            yAxisIndex: 1,
            data: adx,
            smooth: true,
            showSymbol: false,
            lineStyle: {
                width: 1,
                color: '#9a60b4'
            }
        };
    }
    if(seria_name == 'standardDeviation'){
        var arr_standard_deviation = get_data_by_period(TICKER_INFO_TECHNICAL_STANDARD_DEVIATION, period);
        var standard_deviation = arr_standard_deviation.map(function (item) {
            return item.standardDeviation.toFixed(2);
        });
        return {
            name: 'Standart Deviation',
            type: 'line',
            xAxisIndex: 1,
            yAxisIndex: 1,
            data: standard_deviation,
            smooth: true,
            showSymbol: false,
            lineStyle: {
                width: 1,
                color: '#ea7ccc'
            }
        };
    }
}

function get_color(seria_name){
    if(seria_name == 'SMA'){
        return '#5470c6';
    }
    if(seria_name == 'EMA'){
        return '#91cc75';
    }
    if(seria_name == 'WMA'){
        return '#fac858';
    }
    if(seria_name == 'DEMA'){
        return '#ee6666';
    }
    if(seria_name == 'TEMA'){
        return '#73c0de';
    }
    if(seria_name == 'WILLIAMS'){
        return '#3ba272';
    }
    if(seria_name == 'RSI'){
        return '#fc8452';
    }
    if(seria_name == 'ADX'){
        return '#9a60b4';
    }
    if(seria_name == 'Standart Deviation'){
        return '#ea7ccc';
    }
}

//*******************************************************************************


//***** TODAY *****//

function echart_today_emotion() {
    var $snpChart = document.querySelector('.echart-today-snp');
    var $emotionChart = document.querySelector('.echart-today-emotion');
    var emotion_settings = parseInt($('#user-emotion').val());
    if($snpChart){
        var url_emotion = '/algotradersettings/get_all_emotions'
        var url_snp = '/algotradersettings/get_complete_graph_for_ticker/^GSPC';

//        if(is_settings_modal){
//            var loading = $(".emotion-loading")
//            var spinner = $('<div class="spinner-border text-info" role="status"><span class="sr-only">Loading...</span></div>');
//            loading.empty();
//            $(".emotion-filter").empty();
//            $(".emotion-fixed-filter-text").empty();
//            loading.append(spinner);
//        }

        Promise.all([
          $.ajax({ url: url_emotion }),
          $.ajax({ url: url_snp })
        ])
        .then(([emotion, snp]) => {

            //***** EMOTIONS DATA *****//
            emotion = emotion.historical;
            TODAY_EMOTION = emotion.historical;
//            var pos_emotion_arr=[];
//            var date_index = new Date();
//            var index = 0;
//            for (e of emotion)
//            {
//                var date_e = new Date(e.score_time);
//                var parsed_e = Date.parse(date_e.toDateString());
//                main_emotion.push( [parsed_e , e.fgi_value]);
//                if(is_settings_modal){
//                    main_reports_emotion.push( [parsed_e , e.fgi_value]);
//                }
//            }

            var emotion_dic = get_days_for_snp_backtesting(emotion_settings, TODAY_EMOTION, true);

            //***** DRAW EMOTION CHART *****//
            if(!is_settings_modal){
                var emotion_chart = draw_graph('container_emotion', 'Market Emotion', emotion_dic.series, 4, true, false);
            }

            //***** SNP DATA *****//
            snp=snp.historical
            for (d of snp)
            {
                var date_d = new Date(d.Date);
                var parsed_d = Date.parse(date_d.toDateString());
                main_snp.push([parsed_d , d.Close]);
            }
            if(is_settings_modal){
                $.each(reports, function(k,d)
                {
                    var date_d = new Date(d.report_time);
                    var parsed_d = Date.parse(date_d.toDateString());
                    main_reports.push([parsed_d , d.net_liquidation]);
                })
            }


            var snp_chart = draw_snp_chart(main_snp, emotion_dic.days_arr, [emotion_dic.series[0]], is_settings_modal,'container_sp500');
            if(is_settings_modal){
    //            var report_chart = draw_snp_chart(main_reports, emotion_dic.days_arr, [emotion_dic.series[0]], is_settings_modal,'reports_emotion');
                var dic = get_snp_series_by_emotion(main_reports, emotion_dic.days_arr, [emotion_dic.series[0]]);
                var series = []
                var main = {
                    name: "Reports",
                    data: main_reports,
                    id: 'dataseries_report',
    //                enableMouseTracking: false
                };
                series.push(main);
                series = $.merge(series, dic.series);
                var new_arr = $.merge(series, [emotion_dic.series[0]]);
                var snp_chart = draw_graph('reports_emotion', 'Reports', new_arr, 4, true, true);
                var hidden_series = snp_chart.series[new_arr.length - 1];
                hidden_series.hide();
            }
        });
    }
};

function get_days_for_snp_backtesting(emotion_settings, main_emotion, is_with_emotion_series){
    var days_arr=[];
    var pos_emotion_arr=[];
    var pos_emotion_arr_negative = []

    var date_index = new Date();
    var index = 0;

    var date_index_negative = new Date();
    var index_negative = 0;
    for (e of main_emotion)
    {
        var date = new Date(e[0]);
        if(e[1] >= emotion_settings){
            days_arr.push(e[0]);

            if(is_with_emotion_series){
                date.setDate(date.getDate() - 1);
                if(date.toDateString() == date_index.toDateString() && index > 0){
                    var pos_emotion = $(pos_emotion_arr).get(-1);
                    date.setDate(date.getDate() + 1);
                    pos_emotion.push(e);
                }
                else
                {
                    date.setDate(date.getDate() + 1);
                    var new_pos_emotion = [];
                    new_pos_emotion.push(e);
                    pos_emotion_arr.push(new_pos_emotion);
                }
                date_index = date;
                index += 1;
            }
        }
        else if(is_with_emotion_series){
            date.setDate(date.getDate() - 1);
            if(date.toDateString() == date_index_negative.toDateString() && index_negative > 0){
                var pos_emotion = $(pos_emotion_arr_negative).get(-1);
                date.setDate(date.getDate() + 1);
                pos_emotion.push(e);
            }
            else
            {
                date.setDate(date.getDate() + 1);
                var new_pos_emotion = [];
                new_pos_emotion.push(e);
                pos_emotion_arr_negative.push(new_pos_emotion);
            }
            date_index_negative = date;
            index_negative += 1;
        }
    }

    var series = []
    var main = {
        name: 'Emotion',
        data: main_emotion,
        id: 'dataseries',
    };
    series.push(main);
    if(is_with_emotion_series)
    {
        var i =0;
        for (arr of pos_emotion_arr_negative){
            var range = {
                name: 'EmotionColor',
                data: arr,
                color: '#FF0000',
                id: 'dataseries_neg' + i,
            };
            series.push(range);
            i += 1;
        }
        i =0;
        for (arr of pos_emotion_arr){
            var range = {
                name: 'Emotion',
                data: arr,
                color: '#00c36f',
                id: 'dataseries' + i,
            };
            series.push(range);
            i += 1;
        }
    }

    return {days_arr: days_arr, series: series};
}


