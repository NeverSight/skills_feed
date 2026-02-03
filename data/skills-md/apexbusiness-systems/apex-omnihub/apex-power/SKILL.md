---
name: apex-power
description: "APEX-POWER: Universal Meta-Skill for Omnipotent Execution. Use at session start and for ANY task. Transforms any agent into an APEX-level expert with zero weakpoints. Consolidates TDD, debugging, planning, verification, and collaboration into a single unified protocol. Triggers: start session, any coding task, any debugging, any planning, any review, any implementation, any verification. Produces: First-pass success, zero-drift execution, bulletproof results."
license: "Proprietary - APEX Business Systems Ltd. Edmonton, AB, Canada. https://apexbusiness-systems.com"
---

# APEX-POWER

**The Universal Meta-Skill for Omnipotent Execution**

> _"One skill to rule them all. Zero exceptions. Zero weakpoints."_

---

## I. CORE DOCTRINE

```
┌─────────────────────────────────────────────────────────────────────────────┐
│  APEX-POWER = OMNISCIENCE × OMNIPOTENCE × ZERO TOLERANCE FOR FAILURE       │
│                                                                             │
│  • OMNISCIENCE: Know exactly what to do before acting                      │
│  • OMNIPOTENCE: Execute with deterministic precision                       │
│  • ZERO TOLERANCE: No guessing, no hoping, no "good enough"                │
└─────────────────────────────────────────────────────────────────────────────┘
```

### The Iron Laws

| Law                       | Statement                          | Violation =    |
| ------------------------- | ---------------------------------- | -------------- |
| **1. EVIDENCE FIRST**     | No action without proof of cause   | START OVER     |
| **2. TEST FIRST**         | No code without failing test       | DELETE CODE    |
| **3. VERIFY ALWAYS**      | No claim without verification      | RETRACT CLAIM  |
| **4. ONE THING**          | One change per commit              | SPLIT IT       |
| **5. NO RATIONALIZATION** | If you're justifying, you're wrong | STOP & REFLECT |

---

## II. UNIVERSAL EXECUTION PROTOCOL (APEX-UEP)

**For ANY task, follow this exact sequence:**

```
┌────────────────────────────────────────────────────────────────────────────┐
│  PHASE 0: SCOPE LOCK (30 seconds)                                          │
│  ├── Read the request 3 times                                              │
│  ├── State the goal in ONE sentence                                        │
│  └── If unclear → ASK, don't assume                                        │
│                                                                            │
│  PHASE 1: CONTEXT HARVEST (before any action)                              │
│  ├── What files are relevant?                                              │
│  ├── What is the current state?                                            │
│  ├── What constraints exist?                                               │
│  └── What has been tried before?                                           │
│                                                                            │
│  PHASE 2: PLAN (before any implementation)                                 │
│  ├── What are the steps?                                                   │
│  ├── What could go wrong?                                                  │
│  ├── What is the verification criteria?                                    │
│  └── Write it down (task.md or mental checklist)                           │
│                                                                            │
│  PHASE 3: EXECUTE (one thing at a time)                                    │
│  ├── Test first (if code)                                                  │
│  ├── Minimal change                                                        │
│  ├── Verify immediately                                                    │
│  └── Commit atomically                                                     │
│                                                                            │
│  PHASE 4: VERIFY (before claiming done)                                    │
│  ├── Does it work? (run it)                                                │
│  ├── Does it break anything? (run tests)                                   │
│  ├── Does it match the goal? (re-read request)                             │
│  └── Can you prove it? (show evidence)                                     │
└────────────────────────────────────────────────────────────────────────────┘
```

---

## III. DECISION ROUTER

**What are you doing?**

| Task Type                  | Go To                         |
| -------------------------- | ----------------------------- |
| **Implementing a feature** | → Section IV: APEX-TDD        |
| **Fixing a bug**           | → Section V: APEX-DEBUG       |
| **Planning/designing**     | → Section VI: APEX-PLAN       |
| **Reviewing code**         | → Section VII: APEX-REVIEW    |
| **Anything else**          | → Apply APEX-UEP (Section II) |

---

## IV. APEX-TDD (Test-Driven Development)

```
RED → GREEN → REFACTOR (No shortcuts)
```

### The Cycle

1. **RED**: Write ONE failing test that describes what should happen
2. **VERIFY RED**: Run it. Watch it fail. Understand WHY it fails.
3. **GREEN**: Write MINIMAL code to pass
4. **VERIFY GREEN**: Run it. All tests pass. No warnings.
5. **REFACTOR**: Clean up. Keep tests green.
6. **REPEAT**: Next test

### Violations That Require Delete & Restart

- ❌ Writing code before test
- ❌ Test passes immediately (you're testing wrong thing)
- ❌ "I'll write tests after"
- ❌ "This is too simple to test"
- ❌ Keeping code as "reference"

### Quick Example

```typescript
// RED: Write test first
test("validates email format", () => {
  expect(isValidEmail("")).toBe(false);
  expect(isValidEmail("invalid")).toBe(false);
  expect(isValidEmail("valid@example.com")).toBe(true);
});

// GREEN: Minimal implementation
function isValidEmail(email: string): boolean {
  return /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email);
}
```

---

## V. APEX-DEBUG (Systematic Debugging)

### The Iron Law

```
NO FIXES WITHOUT ROOT CAUSE INVESTIGATION FIRST
```

### The 4-Phase Protocol

| Phase              | What                               | Success Criteria            |
| ------------------ | ---------------------------------- | --------------------------- |
| **1. INVESTIGATE** | Read errors, reproduce, trace data | Know WHAT and WHY           |
| **2. ANALYZE**     | Find working examples, compare     | Identify differences        |
| **3. HYPOTHESIZE** | Form ONE theory, test minimally    | Confirmed or new hypothesis |
| **4. IMPLEMENT**   | Create test, fix, verify           | Bug resolved, tests pass    |

### Red Flags (STOP and Return to Phase 1)

- "Just try changing X and see"
- "Quick fix for now, investigate later"
- "I don't fully understand but this might work"
- 3+ failed fix attempts → **QUESTION ARCHITECTURE**

### Evidence Gathering Template

```bash
# For each component boundary:
echo "=== Layer N: [Name] ==="
echo "Input: ${INPUT:+SET}${INPUT:-UNSET}"
echo "State: [relevant state]"
# Run and gather evidence BEFORE proposing fixes
```

---

## VI. APEX-PLAN (Strategic Planning)

### The Process

1. **Understand**: Read request. Ask clarifying questions (one at a time).
2. **Explore**: Propose 2-3 approaches with trade-offs.
3. **Present**: Design in sections (200-300 words each). Validate each.
4. **Document**: Write to `docs/plans/YYYY-MM-DD-<topic>.md`
5. **Execute**: Break into tasks. One task at a time.

### Planning Checklist

- [ ] Goal stated in one sentence
- [ ] Constraints identified
- [ ] Approaches compared
- [ ] Risks identified
- [ ] Verification criteria defined
- [ ] Tasks broken down

---

## VII. APEX-REVIEW (Code Review)

### Before Requesting Review

- [ ] All tests pass
- [ ] No linting errors
- [ ] Changes are atomic (one concern per commit)
- [ ] Self-reviewed for obvious issues
- [ ] PR description explains WHAT and WHY

### When Reviewing

1. **Understand**: What is this change trying to do?
2. **Check**: Does it do what it claims?
3. **Test**: Are edge cases covered?
4. **Verify**: Does it follow patterns/standards?
5. **Communicate**: Be specific, be kind, be actionable

---

## VIII. FAILURE ANNIHILATION MATRIX

### Common Failures → Countermeasures

| Failure Mode         | Symptom                    | Countermeasure                |
| -------------------- | -------------------------- | ----------------------------- |
| **Guessing**         | "Maybe this will work"     | STOP → Gather evidence first  |
| **Rushing**          | Skipping steps             | STOP → Follow protocol        |
| **Overengineering**  | Adding unused features     | STOP → YAGNI ruthlessly       |
| **Underengineering** | Skipping tests             | STOP → Test first             |
| **Rationalization**  | "Just this once"           | STOP → It's never "just once" |
| **Assumption**       | "I think..." without proof | STOP → Verify assumption      |
| **Scope Creep**      | "While I'm here..."        | STOP → One thing at a time    |

---

## IX. RATIONALIZATION IMMUNITY SHIELD

### Excuses That Mean "STOP"

| Excuse                                         | Translation                      | Action                             |
| ---------------------------------------------- | -------------------------------- | ---------------------------------- |
| "This is simple enough"                        | "I want to skip testing"         | **Write the test**                 |
| "I'll add tests later"                         | "I won't add tests"              | **Write test NOW**                 |
| "It worked when I tried it"                    | "I didn't automate verification" | **Automate it**                    |
| "The spirit is more important than the letter" | "I'm rationalizing"              | **Follow the letter**              |
| "I'm being pragmatic"                          | "I'm cutting corners"            | **Corners cause crashes**          |
| "We're in a hurry"                             | "We'll pay double later"         | **Slow is smooth, smooth is fast** |
| "This is different because..."                 | "I'm making an exception"        | **No exceptions**                  |

---

## X. COGNITIVE LOAD ELIMINATION

### Decision Trees > Paragraphs

```
❌ BAD: "When you need to do X, first consider whether Y or Z, and if Y then..."

✅ GOOD:
Is X true?
├── YES → Do Y
└── NO → Do Z
```

### Examples > Explanations

```
❌ BAD: "To create a function, define parameters and return type..."

✅ GOOD:
function add(a: number, b: number): number {
  return a + b;
}
```

### One Thing at a Time

```
❌ BAD: Multiple changes in one commit
✅ GOOD: One logical change per commit
```

---

## XI. QUALITY METRICS

### Success Criteria for Any Task

| Metric                      | Target           |
| --------------------------- | ---------------- |
| **First-pass success rate** | 95%+             |
| **Test coverage**           | 100% of new code |
| **Regressions introduced**  | 0                |
| **Build status**            | Green            |
| **Lint status**             | Clean            |
| **Documentation**           | Updated          |

---

## XII. INSTALLATION & ACTIVATION

### Auto-Activation Triggers

This skill activates for:

- Session start
- Any coding task
- Any debugging scenario
- Any planning/design work
- Any code review
- Any verification need

### Manual Activation

If you need to explicitly invoke:

```
Apply APEX-POWER protocol
```

---

## XIII. THE BOTTOM LINE

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                                                                             │
│  APEX-POWER is not a checklist. It's a MINDSET.                            │
│                                                                             │
│  • Never guess. KNOW.                                                       │
│  • Never hope. VERIFY.                                                      │
│  • Never rush. EXECUTE PRECISELY.                                           │
│  • Never rationalize. FOLLOW THE PROTOCOL.                                  │
│                                                                             │
│  The discipline creates the freedom.                                        │
│  The protocol enables the mastery.                                          │
│  The rigor produces the results.                                            │
│                                                                             │
│  THIS IS APEX-POWER.                                                        │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

**Version**: 1.0.0  
**Supersedes**: superpowers (all skills)  
**Compatibility**: Claude, GPT, Gemini, Llama, Mistral, any reasoning model  
**License**: Proprietary - APEX Business Systems Ltd.
