$(document).ready(function () {


});

$(".search-input").on("input", function() {
   get_search_results($(this).val());
});

function get_search_results(text_to_search){
$.getJSON( "https://colak.eu.pythonanywhere.com/data_hub/search_quick/"+text_to_search, function( data ) {

  $( ".search-suggested" ).remove();
  $.each( data, function( key, val ) {

    $( "#search_results" ).append(
     '<a class="search-suggested dropdown-item px-card py-2" href="/candidates/info/' + val["symbol"] + '"><div class="d-flex align-items-center"><div class="avatar avatar-l status-online me-2"><img class="rounded-circle" src="assets/img/team/1.jpg" alt="" /></div><div class="flex-1"><h6 class="mb-0 title">'+val["symbol"]+'</h6><p class="fs--2 mb-0 d-flex">'+val["name"]+'</p></div></div></a>'
     );
  });
  b=2

});
}


function isFloat(n){
    return Number(n) === n && n % 1 !== 0;
}