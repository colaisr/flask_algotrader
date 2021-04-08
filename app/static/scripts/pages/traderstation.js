$(document).ready(function(){
paint_pnl()
set_connection_state()
setTimeout(function(){
   window.location.reload(1);
}, 30000);

})

function set_connection_state(){
el=$("#report_time").val()
interval=$("#report_interval").val()
time_report=Date.parse(el)
time_current=Date.now()
seconds_passed=(time_current-time_report)/1000
i=2
if(seconds_passed>(interval+5)){
el=$("#connection_state").addClass('badge-danger').removeClass('badge-success');
el=$("#connection_state").text("Offline");
}else{
el=$("#connection_state").addClass('badge-success').removeClass('badge-danger');
el=$("#connection_state").text("Online");
}


}
function paint_pnl() {
box_pnl=$(".box_pnl");
val_pnl=$(".val_pnl").html();
val_pnl=val_pnl.replace('$ ', '');
test=Math.sign(val_pnl);
if (test==-1) {
box_pnl.toggleClass('bg-grow-early bg-love-kiss');
}
}