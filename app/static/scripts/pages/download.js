$(document).ready(function () {
    $('#signature_full_name').on('input', function(e) {
        var signature_full_name = $('#signature_full_name').val();
        if(signature_full_name.length >0
            && signature_full_name.trim() != ''
            && signature_full_name.trim().split(' ').length > 1
            && signature_full_name.trim().split(' ')[signature_full_name.trim().split(' ').length-1].trim() != ''){
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