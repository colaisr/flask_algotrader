$(document).ready(function () {


});
$("#header_search").submit(function(e){
   active_items=$("#search_results > a.search-suggested.dropdown-item.active.px-card.py-2")
   if(active_items.length>0){
   target=active_items[0].href
   window.location.href = target;
   }
   else{
   //alert( "Handler for .submit() called." );    test only - will do nothing
   }
    return false;
});

$(".search-input").on("input", function() {
   get_search_results($(this).val());
});

function get_search_results(text_to_search){
$.getJSON( "https://colak.eu.pythonanywhere.com/data_hub/search_quick/"+text_to_search, function( data ) {

  $( ".search-suggested" ).remove();
  $.each( data, function( key, val ) {
    if(key==0)
    {
        $( "#search_results" ).append(
     '<a class="search-suggested dropdown-item active px-card py-2" href="/candidates/info/' + val["symbol"] + '"><div class="d-flex align-items-center"><div class="flex-1"><h6 class="mb-0 title">'+val["symbol"]+'</h6><p class="fs--2 mb-0 d-flex">'+val["name"]+'</p></div></div></a>'
     );
    }else{
    $( "#search_results" ).append(
     '<a class="search-suggested dropdown-item px-card py-2" href="/candidates/info/' + val["symbol"] + '"><div class="d-flex align-items-center"><div class="flex-1"><h6 class="mb-0 title">'+val["symbol"]+'</h6><p class="fs--2 mb-0 d-flex">'+val["name"]+'</p></div></div></a>'
     );
     }
  });
});
//$(".search-suggested")[0].addClass('dropdown-item.active');
}


function isFloat(n){
    return Number(n) === n && n % 1 !== 0;
}