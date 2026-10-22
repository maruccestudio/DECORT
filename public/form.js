/* Formulario de contacto DECORT MARUCC.
   Se engancha a cualquier formulario con id "dm-contacto" de la página.
   Envía a Web3Forms sin recargar y empuja un evento form_submit al dataLayer. */

(function () {
    var form = document.getElementById('dm-contacto');
    if (!form) return;

    var btn = form.querySelector('.dm-submit');
    var msg = form.querySelector('.dm-msg');
    var etiquetaBoton = btn ? btn.textContent : 'Enviar';

    // Textos personalizables por pagina (data-*), para que la version en ingles
    // no necesite su propio JS. Si no se declaran, se usan los de siempre.
    function txt(attr, porDefecto) {
        return form.getAttribute(attr) || porDefecto;
    }
    var MSG_INVALIDO = txt('data-msg-invalido', 'Revisa el nombre, el email, la dirección y la aceptación de la política de privacidad.');
    var MSG_OK       = txt('data-msg-ok', 'Recibido. Te respondemos en menos de 24 horas.');
    var MSG_ERROR    = txt('data-msg-error', 'No se ha podido enviar. Escríbenos por WhatsApp al 641 354 788.');
    var MSG_ENVIANDO = txt('data-msg-enviando', 'Enviando…');

    function show(kind, text) {
        if (!msg) return;
        msg.className = 'dm-msg ' + kind;
        msg.textContent = text;
    }

    form.addEventListener('submit', function (e) {
        e.preventDefault();

        if (!form.checkValidity()) {
            show('err', MSG_INVALIDO);
            form.reportValidity();
            return;
        }

        btn.disabled = true;
        btn.textContent = MSG_ENVIANDO;
        if (msg) msg.className = 'dm-msg';

        var data = Object.fromEntries(new FormData(form));
        // De qué página salió el contacto, para saberlo desde el propio correo.
        data.pagina = document.title + ' (' + location.pathname + ')';
        // Origen de la visita (lo decide privacidad-ui.js). El gclid se guarda
        // aparte para poder subir las ventas cerradas a Google Ads en el futuro.
        var origen = window.maruccOrigen && window.maruccOrigen();
        if (origen && origen.canal === 'google-ads') {
            data.origen = 'Google Ads';
            if (origen.clic) data.gclid = origen.clic;
        } else {
            // Canal de llegada (privacidad-ui.js): Google, ChatGPT, Instagram, directo...
            // Sin cookies de analitica solo se sabe si el visitante lleno el
            // formulario en la misma pagina por la que entro.
            var visita = window.maruccVisita && window.maruccVisita();
            var conAnalitica = !!(window.__maruccConsentState && window.__maruccConsentState.analytics);
            data.origen = (visita && visita.canal) ||
                (conAnalitica ? 'No identificado' : 'No identificado (no aceptó cookies de analítica)');
        }
        var v = window.maruccVisita && window.maruccVisita();
        if (v && v.entrada && v.entrada !== location.pathname) data.pagina_entrada = v.entrada;
        if (v && v.veniaDe && v.veniaDe !== location.pathname && v.veniaDe !== data.pagina_entrada) data.venia_de = v.veniaDe;

        fetch('https://api.web3forms.com/submit', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json', Accept: 'application/json' },
            body: JSON.stringify(data)
        })
        .then(function (r) { return r.json(); })
        .then(function (res) {
            if (res.success) {
                form.reset();
                show('ok', MSG_OK);
                window.dataLayer = window.dataLayer || [];
                window.dataLayer.push({
                    event: 'form_submit',
                    form_name: form.getAttribute('data-form-name') || 'contacto',
                    tipo_proyecto: data.tipo_proyecto || ''
                });
            } else {
                show('err', MSG_ERROR);
            }
        })
        .catch(function () {
            show('err', MSG_ERROR);
        })
        .finally(function () {
            btn.disabled = false;
            btn.textContent = etiquetaBoton;
        });
    });
})();
