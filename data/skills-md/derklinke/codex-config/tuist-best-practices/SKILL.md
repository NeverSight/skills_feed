---
name: tuist-best-practices
description: Best practices for Tuist manifests, ProjectDescriptionHelpers, caching, and iOS project workflows.
metadata:
  short-description: Tuist best practices for iOS projects
---

# Tuist Best Practices

## When to use

- editing Tuist manifests or adding targets
- updating project structure or shared helpers
- generating Xcode projects or debugging Tuist behavior

## Repo layout

- root config in `Tuist.swift`
- shared helpers in `Tuist/ProjectDescriptionHelpers`
- iOS manifest in `Project.swift` (often under `ios/` but not required)
- prefer repo-provided task runner (`just`, `make`, etc.) for generate/build/test/open
- if using `tuist xcodebuild`, keep subcommand first to avoid argument reorder issues

## Manifests

- `Project.swift`: root variable should be `let project = Project(...)`
- `Workspace.swift` optional; Tuist auto-generates workspace with project + dependencies
- `Tuist.swift` recommended; Tuist walks up dirs to find it, so running from `ios/` still uses root config

## Code sharing

- place helpers in `Tuist/ProjectDescriptionHelpers`
- import with `import ProjectDescriptionHelpers` in manifests
- helpers available in `Project.swift`, `Workspace.swift`, and `Package.swift` (behind `#TUIST`)

## Caching

- `tuist cache` builds binaries; `tuist generate/test` use binary cache by default when available
- opt out with `--no-binary-cache`
- binary cache is for dev/test, not release builds

## Change workflow

- add targets/settings in `Project.swift` using helpers
- after adding files or project changes: run repo generate task (e.g. `just generate`)
- avoid running `xcodebuild` directly

## References

- Tuist docs: manifests, directory structure, code sharing, module cache, config (docs.tuist.dev)
