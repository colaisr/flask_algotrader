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
    $("#add_candidate_modal").modal("show");
})

//editing a candidate
$('.btn_edit').on('click', function() {

clicked_on=event.target.parentElement;

ticker=$(clicked_on).siblings('.h_tick')[0].value;
reason=$(clicked_on).siblings('.h_reason')[0].value;
$('#txt_ticker').val(ticker);
$('#txt_reason').val(reason);
m=$('#add_candidate_modal')
m.show()
})

// validating ticker and adding data
$('#btn_validate').on('click', function() {
get_data_for_ticker();

})

})
//getting a data for ticker
function get_data_for_ticker(){
ticker=$('#txt_ticker').val();
url='https://financialmodelingprep.com/api/v3/profile/'+ticker+'?apikey=f6003a61d13c32709e458a1e6c7df0b0';
$.getJSON(url, function(data) {
if (data.length==0)
{
alert('Wrong ticker');
}

  else{
  $('#txt_company_name').val(data[0].companyName);
  $('#txt_company_description').val(data[0].description);
  $('#txt_exchange').val(data[0].exchangeShortName);
  $('#txt_industry').val(data[0].industry);
  $('#txt_logo').val(data[0].image);
  $('#txt_ticker').val($('#txt_ticker').val().toUpperCase());

  $("#btn_submit").prop('disabled', false);
  }
})
}



