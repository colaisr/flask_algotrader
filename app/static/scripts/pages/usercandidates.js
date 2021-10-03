 $(document).ready(function () {
//        function to search the candidates table
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

    // validating ticker and adding data
    $('#btn_validate').on('click', function() {
        get_data_for_ticker();
    })

    $( "#btn_submit" ).on('click', function() {
        ticker = $('#txt_ticker').val();
        reason = $('#txt_reason').val();
        email = $('#user-email').val();

//        url = 'http://localhost:8000/candidates/updatecandidate/';
        url = 'https://colak.eu.pythonanywhere.com/candidates/updatecandidate/';
        $.post(url,{ticker: ticker, reason: reason, email: email}, function(data) {
            window.location.reload();
        })
    });

})

//getting a data for ticker
function get_data_for_ticker(){
    ticker=$('#txt_ticker').val();
//    url = 'http://localhost:8000/research/get_info_ticker/' + ticker
    url = 'https://colak.eu.pythonanywhere.com/research/get_info_ticker/' + ticker
    $.getJSON(url, function(data) {
        //var data_parsed = jQuery.parseJSON(data);
        if (data == 'undefined')
        {
            alert('Wrong ticker');
        }
        else{
            $('#txt_company_name').val(data.longName);
            $('#txt_company_description').val(data.longBusinessSummary);
            $('#txt_exchange').val(data.exchange);
            $('#txt_industry').val(data.industry);
            $('#txt_sector').val(data.sector);
            $('#txt_logo').val(data.logo_url);
            $('#txt_ticker').val($('#txt_ticker').val().toUpperCase());

            $("#btn_submit").prop('disabled', false);
        }
    })
}



