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

//function get_days_for_snp_backtesting(emotion_settings, main_emotion){
//
//}

function fill_emotion_data(emotion_settings, is_draw_emotion_graph, main_snp, main_emotion){
    var ticker='SP500';
    var url_emotion = domane + 'research/get_all_emotions'
    var url_snp = domane + 'research/get_complete_graph_for_ticker/^GSPC';

    Promise.all([
      $.ajax({ url: url_emotion }),
      $.ajax({ url: url_snp })
    ])
    .then(([emotion, snp]) => {
        var days_arr=[];
        var dateOffset = (24*60*60*1000) * 370; //370 days
        var days_back = new Date();
        days_back.setTime(days_back.getTime() - dateOffset);

        //***** EMOTIONS DATA *****//
        emotion = emotion.historical;
//        var main_emotion = [];
        for (e of emotion)
        {
            var parsed_e=Date.parse(e.score_time);
            var date_e = new Date(e.score_time);
            if(parsed_e > days_back){
                main_emotion.push( [parsed_e , e.fgi_value]);
                if(e.fgi_value >= emotion_settings){
                    days_arr.push(date_e.toDateString());
                }
            }
        }

        //***** DRAW EMOTION CHART *****//
        if(is_draw_emotion_graph){
            Highcharts.stockChart('container_emotion', {
                rangeSelector: {
                    selected: 1
                },
                title: {
                    text: 'Market Emotion'
                },
                series: [
                    {
                        name: 'Emotion',
                        data: main_emotion,
                        id: 'dataseries',
                        tooltip: {
                            valueDecimals: 2
                        }
                    },
                ]
            });
        }

        //***** SNP DATA *****//
        snp=snp.historical
//        var main_snp = [];
        var pos_snp_arr=[];

        var date_index = new Date();
        var index = 0;
        for (d of snp)
        {
            var parsed_d = Date.parse(d.Date);
            var date_d = new Date(d.Date);
            if(parsed_d > days_back){
                main_snp.push([parsed_d , d.Close]);
                if(days_arr.indexOf(date_d.toDateString()) >= 0){
                date_d.setDate(date_d.getDate() - 1);
                if(date_d.toDateString() == date_index.toDateString() && index > 0){
                    var pos_snp = $(pos_snp_arr).get(-1);
                    date_d.setDate(date_d.getDate() + 1);
                    pos_snp.push([parsed_d , d.Close]);
                }
                else
                {
                    date_d.setDate(date_d.getDate() + 1);
                    var new_pos_snp = [];
                    new_pos_snp.push([parsed_d , d.Close]);
                    pos_snp_arr.push(new_pos_snp);
                }
                date_index = date_d;
                index += 1;
                }
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
        for (arr of pos_snp_arr){
            var range = {
                name: 'position' + i,
                data: arr,
                color: '#00c36f',
                lineWidth:4,
                id: 'dataseries' + i,
                tooltip: {
                valueDecimals: 2
                }
            };
            series.push(range);
            i += 1;
        }


        //***** DRAW SNP CHART *****//
        Highcharts.stockChart('container_sp500', {
            rangeSelector: {
                selected: 1
            },
            title: {
                text: ticker+' Stock Price'
            },
            series: series
        });

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
