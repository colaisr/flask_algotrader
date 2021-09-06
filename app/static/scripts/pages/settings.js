 $(document).ready(function () {

    $('.strategy-change').on('keyup keypress blur change', function(e) {
        $('#strategy_id').val('4')
        $('.strategy-btn').removeClass( "active" )
    })

})

function UpdateDefaultStrategy(el){
    $.post("/algotradersettings/usersettings", {"strategy_id": $(el).val()}).done(function (reply) {
        var newDoc = document.open("text/html", "replace");
        newDoc.write(reply);
        newDoc.close();
    });

}

