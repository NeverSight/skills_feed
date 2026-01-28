---
name: frontend-testing
description: "Plan, implement, and debug frontend tests: unit/integration/E2E/visual/a11y. Use for Playwright/Cypress/Vitest/Jest/RTL, flaky test triage, CI stabilization, and canvas/WebGL games (Phaser) needing deterministic input + screenshot/state assertions."
---

# Frontend Testing

Unlock reliable confidence fast: enable safe refactors by choosing the right test layer, making the app observable, and eliminating nondeterminism so failures are actionable.

## Philosophy: Confidence Per Minute

Frontend tests fail for two reasons: the product is broken, or the test is lying. Your job is to maximize signal and minimize “test is lying”.

**Before writing a test, ask**:
- What user risk am I covering (money, progression, auth, data loss, “can’t start” crashes)?
- What’s the narrowest layer that catches this bug class (pure logic vs UI vs full browser)?
- What nondeterminism exists (time, RNG, async loading, network, animations, fonts, GPU)?
- What “ready” signal can I wait on besides `setTimeout`?
- What should a failure print/screenshot so it’s diagnosable in CI?

**Core principles**:
1. **Test the contract, not the implementation**: assert stable user-meaningful outcomes and public seams.
2. **Prefer determinism over retries**: make time/RNG/network controllable; remove flake at the source.
3. **Observe like a debugger**: console errors, network failures, screenshots, and state dumps on failure.
4. **One critical flow first**: a reliable smoke test beats 50 flaky tests.

## Workflow Decision Tree

Pick the test type by the cheapest layer that provides the needed confidence:

- **Unit tests** (fastest): pure functions, reducers, validators, math, pathfinding, deterministic simulation steps.
- **Component/integration tests** (medium): UI behavior with mocked IO (React Testing Library / Vue Testing Library / Testing Library DOM).
- **E2E tests** (slowest, highest confidence): critical user flows across routing, storage, real bundling/runtime.
- **Visual regression** (specialized): layout/pixel regressions; for canvas/WebGL, only after locking determinism.
- **A11y checks**: great for DOM UIs; limited value for pure canvas unless you expose accessible DOM overlays.

## Quick Start (Any Project)

1. **Define 1 smoke flow**: “page loads → user can start → one key action works”.
2. **Choose runner**:
   - Prefer **Playwright** for browser E2E + screenshots.
   - Prefer **Testing Library** for DOM component behavior.
   - Prefer **unit tests** for logic you can run without a browser.
3. **Add a “ready” signal** in the app (DOM marker, window flag, or game event) and wait on that.
4. **Fail loudly**: treat console errors and failed requests as test failures.
5. **Stabilize**: seed RNG, freeze time, fix viewport/DPR, disable animations, and remove network variability.

## Playwright Patterns (Especially Useful For Games)

Use Playwright when you need “real browser” confidence:
- Drive input via mouse/keyboard/touch; treat the canvas like the user does.
- Add a **test seam**: expose a small, stable test API on `window` (read-only state + a few commands).
- Prefer `waitForFunction`-style readiness over sleep; gate on “scene ready” / “assets loaded” / “first frame rendered”.
- For screenshots: lock viewport, device scale factor, fonts, and animation timing.
- For 9-slice / canvas UI regressions: add a dedicated UI harness scene/page and assert via targeted screenshots (see `references/phaser-canvas-testing.md`).

If using the Playwright MCP tools (browser automation inside Codex), follow the same mindset:
- Use `browser_console_messages` and `browser_network_requests` to catch silent failures.
- Use `browser_evaluate` to assert `window.__TEST__` state and to set up deterministic mode.
- Use `browser_take_screenshot` for visual assertions after determinism is enforced.

## Reconnaissance-Then-Action (Borrowed From Real Debugging)

When a UI is dynamic, don’t guess selectors—recon first, then act:

Quick decision guide:

```
Task → Is it static HTML (no JS runtime needed)?
  ├─ Yes → read the HTML to find stable selectors/content, then automate
  └─ No  → treat as dynamic: run the app, wait for readiness, then inspect rendered state
```

1. **Navigate and wait for readiness**:
   - For many webapps: wait for a meaningful “loaded” element (preferred).
   - `networkidle` can help for SPAs, but avoid it if the app uses websockets/polling.
2. **Capture evidence** (what the user actually sees):
   - screenshot (full page for DOM; targeted for canvas)
   - console errors + failed requests
3. **Discover selectors** from the rendered state:
   - prefer role/text/label selectors over brittle CSS
4. **Execute actions** using discovered selectors and re-check state.

Common pitfall:
❌ Inspect/interact before the app is ready.
✅ Wait on an explicit ready signal (DOM marker or `window.__TEST__.ready`), not a sleep.

## Server Lifecycle Helper (Playwright E2E)

When the dev server isn’t already running, use the bundled helper as a black box:
- Run `python scripts/with_server.py --help` first.
- Start one (or multiple) servers, wait for their ports, then run your test command.

Example:
```bash
python scripts/with_server.py --server "npm run dev" --port 5173 -- npm test
```

## Flake Reduction Checklist

- Replace sleeps with explicit readiness conditions.
- Control time (`Date.now`, timers), RNG, and animation loops.
- Make network deterministic (mock, record/replay, or run against a seeded local backend).
- Eliminate “first-run” differences (asset caches, fonts) or warm them explicitly.
- Lock environment: viewport, DPR, locale/timezone, and rendering settings.

## Anti-Patterns to Avoid

❌ **Testing the wrong layer**: E2E tests for pure logic.
Better: unit tests for logic; reserve E2E for integration contracts.

❌ **Testing implementation details**: asserting DOM structure/classnames or internal engine objects.
Better: assert user-meaningful outputs (text, navigation, score/HP changes) or a small stable test seam.

❌ **Sleep-driven tests**: `wait 2s then click`.
Better: wait on explicit readiness (DOM marker, event, `window` flag).

❌ **Uncontrolled randomness**: RNG/time-based behaviors in assertions.
Better: seed RNG, freeze time, and assert stable invariants.

❌ **Pixel snapshots without determinism** (especially canvas/WebGL).
Better: add deterministic mode first; then screenshot selectively.

❌ **Snapshot explosion**: hundreds of snapshots that no one can interpret.
Better: keep snapshots targeted (critical screens); prefer specific assertions for behavior.

❌ **Retries as a strategy**: “just bump retries in CI”.
Better: fix readiness and determinism; use retries only as temporary guardrails.

## Variation Guidance (Prevent One-Size-Fits-All)

Vary the approach based on:
- **UI type**: DOM app vs canvas/WebGL game vs hybrid.
- **Risk**: core revenue/progression flows get E2E first; edge UI polish gets component tests.
- **CI constraints**: headless-only, limited GPU, slow CPUs, no audio devices.
- **Test seam availability**: if you can add a stable `window.__TEST__` API, assert state; if not, stick to black-box input/output.

## Remember

You can make almost any frontend (including canvas/WebGL games) testable by adding a tiny, stable seam for readiness + state. This skill is meant to empower creative, high-signal testing rather than cargo-cult checklists. Aim for tests that are boring to maintain: deterministic, explicit about readiness, and rich in failure evidence. One reliable smoke test is the foundation; everything else compounds from there.

## Bundled Resources

Read these only when needed:
- `references/playwright-mcp-cheatsheet.md`: patterns for using Playwright MCP tools for assertions, waiting, and diagnostics.
- `references/phaser-canvas-testing.md`: deterministic mode + hooks for Phaser/canvas/WebGL games.
- `references/flake-reduction.md`: deeper flake triage and stabilization tactics.

Use these scripts as black boxes (run `--help` first; don’t read source unless you must):
- `scripts/with_server.py`: start/wait/stop one or more dev servers around a test command.
- `scripts/imgdiff.py`: lightweight screenshot diff helper (requires `pip install pillow`).
