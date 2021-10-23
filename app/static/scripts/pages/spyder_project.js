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





