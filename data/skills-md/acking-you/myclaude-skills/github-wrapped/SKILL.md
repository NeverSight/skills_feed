---
name: github-wrapped
description: Generate a verifiable GitHub Wrapped year-in-review as a single-file HTML (raw gh API JSON saved, Python-built dataset embedded), with a Bilibili-style narrative, smooth transitions, and mobile-friendly paged mode. Requires gh CLI to be authenticated.
---

# GitHub Wrapped (Single-file HTML, Verifiable Data)

This skill generates a GitHub “Year in Review / Wrapped” as a **single self-contained HTML file** with a **Bilibili-style narrative** (scroll/page scenes, cinematic transitions, share card). The non-negotiable requirement is **verifiability**: every number must be traceable to saved `gh api` raw responses committed alongside the report.

## Non-negotiables

- **No fabricated data**: if GitHub APIs cannot provide a metric, show `—` and explain the limitation in-page.
- **Save raw API responses**: the report is invalid without a `raw/` folder containing the original JSON (and the GraphQL queries used).
- **Ship one `.html`**: no runtime `gh` calls; embed a dataset into the HTML.
- **External CDNs are optional** (fonts/icons/screenshot libs/music) but must never break core navigation/rendering if they fail to load.
- **Build step-by-step**: start with a tiny scaffold (≤ ~400 LOC) and iterate towards a 5k–10k LOC finished report; never try to ship the full “final” file in one pass.

## What to ask the user first

- `YEAR` (default: current year)
- `USER` (default: `gh api user --jq .login`)
- Output language for the page copy (Chinese is usually preferred for CN users; this doc stays English)
- Timezone (default: `Asia/Shanghai` for CN users)
- Whether to enable a music widget (autoplay may be blocked; must have a user-gesture fallback)

## Recommended layout

```
data/github-wrapped-$YEAR/
  raw/                  # verifiable gh API responses (JSON)
  processed/             # dataset.json derived from raw/
frontend/standalone/
  github-wrapped-$YEAR.html
```

## Pipeline (raw → dataset → single HTML)

### 1) Collect raw JSON with `gh api` (always paginate)

Pagination rules:

- GraphQL: `--paginate --slurp`
- REST: `--paginate`

Minimum raw set (recommended filenames):

- `raw/user.json` (profile, createdAt)
- `raw/contributions.json` (GraphQL `contributionsCollection(from,to)`)
- `raw/user_repos.json` (REST repos list; stars/forks are snapshots)
- `raw/starred_repos_pages.json` (GraphQL starred repos ordered by `STARRED_AT`, includes topics/language)
- `raw/prs_${YEAR}_pages.json` (GraphQL Search: merged PRs in the year; additions/deletions)
- `raw/contributed_repos_pages.json` (GraphQL `repositoriesContributedTo`)
- `raw/events_90d.json` (optional; REST events; **90-day limit**; only for best-effort easter eggs)

Bundled templates (open only what you need):

- `scripts/collect_raw.sh`
- `scripts/queries/*.graphql`
- `references/data_sources.md`
- `references/single_file_engineering.md`

### 2) Build a deterministic dataset (Python, no guessing)

Write a builder that reads only `raw/*.json` and outputs `processed/dataset.json`:

- Deterministic: same raw input → same dataset output.
- Transparent: write limitations into `meta.dataProvenance.notes[]`.
- Stable for rendering: keep optional fields nullable; avoid breaking changes.

Template: `scripts/build_dataset_template.py`
Schema guidance: `references/dataset_schema.md`

For larger analysis recipes (stars-by-month scatter points, timezone-safe hour buckets, holiday detection, category heuristics), see `cookbook/python/`.

### 3) Embed `dataset.json` into the HTML (no runtime fetch)

Your HTML must contain a stable anchor:

```html
<script id="dataset" type="application/json">{}</script>
```

Embed rules:

- Always escape `<` as `\u003c` before writing into the HTML.
- If the dataset block is missing/corrupted, the embed script should fail loudly (or repair it).
- The page must show a visible overlay if dataset parsing fails (avoid “cover only, buttons dead”).

Template: `scripts/embed_dataset_into_html_template.py`

## Step-by-step delivery (400 LOC → 10k LOC)

Single-file cinematic reports get long fast. To stay correct and maintainable, **ship in iterations**:

- **Iteration 0 (contract)**: agree on a minimal `dataset.json` schema and render placeholders (show `—` for missing fields).
- **Iteration 1 (≤ 400 LOC)**: build the skeleton: cover + “Start”, 2–3 scenes, nav mode toggle stub, dataset parse with a visible failure overlay.
- **Iteration 2 (≤ 1.5k LOC)**: implement the navigation engine (paged/free), reveal system, and a basic card/list system.
- **Iteration 3 (≤ 4k LOC)**: add core charts (heatmap, tower, radar), but keep them simple and verifiable.
- **Iteration 4 (≤ 7k LOC)**: add mobile paged-mode strategy (hide heavy blocks via `data-mhide="paged"` + bottom-sheet that moves DOM nodes).
- **Iteration 5 (≤ 10k LOC)**: polish (motion tokens, full-screen HUD, share card, optional music/fireworks), and do a regression pass for desktop + mobile.

Keep this file (SKILL.md) **high-level**. Put long code samples and analysis recipes into `cookbook/` and implementation notes into `references/` to avoid prompt bloat.

## Single-file HTML engineering notes (battle-tested)

- **Boot layer**: always include an explicit “Start” button; do not rely on scroll-only starts.
- **Two navigation modes**: `paged` (wheel/keys, plus touch swipe on mobile) and `free` (normal scroll).
- **Mobile paged mode**: each scene must fit one viewport; hide heavy blocks via `data-mhide="paged"` and open them in a bottom-sheet that moves existing DOM nodes (avoid duplicate IDs).
- **Touch affordances**: heatmap tap → toast; radar touchstart → point lift + tooltip.

See `references/single_file_engineering.md` for deeper patterns.

## Responsive UX (Desktop + Mobile) — hard-won lessons

The page is one file, but it’s effectively two products: **desktop cinematic** and **mobile slide deck**. Treat responsive work as **surgically isolated** changes to avoid regressions.

### Desktop (readable without full-screen)

- Prefer a wide-but-bounded content column (`--maxw` as a `clamp()`), and reduce `--gutter` slightly on short viewports (e.g. 768px height) instead of shrinking typography.
- Use **density variants** rather than truncating content:
  - Multi-column lists for long leaderboards (keep metadata visible).
  - “Dense” list styling (tighter padding/gaps) for better above-the-fold readability.
- Avoid CSS-stretching canvases (radar charts): size canvas from its rendered rect and DPR, or enforce an `aspect-ratio` and draw in CSS pixels.
- If a 3D/transform section makes buttons unclickable, assume a stacking-context problem first (z-index + transforms + pointer-events).

### Mobile (paged-mode = slide deck)

- Gate layout changes with `@media (max-width: 620px) and (pointer: coarse)` (width-only rules can accidentally affect small desktop windows).
- In mobile `paged` mode, avoid inner scrolling in scenes; hide heavy blocks with `data-mhide="paged"` and expose them via a bottom-sheet modal that **moves the existing DOM node** (so IDs and event listeners remain valid).
- Use touch-first affordances: tap feedback (toast), big hit targets, and optionally draggable floating controls (mode toggle / music) respecting safe-area insets.

For implementation patterns (bottom sheet node-moving, draggable HUD controls, canvas DPR sizing, and stacking-context pitfalls), see `references/responsive_ui_patterns.md`.

## Narrative + UI quality bar (Bilibili-style pacing)

Design as a storyboard: each scene answers **one** question, then transitions.

Suggested pacing:

1. Grand cover + “Start” (cinematic; optional fireworks)
2. “How long since we met GitHub” (account createdAt → years)
3. “Your 2025 pulse” (activity tier + distribution)
4. Heatmap/city + streak + craziest day
5. “Time Tower” (12 months; month selector + star-time scatter points)
6. “Radar / hexagon” (categories; points lift/glow on hover or touch)
7. “New interests unlocked” (2025 stars vs previous years)
8. “Extreme moments” (night-owl / holidays; clearly mark best-effort)
9. “Open Source Award” (external contribution highlight; award ceremony feel)
10. Finale share card (screenshot-friendly; optional fireworks)

Interaction rules:

- Every button/card should be clickable with feedback (links when available; otherwise micro-interaction/toast).
- “Free scroll” vs “Page mode” must behave differently (page mode should snap/lock navigation by wheel/keys, and support touch swipe on mobile).
- Unify motion tokens (duration/easing) across scenes; prefer `transform/opacity`.

## Known data limits (must disclose)

- Contribution calendar provides **day-level counts**, not a complete commit list per day.
- Events API keeps only **~90 days** of history.
- Repo `stargazers_count/forks_count` are **current snapshots**, not year-increment.
- Private contributions / hidden settings can skew the public view.

## Debug checklist

See `references/debug_checklist.md` for the full checklist. Common root causes:

- A JS parse error stops all handlers (duplicate `const`, missing `)`)
- A broken embedded dataset block breaks JSON parsing
- A blocked external script was treated as required instead of optional

## Bundled resources (progressive disclosure)

- `scripts/`: reusable collection/build/embed templates (execute without loading into context)
- `cookbook/`: analysis recipes and larger Python snippets (open only what you need)
- `references/`: schema + storyboard + debugging notes (open only the specific file you need)
