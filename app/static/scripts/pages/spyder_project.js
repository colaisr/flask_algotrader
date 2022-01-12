var domane = 'https://colak.eu.pythonanywhere.com/';

if(window.location.hostname == '127.0.0.1'){
    domane = 'http://localhost:8000/';
}

function get_data_for_ticker(){
    $('.content-hidden').prop('hidden', true);
    $('#candidate-flash').empty();
    ticker=$('#txt_ticker').val();
    if(ticker == ""){
        $('#candidate-flash').append(flashMessage("danger","Ticker is must!"));
    }
    else{
        $('#candidate-flash').empty();
        loading('add-candidate-body'); //from base.js
        url = domane + 'research/get_info_ticker/' + ticker
        $.getJSON(url, function(data) {
            if (data.length == 0 ||
                data.cik == undefined ||
                data.cik == null ||
                data.cik=="" ||
                data.isEtf ||
                !data.isActivelyTrading) //etfs and funds have no cik //cik - num of company
            {
                $('#candidate-flash').append(flashMessage("danger","Not Actively traded stock"));
            }
            else{
                $('#txt_company_name').val(data.companyName);
                $('#txt_company_description').val(data.description);
                $('#txt_exchange').val(data.exchange);
                $('#txt_industry').val(data.industry);
                $('#txt_sector').val(data.sector);
                $('#txt_logo').val(data.image);
                $('#txt_ticker').val($('#txt_ticker').val().toUpperCase());
                $("#btn_submit").prop('disabled', false);
            }
            stop_loading('add-candidate-body'); //from base.js
            $('.content-hidden').prop('hidden',false);
        })
    }
}

function update_candidate(){
    $('.content-hidden').prop('hidden',true);
    loading('add-candidate-body'); //from base.js
    $('#candidate-flash').empty();
    ticker = $('#txt_ticker').val();
    reason = $('#txt_reason').val();
    email = $('#user-email').val();

    $('.content-hidden').prop('hidden',true);
    url = domane + 'candidates/updatecandidate/';
    $.post(url,{ticker: ticker, reason: reason, email: email}, function(data) {
        var data_parsed = jQuery.parseJSON(data);
        upload_personal_list(); //from base.js
        stop_loading('add-candidate-body'); //from base.js
        $('#candidate-flash').append(flashMessage(data_parsed["color_status"],data_parsed["message"]));
        $('.content-hidden').prop('hidden',false);
        setTimeout(function(){
            $('#candidate-flash').empty();
        }, 2000);
    })
}

function update_market_data(ticker){
    url = domane + 'research/updatemarketdataforcandidate/';
    $.post(url,{ticker_to_update: ticker}, function(data) {
            window.location.reload();
    })
}

function get_fmp_ticker_data(ticker){
    url = domane + 'data_hub/current_stock_price_full/' + ticker
    $.getJSON(url, function(data) {
        data = data[0];
        $('.fmp-change').removeClass('text-success');
        $('.fmp-change').removeClass('text-danger');
        $('.fmp-pe').removeClass('text-success');
        $('.fmp-pe').removeClass('text-warning');
        $('.fmp-price').html(data.price.toFixed(2).toString() + '$');
        $('.fmp-change').html(data.change.toFixed(2).toString() + ' (' + data.changesPercentage.toFixed(2).toString() + '%)');
        if(data.change > 0){
            $('.fmp-change').addClass('text-success');
        }
        else{
            $('.fmp-change').addClass('text-danger');
        }
        $('.fmp-last-close').html(data.previousClose.toFixed(2));
        if(buying_target_price_fm >= data.price.toFixed(2)){
            $('.buying_target_price_fmp').removeClass('btn-success');
            $('.buying_target_price_fmp').removeClass('btn-warning');
            $('.buying_target_price_fmp').addClass('btn-success');
        }
        else{
            $('.buying_target_price_fmp').removeClass('btn-success');
            $('.buying_target_price_fmp').removeClass('btn-warning');
            $('.buying_target_price_fmp').addClass('btn-warning');
        }
        if(data.pe != null){
            $('.fmp-pe').html(data.pe.toFixed(2));
            if(data.pe > avg_pe){
                $('.fmp-pe').addClass('text-success');
            }
            else{
                $('.fmp-pe').addClass('text-warning');
            }
        }
        else{
            $('.fmp-pe').html('-');
        }
        $('.fmp-eps').html(data.eps.toFixed(2));
    })
}

function get_avg_pe_from_fmp(sector){
    url = domane + 'data_hub/average_sector_pe_today/' + sector
    $.getJSON(url, function(data) {
        avg_pe=parseFloat(data.pe); //avg_pe - global from ticker_info
    })
}

function fill_container_ticker_info(ticker){
    url = domane + 'data_hub/historical_daily_price_full/'+ticker
    $.getJSON(url, function(data) {
        data=data['historical']
        var arr = [];
        var score_arr = [];
        for (d of data)
        {
            parsed_d=Date.parse(d.date);
            arr.push( [parsed_d , d.close ]);
        }
        hist_data=jQuery.parseJSON(hist_data)
        for (t of hist_data){
//            if(t[1]>0){
//                parsed_d=Date.parse(t[0]);
//                score_arr.push( [parsed_d , t[1] ]);
//            }
            parsed_d=Date.parse(t[0]);
            score_arr.push( [parsed_d , t[1] ]);
        }

        Highcharts.stockChart('container', {
            chart: {
                zoomType: 'xy'
            },
            rangeSelector: {
                selected: 2
            },
            title: {
                text: ticker+' Stock Price'
            },
            yAxis: [
                { // Primary yAxis
                    gridLineWidth: 1,
                    labels: {
                        format: '{value}$',
                        style: {
                            color: Highcharts.getOptions().colors[0]
                        }
                    },
                    title: {
                        text: 'Close Price',
                        style: {
                            color: Highcharts.getOptions().colors[0]
                        }
                    },
                    opposite: true
                },
                {
                    title: {
                        text: 'Stock Score Score',
                        style: {
                            color: Highcharts.getOptions().colors[3]
                        }
                    },
                    labels: {
                        format: '{value}',
                        style: {
                            color: Highcharts.getOptions().colors[3]
                        }
                    },
                    opposite: true
                }],
            tooltip: {
                valueDecimals: 2,
                shared: true
            },
            legend: {
                layout: 'vertical',
                align: 'left',
                x: 80,
                verticalAlign: 'top',
                y: 55,
                floating: true,
                backgroundColor:
                    Highcharts.defaultOptions.legend.backgroundColor || // theme
                    'rgba(255,255,255,0.25)'
            },
            series: [
                {
                    name: 'Score',
                    yAxis: 1,
                    type: 'spline',
                    data: score_arr,
                    tooltip: {
                        valueSuffix: ''
                    },
                    color: Highcharts.getOptions().colors[3]
                },
                {
                    name: ticker,
                    type: 'spline',
                    data: arr.reverse(),
                    tooltip: {
                        valueSuffix: ' $'
                    },
                    color: Highcharts.getOptions().colors[0]

                }],
            responsive: {
                rules: [
                    {
                        condition: {
                            maxWidth: 500
                        },
                        chartOptions: {
                            legend: {
                                floating: false,
                                layout: 'horizontal',
                                align: 'center',
                                verticalAlign: 'bottom',
                                x: 0,
                                y: 0
                            },
                            yAxis: [{
                                labels: {
                                    align: 'right',
                                    x: 0,
                                    y: -6
                                },
                                showLastLabel: false
                            },
                                {
                                    labels: {
                                        align: 'left',
                                        x: 0,
                                        y: -6
                                    },
                                    showLastLabel: false
                                }]
                        }
                    }]
            }
        });
    })
}

function similar_companies(ticker){
    url = domane + 'data_hub/similar/' + ticker
    $.getJSON(url, function(data) {
        $.each(data[0].peersList, function(i, item)
        {
//            var ticker_item = '<a href="/candidates/info/' + item + '"><div class="card overflow-hidden">'
//                +'<div class="bg-holder bg-card" style="background-image:url(/static/falcon/assets/img/icons/spot-illustrations/corner-5.png);"></div>'
//                +'<div class="card-body position-relative">'
//                +'<div class="display-4 fs-1 mb-2 fw-normal font-sans-serif text-primary" >' + item + '</div></div></div></a>';
//
            var ticker_item = '<a href="/candidates/info/' + item + '" class="ms-2"><label class="btn btn-sm btn-info">' + item + '</label></a>';

            $('.similar-companies').append(ticker_item);
        })
    })
}




