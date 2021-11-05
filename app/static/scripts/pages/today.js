candidates =jQuery.parseJSON(candidates);
//market_data =jQuery.parseJSON(market_data);

 $(document).ready(function () {
    var emotion_settings = parseInt($('#user-emotion').val());
    var main_snp = [];
    var main_emotion = [];
    var count_days_emotion = 0;

    upload_personal_list();
    fill_emotion_and_snp_graphs(emotion_settings, false, main_snp, main_emotion);

    $('.show_signals_modal').click(function(){
        $(".signals_modal").show();
    });

    $('.signals-modal-close').click(function(){
        $(".signals_modal").hide();
    });

    $('.show_personal_modal').click(function(){
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

    //editing a candidate
    $('.btn_edit').on('click', function() {
        clicked_on=event.target.parentElement;
        $('.ticker-desc').val('');
        ticker=$(clicked_on).siblings('.h_tick')[0].value;
        reason=$(clicked_on).siblings('.h_reason')[0].value;
        $('#txt_ticker').val(ticker);
        $('#txt_reason').val(reason);
        $('#btn_validate').click();
        $("#add_candidate_modal").show();
    })

    $('.remove-candidate').on('click',function(){
        var ticker = $(this).data('ticker');
        remove_candidate(ticker);
    })

    $('.enable-checkbox').on('change',function(){
        var ticker = $(this).data('ticker');
        var enabled = $(this).is(':checked');
        change_enabled(ticker, enabled);
    })


    $('#txt_ticker, #txt_reason').on('input',function(){
        $('#candidate-flash').empty();
    });

})

function change_enabled(ticker, enabled){
    if($(this).data('ticker') != undefined){
        ticker = $(this).data('ticker');
        enabled = $(this).is(':checked');
    }
    $.post("/candidates/enabledisable_ajax",{ticker: ticker}, function(data) {
        var data_parsed = jQuery.parseJSON(data);
        if(data_parsed["result"]){
            var candidate = $.grep( candidates, function( n, i ) { return n.ticker == ticker;});
            if(candidate.length != 0){
                candidate.enabled = enabled;
            }
        }
    });
}

function remove_candidate(ticker){
    if($(this).data('ticker') != undefined){
        ticker = $(this).data('ticker');
    }
    $.post("/candidates/removecandidate_ajax",{ticker: ticker}, function(data) {
        var data_parsed = jQuery.parseJSON(data);
        draw_user_candidates_tbl(data_parsed);
    });
}

function upload_personal_list(){
    url = '/candidates/user_candidates';
    $.getJSON(url, function(data) {
        draw_user_candidates_tbl(data);
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
    })
}



