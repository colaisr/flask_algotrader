var domane = 'https://colak.eu.pythonanywhere.com/';
//var domane = 'http://localhost:8000/';

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
            if (data.longName == undefined)
            {
                $('#candidate-flash').append(flashMessage("danger","Wrong ticker"));
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





