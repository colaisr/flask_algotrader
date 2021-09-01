 $(document).ready(function () {

    $('.strategy-change').on('keyup keypress blur change', function(e) {
        $('#strategy_id').val('4')
        $('.strategy-btn').removeClass( "active" )
    })

//    $('.strategy-option').change(function(){
////            $.post("/algotradersettings/usersettings", {"strategy_id": $(this).val()});
//                alert("test")
//    });

//    $('[name=options]').on('change', function(e){
//        $.post("/algotradersettings/usersettings", {strategy_id:$(this).val()}).done(function (reply) {
//                alert ("test")
//        })
//    })
})

function Test(el){
    $.post("/algotradersettings/usersettings", {"strategy_id": $(el).val()}).done(function (reply) {
        var newDoc = document.open("text/html", "replace");
        newDoc.write(reply);
        newDoc.close();
    });

}

