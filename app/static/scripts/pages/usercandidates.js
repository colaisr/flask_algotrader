 $(document).ready(function () {

// creating a candidate
    $('#btnAddCandidate').on('click', function() {
        $("#add_candidate_modal").show();
    })

    $('#btn-modal-hide').on('click', function() {
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

    $('#emotion_box').click(function(){
        window.open("https://money.cnn.com/data/fear-and-greed/", "_blank");
    });

})



