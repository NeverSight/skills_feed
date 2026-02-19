---
name: spec-init
description: Unified skill that guides spec creation through structured, interactive process.
version: 1.0.0
model: sonnet
invoked_by: user
user_invocable: true
tools: [Read, Write, Edit]
verified: false
lastVerifiedAt: 2026-02-19T05:29:09.098Z
---

# SKILL: spec-init

## Overview

Unified skill that guides spec creation through structured, interactive process.

Wraps these existing skills:

- progressive-disclosure (requirements gathering)
- spec-validator (schema validation)
- plan-generator (plan from spec)

## Workflow

### 1. Type Detection

Question: "What are you building?"

Auto-detect from description:

- Feature: "Build X functionality" → `type: feature`
- Bug: "Fix X issue" → `type: bug`
- Chore: "Update X component" → `type: chore`
- Refactor: "Reorganize X" → `type: refactor`
- Docs: "Document X" → `type: docs`

### 2. Progressive Disclosure v2 (Adaptive, 5-7 questions)

Invoke progressive-disclosure with adaptive algorithm:

```javascript
const { AdaptiveQuestioner } = require('.claude/lib/utils/adaptive-discloser.cjs');
const { ContextAccumulator } = require('.claude/lib/utils/context-accumulator.cjs');

// Determine domain from detected type
const domainMap = {
  feature: 'general',
  bug: 'debugging',
  chore: 'general',
  refactor: 'architecture',
  docs: 'documentation',
};
const domain = domainMap[detectedType] || 'general';

const aq = new AdaptiveQuestioner(domain);
const ca = new ContextAccumulator();

let history = [];
let questionCount = 0;

while (questionCount < 7) {
  const context = ca.getContext();
  const result = await aq.getNextQuestion(context, history);

  // Check if we should stop early
  const readiness = await aq.detectOptimalStop(history, context);
  if (readiness.shouldStop) {
    break;
  }

  // Ask the question
  const answer = await AskUserQuestion({ question: result.question });

  // Store answer with metadata
  ca.addAnswer(result.question, answer, { domain, priority: 'HIGH' });
  history.push({ question: result.question, answer });

  questionCount++;
}

// Summary from accumulated context
const summary = ca.buildSummary();
```

**Key Improvements over v1:**

- Adaptive questioning (skips redundant questions)
- Context-aware (learns from answers)
- Memory-integrated (leverages learnings.md)
- Optimal stopping (5-7 questions typical, down from 10-12)
- Quality scoring (detects when ready for spec generation)

### 3. Spec Template Generation

Auto-populate spec from answers:

```markdown
# SPEC: [Feature Name]

## 1. Overview

**Title**: [From question 1]
**Type**: [Detected type]
**Objective**: [User summary]

**User Story**: As a [user type], I want [capability], so that [benefit]

**Acceptance Criteria**: [From question 5]

## 2. Problem Statement

- **Current State**: [From question 1 answers]
- **Pain Points**: [Extracted from answers]
- **Impact**: [Quantified if possible]

## 3. Proposed Solution

- **Approach**: [From user input]
- **Key Features**: [From answers]
- **Scope**: [What's in/out]

## 4. Implementation Approach

- **Phase 1**: [Design/spike if needed]
- **Phase 2**: [Core implementation]
- **Phase 3**: [Testing]
- **Phase 4**: [Documentation]

## 5. Success Metrics

- **Quantitative**: [From question 3]
- **Qualitative**: [User satisfaction]
- **Timeline**: [From question 4]

## 6. Effort Estimate

- **Design**: 1 day
- **Implementation**: 3 days
- **Testing**: 2 days
- **Documentation**: 1 day
- **Total**: 7 days

## 7. Dependencies

- **Required**: [Extracted from context]
- **Blocking**: [What must complete first]
- **Risk**: [Key risks identified]

## 8. Acceptance Criteria Checklist

- [ ] Feature implemented per spec
- [ ] All tests passing
- [ ] Documentation updated
- [ ] No breaking changes
- [ ] Performance targets met
```

### 4. Validation

Validate spec against schema:

- Invoke spec-validator skill
- Check: all required sections present
- Check: at least 3 acceptance criteria
- Check: effort estimate in days

### 5. Plan Suggestion

After spec approved:

- Suggest: "Ready for planner to create plan?"
- If yes: Show `Skill({ skill: "plan-generator", args: { specPath: "..." } })`
- If no: Allow editing spec

### 6. Storage

Save spec to:

```
.claude/context/artifacts/specs/[feature-name]-spec-YYYYMMDD.md
```

Track metadata:

- trackId: auto-generated
- type: detected
- status: "new"
- created_at: timestamp

## Usage Examples

### Example 1: Quick Feature

```
User: "I want to add dark mode to the UI"

spec-init workflow:
1. Detect: type = "feature"
2. Ask: 5 questions about dark mode
3. User answers in <5 minutes
4. Generate spec
5. Validate against schema
6. Store and offer plan generation
```

### Example 2: Bug Fix

```
User: "There's a memory leak in the scheduler"

spec-init workflow:
1. Detect: type = "bug"
2. Ask: 5 questions (reproduce steps, impact, etc)
3. Generate bug fix spec
4. Suggest acceptance criteria
5. Ready for planner
```

## Output

- Generated spec markdown (saved)
- Track metadata JSON
- Plan generation suggestion
- Next steps guidance

## Integration Points

- progressive-disclosure (requirements gathering)
- spec-validator (schema validation)
- plan-generator (next step)
- track-metadata schema (metadata)

## Memory Protocol (MANDATORY)

**Before starting:**
Read `.claude/context/memory/learnings.md`

**After completing:**

- New pattern -> `.claude/context/memory/learnings.md`
- Issue found -> `.claude/context/memory/issues.md`
- Decision made -> `.claude/context/memory/decisions.md`

> ASSUME INTERRUPTION: If it's not in memory, it didn't happen.
