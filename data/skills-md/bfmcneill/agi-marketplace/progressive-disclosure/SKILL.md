---
name: progressive-disclosure
description: Use when designing interfaces with complex functionality, settings panels, or expert features. Covers layering information so beginners aren't overwhelmed and experts aren't held back.
---

# Progressive Disclosure

Show users what they need when they need it. Hide complexity until it's relevant. Let depth feel like discovery, not burden.

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

## Research Foundation

**[Research — Limited]** Carroll and Rosson (1987) developed the "training wheels" approach, hiding advanced functionality to help novices succeed. However, they noted that **empirical evidence for progressive disclosure effectiveness is limited**.

From Carroll & Rosson (1997): "No empirical evidence exists regarding the effectiveness of progressive disclosure."

**What we do know:**
- **[Research]** Miller's Law (1956): Working memory holds ~7±2 items (some modern research suggests ~4 chunks)
- **[Research]** Cognitive Load Theory (Sweller, 1988): Reducing extraneous load improves learning
- **[Expert]** Nielsen Norman Group recommends progressive disclosure for improving learnability, efficiency, and reducing errors

**Honest assessment:** Progressive disclosure is widely accepted as good practice, but rigorous controlled studies are sparse. Most evidence comes from case studies and practitioner experience.

**Source:** [Nielsen Norman - Progressive Disclosure](https://www.nngroup.com/articles/progressive-disclosure/)

---

## The Depth Hierarchy

**[Expert]** Structure complexity in layers:

```
┌─────────────────────────────────────┐
│  Layer 1: Essential (always shown)  │  ← What 80% of users need
├─────────────────────────────────────┤
│  Layer 2: Common (one click away)   │  ← Frequently used options
├─────────────────────────────────────┤
│  Layer 3: Advanced (discoverable)   │  ← Power user features
├─────────────────────────────────────┤
│  Layer 4: Expert (documented)       │  ← Edge cases, configs
└─────────────────────────────────────┘
```

Users should be able to operate entirely at Layer 1.

---

## Core Patterns

### disclosure-1: Default to Simplicity

**[Research]** Supported by cognitive load theory. Fewer visible options = less extraneous load.

**Overwhelming:**
```
┌─────────────────────────────────────┐
│ Name: [________]                    │
│ Email: [________]                   │
│ Phone: [________]                   │
│ Address: [________]                 │
│ [14 more fields...]                 │
└─────────────────────────────────────┘
```

**Progressive:**
```
┌─────────────────────────────────────┐
│ Name: [________]                    │
│ Email: [________]                   │
│                                     │
│ [+ Add more details]                │
└─────────────────────────────────────┘
```

Ask: "What's the minimum to accomplish the task?"

### disclosure-2: Experts Can Skip, Beginners Can't Be Lost

**[Convention]** Design for two paths through the same interface:

**Beginner path:**
```
Step 1 → Step 2 → Step 3 → Done
[Clear linear flow with help text]
```

**Expert path:**
```
[Jump directly to any step]
[Keyboard shortcuts]
[Collapse help text]
```

### disclosure-3: Expand In-Place

**[Convention]** When revealing more, don't teleport users to new screens.

**Disorienting:**
```
[Click "More options"]
[New page loads]
[Click back to return]
```

**Smooth:**
```
[Click "More options"]
[Section expands below]
[Click again to collapse]
```

Spatial memory matters. Users remember *where* things are.

---

## High-Impact Patterns

### disclosure-4: Smart Defaults Reduce Choices

**[Research]** Related to choice overload research. Iyengar & Lepper's jam study showed too many choices can paralyze decision-making (though effect size is debated in meta-analyses).

```
// No default — user must choose
Date format: [dropdown with 15 options]

// Smart default — user can change if needed
Date format: [MM/DD/YYYY ▼] (based on locale)
```

### disclosure-5: Contextual Revelation

**[Convention]** Show options when they become relevant, not before.

**Too early:**
```
[Shows "Export options" before user has created anything]
```

**Contextual:**
```
[User creates something]
[Export options appear]
```

### disclosure-6: Search as Escape Hatch

**[Convention]** For complex interfaces, search lets users skip the hierarchy.

```
[User knows what they want but not where]
[Presses ⌘K]
[Types "export pdf"]
[Jumps directly to feature]
```

Search is disclosure for experts.

---

## Case Study: GOV.UK Bank Holidays

**[Case Study]** The UK government's GOV.UK redesigned their bank holiday page based on user research:

**Before:** Busy page with all bank holidays, multiple regions, historical data
**After:** Single upcoming bank holiday prominently displayed, details below

User research revealed most people wanted one thing: the next bank holiday date.

**Source:** [GOV.UK Design System](https://design-system.service.gov.uk/)

---

## Patterns Reference

| Pattern | Use When | Evidence |
|---------|----------|----------|
| **Accordion** | Related sections, one open at a time | [Convention] |
| **Expandable rows** | Tables with detail views | [Convention] |
| **Tabs** | Parallel categories, similar importance | [Convention] |
| **Drawer/sidebar** | Secondary content needs space | [Convention] |
| **Modal** | Focused subtask, temporary context | [Expert] NNg |
| **Tooltip** | Brief explanation, no interaction | [Convention] |
| **Popover** | Small interactions | [Convention] |

---

## Myths & Debunked Patterns

### MYTH: The Three-Click Rule

**Status:** Debunked
**Origin:** Jeffrey Zeldman's *Taking Your Talent to the Web* (2001) — no data provided

**The claim:** Users will abandon tasks if they can't complete them in 3 clicks.

**What research shows:**

- **Joshua Porter (UIE, 2003):** Analyzed 44 users, 620 tasks, 8,000+ clicks. Found **no dropoff after 3 clicks** and no decrease in satisfaction.
- **Jakob Nielsen:** Found a site where moving products to 4 clicks from homepage **increased findability by 600%** over the 3-click version.

**Why it persists:** It's simple, memorable, and sounds logical. But click counting ignores cognitive factors like information scent, clarity of options, and confidence in progress.

**What actually matters:** Each click should make users feel closer to their goal. Strong information scent beats low click counts.

**Sources:**
- [Nielsen Norman - 3 Click Rule is False](https://www.nngroup.com/articles/3-click-rule/)
- [UX Myths - All Pages in 3 Clicks](https://uxmyths.com/post/654026581/myth-all-pages-should-be-accessible-in-3-clicks)

---

### NUANCE: Above the Fold

**Status:** Partially true, often overstated
**Origin:** Newspaper terminology, adapted to web in 1990s

**The claim:** Users won't scroll; everything important must be above the fold.

**What research shows:**

- **Eye tracking (NNg):** 57% of viewing time is above the fold (down from 80% in 2010)
- **The fold effect is real:** 102% more attention to 100px above fold vs 100px below
- **But people DO scroll:** Chartbeat found 66% of attention on media pages is below the fold. ClickTale found 76% of pages get scrolled.

**The nuance:** The fold matters for *initial* engagement, but it's not a hard boundary. Users scroll when:
- Content above signals value below
- There's no "false bottom" (design that looks like the page ends)
- Information scent is strong

**Guidance:** Put your most important content and value proposition above the fold, but don't cram everything there. Design to invite scrolling.

**Sources:**
- [Nielsen Norman - Scrolling and Attention](https://www.nngroup.com/articles/scrolling-and-attention/)
- [Nielsen Norman - The Fold Manifesto](https://www.nngroup.com/articles/page-fold-manifesto/)

---

## Key Sources

- Miller, G.A. (1956). The magical number seven, plus or minus two.
- Carroll, J.M. & Rosson, M.B. (1987). The paradox of the active user.
- Sweller, J. (1988). Cognitive load during problem solving.
- [Nielsen Norman - Progressive Disclosure](https://www.nngroup.com/articles/progressive-disclosure/)
- [Interaction Design Foundation - Progressive Disclosure](https://www.interaction-design.org/literature/topics/progressive-disclosure)
