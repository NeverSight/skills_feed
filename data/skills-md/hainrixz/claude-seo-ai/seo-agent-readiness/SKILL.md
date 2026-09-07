---
name: seo-agent-readiness
description: "Audit how well a page can be operated by AI agents and agentic browsers — semantic interactive controls (<button>/<a href> instead of div/span click handlers), named buttons and links, labeled form controls, no javascript: hrefs, primary content outside iframes, and WebMCP detection — following Google's generative-AI guidance and the web.dev agent-friendly websites guide. Module M22 \"Agent-readiness\". Feeds the AI Visibility score (weight 4, all directional)."
allowed-tools: Read, Grep, Glob, Bash
---

# seo-agent-readiness (M22 — Agent-readiness)

Google's *Optimizing your website for generative AI features* guide points to "agent-friendly website best practices" (web.dev *Build agent-friendly websites*): agents drive a page through its accessibility tree, so unnamed, non-semantic, or script-only controls are invisible to them. This module checks the statically checkable subset and names the rest. Alt text is M9, anchor-text quality is M10, rendering is M4 — reference them, never re-emit them.

## Inputs
Work from the PageSnapshot named in your dispatch envelope: read `parsed` (`anchors[]`, `forms`, `iframes`, `scripts[]`, `landmarks`) from `<run_dir>/pages/<slug>.json`, preferring `parsed_rendered` when `render.used` is not `none`; Grep `pages/<slug>.html` (or `.rendered.html`) for the offending elements as verbatim evidence. Deterministic findings already emitted by `audit.mjs` are listed in `<run_dir>/findings.deterministic.json` — do not re-emit those ids; add model-judged findings only. If invoked directly with a URL/path and no snapshot exists, first run `node "${CLAUDE_PLUGIN_ROOT}/scripts/snapshot.mjs" <target> --out "${CLAUDE_PLUGIN_DATA}/runs"` and use the printed snapshot path.

## Audits
1. **Semantic controls** — interactive behavior on `div`/`span` (`onclick`, `role="button"`, `tabindex` + handler) instead of `<button>` / `<a href>`; count against total controls.
2. **Named buttons** — `<button>`, `role="button"`, `input[type=button|submit]` with no text content, `aria-label`, `aria-labelledby`, `title`, or `value`.
3. **Named links** — `<a href>` whose accessible name is empty (icon-only, image without alt inside). Generic-vs-descriptive anchor wording stays in M10.
4. **Labeled form controls** — `input`/`select`/`textarea` without `<label for>`, a wrapping `<label>`, `aria-label`, or `aria-labelledby` (a placeholder alone does not count).
5. **`href="javascript:"`** (and `href="#"` carrying handlers) — navigation that only works through script.
6. **Primary content in an iframe** — the main article/product content lives inside `<iframe>`; agents and crawlers see only the shell.
7. **WebMCP** — `navigator.modelContext` in inline/linked scripts: report presence as informational. It is a W3C Community Group draft (2026-04-23) in a Chrome origin trial — never a recommendation.
8. **Not checkable statically** — `cursor: pointer`, target size (web.dev's > 8px² guidance), ghost overlays / off-screen click blockers. List them explicitly as `not_checkable_static`; Tier 1 covers them through Lighthouse's "Agentic browsing" category (M150+).

## Fixes
- **PROPOSED** (`fixable: proposed`): swap a `div[onclick]` for `<button type="button">`, add `aria-label`/visible text to an unnamed control, add `<label for>` to a form control, replace `href="javascript:"` with a real URL or a `<button>` — per-item diffs because they touch templates and event wiring.
- **ADVISORY** (`fixable: advisory`): moving primary content out of an iframe, framework component changes, overlay/target-size work, WebMCP adoption.
- **Never fabricate** labels or link text the surrounding content does not support — leave a clearly-marked `TODO` placeholder or ask.

## Verification
- `node "${CLAUDE_PLUGIN_ROOT}/scripts/agent-readiness.mjs" --snapshot <pages/<slug>.json>` — counts per check with the offending elements (method `dom_assert`).
- Tier 1, **consent-gated** (ask first — it downloads and launches a browser): `npx lighthouse <url> --output=json --output-path <run_dir>/lighthouse.json` and read the agentic-browsing category (category id TO-VERIFY against the installed Lighthouse version). Run only when the user agrees and Chrome is available; otherwise `M22.lighthouse.agentic_browsing` stays `needs_api`.
- When the page is client-rendered and not rendered (`render.needed && render.used === "none"`), control checks run on the shell only: state that limit and keep `needs_api` where the shell is empty.

## Findings
Conform to `schema/finding.schema.json`; axis `ai`; confidence **`directional`** for every id; severity **≤3**. **Severity policy**: 5 is reserved for catastrophic, eligibility-killing facts at site/template scope; 4 major · 3 moderate · 2 minor · 1 cosmetic · 0 informational — and only an `established` severity-5 `fail` in an active category can cap a score (`references/scoring-model.md`). Nothing in M22 is `established`, so nothing here ever caps. `evidence.observed` quotes the element(s) verbatim (selector + outer tag), `verification.reproduce` is the command above, `expected_impact` is banded (no naked %).
- `M22.controls.non_semantic_interactive` — div/span click handlers act as controls (warn 3; fail 3 when they are the majority of controls or gate the primary action; `fixable: proposed`).
- `M22.controls.button_without_name` (warn 2, `fixable: proposed`) · `M22.links.empty_name` (warn 2, `fixable: proposed`) · `M22.links.href_javascript` (warn 2, `fixable: proposed`).
- `M22.forms.unlabeled_controls` (warn 3, `fixable: proposed`) · `M22.content.iframe_primary` (warn 2, `fixable: advisory`).
- `M22.lighthouse.agentic_browsing` (severity 3; `needs_api` unless the consent-gated run happened, then pass/warn/fail from its score).
- `M22.static.not_checkable` (`not_applicable`, severity 0 — lists the cursor/target-size/overlay items and the Tier 1 path) · `M22.semantics.ok` (pass 3 — controls, names, and labels all clean).
- `M22.webmcp.present` (pass, severity 0, informational — presence only).

## Honesty
- Agent-readiness is **directional**: Google recommends agent-friendly practices; no vendor documents a ranking or citation effect. Never `established`, never severity 4–5, never a score cap.
- These are largely accessibility fundamentals (name / role / value) with a new consumer; frame fixes as removing a barrier for assistive tech and agents alike, not as "AI SEO".
- Lighthouse's agentic category is **lab** tooling; a green score does not prove an agent completed a task on the page. WebMCP is an origin-trial draft — report presence, recommend nothing.
