/* Deck engine: scale to fit, keyboard/click navigation, #hash, progress, overview (O), fullscreen (F), print (P). */
(function () {
  const slides = [...document.querySelectorAll('.slide')];
  const total = slides.length;
  const pad = n => String(n).padStart(2, '0');
  const title = document.body.dataset.deck || '';
  const part = document.body.dataset.part || '';

  slides.forEach((s, i) => {
    const slot = document.createElement('div');
    slot.className = 'slot';
    s.parentNode.insertBefore(slot, s);
    slot.appendChild(s);
    if (!s.querySelector('.topbar')) {
      s.insertAdjacentHTML('afterbegin',
        `<div class="topbar"><div class="brand"><span data-i="langfuse-wordmark"></span><span class="x">× AIDE · Workshop 5</span></div>` +
        `<div class="crumb">${part} · <b>${s.dataset.title || title}</b></div>` +
        `<div class="kbd">${pad(i + 1)} / ${pad(total)}</div></div>`);
    }
    if (!s.querySelector('.footer')) {
      s.insertAdjacentHTML('beforeend',
        `<div class="footer"><span>${title}</span><span>Orbisa · Helix · Langfuse — fictional company</span>` +
        `<span class="keys"><span class="kbd">←</span><span class="kbd">→</span><span style="margin-left:6px">navigate</span>` +
        `<span class="kbd" style="margin-left:10px">O</span><span>overview</span></span></div>`);
    }
  });
  const bar = document.createElement('div');
  bar.className = 'progress';
  document.body.appendChild(bar);
  if (window.LF_ICONS) document.querySelectorAll('.topbar [data-i]').forEach(el => {
    const ic = window.LF_ICONS[el.dataset.i];
    el.innerHTML = `<svg viewBox="${ic.vb}" aria-hidden="true">${ic.body}</svg>`;
  });

  const fromHash = () => location.hash === '#last' ? total - 1 : (parseInt(location.hash.slice(1), 10) - 1 || 0);
  let cur = Math.min(Math.max(fromHash(), 0), total - 1);
  const next = document.body.dataset.next, prev = document.body.dataset.prev;
  function go(i) {
    if (i >= total && next) { location.href = next + '#1'; return; }
    if (i < 0 && prev) { location.href = prev + '#last'; return; }
    show(i);
  }

  function fit() {
    const s = Math.min(innerWidth / 1600, innerHeight / 900);
    document.documentElement.style.setProperty('--scale', s);
  }
  function show(i) {
    cur = Math.min(Math.max(i, 0), total - 1);
    slides.forEach((s, j) => s.classList.toggle('active', j === cur));
    document.querySelectorAll('.slot').forEach((s, j) => s.classList.toggle('cur', j === cur));
    bar.style.width = ((cur + 1) / total * 100) + '%';
    history.replaceState(null, '', '#' + (cur + 1));
  }
  function overview(on) {
    document.body.classList.toggle('overview', on);
    if (on) document.querySelector('.slot.cur')?.scrollIntoView({ block: 'center' });
  }

  addEventListener('resize', fit);
  addEventListener('keydown', e => {
    if (e.metaKey || e.ctrlKey || e.altKey) return;
    const k = e.key;
    if (['ArrowRight', 'PageDown', ' ', 'ArrowDown', 'Enter'].includes(k)) { e.preventDefault(); overview(false); go(cur + 1); }
    else if (['ArrowLeft', 'PageUp', 'ArrowUp', 'Backspace'].includes(k)) { e.preventDefault(); overview(false); go(cur - 1); }
    else if (k === 'Home') show(0);
    else if (k === 'End') show(total - 1);
    else if (k === 'o' || k === 'O' || k === 'Escape') overview(k !== 'Escape' && !document.body.classList.contains('overview'));
    else if (k === 'f' || k === 'F') document.fullscreenElement ? document.exitFullscreen() : document.documentElement.requestFullscreen();
    else if (k === 'p' || k === 'P') print();
  });
  document.addEventListener('click', e => {
    const slot = e.target.closest('.slot');
    if (document.body.classList.contains('overview') && slot) {
      show([...document.querySelectorAll('.slot')].indexOf(slot)); overview(false); return;
    }
    if (e.target.closest('a, button')) return;
    go(e.clientX > innerWidth / 3 ? cur + 1 : cur - 1);
  });
  addEventListener('hashchange', () => show(Math.min(Math.max(fromHash(), 0), total - 1)));

  fit();
  show(cur);
})();
