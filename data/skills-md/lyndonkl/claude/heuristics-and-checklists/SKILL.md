---
name: heuristics-and-checklists
description: Use when making decisions under time pressure or uncertainty, preventing errors in complex procedures, designing decision rules or checklists, simplifying complex choices, or when user mentions heuristics, rules of thumb, mental models, checklists, error prevention, cognitive biases, satisficing, or needs practical decision shortcuts and systematic error reduction.
---
# Heuristics and Checklists

## Table of Contents
- [Purpose](#purpose)
- [When to Use](#when-to-use)
- [What Is It?](#what-is-it)
- [Workflow](#workflow)
- [Common Patterns](#common-patterns)
- [Guardrails](#guardrails)
- [Quick Reference](#quick-reference)

## Purpose

Heuristics and Checklists provides practical frameworks for fast decision-making through mental shortcuts (heuristics) and systematic error prevention through structured procedures (checklists). This skill guides you through designing effective heuristics for routine decisions, creating checklists for complex procedures, and understanding when shortcuts work vs. when they lead to biases.

## When to Use

Use this skill when:

- **Time-constrained decisions**: Need to decide quickly without full analysis
- **Routine choices**: Repetitive decisions where full analysis is overkill (satisficing)
- **Error prevention**: Complex procedures where mistakes are costly (surgery, software deployment, flight operations)
- **Checklist design**: Creating pre-flight, pre-launch, or pre-deployment checklists
- **Cognitive load reduction**: Simplifying complex decisions into simple rules
- **Bias mitigation**: Understanding when heuristics mislead (availability, anchoring, representativeness)
- **Knowledge transfer**: Codifying expert intuition into transferable rules
- **Quality assurance**: Ensuring critical steps aren't skipped
- **Onboarding**: Teaching newcomers reliable decision patterns
- **High-stakes procedures**: Surgery, aviation, nuclear operations, financial trading

Trigger phrases: "heuristics", "rules of thumb", "mental models", "checklists", "error prevention", "cognitive biases", "satisficing", "quick decision", "standard operating procedure"

## What Is It?

**Heuristics and Checklists** combines two complementary approaches for practical decision-making and error prevention:

**Core components**:
- **Heuristics**: Mental shortcuts or rules of thumb that simplify decisions (e.g., "recognition heuristic": choose the option you recognize)
- **Checklists**: Structured lists ensuring critical steps completed in order (aviation pre-flight, surgical safety checklist)
- **Fast & Frugal Trees**: Simple decision trees with few branches, good enough decisions with minimal information
- **Satisficing**: "Good enough" decisions (Simon) vs. exhaustive optimization
- **Bias awareness**: Recognizing when heuristics fail (availability bias, anchoring, representativeness)
- **Error prevention**: Swiss cheese model, forcing functions, fail-safes

**Quick example:**

**Scenario**: Startup CEO deciding whether to hire a candidate after interview.

**Without heuristics** (exhaustive analysis):
- Compare to all other candidates (takes weeks)
- 360-degree reference checks (10+ calls)
- Skills assessment, culture fit survey, multiple rounds
- Analysis paralysis, miss good candidates to faster competitors

**With heuristics** (fast & frugal):
1. **Recognition heuristic**: Have they worked at company I respect? (Yes → +1)
2. **Take-the-best**: What's their track record on most important skill? (Strong → +1)
3. **Satisficing threshold**: If 2/2 positive, hire. Don't keep searching for "perfect" candidate.

**Outcome**: Hired strong candidate in 3 days instead of 3 weeks. Not perfect, but good enough and fast.

**Checklist example** (Software Deployment):
```
Pre-Deployment Checklist:
☐ All tests passing (unit, integration, E2E)
☐ Database migrations tested on staging
☐ Rollback plan documented
☐ Monitoring dashboards configured
☐ On-call engineer identified
☐ Stakeholders notified of deployment window
☐ Feature flags configured for gradual rollout
☐ Backups completed
```

**Benefit**: Prevents missing critical steps. Reduces deployment failures by 60-80% (empirical data from aviation, surgery, software).

**Core benefits**:
- **Speed**: Heuristics enable fast decisions under time pressure
- **Cognitive efficiency**: Reduce mental load, free capacity for complex thinking
- **Error reduction**: Checklists catch mistakes before they cause harm
- **Consistency**: Standardized procedures reduce variance in outcomes
- **Knowledge codification**: Capture expert intuition in transferable form

## Workflow

Copy this checklist and track your progress:

```
Heuristics & Checklists Progress:
- [ ] Step 1: Identify decision or procedure
- [ ] Step 2: Choose approach (heuristic vs. checklist)
- [ ] Step 3: Design heuristic or checklist
- [ ] Step 4: Test and validate
- [ ] Step 5: Apply and monitor
- [ ] Step 6: Refine based on outcomes
```

**Step 1: Identify decision or procedure**

What decision or procedure needs simplification? Is it repetitive? Time-sensitive? Error-prone? See [resources/template.md](resources/template.md#decision-procedure-identification-template).

**Step 2: Choose approach (heuristic vs. checklist)**

Heuristic for decisions (choose option). Checklist for procedures (sequence of steps). See [resources/methodology.md](resources/methodology.md#1-when-to-use-heuristics-vs-checklists).

**Step 3: Design heuristic or checklist**

Heuristic: Define simple rule (recognition, take-the-best, satisficing threshold). Checklist: List critical steps, add READ-DO or DO-CONFIRM format. See [resources/template.md](resources/template.md#heuristic-design-template) and [resources/template.md](resources/template.md#checklist-design-template).

**Step 4: Test and validate**

Pilot test with sample cases. Check: Does heuristic produce good enough decisions? Does checklist catch errors? See [resources/methodology.md](resources/methodology.md#4-validating-heuristics-and-checklists).

**Step 5: Apply and monitor**

Use in real scenarios. Track outcomes: decision quality, error rate, time saved. See [resources/template.md](resources/template.md#application-monitoring-template).

**Step 6: Refine based on outcomes**

Adjust rules based on data. If heuristic fails in specific contexts, add exception. If checklist too long, prioritize critical items. See [resources/methodology.md](resources/methodology.md#5-refinement-and-iteration).

Validate using [resources/evaluators/rubric_heuristics_and_checklists.json](resources/evaluators/rubric_heuristics_and_checklists.json). **Minimum standard**: Average score ≥ 3.5.

## Common Patterns

**Pattern 1: Recognition Heuristic**
- **Rule**: Choose the option you recognize over the one you don't
- **Best for**: Choosing between brands, cities, experts when quality correlates with fame
- **Example**: "Which city is larger, Detroit or Milwaukee?" (Choose Detroit if only one recognized)
- **When works**: Stable environments where recognition predicts quality
- **When fails**: Advertising creates false recognition, niche quality unknown

**Pattern 2: Take-the-Best Heuristic**
- **Rule**: Identify single most important criterion, choose based on that alone
- **Best for**: Multi-attribute decisions with one dominant factor
- **Example**: Hiring - "What's their track record on [critical skill]?" Ignore other factors.
- **When works**: One factor predictive, others add little value
- **When fails**: Multiple factors equally important, interactions matter

**Pattern 3: Satisficing (Good Enough Threshold)**
- **Rule**: Set minimum acceptable criteria, choose first option that meets them
- **Best for**: Routine decisions, time pressure, diminishing returns from analysis
- **Example**: "Candidate meets 80% of requirements → hire, don't keep searching for 100%"
- **When works**: Searching costs high, good enough > perfect delayed
- **When fails**: Consequences of suboptimal choice severe

**Pattern 4: Aviation Checklist (DO-CONFIRM)**
- **Format**: Perform actions from memory, then confirm each with checklist
- **Best for**: Routine procedures with critical steps (pre-flight, pre-surgery, deployment)
- **Example**: Pilot flies from memory, then reviews checklist to confirm all done
- **When works**: Experts doing familiar procedures, flow state preferred
- **When fails**: Novices, unfamiliar procedures (use READ-DO instead)

**Pattern 5: Surgical Checklist (READ-DO)**
- **Format**: Read each step, then perform, one at a time
- **Best for**: Unfamiliar procedures, novices, high-stakes irreversible actions
- **Example**: Surgical team reads checklist aloud, confirms each step before proceeding
- **When works**: Unfamiliar context, learning mode, consequences of error high
- **When fails**: Expert routine tasks (feels tedious, adds overhead)

**Pattern 6: Fast & Frugal Decision Tree**
- **Format**: Simple decision tree with 1-3 questions, binary choices at each node
- **Best for**: Triage, classification, go/no-go decisions
- **Example**: "Is customer enterprise? Yes → Assign senior rep. No → Is deal >$10k? Yes → Assign mid-level. No → Self-serve."
- **When works**: Clear decision structure, limited information needed
- **When fails**: Nuanced decisions, exceptions common

## Guardrails

**Critical requirements:**

1. **Know when heuristics work vs. fail**: Heuristics excel in stable, familiar environments with time pressure. They fail in novel, deceptive contexts (adversarial, misleading information). Don't use recognition heuristic when advertising creates false signals.

2. **Satisficing ≠ low standards**: "Good enough" threshold must be calibrated. Set based on cost of continued search vs. value of better option. Too low → poor decisions. Too high → analysis paralysis.

3. **Checklists for critical steps only**: Don't list every trivial action. Focus on steps that (1) are skipped often, (2) have serious consequences if missed, (3) not immediately obvious. Short checklists used > long checklists ignored.

4. **READ-DO for novices, DO-CONFIRM for experts**: Match format to user expertise. Forcing experts into READ-DO creates resistance and abandonment. Let experts flow, confirm after.

5. **Test heuristics empirically**: Don't assume rule works. Test on historical cases. Compare heuristic decisions to optimal decisions. If accuracy <80%, refine or abandon.

6. **Bias awareness is not bias elimination**: Knowing availability bias exists doesn't prevent it. Heuristics are unconscious. Need external checks (checklists, peer review, base rates) to counteract biases.

7. **Update heuristics when environment changes**: Rules optimized for past may fail in new context. Market shifts, technology changes, competitor strategies evolve. Re-validate quarterly.

8. **Forcing functions beat reminders**: "Don't forget X" fails. "Can't proceed until X done" works. Build constraints (e.g., deployment script requires all tests pass) rather than relying on memory.

**Common pitfalls:**

- ❌ **Heuristic as universal law**: "Always choose recognized brand" fails when dealing with deceptive advertising or niche quality.
- ❌ **Checklist too long**: 30-item checklist gets skipped. Keep to 5-10 critical items max.
- ❌ **Ignoring base rates**: "This customer seems like they'll buy" (representativeness heuristic) vs. "Only 2% of leads convert" (base rate). Use base rates to calibrate intuition.
- ❌ **Anchoring on first option**: "First candidate seems good, let's hire" without considering alternatives. Set satisficing threshold, then evaluate multiple options.
- ❌ **Checklist as blame shield**: "I followed checklist, not my fault" ignores responsibility to think. Checklists augment judgment, don't replace it.
- ❌ **Not testing heuristics**: Assume rule works without validation. Test on past cases, measure accuracy.

## Quick Reference

**Common heuristics:**

| Heuristic | Rule | Example | Best For |
|-----------|------|---------|----------|
| **Recognition** | Choose what you recognize | Detroit > Milwaukee (size) | Stable correlations between recognition and quality |
| **Take-the-best** | Use single most important criterion | Hire based on track record alone | One dominant factor predicts outcome |
| **Satisficing** | First option meeting threshold | Candidate meets 80% requirements → hire | Time pressure, search costs high |
| **Availability** | Judge frequency by ease of recall | Plane crashes seem common (vivid) | Recent, vivid events (WARNING: bias) |
| **Representativeness** | Judge by similarity to prototype | "Looks like successful startup founder" | Stereotypes exist (WARNING: bias) |
| **Anchoring** | Adjust from initial value | First price shapes negotiation | Numerical estimates (WARNING: bias) |

**Checklist formats:**

| Format | When to Use | Process | Example |
|--------|-------------|---------|---------|
| **READ-DO** | Novices, unfamiliar, high-stakes | Read step → Do step → Repeat | Surgery (WHO checklist) |
| **DO-CONFIRM** | Experts, routine, familiar | Do from memory → Confirm with checklist | Aviation pre-flight |
| **Challenge-Response** | Two-person verification | One reads, other confirms | Nuclear launch procedures |

**Checklist design principles:**

1. **Keep it short**: 5-10 items max (critical steps only)
2. **Use verb-first language**: "Verify backups complete" not "Backups"
3. **One step per line**: Don't combine "Test and deploy"
4. **Checkbox format**: ☐ Clear visual confirmation
5. **Pause points**: Identify natural breaks (before start, after critical phase, before finish)
6. **Killer items**: Mark items that block proceeding (e.g., ⚠ Tests must pass)

**When to use heuristics vs. checklists:**

| Decision Type | Use Heuristic | Use Checklist |
|---------------|---------------|---------------|
| **Choose between options** | ✓ Recognition, take-the-best, satisficing | ✗ Not applicable |
| **Sequential procedure** | ✗ Not applicable | ✓ Pre-flight, deployment, surgery |
| **Complex multi-step** | ✗ Too simplified | ✓ Ensures nothing skipped |
| **Routine decision** | ✓ Fast rule (satisficing) | ✗ Overkill |
| **Error-prone procedure** | ✗ Doesn't prevent errors | ✓ Catches mistakes |

**Cognitive biases (when heuristics fail):**

| Bias | Heuristic | Failure Mode | Mitigation |
|------|-----------|--------------|------------|
| **Availability** | Recent/vivid events judged as frequent | Overestimate plane crashes (vivid), underestimate heart disease | Use base rates, statistical data |
| **Representativeness** | Judge by stereotype similarity | "Looks like successful founder" ignores base rate of success | Check against actual base rates |
| **Anchoring** | First number shapes estimate | Initial salary offer anchors negotiation | Set own anchor first, adjust deliberately |
| **Confirmation** | Seek supporting evidence | Only notice confirming data | Actively seek disconfirming evidence |
| **Sunk cost** | Continue due to past investment | "Already spent $100k, can't stop now" | Evaluate based on future value only |

**Inputs required:**
- **Decision/procedure**: What needs simplification or systematization?
- **Historical data**: Past cases to test heuristic accuracy
- **Critical steps**: Which steps, if skipped, cause failures?
- **Error patterns**: Where do mistakes happen most often?
- **Time constraints**: How quickly must decision be made?

**Outputs produced:**
- `heuristic-rule.md`: Defined heuristic with conditions and exceptions
- `checklist.md`: Structured checklist with critical steps
- `validation-results.md`: Test results on historical cases
- `refinement-log.md`: Iterations based on real-world performance
