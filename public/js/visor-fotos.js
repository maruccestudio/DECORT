/* Visor de fotos (26-10-2026): proyectos y paginas de producto.
   Clarity registro clics muertos en las fotos: la gente intentaba ampliarlas.
   Toma las fotos del <main> que no son enlaces (las de "Tambien te puede
   interesar" llevan a otra pagina), las abre a pantalla completa en un
   <dialog> nativo y permite pasar con flechas, teclado o deslizando el dedo.
   Para excluir una foto: data-visor="no". Estilos en src/input.css. */
(function () {
  var imgs = Array.prototype.slice.call(document.querySelectorAll('main img'))
    .filter(function (img) { return !img.closest('a, button, [aria-hidden="true"], [data-visor="no"]'); });
  if (!imgs.length || typeof HTMLDialogElement !== 'function') return;

  // La version mas grande del srcset: la miniatura se ve al instante y se cambia al cargar.
  function grande(img) {
    var mejor = img.currentSrc || img.src, ancho = 0;
    (img.getAttribute('srcset') || '').split(',').forEach(function (c) {
      var p = c.trim().split(/\s+/), w = parseInt(p[1], 10);
      if (p[0] && w > ancho) { ancho = w; mejor = p[0]; }
    });
    return mejor;
  }
  function pie(img) {
    var fig = img.closest('figure'), fc = fig && fig.querySelector('figcaption');
    return fc ? fc.textContent.trim() : '';
  }

  var flecha = function (d) {
    return '<svg xmlns="http://www.w3.org/2000/svg" width="22" height="22" viewBox="0 0 24 24" aria-hidden="true" focusable="false"><path fill="none" stroke="currentColor" stroke-linecap="round" stroke-linejoin="round" stroke-width="1.75" d="' + d + '"/></svg>';
  };
  var dlg = document.createElement('dialog');
  dlg.className = 'visor';
  dlg.setAttribute('aria-label', 'Visor de fotos');
  dlg.innerHTML =
    '<div class="visor-escena">' +
      '<img class="visor-img" alt="" decoding="async">' +
    '</div>' +
    '<button type="button" class="visor-btn visor-cerrar" aria-label="Cerrar">' + flecha('M18 6 6 18M6 6l12 12') + '</button>' +
    '<button type="button" class="visor-btn visor-ant" aria-label="Foto anterior">' + flecha('m15 18-6-6 6-6') + '</button>' +
    '<button type="button" class="visor-btn visor-sig" aria-label="Foto siguiente">' + flecha('m9 18 6-6-6-6') + '</button>' +
    '<div class="visor-pie"><p class="visor-texto"></p><p class="visor-cuenta" aria-live="polite"></p></div>';
  // Con una sola foto no hay nada que pasar.
  if (imgs.length === 1) dlg.classList.add('visor-una');
  document.body.appendChild(dlg);

  var foto = dlg.querySelector('.visor-img'),
      texto = dlg.querySelector('.visor-texto'),
      cuenta = dlg.querySelector('.visor-cuenta'),
      actual = 0, origen = null;

  function precargar(i) {
    var img = imgs[(i + imgs.length) % imgs.length];
    if (img) { var p = new Image(); p.src = grande(img); }
  }

  function mostrar(i) {
    actual = (i + imgs.length) % imgs.length;
    var img = imgs[actual], src = grande(img);
    foto.classList.remove('visor-entra');
    foto.alt = img.alt || '';
    // Primero la version ya descargada en la pagina (sin hueco en blanco), luego la grande.
    foto.src = img.currentSrc || img.src;
    if (src !== foto.src) {
      var hd = new Image();
      hd.onload = function () { if (imgs[actual] === img) foto.src = src; };
      hd.src = src;
    }
    void foto.offsetWidth;
    foto.classList.add('visor-entra');
    var t = pie(img);
    texto.textContent = t;
    texto.hidden = !t;
    cuenta.textContent = imgs.length > 1 ? (actual + 1) + ' / ' + imgs.length : '';
    precargar(actual + 1);
    precargar(actual - 1);
  }

  function abrir(i) {
    origen = document.activeElement;
    mostrar(i);
    document.documentElement.classList.add('visor-abierto');
    dlg.showModal();
    dlg.querySelector(imgs.length > 1 ? '.visor-sig' : '.visor-cerrar').focus({ preventScroll: true });
  }

  dlg.addEventListener('close', function () {
    document.documentElement.classList.remove('visor-abierto');
    if (origen && origen.focus) origen.focus({ preventScroll: true });
  });

  dlg.querySelector('.visor-cerrar').addEventListener('click', function () { dlg.close(); });
  dlg.querySelector('.visor-ant').addEventListener('click', function () { mostrar(actual - 1); });
  dlg.querySelector('.visor-sig').addEventListener('click', function () { mostrar(actual + 1); });

  // Clic fuera de la foto y de los controles: cerrar.
  dlg.addEventListener('click', function (e) {
    if (e.target === dlg || e.target.classList.contains('visor-escena')) dlg.close();
  });

  dlg.addEventListener('keydown', function (e) {
    if (e.key === 'ArrowRight') { e.preventDefault(); mostrar(actual + 1); }
    else if (e.key === 'ArrowLeft') { e.preventDefault(); mostrar(actual - 1); }
  });

  // Deslizar con el dedo: horizontal pasa de foto; hacia abajo cierra.
  var x0 = null, y0 = 0;
  dlg.addEventListener('touchstart', function (e) {
    if (e.touches.length !== 1) { x0 = null; return; }
    x0 = e.touches[0].clientX; y0 = e.touches[0].clientY;
  }, { passive: true });
  dlg.addEventListener('touchend', function (e) {
    if (x0 === null) return;
    var dx = e.changedTouches[0].clientX - x0, dy = e.changedTouches[0].clientY - y0;
    x0 = null;
    if (Math.abs(dx) > 50 && Math.abs(dx) > Math.abs(dy)) { if (imgs.length > 1) mostrar(actual + (dx < 0 ? 1 : -1)); }
    else if (dy > 90 && Math.abs(dy) > Math.abs(dx)) dlg.close();
  }, { passive: true });

  imgs.forEach(function (img, i) {
    img.classList.add('visor-ampliable');
    img.setAttribute('tabindex', '0');
    img.setAttribute('role', 'button');
    img.setAttribute('aria-label', 'Ampliar foto' + (img.alt ? ': ' + img.alt : ''));
    img.addEventListener('click', function () { abrir(i); });
    img.addEventListener('keydown', function (e) {
      if (e.key === 'Enter' || e.key === ' ') { e.preventDefault(); abrir(i); }
    });
  });
})();
