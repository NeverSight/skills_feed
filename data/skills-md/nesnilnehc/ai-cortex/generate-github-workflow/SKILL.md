---
name: generate-github-workflow
description: "GitHub Actions YAML with embedded output contract: security-first, minimal permissions, version pinning. For CI, release, PR checks. Differs from generic templates by spec compliance and auditability."
tags: [devops, eng-standards]
version: 1.0.0
license: MIT
related_skills: []
recommended_scope: project
metadata:
  author: ai-cortex
---

# Skill: Generate GitHub Workflow

## Purpose

Produce **GitHub Actions workflow files** that satisfy this skill’s **Appendix A: Workflow output contract** for a wide range of software projects. Standardized structure, triggers, and security reduce CI/CD setup cost and improve maintainability and auditability while avoiding common security and permission issues. This skill only produces workflow YAML; it does not chain to documentation or rule skills. If the user later needs README or AGENTS.md updates, invoke those skills separately.

---

## Use Cases

- **New project setup**: Add CI (build, test, lint) or PR-check workflows to a new repo.
- **Unified standards**: Align workflow style and naming across many repos for ops and audit.
- **Fill gaps**: Add missing CI/release/scheduled workflows to legacy projects, with minimal permissions and pinned versions.
- **Scenario-based**: Generate YAML for a given scenario (e.g. “run tests only on PR”, “build and publish on tag”).

**When to use**: When the user or project needs to “create or add GitHub workflows for the current or specified project.”

**Scope**: This skill’s output follows the **embedded Appendix A** (narrow triggers, minimal permissions, pinned versions, auditable). Generic templates (e.g. skills.sh `github-actions-templates`) are more general; this skill emphasizes security and maintainability.

---

## Behavior

### Principles

- **Appendix A is authoritative**: Output YAML must satisfy Appendix A (structure, naming, security, maintainability).
- **Narrow triggers**: `on` must specify branches/paths/tags; avoid triggering on every push. Common pattern: `push`/`pull_request` with `branches` or `paths`. **Release** workflows must trigger only on version tags (e.g. `push: tags: ['v*']`) and live in a separate file from CI.
- **Minimal permissions**: When the workflow needs repo write, PR, or Secrets, set `permissions` at workflow or job level to the minimum required; e.g. CI `contents: read`, release `contents: write`, `packages: write`; avoid `all`.
- **Pinned versions**: Pin third-party actions (commit SHA or major-version tag); do not use `@master` or unpinned refs; prefer specific versions for security/scan actions (e.g. Trivy).

### Tone and style

- Use objective, technical language; keep workflow and step `name` short and readable for the Actions log.
- Match the project stack: choose runner, package manager, and build commands by project type (Node/Python/Go/Rust) and existing conventions; if the project already has workflows, align naming and style.

### Input-driven

- Use the user’s **scenario** (e.g. “CI: run tests on PR”, “Release: build and upload on tag”) and **stack** (language, package manager, test/build commands) to generate the workflow; use sensible placeholders when information is missing and mark them for replacement; do not invent commands or paths.

### Interaction

- **Confirm before write**: After generating YAML, list **required notes** (placeholders, branch names, Secret names the user must set), then ask for confirmation; do not write to `.github/workflows/` or commit without user confirmation.
- **Multiple files / release**: If generating several workflows (e.g. CI + Release) or using write permissions (`contents: write`, `packages: write`), list files to be created/overwritten and permission scope, then confirm before writing.
- **Conflicts**: If the target path already has a workflow with the same or overlapping purpose, warn and ask whether to overwrite or save elsewhere; do not overwrite silently.

---

## Input & Output

### Input

- **Scenario**: Purpose (CI, PR check, release, scheduled, matrix).
- **Stack**: Language and version (e.g. Node 20, Python 3.11, Go 1.21), package manager (npm/pnpm/yarn, pip, cargo), test/build/release commands.
- **Triggers**: Branches (e.g. `main`, `develop`), path filters, optional `workflow_dispatch`.
- **Target path**: Where to write the file(s), default `.github/workflows/` under project root; for multiple workflows, specify each filename (e.g. `ci.yml`, `release.yml`).

### Output

- **Workflow YAML**: Full file content conforming to Appendix A, ready to write to `.github/workflows/<name>.yml`.
- **Notes**: List placeholders (e.g. `npm run test`, branch `main`), Secret names, and any items the user must configure.

---

## Restrictions

- **Do not violate Appendix A**: Output must have `name`, `on`, `jobs`, and each job must have `runs-on` and `steps`; do not use unpinned third-party actions or hardcoded secrets.
- **Do not over-trigger**: Do not use bare `on: push` with no branch/path filter unless the user explicitly requests it.
- **Do not invent commands**: Use placeholders for unknown test/build/release commands and mark “replace with actual command”; do not invent scripts or paths.
- **Do not ignore existing workflows**: If the project already has `.github/workflows/`, align naming and style and avoid duplication or conflict.
- **Do not duplicate build logic**: If the project uses GoReleaser, Dockerfile, etc. for build and image shape, the workflow only triggers, logs in, and passes args (e.g. `GITHUB_TOKEN`, `BUILDX_BUILDER`); do not reimplement that logic.

---

## Self-Check

- [ ] **Appendix A**: Does output satisfy mandatory structure and security in Appendix A?
- [ ] **Triggers**: Is `on` narrowed to specific branches/paths/tags?
- [ ] **Permissions and security**: Are minimal `permissions` set? Third-party actions pinned? No hardcoded secrets?
- [ ] **Runnable**: After the user replaces placeholders, can the workflow run in the target repo?
- [ ] **Stack alignment**: Runner, language version, package manager, and commands match the user’s stack?
- [ ] **Step order and deps**: For multi-step jobs (e.g. QEMU → Buildx → login → GoReleaser), is order correct and are ids/env vars passed? See **Appendix B** for Go + Docker + GoReleaser.

---

## Examples

### Example 1: Node CI (test + lint on PR)

**Input**: Scenario: CI. Stack: Node 20, pnpm, test `pnpm test`, lint `pnpm lint`. Trigger: `pull_request` to `main`. File: `ci.yml`.

**Expected**: Single `ci.yml` with `name` e.g. “CI”; `on: pull_request: branches: [main]`; job on `ubuntu-latest` with checkout, setup Node/pnpm, install, lint, test; use official `actions/checkout` and `pnpm/action-setup` (or equivalent) pinned; no hardcoded secrets; `permissions` read-only if set.

### Example 2: Go PR check with path filter

**Input**: Scenario: PR check. Stack: Go 1.21, test `go test ./...`. Trigger only when `go.mod` or `*.go` change. File: `pr-check.yml`.

**Expected**: `on.pull_request` with `paths: ['**.go', 'go.mod']`; job with `actions/setup-go` pinned, steps checkout, setup Go, go test; `permissions` omitted or `contents: read` if no write needed.

### Example 3: Go release (Docker + GHCR + GoReleaser)

**Input**: Scenario: CD/release. Stack: Go, Docker multi-arch (amd64/arm64), GoReleaser for image and GitHub Release. Trigger: only `push` tags `v*`. File: `release.yml`.

**Expected**: `on: push: tags: ['v*']`; `permissions` include `contents: write`, `packages: write`. Steps: Checkout (`fetch-depth: 0`) → Set up Go (`go-version-file: go.mod`, cache) → Set up QEMU (`linux/amd64`, `linux/arm64`) → Set up Docker Buildx (`id: buildx`, same platforms) → Login to GHCR (`docker/login-action`, `ghcr.io`) → GoReleaser (`goreleaser/goreleaser-action` pinned, pass `GITHUB_TOKEN` and `BUILDX_BUILDER: ${{ steps.buildx.outputs.name }}`). Do not reimplement logic defined in `.goreleaser.yaml`/Dockerfile. **See Appendix B**.

### Example 4 (edge): Minimal info

**Input**: Project: legacy-api. No description. Language and commands unknown. User wants “at least one CI placeholder workflow”.

**Expected**: Produce one structurally complete, Appendix A–compliant YAML; use placeholders for runner and steps (e.g. “Specify runner and install/test commands”) and mark “to be replaced”; keep `on` narrow (e.g. `pull_request: branches: [main]`); do not invent test or build commands; keep `name`, `on`, `jobs`, `runs-on`, `steps`, and recommended fields (e.g. `permissions`) so the user can fill in later.

---

## Appendix A: Workflow output contract

The following are **mandatory** for workflow files produced by this skill; use this appendix for self-check.

**Scope**: YAML workflow files produced by this skill for a project’s `.github/workflows/`.

### A.1 File and path

- **Location**: Must live under the target project’s `.github/workflows/`.
- **Naming**: `kebab-case`, extension `.yml` or `.yaml`; name should reflect purpose (e.g. `ci.yml`, `pr-check.yml`, `release.yml`).
- **One file, one workflow**: One file defines one workflow; split into multiple files for complex cases; avoid many unrelated jobs in one file.

### A.2 Required structure

Each workflow YAML must contain (order recommended):

| Field | Required | Description |
| :--- | :--- | :--- |
| `name` | Yes | Display name in GitHub UI; short and readable (e.g. “CI”, “PR check”, “Release”). |
| `on` | Yes | Triggers: `push`, `pull_request`, `workflow_dispatch`, etc.; must narrow branch/path/tag; avoid broad `on: push` with no filter. |
| `jobs` | Yes | At least one job; each job must have `runs-on` and `steps`. |
| `jobs.<id>.runs-on` | Yes | Runner (e.g. `ubuntu-latest`). |
| `jobs.<id>.steps` | Yes | List of steps; each step has `name` (human-readable) and `uses` or `run`. |

Optional but recommended: `permissions`, `concurrency`, `env`.

### A.3 Naming and readability

- **Job id**: `kebab-case`, clear meaning (e.g. `build`, `test`, `lint`, `deploy-preview`).
- **Step name**: Short, scannable description for the Actions log.
- **Workflow name**: Align with filename and other workflows in the repo.

### A.4 Security and minimal permissions

- **Permissions**: If `permissions` is not set, GitHub uses default `GITHUB_TOKEN` permissions. For sensitive operations, set `permissions` at workflow or job level to the minimum needed. **By type**: CI (build/test/scan only) → `contents: read`; release (Release, GHCR push) → explicit `contents: write`, `packages: write`; avoid default or `all`.
- **Secrets**: Inject secrets via Secrets; never hardcode keys, tokens, or passwords in YAML.
- **Third-party actions**: Prefer official or widely used actions; pin version (commit SHA or major-version tag); do not use `@master` or unpinned; use specific versions for security/scan actions to reduce drift.

### A.5 Maintainability

- **CI vs CD (recommended)**: CI only builds, tests, and scans; **no release**. CD (image push, GitHub Release) runs only on version tags (e.g. `v*`). Use separate files (e.g. `ci.yml`, `release.yml`); do not mix “run on every push” and “release only on tag” in one workflow.
- **Reuse**: Extract common logic into Composite Actions or reusable workflows.
- **Comments**: Briefly comment non-obvious triggers, matrix strategy, or env usage; keep comments short.
- **Project alignment**: Runner, language version, package manager, and commands must match the target project; if the project has existing workflows, align style and naming.

### A.6 Self-check (producer)

After producing the workflow:

- [ ] File is under `.github/workflows/` with a kebab-case name.
- [ ] Contains `name`, `on`, `jobs`; each job has `runs-on` and `steps`.
- [ ] `on` is narrowed to specific branches/paths/tags.
- [ ] No hardcoded secrets; third-party actions pinned (specific version for security/scan).
- [ ] Step and job names are clear; consistent with project stack and existing workflow style.
- [ ] YAML is valid (indent, no duplicate keys); step order and dependencies are correct.

---

## Appendix B: Go + Docker + GHCR + GoReleaser

Conventions and practices for **Go + Docker + GHCR + GoReleaser** workflows; follow together with the main skill and Appendix A when generating or editing such workflows.

### B.1 Layout

- **CI and CD separate**: Two workflows.
  - **CI** (e.g. `ci.yml`): `push`/`pull_request` to main branch. Build, test, security scan only; **no release**.
  - **CD** (e.g. `release.yml`): Only on `push` of version tags (e.g. `v*`). Publish image and GitHub Release.
- Do not mix “run on every push” and “release only on tag” in one workflow.

### B.2 Permissions

- Set `permissions` explicitly. CI: `contents: read`. Release: `contents: write`, `packages: write`. Do not use `all`.

### B.3 Steps and order

**Go**

- Use `actions/setup-go@v5` with `go-version-file: go.mod`. Enable `cache: true`. For release, checkout with `fetch-depth: 0` (needed for GoReleaser); CI can use the same for consistency.

**CI (example order)**

1. Checkout (`fetch-depth: 0`)
2. Set up Go (go.mod + cache)
3. `go test ./...`
4. govulncheck: `go install golang.org/x/vuln/cmd/govulncheck@latest` then `govulncheck ./...`
5. Docker Buildx (setup only, single platform)
6. Build image for scanning: single arch `linux/amd64`, `push: false`, `load: true`, tag e.g. `local/your-app:ci-${{ github.sha }}`
7. Trivy on that image: `severity: HIGH,CRITICAL`, `ignore-unfixed: true`, `exit-code: 1` so CI fails on findings

Multi-arch in Release only; CI scans single arch for speed.

**Release (example order)**

1. Checkout (`fetch-depth: 0`)
2. Set up Go (go.mod + cache)
3. Set up QEMU: `docker/setup-qemu-action`, `platforms: linux/amd64,linux/arm64`
4. Set up Docker Buildx: `id: buildx`, `driver: docker-container`, `platforms: linux/amd64,linux/arm64`
5. Login to GHCR: `docker/login-action`, registry `ghcr.io`, password `secrets.GHCR_TOKEN || secrets.GITHUB_TOKEN`, `logout: true`
6. GoReleaser: `goreleaser/goreleaser-action@v6`, `args: release --clean`, env `GITHUB_TOKEN` and `BUILDX_BUILDER: ${{ steps.buildx.outputs.name }}`

QEMU before Buildx; Buildx `platforms` must match QEMU. GoReleaser needs the Buildx builder name for multi-arch, so set `id: buildx` and pass `BUILDX_BUILDER`.

### B.4 Relation to repo config

- **Docker image**: Shape is defined in `.goreleaser.yaml` and Dockerfile; workflow does not duplicate build logic.
- **GHCR**: Image path and tagging in GoReleaser config; workflow only logs in and passes `GITHUB_TOKEN` and Buildx builder.
- **Makefile**: Local build/test can stay; CI steps can align with Make targets but need not depend on them.

### B.5 When editing

1. **Full flow**: Changing one job may affect the whole flow; verify checkout → Go → QEMU → Buildx → login → GoReleaser order and deps.
2. **Action versions**: Use current major versions (e.g. `checkout@v4`, `setup-go@v5`, `setup-buildx-action@v3`, `goreleaser-action@v6`); check changelog for breaking changes when upgrading.
3. **Trivy**: Pin version (e.g. `@0.33.1`) to avoid CI breakage from behavior changes.
4. **YAML**: Check indent and no duplicate keys; validate with a tool after edits.

### B.6 Lessons learned

| Issue | Approach |
|-------|----------|
| Single workflow too large | Split into **CI + Release**: CI for build/test/scan, Release only on tag via GoReleaser; clearer permissions and logic. |
| GHCR auth too complex | Use minimal login (`docker/login-action` + token); avoid heavy auth-verify that can false-fail. |
| Multi-arch manifest validation fails | Pull and validate **per platform** instead of generic manifest pull. |
| Date/version format inconsistent | Use one format (e.g. ISO8601) in workflow and Dockerfile; add `dist/` to `.gitignore` if using GoReleaser output. |
| GoReleaser multi-arch build fails | GoReleaser needs Buildx builder: set **id: buildx** on Buildx step and pass **BUILDX_BUILDER: ${{ steps.buildx.outputs.name }}**. |
| Version drift | Use reasonable version constraints and check release notes when upgrading; validate on a branch first. |

**Inspect workflow history**: `git log --oneline -- .github/workflows/`

---

## References

- [GitHub Actions docs](https://docs.github.com/en/actions)
- [Workflow syntax](https://docs.github.com/en/actions/using-workflows/workflow-syntax-for-github-actions)
- [Security hardening](https://docs.github.com/en/actions/security-guides/security-hardening-for-github-actions)
