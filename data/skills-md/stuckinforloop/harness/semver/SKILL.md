---
name: semver
description: Semantic versioning guidelines for software releases. Use when assigning version numbers, deciding between major/minor/patch bumps, managing unstable (0.x.x) software versions, evaluating breaking changes, or reviewing changelogs and release notes for correct semver compliance.
---

# Semantic Versioning

Version numbers follow the format **Major.Minor.Patch** (e.g., `1.14.10`).

## Stable Software (1.0.0+)

| Change type | Bump | Reset | Example |
|---|---|---|---|
| Breaking change | Major | Minor and Patch to 0 | `1.14.10` -> `2.0.0` |
| New feature or backwards-compatible behavior change | Minor | Patch to 0 | `1.14.10` -> `1.15.0` |
| Bug fix or security fix (backwards-compatible) | Patch | Nothing | `1.14.10` -> `1.14.11` |

**Reserve patch releases exclusively for fixes. Lack-of-feature is not a bug — use minor releases for those.**

Consumer guarantee: newer releases within the same major version are safe to upgrade to.

## Unstable Software (0.x.x)

Software with major version `0` is unstable — no stability commitment yet.

| Change type | Bump | Example |
|---|---|---|
| Bug fix or security fix | Patch | `0.3.2` -> `0.3.3` |
| Everything else (features AND breaking changes) | Minor | `0.3.2` -> `0.4.0` |

- Start development at `0.1.0`.
- Release `1.0.0` when ready to commit to stability.

Consumer guarantee: fixes available within the same minor version.

## Breaking Changes

Semver communicates breaking changes clearly — but does not make them cheap. For popular software with many downstream consumers, partial upgrades create ecosystem fragmentation.

Guidelines:
- Avoid major version bumps for as long as possible.
- If a major bump is unavoidable, provide a gradual migration path.
- Do not treat semver as a license to make breaking changes.
