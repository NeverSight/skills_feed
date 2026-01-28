---
name: commit-sentinel
id: commit-sentinel
version: 2.1.0
description: "Master of Ceremonies for Git. Architect of High-Integrity Repositories. Expert in Git 3.0, Forensic Bisecting, and Interactive Rebasing."
---

# 🛡️ Skill: Commit Sentinel (v2.1.0)

## Executive Summary
The `commit-sentinel` is the guardian of repository health and historical clarity. In 2026, where AI agents generate thousands of lines of code daily, the role of the sentinel is critical to prevent "History Pollution" and "Type Decay." This skill enforces a rigorous 4-step validation protocol, promotes surgical history sculpting via rebasing, and leverages automated hooks to ensure that only elite-level code reaches the main branch.

---

## 📋 Table of Contents
1. [The 4-Step Validation Protocol](#the-4-step-validation-protocol)
2. [The "Do Not" List (Anti-Patterns)](#the-do-not-list-anti-patterns)
3. [Conventional Commits 2026](#conventional-commits-2026)
4. [History Sculpting (Interactive Rebase)](#history-sculpting-interactive-rebase)
5. [Forensic Validation (Git Bisect)](#forensic-validation-git-bisect)
6. [Git 3.0 Readiness (SHA-256)](#git-30-readiness-sha-256)
7. [Automated Hook Orchestration](#automated-hook-orchestration)
8. [Reference Library](#reference-library)

---

## 🛡️ The 4-Step Validation Protocol

Before every commit, the Sentinel MUST execute:

1.  **Surgical Diff Review**: `git diff --cached` to verify every line.
    - *Filter*: Remove all `console.log`, `TODO` (unless planned), and debug artifacts.
2.  **Strict Type Audit**: `bun x tsc --noEmit` (Mandatory).
    - *Standard*: ZERO type errors allowed in the entire workspace.
3.  **Linter Enforcement**: `bun run lint`.
    - *Standard*: Adherence to the project's formatting and security rules.
4.  **Logical Atomicity**: Ensure the commit does exactly ONE thing.
    - *Check*: If the diff covers multiple features/fixes, use `git add -p` to split.

---

## 🚫 The "Do Not" List (Anti-Patterns)

| Anti-Pattern | Why it fails in 2026 | Modern Alternative |
| :--- | :--- | :--- |
| **`--no-verify`** | Bypasses safety hooks. | Fix the underlying issue. |
| **`git commit -m "update"`** | Useless for forensics/AI context. | Use **Conventional Commits**. |
| **Pushed Rebases** | Breaks the team's local history. | Only rebase **local** branches. |
| **Massive "Cleanup" Commits** | Makes `git bisect` impossible. | Use **Atomic, Incremental Changes**. |
| **SHA-1 Assumptions** | Security risk in modern Git. | Prepare for **SHA-256 (Git 3.0)**. |

---

## 📝 Conventional Commits 2026

We follow the strictly typed commit standard:

-   `feat(scope):` A new feature.
-   `fix(scope):` A bug fix.
-   `refactor(scope):` No feature or bug change.
-   `perf(scope):` Performance improvements.
-   `chore(scope):` Internal tools/config.
-   `docs(scope):` Documentation only.

**Structure:**
```text
type(scope)!: short description (max 50 chars)

Detailed body explaining WHY this change was made.
Wrapped at 72 chars.

BREAKING CHANGE: [details]
Resolves #123
```

---

## 🔨 History Sculpting (Interactive Rebase)

The Sentinel never pushes messy local history.

```bash
# Clean up the last 3 local commits before pushing
git rebase -i HEAD~3
```
*Use `squash` to combine small "fix" commits into a single "feat" or "fix".*

---

## 🔍 Forensic Validation (Git Bisect)

When a bug appears, find the source with binary search.

```bash
git bisect start
git bisect bad HEAD
git bisect good [last_known_good_tag]
# Automate with:
git bisect run bun test
```

---

## 🚀 Git 3.0 Readiness

-   **SHA-256**: Transitioning away from SHA-1 for collision resistance.
-   **Rust Core**: Native speed for monorepo operations.
-   **Push Protection**: Automated secret detection in the commit loop.

---

## 📖 Reference Library

Detailed deep-dives into Git excellence:

- [**Git Forensics**](./references/git-forensics-bisect.md): Regressions and bisecting.
- [**Advanced Rebasing**](./references/advanced-rebasing.md): interactive mode and autosquash.
- [**Git 3.0 Guide**](./references/git-3-readiness.md): SHA-256 and Rust integration.
- [**Hook Automation**](./references/automated-hooks.md): Husky, Lefthook, and Pre-commit.

---

*Updated: January 22, 2026 - 17:50*
