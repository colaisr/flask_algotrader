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

function add_row_to_personal_candidates(c, market_data, tbl_class, is_modal){
    var score = 0;
    var under_priced_pnt = 0;
    var twelve_month_momentum = 0;
    var beta = 0;
    var max_intraday_drop_percent = 0;
    if(market_data[c.ticker] != undefined){
        score = market_data[c.ticker].algotrader_rank || 0;
        under_priced_pnt = market_data[c.ticker].under_priced_pnt.toFixed(2) || 0;
        twelve_month_momentum = market_data[c.ticker].twelve_month_momentum.toFixed(2) || 0;
        beta = market_data[c.ticker].beta.toFixed(2) || 0;
        max_intraday_drop_percent = market_data[c.ticker].max_intraday_drop_percent.toFixed(2) || 0;
    }
    var tr = $('<tr title="' + c.reason + '></tr>');
    var td_logo =$('<td class="text-center"><img src="' + c.logo + '" width="20" height="20"></td>');
    tr.append(td_logo);
    var td_company = $('<td><a href="/candidates/info?ticker_to_show=' + c.ticker + '">' + c.ticker + '</a><div class="text-small">' + c.company_name + '</div></td>');
    tr.append(td_company);
    if(is_modal){
        var td_remove = $('<td class="text-center"><button id="remove-' + c.ticker +'" type="submit" data-ticker="' + c.ticker + '" class="bord-none remove-candidate"><i class="fa fa-trash"></i></button></td>');
        tr.append(td_remove);
        var td_edit = $('<td class="text-center"><button class="btn_edit bord-none"><i class="fa fa-edit mt-1"></i></button><input type="hidden" class="h_tick" value="' + c.ticker + '"><input type="hidden" class="h_reason" value="' + c.reason + '"></td>');
        tr.append(td_edit);
        var td_enabled = $('<td class="text-center"><input class="mt-2 enable-checkbox" id="enabled-' + c.ticker + '" data-ticker="' + c.ticker + '" type="checkbox" onChange="change_enabled()"></td>');
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




