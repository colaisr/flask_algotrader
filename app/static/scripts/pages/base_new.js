var SPYDER_API = 'https://colak.eu.pythonanywhere.com/';
if(window.location.hostname == '127.0.0.1'){
    SPYDER_API = 'http://localhost:8000/';
}

$(document).ready(function () {
    $('.toasts-block').empty();

    $(".search-form").submit(function(e){
    var id = $(this).id();
    active_items=$("#"+ id + " .search_results > a.search-suggested.dropdown-item.active.px-card.py-2")
    if(active_items.length>0){
        target=active_items[0].href
        window.location.href = target;
    }
    else{
        //alert( "Handler for .submit() called." );    test only - will do nothing
    }
    return false;
});

    $(".search-form .search-input").on("input", function() {
        var parent_id = $(this).parent().attr('id');
        get_search_results($(this).val(), parent_id);
    });
});



function get_search_results(text_to_search, parent_id){
    if(!isStringEmpty(text_to_search)){
        $.getJSON( SPYDER_API + "data_hub/search/"+text_to_search, function( data ) {
            $( ".search-suggested" ).remove();

            if(data.length == 0){
                $("." + parent_id + ".fallback").removeClass('d-none');
            }
            else{
                $("." + parent_id + ".fallback").addClass('d-none');
                if(parent_id == 'modal-search'){
                    $.each( data, function( key, val ) {
                    if(key==0){
                        $( "#" + parent_id + "-results" ).append(
                            '<li id="' + val["symbol"] + '" class="search-suggested dropdown-item active px-card py-2"><div class="d-flex align-items-center"><div class="flex-1"><h6 class="mb-0 title">'+val["symbol"]+'</h6><p class="fs--2 mb-0 d-flex">'+val["name"]+'</p></div></div></li>'
                        );
                        $('#' + val["symbol"]).on('click',set_value_to_search);
                    }
                    else{
                        $( "#" + parent_id + "-results" ).append(
                            '<li id="' + val["symbol"] + '" class="search-suggested dropdown-item px-card py-2"><div class="d-flex align-items-center"><div class="flex-1"><h6 class="mb-0 title">'+val["symbol"]+'</h6><p class="fs--2 mb-0 d-flex">'+val["name"]+'</p></div></div></li>'
                        );
                        $('#' + val["symbol"]).on('click',set_value_to_search);
                    }
                });
                }
                else{
                    $.each( data, function( key, val ) {
                    if(key==0){
                        $( "#" + parent_id + "-results" ).append(
                            '<a class="search-suggested dropdown-item active px-card py-2" href="/candidates/info/' + val["symbol"] + '"><div class="d-flex align-items-center"><div class="flex-1"><h6 class="mb-0 title">'+val["symbol"]+'</h6><p class="fs--2 mb-0 d-flex">'+val["name"]+'</p></div></div></a>'
                        );
                    }
                    else{
                        $( "#" + parent_id + "-results" ).append(
                            '<a class="search-suggested dropdown-item px-card py-2" href="/candidates/info/' + val["symbol"] + '"><div class="d-flex align-items-center"><div class="flex-1"><h6 class="mb-0 title">'+val["symbol"]+'</h6><p class="fs--2 mb-0 d-flex">'+val["name"]+'</p></div></div></a>'
                        );
                    }
                });
                }
            }
        });
    }
    //$(".search-suggested")[0].addClass('dropdown-item.active');
}

function set_value_to_search(){
    var ticker = $(this).attr('id');
    $('#modal-search .search-input').val(ticker);
    get_ticker_info(ticker);
}

function get_ticker_info(ticker){
    $('.candidate-bottom').prop('hidden', true);
    $('#btn-submit').addClass('disabled');
    if(isStringEmpty(ticker)){
        create_toast('danger', 'Error', 'Ticker is must!');
    }
    else{
        url = SPYDER_API + 'research/get_info_ticker/' + ticker
        $.getJSON(url, function(data) {
            if (data.length == 0 ||
                data.cik == undefined ||
                data.cik == null ||
                data.cik=="" ||
                data.isEtf ||
                !data.isActivelyTrading) //etfs and funds have no cik //cik - num of company
            {
                create_toast('danger', 'Error', 'Not Actively traded stock');
            }
            else{
                $('.dropdown-menu').removeClass('show');
                $('#txt_company_name').val(data.companyName);
                $('#txt_company_description').val(data.description);
                $('#txt_exchange').val(data.exchange);
                $('#txt_industry').val(data.industry);
                $('#txt_sector').val(data.sector);
                $('.candidate-bottom').prop('hidden',false);
                $('#btn-submit').removeClass('disabled');
            }
        })
    }
}

function isFloat(n){
    return Number(n) === n && n % 1 !== 0;
}

function isStringEmpty(str){
    return str.trim() == '' || str == null || str == undefined;
}


function loading(parrent_div, opacity){
    if(opacity == undefined){opacity = 0.2;}
    $('.' + parrent_div + ' .div-content').css('opacity', opacity);
    var height = $('.' + parrent_div).height();
    $('.' + parrent_div + ' .div-loading').css('height', height);

    $('.' + parrent_div + ' .div-loading').prop('hidden',false);
}

function stop_loading(parrent_div){
    $('.' + parrent_div + ' .div-content').css('opacity', 1);
    $('.' + parrent_div + ' .div-loading').prop('hidden',true);
}


function create_toast(header_color, title, message, time_str=''){
    /*
        time_str = '11 mins ago'
        header_color = 'success'
    */
    var count_toasts = $('.toast').length;
    var id = count_toasts + 1;
    var toast = $('<div class="toast fade" id="toast-' + id + '" role="alert" aria-live="assertive" aria-atomic="true"></div>');
    var toast_header = $('<div class="toast-header bg-' + header_color + ' bg-opacity-25 text-white"><strong class="me-auto">' + title + '</strong><small>' + time_str + '</small></div>');
    var close_btn = $('<button class="btn-close btn-close-white" type="button" data-bs-dismiss="toast" aria-label="Close"></button>');
    var toast_message = $('<div class="toast-body">' + message + '</div>');
    toast_header.append(close_btn);
    toast.append(toast_header);
    toast.append(toast_message);
    $('.toasts-block').append(toast);
    toast.toast('show');
}

function go_to_cnn(){
    window.open("https://money.cnn.com/data/fear-and-greed/", "_blank");
}
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
