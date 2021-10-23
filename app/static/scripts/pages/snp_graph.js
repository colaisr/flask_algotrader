
function draw_graph(container_name, title, series, range_selector, with_tooltip_formatter, if_by_last_el){
    var tooltip = {
            useHTML: true,
            valueDecimals: 2,
            formatter: function() {
                var x = this.x;
                var date = new Date(x);
                var all_series = this.points[0].series.chart.series;
                var i = if_by_last_el ? -2 : 0; // -2: last element - navigation
                var series = $(all_series).get(i);
                var x_arr = series.processedXData;
                var index_in_arr = x_arr.indexOf(x);
                var data = series.processedYData[index_in_arr];
                if(isFloat(data)){
                    data = data.toFixed(2);
                }
                var html = '<table><tr><th colspan="2">'+date.toDateString()+'</th></tr><tr><td style="color: #00c36f">'+series.name+': </td>' +
                           '<td style="text-align: right"><b>'+data+'</b></td></tr></table>';

                return html;
            }
        };
    if(!with_tooltip_formatter){
        tooltip = {
            valueDecimals: 2
        };
    }

    var chart = Highcharts.stockChart(container_name, {
//        xAxis: xAxis,
        rangeSelector: {
            selected: range_selector
        },
        title: {
            text: title
        },
        tooltip: tooltip,
        series: series
    });
    return chart;
}

function get_range_selector_index(e, range_selector){
    var btn_index = range_selector;
    if(typeof(e.rangeSelectorButton)!== 'undefined') {
        var c = e.rangeSelectorButton.count;
        var t = e.rangeSelectorButton.type;
        if(c == 1 && t == "month"){
          btn_index = 0;
        } else if(c == 3 && t == "month"){
          btn_index = 1;
        } else if(c == 6 && t == "month"){
          btn_index = 2;
        } else if(t == "ytd"){
          btn_index = 3;
        } else if(c == 1 && t == "year"){
          btn_index = 4;
        } else if(t == "all"){
          btn_index = 5;
        }
    }
    return btn_index;
}


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
            days_arr.push(date.toDateString());

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

function draw_snp_chart(main_snp, days_arr, emotion_series, is_settings_modal){
    var dic = get_snp_series_by_emotion(main_snp, days_arr, emotion_series);
    var series = []
    var main = {
        name: "S&P 500",
        data: main_snp,
        id: 'dataseries',
        enableMouseTracking: false
    };
    series.push(main);
    series = $.merge(series, dic.series);
    var new_arr = $.merge(series, emotion_series);
    var snp_chart = draw_graph('container_sp500', 'S&P 500', new_arr, 4, true, true);
    var hidden_series = snp_chart.series[new_arr.length - 1];
    hidden_series.hide();

    if(is_settings_modal){
        $(".emotion-loading").empty();
        $(".emotion-fixed-filter-text").empty();
        $(".emotion-filter").empty();
        $(".emotion-filter").text(dic.days_num);
        $(".emotion-fixed-filter-text").text("days in last year");
    }
    return snp_chart;
}

function get_snp_series_by_emotion(main_snp, days_arr){
    var ticker='S&P 500';
    var pos_snp_arr=[];

    var date_index = new Date();
    var index = 0;
    for (d of main_snp)
    {
        var date_d = new Date(d[0]);
        if(days_arr.indexOf(date_d.toDateString()) >= 0){
            date_d.setDate(date_d.getDate() - 1);
            if(date_d.toDateString() == date_index.toDateString() && index > 0){
                var pos_snp = $(pos_snp_arr).get(-1);
                date_d.setDate(date_d.getDate() + 1);
                pos_snp.push(d);
            }
            else
            {
                date_d.setDate(date_d.getDate() + 1);
                var new_pos_snp = [];
                new_pos_snp.push(d);
                pos_snp_arr.push(new_pos_snp);
            }
            date_index = date_d;
            index += 1;
        }
    }

//        //***** SERIES SNP *****//
    var series = []
    var i =1;
    var days_num = 0;
    for (arr of pos_snp_arr){
        days_num += arr.length;
        var range = {
            name: "Color",
            data: arr,
            color: '#00c36f',
            lineWidth:3,
            id: 'Color' + i,
        };
        series.push(range);
        i += 1;
    }
    return {series: series, days_num: days_num};
}

function fill_emotion_and_snp_graphs(emotion_settings, is_settings_modal, main_snp, main_emotion){
    var url_emotion = '/algotradersettings/get_all_emotions'
    var url_snp = '/algotradersettings/get_complete_graph_for_ticker/^GSPC';

    if(is_settings_modal){
        var loading = $(".emotion-loading")
        var spinner = $('<div class="spinner-border text-info" role="status"><span class="sr-only">Loading...</span></div>');
        loading.empty();
        $(".emotion-filter").empty();
        $(".emotion-fixed-filter-text").empty();
        loading.append(spinner);
    }

    Promise.all([
      $.ajax({ url: url_emotion }),
      $.ajax({ url: url_snp })
    ])
    .then(([emotion, snp]) => {

        //***** EMOTIONS DATA *****//
        emotion = emotion.historical;
        var pos_emotion_arr=[];
        var date_index = new Date();
        var index = 0;
        for (e of emotion)
        {
            var date_e = new Date(e.score_time);
            var parsed_e = Date.parse(date_e.toDateString());
            main_emotion.push( [parsed_e , e.fgi_value]);
        }

        var emotion_dic = get_days_for_snp_backtesting(emotion_settings, main_emotion, true);

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

        var snp_chart = draw_snp_chart(main_snp, emotion_dic.days_arr, [emotion_dic.series[0]], is_settings_modal);
    });
}

function remove_series(chart, seriesname){
    var series = chart.series;
    for (s of series){
        if(s.name == seriesname){
            s.remove();
        }
    }
}

function add_series(chart, series_arr){
    for (s of series_arr){
        chart.addSeries(s);
    }
}


//**** BLACK SWAN ****

function blackswan_modal(bsw_snp_main, snp_drop_arr, min_snp, bsw_global){
    var loading = $(".bsw-loading")
    var spinner = $('<div class="spinner-border text-info" role="status"><span class="sr-only">Loading...</span></div>');
    loading.empty();
    $(".blackswan-events").empty();
    loading.append(spinner);

    var url = '/algotradersettings/get_snp500_data/' + min_snp
    $.getJSON(url, function(data) {
        data = data['historical'];
        bsw_global = $.merge(bsw_global, data);
        var pos_snp_arr=[];
        var snp_arr=[];

        for (d of bsw_global)
        {
            parsed_d=Date.parse(d["Date"]);
            snp_drop_arr.push( [parsed_d , d["dropP"] ]);
            bsw_snp_main.push( [parsed_d , d["Close"] ]);

            if(d["dropP"] < min_snp){
                pos_snp_arr.push([parsed_d , d["dropP"]]);
            }
        }

        var series = []
        var main = {
            name: "S&P 500",
            data: bsw_snp_main,
            id: 'dataseries_snp_main'
//            enableMouseTracking: false
        };
        series.push(main);
        var data_flag = [];
        for (arr of pos_snp_arr){
            var flag = {
                x: arr[0],
                title: ' ',
                text: 'DropP: ' + arr[1].toFixed(2)
            }
            data_flag.push(flag);
        }

        var flags = {
                type: 'flags',
                data: data_flag,
                onSeries: 'dataseries_snp_main',
                shape: 'circlepin',
                color: '#FF0000',
                fillColor: '#FF0000',
                width: 10
            }

        series.push(flags);

        var days_num = pos_snp_arr.length;

        var dropP = {
            name: 'DropP',
            data: snp_drop_arr,
            id: 'dataseries_drop',
        };
        series.push(dropP);

        var snp_chart = draw_graph('blackswan_sp500', 'S&P 500', series, 5, false, true);
        var hidden_series = snp_chart.series[series.length - 1];
        hidden_series.hide();

        $('.blackswan-min').html(min_snp+'%');
        $('.blackswan-events').html(days_num);
        $('.blackswan-filter').html(days_num);
        $('.blackswan-fixed-filter-text').html("events in last 5 Years");
        loading.empty();
    });

}

function change_black_swan(bsw_snp_main, snp_drop_arr, bsw_global, min_snp){
        var loading = $(".bsw-loading")
        var spinner = $('<div class="spinner-border text-info" role="status"><span class="sr-only">Loading...</span></div>');
        loading.empty();
        $(".blackswan-events").empty();
        loading.append(spinner);

        var pos_snp_arr=[];

        for (d of bsw_global)
        {
            parsed_d=Date.parse(d["Date"]);

            if(d["dropP"] < min_snp){
                pos_snp_arr.push([parsed_d , d["dropP"]]);
            }
        }

        var series = []
        var main = {
            name: "S&P 500",
            data: bsw_snp_main,
            id: 'dataseries_snp_main'
//            enableMouseTracking: false
        };
        series.push(main);

        var data_flag = [];
        for (arr of pos_snp_arr){
            var flag = {
                x: arr[0],
                title: ' ',
                text: 'DropP: ' + arr[1].toFixed(2)
            }
            data_flag.push(flag);
        }

        var flags = {
                type: 'flags',
                data: data_flag,
                onSeries: 'dataseries_snp_main',
                shape: 'circlepin',
                color: '#FF0000',
                fillColor: '#FF0000',
                width: 10
            }

        series.push(flags);

        var days_num = pos_snp_arr.length;

        var dropP = {
            name: 'DropP',
            data: snp_drop_arr,
            id: 'dataseries_drop',
        };
        series.push(dropP);

        var snp_chart = draw_graph('blackswan_sp500', 'S&P 500', series, 5, false, true);
        var hidden_series = snp_chart.series[series.length - 1];
        hidden_series.hide();

        $('.blackswan-min').html(min_snp+'%');
        $('.blackswan-events').html(days_num);
        $('.blackswan-filter').html(days_num);
        $('.blackswan-fixed-filter-text').html("events in last 5 Years");
        loading.empty();
}