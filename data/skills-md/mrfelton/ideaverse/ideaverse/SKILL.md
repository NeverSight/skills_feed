---
name: ideaverse
description: Work with Ideaverse-based Obsidian vaults using the ACE framework (Atlas/Calendar/Efforts) and LYT (Linking Your Thinking) methodology. Use when creating notes, organizing knowledge, building Maps of Content (MOCs), maintaining daily logs, cross-referencing ideas, assimilating new information, or working with any Obsidian vault that follows Ideaverse conventions. Triggers on requests to add knowledge, link notes, create MOCs, update daily logs, archive projects, or discover connections between ideas.
---

# The Ideaverse Methodology

Apply the ACE framework (Atlas/Calendar/Efforts), LYT (Linking Your Thinking) conventions, and the ARC workflow (Add/Relate/Communicate) to organize and connect knowledge.

## Core Framework: ACE

**ACE** organizes all content by **intention**, not topic:

| Folder | Purpose | Question It Answers | Orientation |
|--------|---------|---------------------|--------------|
| **Atlas/** | Permanent, reusable knowledge | "What do I know?" | Space (relatedness) |
| **Calendar/** | Temporal records, when things happened | "When did this happen?" | Time (reflection) |
| **Efforts/** | Active work, goals, and projects | "What am I working on?" | Action (importance) |

Separate project-specific material (Efforts/) from permanent knowledge (Atlas/). When a concept has reuse value beyond its originating project, extract it to Atlas/ and link back.

## The ARC Workflow

Follow the three phases:

### 1. ADD (Capture)
- Capture to daily logs, inboxes, or fleeting notes without friction
- Do not organize immediately; avoid decision fatigue
- Get ideas into the system first, then process

### 2. RELATE (Connect) - The Critical Phase
Before creating or filing any permanent note:

1. **Search first** - Check if the concept already exists in your vault
2. **Read relevant MOCs** - Understand existing structure before adding
3. **Extract atomic concepts** - One idea per note
4. **Set relationship properties** in frontmatter (up, related, created)
5. **Check for squeeze points** - If you're linking to a term 10+ times without an MOC, create one

### 3. COMMUNICATE (Express)
- Use connected notes as sources for output
- Link and transclude from existing notes rather than duplicating
- Transform captured ideas into finished work

## MOC-First Navigation

When exploring or searching the vault:

1. **Start with MOCs** - They contain human-curated structure and signal
2. **Follow links** from MOCs to atomic notes
3. **Prefer MOC paths over keyword search** - MOCs guide; raw search returns noise
4. **Create MOCs when squeezed** - When 10+ related notes exist without structure

## Required Conventions

Use YAML frontmatter to express relationships and creation dates. Keep relationship links in frontmatter as arrays and use quoted wikilinks.

For the complete frontmatter specification and examples, read [references/frontmatter.md](references/frontmatter.md).

### Linking
- Use Wikilinks in Obsidian: `[[Page Name]]` or `[[Page Name|Alias]]`
- Avoid markdown links for internal references
- Link freely where relationships are meaningful
- Use aliases for clarity when helpful

### Text Style
- Use hyphens with spaces (` - `), not em-dashes (`—`)
- Use `-` for unordered lists
- Keep notes atomic and focused

## Key Workflows

Use the ARC workflow (Add → Relate → Communicate) as the core process. For detailed procedures, read [references/workflows.md](references/workflows.md):

1. **Add (Capture)** - Get information into the system without friction
2. **Relate (Connect)** - Transform raw capture into connected knowledge
3. **Communicate (Express)** - Use connected knowledge to produce output

Other essential workflows:

- **Creating/evolving MOCs** - When and how to build Maps of Content
- **Daily log maintenance** - Keeping temporal records updated and linked
- **Work completion** - Extracting knowledge before archiving completed projects
- **Cross-reference discovery** - Finding and adding back-references proactively

## Extending Ideaverse

Allow vault-specific extensions (status, type, tags, area, rank) as needed. Use the vault’s implementation guide for those customizations.

## Templates

Optional template for daily logs:
- [assets/daily-log-template.md](assets/daily-log-template.md) - Structured daily log format

## Vault Maintenance Scripts

Use the maintenance skill for diagnostics and scripts: [../ideaverse-maintenance/SKILL.md](../ideaverse-maintenance/SKILL.md).

## Common Pitfalls

| Pitfall | Symptom | Solution |
|---------|---------|----------|
| **Over-connecting** | Links everywhere, none meaningful | Only link where genuine relationship exists. Ask: "Would a reader benefit from this connection?" |
| **Premature organization** | Complex folder structures before ideas stabilize | Wait for the mental squeeze point (10+ notes on a topic) before creating MOCs |
| **Knowledge fragmentation** | Same idea captured in multiple places | Search Atlas/ before creating new notes; consolidate duplicates |
| **Under-linking** | Notes feel isolated, no emergent connections | Link freely during Relate phase; follow the "squeeze point" principle for MOCs |
| **Garden neglect** | Orphaned notes, broken links, stale content | Schedule regular maintenance sweeps (weekly or monthly) using validation scripts |
