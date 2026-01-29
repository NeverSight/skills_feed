---
name: ai-code-review-collaboration
description: Framework for bouncing code reviews between multiple AI models (Claude, Gemini, DeepSeek, GPT, etc.) to get comprehensive analysis. Use when user wants multiple AI perspectives on code, architecture decisions, or technical reviews. Triggers on "get other AI opinions", "review with multiple AIs", "bounce ideas off other AI", "multi-AI review", or "collaborative AI review".
---

# Multi-AI Code Review Collaboration Framework

A systematic approach to getting diverse AI perspectives on code, then synthesizing insights into actionable improvements.

## When to Use This

- Complex codebases where blind spots are likely
- Production/live trading code where reliability is critical
- Architecture decisions with trade-offs
- When you want to validate Claude's recommendations
- Before major refactoring or deployment

## The Process

### Phase 1: Initial Review (Claude)
1. Claude reviews code and documents findings
2. Creates context prompt for external AI
3. Identifies platform-specific constraints external AI must understand

### Phase 2: External AI Review
1. User pastes prompt to external AI (Gemini, DeepSeek, GPT, etc.)
2. External AI provides structured review
3. User brings response back to Claude

### Phase 3: Synthesis & Debate
1. Claude evaluates external AI's points
2. Categorizes into: Valid, Partially Valid, Invalid
3. Explains reasoning for each categorization
4. Creates response prompt for user to continue dialogue

### Phase 4: Consensus
1. Continue rounds until agreement reached
2. Document final action plan
3. Prioritize fixes by risk and effort

## Prompt Templates

### Template A: Initial External AI Request

```
**[AI NAME] CODE REVIEW REQUEST - [PROJECT TYPE]**

I need a comprehensive code review. This code [CRITICAL CONTEXT - e.g., "runs on live funded accounts"]. Please review thoroughly and respond in a format I can share with another AI for collaborative discussion.

---

## CRITICAL PLATFORM CONTEXT (Read First)

[List platform-specific constraints that might not be obvious]
[List what IS and ISN'T possible on this platform]
[Explain why certain "standard" patterns don't apply]

---

## REVIEW SCOPE

Please analyze:
1. **Logic & Correctness** - [specific concerns]
2. **Risk Management** - [specific concerns]  
3. **Performance** - [specific concerns]
4. **Reliability** - [specific concerns]
5. **Code Quality** - [specific concerns]
6. **Scalability** - [planned expansion, multi-instance needs, performance at scale]
7. **Future Updateability** - [extension points, configuration extensibility, technical debt, breaking change risks]

---

## FUTURE ROADMAP (if applicable)

[Describe planned features, scaling needs, and future requirements so the reviewer can assess how well the current architecture supports them]

---

## THE CODE

[Include full code or key sections]

---

## RESPONSE FORMAT

Structure your response as:

**[AI NAME] CODE REVIEW - ROUND 1**

## ðŸ”´ CRITICAL ISSUES (Must Fix)
## ðŸŸ¡ IMPORTANT CONCERNS (Should Fix)  
## ðŸŸ¢ MINOR SUGGESTIONS (Nice to Have)
## âœ… WELL IMPLEMENTED
## ðŸ”® SCALABILITY ASSESSMENT
## ðŸ”§ FUTURE UPDATEABILITY ASSESSMENT
## â“ QUESTIONS / CLARIFICATIONS NEEDED
## ðŸ“‹ PRIORITIZED ACTION PLAN

---

## EXISTING FINDINGS (if any)

[Include prior AI findings so new AI can confirm/challenge]
```

### Template B: Response to External AI

```
**CLAUDE'S RESPONSE TO [AI NAME] - ROUND [N]**

## âœ… FULL AGREEMENT
[Points we agree on completely]

## ðŸ¤ CONCESSIONS & MODIFICATIONS  
[Points where Claude adjusts position with explanation]

## ðŸ›¡ï¸ POINTS I STILL MAINTAIN
[Disagreements with detailed reasoning]

## ðŸ” NEW OBSERVATIONS
[Anything new Claude notices based on discussion]

## ðŸ“‹ UPDATED ACTION PLAN
[Current consensus on what to fix]

## ðŸ¤ CLOSING QUESTION
[Ask if they agree or have remaining concerns]
```

### Template C: Final Consensus Summary

```
## MULTI-AI REVIEW CONSENSUS

**Participants:** [List AIs involved]
**Code Reviewed:** [File/project name]
**Date:** [Date]

### AGREED FIXES (In Priority Order)
| # | Issue | Fix | Effort | Risk |
|---|-------|-----|--------|------|
| 1 | [Issue] | [Solution] | [Low/Med/High] | [Low/Med/High] |

### EXPLICITLY REJECTED SUGGESTIONS
| Suggestion | Rejected Because |
|------------|------------------|
| [Suggestion] | [Platform constraint / Not applicable / etc.] |

### VERIFIED AS CORRECT
- [Item 1 that was reviewed and confirmed good]
- [Item 2]

### OPEN QUESTIONS FOR FUTURE
- [Any unresolved items to revisit later]
```

## Best Practices

1. **Always provide platform context** - External AIs apply generic patterns without knowing constraints
2. **Be specific about what CAN'T be done** - Prevents suggestions for impossible approaches
3. **Request structured responses** - Makes synthesis easier
4. **Track rounds** - Label each exchange for clarity
5. **Document consensus** - Final agreement should be explicit
6. **Implement incrementally** - Test each fix before moving to next

## Reference Files

- `references/prompt-templates.md` - Copy-paste ready templates
- `references/platform-contexts.md` - Pre-written context blocks for common platforms
- `references/synthesis-checklist.md` - How to evaluate external AI suggestions
