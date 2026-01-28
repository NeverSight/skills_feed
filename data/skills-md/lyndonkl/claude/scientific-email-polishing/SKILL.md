---
name: scientific-email-polishing
description: Use when writing or polishing professional scientific emails, journal cover letters, or responses to reviewers. Invoke when user mentions email to collaborator, cover letter to editor, reviewer response, professional correspondence, or needs help with professional tone, clear asks, or diplomatic communication in academic/scientific contexts.
---

# Scientific Email Polishing

## Table of Contents
- [Purpose](#purpose)
- [When to Use](#when-to-use)
- [Core Principles](#core-principles)
- [Workflow](#workflow)
- [Email Types](#email-types)
- [Tone Guidelines](#tone-guidelines)
- [Guardrails](#guardrails)
- [Quick Reference](#quick-reference)

## Purpose

This skill helps compose and polish professional scientific correspondence including emails to collaborators, cover letters to journal editors, and responses to peer reviewers. It ensures clear communication, appropriate tone, explicit asks, and professional formatting for academic contexts.

## When to Use

Use this skill when:

- **Professional emails**: To collaborators, department heads, funding officers
- **Journal cover letters**: Submitting manuscripts to journals
- **Response to reviewers**: Addressing peer review comments
- **Editor correspondence**: Queries, appeals, resubmission letters
- **Cold outreach**: Potential collaborators, speakers, advisors
- **Administrative emails**: To program officers, committee members

Trigger phrases: "write an email", "cover letter to journal", "response to reviewers", "email to collaborator", "professional email", "polish this email"

**Do NOT use for:**
- Recommendation letters (use `academic-letter-architect`)
- Research statements (use `career-document-architect`)
- Grant proposals (use `grant-proposal-assistant`)

## Core Principles

**1. One email, one purpose**: Each email should have a clear, single objective

**2. Explicit asks**: State exactly what you need from the recipient and by when

**3. Context first**: Open with enough context for the reader to understand immediately

**4. Professional but warm**: Formal doesn't mean cold; collegial is appropriate

**5. Scannable format**: Busy recipients skim; use structure to aid quick reading

## Workflow

Copy this checklist and track your progress:

```
Email Polishing Progress:
- [ ] Step 1: Identify purpose and desired outcome
- [ ] Step 2: Draft subject line (clear, specific)
- [ ] Step 3: Write opening (context in first sentence)
- [ ] Step 4: Compose body (organized, scannable)
- [ ] Step 5: State explicit ask (what, by when)
- [ ] Step 6: Close professionally (next steps, sign-off)
- [ ] Step 7: Review tone (polite, appropriate)
```

**Step 1: Identify Purpose and Outcome**

What action do you want the recipient to take? What decision do you need? By when? If you can't state this clearly, the email isn't ready to send.

**Step 2: Draft Subject Line**

Subject should preview content and signal urgency/type. Be specific: "Meeting request: Collaboration on X project" not "Quick question". See [resources/template.md](resources/template.md#subject-lines) for examples.

**Step 3: Write Opening**

First sentence should establish context. Who are you (if unknown), why are you writing, what's this about? No need for extensive pleasantries. See [resources/template.md](resources/template.md#openings) for openers.

**Step 4: Compose Body**

Organize information logically. Use short paragraphs. Consider bullets for multiple points. Bold key information if needed. Keep under 3-4 paragraphs for most emails.

**Step 5: State Explicit Ask**

Be clear about what you need. Include timeline if relevant. Make it easy to say yes. Don't bury the ask.

**Step 6: Close Professionally**

Thank them, indicate next steps, offer to provide more info. Use appropriate sign-off for relationship level. See [resources/template.md](resources/template.md#closings) for sign-offs.

**Step 7: Review Tone**

Read aloud. Is it polite but efficient? Not too casual, not too stiff? Appropriate for your relationship with recipient? Validate using [resources/evaluators/rubric_email.json](resources/evaluators/rubric_email.json).

## Email Types

### Journal Cover Letter

**Purpose:** Introduce manuscript, explain significance, suggest reviewers

**Structure:**
```
Subject: Submission: [Manuscript Title] - [Type: Original Research/Review/etc.]

Dear Dr. [Editor] / Dear Editors,

[PARAGRAPH 1: What and why]
Please find attached our manuscript entitled "[Title]" for consideration
as a [Article Type] in [Journal Name]. This work [brief significance statement].

[PARAGRAPH 2: What's new]
Our study [key finding/contribution]. This advances the field by [impact].
We believe this work will interest readers of [Journal] because [fit with
journal scope].

[PARAGRAPH 3: Practicalities]
The manuscript is [X] words with [Y] figures. All authors have approved
the submission and there are no conflicts of interest to declare. This
work has not been published elsewhere and is not under consideration
at another journal.

[OPTIONAL: Reviewer suggestions]
We suggest the following potential reviewers: [Names with institutions
and emails].

[CLOSING]
Thank you for your consideration. We look forward to hearing from you.

Sincerely,
[Corresponding Author]
```

### Response to Reviewers

**Purpose:** Address each point thoroughly and professionally

**Structure:**
```
Subject: Revised Manuscript [ID]: [Title]

Dear Dr. [Editor],

Thank you for the opportunity to revise our manuscript "[Title]". We
appreciate the thoughtful comments from the reviewers, which have
significantly improved our work. Below we provide point-by-point
responses to each comment. Reviewer comments are in italics, our
responses in plain text, and changes to the manuscript are noted.

---

REVIEWER 1

*Comment 1: [Quote reviewer comment]*

Response: [Your response]. We have [action taken]. This change appears
on page X, lines Y-Z.

*Comment 2: [Quote reviewer comment]*

Response: [Your response].

[Continue for all comments]

---

REVIEWER 2
[Same format]

---

We hope these revisions address the reviewers' concerns and that the
manuscript is now suitable for publication in [Journal]. Please do not
hesitate to contact us if additional revisions are needed.

Sincerely,
[Corresponding Author]
```

### Collaboration Request

**Purpose:** Propose collaboration with new contact

**Structure:**
```
Subject: Collaboration opportunity: [Brief topic description]

Dear Dr. [Name],

I am [Your Name], a [position] at [Institution], working on [research area].
I am reaching out because [why them specifically - be genuine and specific].

[Brief background on your work and why collaboration makes sense]

I would be interested in [specific collaboration proposal]. This could involve
[what you're proposing - be concrete].

Would you be available for a brief call to discuss? I'm flexible on timing
and happy to work around your schedule.

Thank you for considering this. [Optional: note any mutual connection]

Best regards,
[Your Name]
```

## Tone Guidelines

### Formality Spectrum

| Recipient | Tone | Example Sign-off |
|-----------|------|-----------------|
| Unknown editor/senior | Formal | "Sincerely," "Respectfully," |
| Known colleague (distant) | Professional-warm | "Best regards," "Best," |
| Known colleague (close) | Warm-professional | "Best," "Thanks," |
| Close collaborator | Friendly-professional | "Thanks," "Cheers," |

### Professional but Not Stiff

**Too stiff:**
> "I am writing to inquire as to whether you might be available to provide guidance regarding..."

**Too casual:**
> "Hey! Quick q - you free to chat about that thing?"

**Just right:**
> "I'm reaching out to see if you'd have time to discuss [topic]. Would a brief call work for you next week?"

### Diplomatic Language

**When declining:**
- "Unfortunately, I won't be able to..."
- "While I appreciate the opportunity, my current commitments prevent..."
- "I'd recommend reaching out to [alternative] who might be better positioned..."

**When disagreeing (reviewer response):**
- "We respectfully disagree with this interpretation because..."
- "While we understand the reviewer's concern, our data suggests..."
- "We have added clarification to address this point, though we maintain that..."

**When following up:**
- "I wanted to follow up on my previous email..."
- "I'm circling back on [topic]..."
- "Apologies for the additional email, but I wanted to check..."

## Guardrails

**Critical requirements:**

1. **Clear purpose**: Every email needs an identifiable goal
2. **Explicit asks**: Don't make recipients guess what you need
3. **Professional tone**: Appropriate for academic/scientific context
4. **Proofread**: Errors undermine credibility
5. **Appropriate length**: Respect recipients' time
6. **Complete information**: Include everything needed to respond

**Common pitfalls:**
- ❌ **Buried ask**: Request hidden in paragraph 4
- ❌ **No deadline**: "When you get a chance" = never
- ❌ **Wall of text**: Long unbroken paragraphs
- ❌ **Too casual**: "Hey" to journal editor
- ❌ **Too formal**: Stilted language to close colleague
- ❌ **Missing context**: Assuming they remember previous exchange
- ❌ **Multiple topics**: Should be separate emails

## Quick Reference

**Key resources:**
- **[resources/template.md](resources/template.md)**: Subject lines, openings, closings, full templates
- **[resources/evaluators/rubric_email.json](resources/evaluators/rubric_email.json)**: Quality scoring

**Subject line formulas:**
- Request: "Meeting request: [Topic]"
- Follow-up: "Follow-up: [Original topic]"
- Submission: "Submission: [Title]"
- Response: "RE: [Topic] - [Your action]"
- Question: "Question about [Specific topic]"

**Time estimates:**
- Quick email: 5-10 minutes
- Cover letter: 15-30 minutes
- Response to reviewers: 1-4 hours (depending on revisions)

**Before sending checklist:**
- [ ] Purpose clear?
- [ ] Ask explicit?
- [ ] Context provided?
- [ ] Tone appropriate?
- [ ] Proofread?
- [ ] Attachments attached?

**Inputs required:**
- Purpose/desired outcome
- Recipient relationship
- Key information to convey
- Any constraints (deadline, politics)

**Outputs produced:**
- Polished email draft
- (Optional) Commentary on tone/structure
