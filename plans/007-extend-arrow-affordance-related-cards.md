# 007 — Extend Home's arrow-reveal hover affordance to the "También te puede interesar" cards

- **Status**: DONE
- **Commit**: a68fcf2
- **Severity**: LOW (missed opportunity, cohesion)
- **Category**: Cohesion & tokens / Missed opportunities
- **Estimated scope**: 13 HTML files, 3 cards each (39 `<a>` elements total), same exact edit repeated.

## Problem

Home's Colecciones cards (`index.html:592` onward) have a distinctive, branded hover affordance: a circular arrow icon that fades and slides in from the left on hover, signaling "this is clickable, here's where it goes":

```html
<!-- index.html:600-603 — current, one of 10 Colecciones cards, this affordance is NOT part of this plan's scope, cited only as the exemplar to imitate -->
<div class="w-8 h-8 rounded-full border border-arena-400 flex items-center justify-center opacity-60 md:opacity-0 md:group-hover:opacity-100 transition-opacity translate-x-0 md:-translate-x-2 md:group-hover:translate-x-0 duration-300 text-terracotta-500">
    <iconify-icon icon="lucide:arrow-right" width="14" stroke-width="1.5"></iconify-icon>
</div>
```

The site's other major card-link pattern — the "También te puede interesar" cross-link cards that appear near the bottom of 13 product/B2B pages — has no equivalent directional affordance. It only gets a border-color and shadow change on hover, with no icon signaling navigability:

```html
<!-- cortinas-a-medida.html:340-343 — current, representative of the pattern repeated identically (with different href/text) 3x per page across 13 pages -->
<a href="visillos.html" class="group p-6 bg-arena-100 rounded-2xl border border-arena-300/50 hover:border-terracotta-300 transition-all duration-300 hover:shadow-md">
    <span class="text-[10px] font-bold tracking-widest uppercase text-terracotta-500 font-body block mb-2">Colección Visillos</span>
    <h3 class="text-base font-semibold font-display text-neutral-800 group-hover:text-terracotta-600 transition-colors">Visillos</h3>
    <p class="text-xs text-neutral-400 font-body mt-1">Lino y voile traslúcido a medida.</p>
</a>
```

The 13 pages with this pattern (verified via `grep -l "También te puede interesar" *.html`): `cortinas-a-medida.html`, `cortinas-blackout.html`, `cortinas-confeccionadas.html`, `cortinas-enrollables.html`, `cortinas-verticales.html`, `estor-de-tela.html`, `motorizacion.html`, `paneles-japoneses.html`, `para-arquitectos.html`, `para-hoteles.html`, `plisadas.html`, `venecianas.html`, `visillos.html`. Each has exactly 3 of these cards.

This is a cohesion gap, not a bug: the same underlying interaction (a card that navigates somewhere on click) has two different hover languages on the same site, and the more informative one (Home's arrow) is missing from the pattern used 3x more often (13 pages × 3 cards = 39, vs. Home's 10).

## Target

Add a small header row to each card (`flex justify-between items-start`, wrapping the existing `<span>` eyebrow) with the same circular arrow-reveal treatment used on Home, sized down slightly to fit this card's smaller footprint (`w-6 h-6` instead of Home's `w-8 h-8`, icon `width="12"` instead of `14`):

```html
<!-- cortinas-a-medida.html:340-343 — target -->
<a href="visillos.html" class="group p-6 bg-arena-100 rounded-2xl border border-arena-300/50 hover:border-terracotta-300 transition-all duration-300 hover:shadow-md">
    <div class="flex justify-between items-start mb-2">
        <span class="text-[10px] font-bold tracking-widest uppercase text-terracotta-500 font-body">Colección Visillos</span>
        <div class="w-6 h-6 rounded-full border border-arena-400 flex items-center justify-center opacity-0 group-hover:opacity-100 transition-opacity translate-x-0 group-hover:-translate-x-0 duration-300 text-terracotta-500 shrink-0">
            <iconify-icon icon="lucide:arrow-right" width="12" stroke-width="1.5"></iconify-icon>
        </div>
    </div>
    <h3 class="text-base font-semibold font-display text-neutral-800 group-hover:text-terracotta-600 transition-colors">Visillos</h3>
    <p class="text-xs text-neutral-400 font-body mt-1">Lino y voile traslúcido a medida.</p>
</a>
```

Note: unlike Home's version (which has a `md:` mobile/desktop split because those cards show the arrow faintly at `opacity-60` on mobile with no hover), these smaller related-cards are simpler — no touch device shows `:hover` at all once plan 001 lands, so keep this one un-split: `opacity-0 group-hover:opacity-100` on all breakpoints is correct (mobile users just won't see the arrow reveal at all pre-tap, which is fine, the card itself is still fully tappable).

The `transition-all duration-300` on the parent `<a>` stays as-is here (or becomes plain `transition` if plan 002 has already landed — check current state before assuming) since this plan only adds the new inner arrow element, not the existing hover-driven border/shadow transition.

## Repo conventions to follow

- Copy Home's arrow-affordance markup pattern exactly (`w-N h-N rounded-full border border-arena-400 flex items-center justify-center ... text-terracotta-500` wrapping an `iconify-icon icon="lucide:arrow-right"`) — do not invent a different icon, color, or shape. Exemplar: `index.html:600-603`.
- `iconify-icon` is already the site's icon system (used via a `defer`red `<script src="https://code.iconify.design/iconify-icon/1.0.7/iconify-icon.min.js">` on every page) — no new icon library needed.

## Steps

1. For each of the 13 pages listed in Problem, locate its "También te puede interesar" section (search for the exact string `También te puede interesar`).
2. For each of the 3 `<a>` cards inside that section on that page:
   a. Wrap the existing `<span class="text-[10px] font-bold ...">...</span>` (the eyebrow) in a new `<div class="flex justify-between items-start mb-2">`.
   b. Remove the `mb-2` class from the `<span>` itself (it moves to the new wrapping `<div>`).
   c. Immediately after the `<span>` (still inside the new wrapping `<div>`), add the arrow-reveal `<div>` shown in Target above, keeping the `href`'s destination-appropriate content unchanged — only the markup structure and the new arrow element change, not any text or link.
3. Repeat for all 3 cards on all 13 pages (39 edits total, mechanically identical in structure, differing only in the pre-existing text/href on each card which must not change).

## Boundaries

- Do NOT change any `href`, card text (eyebrow label, `<h3>` title, `<p>` description), or which 3 related pages each card links to.
- Do NOT touch the outer `<a class="group ...">` classes except where explicitly noted (removing `mb-2` from the inner `<span>` only).
- Do NOT touch Home's own Colecciones cards (`index.html`) — they already have this affordance, they are the exemplar, not the target.
- Do NOT apply this to any page without a "También te puede interesar" section — verify the 13-page list above is still accurate (`grep -l "También te puede interesar" *.html`) before starting, in case pages were added/removed since the commit stamp.
- If any of the 39 cards has different markup than the representative example shown (e.g. missing the `<span>` eyebrow, or already has some arrow element), STOP on that specific card and report instead of guessing.

## Verification

- **Mechanical**: `grep -c "arrow-right" *.html` for each of the 13 files should increase by exactly 3 compared to before this plan ran (verify with `git diff --stat` showing only these 13 files touched, 3 new `iconify-icon` blocks each).
- **Feel check**:
  - On `cortinas-a-medida.html`, scroll to "También te puede interesar", hover each of the 3 cards (desktop/mouse emulation). Confirm the small circular arrow fades in on hover, consistent in timing/feel with Home's Colecciones arrow.
  - Confirm the existing border-color and shadow hover feedback on the card still works unchanged alongside the new arrow.
  - Spot-check 2 more pages from the 13 (`motorizacion.html`, `visillos.html`) for the same behavior.
  - Confirm mobile/touch (no hover capability, per plan 001) simply never reveals the arrow — acceptable, the card remains fully tappable and functional without it.
- **Done when**: all 39 related-page cards across the 13 pages show the same arrow-reveal affordance as Home's Colecciones cards on hover, with zero text or link changes.
