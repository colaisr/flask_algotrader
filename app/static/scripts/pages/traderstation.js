$(document).ready(function(){
paint_pnl()
set_connection_state()
setTimeout(function(){
   window.location.reload(1);
}, 30000);

})



function paint_pnl() {
box_pnl=$(".box_pnl");
val_pnl=$(".val_pnl").html();
val_pnl=val_pnl.replace('$ ', '');
test=Math.sign(val_pnl);
if (test==-1) {
box_pnl.toggleClass('bg-grow-early bg-love-kiss');
}
}