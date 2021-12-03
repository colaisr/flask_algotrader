avg_pe = 0;
TOOLTIPS = jQuery.parseJSON(TOOLTIPS)

$(document).ready(function () {
//    get_avg_pe_from_fmp($('.ticker-sector-val').data('sector'));
    get_fmp_ticker_data(ticker);
//    get_stock_news(10);
//    get_insider_actions();
//    get_press_relises();
//    get_fundamentals_summary();
//    get_fundamentals_feed();
//    get_company_info();
//    fill_container_ticker_info(ticker); //from spider_project.js

    setInterval(function(){
       get_fmp_ticker_data(ticker);
    }, 15000);


})