---
name: putio-sdk-dev
description: "Develop or review SDK and API client code owned by put.io across TypeScript, Swift, Kotlin, and similar packages. Use only for work in a put.io SDK repository or explicit requests for put.io SDK conventions. Do not use for unrelated SDKs, browser-only put.io inspection, end-user application code, or putio CLI operations."
---

# put.io SDK development

Apply put.io SDK conventions after the target repository's own guidance.

## Shared defaults

- Treat each SDK as a public package, not an internal compatibility layer.
- Treat TypeScript as the canonical full put.io API client, not just the richest reference.
- Keep every public surface domain-first, strongly typed, and native to its host language.
- Update request, response, and typed error contracts together.
- Prove behavior with deterministic tests plus safe live tests when real API behavior matters.
- Keep Swift and Kotlin scope narrower than TypeScript only when product usage justifies it.

## Source order

When sources disagree, prefer local backend behavior and tests, current
first-party app usage, maintained SDKs, archived clients, then published API
documentation.

Start with sources present in the target repository. Add backend or first-party
consumer evidence only when it is authorized and available.

Widen SDK surfaces only when real app use and verified backend behavior justify it.

## Start

Read only what you need:

- every filesystem `AGENTS.md` that applies from the target repo root to the
  files being changed, including untracked files, followed by the tracked
  auxiliary guidance inventory from `git ls-files '*AGENTS.md' '*SKILL.md'`
- the frontmatter and instructions from task-matching project-local `SKILL.md`
  files under `.agents/skills/`, `.claude/skills/`, or `skills/`; ignore
  dependency and vendored trees
- the canonical verify and live-test commands from `README.md`, `AGENTS.md`, or `docs/*`
- [SDK vision](./references/sdk-vision.md) for scope, parity, and endpoint-family decisions
- [patterns](./references/patterns.md) for typed boundaries, error mapping, pagination, and live-test layering
- [language notes](./references/language-notes.md) for TypeScript, Swift, or Kotlin-specific guidance
- [release security](./references/release-security.md) when publishing,
  signing, releasing, or building distributable binaries

Target-repo guidance and matching repo-local skills override this shared skill.

If the repo has a canonical verify command, use that as the source of truth before editing delivery automation.
Target-repo delivery and supply-chain guidance overrides the shared release
defaults.

## Workflow

1. Inspect the target namespace and the shared transport or client runtime.
2. Check backend behavior, backend tests, and current app usage before widening or changing a contract.
3. Update typed request input, response parsing, and operation-specific error mapping together.
4. Add or update deterministic coverage for request shaping, parsing, errors, and public client contracts.
5. Add or refresh safe live verification when production behavior matters and the surface is reversible.
6. Keep multiple public clients aligned when the repo exposes more than one interface style.
7. Select the owner's documented checks for the affected contracts and their
   dependents, including installed-package and downstream-consumer proof when
   relevant. Run the full canonical gate when mandated, shared inputs changed,
   or focused coverage is uncertain. Fix failures and refresh affected proof;
   reuse passing results while their source, inputs and environment remain
   valid. Record unavailable proof and its exact blocker without claiming it
   passed or inferring authorization from command discovery.
8. Update package-facing docs and release notes when the public surface changes.

## Endpoint changes

For a new or changed endpoint, discover the tracked source, test, fixture, and
consumer paths first. Search only paths that exist:

```bash
git ls-files -z -- \
  ':(glob)**/src/**' \
  ':(glob)**/test/**' \
  ':(glob)**/tests/**' \
  ':(glob)**/Tests/**' \
  ':(glob)**/Sources/**' \
  ':(glob)**/docs/**' \
  ':(glob)**/fixtures/**' \
  ':(glob)**/Package.swift' \
  ':(glob)**/build.gradle' \
  ':(glob)**/package.json' |
  xargs -0 rg -n "route_name|endpoint_path|field_name" -- || true
```

Repeat this search from a backend, fixture, or first-party consumer checkout
only when that source is available and authorized.

Then update the SDK in this order:

1. request input type or query model
2. response parser or native decode model
3. operation-specific error mapping
4. public client method or namespace export
5. unit tests for request, response, and error behavior
6. safe live test when the endpoint behavior cannot be proven locally
7. README, API docs, or release notes when the public surface changed

## Verification

Use the owning repository's documented commands. Do not infer a Vite+, Gradle,
or Make entrypoint from this shared skill.

An SDK repo should expose both:

- a default deterministic unit-test path that is safe for CI and local iteration
- a separate documented live-test path for real API verification

If one of those layers is missing, treat it as a repo gap to document or fix rather than silently accepting a weaker verification story.

Discover the owned commands before running them:

```bash
rg --hidden -n "verify|check|test|example" . \
  --glob 'README.md' \
  --glob 'AGENTS.md' \
  --glob 'docs/**' \
  --glob '.github/**' \
  --glob 'package.json' \
  --glob 'Makefile' \
  --glob 'pyproject.toml' \
  --glob 'Cargo.toml' \
  --glob 'build.gradle*' \
  --glob 'settings.gradle*' \
  --glob 'Package.swift' || true
```

For runtime verification, prefer the repo's documented live-test entrypoints and follow the shared-account safety rules in that repo's testing docs.

## Boundaries

- Verify backend contracts with current docs, source, fixtures, or live probes rather than old SDKs alone.
- Claim full verification only when the unit, fixture, and live layers that matter for the change were exercised.
- Keep live coverage against shared accounts non-destructive.
- Finish in-scope edits, verification, and fixes without pausing for approval; ask before publishing, release writes, coverage-threshold changes, and live writes that are not reversible.
- Preserve naming, parity, and type-safety unless a documented reason justifies a change.
- Keep repo-specific implementation guidance in that repo's `AGENTS.md` or
  `docs/*`
- Generic SDK work, end-user application code, and CLI consumer operations are
  outside this skill.
