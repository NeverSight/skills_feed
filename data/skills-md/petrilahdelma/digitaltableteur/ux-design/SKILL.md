---
name: ux-design
description: Expert UX design guidance for user research, information architecture, user flows, wireframing, usability testing, and design system UX patterns. Use when planning user experiences, conducting user research, creating user journeys, optimizing conversion funnels, improving accessibility, or designing intuitive interfaces. Includes heuristic evaluation and cognitive load optimization.
---

# UX Design Expert

## Core UX Principles

When designing user experiences, always follow these principles:

1. **User-Centered Design**: Start with user needs, not business requirements
2. **Cognitive Load Minimization**: Reduce mental effort required to complete tasks
3. **Consistency**: Maintain predictable patterns across the experience
4. **Feedback & Feedforward**: Show system status and next steps clearly
5. **Error Prevention**: Design to prevent errors before they occur
6. **Accessibility First**: WCAG 2.1 AA minimum, aim for AAA

---

## UX Research Methods

### 1. User Interviews (Discovery)

**When to use**: Understanding user motivations, pain points, mental models

**Process**:
1. Define research questions (3-5 core questions)
2. Recruit participants (5-8 users per segment)
3. Prepare interview guide (open-ended questions)
4. Conduct 30-45 min sessions
5. Synthesize findings into themes

**Interview Script Template**:
```
Opening (5 min):
- Introduce yourself and research goals
- Explain confidentiality and recording
- Ask for permission to record

Background (10 min):
- Tell me about your role...
- How do you currently solve [problem]?
- Walk me through your last experience with [task]...

Deep Dive (20 min):
- What frustrates you most about [current solution]?
- If you could change one thing, what would it be?
- How do you decide when to [key decision]?

Closing (5 min):
- Is there anything I should have asked but didn't?
- Can you recommend others I should speak with?
```

**Output**: Affinity map of user needs, pain points, and opportunities

---

### 2. Usability Testing

**When to use**: Validating designs, identifying friction points

**Process**:
1. Define tasks (3-5 critical user flows)
2. Create prototype (low-fi for early testing, high-fi for refinement)
3. Recruit 5 participants per round
4. Conduct moderated sessions (30-45 min)
5. Measure: task success rate, time on task, error rate, satisfaction

**Task Script Template**:
```
Scenario: You need to [realistic goal]. Using this prototype, show me how you would do that.

Observation Notes:
- Where do they hesitate?
- What do they click first?
- Do they use search or navigation?
- What error messages do they encounter?
- Do they complete the task successfully?

Follow-up Questions:
- On a scale of 1-5, how difficult was that?
- What was confusing?
- What would you change?
```

**Nielsen's Severity Rating**:
- **0**: Not a usability problem
- **1**: Cosmetic (fix if time)
- **2**: Minor (low priority)
- **3**: Major (high priority)
- **4**: Catastrophic (fix before launch)

---

### 3. Heuristic Evaluation (Jakob Nielsen's 10 Heuristics)

Use this checklist to audit any interface:

1. **Visibility of System Status**: Does the system keep users informed?
   - Loading indicators, progress bars, confirmation messages
   - ✅ Example: "Saving..." → "Saved!" feedback

2. **Match Between System and Real World**: Does it use familiar language?
   - Avoid jargon, use user vocabulary
   - ✅ Example: "Archive" not "Deprecate"

3. **User Control and Freedom**: Can users undo mistakes?
   - Undo/redo, cancel buttons, back navigation
   - ✅ Example: "Are you sure?" confirmation for destructive actions

4. **Consistency and Standards**: Do similar things look/behave the same?
   - Consistent button placement, color meanings, terminology
   - ✅ Example: Primary action always on right, danger always red

5. **Error Prevention**: Does it prevent errors before they happen?
   - Constraints (disable invalid options), confirmation dialogs
   - ✅ Example: Disable "Submit" until required fields are filled

6. **Recognition Rather Than Recall**: Is information visible, not hidden?
   - Show recent items, autocomplete, tooltips
   - ✅ Example: Show recently used colors in color picker

7. **Flexibility and Efficiency**: Are there shortcuts for experts?
   - Keyboard shortcuts, batch actions, customization
   - ✅ Example: Cmd+K for search, drag-to-select multiple

8. **Aesthetic and Minimalist Design**: Is every element necessary?
   - Remove decorative elements, prioritize content
   - ✅ Example: Hide advanced options behind "Advanced" toggle

9. **Help Users Recognize, Diagnose, and Recover from Errors**: Are errors helpful?
   - Plain language, suggest solutions, show where error occurred
   - ✅ Example: "Email format invalid. Try: name@example.com"

10. **Help and Documentation**: Is help contextual and searchable?
    - Tooltips, inline help, search-optimized docs
    - ✅ Example: "What's this?" icon next to complex fields

---

## Information Architecture

### Card Sorting (for Navigation)

**Purpose**: Understand how users mentally group content

**Process**:
1. Create cards for each content item (30-50 cards)
2. Ask users to group cards into categories that make sense
3. Ask users to name each category
4. Analyze groupings to find patterns

**Output**: Sitemap with user-validated categories

### Site Map Template

```
Homepage
├── About
│   ├── Team
│   ├── Mission
│   └── Contact
├── Services
│   ├── Design System Lift-Off
│   ├── AI Brand Ops
│   └── AI UX Sprint
├── Work (Portfolio)
│   ├── Case Study 1
│   ├── Case Study 2
│   └── All Projects
└── Blog
    ├── Articles
    └── Authors
```

---

## User Flows & Journey Mapping

### User Flow Diagram

**Purpose**: Visualize how users move through a task

**Example: Contact Form Submission**

```
[User lands on Contact page]
        ↓
[Reads page content]
        ↓
[Fills form fields] → [Validation error?] → [Fix errors]
        ↓                                          ↓
[Clicks Submit] ←───────────────────────────────────┘
        ↓
[Loading state]
        ↓
[Success confirmation] → [Receives email]
        ↓
[CTA: Browse services]
```

**Flow Analysis Checklist**:
- [ ] Is the happy path clear?
- [ ] Are error states handled gracefully?
- [ ] Can users exit at any point?
- [ ] Is there a clear next action after completion?

---

### Journey Map Template

**For**: [User Persona Name]
**Scenario**: [Specific goal or task]

| Stage | User Action | Thoughts | Emotions | Pain Points | Opportunities |
|-------|-------------|----------|----------|-------------|---------------|
| **Awareness** | Googles "design system consultancy" | "Need help scaling our design..." | Hopeful but overwhelmed | Too many options | Clear positioning: "DS Lift-Off in 4 weeks" |
| **Consideration** | Visits homepage, reads case studies | "Do they understand my problem?" | Skeptical | Vague outcomes | Show metrics: "50% faster onboarding" |
| **Decision** | Checks pricing, reads testimonials | "Can I afford this?" | Anxious | No transparent pricing | Price ranges + ROI calculator |
| **Onboarding** | Books consultation, fills form | "What happens next?" | Uncertain | No confirmation email | Auto-reply + calendar invite |
| **Experience** | Receives deliverables | "This is exactly what I needed!" | Relieved | - | Upsell: Care retainer |

---

## Wireframing Guidelines

### Low-Fidelity Wireframes (Sketches)

**When**: Early exploration, rapid iteration

**Tools**: Paper, whiteboard, Figma low-fi kit

**Focus**:
- Layout structure
- Content hierarchy
- Navigation patterns
- Interaction zones

**Example: Service Page Wireframe**

```
┌─────────────────────────────────────┐
│  Logo    Nav1  Nav2  Nav3  [CTA]   │  ← Header
├─────────────────────────────────────┤
│                                     │
│   ┌─────────────────────────────┐  │
│   │  [ Hero Image ]             │  │  ← Hero
│   │  DESIGN SYSTEM LIFT-OFF     │  │
│   │  Get production-ready DS    │  │
│   │  in 4 weeks                 │  │
│   │  [Book Consultation]        │  │
│   └─────────────────────────────┘  │
│                                     │
│   ┌───────────┬───────────┬──────┐ │
│   │ Week 1    │ Week 2    │Week 3│ │  ← Process
│   │ Discovery │ Build     │Launch│ │
│   └───────────┴───────────┴──────┘ │
│                                     │
│   DELIVERABLES:                     │  ← Details
│   - Token system                    │
│   - 20+ components                  │
│   - Documentation                   │
│                                     │
│   PRICING: €18-25k                  │
│   [Get Started]                     │
│                                     │
│   ┌─────────┐ ┌─────────┐          │  ← Testimonials
│   │ Quote 1 │ │ Quote 2 │          │
│   └─────────┘ └─────────┘          │
└─────────────────────────────────────┘
```

### High-Fidelity Wireframes

**When**: Pre-development handoff

**Include**:
- Real content (not lorem ipsum)
- Actual component names from design system
- Interaction states (hover, active, disabled)
- Responsive breakpoints (mobile, tablet, desktop)
- Annotations for developers

---

## Conversion Optimization

### Landing Page Anatomy (CRO Best Practices)

```
Above the Fold:
├── Unique Value Prop (10 words max)
├── Subheadline (explain who it's for)
├── Hero Image/Video (show product in context)
└── Primary CTA (action-oriented: "Start Your Lift-Off")

Social Proof:
├── Client logos (6-8 recognizable brands)
├── Testimonial with photo + name + company
└── Metric (e.g., "500+ components shipped")

Benefits (Not Features):
├── Benefit 1: "Launch faster" (not "Component library")
├── Benefit 2: "Scale your team" (not "Documentation")
└── Each with icon + short description

How It Works:
├── Step 1 → Step 2 → Step 3 (visual timeline)
└── Keep it to 3-4 steps max

Objection Handling:
├── FAQ (address top 5 objections)
└── Risk reversal ("If we don't hit KPIs, 2 weeks free")

Final CTA:
├── Repeat primary CTA
└── Low-friction secondary ("Download case study")
```

---

## Accessibility UX Patterns

### Keyboard Navigation

**Tab Order**:
1. Skip to main content link (first tab)
2. Navigation menu
3. Main content (logical reading order)
4. Footer

**Shortcuts**:
- `Tab` / `Shift+Tab`: Navigate forward/back
- `Enter` / `Space`: Activate buttons/links
- `Esc`: Close modals/menus
- `Arrow keys`: Navigate within components (tabs, dropdowns)

### Screen Reader Optimization

**Landmarks**:
```html
<header>...</header>        <!-- Banner -->
<nav aria-label="Main">...</nav>
<main>...</main>
<aside>...</aside>          <!-- Complementary -->
<footer>...</footer>        <!-- Contentinfo -->
```

**ARIA Labels**:
```html
<!-- For icons without text -->
<button aria-label="Close dialog">
  <svg>...</svg>
</button>

<!-- For complex widgets -->
<div role="tablist" aria-label="Service options">
  <button role="tab" aria-selected="true">Lift-Off</button>
  <button role="tab" aria-selected="false">Brand Ops</button>
</div>
```

---

## Mobile-First UX

### Progressive Disclosure

**Pattern**: Show essentials first, reveal details on demand

**Example: Service Card**

**Mobile (320px)**:
```
┌─────────────────┐
│ DS Lift-Off     │
│ 4 weeks         │
│ €18-25k         │
│ [Learn More]    │
└─────────────────┘
```

**Desktop (1024px)**:
```
┌─────────────────────────────────────────────┐
│ Design System Lift-Off               €18-25k│
│ Get a production-ready design system in 4   │
│ weeks. Includes tokens, components, docs.   │
│                                             │
│ ✓ Token system    ✓ Documentation          │
│ ✓ 20+ components  ✓ Training sessions      │
│                                             │
│ [Book Consultation] [Download Case Study]  │
└─────────────────────────────────────────────┘
```

### Touch Target Sizes

- Minimum: 44×44px (iOS), 48×48px (Material Design)
- Spacing: 8px between targets minimum
- Hit area > visual size (padding increases tap zone)

```css
.button {
  padding: 12px 24px; /* Visual size */

  /* Extend hit area with pseudo-element */
  position: relative;
}

.button::before {
  content: '';
  position: absolute;
  inset: -8px; /* 8px hit area extension */
}
```

---

## Cognitive Load Optimization

### Miller's Law: 7±2 Items

**Problem**: Long lists overwhelm users

**Solution**: Chunk information into 5-7 groups

**Bad Example** (12 navigation items):
```
Home | About | Team | Mission | Services | Pricing | Work | Case Studies | Blog | Authors | Contact | FAQ
```

**Good Example** (5 groups):
```
About (Team, Mission)
Services (Pricing, Offerings)
Work (Portfolio, Case Studies)
Insights (Blog, Authors)
Contact
```

### Hick's Law: Choice Overload

**Problem**: More options = slower decisions

**Solution**: Reduce choices, guide users

**Example: Service Selection**

**Bad** (overwhelming):
- Design System Audit ($X)
- Token Architecture ($Y)
- Component Library ($Z)
- Documentation ($A)
- Training ($B)
- Governance ($C)
- Maintenance ($D)

**Good** (packaged):
- **Lift-Off** (Audit + Tokens + Library) - €18-25k
- **Brand Ops** (Templates + Governance) - €12-18k
- **AI Sprint** (Prototype + Evaluation) - €9-14k

---

## Micro-Interactions

### Feedback Patterns

**States to design for**:
1. **Idle**: Default state
2. **Hover**: Cursor over element (desktop only)
3. **Focus**: Keyboard navigation
4. **Active**: Click/tap in progress
5. **Loading**: Async operation
6. **Success**: Operation complete
7. **Error**: Operation failed
8. **Disabled**: Unavailable

**Button Example**:
```
Idle:     [Submit]              (blue background)
Hover:    [Submit]              (darker blue, slight scale)
Focus:    [Submit]              (outline visible)
Active:   [Submit]              (pressed effect)
Loading:  [○ Submitting...]    (spinner + text)
Success:  [✓ Submitted]        (green, checkmark)
Error:    [✕ Try Again]        (red, error icon)
Disabled: [Submit]              (gray, cursor not-allowed)
```

---

## Form UX Best Practices

### Input Field Design

```
Label:
- Always visible (not placeholder)
- Above input (not inline)
- Clear language ("Email address" not "Email")

Input:
- Large enough for touch (48px height min)
- Correct input type (email, tel, number)
- Autocomplete enabled
- Clear error state (red border + icon)

Help Text:
- Below input (not in placeholder)
- Show before user interacts
- Example: "We'll never share your email"

Error Message:
- Specific ("Email missing @" not "Invalid")
- Show immediately after blur
- Suggest fix ("Try: name@example.com")

Success State:
- Green checkmark when valid
- Optional: "Looks good!" message
```

### Multi-Step Forms

**Progress Indicator**:
```
Step 1: Contact Info  →  Step 2: Details  →  Step 3: Review
  [●]                      [○]                  [○]
```

**Best Practices**:
- Show progress (step X of Y)
- Allow back navigation (no data loss)
- Save drafts automatically
- Show error summary at top
- Validate per-step, not only on submit

---

## Design System UX Patterns

### Component Discovery

**Problem**: Designers/developers can't find the right component

**Solution**: Multi-faceted navigation in Storybook

1. **By Category**: Layout, Forms, Feedback, Data Display
2. **By Use Case**: "I need to show a loading state" → Spinner
3. **By Search**: Fuzzy search across component names and tags
4. **By Status**: Production, Beta, Deprecated, WIP

### Component Documentation Template

```markdown
# Button

## When to use
Use buttons for primary actions like submitting forms or confirming decisions.

## When NOT to use
Don't use buttons for navigation—use links instead.

## Variants
- **Primary**: Main action on page (one per screen)
- **Secondary**: Alternative actions
- **Danger**: Destructive actions (delete, remove)

## Accessibility
- Always include visible text (not icon-only)
- Loading state announces to screen readers
- Disabled buttons explain why ("Save unavailable: form incomplete")

## Examples
[Storybook playground with live code]
```

---

## Metrics & KPIs

### UX Metrics Framework

| Metric | What | How to Measure |
|--------|------|----------------|
| **Task Success Rate** | % of users who complete task | Usability testing |
| **Time on Task** | How long to complete | Analytics + testing |
| **Error Rate** | % of actions that result in error | Error tracking |
| **Satisfaction (SUS)** | Subjective usability score | Post-task survey |
| **Net Promoter Score** | Would recommend? | Email survey |
| **Bounce Rate** | % who leave immediately | Google Analytics |
| **Conversion Rate** | % who complete goal | Analytics funnel |

### System Usability Scale (SUS) Survey

**Post-task questionnaire** (1 = Strongly Disagree, 5 = Strongly Agree):

1. I think I would like to use this system frequently
2. I found the system unnecessarily complex
3. I thought the system was easy to use
4. I think I would need support to use this system
5. I found the various functions well integrated
6. I thought there was too much inconsistency
7. I would imagine most people would learn quickly
8. I found the system very cumbersome to use
9. I felt very confident using the system
10. I needed to learn a lot before I could get going

**Score**: (Sum odd items - 5) + (25 - sum even items) × 2.5
**Benchmark**: 68+ is above average

---

## When to Use This Skill

Activate this skill when:
- Planning user research studies
- Creating user personas or journey maps
- Designing user flows or wireframes
- Conducting usability tests
- Performing heuristic evaluations
- Optimizing conversion funnels
- Improving form UX
- Designing accessible experiences
- Reducing cognitive load
- Measuring UX success metrics
- Auditing information architecture
- Creating mobile-first experiences

**Remember**: Always validate designs with real users before development.
