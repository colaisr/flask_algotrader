var interval;

$(document).ready(function(){
    //paint_pnl()
//    setTimeout(function(){
//       window.location.reload(1);
//    }, 30000);

    interval_start();

    var emotion_settings = parseInt($('#user-emotion').val());
    var main_snp = [];
    var main_emotion = [];
    var count_days_emotion = 0;
    fill_emotion_and_snp_graphs(emotion_settings, false, main_snp, main_emotion);

    $('#user_emotion_box').click(function(){
        clearInterval(interval);
        $(".emotion-modal").show();
    });

    $('.emotion-modal-close').click(function(){
        $(".emotion-modal").hide();
//        interval_start();
        window.location.reload(1);
    });
})

function interval_start(){
    interval = setInterval(function(){
       window.location.reload(1);
    }, 30000);
}

function fill_graph(){
    $("#sectors_modal").modal("show");
    var ctx = document.getElementById('sectorsChart').getContext('2d');
    var myChart = new Chart(ctx, {
        type: 'pie',
        data: {
            labels: graph_sectors,
            datasets: [{
                label: '# of Votes',
                data: graph_sectors_values,
                backgroundColor: [
                    'rgba(255, 99, 132, 0.2)',
                    'rgba(54, 162, 235, 0.2)',
                    'rgba(255, 206, 86, 0.2)',
                    'rgba(75, 192, 192, 0.2)',
                    'rgba(153, 102, 255, 0.2)'

                ]
            }]
        },
    });
}

function go_to_cnn(){
    window.open("https://money.cnn.com/data/fear-and-greed/", "_blank");
}
