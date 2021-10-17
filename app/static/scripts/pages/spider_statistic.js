$(document).ready(function () {
    var status = get_spider_status();
    if(status == 1){
        var status_refresh = setInterval (function(){
            status = get_spider_status();
            if(status==0){
//                clearInterval(status_refresh);
                window.location.reload(1);
            }
        }, 40000);
    }


    $(".modal-btn").on("click", function(){
        $(".error-tickers-modal").modal("show");
        var data = $(this).attr("data");
        data = data.replaceAll("'",'"');
        json_data = JSON.parse(data);
        error_tickers = json_data["error_tickers"]
        research_error_tickers = json_data["research_error_tickers"]
        if(error_tickers.length > 0){
            $(".process-error").find(".item-content").html(error_tickers.join(", "))
            $(".process-error").show();
        }
        else{
            $(".process-error").hide();
        }
        if(research_error_tickers.length > 0){
            var str="";
            $.each(research_error_tickers, function( key, value ) {
                $.each(value, function(key, value){
                    str +=key + ": " + value.join(", ") + "; ";
                });
            });
            $(".research-error").find(".item-content").html(str);
            $(".research-error").show();
        }
        else{
            $(".research-error").hide();
        }
    })
});

function get_spider_status(){
    var status=1;
    $.ajax({
            url: '/admin/spider_status_ajax',
            async: false,   // this is the important line that makes the request sincronous
            type: 'get',
            dataType: 'json',
            success: function(data) {
                if(data != null){
                    var dateNow = (new Date()).toDateString();
                    $(".spider-date-status").text(dateNow);
                    var percent = data.percent;
                    var spider_status = data.status;
                    if(spider_status=="spider finished")
                    {
                        status = 0;
                        var date = new Date(data.start_process_date);
                        if(date.toDateString() != dateNow)
                        {
                            percent=0;
                            spider_status="";
                        }
                    }
                    $(".spider-percent").text(percent+"%");
                    $(".spider-progress-bar").attr("aria-valuenow", percent);
                    $(".spider-progress-bar").css( "width",percent+"%" )
                    $(".spider-status").text(spider_status);
                }
                else{
                    status = 0;
                }
            }
    });
    return status;
}