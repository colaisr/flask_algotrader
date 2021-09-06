 $(document).ready(function () {
    user = $("#user").val()
    $.post("/closed_position_info/user_reports_history",{user: user}, function(data) {
        var arr = [];
        data_parsed = jQuery.parseJSON(data);
        for (d of data_parsed) {
            parsed_d=Date.parse(d["report_time"])
            arr.push( [parsed_d , d["net_liquidation"] ]);
        }
        rev_main=arr.reverse()

        Highcharts.stockChart('net-report', {
            rangeSelector: {
              selected: 1
            },
            title: {
              text: 'NET statistics'
            },
            series: [
                {
                  name: 'NET',
                  data: rev_main,
                  id: 'dataseries',
                  tooltip: {
                    valueDecimals: 2
                  }
                }
            ]
        });
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
})