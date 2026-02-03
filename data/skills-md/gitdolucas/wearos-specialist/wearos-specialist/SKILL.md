---
name: wearos-specialist
description: Wear OS-focused implementation, review, and debugging guidance (Kotlin, Jetpack Compose for Wear OS, coroutines/Flow, MVVM, Room/DataStore, navigation, tiles/complications, sensors, haptics). Use when building or reviewing smartwatch apps, improving wearable UX, or addressing watch performance/battery/lifecycle issues.
---

# Wear OS Specialist

## Scope

Use this skill when implementing, reviewing, or debugging **Wear OS** apps. Optimize for:

- **Fast, glanceable UI** on small screens
- **Battery-aware** behavior and background limits
- **Lifecycle correctness** (navigation/back behavior, resumability, ambient/AOD where relevant)
- **Modern Android stack**: Kotlin + coroutines/Flow, Compose for Wear OS, MVVM-ish state holders, Room/DataStore, Navigation, and watch-specific surfaces (Tiles/Complications)

## Operating principles (Wear OS)

- **Glanceability first**: show the primary metric/action clearly; remove secondary UI.
- **Big tap targets**: prefer few large buttons over dense controls.
- **Minimize work per frame**: avoid heavy computation/IO on the main thread.
- **Battery-friendly**: background work, sensors, timers, and haptics must be intentional and lifecycle-safe.
- **Predictable state**: single source of truth; restore correctly after process death where it matters.

## Default implementation workflow (stack-first)

When adding or changing a feature, follow this path unless there’s a strong reason not to:

1. **UI (Compose screen)**
   - Keep UI stateless where possible; pass state + event callbacks.
   - Make the primary action the largest and easiest to hit.
   - Avoid “clever” gestures; assume sweaty hands + motion.

2. **State holder (ViewModel / state container)**
   - Own business rules and validation; coordinate transient effects (snack/haptics).
   - Use coroutines; do not block UI.
   - Expose immutable UI state (`data class`) and event methods.

3. **Data layer (Room / DataStore)**
   - Use Room for relational/history data; DataStore for preferences and small key-value config.
   - Prefer simple, efficient queries; stream to UI via Flow when appropriate.

4. **Navigation**
   - Keep routes explicit; avoid fragile stringly-typed args.
   - Ensure back behavior feels natural on watch (no deep stacks).

5. **Validation**
   - Define a short on-watch test plan: key flows, rapid tapping, interruptions, background/return behavior.

## Wearable UX checklist (quick)

- Primary action is reachable in **one tap** from the screen.
- All actions are usable with **one thumb** (no precision).
- Defaults are sensible (don’t force setup before the core action).
- “Reference/History” info is supportive, not dominating.
- Avoid blocking flows; confirmations only for destructive actions.

## Performance and recomposition rules of thumb

- Keep derived values with `remember`/`derivedStateOf` when they’re non-trivial.
- Avoid allocating new lists/objects on every recomposition in hot UI paths.
- Prefer `Flow`/`StateFlow` from data layer to UI rather than manual polling.
- Timer updates should be **coarse** (e.g., once per second) and stop when not needed.
- Be careful with formatters/parsers in composables; cache them.

## Debugging workflow (watch-first)

When something is “weird on device”:

- Reproduce on the watch (not emulator) and note:
  - screen, action sequence, watch state (AOD on/off), battery saver, connectivity
- Add temporary logs around:
  - navigation arguments
  - data reads/writes (Room/DataStore/network)
  - sensors/timers start/stop and lifecycle callbacks
- Check for:
  - main-thread IO
  - state being recreated incorrectly (missing persistence/restoration)
  - runaway coroutines/timers/sensor listeners continuing after leaving a screen

## Output templates

### Implementation plan template

Use this format when proposing work:

```markdown
## Summary
- What user-facing behavior changes (1–3 bullets)

## Files to touch
- `...`

## Data/state changes
- UI state:
- Events:
- Persistence (Room/DataStore):
- Background work (if any):

## Wear OS constraints check
- Glanceability:
- Tap targets:
- Battery/background:
- Lifecycle/restore:

## Test plan
- On-watch manual checks (key flows + edge cases):
```

### Review template (PR-style)

```markdown
## Correctness
- [ ] State transitions are correct under rapid taps / interruptions
- [ ] Data reads/writes are correct and resilient (restart, process death)

## Wear OS UX
- [ ] Primary action is largest and easiest to hit
- [ ] No dense UI / tiny tap targets
- [ ] No blocking flows during primary usage

## Performance/battery
- [ ] No IO on main thread
- [ ] Timers/sensors stop when leaving screen
- [ ] Recomposition hotspots avoided (no per-frame allocations)

## Data layer
- [ ] Room/DataStore usage fits the problem (history vs settings)
- [ ] Queries are minimal and efficient (only load what UI needs)
```

## Additional references (one-level deep)

- Review checklist: [review-checklist.md](review-checklist.md)
- Performance/battery notes: [perf-battery.md](perf-battery.md)
- Examples: [examples.md](examples.md)

