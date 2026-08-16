/* ==========================================================================
   Volunteering index — language filter.
   The list itself is rendered into the HTML at build time (tools/build.py),
   so it works, and is indexable, with JavaScript switched off.
   ========================================================================== */
(function () {
  'use strict';

  var toolbar = document.querySelector('.post-toolbar');
  if (!toolbar) return;

  var buttons = Array.prototype.slice.call(toolbar.querySelectorAll('.filter-btn'));
  var counter = toolbar.querySelector('.post-count');
  var cards = Array.prototype.slice.call(document.querySelectorAll('.post-card'));
  var years = Array.prototype.slice.call(document.querySelectorAll('.post-year'));
  var grids = Array.prototype.slice.call(document.querySelectorAll('.post-grid'));

  function label(n) {
    return n + (n === 1 ? ' report' : ' reports');
  }

  function apply(lang) {
    var shown = 0;

    cards.forEach(function (card) {
      var match = lang === 'all' || card.getAttribute('data-lang') === lang;
      card.hidden = !match;
      if (match) shown++;
    });

    /* hide a year heading when its whole group filtered out */
    grids.forEach(function (grid, i) {
      var any = Array.prototype.some.call(grid.querySelectorAll('.post-card'), function (c) {
        return !c.hidden;
      });
      grid.hidden = !any;
      if (years[i]) years[i].hidden = !any;
    });

    /* aria-pressed carries the state for assistive tech; the class carries the
       styling, because attribute-selector restyling did not repaint reliably */
    buttons.forEach(function (b) {
      var on = b.getAttribute('data-lang') === lang;
      b.setAttribute('aria-pressed', String(on));
      b.classList.toggle('is-on', on);
    });

    if (counter) counter.textContent = label(shown);

    try { history.replaceState(null, '', lang === 'all' ? location.pathname : '?lang=' + lang); }
    catch (e) { /* file:// */ }
  }

  buttons.forEach(function (b) {
    b.addEventListener('click', function () { apply(b.getAttribute('data-lang')); });
  });

  var initial = new URLSearchParams(location.search).get('lang');
  apply(initial === 'en' || initial === 'uk' ? initial : 'all');
})();
