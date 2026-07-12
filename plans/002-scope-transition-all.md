# 002 — Replace `transition-all` with scoped `transition`

- **Status**: DONE
- **Commit**: a68fcf2
- **Severity**: MEDIUM
- **Category**: Performance
- **Estimated scope**: 21 HTML files, ~306 mechanical occurrences of one exact string.

## Problem

`transition-all` (Tailwind class) compiles to `transition-property: all` in `public/output.css`:

```css
/* public/output.css — current, class .transition-all */
.transition-all{transition-property:all;transition-timing-function:cubic-bezier(.4,0,.2,1);transition-duration:.15s}
```

AUDIT.md flags `transition: all` as always a finding: it watches every animatable property, including layout-triggering ones (`width`, `height`, `margin`, `padding`, `top`, `left`), even when the element never actually changes those on interaction. It is used 306 times across all 21 HTML pages, e.g.:

```html
<!-- ANTIGRAVITY_DECORT/index.html:593 — current -->
<img ... class="w-full h-full object-cover grayscale-[30%] transition-all duration-700 group-hover:grayscale-0 group-hover:scale-105" ...>
```

Recon of every `transition-all` element's paired `hover:`/`group-hover:`/`active:` utilities (grep across all 21 files) confirms the properties actually changing are always among: border-color, box-shadow, background-color, text color, transform (`scale-*`, `-translate-y-*`), `grayscale-*` (filter), and opacity. **No element anywhere in the codebase changes `width`, `height`, `margin`, `padding`, `top`, `left`, `right`, or `bottom` on `hover:`/`group-hover:`/`active:`** (verified: `grep -ohE 'class="[^"]*transition-all[^"]*"' *.html | grep -oE "(hover:|group-hover:)(w-|h-|m[trblxy]?-|p[trblxy]?-|top-|left-|right-|bottom-)[a-zA-Z0-9\[\]/.]*"` returns nothing).

## Target

Tailwind's plain `transition` utility (no `-all` suffix) already compiles to exactly the safe, non-layout property list this codebase needs:

```css
/* public/output.css — Tailwind's built-in .transition, already present, unmodified */
.transition{transition-property:color,background-color,border-color,text-decoration-color,fill,stroke,opacity,box-shadow,transform,filter,backdrop-filter;transition-timing-function:cubic-bezier(.4,0,.2,1);transition-duration:.15s}
```

Every one of the 306 `transition-all` occurrences becomes `transition` (drop the `-all` suffix only — keep the exact same `duration-*` class that already follows it on each element, do not change durations here, that's plan 004/005's job if anything).

```html
<!-- ANTIGRAVITY_DECORT/index.html:593 — target -->
<img ... class="w-full h-full object-cover grayscale-[30%] transition duration-700 group-hover:grayscale-0 group-hover:scale-105" ...>
```

## Repo conventions to follow

- This is a pure Tailwind utility swap — no custom CSS, no new classes, no config changes. Tailwind's default `transition` utility is already compiled into `public/output.css` (used elsewhere in the codebase), so no rebuild-breaking risk from a missing class.
- Rebuild via `npm run build` from `ANTIGRAVITY_DECORT/` is still required after the HTML edits, per this project's established rule (`tailwindcss -i ./src/input.css -o ./public/output.css --minify`, no browser JIT) — even though `transition` was likely already compiled in from other usages, always rebuild after any HTML class change to keep the committed CSS reproducible.

## Steps

1. In `ANTIGRAVITY_DECORT/`, run a literal string replacement across all `*.html` files: every occurrence of the exact substring `transition-all` becomes `transition`. This must match `transition-all` as a whole word within a `class="..."` attribute (word boundary on both sides) — do not match it as a substring of some other class name (none exist in this codebase, but check).
   - Example command (verify count before/after): `grep -c "transition-all" *.html` before the edit should sum to ~306; after, it should be 0 in every file.
2. Do not touch anything else on the matched lines — same `duration-*`, same `hover:`/`group-hover:`/`active:` utilities, same everything else in the `class` attribute.
3. Run `npm run build` from `ANTIGRAVITY_DECORT/`.
4. Re-run `grep -c "transition-all" *.html` — must return 0 for every file. Re-run `grep -c "\btransition\b" public/output.css` (or equivalent) to confirm the compiled `.transition{...}` rule is present and unchanged from the snippet in Target above.

## Boundaries

- Do NOT change any `duration-*` value — that's out of scope for this plan.
- Do NOT change any `hover:`/`group-hover:`/`active:` utility values.
- Do NOT touch `tailwind.config.js` (that's plan 001's scope).
- Do NOT touch inline `<style>` blocks (`@keyframes`, `.reveal-up`, `.btn-press`, etc.) — those are hand-written CSS, not the Tailwind `transition-all` utility, and are out of scope here.
- If any file has a `transition-all` occurrence where the paired hover/active utility changes a layout property (width/height/margin/padding/top/left/right/bottom) that this plan's recon missed, STOP on that specific occurrence, do not swap it to `transition`, and report it as an exception instead (it would need a scoped `transition-[...]` arbitrary value, not the plain default).

## Verification

- **Mechanical**: `grep -c "transition-all" *.html` returns 0 for all 21 files. `npm run build` exits 0. `git diff --stat` shows only the expected files changed, with a 1-for-1 line-count-neutral diff (same number of lines, only `transition-all` → `transition` substitutions).
- **Feel check**:
  - On Home, hover a Colecciones card (desktop/mouse emulation): confirm the grayscale→color and scale-105 transition still animates smoothly over 700ms, no visual change from before.
  - On Home, hover a Showroom feature card: confirm the shadow-lift (`shadow-2xl`) and `-translate-y-2` still animate together, no stutter.
  - Open DevTools Performance panel, record a hover interaction on a card grid before and after — confirm no new layout/reflow entries appear (there shouldn't have been any before either, this is a defensive check).
- **Done when**: zero `transition-all` occurrences remain, the build is green, and hovering any previously-affected element on Home and on one product page (`cortinas-a-medida.html`) looks and feels identical to before the change.
