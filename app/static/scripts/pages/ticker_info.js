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

//    var ctx = document.getElementById('myChart').getContext('2d');
//    //const labels = hist_dates;
//    const data = {
//        labels: hist_dates,
//        datasets: [{
//        label: 'Algotrader Analytics',
//        data: hist_algo_ranks,
//        fill: false,
//        borderColor: 'rgb(75, 192, 192)',
//        tension: 0.1
//        }]
//    };
//    const config = {
//        type: 'line',
//        data,
//        options: {}
//    };
//
//    var myChart = new Chart(
//        document.getElementById('myChart'),
//        config
//    );

})

//function fill_container_ticker_info(ticker){
//
//    url = '/algotradersettings/get_complete_graph_for_ticker/'+ticker
//    $.getJSON(url, function(data) {
//        data=data['historical']
//        var arr = [];
//        var score_arr = [];
//        for (d of data)
//        {
////            parsed_d=Date.parse(d["Date"]);
//            date = new Date(d["Date"])
//            month = date.getMonth()+1
//            month = month.length > 1 ? month : '0'+month;
//            day = date.getDate().length > 1 ? date.getDate() : '0'+date.getDate();
//            parsed_d_str=date.getFullYear()+'-'+month+'-'+day;
//            parsed_d=Date.parse(parsed_d_str);
//            arr.push( [parsed_d , d["Close"] ]);
//        }
//        hist_data=jQuery.parseJSON(hist_data)
//        for (t of hist_data){
//            parsed_d=Date.parse(t[0]);
//            score_arr.push( [parsed_d , t[1] ]);
//        }
////        series.push(jQuery.parseJSON(test));
////        var chart = draw_graph('container', ticker+' Stock Price', series, 4, true, false);
//        Highcharts.stockChart('container', {
//            chart: {
//                zoomType: 'xy'
//            },
//            rangeSelector: {
//                selected: 2
//            },
//            title: {
//                text: ticker+' Stock Price'
//            },
//            yAxis: [
//                { // Primary yAxis
//                    gridLineWidth: 1,
//                    labels: {
//                        format: '{value}$',
//                        style: {
//                            color: Highcharts.getOptions().colors[0]
//                        }
//                    },
//                    title: {
//                        text: 'Close Price',
//                        style: {
//                            color: Highcharts.getOptions().colors[0]
//                        }
//                    },
//                    opposite: true
//                },
//                {
//                    title: {
//                        text: 'Algotrader Score',
//                        style: {
//                            color: Highcharts.getOptions().colors[3]
//                        }
//                    },
//                    labels: {
//                        format: '{value}',
//                        style: {
//                            color: Highcharts.getOptions().colors[3]
//                        }
//                    },
//                    opposite: true
//                }],
//            tooltip: {
//                valueDecimals: 2,
//                shared: true
//            },
//            legend: {
//                layout: 'vertical',
//                align: 'left',
//                x: 80,
//                verticalAlign: 'top',
//                y: 55,
//                floating: true,
//                backgroundColor:
//                    Highcharts.defaultOptions.legend.backgroundColor || // theme
//                    'rgba(255,255,255,0.25)'
//            },
//            series: [
//                {
//                    name: 'Score',
//                    yAxis: 1,
//                    type: 'spline',
//                    data: second_arr,
//                    tooltip: {
//                        valueSuffix: ''
//                    },
//                    color: Highcharts.getOptions().colors[3]
//                },
//                {
//                    name: ticker,
//                    type: 'spline',
//                    data: arr,
//                    tooltip: {
//                        valueSuffix: ' $'
//                    },
//                    color: Highcharts.getOptions().colors[0]
//
//                }],
//            responsive: {
//                rules: [
//                    {
//                        condition: {
//                            maxWidth: 500
//                        },
//                        chartOptions: {
//                            legend: {
//                                floating: false,
//                                layout: 'horizontal',
//                                align: 'center',
//                                verticalAlign: 'bottom',
//                                x: 0,
//                                y: 0
//                            },
//                            yAxis: [{
//                                labels: {
//                                    align: 'right',
//                                    x: 0,
//                                    y: -6
//                                },
//                                showLastLabel: false
//                            },
//                                {
//                                    labels: {
//                                        align: 'left',
//                                        x: 0,
//                                        y: -6
//                                    },
//                                    showLastLabel: false
//                                }]
//                        }
//                    }]
//            }
//        });
//    })
//
//}


