---
name: one-pass-debug
version: 1.0.0
description: "Omniscient zero-iteration debugging protocol. Triggers: debug, fix bug, error, crash, failing test, broken code, not working, exception, stack trace, troubleshoot, diagnose issue. Produces: Single surgical fix with 100% certainty. BLOCKS code changes until root cause proven. Eliminates guess-and-check loops entirely."
license: "Proprietary - APEX Business Systems Ltd. Edmonton, AB, Canada. https://apexbusiness-systems.com"
compatibility: "Universal LLM (Claude, GPT, Gemini, Llama, Mistral, Codex, DeepSeek, Qwen)"
---

# ONE-PASS DEBUG — Omniscient Zero-Iteration Debugging Protocol

> **"NEVER touch code until you're 1000% certain. Simulate first. Execute once. Done."**

## CONTRACT

**Input**: Bug report, error message, failing test, broken behavior, stack trace, or "it doesn't work"
**Output**: Single surgical fix applied with zero guessing, zero iteration, zero rollback needed
**Success**: Problem solved in ONE code change. No "let me try this" loops.

---

## THE GOLDEN RULE

```
┌─────────────────────────────────────────────────────────────────┐
│  ⛔ NEVER TOUCH CODE UNTIL PRE-FLIGHT CHECKLIST = 100% GREEN   │
│                                                                 │
│  If ANY uncertainty exists → GATHER MORE EVIDENCE              │
│  If simulation reveals gaps → MAP THE UNKNOWN                  │
│  If root cause is assumed → PROVE IT FIRST                     │
│                                                                 │
│  CODE CHANGES ARE THE LAST STEP, NOT THE FIRST                 │
└─────────────────────────────────────────────────────────────────┘
```

---

## PHASE 1: SCOPE LOCK (2 minutes max)

**Goal**: Define EXACT problem boundaries. No scope creep. No tangents.

### Checklist
```
□ What EXACTLY is broken? (One sentence, no "and")
□ What is the EXPECTED behavior?
□ What is the ACTUAL behavior?
□ When did it LAST work? (Commit hash, date, or "never")
□ What CHANGED since it last worked?
```

### Decision Tree
```
Can you answer ALL 5 questions with certainty?
├─ YES → Proceed to Phase 2
└─ NO → STOP. Get answers first. DO NOT PROCEED.
```

### Output Template
```
SCOPE LOCK COMPLETE:
- Broken: [exact symptom]
- Expected: [exact behavior]  
- Actual: [exact behavior]
- Last worked: [timestamp/commit]
- Changed since: [specific changes]
```

---

## PHASE 2: CONTEXT HARVEST (5-15 minutes)

**Goal**: Gather ALL relevant evidence. Leave no stone unturned.

### Mandatory Collection
```
1. ERROR EVIDENCE
   □ Full stack trace (not truncated)
   □ Exact error message (copy-paste, not paraphrased)
   □ Error code if present
   □ Line numbers + file paths

2. STATE EVIDENCE  
   □ Input that triggers bug
   □ Environment (OS, runtime version, config)
   □ Relevant variable values at crash point
   □ Database/API state if applicable

3. CODE EVIDENCE
   □ The failing code block (with 20 lines context above/below)
   □ Related functions/methods it calls
   □ Recent changes (git diff or equivalent)
   □ Test that reproduces the bug

4. TIMELINE EVIDENCE
   □ When bug first appeared
   □ Frequency (always/sometimes/rare)
   □ Conditions that trigger vs don't trigger
```

### Evidence Sufficiency Check
```
Can you answer these WITHOUT guessing?
├─ What exact line fails? → If NO, add logging/breakpoints
├─ What exact value causes failure? → If NO, inspect state
├─ What exact condition triggers it? → If NO, test variations
└─ ALL YES? → Proceed to Phase 3
```

---

## PHASE 3: ROOT CAUSE DEDUCTION (The Core)

**Goal**: Eliminate ALL possibilities until ONE remains. Not guessing—PROVING.

### The Deduction Matrix

```
┌────────────────────────────────────────────────────────────────┐
│ HYPOTHESIS → EVIDENCE → VERDICT                                │
├────────────────────────────────────────────────────────────────┤
│ H1: [theory]                                                   │
│   Evidence for: [what supports this]                           │
│   Evidence against: [what contradicts this]                    │
│   Verdict: ✓ PROVEN / ✗ ELIMINATED / ? NEEDS MORE DATA        │
├────────────────────────────────────────────────────────────────┤
│ H2: [theory]                                                   │
│   Evidence for: [...]                                          │
│   Evidence against: [...]                                      │
│   Verdict: ✓ / ✗ / ?                                          │
├────────────────────────────────────────────────────────────────┤
│ H3: [theory]                                                   │
│   ... continue until ONE remains proven                        │
└────────────────────────────────────────────────────────────────┘
```

### Hypothesis Generation Rules
```
ALWAYS generate minimum 3 hypotheses:
1. The obvious cause (what it looks like)
2. The upstream cause (what feeds into it)
3. The environmental cause (what surrounds it)

COMMON ROOT CAUSE CATEGORIES:
- Data: null/undefined, wrong type, missing field, stale cache
- Logic: off-by-one, wrong operator, inverted condition, race condition
- State: mutation, async timing, lifecycle order, memory leak
- Config: wrong env var, missing dependency, version mismatch
- Integration: API contract change, network, timeout, auth
```

### Elimination Protocol
```
For each hypothesis:
1. What would be TRUE if this hypothesis is correct?
2. What would be FALSE if this hypothesis is correct?
3. Check the evidence against both.
4. If evidence contradicts → ELIMINATE
5. If evidence supports → KEEP, gather more proof
6. Continue until ONE hypothesis has overwhelming evidence
```

### Root Cause Certainty Gate
```
⛔ DO NOT PROCEED UNLESS:
□ Only ONE hypothesis remains
□ You can explain WHY all others are wrong
□ You can predict EXACTLY what the fix will change
□ You can describe the bug to a colleague in 30 seconds
```

---

## PHASE 4: MENTAL SIMULATION (Critical)

**Goal**: Execute the fix IN YOUR MIND first. Find edge cases before touching code.

### Simulation Protocol
```
1. TRACE FORWARD
   - Start at the bug
   - Apply your fix mentally
   - Trace execution path forward
   - What changes? What stays same?

2. TRACE BACKWARD  
   - Start at desired outcome
   - What must be true for fix to work?
   - What assumptions are you making?
   - Are those assumptions valid?

3. EDGE CASE SWEEP
   □ What if input is null/empty?
   □ What if input is maximum size?
   □ What if called multiple times?
   □ What if called out of order?
   □ What if network/IO fails?
   □ What if concurrent access?

4. BLAST RADIUS CHECK
   □ What other code calls this function?
   □ Will fix break any of those callers?
   □ Are there tests that will now fail?
   □ Are there dependent systems affected?
```

### Simulation Output
```
MENTAL SIMULATION COMPLETE:
- Fix location: [file:line]
- Fix action: [exact change]
- Execution path verified: [YES/NO]
- Edge cases checked: [list]
- Blast radius: [none/contained/widespread]
- Side effects: [none/list them]
- Confidence: [must be 100% to proceed]
```

---

## PHASE 5: PRE-FLIGHT CHECKLIST

**⛔ MANDATORY GATE — Code changes BLOCKED until ALL green**

```
┌─────────────────────────────────────────────────────────────────┐
│                    PRE-FLIGHT CHECKLIST                         │
├─────────────────────────────────────────────────────────────────┤
│ □ Scope is locked (no creep)                                   │
│ □ All evidence collected (no gaps)                             │
│ □ Root cause PROVEN (not assumed)                              │
│ □ Other hypotheses ELIMINATED (with evidence)                  │
│ □ Mental simulation passed (all paths traced)                  │
│ □ Edge cases checked (no surprises)                            │
│ □ Blast radius known (side effects mapped)                     │
│ □ Fix is MINIMAL (smallest possible change)                    │
│ □ Fix is SURGICAL (touches only what's needed)                 │
│ □ Rollback plan exists (if impossible scenario)                │
├─────────────────────────────────────────────────────────────────┤
│ ALL GREEN? → Execute Phase 6                                   │
│ ANY RED?   → Return to appropriate phase. DO NOT PROCEED.      │
└─────────────────────────────────────────────────────────────────┘
```

---

## PHASE 6: SURGICAL EXECUTION

**Goal**: One precise cut. No exploratory surgery.

### Execution Rules
```
1. Make the SMALLEST change that fixes the root cause
2. Change ONE thing at a time (even if fix has multiple parts)
3. Each change must be independently testable
4. Comment WHY if the fix is non-obvious
5. NO "while I'm here" improvements—fix ONLY the bug
```

### Fix Template
```
// FIX: [ticket/issue number]
// ROOT CAUSE: [one sentence]
// CHANGE: [what you're changing and why]
[minimal code change here]
```

### Post-Fix Validation
```
□ Bug reproduction test now passes
□ All existing tests still pass
□ Manual verification of expected behavior
□ Edge cases from simulation verified
□ No new warnings/errors introduced
```

---

## PHASE 7: CLOSURE PROTOCOL

**Goal**: Ensure bug CANNOT return. Document for future.

### Closure Checklist
```
□ Root cause documented (for future reference)
□ Regression test added (catches if bug returns)
□ Related code reviewed (same pattern elsewhere?)
□ Knowledge shared (team aware of pattern)
```

### Closure Statement
```
BUG RESOLVED:
- Root cause: [one sentence]
- Fix applied: [file:line, change summary]
- Regression test: [test name/location]
- Pattern risk: [none/low/medium—where else might this exist?]
```

---

## ANTI-PATTERNS (What Creates Loops)

### ❌ "Let me try this"
Changing code to see what happens = GUESSING
→ You will loop. Go back to Phase 3.

### ❌ "It might be..."
Uncertainty = insufficient evidence
→ Go back to Phase 2. Collect more.

### ❌ "I'll fix this and that"
Multiple changes = unknown cause of success
→ ONE change. ONE test. ONE conclusion.

### ❌ "The stack trace points here"
Stack trace shows WHERE, not WHY
→ Phase 3 finds WHY. Don't skip it.

### ❌ "Works on my machine"
Environment difference = missing evidence
→ Add environment to Phase 2 collection.

### ❌ "I've seen this before"
Pattern matching without proof = assumption
→ PROVE it's the same. Evidence required.

---

## UNIVERSAL APPLICABILITY

This protocol works for ALL code because it targets the DEBUG PROCESS, not the language:

| Domain | Phase 2 Additions | Phase 3 Focus |
|--------|------------------|---------------|
| Frontend | Console logs, network tab, DOM state | State management, async timing, render cycles |
| Backend | Server logs, DB queries, API traces | Request lifecycle, auth flow, data transform |
| Mobile | Device logs, crash reports, memory profile | Lifecycle, threading, platform APIs |
| Database | Query plans, locks, transaction logs | Joins, indexes, constraints, isolation |
| Infra | System logs, metrics, config diffs | Resource limits, network, permissions |
| ML/AI | Training logs, tensor shapes, gradients | Data pipeline, model architecture, hyperparams |

---

## QUICK REFERENCE

```
PHASE 1: SCOPE LOCK      → What EXACTLY is broken?
PHASE 2: CONTEXT HARVEST → Gather ALL evidence
PHASE 3: ROOT CAUSE      → Prove ONE cause, eliminate rest
PHASE 4: SIMULATION      → Run fix mentally first
PHASE 5: PRE-FLIGHT      → ALL checks green?
PHASE 6: EXECUTION       → One surgical change
PHASE 7: CLOSURE         → Prevent return, document
```

---

## THE PROMISE

If you complete all phases with discipline:
- **ZERO** "let me try this" loops
- **ZERO** "that didn't work, let me try something else"
- **ZERO** debugging sessions lasting hours
- **ONE** pass from bug to fix
- **100%** confidence before touching code

**This is not debugging. This is SURGERY.**

---

© 2025 APEX Business Systems Ltd. Edmonton, AB, Canada.
Licensed for use within Claude AI skills framework.
All rights reserved.
