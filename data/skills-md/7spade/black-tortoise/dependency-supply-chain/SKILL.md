---
name: dependency-supply-chain
description: Change discipline for adding/upgrading dependencies; keeps diffs small, avoids unnecessary packages, and preserves deletion-friendly architecture.
---

# Dependency & Supply-Chain (Change Discipline)

## Use when
- Adding a new npm package.
- Upgrading Angular/Firebase/tooling versions.

## Workflow
1. Justify: what existing platform feature cannot solve it?
2. Minimize: smallest package/scope; avoid runtime deps for build-time needs.
3. Isolate: keep dependency behind a boundary (adapter/port) if it’s not a core framework lib.
4. Validate: run lint, type-check, architecture gate, and tests.

## References
- `.github/instructions/66-dependency-supply-chain-copilot-instructions.md`

