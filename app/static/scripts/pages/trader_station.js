

$(document).ready(function(){
    var emotion_settings = parseInt($('#user-emotion').val());
    var user_email = $('#user-email').val();
    var main_snp = [];
    var main_emotion = [];
    var count_days_emotion = 0;
    fill_emotion_and_snp_graphs(emotion_settings, false, main_snp, main_emotion);
    refresh_candidates_list(user_email);


})

function refresh_candidates_list(user_email){
    loading('candidates-table');
    url = '/connections/get_fitered_candidates_for_user';
    $.get(url,{ user: user_email}, function(data) {
        if(data.length >0){
        $('.candidates-table').empty();
        $('.candidates-table').append(data);
        }
        stop_loading('candidates-table');
    });
}

