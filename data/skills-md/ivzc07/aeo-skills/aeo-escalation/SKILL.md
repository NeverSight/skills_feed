---
name: aeo-escalation
description: Human-AI interface for when to interrupt and involve humans. Presents clear options and records decisions.
---

# AEO Escalation

**Purpose:** Human-AI interface for when to interrupt and involve humans. Presents clear, actionable options and records decisions for learning.

## When to Escalate

Invoke this skill when:
- Confidence score < 0.70 (advisory/blocking from aeo-core)
- Spec score < 40 (refuse from aeo-spec-validator)
- QA veto occurs (from aeo-qa-agent)
- Failure pattern can't be resolved (from aeo-failure-patterns)
- Cost limit approaching (if cost-governor enabled)
- Architecture violation detected (if architecture skill enabled)

## Escalation Framework

All escalations must follow this format:

```
⚠️ ESCALATION REQUIRED

[Clear one-line summary of the issue]

Context:
• [Why we're here - what triggered escalation]
• [What we've tried so far]
• [What's blocking progress]

Options:
1. [Clear, actionable option] - [Expected outcome]
2. [Clear, actionable option] - [Expected outcome]
3. [Clear, actionable option] - [Expected outcome]

Recommended: [Option X] - [Brief rationale]

Your choice (1-3):
```

## Escalation Scenarios

### Scenario 1: Low Confidence (Blocking)

**Trigger:** Confidence 0.50-0.69

```
⚠️ CONFIDENCE BELOW THRESHOLD

Confidence: 0.62
Threshold: 0.70 (Autonomous)

Task: Add user authentication with email verification

Context:
• Spec score: 68/100 (minor gaps)
• Risk: Touching authentication system
• Missing: Email service configuration
• Similar tasks: 2 successful, 1 failed

Concerns:
• [Spec] No email service specified
• [Risk] Auth changes require review
• [Context] Need email provider details

Options:
1. Proceed with Resend for emails (default) - Autonomously complete with assumptions
2. Provide email service details first - Improve spec, then execute autonomously
3. Break into smaller tasks - Create subtasks for review and approval

Recommended: Option 2 - Specify email service to improve confidence

Your choice (1-3):
```

**After user responds:**
- Record decision to `$PAI_DIR/MEMORY/aeo-escalations.jsonl`
- Update confidence model based on outcome
- Continue with chosen path

---

### Scenario 2: Spec Refused (Unacceptable)

**Trigger:** Spec score < 40

```
❌ CANNOT EXECUTE - SPEC TOO UNCLEAR

Spec Score: 28/100
Threshold: 40 (Minimum)

Task: Improve the signup

Why this was refused:
• Objective vague (5/15) - "improve" is subjective
• No acceptance criteria (0/15) - What defines "done"?
• Missing context (0/10) - Which signup flow?
• No dependencies listed (0/10)
• Ambiguity penalty: -10 (vague verb "improve")

What's needed:
1. **Clear Objective:** What specific improvement?
2. **Acceptance Criteria:** How do we measure success?
3. **Context:** Which page/component?
4. **Dependencies:** Libraries, APIs, services?

Good spec example:
"Add email validation to /pages/auth/signup.tsx using validator.js.
 Must validate RFC 5322, reject + aliases, show inline errors.
 Tests for valid, invalid, duplicate emails."

Options:
1. Provide improved spec - I'll wait for your updated specification
2. Answer clarifying questions - I'll ask specific questions to build spec
3. Use template - I'll provide a spec template for you to fill

Recommended: Option 2 - Answer questions to build spec together

Your choice (1-3):
```

---

### Scenario 3: QA Veto (Security Issue)

**Trigger:** Security vulnerability detected

```
🚨 SECURITY VETO - CANNOT PROCEED

Issue: SQL Injection vulnerability
File: /routes/users.js:Line 47
Severity: CRITICAL

Current Code:
```javascript
const query = `SELECT * FROM users WHERE id = ${userId}`
```

Why this is dangerous:
• User input directly interpolated into SQL query
• Attacker can execute arbitrary SQL commands
• Can expose, modify, or delete all data

Required Fix:
```javascript
const query = 'SELECT * FROM users WHERE id = $1'
await db.query(query, [userId])
```

Action Required:
• This MUST be fixed before commit
• No exceptions - security is non-negotiable
• All changes with security issues are blocked

Options:
1. Fix immediately - I'll apply the required fix now
2. Review fix together - I'll show you the fix for approval
3. Explain more - I'll provide detailed explanation of vulnerability

Recommended: Option 1 - Fix immediately (this is a critical issue)

Your choice (1-3):
```

---

### Scenario 4: Failure Pattern Not Recognized

**Trigger:** Error not in core patterns or project patterns

```
❌ CANNOT AUTO-FIX - PATTERN NOT RECOGNIZED

Error: TypeError: Cannot read properties of undefined (reading 'data')

Searched:
• 20 core patterns - No match
• 12 project patterns - No match
• Fuzzy match: None with confidence ≥ 0.70

Context:
• File: /src/services/UserService.js:125
• Function: fetchUserData()
• Error occurred during: API call processing

Stack trace:
TypeError: Cannot read properties of undefined (reading 'data')
    at UserService.fetchUserData (/src/services/UserService.js:125)
    at async Component.render (/src/components/UserList.tsx:45)

What I've tried:
• Verified module is installed ✓
• Checked imports - all valid ✓
• Reviewed recent changes - no obvious issues ✗

Options:
1. Provide fix - If you know the solution, I'll apply it
2. Investigate together - I'll add logging and we'll debug
3. Create new pattern - After we fix it, I'll save this pattern for future

Recommended: Option 2 - Investigate together to understand root cause

Your choice (1-3):
```

---

### Scenario 5: Cost Limit Warning

**Trigger:** Budget 80% consumed

```
⚠️ COST LIMIT APPROACHING

Budget Status:
• Daily budget: $10.00
• Used so far: $8.47 (84.7%)
• Remaining: $1.53
• Tasks completed: 7

Current task estimate: ~$0.75
Projected overage: ~$0.22 if we continue

Options:
1. Continue anyway - Proceed with current task (may exceed budget)
2. Pause and review - Review completed work, decide what's essential
3. Adjust scope - Complete current task with reduced scope

Recommended: Option 2 - Review progress before continuing

Your choice (1-3):
```

---

### Scenario 6: Architecture Violation

**Trigger:** Circular dependency detected

```
⚠️ ARCHITECTURE VIOLATION DETECTED

Issue: Circular dependency between modules

Circular Path:
→ fileA.js imports fileB.js
→ fileB.js imports fileA.js
→ (cycle detected)

Why this matters:
• Creates tight coupling
• Makes code hard to test
• Can cause runtime errors
• Violates clean architecture principles

Options:
1. Extract shared code - Create new module for shared functionality
2. Refactor dependencies - Restructure to remove cycle
3. Defer to architect - Let architecture skill analyze and propose solution

Recommended: Option 1 - Extract shared code (most common pattern)

Your choice (1-3):
```

---

## Decision Recording

After human chooses an option, record to memory:

```bash
# Append to escalation log
echo '{
  "timestamp": "$(date -u +%Y-%m-%dT%H:%M:%SZ)",
  "task_id": "unique-id",
  "escalation_type": "low_confidence|spec_refused|qa_veto|pattern_unknown|cost_warning|arch_violation",
  "confidence_before": 0.62,
  "option_presented": [1, 2, 3],
  "option_chosen": 2,
  "human_input": "User provided email service details",
  "resolution": "Improved spec, confidence increased to 0.85",
  "success": true,
  "learning": "Context details improve confidence by ~0.20"
}' >> ~/.claude/MEMORY/aeo-escalations.jsonl
```

## Learning from Escalations

**Weekly Analysis:**
```bash
# Read escalation patterns
jq -s 'group_by(.escalation_type) | map({type: .[0].escalation_type, count: length})' \
  ~/.claude/MEMORY/aeo-escalations.jsonl
```

**Insights to track:**
- Most common escalation types
- Which options are chosen most frequently
- Average confidence after escalation
- Resolution time
- Success rate of different options

## Integration Flow

1. **Trigger received** from another AEO skill
2. **Format escalation** with clear options
3. **Present to human** with recommended option
4. **Wait for response**
5. **Record decision** to memory
6. **Execute chosen option**
7. **Follow up** - Was the resolution successful?
8. **Learn** - Update escalation patterns

## Best Practices

**DO:**
- Always provide 2-4 clear, actionable options
- Include a recommended option with rationale
- Explain context clearly (what led to escalation)
- Keep options mutually exclusive
- Make options specific and actionable
- Record outcome for future learning

**DON'T:**
- Present vague options like "continue or stop"
- Overwhelm with >4 options
- Skip the recommendation
- Forget to explain the context
- Present options that aren't actually available
- Skip recording the outcome

## Example Session

```
AEO-Core: Confidence 0.52 - below threshold
        [Invokes aeo-escalation]

Escalation: ⚠️ CONFIDENCE BELOW THRESHOLD

           Confidence: 0.52
           Threshold: 0.70

           Task: Refactor authentication system

           Concerns:
           • [Spec] No clear requirements defined
           • [Risk] Touching critical auth system
           • [Scope] Large, unclear boundaries

           Options:
           1. Define requirements first - Create detailed spec
           2. Break into smaller tasks - Create manageable subtasks
           3. Get architect approval - Ensure approach is sound

           Recommended: Option 1 - Define requirements

Human: 1

Escalation: [Recording choice]
           What specific requirements do you need documented?

Human: We need to support OAuth, JWT, and API keys

Escalation: [Updating spec]
           [Recalculating confidence...]
           New confidence: 0.78 ✓

           Proceeding with implementation.

[Records to memory: escalation_type=low_confidence, option_chosen=1, success=true]
```

## Escalation Outcomes

Track outcomes to improve escalation quality:

**Successful Outcomes:**
- Human provides needed info → Task completes
- Issue resolved → Continue autonomously
- Learning captured → Better future decisions

**Unsuccessful Outcomes:**
- Wrong option recommended → Adjust recommendation logic
- Unclear options → Improve option clarity
- Missing context → Add more context to escalation
- Repeated escalations → Identify root cause

Use outcomes to refine escalation patterns and recommendations.
