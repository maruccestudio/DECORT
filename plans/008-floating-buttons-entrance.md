# 008 — Give the phone/WhatsApp floating buttons an entrance instead of appearing instantly

- **Status**: DONE
- **Commit**: a68fcf2
- **Severity**: LOW (missed opportunity, polish)
- **Category**: Missed opportunities
- **Estimated scope**: 1 file (`index.html`), ~10 new lines. Home only — verified `floating-btns`/`whatsapp-float` exist only on `index.html` (`grep -l "floating-btns" *.html` returns only `index.html`; the other 20 pages have no floating phone/WhatsApp buttons at all, which is a content/conversion question out of scope for this plan).

## Problem

The phone and WhatsApp floating buttons are present at full opacity from the very first paint, with zero entrance:

```html
<!-- index.html:1411-1421 — current -->
<div id="floating-btns" class="fixed bottom-6 right-5 z-[90] flex flex-col items-end gap-2.5 transition-opacity duration-300">
    <button id="scroll-top-btn" ...>...</button>
    <div id="phone-wrap" style="position:relative;">
        <a href="tel:+34641354788" id="phone-float-btn" ...>...</a>
        <div id="phone-tooltip" ...>+34 641 35 47 88</div>
    </div>
    <a href="https://wa.me/..." ... class="whatsapp-float w-11 h-11 bg-[#25D366] ...">...</a>
</div>
```

Note: `#scroll-top-btn` already has its own correct show/hide animation tied to scroll position (`index.html:107-117`, a separate `.visible` class toggle with `opacity`/`transform` transitions) — **that logic is out of scope and must not be touched**. This plan only concerns the two elements that are always visible regardless of scroll: the phone button (`#phone-wrap`) and the WhatsApp button (`.whatsapp-float`).

AUDIT.md Category 8: "Spatially-connected UI... with no motion explaining where it came from" and "Rare, high-emotion moments... rendered with none of the delight budget they're allowed" — a floating conversion CTA that's present on every single page load of Home is a good candidate for a small, one-time arrival moment, cheap to add, that makes the page feel considered rather than assembled.

## Target

Add a `float-in` entrance to the phone and WhatsApp buttons only (not the container, not scroll-top-btn), delayed until just after the hero's own reveal sequence finishes (hero uses `delay-100`/`delay-200` on a `0.8s` animation, finishing around 1s after load — this plan starts at 1.1s so it reads as a deliberate second beat, not part of the same burst):

```css
/* index.html — new rule, add near the other keyframes (after .whatsapp-pulse's @keyframes block, index.html:144-147) */
@keyframes float-in {
    from { opacity: 0; transform: scale(0.9) translateY(8px); }
    to { opacity: 1; transform: scale(1) translateY(0); }
}
.js #phone-wrap,
.js .whatsapp-float {
    animation: float-in 0.4s var(--ease-out) 1.1s backwards;
}
@media (prefers-reduced-motion: reduce) {
    .js #phone-wrap,
    .js .whatsapp-float {
        animation: none;
    }
}
```

Notes on the exact values:
- `scale(0.9)`, not `scale(0)` — per AUDIT.md, nothing in the real world appears from nothing; `0.9` is within the recommended `0.9–0.97` range for a subtle pop.
- `backwards` fill-mode ensures the element stays at its `from` state (invisible) during the `1.1s` delay, instead of flashing at full opacity before the delay elapses.
- Reuses `var(--ease-out)` (this project's established curve — see plan 005; if plan 005 has not landed yet, substitute the literal `cubic-bezier(0.16, 1, 0.3, 1)` instead of the `var()`).
- Gated behind the `.js` class on `<html>` (added synchronously in `<head>`, see `index.html:29-31` from this session's earlier polish pass) for the same anti-FOUC reason as the scroll-reveal system: without JS, or in a renderer where `.js` never gets added, these buttons must default to fully visible, not stuck at `opacity: 0`.
- The reduced-motion override removes the animation entirely (buttons appear instantly, fully visible) rather than keeping a fade — a 1.1s delay before a CTA becomes visible is itself a minor UX cost that reduced-motion users shouldn't have to pay for a decorative entrance.

## Repo conventions to follow

- This project already gates JS-dependent visual state behind the `.js` class on `<html>` — see `index.html:173-179` (the scroll-reveal reduced-motion block) and the `.js` class assignment at `index.html:29-31`. Follow the same pattern here rather than introducing a different anti-FOUC mechanism.
- Reuse `var(--ease-out)` per plan 005's token, or the literal curve if plan 005 hasn't executed yet — do not introduce a fourth easing curve.
- Keyframe naming in this file so far is short and purpose-descriptive (`reveal`, `pulse-warm`, `scroll-hint`, `whatsapp-pulse`) — `float-in` matches that convention.

## Steps

1. Open `ANTIGRAVITY_DECORT/index.html`.
2. After the existing `@keyframes whatsapp-pulse { ... }` block (`index.html:144-147`), add the `@keyframes float-in` block and the `.js #phone-wrap, .js .whatsapp-float { animation: ... }` rule shown in Target above.
3. Add the `@media (prefers-reduced-motion: reduce)` override shown in Target — append it to the **existing** reduced-motion block at `index.html:173` if plan 003 has already added `.animate-scroll-hint`/`.animate-pulse-warm` rules there, following the same consolidation approach as plan 003; otherwise create the addition as its own block only if no other reduced-motion block exists yet at that location (check current file state first).
4. Do not add any class to the HTML elements themselves — the CSS selectors `#phone-wrap` and `.whatsapp-float` already exist as-is on the elements at `index.html:1415` and `index.html:1421`, no markup changes needed.

## Boundaries

- Do NOT touch `#scroll-top-btn` or its existing `.visible` class toggle logic (`index.html:107-117` and the JS that adds/removes `.visible` on scroll) — that is a correct, separate, already-animated pattern.
- Do NOT touch `#floating-btns` (the parent container) — apply the entrance to the two inner elements only, so the container's own `transition-opacity duration-300` (used for some other purpose — check before assuming it's unused) is left alone.
- Do NOT change the phone tooltip (`#phone-tooltip`) behavior or timing.
- Do NOT add this to any other page — floating buttons don't exist elsewhere at this commit.
- If `#phone-wrap` or `.whatsapp-float` selectors are no longer present at the cited lines (structure changed since the commit stamp), STOP and report instead of guessing new selectors.

## Verification

- **Mechanical**: no build step (hand-written CSS in `<style>`, not a Tailwind utility). Confirm the `<style>` block remains well-formed (matching braces) after the edit.
- **Feel check**:
  - Hard-reload Home (disable cache) at desktop width. Confirm the phone and WhatsApp buttons are invisible for about the first second, then pop in together with a subtle scale+fade, arriving just after the hero content has settled — not competing with it, not perceptibly delayed to the point of feeling broken.
  - Confirm `#scroll-top-btn` continues to behave exactly as before (hidden until scrolling past the hero, no change to that logic).
  - In DevTools Rendering panel, emulate `prefers-reduced-motion: reduce`, hard-reload. Confirm phone and WhatsApp buttons are visible immediately, with no 1.1s delay and no animation.
  - Confirm this only affects `index.html` — spot check one other page (`cortinas-a-medida.html`) has no floating buttons at all, unchanged from before.
- **Done when**: the phone/WhatsApp buttons arrive with a single deliberate, subtle entrance after the hero settles, reduced-motion users see them instantly, and scroll-top-btn's independent behavior is untouched.
