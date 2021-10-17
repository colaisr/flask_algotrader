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

function fill_emotion_data(){

    ticker='SP500';

    url_snp = domane + 'research/get_complete_graph_for_ticker/^GSPC'
    $.getJSON(url_snp, function(data) {
        data=data['historical']
        var arr = [];
        var dateOffset = (24*60*60*1000) * 280; //280 days
        var days_back = new Date();
        days_back.setTime(days_back.getTime() - dateOffset);
        for (d of data)
        {
            parsed_d=Date.parse(d["Date"]);
            if(parsed_d>days_back){
               arr.push( [parsed_d , d["Close"] ]);
            }
        }
        rev_main=arr

        Highcharts.stockChart('container_sp500', {
            rangeSelector: {
                selected: 1
            },
            title: {
                text: ticker+' Stock Price'
            },
            rangeSelector: {
                enabled: false
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

    url_emotion = domane + 'research/get_all_emotions'
    $.getJSON(url_emotion, function(data) {
        data=data['historical']
        var e_arr = [];
        var dateOffset = (24*60*60*1000) * 280; //280 days
        var days_back = new Date();
        days_back.setTime(days_back.getTime() - dateOffset);
        for (d of data)
        {
            parsed_d=Date.parse(d["score_time"]);
            if(parsed_d>days_back){
            e_arr.push( [parsed_d , d["fgi_value"] ]);
            }
        }
        main_emotion=e_arr
        Highcharts.stockChart('container_emotion', {
            rangeSelector: {
                selected: 1
            },
            title: {
                text: 'Market Emotion'
            },
            rangeSelector: {
                enabled: false
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
