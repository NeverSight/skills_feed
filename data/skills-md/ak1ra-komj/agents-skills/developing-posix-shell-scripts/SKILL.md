---
name: developing-posix-shell-scripts
description: Guidelines for writing, reviewing, and refactoring strictly POSIX-compliant shell scripts (/bin/sh). No Bash features allowed. Classifies the script as simple or complex, then delegates to the appropriate reference document. Use when targeting /bin/sh, Alpine, BusyBox, embedded systems, or any environment where Bash cannot be assumed.
---

# developing-posix-shell-scripts skill

This skill covers any task involving **writing, reviewing, or refactoring** a POSIX-compliant shell script (`/bin/sh`).

**Bash-specific features are forbidden.** See [common.md](common.md) for the full list of bash-isms to avoid.

Its primary responsibility is **classification**: determine whether the script is simple or complex, then follow the matching reference document exclusively.

## Step 1 — Classify the Script

Read the script or request and evaluate the table below.

### Counting flags correctly

Before filling in the "Named flags" row, audit every proposed flag:

> **A flag only counts if a caller would genuinely pass different values in different invocations.**

- If a flag's value never varies in practice, it is a **constant** — define it with `readonly` or a plain assignment at the top of the script, not as a CLI flag.
- If a flag exists only to appear flexible, or was added because a template included it, it does not count.
- Test: _if converting this flag to a top-level constant would not change how anyone actually calls the script, it should not be a flag._

When reviewing or refactoring an existing script, re-evaluate actual flag usage — do not assume the current implementation reflects the true complexity. Re-classify from scratch using only flags that survive this audit. If the existing script is over-engineered, simplify it to match the correct classification; only preserve complexity that the script's actual functionality justifies.

| Question                              | Simple     | Complex    |
| ------------------------------------- | ---------- | ---------- |
| Expected line count (logic only)      | < 50 lines | ≥ 50 lines |
| Named flags / options needed          | 0–2        | 3 or more  |
| Structured logging required?          | No         | Yes        |
| `-h` / help output required?          | No         | Yes        |
| Cleanup / resource management?        | No         | Yes        |
| Reused across systems / environments? | No         | Yes        |

**If all answers fall in the Simple column → use [developing-simple-posix-shell-scripts.md](developing-simple-posix-shell-scripts.md).**
**If any answer falls in the Complex column → use [developing-complex-posix-shell-scripts.md](developing-complex-posix-shell-scripts.md).**

When in doubt, prefer **Simple**. It is always easier to promote a simple script to complex than to untangle unnecessary boilerplate.

## Step 2 — Follow the Reference Document

Follow the chosen reference document entirely:

- **[developing-simple-posix-shell-scripts.md](developing-simple-posix-shell-scripts.md)**: concise scripts, no boilerplate, brevity and portability over structure.
- **[developing-complex-posix-shell-scripts.md](developing-complex-posix-shell-scripts.md)**: production system utilities, compose only the reference blocks the script actually needs (see [reference-code-blocks.md](reference-code-blocks.md)).

Both documents share a common baseline defined in **[common.md](common.md)**.
