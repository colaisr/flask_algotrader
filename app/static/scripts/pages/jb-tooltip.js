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
        var title = val.title != null ? ': ' + val.title : '';
        var content = '<div class="jb-tooltip-title fw-bold">' + val.short_name + title + '</div><div class="jb-tooltip-content fs--1">' + val.content + '</div>';
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

