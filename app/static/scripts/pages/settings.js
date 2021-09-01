 $(document).ready(function () {

//    $('.strategy-change').on('keyup keypress blur change', function(e) {
//        $('#strategy_id').val('4')
//        $('.strategy-btn').removeClass( "active" )
//    })

    $('.strategy-option').change(function(){
            alert('Radio Box has been changed!');
        });

//    $('[name=options]').on('change', function(e){
//        $.post("/algotradersettings/usersettings", {strategy_id:$(this).val()}).done(function (reply) {
//                alert ("test")
//        })
//    })
})

function Test(){
 $.post("/algotradersettings/usersettings", {strategy_id:$(this).val()})
}

