function create_simple_tooltip(){
    new jBox('Tooltip', {
      attach: '.jb-tooltip',
      delayOpen: 500,
      delayClose: 1000,
    //      theme:"TooltipDark", white
      closeOnMouseleave: !0,
    });
}

function create_info_tooltip(tooltip_ids){
    var tooltips = get_tooltips(tooltip_ids);
    $.each(tooltips, function (index, val) {
        var content = '<div class="jb-tooltip-title" style="font-weight: 900;">' + val.short_name + ':' + val.title + '</div><div class="jb-tooltip-content">' + val.content + '</div>';
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
}

function get_tooltips(ids){
    return TOOLTIPS.filter(x => ids.indexOf(x.id) >= 0);
}