---
name: person-dossier
displayName: Person Dossier
description: "Build and update person dossiers from communication history. Use when a person is discussed for strategy, follow-up, opportunities, relationship context, or decisions. Automatically pull evidence from Front email, Granola meetings, memory recall, and event logs; then write/update a structured dossier in Vault/Resources/."
version: 1.0.0
author: Joel Hooks
tags: [joelclaw, people, dossiers, memory, relationships]
---

# Person Dossier

Build or refresh a dossier whenever an individual is discussed.

## Trigger

Run this workflow when a person is mentioned in:

- strategy or planning conversations
- follow-up decisions
- relationship context questions
- opportunity/deal/property discussions

## Output Path

- `Vault/Resources/<Person Name> - Dossier.md`

## Required Sections

1. All Email Threads
2. Key Topics Discussed
3. Projects Mentioned
4. Properties or Deals Referenced
5. Timeline of Interactions
6. Current Status of Open Items

## Workflow

### 1. Validate runtime and auth

```bash
secrets status
secrets lease front_api_token --ttl 15m
```

If secrets service is down:

```bash
secrets serve &
```

### 2. Resolve identifiers

Collect:

- primary name
- known email(s)
- aliases/handles

Use these as query inputs for all sources.

### 3. Pull Front threads (primary)

```bash
joelclaw email inbox -q "<person name>" -n 200
joelclaw email inbox -q "from:<email-or-handle>" -n 200
```

Read each matching conversation:

```bash
joelclaw email read --id <cnv_id>
```

### 4. Pull Granola meetings

List meetings in a practical window:

```bash
granola meetings --range this_week
granola meetings --range this_month
```

For each candidate meeting ID:

```bash
granola meeting <meeting_id>
granola meeting <meeting_id> --transcript
```

### 5. Pull memory context

```bash
joelclaw recall "<person name> <company> <project>" --limit 20 --min-score 0.25
joelclaw recall "<person email or alias>" --limit 20
```

### 6. Pull event timeline context

```bash
joelclaw events --hours 720 --count 200
joelclaw events --prefix meeting --hours 720 --count 200
```

### 7. Normalize extracted data

Populate these buckets from evidence:

- email threads: subject, conversation id, participants, last activity date
- topics: recurring discussion themes
- projects: named initiatives
- properties/deals: assets, opportunities, transactions
- timeline: dated interaction entries by channel
- open items: owner, status, due date, next step

### 8. Create or update dossier markdown

If file does not exist: create from template.

If file exists: update in-place.

Update rules:

- append new timeline entries without removing older ones
- dedupe by stable key (`channel + source_id + date + summary`)
- merge open item status updates instead of creating duplicates
- keep `Verified` and `Inferred` labels on each material claim
- refresh `Last Updated` timestamp

### 9. Record evidence and confidence

Each section must indicate provenance:

- `Verified from Front thread`
- `Verified from Granola meeting`
- `Inferred from memory/event context`

Never present inferred content as verified.

### 10. Blocker handling

If blocked:

1. record exact technical error text
2. attempt one fallback source (`joelclaw events` or `joelclaw recall`)
3. produce a blocked dossier with explicit gaps
4. include exact next-run commands

No silent partials.

## Dossier Template

```markdown
# <Person Name> - Dossier

## Identity
- Name: <name>
- Emails: <email1>, <email2>
- Aliases: <alias1>, <alias2>
- Last Updated: YYYY-MM-DD

## 1. All Email Threads with <Person Name>
- Thread: <subject>
  - Conversation ID: <cnv_id>
  - Last activity: YYYY-MM-DD
  - Evidence: Verified from Front thread

## 2. Key Topics Discussed
- <topic> (Verified/Inferred)

## 3. Projects Mentioned
- <project> (Verified/Inferred)

## 4. Properties or Deals Referenced
- <item> (Verified/Inferred)

## 5. Timeline of Interactions
- YYYY-MM-DD | <channel> | <summary> | <source_id>

## 6. Current Status of Open Items
- Item: <description>
  - Owner: system owner | other person | unknown
  - Status: open | blocked | closed
  - Next step: <text>
  - Due: YYYY-MM-DD | unknown
  - Evidence: <source>

## Evidence Index
- Front conversation IDs: <list>
- Granola meeting IDs: <list>
- Memory queries: <list>
- Event windows: <list>

## Blockers
- <none or error text>
```

## Quick Build Command Set

```bash
# 1) Front discovery
joelclaw email inbox -q "<person name>" -n 200

# 2) Front thread read
joelclaw email read --id <cnv_id>

# 3) Granola context
granola meetings --range this_month
granola meeting <meeting_id> --transcript

# 4) Memory context
joelclaw recall "<person name>" --limit 20

# 5) Event timeline
joelclaw events --prefix meeting --hours 720 --count 200
```

## Quality Bar

- No fabricated facts
- Open items always include owner
- Timeline uses concrete dates whenever available
- Verified and inferred content clearly separated
