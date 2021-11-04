candidates =jQuery.parseJSON(candidates);
market_data =jQuery.parseJSON(market_data);

 $(document).ready(function () {
    var emotion_settings = parseInt($('#user-emotion').val());
    var main_snp = [];
    var main_emotion = [];
    var count_days_emotion = 0;
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


    $('#txt_ticker, #txt_reason').on('input',function(){
        $('#candidate-flash').empty();
    });

})

function change_enabled()
{
    alert('test');
}

function remove_candidate(ticker){
    if($(this).data('ticker') != undefined){
        ticker = $(this).data('ticker');
    }
    $.post("/candidates/removecandidate_ajax",{ticker: ticker}, function(data) {
        var data_parsed = jQuery.parseJSON(data);
        if(data_parsed["result"]){
            $('.personal-modal-tbl tbody td:icontains(' + ticker + ')').closest('tr').remove();
            if($('.personal-tbl tbody td:icontains(' + ticker + ')').length > 0){
                $('.personal-tbl tbody').empty();
                var candidates_updated = $.grep( candidates, function( n, i ) { return n.ticker == ticker;},true);
                var top_candidates = candidates_updated.slice(0,5);
                $.each(top_candidates, function( index, c ){
                    add_row_to_personal_candidates(c, market_data, 'personal-tbl', false)       //from base.js
                })
            }
        }
    });
}



