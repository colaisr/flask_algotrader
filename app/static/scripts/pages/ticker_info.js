avg_pe = 0;

$(document).ready(function () {

    get_avg_pe_from_fmp($('.ticker-sector-val').data('sector'));
    get_fmp_ticker_data(ticker);
    get_stock_news(10);
    get_insider_actions();
    get_press_relises();
    fill_container_ticker_info(ticker); //from spider_project.js

    setInterval(function(){
       get_fmp_ticker_data(ticker);
    }, 15000);


    $('.add-candidate').on('click', function(){
        add_candidate_from_ticker_info() //from spyder_project.js
    })

    $('.candidate-in-list').on('click', function(){
        remove_candidate();
    })

    $('.news-btn').on('change',function(){
        var limit = $(this).data('limit');
        get_stock_news(limit);
    })

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

function get_stock_news(limit){
    loading('tab-news-card');
    $('.tab-news-card .div-loading').css('height', 0);
    $('.tab-news-card .spinner-border').css('margin-right', '9%');

    $.getJSON("/api/stock_news",{tickers: ticker, limit: limit}, function(data) {
        $('.tab-news-card .div-content').empty();
        $('.tab-news-card .div-content').append($(data.data));
        stop_loading('tab-news-card'); //from base.js
    })
}

function get_insider_actions(){
    loading('tab-insiders-card');
    $('.tab-insiders-card .div-loading').css('height', 0);
    $('.tab-insiders-card .spinner-border').css('margin-right', '9%');

    $.getJSON("/api/insider_actions",{ticker: ticker}, function(data) {
        $('.tab-insiders-card .div-content').empty();
        $('.tab-insiders-card .div-content').append($(data.data));
        stop_loading('tab-insiders-card'); //from base.js
    })
}

function get_press_relises(){
    loading('tab-press-relises-card');
    $('.tab-press-relises-card .div-loading').css('height', 0);
    $('.tab-press-relises-card .spinner-border').css('margin-right', '9%');

    $.getJSON("/api/press_relises",{ticker: ticker}, function(data) {
        $('.tab-press-relises-card .div-content').empty();
        $('.tab-press-relises-card .div-content').append($(data.data));
        stop_loading('tab-press-relises-card'); //from base.js
    })
}



