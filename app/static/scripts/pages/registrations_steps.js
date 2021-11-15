$(document).ready(function () {

    $('input').on('input',function(){
        $("#data-changed").val("1");
    });

    $('.station-login-btn').on('click',function(){
        $( "#station-login-form" ).submit();
    });

})