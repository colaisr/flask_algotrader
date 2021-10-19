var domane = 'https://colak.eu.pythonanywhere.com/';
//var domane = 'http://localhost:8000/';

function get_data_for_ticker(){
    ticker=$('#txt_ticker').val();
    url = domane + 'research/get_info_ticker/' + ticker
    $.getJSON(url, function(data) {
        //var data_parsed = jQuery.parseJSON(data);
        if (data == 'undefined')
        {
            alert('Wrong ticker');
        }
        else{
            $('#txt_company_name').val(data.longName);
            $('#txt_company_description').val(data.longBusinessSummary);
            $('#txt_exchange').val(data.exchange);
            $('#txt_industry').val(data.industry);
            $('#txt_sector').val(data.sector);
            $('#txt_logo').val(data.logo_url);
            $('#txt_ticker').val($('#txt_ticker').val().toUpperCase());

            $("#btn_submit").prop('disabled', false);
        }
    })
}

function update_candidate(){
    ticker = $('#txt_ticker').val();
    reason = $('#txt_reason').val();
    email = $('#user-email').val();

    url = domane + 'candidates/updatecandidate/';
    $.post(url,{ticker: ticker, reason: reason, email: email}, function(data) {
        window.location.reload();
    })
}

function update_market_data(ticker){
    url = domane + 'research/updatemarketdataforcandidate/';
    $.post(url,{ticker_to_update: ticker}, function(data) {
            window.location.reload();
    })
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
        tooltip: {
            valueDecimals: 2
        }
    };
    series.push(main);
    if(is_with_emotion_series)
    {
        var i =0;
        for (arr of pos_emotion_arr_negative){
            var range = {
                name: 'position_neg' + i,
                data: arr,
                color: '#FF0000',
//                lineWidth:4,
                id: 'dataseries_neg' + i,
                tooltip: {
                valueDecimals: 2
                }
            };
            series.push(range);
            i += 1;
        }
        i =0;
        for (arr of pos_emotion_arr){
            var range = {
                name: 'position' + i,
                data: arr,
                color: '#00c36f',
//                lineWidth:4,
                id: 'dataseries' + i,
                tooltip: {
                valueDecimals: 2
                }
            };
            series.push(range);
            i += 1;
        }
    }

    return {days_arr: days_arr, series: series};
}

function get_snp_series_by_emotion(main_snp, days_arr){
    var ticker='SP500';
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
//        var filtered_arr = pos_snp_arr.filter(x => x.length > 1);
    var series = []
    var main = {
        name: ticker,
        data: main_snp,
        id: 'dataseries',
        tooltip: {
            valueDecimals: 2
        }
    };
    series.push(main);
    var i =1;
    var days_num = 0;
    for (arr of pos_snp_arr){
        days_num += arr.length;
        var range = {
            name: 'position' + i,
            data: arr,
            color: '#00c36f',
            lineWidth:3,
            id: 'dataseries' + i,
            tooltip: {
            valueDecimals: 2
            }
        };
        series.push(range);
        i += 1;
    }

    return {series: series, days_num: days_num};
}

function draw_snp_graph(series){
    var chart = Highcharts.stockChart('container_sp500', {
        rangeSelector: {
            selected: 4
        },
        title: {
            text: 'S&P 500'
        },
        series: series
    });
    return chart;
}

function draw_emotion_graph(series){
    var chart = Highcharts.stockChart('container_emotion', {
                rangeSelector: {
                    selected: 4
                },
                title: {
                    text: 'Market Emotion'
                },
                series: series
            });
    return chart;
}

function fill_emotion_and_snp_graphs(emotion_settings, is_draw_emotion_graph, main_snp, main_emotion){
    var url_emotion = domane + 'research/get_all_emotions'
    var url_snp = domane + 'research/get_complete_graph_for_ticker/^GSPC';

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
            var parsed_e=Date.parse(e.score_time);
            var date_e = new Date(e.score_time);
            main_emotion.push( [parsed_e , e.fgi_value]);
        }
        var emotion_dic = get_days_for_snp_backtesting(emotion_settings, main_emotion, true);

        //***** DRAW EMOTION CHART *****//
        if(is_draw_emotion_graph){
            var emotion_chart = draw_emotion_graph(emotion_dic.series);
        }

        //***** SNP DATA *****//
        snp=snp.historical
        for (d of snp)
        {
            var parsed_d = Date.parse(d.Date);
            main_snp.push([parsed_d , d.Close]);
        }
        var dic = get_snp_series_by_emotion(main_snp, emotion_dic.days_arr);
        var snp_chart = draw_snp_graph(dic.series);

        //**************************************************************
        // is_draw_emotion_graph is FALSE then func called from settings
        // then to set num of emotions days to link row
        //**************************************************************
        if(!is_draw_emotion_graph){
            $(".emotion-fixed-filter-text").empty();
            $(".emotion-filter").empty();
            $(".emotion-filter").text(dic.days_num);
            $(".emotion-fixed-filter-text").text("days in last year");
        }
    });
}

function fill_container_ticker_info(ticker){

    url = domane + 'research/get_complete_graph_for_ticker/'+ticker
    $.getJSON(url, function(data) {
        data=data['historical']
        var arr = [];
        for (d of data)
        {
            parsed_d=Date.parse(d["Date"]);
            arr.push( [parsed_d , d["Close"] ]);
        }
        rev_main=arr
        Highcharts.stockChart('container', {
            rangeSelector: {
                selected: 1
            },
            title: {
                text: ticker+' Stock Price'
            },
            series: [
                {
                    name: ticker,
                    data: rev_main,
                    id: 'dataseries',
                    tooltip: {
                        valueDecimals: 2
                    }
                },
            ]
        });
    });
}
