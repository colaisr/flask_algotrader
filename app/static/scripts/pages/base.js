$(document).ready(function () {
    $(window).resize(function() {
        var width = $(this).width() - 100;
        $('.modal-bigger').css('max-width', width);
    }).resize();

    $('.message').each((i, el) => {
        const $el = $(el);
        const $xx = $el.find('.close');
        const sec = $el.data('autohide');
        const triggerRemove = () => clearTimeout($el.trigger('remove').T);

        $el.one('remove', () => $el.remove());
        $xx.one('click', triggerRemove);
        if (sec) $el.T = setTimeout(triggerRemove, sec * 1000);
    });

    $('#search-users').keyup(function () {
        var searchText = $(this).val();
        if (searchText.length > 0) {
            $('tbody td:icontains(' + searchText + ')').addClass('positive');
            $('td.positive').not(':icontains(' + searchText + ')').removeClass('positive');
            $('tbody td').not(':icontains(' + searchText + ')').closest('tr').addClass('hidden').hide();
            $('tr.hidden:icontains(' + searchText + ')').removeClass('hidden').show();
        } else {
            $('td.positive').removeClass('positive');
            $('tr.hidden').removeClass('hidden').show();
        }
    });

    $('#select-role').dropdown({
        onChange: function (value, text, $selectedItem) {
            $('td.user.role:contains(' + value + ')').closest('tr').removeClass('hidden').show();
            $('td.user.role').not(':contains(' + value + ')').closest('tr').addClass('hidden').hide();
        }
    });

});

function range_set_value(){
    var range = $('#range');
    var rangeV = $('#rangeV');
    var value = parseInt(range.val());
    var max = parseInt(range.prop('max'));
    var min = parseInt(range.prop('min'));

    var newValue = (value - min) * 100 / (max - min);
    var newPosition = 10 - (newValue * 0.2);
    rangeV.html('<span>' + value + '</span>');
    rangeV.css('left','calc(' + newValue + '% + (' + newPosition + 'px))');
}

function isFloat(n){
    return Number(n) === n && n % 1 !== 0;
}


//CHARTS
function get_days_for_snp_backtesting(emotion_settings, main_emotion, is_with_emotion_series){
    var days_arr=[];
    var pos_emotion_arr=[];
    var pos_emotion_arr_negative = []

    var date_index = new Date();
    var index = 0;

    var date_index_negative = new Date();
    var index_negative = 0;
    for (e of main_emotion)
    {
        var date = new Date(e[0]);
        if(e[1] >= emotion_settings){
            days_arr.push(date.toDateString());

            if(is_with_emotion_series){
                date.setDate(date.getDate() - 1);
                if(date.toDateString() == date_index.toDateString() && index > 0){
                    var pos_emotion = $(pos_emotion_arr).get(-1);
                    date.setDate(date.getDate() + 1);
                    pos_emotion.push(e);
                }
                else
                {
                    date.setDate(date.getDate() + 1);
                    var new_pos_emotion = [];
                    new_pos_emotion.push(e);
                    pos_emotion_arr.push(new_pos_emotion);
                }
                date_index = date;
                index += 1;
            }
        }
        else if(is_with_emotion_series){
            date.setDate(date.getDate() - 1);
            if(date.toDateString() == date_index_negative.toDateString() && index_negative > 0){
                var pos_emotion = $(pos_emotion_arr_negative).get(-1);
                date.setDate(date.getDate() + 1);
                pos_emotion.push(e);
            }
            else
            {
                date.setDate(date.getDate() + 1);
                var new_pos_emotion = [];
                new_pos_emotion.push(e);
                pos_emotion_arr_negative.push(new_pos_emotion);
            }
            date_index_negative = date;
            index_negative += 1;
        }
    }

    var series = []
    var main = {
        name: 'Emotion',
        data: main_emotion,
        id: 'dataseries',
    };
    series.push(main);
    if(is_with_emotion_series)
    {
        var i =0;
        for (arr of pos_emotion_arr_negative){
            var range = {
                name: 'EmotionColor',
                data: arr,
                color: '#FF0000',
                id: 'dataseries_neg' + i,
            };
            series.push(range);
            i += 1;
        }
        i =0;
        for (arr of pos_emotion_arr){
            var range = {
                name: 'Emotion',
                data: arr,
                color: '#00c36f',
                id: 'dataseries' + i,
            };
            series.push(range);
            i += 1;
        }
    }

    return {days_arr: days_arr, series: series};
}

function get_snp_series_by_emotion(main_snp, days_arr){
    var ticker='SP500';
    var pos_snp_arr=[];

    var date_index = new Date();
    var index = 0;
    for (d of main_snp)
    {
        var date_d = new Date(d[0]);
        if(days_arr.indexOf(date_d.toDateString()) >= 0){
            date_d.setDate(date_d.getDate() - 1);
            if(date_d.toDateString() == date_index.toDateString() && index > 0){
                var pos_snp = $(pos_snp_arr).get(-1);
                date_d.setDate(date_d.getDate() + 1);
                pos_snp.push(d);
            }
            else
            {
                date_d.setDate(date_d.getDate() + 1);
                var new_pos_snp = [];
                new_pos_snp.push(d);
                pos_snp_arr.push(new_pos_snp);
            }
            date_index = date_d;
            index += 1;
        }
    }

//        //***** SERIES SNP *****//
//        var filtered_arr = pos_snp_arr.filter(x => x.length > 1);
    var series = []
    var main = {
        name: ticker,
        data: main_snp,
        id: 'dataseries',
        enableMouseTracking: false
    };
    series.push(main);
    var i =1;
    var days_num = 0;
    for (arr of pos_snp_arr){
        days_num += arr.length;
        var range = {
            name: "Color",
            data: arr,
            color: '#00c36f',
            lineWidth:3,
            id: 'Color' + i,
        };
        series.push(range);
        i += 1;
    }

    return {series: series, days_num: days_num};
}

function draw_graph(container_name, title, series, if_by_last_el){
    var chart = Highcharts.stockChart(container_name, {
        rangeSelector: {
            selected: 4
        },
        title: {
            text: title
        },
        tooltip: {
            useHTML: true,
            valueDecimals: 2,
            formatter: function() {
                var x = this.x;
                var date = new Date(x);
                var all_series = this.points[0].series.chart.series;
                var i = if_by_last_el ? -2 : 0; // -2: last element - navigation
                var series = $(all_series).get(i);
                var x_arr = series.processedXData;
                var index_in_arr = x_arr.indexOf(x);
                var data = series.processedYData[index_in_arr];
                if(isFloat(data)){
                    data = data.toFixed(2);
                }
                var html = '<table><tr><th colspan="2">'+date.toDateString()+'</th></tr><tr><td style="color: #00c36f">'+series.name+': </td>' +
                           '<td style="text-align: right"><b>'+data+'</b></td></tr></table>';

                return html;
            }
        },
        series: series
    });
    return chart;
}

function remove_series(chart, seriesname){
    var series = chart.series;
    for (s of series){
        if(s.name == seriesname){
            s.remove();
        }
    }
}
//END CHARTS

