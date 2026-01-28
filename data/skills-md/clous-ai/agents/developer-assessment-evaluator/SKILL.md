---
name: developer-assessment-evaluator
description: This skill should be used when the user asks to "evaluate a coding assessment", "review take-home project", "score technical interview", "analyze coding challenge submission", "detect trivia over-indexing", or "provide assessment feedback". Evaluates engineering assessments against rubrics while detecting common anti-patterns like excessive focus on trivia over problem-solving ability.
version: 0.1.0
license: MIT
---

# Developer Assessment Evaluator

Evaluate technical assessments (take-homes, live coding, system design) using structured rubrics while detecting over-indexing on trivia vs. core engineering skills.

## Purpose

Provide objective, fair evaluation of candidate technical work that:
- Assesses problem-solving ability over memorization
- Detects over-reliance on algorithmic trivia
- Evaluates code quality, testing, documentation
- Ensures consistent scoring across candidates
- Identifies signal vs. noise in technical performance

## When to Use

Invoke when:
- Reviewing completed take-home assignments
- Scoring live coding interviews
- Evaluating system design discussions
- Detecting assessment anti-patterns
- Training interviewers on evaluation criteria
- Calibrating scoring across interview team

## Core Evaluation Framework

### 1. Problem-Solving Process (40%)

**Assess HOW candidate approaches problem:**
- Asks clarifying questions before coding
- Breaks problem into manageable steps
- Considers edge cases and constraints
- Iterates when hitting obstacles
- Explains thought process clearly

**Scoring:**
- 5: Methodical approach, clear reasoning, handles ambiguity well
- 3: Adequate approach, some structure
- 1: Jumps to code without planning, struggles with unknowns

**Anti-Pattern Detection:**
If candidate knows optimal algorithm immediately → may be memorized, probe deeper with follow-up

### 2. Code Quality (30%)

**Evaluate production-readiness:**
- Readable variable/function names
- Appropriate abstractions
- No obvious bugs or edge case failures
- Handles errors gracefully
- Follows language idioms

**Scoring:**
- 5: Production-ready code, well-organized
- 3: Functional code, some quality issues
- 1: Poor structure, hard to maintain

### 3. Testing & Validation (20%)

**Check verification approach:**
- Writes test cases (unit, integration)
- Tests edge cases (empty input, large input, null)
- Validates assumptions
- Handles error conditions

**Scoring:**
- 5: Comprehensive tests, edge cases covered
- 3: Basic tests present
- 1: No testing or validation

### 4. Communication (10%)

**Assess explanation clarity:**
- Explains design decisions
- Articulates trade-offs
- Responds to feedback
- Documents approach

**Scoring:**
- 5: Clear, thorough explanations
- 3: Adequate communication
- 1: Unclear or defensive

## Detecting Trivia Over-Indexing

**Warning Signs:**
- Assessment requires obscure algorithm knowledge
- Solution depends on memorizing specific pattern
- Time pressure favors memorization over problem-solving
- No partial credit for good process but wrong algorithm

**Example - Bad Assessment:**
"Implement Dijkstra's algorithm from memory in 45 minutes"
→ Tests memorization, not problem-solving

**Example - Good Assessment:**
"Design a route-finding system for our delivery app. Consider real-world constraints."
→ Tests applied problem-solving

**Rebalancing:**
- Allow candidates to look up algorithms
- Value process over perfect solution
- Give hints/guidance during interview
- Accept multiple valid approaches

## Evaluation Rubric Template

```json
{
  "candidate": "Name",
  "assessment_type": "take-home|live-coding|system-design",
  "evaluation": {
    "problem_solving": {
      "score": 4,
      "weight": 0.40,
      "evidence": "Methodical approach, asked good clarifying questions, handled edge cases"
    },
    "code_quality": {
      "score": 3,
      "weight": 0.30,
      "evidence": "Functional code, some naming could be clearer"
    },
    "testing": {
      "score": 5,
      "weight": 0.20,
      "evidence": "Comprehensive unit tests, tested edge cases thoroughly"
    },
    "communication": {
      "score": 4,
      "weight": 0.10,
      "evidence": "Clear explanations, good documentation"
    }
  },
  "weighted_score": 4.0,
  "recommendation": "Strong Hire",
  "feedback": "Excellent problem-solving and testing. Could improve variable naming.",
  "trivia_concerns": false
}
```

## Providing Constructive Feedback

**Feedback Structure:**

```markdown
## Strengths
- [Specific strength with example]
- [Specific strength with example]

## Areas for Growth
- [Constructive suggestion with example]
- [Constructive suggestion with example]

## Overall Assessment
[Summary and recommendation]
```

**Best Practices:**
- Be specific (cite code examples)
- Balance positive and constructive
- Focus on behaviors, not person
- Suggest improvements, don't just criticize

## Using Supporting Resources

### Templates
- **`templates/rubric-template.json`** - Assessment rubric schema
- **`templates/feedback-template.md`** - Candidate feedback structure

### References
- **`references/anti-patterns.md`** - Common assessment anti-patterns
- **`references/trivia-vs-skills.md`** - Distinguishing memorization from ability

### Scripts
- **`scripts/detect-trivia.py`** - Analyze assessment for trivia over-indexing
- **`scripts/score-assessment.py`** - Calculate weighted scores

---

**Progressive Disclosure:** Detailed anti-patterns, trivia detection techniques, and feedback examples in references/.
