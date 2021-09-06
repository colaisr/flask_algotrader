
ticker=$( "#ticker" )[0].value;
profit=$( "#profit" )[0].value;
enp=$("#closed")[0].value;
stp=$( "#opened" )[0].value;
fmp_rating_on_buy=$( "#fmp_rating_on_buy" )[0].value;
tip_rank_on_buy=$( "#tip_rank_on_buy" )[0].value;
point_start=Date.parse(stp)
point_end=Date.parse(enp)
//rank_array.forEach(element => element[0]=element[0].replace(/^"(.*)"$/, '$1'));

if(profit>0){
    position_colour='#00c36f'
}
else{
    position_colour='#FF0000'
}

url='https://financialmodelingprep.com/api/v3/historical-chart/30min/'+ticker+'?apikey=f6003a61d13c32709e458a1e6c7df0b0'
$.getJSON(url, function(data) {
    data
    var arr = [];
    var pos_arr=[];
    for (d of data) {
        parsed_d=Date.parse(d["date"])
        arr.push( [parsed_d , d["close"] ]);
        if(parsed_d<point_end && parsed_d>point_start){
            pos_arr.push([parsed_d , d["close"]]);
        }
    }
    rev_main=arr.reverse()
    rev_pos=pos_arr.reverse()
    Highcharts.stockChart('container_position_on_graph', {
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
            {
              name: 'position',
              data: rev_pos,
              color: position_colour,
              lineWidth:4,
              id: 'dataseries2',
              tooltip: {
                valueDecimals: 2
              }
            },
            {
                type: 'flags',
                data: [{
                        x: Date.parse(stp),
                        title: ' ',
                        text: 'Tiprank: ' + tip_rank_on_buy + ' FMP: ' + fmp_rating_on_buy
                    },
                    {
                        x: Date.parse(enp),
                        title: ' ',
                        text: 'Position closed'
                    }],
                onSeries: 'dataseries',
                shape: 'circlepin',
                width: 16
            }
        ]
    });
});

