---
name: developer-pip-designer
description: This skill should be used when the user asks to "create a PIP", "design performance improvement plan", "write performance plan", "document performance issues", or "create formal improvement plan". Creates fair, legal-safe PIPs with clear expectations, measurable milestones, evidence documentation, and legally-compliant language.
version: 0.1.0
license: MIT
---

# Developer PIP Designer

Create Performance Improvement Plans (PIPs) that are fair, specific, measurable, and legally defensible while supporting employee success.

## Purpose

Design PIPs that:
- Clearly document performance gaps
- Set specific, measurable improvement goals
- Provide support and resources
- Establish fair timeline and checkpoints
- Use legally-safe language
- Create paper trail for potential termination

## Core Framework

### PIP Structure

```markdown
# Performance Improvement Plan

**Employee:** [Name]
**Role:** [Title]
**Manager:** [Manager Name]
**Start Date:** [Date]
**Duration:** 90 days
**Review Date:** [90 days from start]

## Performance Gaps

### Gap 1: [Specific Area]
**Current Performance:** [Observable, specific behaviors]
**Expected Performance:** [Clear standard for role/level]
**Evidence:**
- [Date]: [Specific incident/pattern]
- [Date]: [Specific incident/pattern]

### Gap 2: [Specific Area]
[Same structure]

## Improvement Goals

### Goal 1: [Measurable objective]
**Success Criteria:** [How measured, by when]
**Support Provided:** [Resources, training, mentorship]
**Checkpoint Date:** Week 4

### Goal 2: [Measurable objective]
[Same structure]

## Support & Resources

- Weekly 1:1s with manager
- [Specific training/resources]
- [Mentorship/pairing]
- [Tools/access needed]

## Checkpoints

| Date | Milestone | Success Criteria |
|------|-----------|------------------|
| Week 2 | Early progress check | [Specific deliverable] |
| Week 4 | First formal review | [Measurable outcome] |
| Week 8 | Midpoint assessment | [Measurable outcome] |
| Week 12 | Final review | [All goals met Y/N] |

## Consequences

If performance does not improve to meet expectations by [End Date], employment may be terminated.

## Acknowledgment

_Employee Signature:_ _________________ _Date:_ _______
_Manager Signature:_ _________________ _Date:_ _______

*This is a working document. Please consult HR before finalizing.*
```

## Legal-Safe Language

**❌ AVOID:**
- "You're not a team player"
- "Your attitude is bad"
- "You don't fit our culture"
- "Always" / "Never"
- Vague criticisms

**✅ USE INSTEAD:**
- "Missed 3 of last 4 sprint commitments"
- "Received feedback from 2 teammates about..."
- "Code reviews average 36 hours (team norm: 24 hours)"
- Specific, observable, measurable behaviors

## Documentation Requirements

**For each performance gap:**
1. Specific dates and incidents
2. Observable behaviors (not assumptions)
3. Impact on team/product
4. Prior feedback given (documented)
5. Attempts to address informally

**Evidence to Gather:**
- Performance review notes
- 1:1 meeting notes
- Peer feedback
- Project outcomes
- Attendance records
- Code review metrics

## Common Mistakes

**Mistake:** Surprise PIP (no prior feedback)
**Fix:** Document informal feedback first, escalate gradually

**Mistake:** Vague goals ("be more proactive")
**Fix:** Specific, measurable ("Ship 2 features independently by Week 8")

**Mistake:** Unrealistic timeline
**Fix:** 60-90 days standard, longer for complex skills

**Mistake:** No support provided
**Fix:** Explicit mentorship, training, resources

## Using Supporting Resources

### Templates
- **`templates/pip-template.md`** - Full PIP document template
- **`templates/evidence-log.json`** - Performance issue tracking

### References
- **`references/legal-pip-language.md`** - Compliant phrasing
- **`references/pip-best-practices.md`** - Fair, effective PIPs

### Scripts
- **`scripts/validate-pip-legal.py`** - Check for problematic language

**IMPORTANT:** Always consult HR and legal before issuing PIP.

---

**Progressive Disclosure:** Legal compliance, difficult scenarios, and manager coaching in references/.
