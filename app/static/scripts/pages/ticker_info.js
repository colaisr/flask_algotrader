
ticker=$( "#ticker" )[0].value;

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

