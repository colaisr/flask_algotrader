$(document).ready(function () {

    $('#submit').addClass('disabled');

    $('#terms_agree').click(function(){
        if ($(this).is(':checked')){
            $('#submit').removeClass('disabled');
        } else {
            $('#submit').addClass('disabled');
        }
    });

})