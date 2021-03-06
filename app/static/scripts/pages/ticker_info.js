
ticker=$( "#ticker" )[0].value;
//hist_dates=$( "#hist_dates" )[0].value;
//hist_tr_ranks=$( "#hist_tr_ranks" )[0].value;
//hist_fmp_score=$( "#hist_fmp_score" )[0].value;

url='https://financialmodelingprep.com/api/v3/historical-price-full/'+ticker+'?serietype=line&apikey=f6003a61d13c32709e458a1e6c7df0b0'
$.getJSON(url, function(data) {
  data=data['historical']
  var arr = [];
  for (d of data)
   {
    parsed_d=Date.parse(d["date"]);
    arr.push( [parsed_d , d["close"] ]);
    }
  rev_main=arr.reverse()
  Highcharts.stockChart('container', {


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


var ctx = document.getElementById('myChart').getContext('2d');
const labels = hist_dates;
const data = {
  labels: labels,
  datasets: [{
    label: 'Tipranks Rating',
    data: hist_tr_ranks,
    fill: false,
    borderColor: 'rgb(75, 192, 192)',
    tension: 0.1
  },
  {
    label: 'FMP Score',
    data: hist_fmp_score,
    fill: false,
    borderColor: 'rgb(255, 99, 132)',
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