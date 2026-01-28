---
name: aeo-core
description: Main AEO skill - calculates confidence scores and decides execution path. Auto-loads on /aeo command.
---

# AEO Core - Confidence Engine

**Purpose:** Calculate confidence scores (0-1) and decide whether to execute autonomously or involve the human.

## Activation

Loads when user types `/aeo` in Claude Code.

## Confidence Calculation

### Phase 0: Spec Validation (First Gate)

```javascript
// Invoke spec-validator to check if task is well-defined
spec_score = aeo_spec_validator.validate(task)

if spec_score < 40:
    return REFUSE("Spec too unclear - need more details")

// Continue with confidence calculation
```

### Phase 1: Rule-Based Score

Start with base confidence of 0.50, then adjust:

**Add for Clarity (+0.15 each):**
- [ ] Explicit acceptance criteria defined
- [ ] Tech stack specified
- [ ] Dependencies listed
- [ ] Test requirements defined

**Add for Context (+0.10 each):**
- [ ] Similar successful task exists in memory
- [ ] Familiar codebase area
- [ ] Recent successful commits in this area

**Subtract for Risk (-0.10 each):**
- [ ] Touching authentication/security
- [ ] Modifying core infrastructure
- [ ] Large scope (>5 files, >500 LOC)
- [ ] Unclear dependencies

```javascript
base_confidence = clamp(0.50 + clarity_score + context_score - risk_score, 0.0, 1.0)
```

### Phase 2: Spec Score Adjustment

```javascript
// Adjust based on spec quality
if spec_score >= 80: base_confidence += 0.10  // Excellent spec
elif spec_score < 60: base_confidence -= 0.10  // Poor spec
```

### Phase 3: Security Multipliers

```javascript
// Critical areas get confidence penalty
if task.touches_payments: base_confidence *= 0.5  // Payments need human oversight
elif task.touches_auth: base_confidence *= 0.7    // Auth needs review
```

### Phase 4: LLM Adjustment (Optional)

If you have uncertainty about the task, adjust ±0.10:

```javascript
final_confidence = clamp(base_confidence + llm_adjustment, 0.0, 1.0)
```

## Decision Thresholds

Based on final_confidence, decide execution path:

### **≥ 0.85: AUTONOMOUS**
- Execute without asking
- Note: "Confidence: 0.XX - proceeding autonomously"
- Continue to execution loop

### **≥ 0.70: ADVISORY**
- Note risk clearly
- Offer to pause: "Confidence: 0.XX - [CONCERNS]. I can proceed or pause."
- If no response in 5 seconds, continue
- Otherwise wait for human input

### **≥ 0.50: BLOCKING**
- Explain concerns
- Wait for confirmation before proceeding
- Format:
  ```
  ⚠️ CONFIDENCE BELOW THRESHOLD

  Confidence: 0.XX
  Threshold: 0.70

  Concerns:
  • [Spec] Missing acceptance criteria
  • [Risk] Touching authentication
  • [Context] No similar tasks in memory

  Options:
  1. Proceed with assumptions
  2. Clarify spec first
  3. Break into smaller tasks

  Please confirm (1-3):
  ```

### **< 0.50: REFUSE**
- Explain why task can't be executed
- Request clarification or spec improvement
- Format:
  ```
  ❌ CANNOT EXECUTE - INSUFFICIENT CONFIDENCE

  Confidence: 0.XX

  Why:
  • Spec score: 35/100 (below 40 threshold)
  • Touching security without clear requirements
  • No acceptance criteria defined

  What's needed:
  1. Clear acceptance criteria
  2. Security requirements specified
  3. Test requirements defined

  Please improve spec and try again.
  ```

## Learning from Outcomes

After task completes, write signal to memory:

```bash
# Append to signal log
echo '{
  "timestamp": "$(date -u +%Y-%m-%dT%H:%M:%SZ)",
  "task_id": "unique-id",
  "task_description": "brief description",
  "predicted_confidence": 0.85,
  "actual_difficulty": "easy|medium|hard",
  "success": true,
  "adjustment": +0.05
}' >> ~/.claude/MEMORY/aeo-signals.jsonl
```

**Actual Difficulty Rating:**
- **easy:** Task went smoothly, no blockers
- **medium:** Minor issues or clarifications needed
- **hard:** Significant problems, multiple iterations

**Confidence Adjustment:**
- easy + success: +0.05
- medium + success: +0.00
- hard + success: -0.05
- any failure: -0.10

**Rolling Window:** Keep last 100 signals, calculate adjustment average

## Reading Past Signals

On startup, read recent signals to calibrate:

```bash
# Get last 100 signals
tail -100 ~/.claude/MEMORY/aeo-signals.jsonl | jq -s '. | map(.adjustment) | add / length'
```

Apply average adjustment as offset to all confidence calculations.

## Integration Flow

1. **User activates:** Types `/aeo`
2. **Calculate confidence:** Follow phases 0-4
3. **Make decision:** Based on thresholds
4. **If autonomous:** Execute task
5. **If advisory/blocking:** Invoke aeo-escalation skill
6. **Post-execution:** Invoke aeo-qa-agent for review
7. **Record outcome:** Write to signal log
8. **Update model:** Adjust future confidence based on outcome

## Memory Files

- **Signals:** `$PAI_DIR/MEMORY/aeo-signals.jsonl`
- **Escalations:** `$PAI_DIR/MEMORY/aeo-escalations.jsonl`
- **Patterns:** `$PAI_DIR/MEMORY/aeo-failure-patterns.json`

## Escalation Triggers

Invoke aeo-escalation skill when:
- Confidence < 0.70 (advisory/blocking)
- Spec score < 40 (refuse)
- QA veto occurs
- Failure pattern can't be resolved
- Cost limit approaching (if cost-governor enabled)

## Example Session

```
User: /aeo
User: Add user authentication with email verification

AEO: [Invoking aeo-spec-validator]
AEO: Spec score: 72/100
AEO: Calculating confidence...
      - Base: 0.50
      - Clarity: +0.30 (acceptance criteria, tech stack)
      - Context: +0.10 (similar task in memory)
      - Risk: -0.10 (touching auth)
      - Spec adj: -0.10 (spec < 80)
      - Security mult: ×0.7
      - Final: 0.49

AEO: [Invokes aeo-escalation]
AEO: ❌ CONFIDENCE BELOW THRESHOLD
     Confidence: 0.49

     Concerns:
     • [Spec] Missing security requirements
     • [Risk] Touching authentication
     • [Context] Need email service details

     Options:
     1. Add security requirements and proceed
     2. Provide email service details
     3. Break into smaller tasks

     Please clarify (1-3):

User: 2
User: We use Resend for emails, API key in .env

AEO: Recalculating confidence with added context...
     Final: 0.71

AEO: ⚡ ADVISORY - Confidence: 0.71
     [Acceptance criteria defined]
     [Tech stack: Node.js, bcrypt, jwt]
     [Email: Resend, API key in .env]

     Proceeding with implementation. I'll pause if issues arise.

[Implementation proceeds]
```

## Special Cases

### Repeated Tasks
If same task done successfully 3+ times:
- Add +0.10 to confidence
- Flag as "routine - can be autonomous"

### High-Risk Areas
Never reach full autonomy for:
- Payment processing (max 0.70)
- Authentication changes (max 0.75)
- Database migrations (max 0.80)
- Production deployments (max 0.85)

### Emergency Rollbacks
If task causes test failures or errors:
- Immediately rollback
- Write failure signal
- Reduce confidence by 0.20
- Require human review before retry
