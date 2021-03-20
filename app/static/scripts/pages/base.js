  $('.message').each((i, el) => {
    const $el = $(el);
    const $xx = $el.find('.close');
    const sec = $el.data('autohide');
    const triggerRemove = () => clearTimeout($el.trigger('remove').T);

    $el.one('remove', () => $el.remove());
    $xx.one('click', triggerRemove);
    if (sec) $el.T = setTimeout(triggerRemove, sec * 1000);
  });

