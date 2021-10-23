var emotion_settings = parseInt($('#algo_min_emotion').val());
var min_snp = parseFloat($('#algo_positions_for_swan').val());
var main_snp = [];
var main_emotion =[];
var bsw_snp_main = [];
var snp_drop_arr = [];
var bsw_global = [];

$(document).ready(function () {
//    get_snp_data($('#algo_positions_for_swan').val());
    get_candidates_by_filter();
    fill_emotion_and_snp_graphs(emotion_settings, true, main_snp, main_emotion);
    blackswan_modal(bsw_snp_main, snp_drop_arr, min_snp, bsw_global);
    range_set_value("range","rangeV");
    range_set_value("bsw-range","bsw-rangeV");

    $('.strategy-change').on('input', function(e) {
        $('#strategy_id').val('4')
        $('.strategy-btn').removeClass( "active" )
        get_candidates_by_filter();
    })

    $('.emotion-change').on('input', function(e) {
        var loading = $(".emotion-loading")
        var spinner = $('<div class="spinner-border text-info" role="status"><span class="sr-only">Loading...</span></div>');
        loading.empty();
        $(".emotion-filter").empty();
        $(".emotion-fixed-filter-text").empty();
        loading.append(spinner);

        var emotion = $(this).val();

        $('#range').val(emotion);
        range_set_value("range","rangeV");

        var emotion_dic = update_emotion_days(emotion);
        var new_graph = draw_snp_chart(main_snp, emotion_dic.days_arr, [emotion_dic.series[0]], true);

        loading.empty();
    })

    $('.blackswan-change').on('input', function(e) {
//        var loading = $(".bsw-loading")
//        var spinner = $('<div class="spinner-border text-info" role="status"><span class="sr-only">Loading...</span></div>');
//        loading.empty();
//        $(".blackswan-events").empty();
//        loading.append(spinner);

        var val = $(this).val();
        if($.isNumeric(val)){
            change_black_swan(bsw_snp_main, snp_drop_arr, bsw_global, parseFloat(val));
            $('#bsw-range').val(val);
            range_set_value("bsw-range","bsw-rangeV");
        }
//        loading.empty();
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

    $(".emotion-filter").on('click', function(e) {
        $(".emotion-modal").show();
    });

    $(".emotion-modal-close").on('click', function(e) {
        $(".emotion-modal").hide();
    });

    $("#range").on('input', function(e) {
        range_set_value("range","rangeV");
    });

    $("#range").on('change', function(e) {
//        $('#container_sp500').empty();
        var emotion = $(this).val();
        var emotion_dic = update_emotion_days(emotion);
        var new_graph = draw_snp_chart(main_snp, emotion_dic.days_arr, [emotion_dic.series[0]], true);
        $('.emotion-change').val(emotion);
    });

    $("#bsw-range").on('input', function(e) {
        range_set_value("bsw-range","bsw-rangeV");
    });

    $("#bsw-range").on('change', function(e) {
        var bsw = $(this).val();
//        var loading = $(".bsw-loading")
//        var spinner = $('<div class="spinner-border text-info" role="status"><span class="sr-only">Loading...</span></div>');
//        loading.empty();
//        $(".blackswan-events").empty();
//        loading.append(spinner);
        change_black_swan(bsw_snp_main, snp_drop_arr, bsw_global, parseFloat(bsw));
        $('.blackswan-change').val(bsw);
    });

})

function save_emotion(){
    var emotion = parseInt($('.emotion-change').val());
    $.post("/algotradersettings/save_emotion_settings",{emotion: emotion}, function(data) {
        $('#flash').append(flashMessage("success","Emotion saved"));

    });
}

function save_black_swan(){
    var bsw = parseFloat($('.blackswan-change').val());
    $.post("/algotradersettings/save_black_swan",{bsw: bsw}, function(data) {
        $('#snp-flash').append(flashMessage("success","Market fall safety saved"));

    });
}

function update_emotion_days(emotion){
    var emotion_dic = get_days_for_snp_backtesting(emotion, main_emotion, false);
    var dic = get_snp_series_by_emotion(main_snp, emotion_dic.days_arr, [emotion_dic.series[0]]);
    $(".emotion-fixed-filter-text").empty();
    $(".emotion-filter").empty();
    $(".emotion-filter").text(dic.days_num);
    $(".emotion-fixed-filter-text").text("days in last year");
    return emotion_dic;
}

function updateTextInput(val) {
    $('#textInput').val(val);
}

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



