---
name: gtm-skills
description: AI-powered B2B sales workflow. Research prospects, generate outreach, create content, handle objections, prep discovery calls. Use when asked to "research a company", "write a cold email", "handle an objection", or "prep for a call".
argument-hint: <action> [target]
---

# GTM Skills - AI-Powered Sales Workflow

Complete B2B sales toolkit. Research, outreach, content, objections—one command.

## Quick Start

```
/gtm-skills research Acme Corp
/gtm-skills email John Smith, VP Sales at Acme Corp
/gtm-skills objection "We don't have budget"
/gtm-skills discovery call with Head of Sales at a Series B startup
```

## Actions

When invoked, show this menu:

```
**GTM Skills**

What do you need?

1. Research - Company or person deep-dive
2. Outreach - Cold email, LinkedIn DM, follow-up
3. Content - LinkedIn post, Twitter thread
4. Objections - Handle any objection
5. Discovery - Prep questions for a call
6. Progress - Launch status and next steps

Or just describe what you need.
```

---

## 1. Research

### Company Research

```
Research [COMPANY] and provide:

1. COMPANY OVERVIEW
- What they do (one sentence)
- Business model
- Size (employees, funding)
- Key competitors

2. RECENT ACTIVITY (Last 90 days)
- Funding/financial news
- Product launches
- Executive hires
- Job posting trends

3. KEY CONTACTS
- CEO/Founder
- [Relevant title for your product]
- Likely decision maker

4. PAIN POINTS (Hypothesized)
- Based on stage and industry
- Based on recent activity
- Based on job postings

5. OUTREACH ANGLES
- 3 specific angles
- What signal to reference
- Why they'd care
```

### Person Research

```
Research [PERSON] at [COMPANY]:

1. BACKGROUND
- Current role and tenure
- Career path
- Education

2. ONLINE PRESENCE
- LinkedIn activity/posts
- Twitter presence
- Podcast appearances
- Published content

3. PROFESSIONAL INTERESTS
- Topics they post about
- Causes they support
- Communities they're in

4. CONNECTION POINTS
- Mutual connections
- Shared experiences
- Conversation starters
```

---

## 2. Outreach

### Cold Email

Ask for: Person, Company, Signal (funding, hiring, etc.), Tone

```
Write a cold email to [PERSON], [TITLE] at [COMPANY].

Context:
- They [SIGNAL]
- I sell [YOUR PRODUCT]
- We help [TARGET] with [PROBLEM]
- Desired outcome: [BOOK MEETING/GET REPLY]

Tone: [Direct/Consultative/Casual/Formal/Founder/Challenger]

Rules:
- Under 75 words
- Reference something specific about them
- Clear ask at the end
- Subject line under 5 words
```

### LinkedIn DM

```
Write a LinkedIn connection request + follow-up DM to [PERSON] at [COMPANY].

Context:
- They [SIGNAL/REASON FOR REACHING OUT]
- I help [TYPE OF COMPANY] with [PROBLEM]

Connection request (under 300 chars):
[Generate personalized request]

Follow-up DM (if they accept):
[Generate value-first message]
```

### Follow-Up Email

```
Write a follow-up to [PERSON] at [COMPANY].

Previous touchpoint: [COLD EMAIL/CALL/MEETING]
Days since: [NUMBER]
Goal: [BOOK MEETING/RE-ENGAGE]

Type: [Bump/Value-add/Breakup]

Rules:
- Don't guilt them
- Give reason to respond NOW
- One clear ask
```

---

## 3. Content

### LinkedIn Post

```
Write a LinkedIn post about [TOPIC].

Goal: [Build authority/Share lesson/Start conversation/Subtle promotion]
Tone: [Contrarian/Story-driven/Educational/Vulnerable]

Structure:
- Hook (stops the scroll)
- Body (3-5 short paragraphs)
- Insight or lesson
- Call to engage

Rules:
- No hashtags in body (3-5 at end)
- Under 200 words
- Write like you talk
```

### Twitter Thread

```
Write a Twitter thread about [TOPIC].

Format:
- Tweet 1: Hook + promise
- Tweets 2-8: One idea per tweet, use → for lists
- Final tweet: Summary + CTA

Rules:
- Each tweet under 280 chars
- No hashtags except final tweet
- Controversial or counterintuitive angle
```

---

## 4. Objections

```
Handle this objection:

"[EXACT OBJECTION]"

Context:
- I sell: [YOUR PRODUCT]
- Stage: [COLD CALL/DISCOVERY/DEMO/NEGOTIATION]

Give me:

1. WHAT THEY'RE REALLY SAYING
- Underlying concern
- Fear or priority driving it

2. CLARIFYING QUESTIONS
- 3 questions to understand better

3. RESPONSE OPTIONS
- Option A: Acknowledge and Reframe
- Option B: Use Social Proof
- Option C: Reversing Question

4. PREVENTION
- How to prevent this earlier
```

---

## 5. Discovery

```
Generate discovery questions for [PERSONA] at [COMPANY TYPE].

I sell: [YOUR PRODUCT]
Problems I solve: [LIST 2-3]
Call type: [FIRST CALL/DEEP DISCOVERY/DEMO FOLLOW-UP]

Generate 15 questions:

SITUATION (4 questions)
- Current process, tools, team

PROBLEM (4 questions)
- Challenges, frustrations, bottlenecks

IMPLICATION (4 questions)
- Consequences, costs, ripple effects

NEED-PAYOFF (3 questions)
- Ideal outcomes, what success looks like

Rules:
- Conversational, not interrogation
- Include follow-up prompts
- Avoid yes/no questions
```

---

## Installation

### Claude Code

```bash
cp -r gtm-skills ~/.claude/commands/
```

Or copy SKILL.md contents to `~/.claude/commands/gtm-skills.md`

### Claude.ai

Add this file to Project Knowledge, or paste into a conversation.

---

## Output Format

Always provide:
1. The generated content (email, post, questions, etc.)
2. Why this approach works
3. One alternative angle to try
4. Suggested next action

Keep outputs practical and immediately usable.
