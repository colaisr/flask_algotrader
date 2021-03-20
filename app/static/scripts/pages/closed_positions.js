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
})