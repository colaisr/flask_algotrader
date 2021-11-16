$(document).ready(function () {

    $(window).resize(function() {
        var width = $(this).width() - 100;
        var height = $(this).height() - 400;
        var big_height = $(this).height() - 150;
        $('.modal-bigger').css('max-width', width);
        $('.height-resize').css('height',height);
        $('.big-height-resize').css('height',big_height);

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
            $('.searchable tbody td:icontains(' + searchText + ')').addClass('positive');
            $('.searchable td.positive').not(':icontains(' + searchText + ')').removeClass('positive');
            $('.searchable tbody td').not(':icontains(' + searchText + ')').closest('tr').addClass('hidden').hide();
            $('.searchable tr.hidden:icontains(' + searchText + ')').removeClass('hidden').show();
        } else {
            $('.searchable td.positive').removeClass('positive');
            $('.searchable tr.hidden').removeClass('hidden').show();
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

function add_row_to_personal_candidates(c, tbl_class, is_modal){
    var score = c.algotrader_rank || 0;
    var under_priced_pnt = c.under_priced_pnt != null ? c.under_priced_pnt.toFixed(2) : 0;
    var twelve_month_momentum = c.twelve_month_momentum != null ? c.twelve_month_momentum.toFixed(2) : 0;
    var beta = c.beta != null ? c.beta.toFixed(2) : 0;
    var max_intraday_drop_percent = c.max_intraday_drop_percent != null ? c.max_intraday_drop_percent.toFixed(2) : 0;
    var tr = $('<tr title="' + c.reason + '"></tr>');
    var td_logo =$('<td class="text-center"><img src="' + c.logo + '" width="20" height="20"></td>');
    tr.append(td_logo);
    var td_company = $('<td><a href="/candidates/info/' + c.ticker + '">' + c.ticker + '</a><div class="text-small">' + c.company_name + '</div></td>');
    tr.append(td_company);
    if(is_modal){
        var td_remove = $('<td class="text-center"><button id="remove-' + c.ticker +'" type="submit" data-ticker="' + c.ticker + '" class="bord-none remove-candidate"><i class="fa fa-trash"></i></button></td>');
        tr.append(td_remove);
        var td_edit = $('<td class="text-center"><button class="btn_edit bord-none" id="edit-' + c.ticker + '"><i class="fa fa-edit mt-1"></i></button><input type="hidden" class="h_tick" value="' + c.ticker + '"><input type="hidden" class="h_reason" value="' + c.reason + '"></td>');
        tr.append(td_edit);
        var td_enabled = $('<td class="text-center"><input class="mt-2 enable-checkbox" id="enabled-' + c.ticker + '" data-ticker="' + c.ticker + '" type="checkbox"></td>');
        tr.append(td_enabled);
    }
    var td_score = $('<td class="text-center">'+score+'</td>');
    tr.append(td_score);
    var td_sector = $('<td class="text-small">' + c.sector + '</td>');
    tr.append(td_sector);
    var td_under_price = $('<td class="text-center">' + under_priced_pnt + '</td>');
    tr.append(td_under_price);
    var td_momentum = $('<td class="text-center">' + twelve_month_momentum + '</td>');
    tr.append(td_momentum);
    var td_beta = $('<td class="text-center">' + beta + '</td>');
    tr.append(td_beta);
    var td_intraday_drop = $('<td class="text-center">' + max_intraday_drop_percent + '</td>');
    tr.append(td_intraday_drop);
    $('.' + tbl_class + ' tbody').append(tr);
    $('#enabled-' + c.ticker).prop('checked', c.enabled);
}

function draw_user_candidates_tbl(data){
    $('.personal-tbl tbody').empty();
    $('.personal-modal-tbl tbody').empty();
    $.each(data, function( index, c ){
        if(parseInt(index) < 5){
            add_row_to_personal_candidates(c, 'personal-tbl', false)       //from base.js
        }
        add_row_to_personal_candidates(c, 'personal-modal-tbl', true)       //from base.js
        $('#remove-' + c.ticker).on('click',remove_candidate);
        $('#enabled-' + c.ticker).on('click',change_enabled);
        $('#edit-' + c.ticker).on('click',edit_candidate);
    })
}

function upload_personal_list(){
    loading('personal-list-card-body');
    url = '/candidates/user_candidates';
    $.getJSON(url, function(data) {
        draw_user_candidates_tbl(data); //from base.js
        stop_loading('personal-list-card-body');
    });
}

function loading(parrent_div){
    $('.' + parrent_div + ' .div-content').css('opacity', 0.2);
    var height = $('.' + parrent_div).height();
    $('.' + parrent_div + ' .div-loading').css('height', height);

    $('.' + parrent_div + ' .div-loading').prop('hidden',false);
}

function stop_loading(parrent_div){
    $('.' + parrent_div + ' .div-content').css('opacity', 1);
    $('.' + parrent_div + ' .div-loading').prop('hidden',true);
}




