var domane = 'https://colak.eu.pythonanywhere.com/';

if(window.location.hostname == '127.0.0.1'){
    domane = 'http://localhost:8000/';
}

var TICKER_INFO_DATA = [];
var TICKER_INFO_HIST_DATA = [];
var TODAY_SNP = []
var TODAY_EMOTION = []

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
        var $stockChart = document.querySelector('.echart-icker-info');
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
//                        restore: { show: true },
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


