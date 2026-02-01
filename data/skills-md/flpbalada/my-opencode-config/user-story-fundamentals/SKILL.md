---
name: user-story-fundamentals
description:
  Capture requirements from user perspective with structured user stories. Use
  when writing backlog items, defining acceptance criteria, prioritizing
  features, or communicating requirements between product and development.
---

# User Story Fundamentals - Capturing User-Centered Requirements

A structured framework for capturing product requirements from the user's
perspective. User stories help teams understand who needs a feature, what they
want to accomplish, and why it matters.

## When to Use This Skill

- Writing backlog items
- Defining feature requirements
- Prioritizing development work
- Communicating with development teams
- Breaking down epics into actionable work
- Ensuring user focus in product decisions

## User Story Format

```
THE STANDARD TEMPLATE

"As a [type of user],
 I want [some goal],
 so that [some reason/benefit]."

Components:
┌─────────────────────────────────────────────────────┐
│  WHO: The user persona or role                      │
│  WHAT: The desired functionality or goal            │
│  WHY: The business value or user benefit            │
└─────────────────────────────────────────────────────┘

This format shifts focus from WRITING about requirements
to TALKING about them, with users at the center.
```

## Core Components

### WHO - User Persona

```
Specificity Spectrum:

Generic (avoid):
├── "As a user..."
└── "As a customer..."

Better:
├── "As a first-time visitor..."
├── "As a returning customer..."
├── "As an admin user..."
└── "As a mobile user..."

Best (with job context):
├── "As a marketing manager who needs weekly reports..."
├── "As a parent shopping for school supplies..."
├── "As a developer debugging production issues..."
└── "As a sales rep preparing for a client meeting..."
```

### WHAT - Desired Functionality

```
Focus on GOALS, not IMPLEMENTATION:

❌ "I want a blue button in the header"
   (prescriptive, limits solutions)

✓ "I want to quickly access my saved items"
   (goal-focused, enables creativity)

❌ "I want a REST API endpoint"
   (technical implementation)

✓ "I want to integrate my data with external tools"
   (user goal, flexible implementation)
```

### WHY - Business Value

```
The "So That" Connection:

This part explains:
├── What pain it solves
├── What value it creates
├── Why this matters to the user
└── How it connects to business goals

Without "so that":
"As a user, I want to filter search results"
→ Why? What's the actual need?

With "so that":
"As a user, I want to filter search results
 so that I can find relevant items faster
 when browsing large catalogs"
→ Clear value, enables better solutions
```

## INVEST Criteria

```
QUALITY CHECKLIST FOR USER STORIES

I - Independent
│   Can be developed and delivered separately
│   No tight coupling to other stories
│
N - Negotiable
│   Details open to discussion
│   Not a rigid contract
│
V - Valuable
│   Delivers real value to user or business
│   Not just technical tasks
│
E - Estimable
│   Team can estimate effort
│   Clear enough to size
│
S - Small
│   Fits within single sprint
│   If too big, split it
│
T - Testable
│   Has clear acceptance criteria
│   Can verify when complete
```

## Acceptance Criteria

### Definition

```
ACCEPTANCE CRITERIA (AC)

Purpose: Define what makes the story "done"
Format: Specific, testable conditions

Example Story:
"As a user, I want to reset my password via email
 so that I can regain access if I forget it"

Acceptance Criteria:
□ User can request reset from login page
□ Email sent within 60 seconds of request
□ Reset link expires after 24 hours
□ Link works only once
□ Password must meet security requirements
□ User receives confirmation after successful reset
```

### Writing Good AC

| Characteristic  | Example                                      |
| --------------- | -------------------------------------------- |
| Specific        | "Within 60 seconds" not "quickly"            |
| Testable        | "Email contains reset link" - can verify     |
| Outcome-focused | "User can access account" not "system sends" |
| Complete        | Covers happy path AND edge cases             |

## Prioritization Framework

### RICE Scoring

```
RICE = (Reach × Impact × Confidence) / Effort

Reach: How many users affected per time period?
       (100 users/month, 1000 users/quarter)

Impact: How much will it move the needle?
        3 = Massive, 2 = High, 1 = Medium, 0.5 = Low, 0.25 = Minimal

Confidence: How sure are we about estimates?
            100% = High, 80% = Medium, 50% = Low

Effort: Person-months of work
        (0.5, 1, 2, 3...)

Higher RICE score = Higher priority
```

### MoSCoW Method

```
CATEGORIZATION FOR RELEASE PLANNING

MUST Have (Non-negotiable)
├── Critical for release
├── Legal/compliance requirements
└── Core value proposition

SHOULD Have (Important)
├── High value but not critical
├── Workarounds exist
└── Strong user demand

COULD Have (Nice to have)
├── Desired but not necessary
├── Easy wins if time permits
└── Lower user impact

WON'T Have (Not this time)
├── Explicitly out of scope
├── Future consideration
└── Documented for later
```

## Story Splitting Techniques

### When to Split

```
SPLIT IF:
├── Can't complete in one sprint
├── Story points > 13 (or team max)
├── Multiple distinct user values
├── Contains "and" connecting features
└── Too many acceptance criteria
```

### Splitting Methods

```
1. BY WORKFLOW STEPS
   Original: "User can complete purchase"
   Split:
   ├── User can add items to cart
   ├── User can enter shipping info
   ├── User can enter payment info
   └── User can confirm and place order

2. BY USER TYPE
   Original: "User can view dashboard"
   Split:
   ├── Admin can view full dashboard
   ├── Manager can view team metrics
   └── User can view personal stats

3. BY OPERATIONS (CRUD)
   Original: "User can manage contacts"
   Split:
   ├── User can create contact
   ├── User can view contact details
   ├── User can edit contact
   └── User can delete contact

4. BY DATA VARIATIONS
   Original: "User can import data"
   Split:
   ├── User can import CSV files
   ├── User can import Excel files
   └── User can import from API

5. BY ACCEPTANCE CRITERIA
   Original: "User can search products"
   Split:
   ├── User can basic keyword search
   ├── User can filter by category
   ├── User can sort results
   └── User can save search
```

## Definition of Done vs. Acceptance Criteria

```
DEFINITION OF DONE (DoD)        ACCEPTANCE CRITERIA (AC)
────────────────────────        ────────────────────────
Universal checklist             Story-specific conditions
Same for all stories            Unique per story
Quality standard                Functional requirements

DoD Examples:                   AC Examples:
□ Code reviewed                 □ User can X
□ Tests written                 □ System does Y
□ Documentation updated         □ Data validates as Z
□ No critical bugs              □ Performance meets N
```

## Story Template

```markdown
## User Story

**ID:** [PROJ-123] **Title:** [Brief descriptive title]

### Story

As a [specific user type], I want [goal/desire], so that [benefit/value].

### Acceptance Criteria

- [ ] [Specific, testable condition 1]
- [ ] [Specific, testable condition 2]
- [ ] [Specific, testable condition 3]

### Notes

- [Additional context]
- [Technical considerations]
- [Dependencies]

### Attachments

- [Link to designs]
- [Link to research]

### Estimation

- **Story Points:** [X]
- **Priority:** [High/Medium/Low]
- **Sprint:** [Sprint N]
```

## Real-World Examples

### E-commerce

```
Story: Password-less Login

As a returning customer,
I want to login using a magic link sent to my email,
so that I can access my account without remembering passwords.

Acceptance Criteria:
□ User enters email on login page
□ "Send magic link" option available
□ Email received within 30 seconds
□ Link valid for 15 minutes
□ One-click login from email
□ User lands on their dashboard after login
□ Link cannot be reused after login
```

### SaaS Product

```
Story: Team Invitation

As an account admin,
I want to invite team members via email,
so that I can onboard my team without manual account creation.

Acceptance Criteria:
□ Admin can enter multiple email addresses
□ Invitation email clearly explains next steps
□ Invited user can set their own password
□ Admin can see pending invitations
□ Admin can revoke pending invitations
□ Duplicate email addresses are prevented
□ Admin can set role during invitation
```

## Common Mistakes

```
ANTI-PATTERNS TO AVOID

❌ Implementation as story
   "Create database table for users"
   → Not user value, technical task

❌ Missing "so that"
   "As a user, I want to search"
   → Why? What problem does this solve?

❌ Too vague
   "As a user, I want a better experience"
   → What specifically? Not actionable

❌ Too large
   "As a user, I want full account management"
   → Multiple features, needs splitting

❌ Solution prescribed
   "As a user, I want a dropdown menu"
   → Describes UI, not user goal
```

## Integration with Other Methods

| Method               | Combined Use                      |
| -------------------- | --------------------------------- |
| **Theme-Epic-Story** | Stories fit within epic hierarchy |
| **Jobs to Be Done**  | Stories address user jobs         |
| **Five Whys**        | Find root cause behind story need |
| **Hypothesis Tree**  | Stories as hypotheses to test     |
| **Kanban**           | Stories flow through board stages |

## Quick Reference

```
STORY WRITING CHECKLIST

Format:
□ Follows "As a... I want... so that..." format
□ User type is specific and meaningful
□ Goal is user-focused, not technical
□ Benefit clearly stated

Quality (INVEST):
□ Independent - can be built alone
□ Negotiable - details discussable
□ Valuable - delivers real value
□ Estimable - team can size it
□ Small - fits in single sprint
□ Testable - has clear AC

Acceptance Criteria:
□ Specific and measurable
□ Testable (can verify pass/fail)
□ Covers main scenarios
□ Includes edge cases
□ Outcome-focused
```

## Resources

- [User Stories Applied - Mike Cohn](https://www.mountaingoatsoftware.com/books/user-stories-applied)
- [User Story Mapping - Jeff Patton](https://www.jpattonassociates.com/user-story-mapping/)
- [Writing Effective User Stories - Scrum Alliance](https://www.scrumalliance.org/)
