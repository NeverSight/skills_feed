---
name: playwright-testing
description: >
  Plan, implement, and debug frontend tests: unit/integration/E2E/visual/a11y.
  Use for Playwright MCP browser automation, Vitest/Jest/RTL, flaky test triage,
  CI stabilization, and canvas/WebGL games (Phaser) needing deterministic input
  plus screenshot/state assertions. Trigger: "test", "E2E", "flaky", "visual regression",
  "Playwright", "game testing".
---

# Frontend Testing

Unlock reliable confidence fast: enable safe refactors by choosing the right test layer, making the app observable, and eliminating nondeterminism so failures are actionable.

## Philosophy: Confidence Per Minute

Frontend tests fail for two reasons: the product is broken, or the test is lying. Your job is to maximize signal and minimize "test is lying".

**Before writing a test, ask**:
- What user risk am I covering (money, progression, auth, data loss, crashes)?
- What's the narrowest layer that catches this bug class (pure logic vs UI vs full browser)?
- What nondeterminism exists (time, RNG, async loading, network, animations, fonts, GPU)?
- What "ready" signal can I wait on besides `setTimeout`?
- What should a failure print/screenshot so it's diagnosable in CI?

**Core principles**:
1. **Test the contract, not the implementation**: assert stable user-meaningful outcomes and public seams.
2. **Prefer determinism over retries**: make time/RNG/network controllable; remove flake at the source.
3. **Observe like a debugger**: console errors, network failures, screenshots, and state dumps on failure.
4. **One critical flow first**: a reliable smoke test beats 50 flaky tests.

## Test Layer Decision Tree

Pick the cheapest layer that provides needed confidence:

| Layer | Speed | Use For |
|-------|-------|---------|
| **Unit** | Fastest | Pure functions, reducers, validators, math, pathfinding, deterministic simulation |
| **Component** | Medium | UI behavior with mocked IO (React Testing Library, Vue Testing Library) |
| **E2E** | Slowest | Critical user flows across routing, storage, real bundling/runtime |
| **Visual** | Specialized | Layout/pixel regressions; for canvas/WebGL, only after locking determinism |

## Quick Start: First Smoke Test

1. **Define 1 critical flow**: "page loads → user can start → one key action works"
2. **Add a test seam** to the app (see below)
3. **Choose runner**: Playwright MCP for E2E, unit tests for logic
4. **Fail loudly**: treat console errors and failed requests as test failures
5. **Stabilize**: seed RNG, freeze time, fix viewport, disable animations

## Concrete MCP Workflow: Testing a Game

Step-by-step sequence for testing a Phaser/canvas game:

```
1. mcp__playwright__browser_navigate
   → http://localhost:3000?test=1&seed=42

2. mcp__playwright__browser_evaluate
   → () => new Promise(r => { const c = () => window.__TEST__?.ready ? r(true) : setTimeout(c, 100); c(); })
   (Wait for game ready)

3. mcp__playwright__browser_console_messages
   → level: "error"
   (Fail if any errors)

4. mcp__playwright__browser_snapshot
   → Get UI state and refs

5. mcp__playwright__browser_click
   → element: "Start Button", ref: [from snapshot]

6. mcp__playwright__browser_evaluate
   → () => window.__TEST__.state()
   (Assert game state is correct)

7. mcp__playwright__browser_press_key
   → key: "ArrowRight" (or WASD for movement)

8. mcp__playwright__browser_evaluate
   → () => window.__TEST__.state().player.x
   (Verify movement happened)

9. mcp__playwright__browser_take_screenshot
   → filename: "gameplay-state.png"
   (Visual evidence after deterministic setup)
```

## Recommended Test Seams

Add to the app for testability (read-only, stable, minimal):

```javascript
window.__TEST__ = {
  ready: false,           // true after first interactive frame
  seed: null,             // current RNG seed
  sceneKey: null,         // current scene/route
  state: () => ({         // JSON-serializable snapshot
    scene: this.sceneKey,
    player: { x, y, hp },
    score: gameState.score,
    entities: entities.map(e => ({ id: e.id, type: e.type, x: e.x, y: e.y }))
  }),
  commands: {             // optional mutation commands
    reset: () => {},
    seed: (n) => {},
    skipIntro: () => {}
  }
};
```

**Rule**: Expose IDs + essential fields, not raw Phaser/engine objects.

## Anti-Patterns to Avoid

❌ **Testing the wrong layer**: E2E tests for pure logic
*Why tempting*: "Let's just test everything through the browser"
*Better*: Unit tests for logic; reserve E2E for integration contracts

❌ **Testing implementation details**: Asserting DOM structure/classnames
*Why tempting*: Easy to assert what you can see in DevTools
*Better*: Assert user-meaningful outputs (text, score, HP changes)

❌ **Sleep-driven tests**: `wait 2s then click`
*Why tempting*: Simple and "works on my machine"
*Better*: Wait on explicit readiness (DOM marker, `window.__TEST__.ready`)

❌ **Uncontrolled randomness**: RNG/time in assertions
*Why tempting*: "The game uses random, so the test should too"
*Better*: Seed RNG (`?seed=42`), freeze time, assert stable invariants

❌ **Pixel snapshots without determinism**: Canvas screenshots that flake
*Why tempting*: "I'll catch visual bugs automatically"
*Better*: Deterministic mode first; then screenshot at known stable frames

❌ **Retries as a strategy**: "Just bump retries to 3"
*Why tempting*: Quick fix that makes CI green
*Better*: Fix the flake source; retries hide real problems

## Debugging Failed Tests

When a test fails, gather evidence in this order:

1. **Console errors**: `mcp__playwright__browser_console_messages({ level: "error" })`
2. **Network failures**: `mcp__playwright__browser_network_requests()` → check for non-2xx
3. **Screenshot**: `mcp__playwright__browser_take_screenshot()` → visual state at failure
4. **App state**: `mcp__playwright__browser_evaluate({ function: "() => window.__TEST__.state()" })`
5. **Classify the flake** (see references/flake-reduction.md):
   - Readiness? → add explicit wait
   - Timing? → control animation/physics
   - Environment? → lock viewport/DPR
   - Data? → isolate test data

## Graduation Criteria: When Is Testing "Enough"?

Minimum viable test suite:
- [ ] **1 smoke test** that proves the app loads and primary action works
- [ ] **Test seam exists** (`window.__TEST__` with ready flag and state)
- [ ] **Deterministic mode** for canvas/games (`?test=1` enables seeding)
- [ ] **Console errors fail tests** (no silent failures)
- [ ] **CI runs tests** on every push

Level up when:
- Critical paths (auth, payment, save/load) have dedicated E2E
- Unit tests cover complex logic (pathfinding, damage calc, state machines)
- Visual regression on key screens (menu, HUD) with locked determinism

## Visual Regression with imgdiff.py

For pixel comparison of screenshots:

```bash
# Compare baseline to current
python scripts/imgdiff.py baseline.png current.png --out diff.png

# Allow small tolerance (anti-aliasing differences)
python scripts/imgdiff.py baseline.png current.png --max-rms 2.0
```

Exit codes: 0 = identical, 1 = different, 2 = error

## UI Slicing Regressions (Nine-Slice / Ribbons / Bars)

Canvas UI issues (panel seams, segmented ribbons, invisible HUD fills) are best caught with a dedicated UI harness instead of the full gameplay flow.

1. Build a simple `test.html`/scene that loads *only* the UI assets.
2. Render raw slices next to assembled panels (multi-size), and include ribbon/bars with both “raw crop + scale” and “stitched multi-slice” views.
3. Expose `window.__TEST__` with `.commands.showTest(n)` so Playwright can toggle each mode deterministically.
4. Capture targeted screenshots (panels, ribbons, bars) and diff them in CI.

See `references/phaser-canvas-testing.md` for the deterministic setup + screenshot workflow.

## Variation Guidance

Adapt approach based on context:
- **DOM app**: Standard Playwright selectors, wait for text/elements
- **Canvas game**: Test seams mandatory, wait via `window.__TEST__.ready`
- **Hybrid**: DOM for menus, test seams for gameplay
- **CI-only GPU**: May need software rendering flags or skip visual tests
- **UI slicing regressions**: For nine-slice/ribbon/bar artifacts, prefer a small UI harness scene/page with deterministic modes and targeted screenshots (`references/phaser-canvas-testing.md`).

## Bundled Resources

Read these when needed:
- `references/playwright-mcp-cheatsheet.md`: Detailed MCP tool patterns
- `references/phaser-canvas-testing.md`: Deterministic mode for Phaser games
- `references/flake-reduction.md`: Flake classification and fixes

## Remember

You can make almost any frontend (including canvas/WebGL games) testable by adding a tiny, stable seam for readiness + state. One reliable smoke test is the foundation. Aim for tests that are boring to maintain: deterministic, explicit about readiness, and rich in failure evidence. The goal is confidence, not coverage numbers.
