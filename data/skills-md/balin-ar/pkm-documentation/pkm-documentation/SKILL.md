---
name: pkm-documentation
description: Personal Knowledge Management documentation system based on Zettelkasten principles. Use when documenting conversations, decisions, development work, learnings, or any knowledge that should persist. Triggers on new projects, technical decisions, completed tasks, lessons learned, meeting notes, or when the user says "document this". Apply this workflow to all daily memory notes and long-term memory updates.
---

## 🚀 First Run

If the `knowledge/` directory doesn't exist in your workspace, run the setup script:

```bash
bash skills/pkm-documentation/scripts/setup.sh
```

This creates the vault structure and patches `AGENTS.md`, `SOUL.md`, and `MEMORY.md` with PKM instructions. Alternatively, create the directories manually: `knowledge/{decisions,devlog,learnings,projects,conversations,daily}`.

---

# PKM Documentation

Document everything worth keeping using atomic, connected, iterative notes. Based on Zettelkasten method adapted for an AI agent workspace.

## ⚠️ THIS IS MANDATORY

Read this file BEFORE writing any note. No exceptions.
- NO loose free text
- NO writing without a template
- NO documenting outside the `knowledge/` vault
- If there's no template for it, don't write it

## Core Principles

1. **Atomic notes** — One idea per file. If it covers two topics, split into two files.
2. **Connect everything** — Use `[[wiki-links]]` Obsidian-style for cross-references.
3. **Never delete, iterate** — Update notes with new context. Mark outdated info as `[SUPERSEDED]` rather than removing.
4. **Process fast** — Document while context is fresh. Delayed notes lose value (encoding principle).
5. **Standardize** — Every note follows a template. Every note is a file in its folder.

## Vault Structure

```
knowledge/
├── decisions/      → Decision Records (🔀)
├── devlog/         → Development Logs (🔧)
├── learnings/      → Learning Notes (💡)
├── projects/       → Project Notes (📦) — no date, updated in-place
├── conversations/  → Conversation Summaries (💬)
├── daily/          → Daily indices (links to the day's notes)
└── README.md       → Vault map
```

## File Naming

- **With date:** `YYYY-MM-DD-descriptive-slug.md` (decisions, devlog, learnings, conversations)
- **Without date:** `project-name.md` (projects — updated in-place)
- **Daily index:** `YYYY-MM-DD.md` (only links to the day's notes)

## Note Types & Templates

### 1. Decision Record (decisions/)
Use when a technical or strategic decision is made.

```markdown
## 🔀 Decision: [title]
- **Date:** YYYY-MM-DD
- **Context:** Why this came up
- **Options considered:** What alternatives existed
- **Decision:** What we chose
- **Reasoning:** Why
- **Consequences:** What this affects
- **Related:** [[type/file]] | [[type/file]]
```

### 2. Development Log (devlog/)
Use when building, fixing, or shipping something.

```markdown
## 🔧 Dev: [what was built/fixed]
- **Date:** YYYY-MM-DD
- **Project:** [[projects/name]]
- **What changed:** Brief description
- **Technical details:** Implementation notes worth remembering
- **Issues hit:** Problems encountered and how they were solved
- **Related:** [[type/file]] | [[type/file]]
```

### 3. Learning Note (learnings/)
Use when discovering something new — a tool, technique, pattern.

```markdown
## 💡 Learning: [topic]
- **Date:** YYYY-MM-DD
- **Source:** Where this came from (tweet, docs, experiment)
- **Key insight:** The core takeaway in 1-2 sentences
- **Details:** Deeper explanation if needed
- **Application:** How this applies to our work
- **Related:** [[type/file]] | [[type/file]]
```

### 4. Project Note (projects/)
Use when starting or significantly updating a project.

```markdown
## 📦 Project: [name]
- **Status:** active | paused | completed | abandoned
- **Goal:** What this project achieves
- **Stack:** Technologies used
- **Architecture:** Key design decisions
- **Current state:** Where things stand
- **Next steps:** What comes next
- **Related:** [[type/file]] | [[type/file]]
```

### 5. Conversation Summary (conversations/)
Use at end of significant conversations with the user.

```markdown
## 💬 Conversation: [topic]
- **Date:** YYYY-MM-DD
- **Topics covered:** Bullet list
- **Decisions made:** What was decided (link to decision records)
- **Action items:** What needs to happen next
- **Open questions:** Unresolved items
```

### 6. Daily Index (daily/)
Lightweight daily index. Links only.

```markdown
# YYYY-MM-DD

## Notes of the day
- [[devlog/YYYY-MM-DD-slug]] — short description
- [[decisions/YYYY-MM-DD-slug]] — short description
- [[learnings/YYYY-MM-DD-slug]] — short description
- [[conversations/YYYY-MM-DD-slug]] — short description
```

## Cross-References (Wiki-Links)

Use `[[folder/filename]]` to connect notes:

```markdown
- **Related:** [[projects/webclaw-fork]] | [[devlog/2026-02-10-browserless-setup]]
```

Common patterns:
- Devlog → Project it affects
- Decision → Devlog that implements it
- Learning → Devlog where it was discovered
- Conversation → Decisions and action items from the day
- Daily → Everything from the day

## Workflow

### During conversations
1. Identify documentable moments (decisions, learnings, dev work)
2. After completing a significant task → document BEFORE moving to the next one

### Delegation to sub-agents
To avoid filling the main context or slowing down:
1. Write a detailed `task` with all necessary context
2. Spawn sub-agent with `sessions_spawn`
3. The sub-agent creates notes in the vault following the templates
4. Example task:
```
Document in knowledge vault (knowledge/):
- Type: devlog
- File: knowledge/devlog/2026-02-10-feature-x.md
- Content: [detailed description of what was done, issues, etc.]
- Related: [[projects/name]] | [[decisions/date-slug]]
Also update knowledge/daily/2026-02-10.md adding the link.
```

### At the end of a significant session
1. Create conversation summary
2. Update daily index
3. If there's important info → update `MEMORY.md` with link to the vault

### Periodic review (during heartbeats)
1. Scan recent notes for patterns or connections
2. Promote important items to `MEMORY.md` (with links to the vault)
3. Update project statuses in `knowledge/projects/`
4. Identify knowledge gaps

## MEMORY.md — The Distilled Index

`MEMORY.md` remains the executive summary loaded every session. But now:
- Each item has a link to the vault: `→ see [[devlog/2026-02-10-slug]]`
- Keep it **lean** — 1-2 lines per item
- Details live in the vault, not in MEMORY.md

## Deep Learning Mode ("Learn about this")

When the user asks to learn about a topic:
1. **Full analysis** — read everything, scrape, web search
2. **Go deep** — don't summarize superficially
3. **Document atomically** — individual Learning Notes per concept
4. **Deep dive files** — `knowledge/learnings/YYYY-MM-DD-<topic>.md`
5. **Connect** — links to existing projects, decisions, learnings
6. **Distill** — key takeaways to MEMORY.md with links to the vault

## What to Document

✅ **Always document:**
- Technical decisions and their reasoning
- Bugs found and how they were fixed
- New tools, libs, or techniques discovered
- Architecture changes
- Configuration that took trial and error
- User preferences and requests

❌ **Skip:**
- Routine operations (file reads, simple commands)
- Obvious information the model already knows
- Temporary debugging that led nowhere
