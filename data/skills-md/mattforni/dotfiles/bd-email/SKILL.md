---
name: bd-email
description: Craft Business Development emails for RYLLC fractional CTO consultancy. Handles warm reconnects, job posting outreach, rejection follow-ups, VC intros, and custom BD scenarios. Uses established templates and project voice.
---

# BD Email Skill

**Purpose:** Draft professional, conversational Business Development emails for RYLLC fractional CTO consultancy outreach.

## Core Principles

1. **Tight and conversational** - Target ~130-150 words for initial outreach
2. **Complete sentences** - No sentence fragments, use subjects and verbs
3. **Single version only** - Don't draft multiple alternatives
4. **Natural voice** - Professional but warm, not overly formal
5. **Get to the point** - Lead with value, avoid long introductions
6. **No bragging** - Focus on experience, not metrics or accomplishments
7. **Service orientation** - What can you do for them
8. **Title Case for subject lines** - Always use Title Case for email subjects

## Email Flavors

### 1. Colleague Reconnect
**Use for:** Former colleagues, VCs, advisors, warm contacts
**Template:** templates/06-colleague-reconnect.md
**Key elements:**
- Personal reference to last interaction
- Brief "barbell CTO" positioning
- Ask for perspective/insights (low pressure)
- Scheduling link

### 2. Job Posting Cold Outreach
**Use for:** Found strong technical fit role, want to pitch fractional alternative
**Template:** templates/07-job-posting-cold-outreach.md
**Key elements:**
- Reference job posting with hyperlink
- Forward request to right person
- Brief credentials showing technical fit
- Specific interest in their tech/mission
- Fractional alternative pitch
- "Rather than (or alongside) a full-time hire" framing

### 3. Rejection Follow-Up
**Use for:** Received job rejection, want to turn into network connection
**Template:** templates/05-rejection-follow-up.md
**Key elements:**
- Thank them for consideration
- Express continued interest in company/mission
- Pivot from role to relationship
- Position fractional CTO services as alternative

### 4. Direct Introduction Request
**Use for:** Asking warm contact to intro you to specific company
**Key elements:**
- Acknowledge their offer/suggestion
- Brief positioning relevant to target company
- Specific ways you could add value
- Clear ask (make the intro)
- Offer to provide additional context

### 5. Custom BD Outreach
**Use for:** Unique situations not covered by templates
**Approach:** Follow core principles, adapt tone to relationship warmth

## The "Barbell CTO" Positioning

Standard explanation (adjust as needed):
> "I'm focused on fractional CTO work and reliability staff augmentation. On the CTO side, I'm doing the deep technical work like architecture and system design on one end, and high-level strategy like roadmap and team building on the other."

**Note:** Keep framing positive. Avoid negative language like "skipping all the middle management nonsense" or similar. Focus on what you DO provide, not what you avoid.

## Technical Credentials (Use Sparingly)

Standard positioning:
> "I spent six years as CTO and co-founder of Gremlin, pioneering chaos engineering."

For energy/climate context:
> "At Gremlin, we constantly wrestled with quantifying the impact of failures that didn't happen—exactly the kind of reliability challenge that's critical in [energy systems/climate infrastructure]."

## What to Avoid

- Sentence fragments or choppy writing
- Multiple alternative versions
- Bragging about metrics ($10M+ ARR, 100+ customers)
- Redundant paragraphs
- Multiple bullet lists in email body
- Alternative contact strategy sections
- Long explanations when brevity works

## Standard Components

**Scheduling link:** https://app.reclaim.ai/m/forni/chat
- Preferred phrasing: "You can grab some time here [link] if you like."
- Alternative: "You can find some time here: [link]"
- Always embed in conversational text, not standalone

**Signature:**
```
Matthew Fornaciari
```

**Warm closing (for reconnect emails):**
"Either way, cheers and hope things are going well."
- Use when you want to give warmth without pressure
- Shows genuine interest beyond just the business ask

**Forward request (for cold outreach):**
"If I'm reaching out to the wrong person, I'd appreciate you forwarding this along to whoever's leading this hire."

## Process

1. **Identify email flavor** - Which template/approach fits?
2. **Gather context** - Relationship history, company details, technical fit
   - **Email history analysis:** Use Gmail MCP to search and read past email threads with the contact
   - Look for: Last contact date, nature of relationship, how things ended, any commitments made, warm/cold signals
   - Key insights: Did they offer to stay in touch? Was there a previous engagement discussion? Any specific topics discussed?
3. **Enrich from LinkedIn** - Current role, company stage, recent activity, mutual connections
4. **Draft email** - Follow template structure, customize personal elements with specific details from email history
5. **Check length** - Target ~130-150 words
6. **Review tone** - Natural? Warm but professional? Service-oriented?
7. **Single version** - Don't create alternatives

## Example Usage

**Warm reconnect to former colleague:**
- Use template 06
- Add specific personal reference
- Brief barbell CTO explanation
- Low-pressure ask for perspective

**Cold outreach to job posting:**
- Use template 07
- Hyperlink to job posting
- Show technical fit understanding
- Pitch fractional alternative
- Include forward request

**Introduction request to warm contact:**
- Direct, conversational tone
- Brief positioning relevant to target
- Specific value-add examples
- Clear ask to make intro

## Resources

All templates available in:
- `/Users/forni/Craft/vocation/templates/`

Contact database:
- `/Users/forni/Craft/vocation/network/contacts.md`

Project guidelines:
- `/Users/forni/Craft/vocation/CLAUDE.md`

## Gmail Integration

For details on using Gmail MCP server to draft emails directly in Gmail, see `gmail-integration.md`.

**Quick start:** After Claude Code restart, use `draft_email` tool to create drafts directly in Gmail instead of copy/paste.
