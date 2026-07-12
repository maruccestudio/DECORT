# 001 — Gate all `hover:` motion behind `(hover: hover) and (pointer: fine)`

- **Status**: TODO
- **Commit**: a68fcf2
- **Severity**: HIGH
- **Category**: Accessibility
- **Estimated scope**: 1 file (`tailwind.config.js`) + 1 rebuild. No HTML changes.

## Problem

None of the 21 pages gate `hover:` motion to devices that actually support hovering. On touch devices, tapping a card or button triggers the `:hover` state, which then stays "stuck" (scaled image, shifted color, moved arrow icon) until the user taps elsewhere on the page. This is a real UX bug, not a cosmetic one, on a site whose own brand knowledge base (`knowledge_base/kb_marca_ux.md`) explicitly requires audits to be strict about mobile, since DECORT's traffic and conversion funnel are mobile-first.

Example of the pattern repeated across every page, `index.html:593` (verbatim, one of ~300+ occurrences of `hover:` across the 21 HTML files):

```html
<!-- ANTIGRAVITY_DECORT/index.html:593 — current -->
<img src="public/images/cortinas_a_medida.webp" ... class="w-full h-full object-cover grayscale-[30%] transition-all duration-700 group-hover:grayscale-0 group-hover:scale-105" ...>
```

`tailwind.config.js` currently has `plugins: []` — no custom variants defined, so Tailwind's default `hover:` variant compiles to a plain `&:hover` rule with no media gating.

## Target

Redefine the `hover` variant globally in `tailwind.config.js` so **every** `hover:*` utility across the compiled CSS (all 21 HTML files, zero HTML edits needed) only applies under `(hover: hover) and (pointer: fine)`:

```js
/* ANTIGRAVITY_DECORT/tailwind.config.js — target */
const plugin = require('tailwindcss/plugin')

/** @type {import('tailwindcss').Config} */
module.exports = {
  content: ['./*.html', './src/**/*.css'],
  theme: {
    extend: {
      colors: { /* ...unchanged... */ },
      fontFamily: { /* ...unchanged... */ },
    },
  },
  plugins: [
    plugin(function ({ addVariant }) {
      addVariant('hover', '@media (hover: hover) and (pointer: fine) { &:hover }')
    }),
  ],
}
```

No changes to `colors`, `fontFamily`, or any other part of `theme.extend` — only `plugins` changes.

## Repo conventions to follow

- Tailwind is compiled via `npm run build` (`tailwindcss -i ./src/input.css -o ./public/output.css --minify`) — there is no browser JIT. **After editing `tailwind.config.js`, `npm run build` MUST be run**, or the change has zero effect on the live site. This has caused real shipped bugs earlier in this project's history (missing classes in the committed CSS) — do not skip the rebuild.
- `tailwindcss/plugin` is the standard way to add/override variants; it ships with the `tailwindcss` package already installed in this project (check `package.json` / `node_modules/tailwindcss` — do not add a new dependency).

## Steps

1. Open `ANTIGRAVITY_DECORT/tailwind.config.js`.
2. Add `const plugin = require('tailwindcss/plugin')` as the first line.
3. Replace `plugins: []` with the `plugins: [ plugin(...) ]` block shown in Target above. Leave everything else in the file untouched.
4. Run `npm run build` from `ANTIGRAVITY_DECORT/`.
5. Confirm `public/output.css` changed: `grep -o "hover:hover.*pointer: fine" public/output.css | head -1` should now show the media-query wrapping (or grep for `@media (hover: hover)` and confirm it appears immediately before the compiled hover rules).

## Boundaries

- Do NOT touch any of the 21 HTML files — this fix is designed to require zero HTML changes.
- Do NOT change `theme.extend.colors` or `theme.extend.fontFamily`.
- Do NOT add any new npm dependency — `tailwindcss/plugin` is a subpath of the already-installed `tailwindcss` package.
- If `tailwind.config.js` has been restructured since the commit stamp above (e.g. converted to ESM, or `plugins` already has entries), STOP and report instead of guessing how to merge.

## Verification

- **Mechanical**: `npm run build` exits 0. `grep -c "hover: hover" public/output.css` returns a number > 0 (was 0 before).
- **Feel check**:
  - Open the site with Chrome DevTools device toolbar set to a touch device (e.g. "iPhone 12", which reports `(hover: none) and (pointer: coarse)`), tap a Colecciones card image on Home. Confirm the grayscale→color / scale-105 hover effect does **not** trigger on tap.
  - Switch back to desktop/mouse emulation, hover the same card. Confirm the effect still triggers normally with a mouse.
  - Spot-check one non-Home page (`cortinas-a-medida.html`) the same way — the fix is global, so it must apply there without any page-specific edit.
- **Done when**: `public/output.css` wraps hover rules in the media query, mouse hover behavior on desktop is unchanged, and tap-triggered "stuck hover" no longer occurs on a touch-emulated viewport.
