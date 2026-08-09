/**
 * Gestor de consentimiento (Fase 1) - DECORT MARUCC
 *
 * El estado INICIAL de consentimiento se resuelve en un script inline sincrono,
 * antes de este archivo y antes de GTM (ver <head> de cada pagina). Este archivo
 * solo gestiona: la interfaz (banner + modal accesible), guardar decisiones nuevas,
 * emitir el evento `consent_updated` cuando el usuario cambia su eleccion durante
 * la sesion, y el listener delegado de clics de contacto.
 *
 * No repite la logica de "primer estado" - eso vive exclusivamente en el inline.
 * Todo el DOM se construye con createElement/textContent (sin innerHTML) porque
 * no hay ningun dato externo/no confiable en juego, y es la practica mas segura.
 */
(function () {
  'use strict';

  window.dataLayer = window.dataLayer || [];

  var STORAGE_KEY = 'marucc_consent';
  var CONSENT_VERSION = 1;

  function readState() {
    var state = { necessary: true, analytics: false, ads: false };
    try {
      var raw = localStorage.getItem(STORAGE_KEY);
      if (raw) {
        var parsed = JSON.parse(raw);
        if (
          parsed && typeof parsed === 'object' &&
          parsed.version === CONSENT_VERSION &&
          typeof parsed.analytics === 'boolean' &&
          typeof parsed.ads === 'boolean'
        ) {
          state.analytics = parsed.analytics;
          state.ads = parsed.ads;
        }
      }
    } catch (e) {
      // JSON corrupto o localStorage no disponible: se devuelve el estado denegado por defecto
    }
    return state;
  }

  function saveState(state) {
    try {
      localStorage.setItem(STORAGE_KEY, JSON.stringify({
        version: CONSENT_VERSION,
        analytics: !!state.analytics,
        ads: !!state.ads,
        timestamp: new Date().toISOString()
      }));
    } catch (e) {
      // Almacenamiento no disponible (privado/cuota): el estado se aplica igual
      // para esta carga, pero no persiste - se volvera a preguntar la proxima visita.
    }
  }

  // GTM solo interpreta los comandos de consentimiento cuando llegan al dataLayer como
  // objeto `arguments` - que es justo lo que hace gtag(). Un array literal se ignora en
  // silencio: los tags disparan igual (sus triggers leen `consent_analytics`), pero el
  // Consent Mode de Google se queda en denied y no se escribe ninguna cookie.
  function gtagCmd() {
    window.dataLayer.push(arguments);
  }

  function applyConsent(state, emitUpdatedEvent) {
    gtagCmd('consent', 'update', {
      'analytics_storage': state.analytics ? 'granted' : 'denied',
      'ad_storage': state.ads ? 'granted' : 'denied',
      'ad_user_data': state.ads ? 'granted' : 'denied',
      'ad_personalization': state.ads ? 'granted' : 'denied'
    });

    window.__maruccConsentState = state;

    if (emitUpdatedEvent) {
      // Este evento (no consent_ready) es el que habilita, dentro de GTM, los
      // triggers de "consentimiento concedido durante la sesion" para cada tag.
      window.dataLayer.push({
        event: 'consent_updated',
        consent_analytics: !!state.analytics,
        consent_ads: !!state.ads
      });
    }
  }

  function commitChoice(newState) {
    var current = readState();
    var changed = current.analytics !== !!newState.analytics || current.ads !== !!newState.ads;
    saveState(newState);
    applyConsent(newState, changed || !window.__maruccConsentDecided);
    window.__maruccConsentDecided = true;
  }

  // ---------- Listener delegado de contacto (tel: y wa.me) ----------
  if (!window.__maruccContactListenerBound) {
    window.__maruccContactListenerBound = true;
    document.addEventListener('click', function (e) {
      var link = e.target.closest('a[href^="tel:"], a[href^="https://wa.me/"]');
      if (!link) return;
      var method = link.getAttribute('href').indexOf('tel:') === 0 ? 'telefono' : 'whatsapp';
      window.dataLayer.push({ event: 'contact_click', contact_method: method });
      // Sin preventDefault(): la navegacion a tel:/wa.me sigue su curso normal.
    }, true);
  }

  // ---------- Helpers de construccion de DOM (sin innerHTML) ----------
  function el(tag, attrs, children) {
    var node = document.createElement(tag);
    if (attrs) {
      Object.keys(attrs).forEach(function (key) {
        if (key === 'className') node.className = attrs[key];
        else if (key === 'text') node.textContent = attrs[key];
        else node.setAttribute(key, attrs[key]);
      });
    }
    (children || []).forEach(function (child) { node.appendChild(child); });
    return node;
  }

  // ---------- UI: banner + modal accesible ----------
  var lastFocusedElement = null;
  var bannerEl, modalEl;
  var toggleAnalytics, toggleAds;

  function trapFocus(container, evt) {
    if (evt.key === 'Escape') {
      closeModal();
      return;
    }
    if (evt.key !== 'Tab') return;

    var focusable = container.querySelectorAll(
      'button:not([disabled]), a[href], input:not([disabled]), [tabindex]:not([tabindex="-1"])'
    );
    if (!focusable.length) return;
    var first = focusable[0];
    var last = focusable[focusable.length - 1];

    if (evt.shiftKey && document.activeElement === first) {
      evt.preventDefault();
      last.focus();
    } else if (!evt.shiftKey && document.activeElement === last) {
      evt.preventDefault();
      first.focus();
    }
  }

  function buildBanner() {
    var policyLink = el('a', {
      href: '/politica-cookies.html',
      className: 'underline underline-offset-2 hover:text-terracotta-400 transition-colors',
      text: 'Política de cookies'
    });

    var text = el('p', { className: 'text-sm text-neutral-200 mb-4 leading-relaxed' }, [
      document.createTextNode('Queremos que esta web te resulte fácil de usar. Algunas cookies son necesarias para que funcione. Las demás, solo si nos das permiso, nos muestran qué páginas ayudan y cuáles confunden, para poder mejorarlas. Puedes cambiar tu elección cuando quieras. '),
      policyLink,
      document.createTextNode('.')
    ]);

    var rejectBtn = el('button', {
      type: 'button', id: 'marucc-consent-reject',
      className: 'flex-1 px-5 py-2.5 rounded-full border border-neutral-700 hover:bg-neutral-800 transition-colors text-xs font-semibold tracking-widest uppercase',
      text: 'Rechazar todo'
    });
    var configureBtn = el('button', {
      type: 'button', id: 'marucc-consent-configure',
      className: 'flex-1 px-5 py-2.5 rounded-full border border-neutral-700 hover:bg-neutral-800 transition-colors text-xs font-semibold tracking-widest uppercase',
      text: 'Configurar'
    });
    var acceptBtn = el('button', {
      type: 'button', id: 'marucc-consent-accept',
      className: 'flex-1 px-5 py-2.5 rounded-full bg-terracotta-500 hover:bg-terracotta-400 text-white transition-colors text-xs font-semibold tracking-widest uppercase shadow-lg shadow-terracotta-500/20',
      text: 'Aceptar todo'
    });

    var actions = el('div', { className: 'flex flex-col sm:flex-row gap-2.5' }, [rejectBtn, configureBtn, acceptBtn]);
    var card = el('div', { className: 'max-w-3xl mx-auto bg-neutral-900/95 backdrop-blur-md text-white rounded-2xl shadow-2xl border border-white/10 p-5 md:p-6' }, [text, actions]);

    var wrapper = el('div', {
      id: 'marucc-consent-banner',
      role: 'region',
      'aria-label': 'Aviso de cookies',
      className: 'fixed bottom-0 left-0 w-full z-[100] transform transition duration-500 ease-in-out font-body p-4 md:p-6 translate-y-full opacity-0'
    }, [card]);

    document.body.appendChild(wrapper);
    return wrapper;
  }

  function buildCategoryRow(title, desc, checkboxId, disabledChecked) {
    var labelBlock = el('div', {}, [
      el('p', { className: 'text-sm font-semibold', text: title }),
      el('p', { className: 'text-xs text-neutral-500', text: desc })
    ]);
    var checkbox = el('input', {
      type: 'checkbox',
      className: 'mt-1',
      'aria-label': title
    });
    if (checkboxId) checkbox.id = checkboxId;
    if (disabledChecked) {
      checkbox.checked = true;
      checkbox.disabled = true;
    }
    return { row: el('div', { className: 'flex items-start justify-between gap-4 py-3 border-b border-neutral-100' }, [labelBlock, checkbox]), checkbox: checkbox };
  }

  function buildModal() {
    var title = el('h2', { id: 'marucc-consent-title', className: 'text-lg font-semibold mb-2', text: 'Preferencias de privacidad' });
    var desc = el('p', { id: 'marucc-consent-desc', className: 'text-sm text-neutral-500 mb-6', text: 'Elige qué categorías quieres permitir. Puedes cambiar esta elección en cualquier momento desde este mismo panel.' });

    var necessary = buildCategoryRow('Necesarias', 'Solo guardan tu elección de cookies, para no volver a preguntarte. Siempre activas.', null, true);
    var analytics = buildCategoryRow('Analíticas', 'Nos muestran qué páginas se leen y en qué punto se traba la navegación, para poder mejorarlas. Google Analytics y Microsoft Clarity.', 'marucc-consent-toggle-analytics', false);
    var ads = buildCategoryRow('Publicitarias', 'Nos dicen si un anuncio trajo a alguien realmente interesado, para no gastar de más. Meta y Google Ads.', 'marucc-consent-toggle-ads', false);
    ads.row.className = ads.row.className.replace(' border-b border-neutral-100', '');

    toggleAnalytics = analytics.checkbox;
    toggleAds = ads.checkbox;

    var categories = el('div', { className: 'space-y-4 mb-6' }, [necessary.row, analytics.row, ads.row]);

    var rejectBtn = el('button', {
      type: 'button', id: 'marucc-consent-modal-reject',
      className: 'flex-1 px-5 py-2.5 rounded-full border border-neutral-300 hover:bg-neutral-100 transition-colors text-xs font-semibold tracking-widest uppercase',
      text: 'Rechazar todo'
    });
    var saveBtn = el('button', {
      type: 'button', id: 'marucc-consent-modal-save',
      className: 'flex-1 px-5 py-2.5 rounded-full bg-terracotta-500 hover:bg-terracotta-400 text-white transition-colors text-xs font-semibold tracking-widest uppercase',
      text: 'Guardar preferencias'
    });
    var actions = el('div', { className: 'flex flex-col sm:flex-row gap-2.5' }, [rejectBtn, saveBtn]);

    var dialog = el('div', {
      role: 'dialog',
      'aria-modal': 'true',
      'aria-labelledby': 'marucc-consent-title',
      'aria-describedby': 'marucc-consent-desc',
      className: 'relative bg-white text-neutral-800 rounded-2xl shadow-2xl max-w-lg w-full p-6 md:p-8 max-h-[85vh] overflow-y-auto'
    }, [title, desc, categories, actions]);

    var overlay = el('div', { id: 'marucc-consent-overlay', className: 'absolute inset-0 bg-black/60' });

    var wrapper = el('div', {
      id: 'marucc-consent-modal',
      className: 'fixed inset-0 z-[110] hidden items-center justify-center p-4'
    }, [overlay, dialog]);

    document.body.appendChild(wrapper);
    return wrapper;
  }

  function showBanner() {
    if (!bannerEl) bannerEl = buildBanner();
    requestAnimationFrame(function () {
      bannerEl.classList.remove('translate-y-full', 'opacity-0');
    });
  }

  function hideBanner() {
    if (!bannerEl) return;
    bannerEl.classList.add('translate-y-full', 'opacity-0');
  }

  function onModalKeydown(e) {
    trapFocus(modalEl.querySelector('[role="dialog"]'), e);
  }

  function openModal() {
    lastFocusedElement = document.activeElement;
    if (!modalEl) modalEl = buildModal();

    var current = readState();
    toggleAnalytics.checked = current.analytics;
    toggleAds.checked = current.ads;

    modalEl.classList.remove('hidden');
    modalEl.classList.add('flex');
    document.addEventListener('keydown', onModalKeydown, true);

    var dialog = modalEl.querySelector('[role="dialog"]');
    var firstFocusable = dialog.querySelector('input:not([disabled]), button');
    if (firstFocusable) firstFocusable.focus();
  }

  function closeModal() {
    if (!modalEl) return;
    modalEl.classList.add('hidden');
    modalEl.classList.remove('flex');
    document.removeEventListener('keydown', onModalKeydown, true);
    if (lastFocusedElement && typeof lastFocusedElement.focus === 'function') {
      lastFocusedElement.focus();
    }
  }

  function bindUI() {
    document.addEventListener('click', function (e) {
      var id = e.target && e.target.id;

      if (id === 'marucc-consent-accept') {
        commitChoice({ necessary: true, analytics: true, ads: true });
        hideBanner();
      } else if (id === 'marucc-consent-reject') {
        commitChoice({ necessary: true, analytics: false, ads: false });
        hideBanner();
      } else if (id === 'marucc-consent-configure') {
        openModal();
      } else if (id === 'marucc-consent-modal-save') {
        commitChoice({ necessary: true, analytics: toggleAnalytics.checked, ads: toggleAds.checked });
        closeModal();
        hideBanner();
      } else if (id === 'marucc-consent-modal-reject') {
        commitChoice({ necessary: true, analytics: false, ads: false });
        closeModal();
        hideBanner();
      } else if (id === 'marucc-consent-overlay') {
        closeModal(); // Cierra sin guardar - los toggles tocados no se aplican.
      } else if (e.target.closest && e.target.closest('.js-open-consent-preferences')) {
        e.preventDefault();
        openModal();
      }
    });
  }

  // ---------- API publica: reabrir el panel desde cualquier pagina/enlace ----------
  window.MaruccConsent = {
    openPreferences: openModal
  };

  bindUI();

  if (!window.__maruccConsentDecided) {
    // Misma demora que tenia el banner anterior, para no pisar la animacion de entrada del hero.
    setTimeout(showBanner, 1500);
  }
})();
