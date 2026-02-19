---
name: optimize-agent-prompt
description: Craft agent personality and behavior for Sanity Agent Context. Load when tuning tone, verbosity, interactivity, guardrails, or response style. Covers system prompt structure and the two-surface architecture (instructions field vs system prompt).
---

# Optimize Your Agent's Prompt

Use this skill to craft your agent's personality and behavior. This covers tone, verbosity, interactivity, guardrails, and how to structure your system prompt — the things that make your agent feel like a helpful team member rather than a database interface.

## Prerequisites

- **A working agent** — built using the `create-agent-with-sanity-context` skill or equivalent
- **An Agent Context Document** — created in Sanity Studio with the context plugin

Optionally (but recommended):

- **Run the Agent Context Explorer** to generate `exploration-results.md` — this documents your dataset's schema, working query patterns, and limitations

```bash
npm install -g @sanity/agent-context-explorer

agent-context-explorer \
  --mcp-url https://api.sanity.io/vX/agent-context/PROJECT_ID/DATASET/SLUG \
  --questions ./questions.json \
  --sanity-token $SANITY_API_READ_TOKEN \
  --anthropic-api-key $ANTHROPIC_API_KEY
```

The CLI will tell you where the output is written. Paste the contents of `exploration-results.md` into your Agent Context Document's `instructions` field.

## How to Use This Skill

When helping a user optimize their agent's prompt:

1. **Ask about their agent's purpose** — What does it help users do? Who are the users?
2. **Walk through relevant questions** from the "Questions to Consider" section — don't ask all of them, pick what matters for their use case
3. **Draft a system prompt** using the structure in "System Prompt Structure" — start with Role Statement, add sections as needed
4. **Review against Core Principles** — ensure the prompt doesn't expose technical details or duplicate dataset knowledge
5. **Iterate** — refine based on user feedback

The output is a system prompt the user can paste into their agent's code. Keep it concise — a good system prompt is usually 10-30 lines.

## Two Prompt Surfaces

When using Agent Context, you have two places to put instructions:

| Surface                                           | What goes here                                                                             | How it gets to the agent                  |
| ------------------------------------------------- | ------------------------------------------------------------------------------------------ | ----------------------------------------- |
| **Agent Context Document → `instructions` field** | Dataset-specific knowledge: schema reference, query patterns, limitations, field gotchas   | Injected automatically via the MCP server |
| **Your agent's system prompt**                    | Agent personality: role, tone, verbosity, response format, guardrails, forbidden behaviors | You control this in your code             |

**The key distinction:**

- **Instructions field** = what the agent knows about the data
- **System prompt** = how the agent behaves and communicates

Don't duplicate dataset knowledge in your system prompt — that's what the instructions field is for. Your system prompt should focus on personality, style, and rules.

### Quick Reference

| This concern...                                  | Goes in instructions field | Goes in system prompt |
| ------------------------------------------------ | -------------------------- | --------------------- |
| Schema reference (document types, fields)        | ✅                         | ❌                    |
| Query patterns that work                         | ✅                         | ❌                    |
| Field naming gotchas                             | ✅                         | ❌                    |
| Data limitations (null fields, external systems) | ✅                         | ❌                    |
| Agent role and persona                           | ❌                         | ✅                    |
| Tone of voice                                    | ❌                         | ✅                    |
| Response length and format                       | ❌                         | ✅                    |
| "Never mention competitors"                      | ❌                         | ✅                    |
| "Pricing not in dataset, check website"          | ✅                         | ❌                    |
| "Always direct pricing questions to website"     | ❌                         | ✅                    |

## Questions to Consider

Think through these as you design your agent's personality. Not all will apply to every agent — pick what's relevant.

### Role & Purpose

**What is your agent's job?**
A shopping assistant helps users find and compare products. A support agent troubleshoots issues. A product expert answers detailed technical questions. A concierge guides users through complex decisions. The role shapes everything else — tone, proactivity, depth of answers.

**What should it proactively offer?**
Some agents wait to be asked. Others suggest related products, offer to compare options, or ask if the user needs anything else. More proactive agents feel more helpful but risk being pushy. Consider: should your agent suggest, or just answer?

**What's the scope?**
An agent that does one thing well feels more competent than one that tries to do everything. Define what's in scope (product questions, troubleshooting) and what's out (account issues, returns, complaints). Clear scope helps the agent give confident answers within its domain and graceful redirects outside it.

### Tone & Voice

**How formal or casual?**
A luxury brand might want polished, professional language. A lifestyle brand might want relaxed, conversational tone. Match your brand voice — the agent should sound like it belongs on your team.

**Warm and friendly, or efficient and direct?**
Friendly agents build rapport ("Great question! Let me help you with that..."). Direct agents respect the user's time ("It comes in black and white."). Neither is better — it depends on your brand and use case.

**First person ("I") or brand voice ("We at [Company]")?**
First person feels more personal and conversational. Brand voice feels more official. Some agents mix both — "I'd recommend..." for suggestions, "We offer..." for policies.

**What personality traits?**
Is your agent enthusiastic? Calm? Authoritative? Playful? A few personality traits, consistently applied, make the agent feel like a character rather than a tool.

### Response Style

**How verbose?**
Chat-length responses (1-2 sentences) feel snappy and conversational. Paragraph-length responses provide more context but can overwhelm. Consider: are users on mobile? Skimming quickly? Or reading carefully?

**Use formatting (lists, headers) or plain prose?**
Lists and headers help users scan long responses. Plain prose feels more natural for short answers. A good rule: short answers in prose, longer answers with structure.

**Emojis or no?**
Emojis add warmth and personality but don't fit every brand. If you use them, be consistent — occasional emojis feel random, regular ones feel intentional.

**How should it handle comparisons?**
Tables? Side-by-side bullets? Narrative explanation? The format affects readability. Pick one approach and be consistent.

### Interactivity

**Should it ask clarifying questions?**
"Are you looking for a portable speaker or a home setup?" helps narrow down options but adds a round-trip. Some users prefer to be guided; others want direct answers. Consider offering both: answer if you can, ask if you need to.

**Should it suggest related things?**
"This pairs well with a carrying case" is helpful upselling or annoying noise, depending on context. Consider: when is proactive suggestion welcome vs intrusive?

**Conversational or transactional?**
Conversational agents remember context and build on previous messages. Transactional agents treat each message independently. Most chat agents should be conversational, but the degree varies.

### Boundaries

**What should it never discuss?**
Competitor products? Pricing details? Medical or legal advice? Internal processes? Be explicit — agents need clear boundaries to avoid awkward situations.

**What should it redirect to humans?**
Complaints? Complex returns? Account issues? Anything requiring authentication? Define the handoff points and how the agent should phrase the redirect.

**What topics require extra care?**
Safety-related questions? Warranty claims? Anything where a wrong answer has consequences? The agent should be more conservative in these areas — better to redirect than guess.

## System Prompt Structure

A system prompt can include these sections. Not all are required — include what's relevant for your agent.

### Role Statement

Who the agent is. Keep it to 2-3 sentences.

```
You are a shopping assistant for [Company]. You help customers find products,
compare options, and answer questions about features and compatibility.
You're friendly, knowledgeable, and concise.
```

### Response Style

How to format and deliver answers.

```
## How to Respond
- Give direct answers first, then add detail if helpful
- Keep responses concise — a few sentences for simple questions
- Use bullet points for comparisons or lists of features
- Don't narrate your process ("Let me look that up...")
```

### Boundaries

What's out of scope — and where to direct users instead.

```
## What You Can't Help With
- Pricing — direct users to the website
- Order status or account issues — direct to customer support at support@company.com
- Warranty claims — direct to the warranty page
```

### Guardrails

Things the agent should never do.

```
## Never
- Never mention competitor products by name
- Never make up information — if you don't know, say so
- Never share internal processes or system details
- Never promise discounts or special treatment
```

### Internal Rules

Technical rules the agent follows but doesn't mention to users. These supplement what's in the instructions field — use sparingly.

```
## Internal Rules (never mention to users)
- If multiple products match, ask the user to clarify rather than guessing
- For discontinued products, acknowledge they exist but direct to current alternatives
```

## Core Principles

### Speak On Behalf Of, Not About

The agent represents the brand. It should talk like a knowledgeable team member, not like a database administrator. Users don't care about document types, query patterns, or data sources — they want answers.

**Bad** (talking about the dataset):

> "The pricing data is not available in this dataset. It is managed in an external Commerce API system."

**Good** (talking on behalf of the brand):

> "I don't have current pricing available. You can check pricing on our website or contact our sales team."

**Bad** (exposing internals):

> "I queried the product type and found the X1 Speaker. Based on the media altText fields, it appears to come in black and white."

**Good** (clean answer):

> "The X1 Speaker comes in black and white."

### Handle Gaps Gracefully

When the agent doesn't have information, it should:

1. Acknowledge simply — "I don't have that information"
2. Redirect helpfully — "You can find pricing on our website"
3. Offer alternatives — "I can help you compare features if that's useful"

Never guess. Never make up answers. Never blame the data.

### Keep Technical Details Internal

The agent needs to know about document types, field names, and query patterns to find answers. But users should never see this machinery. Phrases like "the document type," "this field is null," or "the query returned no results" should never appear in responses.

## What NOT to Do

- **Don't duplicate dataset knowledge in your system prompt.** That's what the instructions field is for. Your system prompt handles personality and behavior.

- **Don't let the agent talk like a database.** No "document types," "fields," "queries," or "data sources" in user-facing responses.

- **Don't use "Context MCP" in customer-facing prompts.** The product name is "Agent Context."

- **Don't skip the exploration step.** Running `agent-context-explorer` reveals gotchas you won't discover until production. The 10 minutes it takes saves hours of debugging.

- **Don't be vague about boundaries.** "Don't discuss sensitive topics" is less useful than "Never discuss competitor products, pricing negotiations, or return exceptions."
