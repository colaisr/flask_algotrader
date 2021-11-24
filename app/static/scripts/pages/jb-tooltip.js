$(document).ready(function () {

    new jBox('Tooltip', {
      attach: '.jb-tooltip',
//      title: 'Test',
//      content: '<div style="font-weight: 900;">Test</div><div id="grabMe">Im your content. Remember to set CSS display to none!</div>',
      delayOpen: 500,
      delayClose: 1000,
//      theme:"TooltipDark", white
      closeOnMouseleave: !0,
    });

    $.getJSON("/research/get_tooltips", function(data) {
        $.each(data, function (index, val) {
            var content = '<div class="jb-tooltip-title" style="font-weight: 900;">' + val.short_name + ':' + val.title + '</div>' +
                      + '<div class="jb-tooltip-content">' + val.content + '</div>';
            if(val.url != null){
                content += '<div class="jb-tooltip-footer"><a href="' + val.url + '" target="_blank">More...</a></div>';
            }
            new jBox('Tooltip', {
              attach: '.jb-info-'+ val.id,
              content: content,
              delayOpen: 500,
              delayClose: 1000,
              closeOnMouseleave: !0,
              width: 200
            });
        })
    })
})

function create_info_tooltip(){

}