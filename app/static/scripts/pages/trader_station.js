

$(document).ready(function(){
    var emotion_settings = parseInt($('#user-emotion').val());
    var user_email = $('#user_email').val();
    var main_snp = [];
    var main_emotion = [];
    var count_days_emotion = 0;
    fill_emotion_and_snp_graphs(emotion_settings, false, main_snp, main_emotion);


})


