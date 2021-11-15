$(document).ready(function () {
    if($('#terms_agree').is(':checked')){
        $('#submit').removeClass('disabled');
    }
    else{
        $('#submit').addClass('disabled');
    }

    $('#terms_agree').click(function(){
        if ($(this).is(':checked')){
            $('#submit').removeClass('disabled');
        } else {
            $('#submit').addClass('disabled');
        }
    });

})