$(document).ready(function(){
paint_pnl()
set_connection_state()
setTimeout(function(){
   window.location.reload(1);
}, 30000);

})
function set_connection_state(){
el=$("#seconds_passed").val()
if(el>30){
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