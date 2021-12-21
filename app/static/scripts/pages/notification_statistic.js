$(document).ready(function () {
    var status = get_notification_status();
    if(status == 1){
        var status_refresh = setInterval (function(){
            status = get_notification_status();
            if(status==0){
//                clearInterval(status_refresh);
                window.location.reload(1);
            }
        }, 40000);
    }

});

function get_notification_status(){
    var status=1;
    $.ajax({
            url: '/admin/notification_status_ajax',
            async: false,   // this is the important line that makes the request sincronous
            type: 'get',
            dataType: 'json',
            success: function(data) {
                if(data != null){
                    var dateNow = (new Date()).toDateString();
                    $(".notification-date-status").text(dateNow);
                    var percent = data.percent;
                    var notification_status = data.status;
                    if(notification_status=="notifications finished")
                    {
                        status = 0;
                        var date = new Date(data.start_process_date);
                        if(date.toDateString() != dateNow)
                        {
                            percent=0;
                            notification_status="";
                        }
                    }
                    $(".notification-percent").text(percent+"%");
                    $(".notification-progress-bar").attr("aria-valuenow", percent);
                    $(".notification-progress-bar").css( "width",percent+"%" )
                    $(".notification-status").text(notification_status);
                }
                else{
                    status = 0;
                }
            }
    });
    return status;
}