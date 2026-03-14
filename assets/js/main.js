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
