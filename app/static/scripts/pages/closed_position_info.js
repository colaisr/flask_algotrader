
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

fill_container_closed_position_info();


