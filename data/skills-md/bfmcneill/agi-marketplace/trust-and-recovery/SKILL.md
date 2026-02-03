---
name: trust-and-recovery
description: Use when designing error handling, confirmation dialogs, undo functionality, or any interaction where user trust matters. Covers building confidence through predictability and graceful failure.
---

# Trust and Recovery

Trust is built through predictability and tested through failure. Users trust systems that behave consistently and recover gracefully when things go wrong.

## Evidence Tiers

```
[Research]   — Peer-reviewed studies, controlled experiments
[Expert]     — Nielsen Norman Group, recognized UX authorities
[Case Study] — Documented examples from major products
[Convention] — Industry practice, limited formal validation

Multiple tags = stronger evidence: [Research][Expert]
Mixed findings noted as: [Research — Mixed]
```

---

## Research Foundations

### Peak-End Rule

**[Research][Expert]** Daniel Kahneman's research (Nobel Prize in Economics, 2002) established that people judge experiences based on:

1. The **peak** moment (most intense, positive or negative)
2. The **end** (how it concluded)

They do not average the entire experience.

**UX implication:** A single graceful recovery can redeem an otherwise frustrating experience. Don't let the last interaction be an error.

**Source:** Kahneman, D. (1999). Objective happiness. In *Well-being: Foundations of hedonic psychology*.

### Loss Aversion

**[Research][Expert]** Kahneman & Tversky's Prospect Theory showed losses feel approximately 2x as painful as equivalent gains feel good.

**UX implication:** Users are highly motivated to avoid losing their work. Auto-save, undo, and data preservation are disproportionately important.

**Source:** Kahneman, D. & Tversky, A. (1979). Prospect Theory: An Analysis of Decision under Risk.

---

## Undo vs. Confirmation Dialogs

**[Expert]** Nielsen Norman Group and multiple UX authorities recommend undo over confirmation dialogs in most cases.

### Why Confirmation Often Fails

**[Expert]** From NNg and practitioner observation:
- Users habitually click "OK" without reading
- Frequent confirmations train users to ignore them
- Confirmations interrupt flow

### When to Use Each

| Approach | Use When | Evidence |
|----------|----------|----------|
| **Undo** | Action is reversible | [Expert] NNg |
| **Confirmation** | Action is truly irreversible AND destructive | [Expert] NNg |
| **Neither** | Routine, low-risk actions | [Convention] |

**[Case Study]** Google Drive: No confirmation for moving files to trash (reversible). Confirmation required for emptying trash (irreversible).

### Pattern: Undo Toast

**[Convention]**

```
[User clicks delete]
[Item disappears immediately]
[Toast: "Item deleted" [Undo] — auto-dismisses in 10s]
```

**Caution:** No controlled studies directly comparing undo vs. confirmation outcomes found. This is strong expert consensus, not validated research.

**Source:** [Nielsen Norman - Confirmation Dialogs](https://www.nngroup.com/articles/confirmation-dialog/)

---

## Error Message Design

**[Expert]** Nielsen's Heuristic #9: "Help users recognize, diagnose, and recover from errors."

### The Three Questions

Every error message should answer:
1. **What happened?** (Clear description)
2. **Why?** (Cause, if helpful)
3. **What now?** (Recovery path)

**Useless:**
```
Error 500: Internal Server Error
```

**Actionable:**
```
Couldn't save your changes — the server is temporarily
unavailable. Your draft has been saved locally.

[Try again] [Continue editing]
```

**[Research]** Cognitive Load Theory (Sweller) supports this: vague errors increase extraneous cognitive load.

**Source:** [Nielsen Norman - Error Message Guidelines](https://www.nngroup.com/articles/error-message-guidelines/)

---

## Core Patterns

### trust-1: Confirm Destructive, Not Routine

**[Expert]** Only interrupt for truly irreversible actions.

**Over-confirming (trains users to ignore):**
```
"Are you sure you want to save?"
"Are you sure you want to go back?"
```

**Appropriate confirmation:**
```
"Delete 47 files permanently? This cannot be undone."
[Cancel] [Delete]
```

### trust-2: Preserve Data Aggressively

**[Research]** Loss aversion (Kahneman & Tversky) explains why losing work is disproportionately frustrating.

**Trust-breaking:**
```
[User writes long comment]
[Accidentally navigates away]
[Returns — comment gone]
```

**Trust-building:**
```
[User writes long comment]
[Accidentally navigates away]
[Returns — draft restored]
```

Auto-save drafts. Preserve form state. Cache locally.

### trust-3: Degrade Gracefully

**[Convention]** Isolate failures. Don't let one problem cascade.

**Brittle:**
```
[One image fails to load]
[Entire page shows error]
```

**Graceful:**
```
[One image fails to load]
[Placeholder shown with retry option]
[Rest of page works fine]
```

### trust-4: Show System Status

**[Expert]** Nielsen's Heuristic #1: "Visibility of system status."

**Opaque:**
```
[User clicks Submit]
[Nothing happens for 3 seconds]
[Suddenly: "Submitted!"]
```

**Transparent:**
```
[User clicks Submit]
[Button shows spinner: "Submitting..."]
[Button changes: "✓ Submitted"]
```

---

## Recovery Patterns

### Pattern: Optimistic UI with Rollback

**[Convention]**

```
1. User takes action
2. UI updates immediately (optimistic)
3. Server request in background
4. If success: done
5. If failure: rollback UI + show error + offer retry
```

### Pattern: Forgiving Input

**[Expert]** Postel's Law: "Be liberal in what you accept."

```
// Rigid
Phone: [Must be exactly ###-###-####]

// Forgiving
Phone: [Accepts any format, normalizes internally]
"5551234567" → displays as "(555) 123-4567"
```

### Pattern: Graceful Timeout

**[Convention]**

```
[Operation takes too long]
"This is taking longer than expected.
 You can keep waiting or try again."
[Keep waiting] [Cancel and retry]
```

Don't make users guess if something is frozen.

---

## Anti-Patterns

| Pattern | Why It Breaks Trust | Evidence |
|---------|---------------------|----------|
| Silent failures | User doesn't know something went wrong | [Expert] NNg |
| Generic errors | No path to recovery | [Expert] NNg |
| Lost form data | Punishes user for system failure | [Research] Loss aversion |
| Inconsistent behavior | Can't build mental model | [Expert] Jakob's Law |
| Hidden data usage | Feels deceptive | [Convention] |

---

## Key Sources

- Kahneman, D. & Tversky, A. (1979). Prospect Theory.
- Kahneman, D. (1999). Objective happiness (Peak-End Rule).
- Sweller, J. (1988). Cognitive load during problem solving.
- [Nielsen Norman - Confirmation Dialogs](https://www.nngroup.com/articles/confirmation-dialog/)
- [Nielsen Norman - Error Message Guidelines](https://www.nngroup.com/articles/error-message-guidelines/)
- [A List Apart - Never Use a Warning When You Mean Undo](https://alistapart.com/article/neveruseawarning/)
