# Design Audit — Scanning an Existing App for Generic / AI-Generated Design

Use this file when asked to review, scan, or audit an existing app or website — "does this look AI-generated?", "make this look unique", "design review of my site". The output of this workflow is an **audit report** (template below), not a rewrite. Only redesign after the user has seen the findings, unless they explicitly asked you to fix things in the same pass.

Why this exists: "AI-generated" is not one smell, it's a *co-occurrence* of safe defaults. Any single signal below appears in plenty of intentional human work. The audit's job is to collect evidence, weigh it, and distinguish "committed aesthetic with familiar ingredients" from "the default look that emerges when no one made a decision."

## Workflow

1. **Inventory the surface.** Find the styling sources: CSS/SCSS files, Tailwind classes in JSX/TSX/Vue/Svelte templates, CSS-in-JS, theme/token files, font imports (`<link>` to Google Fonts, `@font-face`, `@import`).
2. **Run the signal scan** (table below). Prefer the bundled script — `python scripts/scan_slop.py <path>` — which produces a hex-color census and signature hits with file:line evidence. Without the script, run the grep patterns manually.
3. **Take a color census.** Extract every hex/rgb/hsl value and cluster them. You're looking at the *palette as a whole*: is it a warm-cream + terracotta scheme? Tailwind's default purple/indigo? Or a considered, specific palette?
4. **Apply the intentionality test** (below) before scoring — this is what prevents false positives.
5. **Score with the rubric** and write the report using the template.
6. **If a browser is available** (Playwright tools, or the app can be served): screenshot at 375px, 768px, and 1440px, and pull computed styles (`getComputedStyle(document.body).fontFamily`, palette of rendered elements). Visual confirmation upgrades confidence, but the source-based scan alone is a complete audit — never skip the audit because you can't render the app.

## Detection Signals

Tier 1 signals are hallmarks — each one alone suggests AI-default design. Tier 2 are supporting signals — meaningful in combination. Tier 3 are weak signals — only mention them when Tier 1/2 evidence already exists.

| Tier | Signal | How to detect |
|---|---|---|
| 1 | Cream/warm off-white page background (`#faf8f5`, `#f8f6f3`, `#fdfcfb` family) | Hex census: background colors ≥ `#f8` with red ≥ green ≥ blue (warm cast) |
| 1 | Terracotta/coral/rust accent family (`#c45c48`, `#e07860`, `#d4715f`) | Hex census: mid-tone colors with red dominant, green ≈ 40–60% of red |
| 1 | Purple/indigo gradient, especially on white | `grep -riE 'linear-gradient[^;]*(#[78][0-9a-f]|purple|violet|indigo)'` and Tailwind `(from\|via\|to)-(purple\|indigo\|violet)-[0-9]+` |
| 1 | Generic font as the display face: Inter, Roboto, Arial, Poppins, DM Sans, Plus Jakarta, Manrope, Space Grotesk | `grep -riE 'font-family[^;}]*(inter\|roboto\|poppins\|dm sans\|plus jakarta\|manrope\|space grotesk)'` + check font `<link>`/imports |
| 1 | Sparkle/rocket emoji or ✨ icon branding an "AI" feature | `grep -rn '✨\|🚀\|🤖'` in markup |
| 2 | Pill-shaped buttons/badges as the default | `grep -riE 'border-radius:\s*(9999px\|999px\|50rem\|100px)'`, Tailwind `rounded-full` on buttons |
| 2 | Uniform generous radii (12–24px) on every card/input | `grep -riE 'border-radius:\s*(1[2-9]\|2[0-4])px'`, Tailwind `rounded-(xl\|2xl\|3xl)` everywhere |
| 2 | `transition: all 0.3s ease` (or `duration-300` + `transition-all`) as the only motion idea | `grep -riE 'transition:\s*all'` |
| 2 | Card hover-lift: `translateY(-Npx)` + bigger soft shadow | `grep -riE 'hover[^{]*\{[^}]*translateY\(-' ` or adjacent hover shadow+transform rules |
| 2 | Warm/colored tinted shadows (`rgba` of the accent color in `box-shadow`) | Compare `box-shadow` rgba values against accent hue |
| 2 | Left-border accent stripe on cards | `grep -riE 'border-left:\s*[3-6]px solid'` |
| 2 | Emoji as feature icons | Emoji characters inside icon/feature markup |
| 2 | Interchangeable startup copy: "Supercharge", "Seamless", "Unlock your potential", "Everything you need to", "all in one platform" | `grep -riE 'supercharge\|seamless\|unlock (your\|their)\|everything you need\|all.in.one platform\|transform your'` |
| 2 | Gradient text on the hero headline (`background-clip: text`) | `grep -riE 'background-clip:\s*text\|text-fill-color'` |
| 3 | Tailwind default palette used raw (`blue-500` `#3b82f6`, `gray-*`) with no custom theme | Hex census matches Tailwind defaults; no `theme.extend.colors` |
| 3 | Every section centered, identical vertical rhythm, 3-or-4-up feature grid | Read the layout: `text-align: center` + `auto-fit minmax` grid + hero/features/CTA/footer skeleton |
| 3 | Fixed px font sizes with no fluid scale | No `clamp()` anywhere; `font-size: NNpx` throughout |
| 3 | No dark mode, no `prefers-reduced-motion`, no logical properties | Absence of `prefers-color-scheme`, `prefers-reduced-motion`, `margin-inline` |

## The Intentionality Test (run BEFORE scoring)

A committed aesthetic can legitimately use familiar ingredients — a serif + red accent is not slop on an editorial site; near-black brutalism is not "missing dark mode polish". Before scoring, look for evidence someone made decisions:

- **A specific font pairing** chosen for the context (display + body from different families, non-default weights/optical features) rather than one generic sans everywhere.
- **A palette with a point of view**: few colors, precise values, used consistently via tokens — rather than Tailwind defaults or the cream/terracotta comfort zone.
- **Consistent geometry**: the corners, rules, and spacing follow one system (all sharp, all hairline rules, one radius) rather than "rounded because that's the default".
- **Context-specific details**: copy, ornament, or layout that could only belong to *this* product (a drop cap in a journal, baker's-math footnote, waitlist counter for a shaper). Slop is interchangeable; design is specific.
- **Deliberate motion**: few transitions, chosen properties and durations — not `all 0.3s ease` sprayed everywhere.

If three or more of these hold, the design passes the intentionality test: discount all Tier 2/3 signals (they're ingredients, not defaults) and report only genuine Tier 1 collisions as minor notes. If the test fails, score everything at face value.

## Scoring Rubric

Score = (Tier 1 hits × 3) + (Tier 2 hits × 2) + (Tier 3 hits × 1), after intentionality discounting.

| Score | Verdict |
|---|---|
| 0–3 | **Low** — reads as designed; note the few signals as minor polish items |
| 4–8 | **Medium** — leaning generic; the design works but is forgettable; targeted changes will fix it |
| 9+ | **High** — reads as AI-generated/template default; recommend a committed redesign direction |

Report the score with its inputs (which signals, where) — never as a bare number. Confidence comes from co-occurrence: cream + terracotta + Inter + pills together are near-conclusive; any one alone is not.

## Report Template

ALWAYS structure the audit output like this:

```markdown
# Design Audit — <project name>

## Verdict
AI-generated look likelihood: <Low | Medium | High> (score N)
<2–3 sentence summary: what the design currently reads as, and the single biggest reason.>

## Evidence
| Signal | Tier | Where |
|---|---|---|
| <signal> | 1/2/3 | <file:line or class name> |

## What's already working
<Genuine strengths to keep — every real project has some. If the intentionality test passed, say so explicitly.>

## Recommended direction
<For Medium/High: ONE committed aesthetic direction (or two options), made concrete: named fonts, specific palette values, geometry rule, one motion idea. Tie it to the product's actual context. "Be bold" is not a recommendation.>

## Fix list
1. <Quick wins — mechanical swaps: fonts, palette tokens, radii, transitions>
2. <Deeper changes — layout/identity work>
```

## Worked Example: slop card → designed card

Before (scores as Tier 2 × 4 — pill radius, hover lift, tinted shadow, transition-all):

```css
.feature-card {
  background: #fdfcfb;
  border-radius: 16px;
  border-left: 4px solid #e07860;
  box-shadow: 0 4px 16px rgba(196, 92, 72, 0.06);
  transition: all 0.3s ease;
}
.feature-card:hover { transform: translateY(-4px); }
```

After — same component, for a field-recording archive with an instrumentation aesthetic (sharp geometry, hairline rules, one accent, one deliberate transition):

```css
.feature-card {
  background: var(--panel);            /* #101418 */
  border: 1px solid var(--hairline);   /* #2a3138 */
  border-radius: 0;
  padding-block: var(--space-4);
}
.feature-card:hover { border-color: var(--signal); } /* #ffb000, 120ms border-color only */
```

The "after" isn't universally correct — it's correct *for that product*. The fix for slop is always a specific direction, never a better default.

## Common Audit Mistakes

- **Flagging ingredients instead of defaults.** A serif font, a red accent, or a rounded button is not evidence by itself. Run the intentionality test first.
- **Recommending a redesign to a Low-verdict project.** If it passes, say it passes and stop.
- **Vague remediation.** Every High/Medium verdict must end in named fonts, hex values, and geometry rules the user could apply today.
- **Auditing only the CSS.** Tailwind utility classes in components carry most of the evidence in modern React apps; scan JSX/TSX too.
- **Skipping evidence.** Every claim gets a file:line or class-name citation so the user can verify.
