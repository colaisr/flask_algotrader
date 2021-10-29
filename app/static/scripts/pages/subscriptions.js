$(document).ready(function () {

    $(".registration").click(function(){
        var subcription = $(this).data("value");
        $.post("/account/register",{subcription: subcription}, function(data) {

        });
    });
})