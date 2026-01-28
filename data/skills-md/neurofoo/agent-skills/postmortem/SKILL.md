---
name: postmortem
description: Blameless post-mortem incident analysis with timeline, root cause, and action items. Use after outages, security incidents, project failures, or any event you want to prevent recurring.
user-invocable: true
---

# Blameless Post-Mortem

Conduct a thorough, blameless analysis of an incident to understand what happened and prevent recurrence.

## Instructions

Work through each section systematically. Focus on systems and processes, not individuals. The goal is learning, not blame.

### Output Format

## Executive Summary

**Incident**: [One-line description]
**Date/Time**: [When it occurred]
**Duration**: [How long]
**Severity**: [Critical/High/Medium/Low]

**Summary**
[2-3 sentence overview: what happened, impact, resolution]

---

## Timeline

All times in [timezone].

| Time | Event | Actor |
|------|-------|-------|
| HH:MM | [What happened] | [Who/what did it] |
| HH:MM | [Detection] | [How it was noticed] |
| HH:MM | [Response action] | [Who responded] |
| HH:MM | [Resolution] | [What fixed it] |

**Key Moments**
- **Trigger**: [What initiated the incident]
- **Detection**: [How/when we knew something was wrong]
- **Mitigation**: [When bleeding was stopped]
- **Resolution**: [When fully resolved]

---

## Impact

**Customer Impact**
- Users affected: [number]
- Duration of impact: [time]
- Symptoms experienced: [what users saw]

**Business Impact**
- Revenue impact: [if applicable]
- SLA/SLO breach: [yes/no, details]

---

## Root Cause Analysis

**Root Cause**
[The fundamental reason this happened—not the trigger, but why the trigger caused an incident]

**Trigger**
[The immediate cause—what set things in motion]

**Contributing Factors**
| Factor | How It Contributed |
|--------|-------------------|
| [factor] | [explanation] |

**Why Wasn't This Caught?**
- Why didn't tests catch it?
- Why didn't monitoring alert earlier?

---

## What Went Well

| What Worked | Why It Helped |
|-------------|---------------|
| [thing] | [explanation] |

---

## What Went Poorly

| What Failed | Impact |
|-------------|--------|
| [thing] | [impact] |

---

## Action Items

**Immediate** (This week)
| Action | Owner | Due |
|--------|-------|-----|
| [action] | [owner] | [date] |

**Short-term** (This month)
| Action | Owner | Due |
|--------|-------|-----|
| [action] | [owner] | [date] |

---

## Lessons Learned

1. [lesson]
2. [lesson]
3. [lesson]

---

## Guidelines

- **Blameless**: "The deploy script didn't validate" not "Alice deployed without checking"
- **Thorough timeline**: Include everything, even embarrassing delays
- **Specific actions**: "Add memory alerting" not "Improve monitoring"
- **Assigned owners**: Unowned actions don't happen

$ARGUMENTS
