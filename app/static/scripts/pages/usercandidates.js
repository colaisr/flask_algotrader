 $(document).ready(function () {

    var emotion_settings = parseInt($('#user-emotion').val());
    var main_snp = [];
    var main_emotion = [];
    var count_days_emotion = 0;
    fill_emotion_and_snp_graphs(emotion_settings, false, main_snp, main_emotion);

    $('#emotion_box').click(function(){
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
        $("#add_candidate_modal").show();
    })

//    $('#emotion_box').click(function(){
//        window.open("https://money.cnn.com/data/fear-and-greed/", "_blank");
//    });

    $('#txt_ticker, #txt_reason').on('input',function(){
        $('#candidate-flash').empty();
    });

})



