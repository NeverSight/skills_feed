---
name: skill-reviewer
description: Identify improvement opportunities in Claude Code skills through targeted review operations. Complements review-multi by focusing on actionable improvements rather than scoring. Use when seeking specific improvements, conducting improvement-focused reviews, or identifying enhancement opportunities for existing skills.
allowed-tools: Read, Write, Edit, Glob, Grep, Bash, WebSearch, WebFetch
---

# Skill Reviewer

## Overview

skill-reviewer identifies specific, actionable improvements for Claude Code skills. While review-multi provides comprehensive scoring (1-5), skill-reviewer focuses on finding and documenting improvement opportunities.

**Purpose**: Improvement discovery for existing skills

**Integration with review-multi**:
- review-multi: Comprehensive scoring, production readiness
- skill-reviewer: Improvement hunting, enhancement focus
- **Use together**: review-multi scores, skill-reviewer improves

**The 4 Review Operations**:
1. **Content Enhancement Review** - Find content that could be clearer, more complete, better examples
2. **Usability Improvement Review** - Identify user experience enhancements
3. **Integration Opportunity Review** - Find integration and composition opportunities
4. **Efficiency Improvement Review** - Identify ways to make skill more efficient

## When to Use

- Finding improvements for good skills (score 4-5 but could be better)
- Post-deployment enhancement planning
- Continuous improvement iterations
- User feedback incorporation
- Periodic skill refreshes

## Operations

### Operation 1: Content Enhancement Review

**Focus**: Better examples, clearer explanations, additional scenarios

**Process**:
1. Review examples - could any be more concrete/helpful?
2. Check explanations - any unclear sections?
3. Review scenarios - missing important use cases?
4. Check completeness - any gaps?

**Output**: List of content improvements with priorities

---

### Operation 2: Usability Improvement Review

**Focus**: Easier to use, faster to learn, more effective

**Process**:
1. Test actual usage - where's friction?
2. Check learning curve - could it be easier?
3. Review navigation - could it be clearer?
4. Check Quick Reference - could it be more helpful?

**Output**: UX improvement opportunities

---

### Operation 3: Integration Opportunity Review

**Focus**: Better integration with other skills, new composition possibilities

**Process**:
1. Review skill dependencies - could integration be smoother?
2. Check for workflow opportunities - could this compose with others?
3. Look for synergies - which skills work well together?
4. Identify gaps - what's missing for good integration?

**Output**: Integration enhancement opportunities

---

### Operation 4: Efficiency Improvement Review

**Focus**: Faster to use, better automation, reduced effort

**Process**:
1. Check for automation opportunities
2. Review process efficiency - any unnecessary steps?
3. Look for shortcuts - quick paths for common cases?
4. Check token efficiency - context optimization possible?

**Output**: Efficiency improvement opportunities

---

## Quick Reference

| Operation | Focus | Output |
|-----------|-------|--------|
| Content Enhancement | Examples, clarity, scenarios | Content improvements |
| Usability Improvement | UX, learning curve, friction | UX enhancements |
| Integration Opportunity | Composition, synergies | Integration ideas |
| Efficiency Improvement | Automation, speed | Efficiency gains |

**Use with**: review-multi (scoring) + skill-reviewer (improvements) + skill-updater (apply changes)

---

**skill-reviewer finds improvement opportunities to make good skills even better.**
