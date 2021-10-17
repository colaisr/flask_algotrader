 $(document).ready(function () {

    get_snp_data($('#algo_positions_for_swan').val());
    get_candidates_by_filter();

    $('.strategy-change').on('input', function(e) {
        $('#strategy_id').val('4')
        $('.strategy-btn').removeClass( "active" )
        get_candidates_by_filter();
    })

    $('.blackswan-change').on('input', function(e) {
        var val = $(this).val();
        if($.isNumeric(val)){
            get_snp_data(val);
        }
    })

    $('#signature_full_name').on('input', function(e) {
        var signature_full_name = $('#signature_full_name').val();
        if(signature_full_name.length >0
            && signature_full_name.trim() != ''
            && signature_full_name.trim().split(' ').length > 1
            && signature_full_name.trim().split(' ')[signature_full_name.trim().split(' ').length-1].trim() != ''){
           $('#signature').prop("disabled", false)
        }
        else{
            $('#signature').prop('checked', false);
            $('#signature').prop("disabled", true)
            $('#signature-submit').prop("disabled", true)
        }

        $("#signature").change(function() {
            if(this.checked) {
                $('#signature-submit').prop("disabled", false)
            }
            else{
                $('#signature-submit').prop("disabled", true)
            }
        });
    })

    $(".show_modal_snp").on('click', function(e) {
        $(".snp-modal").show();
    });

    $(".snp-modal-close").on('click', function(e) {
        $(".snp-modal").hide();
    });

})

function UpdateDefaultStrategy(el){
    $("#strategy_id").val($(el).val());
    $.post("/algotradersettings/get_default_strategy_settings",{strategy_id: $(el).val()}, function(data) {
        var data_parsed = jQuery.parseJSON(data);
        $('#algo_apply_min_rank').prop("checked",data_parsed.algo_apply_min_rank);
        $('#algo_apply_accepted_fmp_ratings').prop("checked",data_parsed.algo_apply_accepted_fmp_ratings);
        $('#algo_apply_max_yahoo_rank').prop("checked",data_parsed.algo_apply_max_yahoo_rank);
        $('#algo_apply_min_stock_invest_rank').prop("checked",data_parsed.algo_apply_min_stock_invest_rank);
        $('#algo_apply_min_underprice').prop("checked",data_parsed.algo_apply_min_underprice);
        $('#algo_apply_min_momentum').prop("checked",data_parsed.algo_apply_min_momentum);
        $('#algo_apply_min_beta').prop("checked",data_parsed.algo_apply_min_beta);
        $('#algo_apply_max_intraday_drop_percent').prop("checked",data_parsed.algo_apply_max_intraday_drop_percent);

        $('#algo_min_rank').val(data_parsed.algo_min_rank);
        $('#algo_accepted_fmp_ratings').val(data_parsed.algo_accepted_fmp_ratings);
        $('#algo_max_yahoo_rank').val(data_parsed.algo_max_yahoo_rank);
        $('#algo_min_stock_invest_rank').val(data_parsed.algo_min_stock_invest_rank);
        $('#algo_min_underprice').val(data_parsed.algo_min_underprice);
        $('#algo_min_momentum').val(data_parsed.algo_min_momentum);
        $('#algo_min_beta').val(data_parsed.algo_min_beta);
        $('#algo_max_intraday_drop_percent').val(data_parsed.algo_max_intraday_drop_percent);
    });
}

function get_snp_data(min_snp){
    $.post("/algotradersettings/get_snp500_data",{min_snp: min_snp}, function(data) {
            var data_parsed = jQuery.parseJSON(data);
            $('.blackswan-min').html(min_snp+'%')
            var tbody = $('.modal-body').find('tbody');
            tbody.empty();
            var tr = $("<tr></tr>");
            var td=$("<td></td>");
            var count = 0;
            $.each(data_parsed, function(key, value) {
                count++;
                tr = $("<tr></tr>")
                td = $("<td class='text-center font-weight-bold'></td>").text(key.substring(0,key.indexOf("T")));
                tr.append(td);
                $.each(value, function(k, v) {
                    td = $("<td class='text-center'></td>").text(value[k].toFixed(2));
                    tr.append(td);
                });
                tbody.append(tr);
            });
            $('.blackswan-events').html(count.toString())
        });
}

function get_candidates_by_filter(){
    var send_data={
        algo_ranks: $("#algo_min_algotrader_rank").val(),
        filtered_underprice: $("#algo_min_underprice").val(),
        filtered_momentum: $("#algo_min_momentum").val(),
        filtered_beta: $("#algo_min_beta").val(),
        filtered_max_intraday_drop: $("#algo_min_algotrader_rank").val(),
        total: $("#algo_max_intraday_drop_percent").val()
    }
    var loading = $(".loading")
    var spinner = $('<div class="spinner-border text-info" role="status"><span class="sr-only">Loading...</span></div>');
    loading.empty();
    $(".num-candidates").empty();
    $(".fixed-filter-text").empty();
    $(".fixed-total-filter-text").empty();
    loading.append(spinner);
    $.post("/connections/filter_candidates_data_ajax", send_data, function(data) {
            var data_parsed = jQuery.parseJSON(data);
            loading.empty();
            $(".algo-rank-filter").text(data_parsed["algo_ranks"]);
            $(".underprice-filter").text(data_parsed["filtered_underprice"]);
            $(".momentum-filter").text(data_parsed["filtered_momentum"]);
            $(".beta-filter").text(data_parsed["filtered_beta"]);
            $(".intraday-filter").text(data_parsed["filtered_max_intraday_drop"]);
            $(".total-filter").text(data_parsed["total"]);
            $(".fixed-filter-text").text("candidates match");
            $(".fixed-total-filter-text").text("Candidates match in Total");
        });
}

