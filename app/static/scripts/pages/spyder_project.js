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

function fill_emotion_and_snp_graphs(emotion_settings, is_settings_modal, main_snp, main_emotion){
    var url_emotion = domane + 'research/get_all_emotions'
    var url_snp = domane + 'research/get_complete_graph_for_ticker/^GSPC';

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
        var chart = draw_graph('container', ticker+' Stock Price', series, 4, true, false);
    });
}

function fill_container_closed_position_info(){

    url = domane + 'research/get_complete_graph_for_ticker/'+ticker
    $.getJSON(url, function(data) {
        data=data['historical']
        var arr = [];
        var pos_arr=[];
        for (d of data)
        {
            parsed_d=Date.parse(d["Date"]);
            arr.push( [parsed_d , d["Close"] ]);
            if(parsed_d<point_end && parsed_d>point_start){
                pos_arr.push([parsed_d , d["Close"]]);
            }
        }
        var series = [
            {
                name: ticker,
                data: arr,
                id: 'dataseries'
            },
            {
                name: 'position',
                data: pos_arr,
                color: '#FF0000',
//                lineWidth:3,
                id: 'dataseries2'
            },
            {
                type: 'flags',
                data: [{
                        x: Date.parse(stp),
                        title: ' ',
                        text: 'Algotrader rank: ' + buying_algotrader_rank + ' Emotion: ' + emotion_on_buy
                    },
                    {
                        x: Date.parse(enp),
                        title: ' ',
                        text: 'Position closed'
                    }],
                onSeries: 'dataseries',
                shape: 'circlepin',
                width: 16
            }
        ];
        var chart = draw_graph('container_position_on_graph', ticker+' Stock Price', series, 1, false, false);
    });
}
