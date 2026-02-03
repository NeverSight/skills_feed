---
name: reinforce-skills
description: "This skill should be used when the user asks to 'reinforce skills', 'add skill map', 'update skill map', 'sync skills to CLAUDE.md', 'persist skills', 'save skills to project', 'embed skills', 'skills keep getting forgotten', 'I keep forgetting skills', or when setting up a new project where installed skills should be persisted as context. Generates a compressed skill-mapping directive in CLAUDE.md following the Vercel AGENTS.md research pattern."
---

# Reinforce Skills

Inject a compressed skill-mapping directive into a project's CLAUDE.md file so skill names and invocation triggers persist across the entire session without being lost to context drift.

## Problem

LLMs lose track of skill names and invocation details as conversation context grows. Skills load at session start but fade from working memory mid-session, causing the agent to guess names, skip invocations, or fail to call skills the user explicitly requested.

## Solution

Vercel's research found that **passive context embedded in project files outperforms active skill retrieval** — 100% vs 79% pass rate in agent evals. Embed a compressed skill map directly in CLAUDE.md using the same directive pattern.

Reference: https://vercel.com/blog/agents-md-outperforms-skills-in-our-agent-evals

For detailed research findings, consult **`references/vercel-research.md`**.

## File Placement

| Tool | File |
|------|------|
| Claude Code | `CLAUDE.md` |
| Cursor | `AGENTS.md` |
| Other agents | `AGENTS.md` |

For Claude Code projects, inject into **CLAUDE.md**. For multi-tool projects, consider both files.

## Compressed Directive Format

Single-line, pipe-delimited block wrapped in HTML comments. Opens with a forceful imperative directive, followed by task-to-skill mappings:

```
<!-- SKILL-MAP-START -->STOP. You WILL forget skill names mid-session. Check this map before ANY task.|task-trigger→Skill(exact-skill-name)|another-trigger→Skill(another-skill)<!-- SKILL-MAP-END -->
```

### Format Rules

- Single line — no line breaks within the block
- Pipe `|` separates each entry
- Arrow `→` maps trigger to skill invocation
- HTML comment markers `SKILL-MAP-START` / `SKILL-MAP-END` enable programmatic updates
- Opening directive must be forceful and imperative
- Use exact skill names as listed in the Skill tool's available skills (shown in system-reminder messages)
- Wildcard syntax `Skill(namespace:*)` for skill families (e.g., `bsv-skills:*`)

## Workflow

### Step 1: Inventory available skills

Two authoritative sources for installed skills:

1. **System-reminder skill list** — The Skill tool's available skills appear in system-reminder messages at conversation start. This is the definitive list of all skills including plugin skills.
2. **Global skills directory** — `ls ~/.claude/skills/` shows user-installed skills (subset of the full list).

Cross-reference both sources.

### Step 2: Identify project-relevant skills

1. **Read CLAUDE.md** — Identify tech stack, frameworks, tools
2. **Check package.json / go.mod / Cargo.toml** — Map dependencies to skills (e.g., `better-auth` → `better-auth-best-practices`, `ai` → `ai-sdk`, `remotion` → `remotion-best-practices`)
3. **Scan recent git history** — Identify recurring work patterns
4. **Check conversation history** — Look for past `Skill()` invocations if available

For a comprehensive trigger-to-skill mapping table, consult **`references/common-mappings.md`**.

### Step 3: Next.js codemod (conditional)

If the project uses Next.js, run the official codemod for framework docs:

```bash
npx @next/codemod@canary agents-md --version <version-from-package.json> --output AGENTS.md
```

This creates a separate compressed Next.js docs index in AGENTS.md. The skill map is independent and goes in CLAUDE.md.

If the project does not use Next.js, skip this step entirely.

### Step 4: Build the skill map

Construct the compressed directive. Only include skills relevant to the project's stack. Refer to **`references/common-mappings.md`** for the full trigger-to-skill reference table.

### Step 5: Inject into CLAUDE.md

Place the skill map near the top of CLAUDE.md. If the file has YAML frontmatter (`---` delimiters), place the skill map **after** the closing `---` but before the first heading or content. If no frontmatter, place after the title heading.

```markdown
---
description: Project description
globs: "*.ts"
---

<!-- SKILL-MAP-START -->STOP. You WILL forget skill names mid-session. Check this map before ANY task.|trigger→Skill(name)|...<!-- SKILL-MAP-END -->

## Project Overview
...
```

Or without frontmatter:

```markdown
# CLAUDE.md

<!-- SKILL-MAP-START -->STOP. You WILL forget skill names mid-session. Check this map before ANY task.|trigger→Skill(name)|...<!-- SKILL-MAP-END -->

## Project Overview
...
```

### Step 6: Verify

1. Block is a single line (no breaks between START and END markers)
2. All skill names are exact (match the Skill tool's available skills list)
3. Directive opens with a forceful imperative
4. CLAUDE.md still reads cleanly for humans
5. If frontmatter exists, the block is outside the `---` delimiters

## Updating an Existing Map

1. Read the existing `<!-- SKILL-MAP-START -->...<!-- SKILL-MAP-END -->` block
2. Parse current mappings
3. Add, remove, or update entries
4. Replace the entire block with the updated single-line version

## Key Principles

1. **Passive over active** — Embedding beats on-demand retrieval for consistent invocation
2. **Forceful directives** — Polite suggestions get ignored mid-session. Imperative commands persist.
3. **Exact names** — Never abbreviate or guess. Use the exact registered skill name.
4. **Project-specific** — Only include skills relevant to the project's actual stack
5. **Single line** — The compressed format must stay on one line to match the proven pattern

## Additional Resources

### Reference Files

- **`references/vercel-research.md`** — Detailed summary of Vercel's AGENTS.md research: methodology, eval results, three factors for passive context superiority, and compression technique details
- **`references/common-mappings.md`** — Comprehensive trigger-to-skill mapping table organized by category (workflow, quality, frontend, video, marketing, auth, infrastructure, desktop)
