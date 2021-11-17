avg_pe = 0;

$(document).ready(function () {

    get_avg_pe_from_fmp($('.ticker-sector-val').data('sector'));

    $('.add-candidate').on('click', function(){
        add_candidate_from_ticker_info(ticker, user_email) //from spyder_project.js
    })

    get_fmp_ticker_data(ticker);

    setInterval(function(){
       get_fmp_ticker_data(ticker);
    }, 15000);

    fill_container_ticker_info(ticker); //from spider_project.js

})



