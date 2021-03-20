

$('.btn_edit').on('click', function() {
i=2;
clicked_on=event.target.parentElement;

ticker=$(clicked_on).siblings('.h_tick')[0].value;
descript=$(clicked_on).siblings('.h_desc')[0].value;
$('#txt_ticker').val(ticker);
//$('#add_candidate_modal').appendTo("body").modal('toggle');
$('#add_candidate_modal').modal('toggle');

})


$(document).ready(function(){


})

function rebase_modals(){


}
