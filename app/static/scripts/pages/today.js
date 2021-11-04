 $(document).ready(function () {
    candidates =jQuery.parseJSON(candidates);
    market_data =jQuery.parseJSON(market_data);
    var emotion_settings = parseInt($('#user-emotion').val());
    var main_snp = [];
    var main_emotion = [];
    var count_days_emotion = 0;
    fill_emotion_and_snp_graphs(emotion_settings, false, main_snp, main_emotion);

    $('.show_signals_modal').click(function(){
        $(".signals_modal").show();
    });

    $('.signals-modal-close').click(function(){
        $(".signals_modal").hide();
    });

    $('.show_personal_modal').click(function(){
        $(".personal_modal").show();
    });

    $('.personal-modal-close').click(function(){
        $(".personal_modal").hide();
    });

    $('.show_improovers_modal').click(function(){
        $(".improovers_modal").show();
    });

    $('.improovers-modal-close').click(function(){
        $(".improovers_modal").hide();
    });


    $('#today_emotion_box').click(function(){
        $(".emotion-modal").show();
    });

    $('.emotion-modal-close').click(function(){
        $(".emotion-modal").hide();
    });

// creating a candidate
    $('#btnAddCandidate').on('click', function() {
        $('#candidate-flash').empty();
        $('.content-hidden').prop('hidden',true);
        $('.modal-body input, .modal-body textarea').val("");
        $("#btn_submit").prop('disabled', true);
        $('#user-email').val($('#user_email').val());
        $("#add_candidate_modal").show();
    })

    $('.btn-modal-hide').on('click', function() {
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

    $('.remove-candidate').on('click',function(){
        var ticker = $(this).data('ticker');
        $.post("/candidates/removecandidate_ajax",{ticker: ticker}, function(data) {
            var data_parsed = jQuery.parseJSON(data);
            if(data_parsed["result"]){
                $('.personal-modal-tbl tbody td:icontains(' + ticker + ')').closest('tr').remove();
                if($('.personal-tbl tbody td:icontains(' + ticker + ')').length > 0){
                    $('.personal-tbl tbody').empty();
                    var candidates_updated = $.grep( candidates, function( n, i ) { return n.ticker == ticker;},true);
                    var top_candidates = candidates_updated.slice(0,5);
                    $.each(top_candidates, function( index, c ){
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
                        var tr = $('<tr></tr>');
                        var td_logo =$('<td class="text-center"><img src="' + c.logo + '" width="20" height="20"></td>');
                        tr.append(td_logo);
                        var td_company = $('<td><a href="/candidates/info?ticker_to_show=' + c.ticker + '">' + c.ticker + '</a><div class="text-small">' + c.company_name + '</div></td>');
                        tr.append(td_company);
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
                        $('.personal-tbl tbody').append(tr);
                    })
                }
            }
        });
    })


    $('#txt_ticker, #txt_reason').on('input',function(){
        $('#candidate-flash').empty();
    });

})



