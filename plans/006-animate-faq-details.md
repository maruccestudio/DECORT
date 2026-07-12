# 006 — Animate the FAQ `<details>`/`<summary>` open/close instead of an instant snap

- **Status**: TODO
- **Commit**: a68fcf2
- **Severity**: MEDIUM (missed opportunity, but high-frequency surface)
- **Category**: Missed opportunities / Interruptibility
- **Estimated scope**: 1 new shared file (`public/js/faq-animate.js`) + a 1-line `<script>` include added to 15 HTML files (every page with a FAQ section).

## Problem

Every FAQ section on the site uses native `<details>`/`<summary>`, with zero animation — content snaps open/closed instantly, no transition at all. This is the single most-repeated interactive surface on the site: **64 `<details>` elements across 15 pages** (`grep -c "<details" *.html`: `index.html:9`, `cortinas-a-medida.html:4`, `cortinas-blackout.html:4`, `cortinas-confeccionadas.html:4`, `cortinas-enrollables.html:4`, `cortinas-palma-de-mallorca.html:5`, `cortinas-verticales.html:4`, `estor-de-tela.html:3`, `motorizacion.html:4`, `paneles-japoneses.html:4`, `para-arquitectos.html:4`, `para-hoteles.html:5`, `plisadas.html:3`, `venecianas.html:4`, `visillos.html:3`).

Representative markup, `cortinas-a-medida.html:300-306`:

```html
<!-- cortinas-a-medida.html:300-306 — current -->
<details class="group border-b border-arena-300/60">
    <summary class="flex justify-between items-center cursor-pointer text-sm font-semibold font-body text-neutral-700 py-5 list-none select-none">
        <span>¿Cuánto tarda en confeccionarse una cortina a medida?</span>
        <iconify-icon icon="lucide:plus" width="18" class="text-terracotta-400 group-open:hidden shrink-0 ml-4"></iconify-icon>
        <iconify-icon icon="lucide:minus" width="18" class="text-terracotta-400 hidden group-open:block shrink-0 ml-4"></iconify-icon>
    </summary>
    <p class="text-sm text-neutral-600 pb-5 leading-relaxed font-body">El plazo habitual es de 3 a 4 semanas...</p>
</details>
```

AAUDIT.md Category 8 (missed opportunities): "State changes that teleport (content swaps, layout jumps) where a brief transition would prevent a jarring change" — this is exactly that. AUDIT.md Category 1 (purpose & frequency) classifies this as "Occasional (modals, drawers, toasts) → Standard animation" — a FAQ answer is functionally a small drawer, and this is a marketing/explanatory page, so a deliberate, unhurried reveal is appropriate (not the sub-300ms UI budget — AUDIT.md's duration table allows "Marketing / explanatory: can be longer" but this is closer to a drawer than a hero, so this plan still targets the drawer budget of 200–500ms for predictability).

A native `<details>` element cannot be smoothly height-animated with CSS alone in a way that's reliable across this project's target browsers (the modern `@starting-style` + `interpolate-size` route is too new/inconsistent to rely on here) — the standard, broadly-supported fix is to intercept the `toggle` event and animate height with the Web Animations API.

## Target

New shared file, `public/js/faq-animate.js`:

```js
// public/js/faq-animate.js — target, new file
(function () {
    var EASE_OUT = 'cubic-bezier(0.16, 1, 0.3, 1)'; // este proyecto's ease-out — ver DESIGN.md / plan 005
    var DURATION = 350; // ms — dentro del rango 200-500ms de AUDIT.md para drawers

    document.querySelectorAll('details').forEach(function (details) {
        var summary = details.querySelector('summary');
        var content = details.querySelector('summary + *');
        if (!summary || !content) return;
        var animating = false;

        summary.addEventListener('click', function (e) {
            e.preventDefault();
            if (animating) return;
            animating = true;

            if (!details.open) {
                details.style.overflow = 'hidden';
                details.open = true;
                var contentHeight = content.getBoundingClientRect().height;
                var anim = details.animate(
                    { height: [summary.getBoundingClientRect().height + 'px', (summary.getBoundingClientRect().height + contentHeight) + 'px'] },
                    { duration: DURATION, easing: EASE_OUT }
                );
                anim.onfinish = function () {
                    details.style.height = '';
                    details.style.overflow = '';
                    animating = false;
                };
            } else {
                details.style.overflow = 'hidden';
                var startHeight = details.getBoundingClientRect().height;
                var endHeight = summary.getBoundingClientRect().height;
                var anim = details.animate(
                    { height: [startHeight + 'px', endHeight + 'px'] },
                    { duration: DURATION, easing: EASE_OUT }
                );
                anim.onfinish = function () {
                    details.open = false;
                    details.style.height = '';
                    details.style.overflow = '';
                    animating = false;
                };
            }
        });
    });
})();
```

This respects `prefers-reduced-motion` implicitly only if the browser's WAAPI respects it — it does not by default, so add an explicit guard at the top of the IIFE:

```js
// public/js/faq-animate.js — add near the top, before the querySelectorAll loop
if (window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches) {
    return; // deja el toggle nativo instantáneo, sin JS de por medio
}
```

(Since the whole file is one IIFE, this `return` at the top exits the function immediately — verify it's placed inside the `(function () { ... })()` wrapper, before the `document.querySelectorAll('details')` line, so the guard actually short-circuits everything below it.)

Include on every page that has a FAQ (all 15 listed above), right before `</body>`:

```html
<script src="public/js/faq-animate.js" defer></script>
```

## Repo conventions to follow

- Reuse `cubic-bezier(0.16, 1, 0.3, 1)` — this project's established ease-out curve (see plan 005, or `index.html:54`/`index.html:157` if plan 005 hasn't run yet and the token doesn't exist as a CSS var — in that case hardcode the literal cubic-bezier in the JS file as shown above, since JS/WAAPI can't reference a CSS custom property directly anyway).
- `duration: 350` sits inside AUDIT.md's 200–500ms drawer budget — do not extend it further even though "marketing" pages get more leeway; a FAQ list opening slower than ~500ms starts to feel laggy when a user is scanning multiple questions.
- Every other script on this site is inlined per-page rather than externalized (see `index.html`'s multiple `<script>` blocks) — this plan deliberately breaks from that pattern because the exact same ~30 lines would otherwise need to be duplicated 15 times; a single shared `public/js/faq-animate.js` is the lower-risk, more maintainable choice, and `public/js/` does not currently exist as a directory, create it.

## Steps

1. Create the directory `ANTIGRAVITY_DECORT/public/js/` if it doesn't exist.
2. Create `ANTIGRAVITY_DECORT/public/js/faq-animate.js` with the exact contents shown in Target above (including the `prefers-reduced-motion` guard placed correctly inside the IIFE).
3. For each of the 15 files listed in Problem above, add `<script src="public/js/faq-animate.js" defer></script>` immediately before the closing `</body>` tag, after any existing inline `<script>` blocks already there. Use the exact same relative path (`public/js/faq-animate.js`) on every page — do not adjust for subdirectory depth, since all 21 HTML pages live flat at the project root alongside `public/`.
4. Do not modify the `<details>`/`<summary>`/`<p>` markup itself, its classes, its text content, or its `iconify-icon` plus/minus toggle icons — the existing `group-open:hidden` / `group-open:block` Tailwind classes for the plus/minus icon swap already key off the `open` attribute and will keep working unchanged, since this script still sets `details.open = true/false`, just with a delay for the height animation.

## Boundaries

- Do NOT touch any FAQ question/answer text, `iconify-icon` markup, or the `class` attributes on `<details>`/`<summary>`/`<p>` — visual and copy changes are out of scope.
- Do NOT touch the FAQPage JSON-LD schema blocks (present on several of these pages) — those are static SEO data, unrelated to the interactive `<details>` rendering, and must not change.
- Do NOT add this script to pages without a FAQ section (the 6 remaining pages: `sobre-nosotros.html`, `contacto.html`, `aviso-legal.html`, `politica-privacidad.html`, `politica-cookies.html`, `whatsapp.html` — confirm via `grep -L "<details" *.html` before starting, since the file list above was generated at commit a68fcf2 and could drift).
- Do NOT introduce a build step or bundler — this is a plain `<script src>` include, no import/export, no transpilation.
- If any page's FAQ markup does not match the `summary + *` structure (e.g. multiple elements after `<summary>` instead of one `<p>`), STOP on that page and report instead of guessing which element is "the content."

## Verification

- **Mechanical**: no build step (plain JS file, not a Tailwind utility) — just confirm `public/js/faq-animate.js` is valid JS (`node -c public/js/faq-animate.js` from `ANTIGRAVITY_DECORT/` should exit 0) and that all 15 target pages have exactly one new `<script src="public/js/faq-animate.js" defer></script>` line each (`grep -c "faq-animate.js" *.html` should show `1` for each of the 15 files, `0` or missing for the other 6).
- **Feel check**:
  - On `cortinas-a-medida.html`, click a FAQ question. Confirm the answer expands smoothly over ~350ms (not an instant snap), and the plus/minus icon still swaps correctly in sync with the open state.
  - Click the same question again to close it — confirm it collapses smoothly, not instantly.
  - Click a second FAQ question while the first is still mid-animation — confirm nothing breaks (the `animating` guard on each individual `<details>` should prevent double-triggering on the *same* item; opening a *different* item concurrently should work independently and not be blocked).
  - In DevTools Rendering panel, enable "Emulate CSS media feature prefers-reduced-motion: reduce", reload, and click a FAQ question — confirm it now opens/closes instantly (native `<details>` behavior, no animation), because the reduced-motion guard exits the script before attaching any listeners.
  - Repeat the open/close click test on `index.html` (which has 9 FAQ items, the most on the site) and on one more page (`para-arquitectos.html`) to confirm the shared script behaves identically across pages.
- **Done when**: all 15 pages animate FAQ open/close smoothly, reduced-motion users get instant native behavior with no JS interference, and no FAQ text, schema, or icon behavior changed.
