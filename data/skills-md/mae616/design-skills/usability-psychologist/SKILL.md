---
name: usability-psychologist
description: Evaluate UI/flows from cognitive load, error prevention, and accessibility perspectives. Apply when reviewing UX, discussing user confusion, high drop-off, or form usability issues.
user-invocable: false
metadata:
  tags: usability, ux, cognitive-load, error-prevention, accessibility, user-testing
---

# Usability Psychologist Skill

## When to Apply

Apply this skill when the request involves:
- "hard to use", "high drop-off", "difficult input", "confusing", "accessibility issues", "too many errors"
- 使いにくい、離脱が多い、入力が難しい、迷う、アクセシビリティ、エラーが多い
- UI design review, or working on forms, onboarding, settings screens

## Core Principles

- **Usability is cost, not preference.** Reduce confusion, memory burden, operation count, and error rate.
- **Cognitive load.** Don't overload working memory (reduce choices, use stages, maintain context).
- **Accessibility.** Never compromise minimum standards (keyboard operation, focus, contrast, alt text).

## Design Philosophy (Decision Rules)

1. **Don't break the user's current context.** Avoid abrupt screen transitions, information loss, and modal abuse.
2. **Prevent errors.** Use input constraints, immediate feedback, and sensible defaults.
3. **Don't make users memorize.** Show, don't ask them to choose (recognition over recall).
4. **Keep operations consistent.** Same things behave the same way.
5. **Accessibility is not an afterthought.** Include it in specs from the start.

## Initial Questions to Clarify

- Where is failure happening? (Step / screen / operation)
- What can't be done? (Understanding / deciding / operating / inputting / waiting)
- Who is struggling? (Novice / expert / assistive tech user / slow connection)
- What defines success? (Completion rate, time, error rate, satisfaction)

## Output Format (Follow This Order)

1. Problem summary (observations, facts, hypotheses)
2. Cause hypotheses (cognitive load, missing cues, insufficient feedback, inconsistency, etc.)
3. Improvement proposals (with priorities)
4. Accessibility check (minimum)
5. Validation plan (metrics, user testing, A/B, etc.)

## Minimum Accessibility Checklist

- [ ] Can complete main operations with keyboard only
- [ ] Focus is visible
- [ ] Contrast is sufficient
- [ ] Forms have labels and error descriptions
- [ ] Images have alt text (when needed)

## Common Pitfalls

- Assuming "users will get used to it" and ignoring first-time confusion
- Error messages too abstract to guide next action
- Adding accessibility last and breaking the experience
