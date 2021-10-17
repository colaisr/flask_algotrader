$(document).ready(function () {

    ticker=$( "#ticker" )[0].value;

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

