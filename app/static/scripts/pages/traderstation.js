$(document).ready(function(){
//paint_pnl()
setTimeout(function(){
   window.location.reload(1);
}, 30000);

})

//$("#sectors_modal").on('shown', function (e) {
//  alert('rrrrr');
//})


//
//function paint_pnl() {
//box_pnl=$(".box_pnl");
//val_pnl=$(".val_pnl").html();
//val_pnl=val_pnl.replace('$ ', '');
//test=Math.sign(val_pnl);
//if (test==-1) {
//box_pnl.toggleClass('bg-grow-early bg-love-kiss');
//}
//}
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