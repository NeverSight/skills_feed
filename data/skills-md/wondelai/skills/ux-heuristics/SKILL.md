---
name: ux-heuristics
description: 'Usability heuristics and principles based on Steve Krug''s "Don''t Make Me Think" and Jakob Nielsen''s 10 heuristics. Use when you need to: (1) audit a UI for usability problems, (2) identify why users are confused or frustrated, (3) simplify navigation and information architecture, (4) conduct heuristic evaluations, (5) prioritize UX fixes by severity, (6) review designs before development, (7) improve form usability, (8) validate that interfaces follow established UX principles.'
---

# UX Heuristics Framework

Practical usability principles for evaluating and improving user interfaces. Based on a fundamental truth: users don't read, they scan. They don't make optimal choices, they satisfice. They don't figure out how things work, they muddle through.

## Core Philosophy

**"Don't Make Me Think"** - Every page should be self-evident. If something requires thinking, it's a usability problem.

## Scoring

**Goal: 10/10.** When reviewing or creating user interfaces, rate them 0-10 based on adherence to the principles below. A 10/10 means full alignment with all guidelines; lower scores indicate gaps to address. Always provide the current score and specific improvements needed to reach 10/10.

## Krug's Three Laws of Usability

### 1. Don't Make Me Think

Every question mark that pops into a user's head adds to their cognitive load and distracts from the task.

**Things that make users think:**
- Clever names vs. clear names
- Marketing-speak vs. plain language
- Unfamiliar categories or labels
- Links that could go anywhere
- Buttons with ambiguous labels

**Self-evident vs. self-explanatory:**

| Self-evident | Self-explanatory |
|--------------|------------------|
| "Get directions" | "Calculate route to destination" |
| "Sign in" | "Access your account portal" |
| "Add to cart" | "Proceed to purchase selection" |

**Goal:** Self-evident. If that's impossible, self-explanatory.

### 2. It Doesn't Matter How Many Clicks

The myth: "Users will leave if it takes more than 3 clicks."

**Reality:** Users don't mind clicks if each click is:
- Painless (fast, easy)
- Obvious (no thinking required)
- Confidence-building (they know they're on the right path)

**Three mindless clicks > one confusing click**

### 3. Get Rid of Half the Words, Then Half of What's Left

**Benefits of brevity:**
- Reduces noise
- Makes useful content more prominent
- Makes pages shorter (less scrolling)
- Shows respect for user's time

**What to cut:**
- Happy-talk ("Welcome to our website!")
- Instructions that nobody reads
- "Please" and "Kindly" and polite fluff
- Redundant explanations

---

## The Trunk Test

A test for navigation clarity: can users answer these questions on any page?

| Question | User Should Know |
|----------|------------------|
| What site is this? | Brand/logo visible |
| What page am I on? | Page title/heading clear |
| What are the major sections? | Navigation visible |
| What are my options at this level? | Links/buttons clear |
| Where am I in the scheme of things? | Breadcrumbs/hierarchy |
| How can I search? | Search box findable |

**If users can't answer these instantly, navigation needs work.**

---

## Nielsen's 10 Usability Heuristics

See: [references/nielsen-heuristics.md](references/nielsen-heuristics.md) for detailed explanations with examples.

### Quick Reference

| # | Heuristic | One-liner |
|---|-----------|-----------|
| 1 | Visibility of system status | Always show what's happening |
| 2 | Match between system and real world | Use user's language, not yours |
| 3 | User control and freedom | Easy undo and exit |
| 4 | Consistency and standards | Same words, same actions |
| 5 | Error prevention | Better than error messages |
| 6 | Recognition rather than recall | Show options, don't require memory |
| 7 | Flexibility and efficiency | Shortcuts for experts |
| 8 | Aesthetic and minimalist design | Remove everything unnecessary |
| 9 | Help users recognize, diagnose, recover from errors | Plain-language errors with solutions |
| 10 | Help and documentation | Searchable, task-focused, concise |

### Heuristic Conflicts

Heuristics sometimes contradict each other. When they do:
- **Simplicity vs. Flexibility**: Use progressive disclosure
- **Consistency vs. Context**: Consistent patterns, contextual prominence
- **Efficiency vs. Error Prevention**: Prefer undo over confirmation dialogs
- **Discoverability vs. Minimalism**: Primary actions visible, secondary hidden

See [heuristic-conflicts.md](references/heuristic-conflicts.md) for resolution frameworks.

### Dark Patterns Recognition

Dark patterns violate heuristics deliberately to manipulate users:
- Forced continuity (hard to cancel)
- Roach motel (easy in, hard out)
- Confirmshaming (guilt-based options)
- Hidden costs (surprise fees at checkout)

See [dark-patterns.md](references/dark-patterns.md) for complete taxonomy and ethical alternatives.

---

## Severity Rating Scale

When auditing interfaces, rate each issue:

| Severity | Rating | Description | Priority |
|----------|--------|-------------|----------|
| **0** | Not a problem | Disagreement, not usability issue | Ignore |
| **1** | Cosmetic | Minor annoyance, low impact | Fix if time |
| **2** | Minor | Causes delay or frustration | Schedule fix |
| **3** | Major | Significant task failure | Fix soon |
| **4** | Catastrophic | Prevents task completion | Fix immediately |

### Rating Factors

Consider all three:

1. **Frequency:** How often does it occur?
2. **Impact:** How severe when it occurs?
3. **Persistence:** One-time or ongoing problem?

---

## Common Usability Violations

See: [references/krug-principles.md](references/krug-principles.md) for full Krug methodology.

### Navigation

| Violation | Problem | Fix |
|-----------|---------|-----|
| Mystery meat navigation | Icons without labels | Add text labels |
| Too many choices | Decision paralysis | Reduce to 7±2 items |
| Inconsistent nav location | Users can't find it | Fixed position always |
| No "you are here" indicator | Lost users | Highlight current section |
| Broken back button | Frustration | Never break browser history |

### Forms

| Violation | Problem | Fix |
|-----------|---------|-----|
| No inline validation | Submit → error → scroll | Validate on blur |
| Unclear required fields | Confusion | Mark optional, not required |
| Poor error messages | "Invalid input" | Explain what's wrong + how to fix |
| Too many fields | Abandonment | Remove unnecessary fields |
| Unexpected format requirements | Frustration | Accept all formats, normalize |

### Content

| Violation | Problem | Fix |
|-----------|---------|-----|
| Wall of text | Nobody reads | Break up, add headings |
| Jargon | Confusion | Plain language |
| Missing labels | Ambiguity | Label all inputs and sections |
| Low contrast text | Unreadable | WCAG AA minimum (4.5:1) |
| Important info below fold | Missed | Move up or add anchor |

### Interactions

| Violation | Problem | Fix |
|-----------|---------|-----|
| No loading indicators | "Is it broken?" | Show progress/spinner |
| No confirmation on delete | Accidental loss | Confirm destructive actions |
| Tiny tap targets | Mobile frustration | Minimum 44×44 px |
| Hover-only info | Mobile users miss it | Don't hide critical info |
| No undo | Fear of acting | Provide undo for all actions |

---

## Quick Audit Checklist

See: [references/audit-template.md](references/audit-template.md) for full structured template.

### 5-Minute Scan

| Check | Pass? |
|-------|-------|
| Can I tell what site/page this is immediately? | [ ] |
| Is the main action obvious? | [ ] |
| Is the navigation clear? | [ ] |
| Can I find the search? | [ ] |
| Are there any dead ends? | [ ] |
| Does anything make me think "huh?" | [ ] |

### 15-Minute Audit

Run through Nielsen's 10 heuristics, rating each 0-4.

### User Observation (Gold Standard)

Watch 3-5 users attempt key tasks:
- Where do they hesitate?
- Where do they click wrong?
- What do they say out loud?
- Where do they give up?

---

## When to Use Each Method

| Method | When | Time | Findings |
|--------|------|------|----------|
| Heuristic evaluation | Before user testing | 1-2 hours | Major violations |
| User testing | After heuristic fixes | 2-4 hours | Real behavior |
| A/B testing | When optimizing | Days-weeks | Statistical validation |
| Analytics review | Ongoing | 30 min | Patterns and problems |

---

## Common Excuses (And Reality)

| Excuse | Reality |
|--------|---------|
| "Users will figure it out" | They won't. They'll leave. |
| "We need to show everything" | Prioritize. Hide complexity. |
| "It tested well with the team" | Team knows too much. Test with real users. |
| "Adding help text will fix it" | Nobody reads help text. Simplify the UI. |
| "Power users need all these options" | 95% of users never need them. Progressive disclosure. |
| "It's industry standard" | Bad standards are still bad. |

---

## Reference Files

- [krug-principles.md](references/krug-principles.md): Full Krug methodology, scanning behavior, navigation clarity
- [nielsen-heuristics.md](references/nielsen-heuristics.md): Detailed heuristic explanations with examples
- [audit-template.md](references/audit-template.md): Structured heuristic evaluation template
- [dark-patterns.md](references/dark-patterns.md): Categories, examples, ethical alternatives, regulations
- [wcag-checklist.md](references/wcag-checklist.md): Complete WCAG 2.1 AA checklist, testing tools
- [cultural-ux.md](references/cultural-ux.md): RTL, color meanings, form conventions, localization
- [heuristic-conflicts.md](references/heuristic-conflicts.md): When heuristics contradict, resolution frameworks

## Further Reading

This skill is based on usability principles developed by Steve Krug and Jakob Nielsen:

- [*"Don't Make Me Think, Revisited"*](https://www.amazon.com/Dont-Make-Think-Revisited-Usability/dp/0321965515?tag=wondelai00-20) by Steve Krug
- [*"10 Usability Heuristics for User Interface Design"*](https://www.nngroup.com/articles/ten-usability-heuristics/) by Jakob Nielsen (Nielsen Norman Group)
