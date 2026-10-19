/* =========================================================================
   Contacto por WhatsApp — una sola fuente para todas las paginas.

   1. Mensaje por pagina: los enlaces wa.me con el texto generico ("pedir
      presupuesto") pasan a decir de que producto viene el cliente.
      data-wa="foto" -> mensaje de "os envio una foto de mi ventana".
      data-wa-msg="..." -> mensaje literal (tarjetas de estancias).
   2. Movil: barra fija abajo con texto, en lugar de los dos iconos. Solo
      aparece cuando el boton principal de la pagina no esta en pantalla.
   3. Ordenador: wa.me abre una pagina intermedia que pide WhatsApp Web.
      En su lugar se abre una ventana con QR + "abrir en este ordenador" +
      telefono + formulario. La conversion se cuenta cuando el visitante
      pulsa el enlace real de dentro de la ventana, no al abrirla.
   ========================================================================= */
(function () {
  'use strict';

  var PHONE = '34641354788';
  var WA_BASE = 'https://wa.me/' + PHONE + '?text=';

  // Producto de cada pagina, con articulo, para "Me interesan ___".
  var PRODUCTO = {
    'cortinas-a-medida': 'las cortinas a medida',
    'cortinas-blackout': 'las cortinas blackout',
    'cortinas-enrollables': 'las cortinas enrollables',
    'cortinas-verticales': 'las cortinas verticales',
    'venecianas': 'las persianas venecianas',
    'paneles-japoneses': 'los paneles japoneses',
    'visillos': 'los visillos',
    'estor-de-tela': 'los estores de tela',
    'estores-a-medida': 'los estores a medida',
    'plisadas': 'las cortinas plisadas',
    'motorizacion': 'las cortinas motorizadas',
    'cortinas-palma-de-mallorca': 'las cortinas a medida en Palma'
  };

  // Paginas cuyo cliente no encaja en "me interesan las ___".
  var MENSAJE_PROPIO = {
    'para-hoteles': 'Hola, vengo de vuestra web. Tengo un hotel o restaurante y solicito información sobre cortinas para el proyecto.',
    'para-arquitectos': 'Hola, vengo de vuestra web. Tengo un proyecto de arquitectura o interiorismo y solicito información sobre cortinas.'
  };

  // Textos genericos que se sustituyen segun el boton. Los demas (p. ej. "que
  // vinierais a medir mis ventanas") ya son especificos y se respetan.
  var GENERICOS = [
    'Hola, me gustaría pedir presupuesto',
    'Hola, me gustaría pedir presupuesto para cortinas a medida',
    'Hola, me gustaría solicitar una visita gratuita'
  ];

  var slug = location.pathname.replace(/^\/|\.html$/g, '') || 'index';
  var producto = PRODUCTO[slug] || 'las cortinas a medida';

  var mensajePagina = MENSAJE_PROPIO[slug] ||
    'Hola, vengo de vuestra web. Solicito información sobre ' + producto + '.';
  var mensajeFoto = 'Hola, vengo de vuestra web. Os envío una foto de mi ventana y solicito información sobre ' + producto + '.';
  var mensajePresupuesto = MENSAJE_PROPIO[slug] ||
    'Hola, vengo de vuestra web. Solicito información y presupuesto sin compromiso sobre ' + producto + '.';
  var mensajeTelas = MENSAJE_PROPIO[slug] ||
    'Hola, vengo de vuestra web. Solicito información sobre ' + producto + ' y me gustaría ver las telas.';

  // Los botones alternan "presupuesto gratis", "ver las telas" y "visita":
  // el mensaje acompaña a lo que dice el boton.
  function mensajeSegunBoton(a) {
    var t = (a.textContent || '').toLowerCase();
    if (t.indexOf('presupuesto') !== -1) return mensajePresupuesto;
    if (t.indexOf('telas') !== -1) return mensajeTelas;
    return mensajePagina;
  }

  function waHref(msg) { return WA_BASE + encodeURIComponent(msg); }

  function textoDe(href) {
    var q = href.split('?text=')[1];
    if (!q) return '';
    try { return decodeURIComponent(q); } catch (e) { return ''; }
  }

  // ---------- 1. Mensaje por pagina ----------
  function reescribirEnlaces() {
    var links = document.querySelectorAll('a[href^="https://wa.me/"]');
    for (var i = 0; i < links.length; i++) {
      var a = links[i];
      if (a.hasAttribute('data-wa-msg')) {
        a.href = waHref(a.getAttribute('data-wa-msg'));
      } else if (a.getAttribute('data-wa') === 'foto') {
        a.href = waHref(mensajeFoto);
      } else if (GENERICOS.indexOf(textoDe(a.getAttribute('href'))) !== -1) {
        a.href = waHref(mensajeSegunBoton(a));
      }
    }
  }

  // ---------- Helpers de DOM (sin innerHTML, como privacidad-ui.js) ----------
  var SVGNS = 'http://www.w3.org/2000/svg';
  var ICON_WA = 'M17.472 14.382c-.297-.149-1.758-.867-2.03-.967-.273-.099-.471-.148-.67.15-.197.297-.767.966-.94 1.164-.173.199-.347.223-.644.075-.297-.15-1.255-.463-2.39-1.475-.883-.788-1.48-1.761-1.653-2.059-.173-.297-.018-.458.13-.606.134-.133.298-.347.446-.52.149-.174.198-.298.298-.497.099-.198.05-.371-.025-.52-.075-.149-.669-1.612-.916-2.207-.242-.579-.487-.5-.669-.51-.173-.008-.371-.01-.57-.01-.198 0-.52.074-.792.372-.272.297-1.04 1.016-1.04 2.479 0 1.462 1.065 2.875 1.213 3.074.149.198 2.096 3.2 5.077 4.487.709.306 1.262.489 1.694.625.712.227 1.36.195 1.871.118.571-.085 1.758-.719 2.006-1.413.248-.694.248-1.289.173-1.413-.074-.124-.272-.198-.57-.347m-5.421 7.403h-.004a9.87 9.87 0 01-5.031-1.378l-.361-.214-3.741.982.998-3.648-.235-.374a9.86 9.86 0 01-1.51-5.26c.001-5.45 4.436-9.884 9.888-9.884 2.64 0 5.122 1.03 6.988 2.898a9.825 9.825 0 012.893 6.994c-.003 5.45-4.437 9.884-9.885 9.884m8.413-18.297A11.815 11.815 0 0012.05 0C5.495 0 .16 5.335.157 11.892c0 2.096.547 4.142 1.588 5.945L.057 24l6.305-1.654a11.882 11.882 0 005.683 1.448h.005c6.554 0 11.89-5.335 11.893-11.893a11.821 11.821 0 00-3.48-8.413z';
  var ICON_TEL = 'M13.832 16.568a1 1 0 0 0 1.213-.303l.355-.465A2 2 0 0 1 17 15h3a2 2 0 0 1 2 2v3a2 2 0 0 1-2 2A18 18 0 0 1 2 4a2 2 0 0 1 2-2h3a2 2 0 0 1 2 2v3a2 2 0 0 1-.8 1.6l-.468.351a1 1 0 0 0-.292 1.233a14 14 0 0 0 6.392 6.384';
  var ICON_X = 'M18 6 6 18M6 6l12 12';

  function icon(d, size, stroke) {
    var svg = document.createElementNS(SVGNS, 'svg');
    svg.setAttribute('width', size);
    svg.setAttribute('height', size);
    svg.setAttribute('viewBox', '0 0 24 24');
    svg.setAttribute('aria-hidden', 'true');
    svg.setAttribute('focusable', 'false');
    var p = document.createElementNS(SVGNS, 'path');
    p.setAttribute('d', d);
    if (stroke) {
      p.setAttribute('fill', 'none');
      p.setAttribute('stroke', 'currentColor');
      p.setAttribute('stroke-width', '2');
      p.setAttribute('stroke-linecap', 'round');
      p.setAttribute('stroke-linejoin', 'round');
    } else {
      p.setAttribute('fill', 'currentColor');
    }
    svg.appendChild(p);
    return svg;
  }

  function el(tag, attrs, children) {
    var node = document.createElement(tag);
    Object.keys(attrs || {}).forEach(function (k) {
      if (k === 'className') node.className = attrs[k];
      else if (k === 'text') node.textContent = attrs[k];
      else node.setAttribute(k, attrs[k]);
    });
    (children || []).forEach(function (c) { node.appendChild(c); });
    return node;
  }

  // ---------- 2. Barra fija en movil ----------
  function barraMovil() {
    var flotantes = document.getElementById('phone-wrap');
    if (!flotantes) return; // solo en paginas con los botones flotantes
    flotantes = flotantes.parentElement;

    var bar = el('div', {
      id: 'wa-bar',
      className: 'fixed bottom-0 inset-x-0 z-[90] md:hidden flex items-center gap-3 px-4 pt-3 bg-arena-50/95 backdrop-blur-md border-t border-arena-300/70 transition-transform duration-300 translate-y-full',
      style: 'padding-bottom:max(12px, env(safe-area-inset-bottom))'
    }, [
      el('a', {
        href: waHref(mensajePresupuesto),
        target: '_blank',
        rel: 'noopener noreferrer',
        className: 'flex-1 inline-flex items-center justify-center gap-2 h-12 bg-terracotta-500 text-white rounded-full text-[11px] font-semibold uppercase tracking-widest font-body shadow-lg shadow-terracotta-500/20'
      }, [icon(ICON_WA, 16), document.createTextNode('Pedir presupuesto gratis')]),
      el('a', {
        href: 'tel:+' + PHONE,
        'aria-label': 'Llamar a DECORT MARUCC',
        className: 'w-12 h-12 shrink-0 inline-flex items-center justify-center rounded-full border border-arena-400 text-neutral-700 bg-white'
      }, [icon(ICON_TEL, 18, true)])
    ]);
    document.body.appendChild(bar);

    var movil = window.matchMedia('(max-width: 767px)');
    function aplicar() {
      flotantes.style.display = movil.matches ? 'none' : '';
      document.body.style.paddingBottom = movil.matches ? '76px' : '';
    }
    aplicar();
    if (movil.addEventListener) movil.addEventListener('change', aplicar);

    // Oculta la barra mientras el boton principal de la pagina esta a la vista
    // (en la home, los botones de la portada); asi no se repite el mismo boton.
    // Es el primer enlace wa.me visible del contenido: fuera del menu, de los
    // flotantes y de la propia barra (en la home la portada es un <header> y el
    // menu movil, cerrado, queda desplazado por encima de la pagina).
    var principal = null;
    var cand = document.querySelectorAll('a[href^="https://wa.me/"]');
    for (var i = 0; i < cand.length && !principal; i++) {
      var c = cand[i];
      if (c.offsetParent === null || bar.contains(c) || flotantes.contains(c) ||
          c.closest('nav, footer, [role="dialog"], [inert], [aria-hidden="true"]') ||
          c.getBoundingClientRect().top + window.pageYOffset < 0) continue;
      principal = c;
    }
    function mostrar(si) { bar.classList.toggle('translate-y-full', !si); }
    if (principal && 'IntersectionObserver' in window) {
      new IntersectionObserver(function (entries) {
        mostrar(!entries[0].isIntersecting);
      }).observe(principal);
    } else {
      mostrar(true);
    }
  }

  // ---------- 3. Ventana con QR en ordenador ----------
  var modal, modalLink, ultimoFoco;

  function crearModal() {
    modalLink = el('a', {
      href: waHref(mensajePagina),
      target: '_blank',
      rel: 'noopener noreferrer',
      'data-wa-modal': '1',
      className: 'w-full inline-flex items-center justify-center gap-2 px-6 py-3 bg-terracotta-500 hover:bg-terracotta-600 text-white rounded-full text-xs font-semibold uppercase tracking-widest font-body transition duration-300'
    }, [icon(ICON_WA, 15), document.createTextNode('Abrir WhatsApp en este ordenador')]);

    var cerrar = el('button', {
      type: 'button',
      'aria-label': 'Cerrar',
      className: 'absolute top-4 right-4 w-9 h-9 inline-flex items-center justify-center rounded-full text-neutral-500 hover:text-neutral-800 hover:bg-arena-200 transition-colors'
    }, [icon(ICON_X, 18, true)]);
    cerrar.addEventListener('click', cerrarModal);

    var qr = el('img', {
      'data-src': '/public/images/whatsapp-qr-v2.svg',
      alt: 'Código QR para abrir el chat de WhatsApp de DECORT MARUCC',
      width: '168',
      height: '168',
      className: 'w-[168px] h-[168px] mx-auto rounded-xl border border-arena-300 p-2 bg-white'
    });

    var panel = el('div', {
      role: 'dialog',
      'aria-modal': 'true',
      'aria-labelledby': 'wa-modal-titulo',
      className: 'relative w-full max-w-sm bg-arena-50 rounded-3xl shadow-2xl p-8 text-center font-body'
    }, [
      cerrar,
      el('p', { className: 'text-[10px] font-medium tracking-widest uppercase text-terracotta-600 mb-2', text: 'Visita y presupuesto sin cargo' }),
      el('h2', { id: 'wa-modal-titulo', className: 'text-3xl font-light font-display text-neutral-800 mb-2', text: 'Hablemos por WhatsApp' }),
      el('p', { className: 'text-sm text-neutral-600 leading-relaxed mb-5', text: 'Escanea el código con la cámara del móvil y se abrirá el chat.' }),
      qr,
      el('p', { className: 'text-[10px] uppercase tracking-widest text-neutral-500 my-5', text: 'o bien' }),
      modalLink,
      el('div', { className: 'mt-5 pt-5 border-t border-arena-300 space-y-2 text-sm text-neutral-600' }, [
        el('p', {}, [
          document.createTextNode('Llámanos: '),
          el('a', { href: 'tel:+' + PHONE, className: 'font-semibold text-neutral-800 hover:text-terracotta-600', text: '+34 641 35 47 88' })
        ]),
        el('p', {}, [
          el('a', { href: '/contacto.html#dm-contacto', className: 'text-terracotta-600 underline underline-offset-4 decoration-terracotta-300 hover:text-terracotta-700', text: 'Déjanos tus datos y te llamamos' })
        ])
      ])
    ]);

    modal = el('div', {
      id: 'wa-modal',
      className: 'fixed inset-0 z-[95] hidden items-center justify-center p-4 bg-neutral-900/50 backdrop-blur-sm'
    }, [panel]);
    modal.addEventListener('click', function (e) { if (e.target === modal) cerrarModal(); });
    modal.addEventListener('keydown', function (e) {
      if (e.key === 'Escape') { cerrarModal(); return; }
      if (e.key !== 'Tab') return;
      var f = panel.querySelectorAll('a[href], button');
      var first = f[0], last = f[f.length - 1];
      if (e.shiftKey && document.activeElement === first) { e.preventDefault(); last.focus(); }
      else if (!e.shiftKey && document.activeElement === last) { e.preventDefault(); first.focus(); }
    });
    // Tras pulsar el enlace real, la ventana ya no hace falta.
    modalLink.addEventListener('click', function () { setTimeout(cerrarModal, 300); });
    document.body.appendChild(modal);
  }

  function abrirModal(href) {
    if (!modal) crearModal();
    var img = modal.querySelector('img[data-src]');
    if (img) { img.src = img.getAttribute('data-src'); img.removeAttribute('data-src'); }
    modalLink.href = href;
    ultimoFoco = document.activeElement;
    modal.classList.remove('hidden');
    modal.classList.add('flex');
    modal.querySelector('button').focus();
    if (window.dataLayer) window.dataLayer.push({ event: 'whatsapp_qr_open' });
  }

  function cerrarModal() {
    if (!modal) return;
    modal.classList.add('hidden');
    modal.classList.remove('flex');
    if (ultimoFoco && ultimoFoco.focus) ultimoFoco.focus();
  }

  function ventanaEscritorio() {
    // QR en ordenadores y tablets; en el movil, WhatsApp directo.
    // Tablet = pantalla tactil cuyo lado corto mide 600 px o mas (un movil
    // no pasa de ~430 ni en horizontal, por eso no se usa el ancho actual).
    var raton = window.matchMedia('(hover: hover) and (pointer: fine)');
    function conQR() {
      return raton.matches || Math.min(screen.width, screen.height) >= 600;
    }
    // Captura en window: corre antes que el listener de contact_click
    // (document, captura) y que el de GTM, asi el clic que solo abre la
    // ventana no cuenta como conversion. Cuenta el enlace de dentro.
    window.addEventListener('click', function (e) {
      if (!conQR()) return;
      var a = e.target.closest && e.target.closest('a[href^="https://wa.me/"]');
      if (!a || a.hasAttribute('data-wa-modal')) return;
      if (e.ctrlKey || e.metaKey || e.shiftKey || e.button !== 0) return;
      e.preventDefault();
      e.stopImmediatePropagation();
      abrirModal(a.href);
    }, true);
  }

  function init() {
    reescribirEnlaces();
    barraMovil();
    ventanaEscritorio();
  }

  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', init);
  else init();
})();
