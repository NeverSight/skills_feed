---
name: codex-review
description: Use after creating design docs or implementation plans to get cross-agent review from Codex. Auto-triggers for non-trivial plans; asks first for simple changes. Captures feedback, addresses critical issues, presents minor concerns for user decision.
---

# Codex Review

## Overview

Cross-agent review workflow: After creating a design doc or implementation plan, invoke Codex to review it, then address the feedback before implementation.

**Core principle:** Two agents catch more issues than one. Codex reviews with fresh eyes while Claude addresses feedback.

## When to Use

```dot
digraph trigger_decision {
    "Plan/design doc created" [shape=box];
    "Is change trivial?" [shape=diamond];
    "Ask user: use codex-review?" [shape=box];
    "Auto-trigger codex-review" [shape=box];
    "User says yes?" [shape=diamond];
    "Skip review" [shape=box];
    "Run review" [shape=box];

    "Plan/design doc created" -> "Is change trivial?";
    "Is change trivial?" -> "Ask user: use codex-review?" [label="yes"];
    "Is change trivial?" -> "Auto-trigger codex-review" [label="no"];
    "Ask user: use codex-review?" -> "User says yes?" ;
    "User says yes?" -> "Run review" [label="yes"];
    "User says yes?" -> "Skip review" [label="no"];
    "Auto-trigger codex-review" -> "Run review";
}
```

**Trivial changes:** Single-file edits, typo fixes, config changes, adding a simple function. Ask before reviewing.

**Non-trivial (auto-trigger):** Multi-file changes, new features, architectural decisions, refactors, anything with design choices.

**Also use when:** User explicitly requests codex-review (e.g., "use codex-review", "get Codex feedback").

## Invoking Codex

Run from the **project root directory**:

```bash
codex exec -C /absolute/path/to/project/root \
    --sandbox read-only \
    --full-auto \
    --skip-git-repo-check \
    "Read relative/path/to/plan.md, do research on the codebase, and then provide feedback on the plan. Point out any issues, flaws, or concerns with the plan. In your final response, provide only the feedback. Don't offer to do anything else or ask follow-up questions." 2>/dev/null
```

**Parameters:**
- `-C`: Absolute path to project root
- `--sandbox read-only`: Codex can read but not modify
- `--full-auto`: No interactive prompts
- `--skip-git-repo-check`: Works in any directory
- `2>/dev/null`: Suppress stderr noise

**Capture stdout directly** - do not write feedback to a file.

**Path handling:**
- **Plan inside project:** Use relative path from project root (e.g., `docs/plan.md`)
- **Plan outside project:** Use absolute path (e.g., `/tmp/scratch/plan.md`)
- The `-C` flag always takes the absolute project root path regardless of where the plan file lives

## What Codex Reviews Well (and Doesn't)

**Codex excels at:**
- Checking if plan matches actual codebase structure (file paths, frameworks, patterns)
- Identifying missing dependencies or incompatible libraries
- Spotting architectural mismatches (e.g., Express patterns in a Next.js app)
- Finding references to non-existent code (routes, models, functions)

**Codex may struggle with:**
- Plans referencing external systems Codex can't access (APIs, databases, third-party services)
- Very high-level or abstract plans with few concrete file/code references
- Plans for greenfield projects where there's no existing code to compare against

**If Codex feedback seems shallow:** The plan may lack enough concrete details for meaningful review. Consider adding specific file paths, function names, or code snippets before re-running.

## Processing Feedback

After receiving Codex's feedback, categorize each item:

| Category | Action |
|----------|--------|
| **Critical issues** | Address immediately without asking. These are bugs, security issues, logical flaws, missing error handling, or architectural problems that would cause failures. |
| **Minor concerns** | Present to user and ask which to address. These are style suggestions, optional improvements, alternative approaches, or "nice to have" items. |

**Format when presenting minor concerns:**

```
Codex raised these additional concerns. Which should I address?

1. [Concern summary] - [Brief context]
2. [Concern summary] - [Brief context]
3. [Concern summary] - [Brief context]

Reply with numbers to address (e.g., "1, 3") or "none" to skip.
```

## Review Rounds

**Default:** 1 round

**User can specify more:** "use codex-review with 2 rounds", "do 3 review rounds"

Do NOT ask after each round whether to continue. Complete all requested rounds, then proceed.

After each round:
1. Update the plan/design doc with changes
2. If more rounds remain, invoke Codex again on the updated doc
3. After final round, proceed to implementation

## Error Handling

```dot
digraph error_handling {
    "Run codex exec" [shape=box];
    "Success?" [shape=diamond];
    "Process feedback" [shape=box];
    "Retry once" [shape=box];
    "Success on retry?" [shape=diamond];
    "Ask user how to proceed" [shape=box];

    "Run codex exec" -> "Success?";
    "Success?" -> "Process feedback" [label="yes"];
    "Success?" -> "Retry once" [label="no (timeout/error)"];
    "Retry once" -> "Success on retry?";
    "Success on retry?" -> "Process feedback" [label="yes"];
    "Success on retry?" -> "Ask user how to proceed" [label="no"];
}
```

**On persistent failure, ask:**
```
Codex review failed after retry. How would you like to proceed?
1. Skip review and continue to implementation
2. Try again
3. I'll review the plan manually
```

## Common Mistakes

| Mistake | Fix |
|---------|-----|
| Running codex from wrong directory | Always use `-C /absolute/path/to/project/root` |
| Writing feedback to file | Capture stdout directly, don't create feedback files |
| Asking after each round | Complete all requested rounds without prompting |
| Addressing all feedback equally | Categorize: critical = auto-fix, minor = ask user |
| Forgetting to update plan between rounds | Always update the doc before next round |
| Using relative path for plan outside project | Use absolute path for files not in project root |
| Running review on vague/abstract plans | Ensure plan has concrete file paths and code references |

## Quick Reference

```
# Single round (default)
[Create plan] → codex-review → address feedback → implement

# Multiple rounds
[Create plan] → codex-review round 1 → update plan →
              → codex-review round 2 → update plan → implement

# Feedback handling
Critical issues  → Address immediately
Minor concerns   → Ask user which to address
```
