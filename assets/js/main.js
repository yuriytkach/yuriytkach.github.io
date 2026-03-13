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
