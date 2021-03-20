 $(document).ready(function () {
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

//        $('.modal-dialog').parent().on('show.bs.modal', function(e){        $(e.relatedTarget.attributes['data-target'].value).appendTo('body'); })
})

$('.btn_edit').on('click', function() {
i=2;
clicked_on=event.target.parentElement;

ticker=$(clicked_on).siblings('.h_tick')[0].value;
descript=$(clicked_on).siblings('.h_desc')[0].value;
$('#txt_ticker').val(ticker);
//$('#add_candidate_modal').appendTo("body").modal('toggle');
$('#add_candidate_modal').modal('toggle');

})


