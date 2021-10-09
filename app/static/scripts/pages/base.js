$(document).ready(function () {
    $('.message').each((i, el) => {
        const $el = $(el);
        const $xx = $el.find('.close');
        const sec = $el.data('autohide');
        const triggerRemove = () => clearTimeout($el.trigger('remove').T);

        $el.one('remove', () => $el.remove());
        $xx.one('click', triggerRemove);
        if (sec) $el.T = setTimeout(triggerRemove, sec * 1000);
    });
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

    $('#select-role').dropdown({
        onChange: function (value, text, $selectedItem) {
            $('td.user.role:contains(' + value + ')').closest('tr').removeClass('hidden').show();
            $('td.user.role').not(':contains(' + value + ')').closest('tr').addClass('hidden').hide();
        }
    });
});


