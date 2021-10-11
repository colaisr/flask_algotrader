$(document).ready(function () {
    get_spider_status();
    setTimeout(function(){
        get_spider_status();
    }, 50000);

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

    $.get("/admin/spider_status_ajax", function(data) {
                var data_parsed = jQuery.parseJSON(data);

                $(".spider-status").text(data_parsed.status);
                $(".spider-percent").text(data_parsed.percent+"%");
                $(".spider-progress-bar").attr("aria-valuenow", data_parsed.percent);
                $(".spider-progress-bar").css( "width",data_parsed.percent+"%" )
            });

}