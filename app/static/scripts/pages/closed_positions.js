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

    $('.filter-btn').on('click', function(e) {
        filter_val = $(this).find(".filter-option").val();
        $('#filter_radio').val(filter_val)
        GetTimeInterval(filter_val);
    })

    $('.filter-option').on('change', function(e) {
        from_date = new Date($("#from_date").val());
        to_date = new Date($("#to_date").val());
        if(from_date < to_date){
            $( "#closed-position-form" ).submit();
        }
    })

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

    function GetTimeInterval(filter_val){
        var date = new Date();
        $("#to_date").val(date.toISOString().split('T')[0]);

        if(filter_val=="2"){
            date.setDate(date.getDate() - 7);
        }
        else if(filter_val=="3"){
            date.setMonth(date.getMonth() - 1);
        }
        else if(filter_val=="4"){
            date.setYear(date.getFullYear() - 1);
        }
        else{
            date = new Date($("#from_date").prop("min"));
        }

        $("#from_date").val(date.toISOString().split('T')[0]);
        $('.filter-option').change();
    }
})