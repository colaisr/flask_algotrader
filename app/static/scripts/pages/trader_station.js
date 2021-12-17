
var user_email;
var user_type;
$(document).ready(function(){
    var emotion_settings = parseInt($('#user-emotion').val());
    user_email = $('#user-email').val();
    user_type = $('#user-type').val();
    var main_snp = [];
    var main_emotion = [];
    var count_days_emotion = 0;
    fill_emotion_and_snp_graphs(emotion_settings, false, main_snp, main_emotion);
    refresh_candidates_list(user_email);
    if(user_type==2){
    refresh_favorites_list(user_email);
    }
    else{
    refresh_positions_list(user_email)
    }
    interval_start();



})

function interval_start(){
    interval = setInterval(function(){
    refresh_candidates_list(user_email);
    if(user_type==2){
    refresh_favorites_list(user_email);
    }
    else{
    refresh_positions_list(user_email)
    }
    }, 15000);
}

function refresh_candidates_list(user_email){
    loading('candidates-table');
    url = '/connections/get_fitered_candidates_for_user';
    $.get(url,{ user: user_email}, function(data) {
        if(data.length >0){
        $('.candidates-table').empty();
        $('.candidates-table').append(data);

        // Define value names
        var table_filters = { valueNames: [ 'ticker', 'price', 'target','score','underpriced','momentum','beta' ] };

        // Init list
        var overviewList = new List('filtered_candidates_table', table_filters);
        }
        stop_loading('candidates-table');
    });
}
function refresh_favorites_list(user_email){
    loading('favorites-table');
    url = '/connections/get_favorites_for_user';
    $.get(url,{ user: user_email}, function(data) {
        if(data.length >0){
        $('.favorites-table').empty();
        $('.favorites-table').append(data);

//        // Define value names
//        var table_filters = { valueNames: [ 'ticker', 'price', 'target','score','underpriced','momentum','beta' ] };
//
//        // Init list
//        var overviewList = new List('filtered_candidates_table', table_filters);
        }
        stop_loading('favorites-table');
    });
}
function refresh_positions_list(user_email){
    loading('favorites-table');
    url = '/connections/get_positions_for_user';
    $.get(url,{ user: user_email}, function(data) {
        if(data.length >0){
        $('.positions-table').empty();
        $('.positions-table').append(data);

//        // Define value names
//        var table_filters = { valueNames: [ 'ticker', 'price', 'target','score','underpriced','momentum','beta' ] };
//
//        // Init list
//        var overviewList = new List('filtered_candidates_table', table_filters);
        }
        stop_loading('favorites-table');
    });
}

