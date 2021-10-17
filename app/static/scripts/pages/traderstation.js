$(document).ready(function(){
    //paint_pnl()
    setTimeout(function(){
       window.location.reload(1);
    }, 30000);

    $('#user_emotion_box').click(function(){
        fill_emotion_data();
        $(".emotion-modal").show();
    });

    $('.emotion-modal-close').click(function(){
        $(".emotion-modal").hide();
    });
})

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
