$(document).ready(function () {

//    alert (width + ' x ' + height);

    $(window).resize(function() {
        var width = $(this).width() - 100;
        var height = $(this).height() - 400;
        $('.modal-bigger').css('max-width', width);
        $('.height-resize').css('height',height);

//        var dpi_x = document.getElementById('dpi').offsetWidth;
//        var dpi_y = document.getElementById('dpi').offsetHeight;
//        var width = screen.width / dpi_x;
//        var height = screen.height / dpi_y;
        var screen_width = screen.width;
        var screen_height = screen.height;
        if(screen_width >= 1500 && screen_height >= 900){
            $('.main-page-styles').remove();
            $( "<link class='main-page-styles' rel='stylesheet' href='/static/styles/mainpage_max.css'>" ).appendTo( "head" );
        }
        else if(screen_width > 767 && screen_width < 1400 && screen_height <= 800){
            $('.main-page-styles').remove();
            $( "<link class='main-page-styles' rel='stylesheet' href='/static/styles/mainpage_min.css'>" ).appendTo( "head" );
        }
        else if(screen_width >= 307 && screen_width <= 767){
            $('.main-page-styles').remove();
            $( "<link class='main-page-styles' rel='stylesheet' href='/static/styles/mainpage_mobile.css'>" ).appendTo( "head" );
            $('.mobile-hidden').prop('hidden', true);
        }
        else{
            $('.main-page-styles').remove();
            $( "<link class='main-page-styles' rel='stylesheet' href='/static/styles/mainpage.css'>" ).appendTo( "head" );
        }

    }).resize();

});






