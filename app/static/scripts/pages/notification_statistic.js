$(document).ready(function () {
//    var status = get_notification_status();
//    if(status == 1){
//        var status_refresh = setInterval (function(){
//            status = get_notification_status();
//            if(status==0){
////                clearInterval(status_refresh);
//                window.location.reload(1);
//            }
//        }, 10000);
//    }
    var status = get_notification_status();
    refresh_notification_bar(status);


    $('.run-notificaions').on('click', function(){
        setInterval (function(){
            get_notification_status();
        }, 5000);
        $.getJSON("/connections/notifications_process", function(data) {
                window.location.reload(1);
        })
    })

});

function refresh_notification_bar(status){
    var status_refresh = setInterval (function(){
        if(status==0){
            clearInterval(status_refresh);
//                window.location.reload(1);
        }
        status = get_notification_status();
    }, 5000);
}


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
                    var all_items = data.all_items;
                    var updated_items = data.updated_items;
                    var notification_status = data.status;
                    if(notification_status=="process finished")
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
                    $(".notif-sended").text(all_items);
                    $(".all-notif").text(updated_items);
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