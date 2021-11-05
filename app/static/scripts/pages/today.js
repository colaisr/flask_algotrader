$(document).ready(function () {
    var emotion_settings = parseInt($('#user-emotion').val());
    var main_snp = [];
    var main_emotion = [];
    var count_days_emotion = 0;

//    load_data();
    upload_personal_list();
    upload_today_improovers_data();
    upload_telegram_signals();
    fill_emotion_and_snp_graphs(emotion_settings, false, main_snp, main_emotion);

    $('.show_signals_modal').click(function(){
        $(".signals_modal").show();
    });

    $('.signals-modal-close').click(function(){
        $(".signals_modal").hide();
    });

    $('.show_personal_modal').click(function(){
        $('#personal-list-flash').empty();
        $(".personal_modal").show();
    });

    $('.personal-modal-close').click(function(){
        $(".personal_modal").hide();
    });

    $('.show_improovers_modal').click(function(){
        $(".improovers_modal").show();
    });

    $('.improovers-modal-close').click(function(){
        $(".improovers_modal").hide();
    });


    $('#today_emotion_box').click(function(){
        $(".emotion-modal").show();
    });

    $('.emotion-modal-close').click(function(){
        $(".emotion-modal").hide();
    });

// creating a candidate
    $('#btnAddCandidate').on('click', function() {
        $('#candidate-flash').empty();
        $('.ticker-desc').val('');
        $('.content-hidden').prop('hidden',true);
        $('.modal-body input, .modal-body textarea').val("");
        $("#btn_submit").prop('disabled', true);
        $('#user-email').val($('#user_email').val());
        $("#add_candidate_modal").show();
    })

    $('.btn-modal-hide').on('click', function() {
        $("#add_candidate_modal").hide();
    })

    $('.remove-candidate').on('click',function(){
        var ticker = $(this).data('ticker');
        remove_candidate(ticker);
    })

    $('#txt_ticker, #txt_reason').on('input',function(){
        $('#candidate-flash').empty();
    });

})


function change_enabled(ticker, enabled){
    $('#personal-list-flash').empty();
    if($(this).data('ticker') != undefined){
        ticker = $(this).data('ticker');
        enabled = $(this).is(':checked');
    }
    $.post("/candidates/enabledisable_ajax",{ticker: ticker}, function(data) {
        var data_parsed = jQuery.parseJSON(data);
        $('#personal-list-flash').append(flashMessage(data_parsed["color_status"],data_parsed["message"]));
    });
    setTimeout(function(){
            $('#personal-list-flash').empty();
    }, 2000);
}

function remove_candidate(ticker){
    if($(this).data('ticker') != undefined){
        ticker = $(this).data('ticker');
    }
    $.post("/candidates/removecandidate_ajax",{ticker: ticker}, function(data) {
        var data_parsed = jQuery.parseJSON(data);
        draw_user_candidates_tbl(data_parsed); //from base.js
    });
}

function edit_candidate(){
    $('.ticker-desc').val('');
    ticker=$(this).siblings('.h_tick')[0].value;
    reason=$(this).siblings('.h_reason')[0].value;
    $('#txt_ticker').val(ticker);
    $('#txt_reason').val(reason);
    $('#btn_validate').click();
    $("#add_candidate_modal").show();
}

function upload_today_improovers_data(){
    loading('improovers-card-body');
    url = '/candidates/today_improovers';
    $.getJSON(url, function(data) {
        draw_today_improovers_tbl(data);
        stop_loading('improovers-card-body');
    });
}

function draw_today_improovers_tbl(data){
    $('.improovers-tbl tbody').empty();
    $('.improovers-modal-tbl tbody').empty();
    $.each(data, function( index, c ){
        if(parseInt(index) < 5){
            add_row_to_today_improovers(c, 'improovers-tbl')       //from base.js
        }
        add_row_to_today_improovers(c, 'improovers-modal-tbl')       //from base.js
    })
}

function add_row_to_today_improovers(c, tbl_class){
    var score = c.last_rank || 0;
    var change = c.change_val != null ? c.change_val.toFixed(2) : 0;
    var tr = $('<tr></tr>');
    var td_logo =$('<td class="text-center"><img src="' + c.logo + '" width="20" height="20"></td>');
    tr.append(td_logo);
    var td_company = $('<td><a href="/candidates/info?ticker_to_show=' + c.ticker + '">' + c.ticker + '</a><div class="text-small">' + c.company_name + '</div></td>');
    tr.append(td_company);
    var td_score = $('<td class="text-center">' + score + '</td>');
    tr.append(td_score);
    var td_change = $('<td class="text-center text-success">' + change + '</td>');
    tr.append(td_change);
    $('.' + tbl_class + ' tbody').append(tr);
}

function upload_telegram_signals(){
    loading('telegram-card-body');
    url = '/candidates/telegram_signals';
    $.getJSON(url, function(data) {
        draw_telegram_signals_tbl(data);
        stop_loading('telegram-card-body');
    });
}

function draw_telegram_signals_tbl(data){
    $('.signals-tbl tbody').empty();
    $('.signals-modal-tbl tbody').empty();
    $.each(data, function( index, c ){
        if(parseInt(index) < 5){
            add_row_to_telegram_signals(c, 'signals-tbl', false)
        }
        add_row_to_telegram_signals(c, 'signals-modal-tbl', true)
    })
}

function add_row_to_telegram_signals(c, tbl_class, is_modal){
    var price = c.signal_price != null ? c.signal_price.toFixed(2) : 0;
    var target = c.target_price != null ? c.target_price.toFixed(2) : 0;

    var tr = $('<tr></tr>');
    var td_logo =$('<td class="text-center"><img src="' + c.logo + '" width="20" height="20"></td>');
    tr.append(td_logo);
    var td_company = $('<td><a href="/candidates/info?ticker_to_show=' + c.ticker + '">' + c.ticker + '</a><div class="text-small">' + c.company_name + '</div></td>');
    tr.append(td_company);

    var td_price = $('<td class="text-center">'+price+'</td>');
    tr.append(td_price);
    var td_target = $('<td class="text-center">' + target + '</td>');
    tr.append(td_target);

    if(is_modal){
        var profit = c.tprofit_percent != null ? c.profit_percent.toFixed(2) : 0;
        var days = c.days_to_get != null ? c.days_to_get.toString() : '--';
        var td_profit = $('<td class="text-center">' + profit + '</td>');
        tr.append(td_profit);
        var td_days = $('<td class="text-center">' + days + '</td>');
        tr.append(td_days);
    }
    $('.' + tbl_class + ' tbody').append(tr);
}

//function load_data(){
//    improovers_url = '/candidates/today_improovers';
//    user_candidates_url = '/candidates/user_candidates';
//    Promise.all([
//      $.ajax({ url: improovers_url }),
//      $.ajax({ url: user_candidates_url })
//    ])
//    .then(([improovers, user_cand]) => {
//        improovers_data = jQuery.parseJSON(improovers);
//        users_candidates_data = jQuery.parseJSON(user_cand);
//        draw_user_candidates_tbl(improovers_data);   //from base.js
//        draw_today_improovers_tbl(users_candidates_data);
//    });
//
//}







