 $(document).ready(function () {

    $('.strategy-change').on('keyup keypress blur change', function(e) {
        $('#strategy_id').val('4')
        $('.strategy-btn').removeClass( "active" )
    })

     $('#first_name_signature, #last_name_signature').on('keyup keypress blur change', function(e) {
        var first_name_signature = $('#first_name_signature').val();
        var last_name_signature = $('#last_name_signature').val();
        if(first_name_signature.length >0
            && last_name_signature.length >0
            && first_name_signature.trim() != ''
            && last_name_signature.trim() != ''){

           $('#signature').prop("disabled", false)
        }
        else{
            $('#signature').prop('checked', false);
            $('#signature').prop("disabled", true)
            $('#signature-submit').prop("disabled", true)
        }

        $("#signature").change(function() {
            if(this.checked) {
                $('#signature-submit').prop("disabled", false)
            }
            else{
                $('#signature-submit').prop("disabled", true)
            }
        });
    })

})

function UpdateDefaultStrategy(el){
    $.post("/algotradersettings/usersettings", {"strategy_id": $(el).val()}).done(function (reply) {
        var newDoc = document.open("text/html", "replace");
        newDoc.write(reply);
        newDoc.close();
    });

}

