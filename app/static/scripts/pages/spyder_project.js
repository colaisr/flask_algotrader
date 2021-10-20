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
            var date_e = new Date(e.score_time);
            var parsed_e = Date.parse(date_e.toDateString());
            main_emotion.push( [parsed_e , e.fgi_value]);
        }
        var emotion_dic = get_days_for_snp_backtesting(emotion_settings, main_emotion, true);

        //***** DRAW EMOTION CHART *****//
        if(is_draw_emotion_graph){
            var emotion_chart = draw_graph('container_emotion', 'Market Emotion', emotion_dic.series, false);
        }

        //***** SNP DATA *****//
        snp=snp.historical
        for (d of snp)
        {
            var date_d = new Date(d.Date);
            var parsed_d = Date.parse(date_d.toDateString());
            main_snp.push([parsed_d , d.Close]);
        }
        var dic = get_snp_series_by_emotion(main_snp, emotion_dic.days_arr);

        var new_arr = $.merge(dic.series, [emotion_dic.series[0]])
        var snp_chart = draw_graph('container_sp500', 'S&P 500', new_arr, true);
        var hidden_series = snp_chart.series[new_arr.length - 1];
        hidden_series.hide();

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
        var series = [
            {
                name: ticker,
                data: arr,
                id: 'dataseries',
                tooltip: {
                    valueDecimals: 2
                }
            }
        ];
        var chart = draw_graph('container', ticker+' Stock Price', series, false);
    });
}
