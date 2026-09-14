/* ============================================================
   Engine de onboarding — passos com Duo, progresso e CONTINUAR.
   ============================================================ */
(function () {
  'use strict';
  const scaler  = document.getElementById('scaler');
  const slides  = Array.from(document.querySelectorAll('.slide'));
  const counter = document.getElementById('counter');
  const fill    = document.getElementById('ob-fill');
  const back    = document.getElementById('ob-back');
  const cta      = document.getElementById('ob-cta');
  const ctaWrap  = document.getElementById('ob-cta-wrap');
  const tocPanel = document.getElementById('toc-panel');
  const tocList  = document.getElementById('toc-list');
  const DESIGN_W = 1280, DESIGN_H = 720;

  let index = 0, step = 0;

  function fit() {
    const s = Math.min(window.innerWidth / DESIGN_W, window.innerHeight / DESIGN_H);
    scaler.style.transform = 'scale(' + s + ')';
  }
  window.addEventListener('resize', fit);

  const stepsOf = i => Array.from(slides[i].querySelectorAll('.step'));

  function render() {
    slides.forEach((sl, i) => sl.classList.toggle('active', i === index));
    scaler.classList.toggle('splash-mode', slides[index].classList.contains('splash') || slides[index].classList.contains('cover') || slides[index].classList.contains('intro') || slides[index].classList.contains('trail-slide'));
    stepsOf(index).forEach((el, k) => el.classList.toggle('show', k < step));

    counter.textContent = (index + 1) + ' / ' + slides.length;
    fill.style.width = ((index + 1) / slides.length * 100) + '%';
    back.disabled = (index === 0 && step === 0);

    // botão CONTINUAR: label por slide (data-cta); vazio = esconde
    const label = slides[index].dataset.cta;
    if (label === '') { ctaWrap.style.display = 'none'; }
    else { ctaWrap.style.display = 'flex'; cta.textContent = label || 'CONTINUAR'; }

    Array.from(tocList.children).forEach((li, i) =>
      li.classList.toggle('current', +li.dataset.goto === index));
    location.replace('#' + (index + 1));
  }

  function next() {
    const steps = stepsOf(index);
    if (step < steps.length) { step++; return render(); }
    if (index < slides.length - 1) { index++; step = 0; render(); }
  }
  function prev() {
    if (step > 0) { step--; return render(); }
    if (index > 0) { index--; step = stepsOf(index).length; render(); }
  }
  function goto(i) { index = Math.max(0, Math.min(slides.length - 1, i)); step = 0; render(); closeToc(); }

  function buildToc() {
    slides.forEach((sl, i) => {
      const title = sl.dataset.title || ('Passo ' + (i + 1));
      const li = document.createElement('li');
      li.className = 'toc-item'; li.dataset.goto = i;
      li.innerHTML = '<span class="toc-num">' + String(i + 1).padStart(2, '0') + '</span><span>' + title + '</span>';
      li.addEventListener('click', () => goto(i));
      tocList.appendChild(li);
    });
  }
  const toggleToc = () => tocPanel.classList.toggle('open');
  const closeToc  = () => tocPanel.classList.remove('open');

  window.addEventListener('keydown', (e) => {
    switch (e.key) {
      case 'ArrowRight': case ' ': case 'PageDown': e.preventDefault(); next(); break;
      case 'ArrowLeft':  case 'PageUp': e.preventDefault(); prev(); break;
      case 'Home': goto(0); break;
      case 'End':  goto(slides.length - 1); break;
      case 't': case 'T': toggleToc(); break;
      case 'Escape': closeToc(); break;
      case 'f': case 'F':
        if (!document.fullscreenElement) document.documentElement.requestFullscreen();
        else document.exitFullscreen();
        break;
    }
  });

  cta.addEventListener('click', next);
  back.addEventListener('click', prev);
  // botões flutuantes que avançam (ex.: COMEÇAR da intro)
  document.querySelectorAll('[data-advance]').forEach(b => b.addEventListener('click', next));
  document.getElementById('toc-toggle').addEventListener('click', toggleToc);

  // cartões de opção: seleciona e avança
  document.querySelectorAll('.ob-option').forEach(opt => {
    opt.addEventListener('click', () => {
      const siblings = opt.parentElement.querySelectorAll('.ob-option');
      siblings.forEach(s => s.classList.remove('sel'));
      opt.classList.add('sel');
      setTimeout(next, 420);
    });
  });

  // gestos de toque
  let tx = 0;
  window.addEventListener('touchstart', e => tx = e.changedTouches[0].clientX, {passive:true});
  window.addEventListener('touchend',   e => {
    const dx = e.changedTouches[0].clientX - tx;
    if (Math.abs(dx) > 50) (dx < 0 ? next() : prev());
  }, {passive:true});

  slides.forEach((sl, i) => { const c = sl.querySelector('.corner-num'); if (c) c.textContent = String(i + 1).padStart(2, '0'); });
  buildToc();
  fit();
  const hash = parseInt(location.hash.replace('#', ''), 10);
  if (hash && hash >= 1 && hash <= slides.length) index = hash - 1;
  render();
})();
