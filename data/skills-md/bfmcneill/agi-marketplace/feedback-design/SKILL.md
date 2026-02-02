---
name: feedback-design
description: Use when building loading states, progress indicators, success confirmations, or error messages. Covers feedback loops and patterns that feel satisfying.
---

# Feedback Design

Feedback is how software communicates with users. Good feedback creates anticipation, confirms actions, and guides recovery.

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

## Response Time Thresholds

**[Research][Expert]** Jakob Nielsen, based on Miller (1968), established response time limits in *Usability Engineering* (1993):

| Threshold | User Perception |
|-----------|-----------------|
| **0.1 sec** | Feels instantaneous — direct manipulation illusion |
| **1.0 sec** | Noticeable delay — user stays focused but notices wait |
| **10 sec** | Attention limit — user needs progress indicator or will leave |

These thresholds are based on human perceptual abilities and remain foundational in interaction design.

**Source:** [Nielsen Norman Group - Response Times](https://www.nngroup.com/articles/response-times-3-important-limits/)

---

## Progress Indicators

**[Research]** Dopamine research (Schultz, Sapolsky) shows the brain releases dopamine during *anticipation* of reward, not after. Progress indicators work because they create anticipation.

### Pattern: Progress Over Spinners

**Weak feedback:**
```
Loading...
```

**Strong feedback:**
```
Uploading photo 3 of 7...
████████░░░░░░░░ 47%
```

Progress creates anticipation. Spinners create uncertainty.

---

## Skeleton Screens

**[Research — Mixed Results]** Skeleton screen research shows inconsistent findings:

- Mejtoft et al. (2018) found skeleton screens scored higher on perceived speed
- Viget's study (136 participants) found skeleton screens **performed worse** than spinners — users took longer and evaluated wait time more negatively

**When skeletons may help:**
- Familiar interfaces where users know what to expect
- Very short wait times
- Slow, steady animation (not rapid motion)

**When spinners may be better:**
- Novel interfaces
- Longer wait times
- Users unfamiliar with the layout

**Source:** [Viget - A Bone to Pick with Skeleton Screens](https://www.viget.com/articles/a-bone-to-pick-with-skeleton-screens/)

---

## Immediate Acknowledgment

**[Expert]** Nielsen Norman and UX practitioners recommend immediate feedback for every user action:

| Timing | Feedback Type |
|--------|---------------|
| 0-100ms | Visual state change (button press, hover) |
| 100ms-1s | Loading indicator if not complete |
| 1-10s | Progress indicator with status |
| 10s+ | Explanation + option to cancel |

---

## Success Confirmation

**[Convention]** Acknowledge completion without over-celebrating.

**Patronizing:**
```
🎉 Great job! You did it! Your file was uploaded successfully!
```

**Respectful:**
```
File uploaded. 2.4 MB
```

Users need confirmation, not praise. Objective acknowledgment respects user intelligence.

---

## Error Messages

**[Expert]** Nielsen's Heuristic #9: "Help users recognize, diagnose, and recover from errors."

Error messages should answer three questions:
1. **What happened?**
2. **Why?**
3. **What can I do now?**

**Useless:**
```
Error: Something went wrong
```

**Actionable:**
```
Upload failed: File exceeds 10MB limit
[Compress image] [Choose different file]
```

**[Research]** Cognitive Load Theory (Sweller, 1988) supports this: vague error messages increase extraneous cognitive load, forcing users to diagnose problems instead of solving them.

**Source:** [Nielsen Norman - Error Message Guidelines](https://www.nngroup.com/articles/error-message-guidelines/)

---

## Optimistic UI

**[Convention]** Update UI immediately, reconcile with server afterward.

```javascript
// Optimistic: Update UI first
updateUI()         // Instant feedback
sendToServer()     // Background
handleFailure()    // Rollback if needed

// Pessimistic: Wait for server
await sendToServer()  // User waits
updateUI()
```

**Use when:**
- Success rate is very high (>99%)
- Action is reversible
- Failure can be gracefully handled

**Caution:** No formal research validates optimistic UI. It's practitioner convention based on perceived performance benefits.

---

## Sound and Haptic Feedback

**[Research]** Studies on haptic feedback show tactile sensations can increase engagement (Apple's Taptic Engine research). However, overuse causes habituation.

**[Convention]** Use sparingly:
- Completion of significant actions
- Destructive actions requiring attention
- Errors that need immediate notice

**Avoid for:**
- Every button tap
- Routine navigation
- Background updates

---

## Anti-Patterns With Research

### Carousels / Auto-Rotating Sliders

**Status:** Generally ineffective
**Evidence:** [Research] — Multiple studies with consistent findings

**What research shows:**

- **Notre Dame study:** 1% click-through rate; 84% of clicks on first slide only
- **Search Engine Land:** 0.65% CTR across B2B sites
- **Adobe test:** Removing slider entirely **increased sales 23%**
- **Eye tracking (NNg):** Users often skip carousels, perceiving them as ads ("banner blindness")

**Why they fail:**
- Auto-rotation moves content before users can read it
- Users don't trust rotating content (ad-like)
- Most users see only slide 1
- Creates "choice paralysis" — nothing feels primary

**If you must use a carousel:**
- Don't auto-rotate (or use 7+ second intervals)
- Pause on hover/interaction
- Replace dots with meaningful labels
- Make first slide count (84% of engagement)
- Consider if static content would work better

**Better alternatives:**
- Static hero with clear hierarchy
- Tabbed content (user-controlled)
- Scrolling content sections

**Sources:**
- [Orbit Media - Do Sliders Hurt Websites?](https://www.orbitmedia.com/blog/rotating-sliders-hurt-website/)
- [Smashing Magazine - Better Carousel UX](https://www.smashingmagazine.com/2022/04/designing-better-carousel-ux/)
- [Nielsen Norman - Effective Carousels](https://www.nngroup.com/articles/designing-effective-carousels/)

---

## Key Sources

- Nielsen, J. (1993). *Usability Engineering*. Academic Press.
- Miller, R.B. (1968). Response time in man-computer conversational transactions.
- Sweller, J. (1988). Cognitive load during problem solving.
- [Nielsen Norman Group - Response Times](https://www.nngroup.com/articles/response-times-3-important-limits/)
- [Mejtoft et al. (2018) - Skeleton Screens Study](https://dl.acm.org/doi/10.1145/3232078.3232086)
- [Viget - Skeleton Screens Research](https://www.viget.com/articles/a-bone-to-pick-with-skeleton-screens/)
