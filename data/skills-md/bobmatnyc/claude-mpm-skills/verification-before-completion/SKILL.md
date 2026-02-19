---
name: verification-before-completion
description: Run verification commands and confirm output before claiming success
version: 2.0.0
category: debugging
author: Jesse Vincent
license: MIT
source: https://github.com/obra/superpowers-skills/tree/main/skills/debugging/verification-before-completion
progressive_disclosure:
  entry_point:
    summary: "Evidence before claims: mandatory verification before ANY completion claim"
    when_to_use: "When about to claim work is complete, fixed, passing, or ready. ESPECIALLY before commits, PRs, or task completion."
    quick_start: "1. Identify verification command 2. Run FULL command 3. Read complete output 4. Verify results 5. THEN claim with evidence"
  references:
    - gate-function.md
    - verification-patterns.md
    - red-flags-and-failures.md
    - integration-and-workflows.md
context_limit: 800
tags:
  - verification
  - quality-assurance
  - honesty
  - evidence
requires_tools: []
---

# Verification Before Completion

## Overview

Claiming work is complete without verification is dishonesty, not efficiency.

**Core principle:** Evidence before claims, always.

**Violating the letter of this rule is violating the spirit of this rule.**

This skill enforces mandatory verification before ANY completion claim, preventing false positives, broken builds, and trust violations.

## When to Use This Skill

Activate ALWAYS before claiming:
- Success, completion, or satisfaction ("Done!", "Fixed!", "Great!")
- Tests pass, linter clean, build succeeds
- Committing, pushing, creating PRs
- Marking tasks complete or delegating to agents

**Use this ESPECIALLY when:**
- Under time pressure or tired
- "Quick fix" seems obvious or confidence is high
- Agent reports success or tests "should" pass

## The Iron Law

```
NO COMPLETION CLAIMS WITHOUT FRESH VERIFICATION EVIDENCE
```

Without running the verification command in this message, claiming success is not allowed.

## Core Principles

1. **Evidence Required**: Every claim needs supporting evidence
2. **Fresh Verification**: Must verify now, not rely on previous runs
3. **Complete Verification**: Full command, not partial checks
4. **Honest Reporting**: Report actual state, not hoped-for state

## Quick Start

The five-step gate function:

1. **IDENTIFY**: What command proves this claim?
2. **RUN**: Execute the FULL command (fresh, complete)
3. **READ**: Full output, check exit code, count failures
4. **VERIFY**: Does output confirm the claim?
   - If NO: State actual status with evidence
   - If YES: State claim WITH evidence
5. **ONLY THEN**: Make the claim

Skip any step = lying, not verifying.

## Key Patterns

**Correct Pattern:**
```
✅ [Run pytest] [Output: 34/34 passed] "All tests pass"
```

**Incorrect Patterns:**
```
❌ "Should pass now"
❌ "Looks correct"
❌ "Tests were passing"
❌ "I'm confident it works"
```

## Red Flags - STOP Immediately

STOP when:
- Using "should", "probably", "seems to"
- Expressing satisfaction before verification
- About to commit/push/PR without verification
- Trusting agent success reports
- Relying on partial verification

**ALL of these mean: STOP. Run verification first.**

## Why This Matters

**Statistics from real-world failures:**
- Verification cost: 2 minutes
- Recovery cost: 120+ minutes (60x more expensive)
- 40% of unverified "complete" claims required rework

**Core violation:** "Lying leads to replacement"

## Navigation

For detailed information:
- **[Gate Function](references/gate-function.md)**: Complete five-step verification process with decision trees
- **[Verification Patterns](references/verification-patterns.md)**: Correct verification patterns for tests, builds, deployments, and more
- **[Red Flags and Failures](references/red-flags-and-failures.md)**: Common failure modes, red flags, and real-world examples with time/cost data
- **[Integration and Workflows](references/integration-and-workflows.md)**: Integration with other skills, CI/CD patterns, and agent delegation workflows

## The Bottom Line

**No shortcuts for verification.**

Run the command. Read the output. THEN claim the result.

This is non-negotiable.
