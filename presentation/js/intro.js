/* ============================================================
   Intro cinemática (slide 1): folha de maple pulsando →
   clique na folha → loader → capa.
   ============================================================ */
(function () {
  'use strict';
  const hero = document.querySelector('.slide.intro');
  if (!hero) return;

  const sCan    = hero.querySelector('#scene-canada');
  const sLoader = hero.querySelector('.scene-loader');
  const sCover  = hero.querySelector('.scene-cover');

  let timers = [];
  let playing = false;
  const T = (fn, ms) => timers.push(setTimeout(fn, ms));
  const clearAll = () => { timers.forEach(clearTimeout); timers = []; };

  // Estado inicial: só a cena do Canadá.
  function arm() {
    clearAll();
    playing = false;
    [sLoader, sCover].forEach(s => s && s.classList.remove('show'));
    if (sCan) sCan.classList.add('show');
  }

  // Dispara a animação (chamado pelo clique na folha).
  function play() {
    if (playing) return;
    playing = true;
    clearAll();

    // Cena 2 — Loader
    T(() => { sCan.classList.remove('show'); sLoader.classList.add('show'); }, 350);

    // Cena 3 — Capa
    T(() => { sLoader.classList.remove('show'); sCover.classList.add('show'); }, 4350);
  }

  if (sCan) {
    sCan.addEventListener('click', play);
    sCan.addEventListener('keydown', (e) => {
      if (e.key === 'Enter' || e.key === ' ') { e.preventDefault(); e.stopPropagation(); play(); }
    });
  }

  // arma o estado inicial ao abrir e sempre que o slide 1 volta a ficar ativo
  if (hero.classList.contains('active')) arm();
  const mo = new MutationObserver(() => {
    if (hero.classList.contains('active')) arm();
    else clearAll();
  });
  mo.observe(hero, { attributes: true, attributeFilter: ['class'] });
})();
