const btn = document.querySelector('.menu-toggle');
const nav = document.getElementById('main-nav');
if (btn && nav) {
  btn.addEventListener('click', () => {
    const expanded = btn.getAttribute('aria-expanded') === 'true';
    btn.setAttribute('aria-expanded', String(!expanded));
    nav.classList.toggle('open');
  });
}
const yearEl = document.getElementById('year');
if (yearEl) yearEl.textContent = String(new Date().getFullYear());
const path = location.pathname.replace(/\/$/, '') || '/';
for (const a of document.querySelectorAll('#main-nav a')) {
  const href = new URL(a.href).pathname.replace(/\/$/, '') || '/';
  if (href === path) a.setAttribute('aria-current', 'page');
}

const heroParallaxItems = [...document.querySelectorAll('.hero-banner[data-parallax="hero"]')];
const reduceMotionQuery = window.matchMedia('(prefers-reduced-motion: reduce)');
const smallScreenQuery = window.matchMedia('(max-width: 767px)');

if (heroParallaxItems.length) {
  let ticking = false;

  const applyHeroParallax = () => {
    const disableParallax = reduceMotionQuery.matches || smallScreenQuery.matches;

    for (const hero of heroParallaxItems) {
      if (disableParallax) {
        hero.style.setProperty('--hero-shift', '0px');
        continue;
      }

      const rect = hero.getBoundingClientRect();
      const viewportHeight = window.innerHeight || document.documentElement.clientHeight;
      const offset = (viewportHeight - rect.top) * 0.08;
      const clamped = Math.max(-18, Math.min(26, offset));
      hero.style.setProperty('--hero-shift', `${clamped}px`);
    }

    ticking = false;
  };

  const requestHeroParallax = () => {
    if (ticking) return;
    ticking = true;
    window.requestAnimationFrame(applyHeroParallax);
  };

  window.addEventListener('scroll', requestHeroParallax, { passive: true });
  window.addEventListener('resize', requestHeroParallax);
  if (typeof reduceMotionQuery.addEventListener === 'function') {
    reduceMotionQuery.addEventListener('change', requestHeroParallax);
    smallScreenQuery.addEventListener('change', requestHeroParallax);
  } else if (typeof reduceMotionQuery.addListener === 'function') {
    reduceMotionQuery.addListener(requestHeroParallax);
    smallScreenQuery.addListener(requestHeroParallax);
  }
  requestHeroParallax();
}

/* Lightbox — supports [data-lightbox] (embed src) and .post-gallery-item img */
(function () {
  var triggers = document.querySelectorAll('[data-lightbox]');
  var galleryImgs = document.querySelectorAll('.post-gallery-item img');
  if (!triggers.length && !galleryImgs.length) return;

  // Create overlay DOM
  var overlay = document.createElement('div');
  overlay.className = 'lightbox-overlay';
  overlay.id = 'lightbox';
  overlay.innerHTML =
    '<button class="lightbox-close" aria-label="Close">&times;</button>' +
    '<div class="lightbox-content"></div>';
  document.body.appendChild(overlay);

  var content = overlay.querySelector('.lightbox-content');

  function open(el) {
    content.innerHTML = '';
    var src = el.getAttribute('data-lightbox');
    if (src) {
      var embed = document.createElement('embed');
      embed.src = src;
      content.appendChild(embed);
    } else if (el.tagName === 'IMG') {
      var img = document.createElement('img');
      img.src = el.src;
      img.alt = el.alt || '';
      content.appendChild(img);
    }
    overlay.classList.add('active');
    document.body.style.overflow = 'hidden';
  }

  function close() {
    overlay.classList.remove('active');
    document.body.style.overflow = '';
    content.innerHTML = '';
  }

  triggers.forEach(function (el) {
    el.addEventListener('click', function () { open(el); });
  });
  galleryImgs.forEach(function (img) {
    img.addEventListener('click', function () { open(img); });
  });

  overlay.addEventListener('click', function (e) {
    if (e.target === overlay || e.target.classList.contains('lightbox-close')) close();
  });
  document.addEventListener('keydown', function (e) {
    if (e.key === 'Escape') close();
  });
})();
