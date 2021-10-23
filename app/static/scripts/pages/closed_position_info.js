
ticker=$( "#ticker" )[0].value;
profit=$( "#profit" )[0].value;
enp=$("#closed")[0].value;
stp=$( "#opened" )[0].value;
buying_algotrader_rank=$( "#buying_algotrader_rank" )[0].value;
emotion_on_buy=$( "#emotion_on_buy" )[0].value;
point_start=Date.parse(stp)
point_end=Date.parse(enp)
//rank_array.forEach(element => element[0]=element[0].replace(/^"(.*)"$/, '$1'));

if(profit>0){
    position_colour='#00c36f'
}
else{
    position_colour='#FF0000'
}

$(document).ready(function () {

    fill_container_closed_position_info();
})

function fill_container_closed_position_info(){

    url = '/algotradersettings/get_complete_graph_for_ticker/'+ticker
    $.getJSON(url, function(data) {
        data=data['historical']
        var arr = [];
        var pos_arr=[];
        for (d of data)
        {
            parsed_d=Date.parse(d["Date"]);
            arr.push( [parsed_d , d["Close"] ]);
            if(parsed_d<point_end && parsed_d>point_start){
                pos_arr.push([parsed_d , d["Close"]]);
            }
        }
        var series = [
            {
                name: ticker,
                data: arr,
                id: 'dataseries'
            },
            {
                name: 'position',
                data: pos_arr,
                color: '#FF0000',
//                lineWidth:3,
                id: 'dataseries2'
            },
            {
                type: 'flags',
                data: [{
                        x: Date.parse(stp),
                        title: ' ',
                        text: 'Algotrader rank: ' + buying_algotrader_rank + ' Emotion: ' + emotion_on_buy
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
        ];
        var chart = draw_graph('container_position_on_graph', ticker+' Stock Price', series, 1, false, false);
    });
}


