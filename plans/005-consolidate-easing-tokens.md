# 005 — Consolidate hand-typed cubic-béziers into CSS custom-property tokens

- **Status**: TODO
- **Commit**: a68fcf2
- **Severity**: LOW
- **Category**: Cohesion & tokens
- **Estimated scope**: 1 file (`index.html`) + 1 doc file (`DESIGN.md`).

## Problem

`index.html` has two identical hand-typed cubic-béziers for entrance motion, plus a third distinct one for the pulsing dot, with no shared token:

```css
/* index.html:54 — current */
.reveal-text {
    animation: reveal 0.8s cubic-bezier(0.16, 1, 0.3, 1) forwards;
    ...
}
```

```css
/* index.html:157 — current (added this session for scroll-reveal) */
.js .reveal-up,
.js .reveal-group > * {
    ...
    transition: opacity 0.7s cubic-bezier(0.16, 1, 0.3, 1), transform 0.7s cubic-bezier(0.16, 1, 0.3, 1);
}
```

```css
/* index.html:81 — current, a different curve, left as-is by this plan */
.animate-pulse-warm {
    animation: pulse-warm 2s cubic-bezier(0.4, 0, 0.6, 1) infinite;
}
```

`cubic-bezier(0.16, 1, 0.3, 1)` is typed out by hand in two places already (three, if plan 004 — the mobile menu ease-out fix — has been applied first, since it reuses this same curve as a Tailwind arbitrary value `ease-[cubic-bezier(0.16,1,0.3,1)]`). This is exactly the "five hand-typed cubic-béziers that almost match" pattern AUDIT.md calls out as a consolidation finding — low risk today at 2-3 occurrences, but the site has no single place that says "this is the project's ease-out," so the next person (or agent) touching motion has nothing to imitate and will likely type a fourth slightly-different value.

## Target

1. Add two CSS custom properties to `index.html`'s existing `<style>` block, at the very top (before the first rule, right after the opening `<style>` tag):

```css
/* index.html — new, first rule inside <style> */
:root {
    --ease-out: cubic-bezier(0.16, 1, 0.3, 1);
}
```

(Only `--ease-out` for now — there is exactly one recurring curve to consolidate at this commit. Do not invent additional tokens like `--ease-in-out` or `--ease-drawer` speculatively; add them in a future pass if and when a second recurring curve appears. `pulse-warm`'s `cubic-bezier(0.4, 0, 0.6, 1)` is used exactly once — leave it as a literal, it is not a duplication yet.)

2. Replace both hand-typed occurrences of `cubic-bezier(0.16, 1, 0.3, 1)` with `var(--ease-out)`:

```css
/* index.html:54 — target */
.reveal-text {
    animation: reveal 0.8s var(--ease-out) forwards;
    ...
}
```

```css
/* index.html:157 — target */
.js .reveal-up,
.js .reveal-group > * {
    ...
    transition: opacity 0.7s var(--ease-out), transform 0.7s var(--ease-out);
}
```

3. If plan 004 (mobile menu ease-out) has already been applied, its Tailwind arbitrary-value class `ease-[cubic-bezier(0.16,1,0.3,1)]` on `#mobile-menu` (index.html:446) **cannot** reference a CSS custom property inside a Tailwind arbitrary value in this way reliably across all Tailwind versions — leave that one as the literal arbitrary value, do not attempt to convert it to `ease-[var(--ease-out)]`. Note this as a known, accepted exception in this plan rather than a gap.

## Repo conventions to follow

- This project already defines design tokens as YAML frontmatter in `DESIGN.md` (colors, typography, spacing) — motion has no equivalent section yet. Adding one keeps this project's documentation pattern consistent (see `DESIGN.md`'s existing `colors:`/`typography:` frontmatter keys as the exemplar to follow in spirit, though CSS custom properties for motion live in `index.html` itself since this is a static multi-page site with no shared stylesheet include).
- `index.html`'s `<style>` block already has section comments (`/* Base Typography */`, `/* Smooth Reveal Animation */`, etc.) — add `:root { --ease-out: ...; }` with a one-line comment in the same style, e.g. `/* Motion tokens */`.

## Steps

1. Open `ANTIGRAVITY_DECORT/index.html`.
2. Immediately after the opening `<style>` tag (before the `/* Base Typography */` comment), insert:
   ```css
   /* Motion tokens */
   :root {
       --ease-out: cubic-bezier(0.16, 1, 0.3, 1);
   }
   ```
3. At `index.html:54` (inside `.reveal-text`), replace `cubic-bezier(0.16, 1, 0.3, 1)` with `var(--ease-out)`.
4. At `index.html:157` (inside `.js .reveal-up, .js .reveal-group > *`), replace both occurrences of `cubic-bezier(0.16, 1, 0.3, 1)` with `var(--ease-out)`.
5. Leave `index.html:81` (`pulse-warm`'s `cubic-bezier(0.4, 0, 0.6, 1)`) untouched.
6. Open `ANTIGRAVITY_DECORT/DESIGN.md`. Add a new `## 7. Motion` section (after the existing `## 6. Do's and Don'ts` section, renumbering is not required — append at the end) documenting: `--ease-out: cubic-bezier(0.16, 1, 0.3, 1)` as "the project's strong ease-out, used for all entrance motion (hero reveal, scroll-reveal, drawer/menu open-close). Reuse this token for any new entrance or exit animation rather than typing a new curve."

## Boundaries

- Do NOT add tokens for curves that only appear once (`pulse-warm`'s curve, `whatsapp-pulse`'s implicit `ease-in-out`, `scroll-hint`'s `ease-in-out`) — only consolidate the one curve that is genuinely duplicated.
- Do NOT touch any other file besides `index.html` and `DESIGN.md`.
- Do NOT touch `tailwind.config.js` — this is hand-written CSS in an inline `<style>` block, not a Tailwind utility, so no `npm run build` is required and no Tailwind config change applies here.
- If a third genuine duplicate of `cubic-bezier(0.16, 1, 0.3, 1)` exists elsewhere in `index.html` beyond lines 54 and 157 at the time this plan runs (e.g. because plan 004 was applied as a raw `<style>` rule rather than a Tailwind arbitrary value — check how plan 004 was actually implemented before assuming), migrate that one too, following the same `var(--ease-out)` substitution.

## Verification

- **Mechanical**: `grep -c "cubic-bezier(0.16, 1, 0.3, 1)" index.html` returns 0 after the edit (both prior occurrences now read `var(--ease-out)`). `grep -c "var(--ease-out)" index.html` returns 2 (or 3, if the plan-004 exception in step 3 above turns out to be migratable after inspection). No build step needed.
- **Feel check**:
  - Reload Home. Confirm the hero's initial fade/slide-up entrance still animates exactly as before (same speed, same curve feel).
  - Scroll to any section with the scroll-reveal system (e.g. Colecciones). Confirm cards still fade/slide in with the same timing as before this change.
  - Both should look pixel-identical in motion to before — this plan changes zero visual behavior, only where the value is defined.
- **Done when**: `var(--ease-out)` is defined once in `:root` and referenced by both `.reveal-text` and the scroll-reveal system, `DESIGN.md` documents it under a new Motion section, and nothing about how the site actually animates has changed.
