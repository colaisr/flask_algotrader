$(document).ready(function () {

//    ticker=$("#ticker")[0].value;

    $('.add-candidate').on('click', function(){
        add_candidate_from_ticker_info(ticker, user_email) //from spyder_project.js
    })

    fill_container_ticker_info(ticker);

    var ctx = document.getElementById('myChart').getContext('2d');
    //const labels = hist_dates;
    const data = {
        labels: hist_dates,
        datasets: [{
        label: 'Algotrader Analytics',
        data: hist_algo_ranks,
        fill: false,
        borderColor: 'rgb(75, 192, 192)',
        tension: 0.1
        }]
    };
    const config = {
        type: 'line',
        data,
        options: {}
    };

    var myChart = new Chart(
        document.getElementById('myChart'),
        config
    );

})

function fill_container_ticker_info(ticker){

    url = '/algotradersettings/get_complete_graph_for_ticker/'+ticker
    $.getJSON(url, function(data) {
        data=data['historical']
        var arr = [];
        for (d of data)
        {
            parsed_d=Date.parse(d["Date"]);
            arr.push( [parsed_d , d["Close"] ]);
        }
        var series = [
            {
                name: ticker,
                data: arr,
                id: 'dataseries',
                tooltip: {
                    valueDecimals: 2
                }
            }
        ];
        var chart = draw_graph('container', ticker+' Stock Price', series, 4, true, false);
    });
}

