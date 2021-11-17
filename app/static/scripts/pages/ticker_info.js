avg_pe = 0;

$(document).ready(function () {

    get_avg_pe_from_fmp($('.ticker-sector-val').data('sector'));

    $('.add-candidate').on('click', function(){
        add_candidate_from_ticker_info() //from spyder_project.js
    })

    $('.candidate-in-list').on('click', function(){
        remove_candidate();
    })

    get_fmp_ticker_data(ticker);

    setInterval(function(){
       get_fmp_ticker_data(ticker);
    }, 15000);

    fill_container_ticker_info(ticker); //from spider_project.js

})

function remove_candidate(){
    loading('ticker-action', 0); //from base.js
    $('.flashes').empty();
    $.post("/candidates/removecandidate_ajax",{ticker: ticker}, function(data) {
        var data_parsed = jQuery.parseJSON(data);
        $('.flashes').append(flashMessage("success","Ticker removed from your list"));
        var button = $('<button type="button" class="btn btn-outline-info add-candidate">Add</button>');
        $('.ticker-action .ticket-info-val').empty();
        $('.ticker-action .ticket-info-val').append(button);
        $('.add-candidate').on('click',add_candidate_from_ticker_info);
        stop_loading('ticker-action'); //from base.js
        setTimeout(function(){
            $('.flashes').empty();
        }, 2000);
    })
}



