# 004 — Fullscreen mobile menu: swap `ease-in-out` for a strong `ease-out`

- **Status**: DONE
- **Commit**: a68fcf2
- **Severity**: MEDIUM
- **Category**: Easing & duration
- **Estimated scope**: 1 file (`index.html`), 1 class attribute.

## Problem

The fullscreen mobile nav menu uses `ease-in-out` for both opening and closing:

```html
<!-- index.html:446 — current -->
<div id="mobile-menu" class="fixed inset-0 z-[60] bg-neutral-900 text-arena-100 flex flex-col justify-center items-center gap-8 -translate-y-full transition-transform duration-500 ease-in-out font-display">
```

```js
// index.html:1532-1542 — current, unchanged by this plan
function openMobileMenu() {
    mobileMenu.classList.remove('-translate-y-full');
    ...
}
function closeMobileMenu() {
    mobileMenu.classList.add('-translate-y-full');
    ...
}
```

AUDIT.md's easing decision order states plainly: **"Entering or exiting → `ease-out` (starts fast, feels responsive)."** This is a single rule covering both directions — the menu currently uses the "moving/morphing on screen" curve (`ease-in-out`) instead, which is the wrong category for an open/close drawer. `ease-in-out` eases in at both ends, so the menu feels like it's winding up before it moves, rather than responding immediately to the tap.

## Target

Swap `ease-in-out` for this project's own established strong ease-out curve — `cubic-bezier(0.16, 1, 0.3, 1)` — which is already used three times in this same file for the hero's `.reveal-text` animation (`index.html:54`) and this session's scroll-reveal system (`index.html:157`). Per this project's repo conventions (see below), reuse it rather than introducing AUDIT.md's generic `cubic-bezier(0.23, 1, 0.32, 1)` as a fourth, near-duplicate curve.

Tailwind doesn't have a built-in class for an arbitrary cubic-bezier easing on `transition-transform`, so express it as an arbitrary value:

```html
<!-- index.html:446 — target -->
<div id="mobile-menu" class="fixed inset-0 z-[60] bg-neutral-900 text-arena-100 flex flex-col justify-center items-center gap-8 -translate-y-full transition-transform duration-500 ease-[cubic-bezier(0.16,1,0.3,1)] font-display">
```

Note: no spaces inside the arbitrary-value brackets — Tailwind's arbitrary value syntax requires `cubic-bezier(0.16,1,0.3,1)` with commas but no spaces between the numbers, or the class will fail to compile. Duration stays `duration-500` (500ms is within AUDIT.md's budget for "Modals, drawers: 200–500ms" — no change needed there).

## Repo conventions to follow

- `cubic-bezier(0.16, 1, 0.3, 1)` is this project's existing "strong ease-out for entrances" curve — exemplar at `index.html:54` (`.reveal-text { animation: reveal 0.8s cubic-bezier(0.16, 1, 0.3, 1) forwards; }`) and `index.html:157` (the scroll-reveal system added earlier this session). Reuse this exact curve; do not introduce AUDIT.md's `--ease-out: cubic-bezier(0.23, 1, 0.32, 1)` token as a competing value in the same file.
- This codebase has no Tailwind `theme.extend.transitionTimingFunction` tokens defined yet — the arbitrary-value class (`ease-[cubic-bezier(...)]`) is the correct approach given the current setup, matching how other one-off values are already expressed in this codebase (e.g. `rounded-tl-[120px]`, `shadow-terracotta-500/10`).

## Steps

1. Open `ANTIGRAVITY_DECORT/index.html`.
2. On line 446, replace the class `ease-in-out` with `ease-[cubic-bezier(0.16,1,0.3,1)]`. Leave every other class on that element (`fixed inset-0 z-[60] bg-neutral-900 text-arena-100 flex flex-col justify-center items-center gap-8 -translate-y-full transition-transform duration-500 font-display`) exactly as-is.
3. Run `npm run build` from `ANTIGRAVITY_DECORT/` — this is a new arbitrary-value Tailwind class not previously compiled, so the rebuild is required or the class has zero effect (established project rule).
4. Confirm the new rule landed: `grep -o "cubic-bezier(0.16,1,0.3,1)" public/output.css` should now match at least once more than before (it already appears from other usages, so confirm the count went up by exactly 1, or grep for the specific selector tied to the arbitrary ease class).

## Boundaries

- Do NOT touch `openMobileMenu()` / `closeMobileMenu()` JS logic (`index.html:1532-1542`) — this is a pure CSS timing-function swap, the same class governs both directions and that's fine per AUDIT.md's single "entering or exiting" rule.
- Do NOT change `duration-500`.
- Do NOT touch any other `ease-in-out` occurrence elsewhere in the codebase unless it is also gating a `-translate-y-full` / `-translate-x-full` style enter/exit drawer — grep first (`grep -rn "ease-in-out" *.html`) and confirm any other match is out of scope (e.g. `.animate-scroll-hint`'s `ease-in-out` at `index.html:89` is a different case — constant bobbing motion, not an enter/exit — leave it untouched; that one is covered by plan 003 instead).
- If line 446's class list has changed since the commit stamp (e.g. `ease-in-out` no longer present, or the element restructured), STOP and report instead of guessing which class to replace.

## Verification

- **Mechanical**: `npm run build` exits 0. `grep -n "ease-\[cubic-bezier(0.16,1,0.3,1)\]" index.html` matches line 446.
- **Feel check**:
  - At a mobile viewport (375px), tap the hamburger menu button (`#mobile-menu-btn`). Confirm the fullscreen menu slides down and feels like it starts moving immediately on tap (no perceptible "wind-up" pause before motion begins), unlike the previous `ease-in-out` feel.
  - Tap the close button (`#close-mobile-menu`). Confirm the menu slides back up with the same immediate-start feel.
  - In DevTools, set Animations panel playback to 10% and scrub through the open transition — confirm the curve visibly front-loads the motion (fast start, gentle settle) rather than easing in from a standstill.
- **Done when**: both open and close feel immediate/responsive rather than eased-in, and the rest of the menu (links, CTA, close button) is visually and functionally unchanged.
