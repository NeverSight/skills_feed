---
name: swift-observation
description: Apple Observation framework for Swift. Use when modeling observable state with the `@Observable` macro, tracking changes with `withObservationTracking`, integrating with SwiftUI, or working with ObservationRegistrar and Observations async sequences.
---

# Observation

## What to open

- Use `swift-observation/observation.md` for full API details and examples.
- Search within it for `@Observable`, `withObservationTracking`, `ObservationRegistrar`, `Observations`, and `ObservationIgnored`.
- Use `swift-observation/observations_pre_iOS_26_backport.md` for availability notes and backport discussion.
- Use `swift-observation/Observation/` source files to inspect the `Observations` implementation and any supporting runtime pieces when evaluating backport feasibility.

## Workflow

- Prefer `@Observable` to make models observable; do not conform to `Observable` manually.
- Read properties inside `withObservationTracking` to define the dependency set.
- Use `ObservationIgnored` for properties that should not trigger updates.
- Use `Observations` when you need async change streams.

## SwiftUI usage

- For SwiftUI, treat `@Observable` models as the source of truth and let the view read the properties it needs.
- Use `withObservationTracking` for non-SwiftUI rendering or custom observers.

## Availability and backport notes

- `Observations` is available on iOS 26+; plan for fallbacks on earlier OSes.
- For pre-iOS 26 support, consider community backports or vendor forks; see `swift-observation/observations_pre_iOS_26_backport.md` for options and caveats.
