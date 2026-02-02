---
name: pre-mortem
description: 'Checklist-driven spec validation. Generates explicit checklists from failure-taxonomy.md, runs available tooling, then dispatches agents to verify checklist items. Triggers: "pre-mortem", "validate spec", "what could go wrong".'
---

# Pre-Mortem Skill

> **Quick Ref:** Checklist generation -> Tooling -> Agent verification. Output: `.agents/pre-mortems/*.md`

**YOU MUST EXECUTE THIS WORKFLOW. Do not just describe it.**

**Architecture:** Generate explicit checklist from failure-taxonomy.md BEFORE reading spec. Tools verify what's verifiable. Agents check what requires judgment. Every finding must have location (line number) and specific fix.

## Execution Steps

Given `/pre-mortem <spec-or-plan>`:

### Step 1: Load the Spec/Plan

If a path is provided, read it:
```
Tool: Read
Parameters:
  file_path: <provided path>
```

If no path, check for recent plans:
```bash
ls -lt .agents/plans/ .agents/specs/ 2>/dev/null | head -5
```

### Step 1a: Search for Prior Failure Learnings (if ao available)

**Before generating the checklist, search for relevant past failures:**

```bash
# Search for prior failure patterns related to this topic
ao search "failure <topic>" 2>/dev/null || echo "ao not available, skipping failure pattern search"

# Also search for incidents and anti-patterns
ao search "incident <topic>" 2>/dev/null
ao anti-patterns 2>/dev/null | grep -i "<topic>" || true
```

**Review ao search results:** If ao returns relevant learnings, incorporate them:
- **Prior incidents:** Add checks for conditions that caused past failures
- **Known anti-patterns:** Add specific checklist items to verify they're avoided
- **Lessons learned:** Use these to generate additional verification questions

**Note:** This search runs BEFORE generating the checklist so prior knowledge can inform what to check.

### Step 2: Generate Explicit Checklist BEFORE Reading

**Load the failure taxonomy FIRST:**
```
Tool: Read
Parameters:
  file_path: skills/pre-mortem/references/failure-taxonomy.md
```

**For each category in the taxonomy, generate specific questions:**

| Category | Checklist Item | Verification Method |
|----------|----------------|---------------------|
| Interface Mismatch | Does spec define API schema? | Search for `schema:` or `interface` |
| Timing | Does spec define timeouts? | Search for `timeout:` |
| Error Handling | Does spec define error states? | Search for `error:` or `failure:` |
| Safety | Does spec require confirmation for destructive ops? | Search for `confirm` |
| Integration | Does spec list dependencies? | Search for `depends:` or `requires:` |
| Rollback | Does spec define rollback procedure? | Search for `rollback` or `revert` |
| State | Does spec define state transitions? | Search for `state:` or `transition` |

**The checklist above covers 7 essential items. For comprehensive validation, use all 10 categories from `references/failure-taxonomy.md`.**

**Build the checklist BEFORE reading the spec.** This prevents pattern-matching bias.

### Step 3: Run Mechanical Cross-Reference Check

**Before dispatching agents, run automated cross-reference:**

```bash
./scripts/spec-cross-reference.sh <spec-file> | tee .agents/pre-mortems/cross-ref.md
```

This catches mechanically:
- File paths that don't exist
- Function/type references that aren't defined
- Broken markdown links

Include output in pre-mortem report under "## Cross-Reference Verification"

### Step 3a: Run Available Tooling

**If the spec references code that exists:**

```bash
# If code exists, run linting
./scripts/toolchain-validate.sh --quick 2>&1 | head -30
```

**If spec is for new code:** Skip to Step 4.

### Step 4: Dispatch Verification Agents (with Checklist)

**Agents VERIFY checklist items, not "simulate failures".**

Launch 3 agents in parallel:

```
Tool: Task (ALL 3 IN PARALLEL)
Parameters:
  subagent_type: "agentops:gap-identifier"
  model: "haiku"
  description: "Verify spec completeness against checklist"
  prompt: |
    Spec file: <spec content>

    Checklist to verify (from failure-taxonomy.md):

    For EACH item, read the spec and answer:
    | Checklist Item | Present? | Location (line) | Complete? |
    |----------------|----------|-----------------|-----------|
    | API schema defined | yes/no | line N | yes/partial/no |
    | Timeouts specified | yes/no | line N | yes/partial/no |
    | Error states listed | yes/no | line N | yes/partial/no |
    | Rollback procedure | yes/no | line N | yes/partial/no |
    | Dependencies listed | yes/no | line N | yes/partial/no |
    | State transitions | yes/no | line N | yes/partial/no |
    | Confirmation for destructive ops | yes/no | line N | yes/partial/no |

    For items marked "no" or "partial": flag as GAP with specific fix.

Tool: Task
Parameters:
  subagent_type: "agentops:assumption-challenger"
  model: "haiku"
  description: "Find implicit assumptions"
  prompt: |
    Spec file: <spec content>

    Find statements that assume something without stating it:
    - "The user will..." -> What if they don't?
    - "The API returns..." -> What if it errors?
    - "This runs after..." -> What if order changes?

    For each assumption:
    | Location (line) | Assumption | What If Wrong? | Specific Clarification Needed |
    |-----------------|------------|----------------|-------------------------------|

    Every finding MUST have a line number and specific fix.

Tool: Task
Parameters:
  subagent_type: "agentops:edge-case-hunter"
  model: "haiku"
  description: "Find boundary conditions"
  prompt: |
    Spec file: <spec content>

    For each input/parameter in the spec:
    | Location (line) | Input | Type | Min/Max Stated? | Empty Handling? | Invalid Handling? |
    |-----------------|-------|------|-----------------|-----------------|-------------------|

    Flag any inputs without explicit boundary handling.
    Every finding MUST have a line number and specific fix.
```

**Timeout:** 2 minutes per agent.

### Step 5: Categorize Findings

Combine agent outputs and categorize:

| Severity | Definition | Action |
|----------|------------|--------|
| **CRITICAL** | Spec has fundamental gap (no rollback, no error handling) | Must fix before implementation |
| **HIGH** | Spec makes unstated assumptions | Should clarify |
| **MEDIUM** | Spec could be clearer | Worth noting |
| **LOW** | Minor improvements | Optional |

**Every finding must have:**
1. Location (line number in spec)
2. Description (what's missing or unclear)
3. Specific fix (exact text to add/change)

### Apply Enhancement Patterns

For each finding, identify the applicable pattern from `references/enhancement-patterns.md`:

| Gap Type | Enhancement Pattern |
|----------|---------------------|
| Missing schema | "Schema from Code" - Extract schema from actual code |
| Missing error handling | "Error Recovery Matrix" - Map all error types to actions |
| Missing timeouts | "Per-Tool Timeout Configuration" - Add per-operation timeouts |
| Missing safety info | "Mandatory Safety Display" - Add safety level classification |
| Missing progress feedback | "Progress Feedback Specification" - Add update frequency |
| Missing escalation | "Escalation Flow" - Define when/how to escalate |
| Missing audit trail | "Audit Trail Requirements" - Add logging requirements |

### Step 6: Write Pre-Mortem Report

**Write to:** `.agents/pre-mortems/YYYY-MM-DD-<topic>.md`

```markdown
# Pre-Mortem: <Topic>

**Date:** YYYY-MM-DD
**Spec:** <path to spec/plan>

## Checklist Verification

| Category | Item | Present? | Location | Complete? |
|----------|------|----------|----------|-----------|
| Interface | API schema | yes/no | line N | yes/no |
| Timing | Timeouts | yes/no | line N | yes/no |
| Error | Error states | yes/no | line N | yes/no |
| Safety | Confirmation | yes/no | line N | yes/no |
| Rollback | Rollback procedure | yes/no | line N | yes/no |
| Deps | Dependencies listed | yes/no | line N | yes/no |
| State | State transitions | yes/no | line N | yes/no |

## Findings

### CRITICAL (Must Fix Before Implementation)
1. **<Issue>**: <Description>
   - **Location:** line N
   - **Why Critical:** <explanation>
   - **Specific Fix:** <exact text to add to spec>

### HIGH (Should Clarify)
1. **<Issue>**: <Description>
   - **Location:** line N
   - **Assumption Made:** <what's assumed>
   - **Specific Clarification:** <exact question to answer>

### MEDIUM
- **<Issue>** (line N): <issue and specific fix>

## Implicit Assumptions Found
| Location | Assumption | Risk | Clarification Needed |
|----------|------------|------|---------------------|

## Edge Cases Without Handling
| Location | Input | Boundary Missing | Suggested Handling |
|----------|-------|-----------------|-------------------|

## Verdict

[ ] READY - All checklist items present, no CRITICAL gaps
[ ] NEEDS WORK - <count> CRITICAL gaps must be addressed
```

### Step 7: Request Human Approval (Gate 3)

**Gate Criteria:**
- **READY**: 0 CRITICAL gaps, <=2 HIGH gaps
- **NEEDS WORK**: 1+ CRITICAL or >2 HIGH gaps

```
Tool: AskUserQuestion
Parameters:
  questions:
    - question: "Pre-mortem found <N> gaps. Proceed to implementation?"
      header: "Gate 3"
      options:
        - label: "Proceed"
          description: "Gaps acceptable, start implementation"
        - label: "Fix Spec"
          description: "Address gaps before implementing"
        - label: "More Research"
          description: "Need more information"
      multiSelect: false
```

### Step 8: Report to User

Tell the user:
1. Checklist verification results (table)
2. Number of gaps by severity
3. Top 3 items that need attention (with line numbers)
4. Location of pre-mortem report
5. Gate 3 decision

## Key Differences from Previous Version

| Before | After |
|--------|-------|
| "Simulate failures" (vague) | Verify checklist items (specific) |
| 4 failure experts | 3 verification agents |
| Gestalt impression | Explicit checklist + location (line number) |
| No methodology | Uses failure-taxonomy.md |
| Findings without location | Every finding has line number and specific fix |
| Pattern matching | Mechanical verification |
