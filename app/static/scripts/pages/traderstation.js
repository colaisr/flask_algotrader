$(document).ready(function(){
    //paint_pnl()
    setTimeout(function(){
       window.location.reload(1);
    }, 30000);

    $('#user_emotion_box').click(function(){
    show_modal_emotion()
    });
})

function fill_graph(){
$("#sectors_modal").modal("show");
var ctx = document.getElementById('sectorsChart').getContext('2d');
var myChart = new Chart(ctx, {
    type: 'pie',
    data: {
        labels: graph_sectors,
        datasets: [{
            label: '# of Votes',
            data: graph_sectors_values,
            backgroundColor: [
                'rgba(255, 99, 132, 0.2)',
                'rgba(54, 162, 235, 0.2)',
                'rgba(255, 206, 86, 0.2)',
                'rgba(75, 192, 192, 0.2)',
                'rgba(153, 102, 255, 0.2)'

            ]
        }]
    },
});

}

function show_modal_emotion(){
$(".emotion-modal").modal("show");
fill_emotion_data();
}
function go_to_cnn(){
window.open("https://money.cnn.com/data/fear-and-greed/", "_blank");
}
function fill_emotion_data(){

ticker='SP500';

//url='https://financialmodelingprep.com/api/v3/historical-price-full/'+ticker+'?serietype=line&apikey=f6003a61d13c32709e458a1e6c7df0b0'
url_snp='https://colak.eu.pythonanywhere.com/research/get_complete_graph_for_ticker/'+'^GSPC'
$.getJSON(url_snp, function(data) {
    data=data['historical']
    var arr = [];
    for (d of data)
    {
        parsed_d=Date.parse(d["Date"]);
        arr.push( [parsed_d , d["Close"] ]);
    }
    rev_main=arr
    Highcharts.stockChart('container_sp500', {
        rangeSelector: {
            selected: 1
        },
        title: {
            text: ticker+' Stock Price'
        },
        series: [
            {
                name: ticker,
                data: rev_main,
                id: 'dataseries',
                tooltip: {
                    valueDecimals: 2
                }
            },
        ]
    });
});

url_emotion='https://colak.eu.pythonanywhere.com/research/get_all_emotions'
$.getJSON(url_emotion, function(data) {
    data=data['historical']
    var e_arr = [];
    for (d of data)
    {
        parsed_d=Date.parse(d["score_time"]);
        arr.push( [parsed_d , d["fgi_value"] ]);
    }
    main_emotion=e_arr
    Highcharts.stockChart('container_emotion', {
        rangeSelector: {
            selected: 1
        },
        title: {
            text: 'Market Emotion'
        },
        series: [
            {
                name: Emotion,
                data: main_emotion,
                id: 'dataseries',
                tooltip: {
                    valueDecimals: 2
                }
            },
        ]
    });
});


}