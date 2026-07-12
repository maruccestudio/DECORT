# 003 — Respect `prefers-reduced-motion` for the scroll hint and terracotta pulse

- **Status**: TODO
- **Commit**: a68fcf2
- **Severity**: MEDIUM
- **Category**: Accessibility
- **Estimated scope**: 1 file (`index.html`), ~10 new lines.

## Problem

`index.html` has three `@media (prefers-reduced-motion: reduce)` concerns today: one hides the hero video (`index.html:136-138`), and one (added in this session's polish pass) freezes the scroll-reveal system (`index.html:173-179`). Neither covers two infinite-loop animations that also run on Home, one of which moves an element:

```css
/* index.html:76-83 — current, no reduced-motion fallback */
@keyframes pulse-warm {
    0%, 100% { opacity: 1; }
    50% { opacity: 0.5; }
}
.animate-pulse-warm {
    animation: pulse-warm 2s cubic-bezier(0.4, 0, 0.6, 1) infinite;
}
```

```css
/* index.html:85-89 — current, no reduced-motion fallback */
@keyframes scroll-hint {
    0%, 100% { transform: translateY(0); opacity: 0.5; }
    55% { transform: translateY(6px); opacity: 1; }
}
.animate-scroll-hint { animation: scroll-hint 2s ease-in-out infinite; }
```

`scroll-hint` moves the element (`translateY(6px)`) forever, on loop, with no way to turn it off for a user who has set `prefers-reduced-motion: reduce`. AUDIT.md's accessibility rule: reduced motion means fewer/gentler animations, not zero — keep opacity/color feedback, drop movement.

`pulse-warm` (a small terracotta dot, `index.html:560`, `<span class="w-2 h-2 bg-terracotta-500 rounded-full animate-pulse-warm">`) only animates opacity, so it is already reduced-motion-safe in spirit, but per AUDIT.md's own example pattern it's best practice to make this explicit rather than rely on it being "accidentally fine."

Used at:
- `index.html:547` — `<div class="animate-scroll-hint flex flex-col items-center">` (the mobile scroll-hint nudge under the hero).
- `index.html:560` — `<span class="w-2 h-2 bg-terracotta-500 rounded-full animate-pulse-warm"></span>`.

## Target

Add `.animate-scroll-hint` and `.animate-pulse-warm` to the **existing** reduced-motion block at `index.html:173-179` (do not create a third, separate `@media (prefers-reduced-motion: reduce)` block — consolidate into the one already there):

```css
/* index.html:173-179 — target, extending the existing block */
@media (prefers-reduced-motion: reduce) {
    .js .reveal-up, .js .reveal-group > * {
        opacity: 1;
        transform: none;
        transition: none;
    }
    .animate-scroll-hint {
        animation: none;
        opacity: 0.5;
    }
    .animate-pulse-warm {
        animation: none;
    }
}
```

`scroll-hint`'s movement (`translateY`) is fully removed; a static `opacity: 0.5` keeps the hint visible (matching its resting-frame opacity) without motion. `pulse-warm`'s animation is removed entirely since it's opacity-only pulsing on a purely decorative dot with no informational content — freezing it at its natural CSS opacity (1, from `.w-2.h-2` base state, no override needed) is sufficient.

## Repo conventions to follow

- This codebase already consolidates reduced-motion overrides for new motion into a single block rather than scattering multiple `@media (prefers-reduced-motion: reduce)` blocks — follow `index.html:173-179` (added earlier this session) as the exemplar and extend it, do not add a 4th block.
- The existing hero-video reduced-motion block at `index.html:136-138` stays separate since it predates this convention and serves a different purpose (hiding an element vs. freezing an animation) — do not merge it in, just leave it as-is.

## Steps

1. Open `ANTIGRAVITY_DECORT/index.html`.
2. Locate the `@media (prefers-reduced-motion: reduce)` block at line 173 (the one containing `.js .reveal-up, .js .reveal-group > *`).
3. Inside that same block, after the existing `.js .reveal-up, .js .reveal-group > *` rule, add the two new rules shown in Target above (`.animate-scroll-hint` and `.animate-pulse-warm`).
4. Do not touch the `@keyframes pulse-warm`, `@keyframes scroll-hint`, `.animate-pulse-warm`, or `.animate-scroll-hint` base definitions elsewhere in the file — this plan only adds the reduced-motion override, it does not change default (motion-allowed) behavior.

## Boundaries

- Do NOT touch the hero-video reduced-motion block (`index.html:136-138`).
- Do NOT change the base `@keyframes` or `.animate-*` class definitions — only add to the reduced-motion media block.
- Do NOT touch any other file — `scroll-hint`/`pulse-warm` only exist on `index.html` (verified: `grep -l "animate-scroll-hint\|animate-pulse-warm" *.html` returns only `index.html`).
- If the reduced-motion block at line 173 has been modified or removed since the commit stamp, STOP and report instead of creating a new block from scratch.

## Verification

- **Mechanical**: no build step needed (hand-written CSS in a `<style>` block, not a Tailwind utility) — just confirm the HTML is well-formed (`<style>...</style>` still balances, no stray braces) by opening the file and checking the media block's brace count.
- **Feel check**:
  - In Chrome DevTools, open the Rendering panel, set "Emulate CSS media feature prefers-reduced-motion" to "reduce". Reload Home.
  - Confirm the mobile scroll-hint under the hero (`index.html:547`, visible at a mobile viewport width) is static — no vertical bobbing — but still visibly present at ~50% opacity, not vanished.
  - Confirm the small terracotta pulsing dot (`index.html:560`, in the Showroom "Gratis" area or wherever it renders) is static, not fading in and out.
  - Set the emulation back to "no preference" and confirm both animations resume normally (bobbing scroll hint, pulsing dot).
- **Done when**: with reduced motion emulated, neither element moves or pulses, but both remain visible; with no preference set, both animate exactly as before this change.
