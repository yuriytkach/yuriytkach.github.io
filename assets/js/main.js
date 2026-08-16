/* ==========================================================================
   Field Report — site behaviour
   Theme, navigation, hero parallax, lightbox.
   ========================================================================== */
(function () {
  'use strict';

  var root = document.documentElement;

  /* ----------------------------------------------------------------------
     Theme — three states: system (default), light, dark.
     The no-flash bootstrap in <head> has already applied the stored value;
     this wires up the toggle.
     ---------------------------------------------------------------------- */
  var THEMES = ['system', 'light', 'dark'];

  function applyTheme(pref) {
    root.setAttribute('data-theme-pref', pref);
    if (pref === 'system') {
      root.removeAttribute('data-theme');
    } else {
      root.setAttribute('data-theme', pref);
    }
    var btn = document.querySelector('.theme-toggle');
    if (btn) {
      btn.setAttribute('aria-label', 'Colour theme: ' + pref + '. Activate to change.');
      btn.setAttribute('title', 'Theme: ' + pref);
    }
  }

  function readTheme() {
    try {
      var v = localStorage.getItem('theme');
      return THEMES.indexOf(v) > -1 ? v : 'system';
    } catch (e) {
      return 'system';
    }
  }

  applyTheme(readTheme());

  var themeBtn = document.querySelector('.theme-toggle');
  if (themeBtn) {
    themeBtn.addEventListener('click', function () {
      var next = THEMES[(THEMES.indexOf(readTheme()) + 1) % THEMES.length];
      try { localStorage.setItem('theme', next); } catch (e) { /* private mode */ }
      applyTheme(next);
      document.dispatchEvent(new CustomEvent('themechange', { detail: { pref: next } }));
    });
  }

  /* ----------------------------------------------------------------------
     Navigation — mark the current page, and run the mobile sheet properly:
     closes on Escape, on outside click, on navigation and on resize.
     ---------------------------------------------------------------------- */
  var nav = document.getElementById('main-nav');
  var menuBtn = document.querySelector('.menu-toggle');

  var here = location.pathname.replace(/\/$/, '') || '/';
  if (nav) {
    Array.prototype.forEach.call(nav.querySelectorAll('a'), function (a) {
      var href = new URL(a.href, location.origin).pathname.replace(/\/$/, '') || '/';
      if (href === here) a.setAttribute('aria-current', 'page');
    });
  }

  if (menuBtn && nav) {
    var isOpen = function () { return nav.classList.contains('open'); };

    var setOpen = function (open, restoreFocus) {
      nav.classList.toggle('open', open);
      menuBtn.setAttribute('aria-expanded', String(open));
      document.body.style.overflow = open ? 'hidden' : '';
      if (open) {
        var first = nav.querySelector('a');
        if (first) first.focus();
      } else if (restoreFocus) {
        menuBtn.focus();
      }
    };

    menuBtn.addEventListener('click', function (e) {
      e.stopPropagation();
      setOpen(!isOpen(), true);
    });

    document.addEventListener('click', function (e) {
      if (isOpen() && !nav.contains(e.target) && e.target !== menuBtn) setOpen(false, false);
    });

    document.addEventListener('keydown', function (e) {
      if (e.key === 'Escape' && isOpen()) setOpen(false, true);
    });

    nav.addEventListener('click', function (e) {
      if (e.target.tagName === 'A') setOpen(false, false);
    });

    window.addEventListener('resize', function () {
      if (window.innerWidth > 760 && isOpen()) setOpen(false, false);
    });
  }

  /* ----------------------------------------------------------------------
     Hero parallax — off on small screens and under reduced motion.
     ---------------------------------------------------------------------- */
  var heroes = Array.prototype.slice.call(document.querySelectorAll('.hero-banner[data-parallax="hero"]'));
  if (heroes.length) {
    var reduceMotion = window.matchMedia('(prefers-reduced-motion: reduce)');
    var smallScreen = window.matchMedia('(max-width: 767px)');
    var ticking = false;

    var apply = function () {
      var off = reduceMotion.matches || smallScreen.matches;
      for (var i = 0; i < heroes.length; i++) {
        var hero = heroes[i];
        if (off) { hero.style.setProperty('--hero-shift', '0px'); continue; }
        var rect = hero.getBoundingClientRect();
        var vh = window.innerHeight || document.documentElement.clientHeight;
        var shift = Math.max(-18, Math.min(26, (vh - rect.top) * 0.08));
        hero.style.setProperty('--hero-shift', shift + 'px');
      }
      ticking = false;
    };

    var request = function () {
      if (ticking) return;
      ticking = true;
      window.requestAnimationFrame(apply);
    };

    window.addEventListener('scroll', request, { passive: true });
    window.addEventListener('resize', request);
    [reduceMotion, smallScreen].forEach(function (mq) {
      if (mq.addEventListener) mq.addEventListener('change', request);
      else if (mq.addListener) mq.addListener(request);
    });
    request();
  }

  /* ----------------------------------------------------------------------
     Lightbox — a real dialog: keyboard-openable, focus-trapped,
     restores focus on close.
     ---------------------------------------------------------------------- */
  var embedTriggers = Array.prototype.slice.call(document.querySelectorAll('[data-lightbox]'));
  var galleryImgs = Array.prototype.slice.call(document.querySelectorAll('.post-gallery-item img'));
  if (embedTriggers.length || galleryImgs.length) {
    var overlay = document.createElement('div');
    overlay.className = 'lightbox-overlay';
    overlay.setAttribute('role', 'dialog');
    overlay.setAttribute('aria-modal', 'true');
    overlay.setAttribute('aria-label', 'Enlarged image');
    overlay.innerHTML =
      '<button class="lightbox-close" type="button" aria-label="Close">&times;</button>' +
      '<div class="lightbox-content"></div>';
    document.body.appendChild(overlay);

    var content = overlay.querySelector('.lightbox-content');
    var closeBtn = overlay.querySelector('.lightbox-close');
    var lastFocused = null;

    var openBox = function (el) {
      lastFocused = el;
      content.innerHTML = '';
      var src = el.getAttribute('data-lightbox');
      if (src) {
        var em = document.createElement('embed');
        em.src = src;
        content.appendChild(em);
      } else if (el.tagName === 'IMG') {
        var img = document.createElement('img');
        img.src = el.currentSrc || el.src;
        img.alt = el.alt || '';
        content.appendChild(img);
      }
      overlay.classList.add('active');
      document.body.style.overflow = 'hidden';
      closeBtn.focus();
    };

    var closeBox = function () {
      overlay.classList.remove('active');
      document.body.style.overflow = '';
      content.innerHTML = '';
      if (lastFocused && lastFocused.focus) lastFocused.focus();
      lastFocused = null;
    };

    var makeTrigger = function (el) {
      if (!el.hasAttribute('tabindex')) el.setAttribute('tabindex', '0');
      if (!el.hasAttribute('role')) el.setAttribute('role', 'button');
      el.addEventListener('click', function () { openBox(el); });
      el.addEventListener('keydown', function (e) {
        if (e.key === 'Enter' || e.key === ' ') { e.preventDefault(); openBox(el); }
      });
    };

    embedTriggers.forEach(makeTrigger);
    galleryImgs.forEach(makeTrigger);

    overlay.addEventListener('click', function (e) {
      if (e.target === overlay || e.target === closeBtn) closeBox();
    });

    document.addEventListener('keydown', function (e) {
      if (!overlay.classList.contains('active')) return;
      if (e.key === 'Escape') { closeBox(); return; }
      /* trap focus: the close button is the only stop inside the dialog */
      if (e.key === 'Tab') { e.preventDefault(); closeBtn.focus(); }
    });
  }

  /* ----------------------------------------------------------------------
     Footer year
     ---------------------------------------------------------------------- */
  var yearEl = document.getElementById('year');
  if (yearEl) yearEl.textContent = String(new Date().getFullYear());
})();
