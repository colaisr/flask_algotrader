$(document).ready(function () {

    $(window).resize(function() {
        set_min_height_to_divs();
    }).resize();

    $('#search-tickers').keypress(function (e) {
        var key = e.which;
        if(key == 13)  // the enter key code
        {
            var href = $('.ui-autocomplete li:first a').attr("href");
            if(href != undefined && $(this).val() != '' && $(this).val() != undefined){
                window.location.href = window.location.origin + href;
            }
        }
    });

    $( "#search-tickers" ).autocomplete({
        source: function( request, response ) {
//            loading('today-search-tab');
            $('.search-input').addClass('placeholder-glow');
            $('.search-input').addClass('opacity-25');
            $('#search-tickers').addClass('placeholder');
            $('.loading-element').removeClass('invisible');
            $.getJSON("/api/search",{query: request.term}, function(data) {
                response(data);
                $('.ui-autocomplete').width($('#search-tickers').width());
                $('.search-input').removeClass('placeholder-glow');
                $('.search-input').removeClass('opacity-25');
                $('#search-tickers').removeClass('placeholder');
                $('.loading-element').addClass('invisible');
            })
        },
        create: function () {
//            loading('search-tab');
            $(this).data('ui-autocomplete')._renderItem = function (ul, item) {
                ul.addClass('list-group');
                var div = '<a class="text-muted" href="/candidates/info/' + item.symbol + '"><div class="d-flex justify-content-between align-items-center">' + item.symbol + '<span>'  + item.name + '</span></div></a>';
                var li = $('<li data-ticker="' + item.symbol + '" class="list-group-item">')
                        .append(div)
                        .appendTo(ul);
                $('.ui-autocomplete li:first .ui-menu-item-wrapper').addClass('ui-state-active');
                return li;
            };
//            stop_loading('search-tab');
        }
    });


    var emotion_settings = parseInt($('#user-emotion').val());
    var main_snp = [];
    var main_emotion = [];
    var count_days_emotion = 0;

//    load_data();
    upload_personal_list();
    upload_today_improovers_data();
//    upload_telegram_signals();
    fill_emotion_and_snp_graphs(emotion_settings, false, main_snp, main_emotion);

//    $('.show_signals_modal').click(function(){
//        $(".signals_modal").show();
//    });
//
//    $('.signals-modal-close').click(function(){
//        $(".signals_modal").hide();
//    });

    $('.show_personal_modal').click(function(){
        $('#personal-list-flash').empty();
        $(".personal_modal").show();
    });

    $('.personal-modal-close').click(function(){
        $(".personal_modal").hide();
    });

//    $('.show_improovers_modal').click(function(){
//        $(".improovers_modal").show();
//    });
//
//    $('.improovers-modal-close').click(function(){
//        $(".improovers_modal").hide();
//    });


//    $('#today_emotion_box').click(function(){
//        $(".emotion-modal").show();
//    });
//
//    $('.emotion-modal-close').click(function(){
//        $(".emotion-modal").hide();
//    });

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
function set_min_height_to_divs(){
    var height = $('.improovers').height();
    $('.personal-list').css('min-height', height);
    $('.signals').css('min-height', height);
}

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
    var td_logo =$('<td class="text-center pe-0 ps-0"><img src="' + c.logo + '" width="20" height="20"></td>');
    tr.append(td_logo);
    var td_company = $('<td class="pe-0 ps-0"><a class="fs--1" href="/candidates/info/' + c.ticker + '">' + c.ticker + '</a><div class="text-small fs--2">' + c.company_name + '</div></td>');
    tr.append(td_company);
    var td_score = $('<td class="text-center pe-0 ps-0">' + score + '</td>');
    tr.append(td_score);
    var td_change = $('<td class="text-center text-success pe-0 ps-0">' + change + '</td>');
    tr.append(td_change);
    $('.' + tbl_class + ' tbody').append(tr);
}

function upload_telegram_signals(){
//    loading('telegram-card-body');
    url = '/candidates/telegram_signals';
    $.getJSON(url, function(data) {
        draw_telegram_signals_tbl(data);
//        stop_loading('telegram-card-body');
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
    var td_company = $('<td><a href="/candidates/info/' + c.ticker + '">' + c.ticker + '</a><div class="text-small">' + c.company_name + '</div></td>');
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

function upload_personal_list(){
    loading('personal-list-card-body');
    url = '/candidates/user_candidates';
    $.getJSON(url, function(data) {
        draw_user_candidates_tbl(data); //from base.js
        stop_loading('personal-list-card-body');
    });
}

function draw_user_candidates_tbl(data){
    $('.personal-tbl tbody').empty();
    $('.personal-modal-tbl tbody').empty();
    $.each(data, function( index, c ){
        if(parseInt(index) < 5){
            add_row_to_personal_candidates(c, 'personal-tbl', false)       //from base.js
        }
        add_row_to_personal_candidates(c, 'personal-modal-tbl', true)       //from base.js
        $('#remove-' + c.ticker).on('click',remove_candidate);
        $('#enabled-' + c.ticker).on('click',change_enabled);
        $('#edit-' + c.ticker).on('click',edit_candidate);
    })
}

function add_row_to_personal_candidates(c, tbl_class, is_modal){
    var score = c.algotrader_rank || 0;
    var under_priced_pnt = c.under_priced_pnt != null ? c.under_priced_pnt.toFixed(2) : 0;
    var twelve_month_momentum = c.twelve_month_momentum != null ? c.twelve_month_momentum.toFixed(2) : 0;
    var beta = c.beta != null ? c.beta.toFixed(2) : 0;
    var max_intraday_drop_percent = c.max_intraday_drop_percent != null ? c.max_intraday_drop_percent.toFixed(2) : 0;
    var tr = $('<tr class="btn-reveal-trigger" title="' + c.reason + '"></tr>');
    var td_logo =$('<td class="text-center pe-0 ps-0"><img src="' + c.logo + '" width="20" height="20"></td>');
    tr.append(td_logo);
    var td_company = $('<td class="pe-0 ps-0"><a class="fs--1" href="/candidates/info/' + c.ticker + '">' + c.ticker + '</a><div class="fs--2">' + c.company_name + '</div></td>');
    tr.append(td_company);
    if(is_modal){
        var td_remove = $('<td class="text-center pe-0 ps-0"><button id="remove-' + c.ticker +'" type="submit" data-ticker="' + c.ticker + '" class="border-0 bg-body remove-candidate"><i class="fa fa-trash"></i></button></td>');
        tr.append(td_remove);
        var td_edit = $('<td class="text-center pe-0 ps-0"><button class="btn_edit border-0 bg-body" id="edit-' + c.ticker + '"><i class="fa fa-edit mt-1"></i></button><input type="hidden" class="h_tick" value="' + c.ticker + '"><input type="hidden" class="h_reason" value="' + c.reason + '"></td>');
        tr.append(td_edit);
        var td_enabled = $('<td class="text-center pe-0 ps-0"><input class="form-check-input enable-checkbox" id="enabled-' + c.ticker + '" data-ticker="' + c.ticker + '" type="checkbox"></td>');
        tr.append(td_enabled);
    }

    var td_score = $('<td class="text-center pe-0 ps-0">'+score+'</td>');
    tr.append(td_score);
    var td_sector = $('<td class="pe-0 ps-0">' + c.sector + '</td>');
    tr.append(td_sector);
    var td_under_price = $('<td class="text-center pe-0 ps-0">' + under_priced_pnt + '</td>');
    tr.append(td_under_price);
    var td_momentum = $('<td class="text-center pe-0 ps-0">' + twelve_month_momentum + '</td>');
    tr.append(td_momentum);
    var td_beta = $('<td class="text-center pe-0 ps-0">' + beta + '</td>');
    tr.append(td_beta);
    var td_intraday_drop = $('<td class="text-center">' + max_intraday_drop_percent + '</td>');
    tr.append(td_intraday_drop);
    if(!is_modal){
        var actions = $('<td class="text-end"></td>');
        var actions_dropdown = $('<div class="dropdown font-sans-serif position-static"></div>');
        var actions_btn = $('<button class="btn btn-link text-600 btn-sm dropdown-toggle btn-reveal" type="button" data-bs-toggle="dropdown" data-boundary="window" aria-haspopup="true" aria-expanded="false"><span class="fas fa-ellipsis-h fs--1"></span></button>');
        var actions_dropdown_menu = $('<div class="dropdown-menu dropdown-menu-end border py-0"></div>');
        var actions_div = $('<div class="bg-white py-2"></div>');
        var actions_edite = $('<button class="dropdown-item btn_edit border-0 bg-body" id="edit-' + c.ticker + '"><i class="fa fa-edit mt-1"></i><span class="ps-2">Edit</span></button>');
        var actions_delete = $('<button id="remove-' + c.ticker +'" type="submit" data-ticker="' + c.ticker + '" class="dropdown-item border-0 bg-body remove-candidate"><i class="fa fa-trash"></i><span class="ps-2">Delete</span></button>');
        actions_div.append(actions_edite);
        actions_div.append(actions_delete);
        actions_dropdown_menu.append(actions_div);
        actions_dropdown.append(actions_btn);
        actions_dropdown.append(actions_dropdown_menu);
        actions.append(actions_dropdown);
        tr.append(actions);
    }
    $('.' + tbl_class + ' tbody').append(tr);
    $('#enabled-' + c.ticker).prop('checked', c.enabled);
}





