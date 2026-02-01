---
name: user-feedback-system
description: Builds feedback collection systems using Superhuman's PMF framework and YC's "talk to users" methodology. Use when implementing NPS surveys, scheduling user interviews, or measuring product-market fit.
---

# The Feedback Loop

## When This Skill Activates

Claude uses this skill when:
- Building feedback collection
- Measuring product-market fit
- Implementing user research
- Creating feedback systems

## Core Frameworks

### 1. Superhuman PMF Survey

**The Question:**
> "How would you feel if you could no longer use [product]?"
> - Very disappointed
> - Somewhat disappointed
> - Not disappointed

**PMF Threshold:**
- >40% "very disappointed" = strong PMF
- <40% = need to improve

### 2. Talk to Users (YC)

**The Approach:**
- Talk to users weekly (minimum)
- Ask open-ended questions
- Watch them use product
- Focus on jobs-to-be-done

---

## Action Templates

### Template: Feedback System

```markdown
# Feedback Collection System

## In-App Surveys
**PMF Survey:**
- Trigger: After 2 weeks of use
- Question: "How disappointed if couldn't use?"
- Follow-up: "What's the main benefit?"

**NPS Survey:**
- Trigger: Quarterly
- Question: "How likely to recommend (0-10)?"
- Follow-up: "Why that score?"

## User Interviews
**Cadence:** [Weekly/biweekly]
**Participants:** [How selected]
**Format:**
- 30-minute calls
- Watch them use product
- Ask "why?" 5 times

## Feature Requests
**Collection:**
- In-app widget
- Support tickets
- User interviews

**Tracking:**
- Count: [number of requests]
- Priority: [using RICE]
- Status: [planned/not planned]
```

---

## Quick Reference

### 💬 Feedback Checklist

**Collect:**
- [ ] PMF survey implemented
- [ ] NPS tracking
- [ ] User interview cadence
- [ ] Feature request system

**Act:**
- [ ] Feedback reviewed weekly
- [ ] Patterns identified
- [ ] Prioritized using RICE
- [ ] Closed loop (tell users what you built)

---

## Key Quotes

**YC:**
> "Talk to users. All the time. Until it feels like you're doing it too much."

**Superhuman:**
> "Product-market fit isn't a feeling. It's a number: 40% very disappointed."

