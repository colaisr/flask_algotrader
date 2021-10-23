$(document).ready(function () {
    $(window).resize(function() {
        var width = $(this).width() - 100;
        var height = $(this).height() - 400;
        $('.modal-bigger').css('max-width', width);
        $('.height-resize').css('height',height);
    }).resize();

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

function flashMessage (type, message){
  var html = '<div class="alert alert-' + type + ' text-center"><a href="#" class="close" data-dismiss="alert">&times;</a>' + message + '</div>';
  return html;
};

function range_set_value(rangeid,range_v_id){
    var range = $('#'+rangeid);
    var rangeV = $('#'+range_v_id);
    var value = parseFloat(range.val());
    var max = parseFloat(range.prop('max'));
    var min = parseFloat(range.prop('min'));

    var newValue = (value - min) * 100 / (max - min);
    var newPosition = 10 - (newValue * 0.2);
    rangeV.html('<span>' + value + '</span>');
    rangeV.css('left','calc(' + newValue + '% + (' + newPosition + 'px))');
}

function isFloat(n){
    return Number(n) === n && n % 1 !== 0;
}




