$(document).ready(function () {
    var emotion_settings = parseInt($('#user-emotion').val());
    var main_snp = [];
    var main_emotion = [];
    var count_days_emotion = 0;

    upload_personal_list(); //from base.js
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







