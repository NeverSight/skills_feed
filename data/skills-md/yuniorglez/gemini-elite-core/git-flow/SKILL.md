---
name: git-flow
id: git-flow
version: 1.1.0
description: "Senior Workflow Architect. Master of Trunk-Based Development, Stacked Changes, and 2026 Branching Strategies."
---

# 🌊 Skill: Git Flow & Workflow Architect (v1.1.0)

## Executive Summary
The `git-flow` architect is responsible for the structural integrity and velocity of the repository. In 2026, where deployment cycles are measured in minutes, choosing the right workflow is a competitive advantage. This skill focuses on **Trunk-Based Development** for speed, **Stacked Changes** for review efficiency, and maintaining a linear, forensic-ready history.

---

## 📋 Table of Contents
1. [Core Workflow Philosophies](#core-workflow-philosophies)
2. [The "Do Not" List (Anti-Patterns)](#the-do-not-list-anti-patterns)
3. [Trunk-Based Development (TBD)](#trunk-based-development-tbd)
4. [Stacked Changes (Graphite/Stack)](#stacked-changes-graphitestack)
5. [Enterprise Branching Strategies](#enterprise-branching-strategies)
6. [Repository Automation Standards](#repository-automation-standards)
7. [Reference Library](#reference-library)

---

## 🏗️ Core Workflow Philosophies

1.  **Linear History**: Prefer `rebase` over `merge` for feature branches to keep a clean line of progression.
2.  **Short-Lived Branches**: Any branch existing for more than 48 hours is a risk to integration.
3.  **Deployability**: The `main` branch must ALWAYS be deployable. Broken `main` is an emergency.
4.  **Verifiability**: No code merges without a green CI status and a positive "Critic Agent" or human review.

---

## 🚫 The "Do Not" List (Anti-Patterns)

| Anti-Pattern | Why it fails in 2026 | Modern Alternative |
| :--- | :--- | :--- |
| **Long-Lived Features** | Leads to "Integration Hell" and massive conflicts. | Use **Feature Flags** and TBD. |
| **Mega Pull Requests** | Reviews are superficial and slow. | Use **Stacked Changes**. |
| **Direct Commits to Main**| Bypasses CI and quality gates. | Use **Branch Protection Rules**. |
| **Merge Commits (Noise)** | Clutters the history and breaks bisect. | Use **Rebase & Squash**. |
| **Manual Versioning** | Error-prone and slow. | Use **Semantic Release / Changesets**. |

---

## ⚡ Trunk-Based Development (TBD)

The gold standard for 2026 velocity.
-   **Step 1**: Tiny commits to `main` (via short-lived PRs).
-   **Step 2**: 100% automated test coverage.
-   **Step 3**: Decouple deployment from release via **Feature Flags**.

*See [References: Trunk-Based Development](./references/trunk-based-development.md) for the workflow.*

---

## 🔨 Stacked Changes (Graphite/Stack)

Master the art of high-volume, low-friction reviews.
-   Break 1 giant feature into 5 dependent PRs.
-   Reviewers approve 100 lines at a time.
-   Restack automatically when parents change.

*See [References: Stacked Changes](./references/stacked-changes-graphite.md) for details.*

---

## 🏢 Enterprise Branching Strategies

When TBD isn't enough:
-   **One-Flow**: For structured but simple environments.
-   **Git Flow (Legacy)**: For rigid, scheduled release cycles.
-   **GitLab Flow**: For complex environment-based deployments.

---

## 🤖 Repository Automation Standards

-   **Pre-merge Checks**: Lint, Types, Tests, Security Scan.
-   **Auto-merge**: Use "Merge when pipeline succeeds" for low-risk PRs.
-   **Stale Branch Cleanup**: Automated scripts to prune merged or abandoned branches.

---

## 📖 Reference Library

Detailed deep-dives into Workflow Architecture:

- [**Trunk-Based Development**](./references/trunk-based-development.md): The high-velocity blueprint.
- [**Stacked Changes**](./references/stacked-changes-graphite.md): Reviewing at 2026 speeds.
- [**Branching Strategies**](./references/branching-strategies-2026.md): Choosing the right flow for your team.

---

*Updated: January 22, 2026 - 19:00*
