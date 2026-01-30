---
name: clawdbot-monitor
description: Monitor Clawdbot repo for updates and identify improvement opportunities for Geoffrey. Use when comparing Geoffrey to Clawdbot patterns, skills, or features.
triggers:
  - "clawdbot monitor"
  - "check clawdbot"
  - "compare to clawdbot"
  - "sync with clawdbot"
  - "clawdbot updates"
argument-hint: "[optional: focus area - skills|hooks|extensions|memory]"
model: claude-opus-4-5-20251101
context: fork
agent: Explore
allowed-tools:
  - WebFetch
  - WebSearch
  - Read
  - Grep
  - Glob
extended-thinking: true
version: 1.0.0
---

# Clawdbot Monitor

Monitor the [Clawdbot](https://github.com/clawdbot/clawdbot) repository and identify opportunities to improve Geoffrey.

## Clawdbot vs Geoffrey Quick Comparison

| Aspect | Clawdbot | Geoffrey |
|--------|----------|----------|
| **Scope** | Multi-channel messaging hub (WhatsApp, Discord, etc.) | Claude Code plugin for personal AI |
| **Skills** | 60+ (CLI wrappers, platform integrations) | 26 (specialized workflows) |
| **Hooks** | Event-driven TypeScript handlers | hooks.json configuration |
| **Memory** | Hybrid vector + BM25 with SQLite-vec | Obsidian vault + knowledge-manager |
| **Releases** | Weekly (v2026.x.x latest) | Versioned plugin (v0.x.x) |

## Focus Areas

When invoked with an argument, focus analysis on that area:
- **skills** - Skill formats, metadata, categories, CLI patterns
- **hooks** - Event types, handler patterns, automation
- **extensions** - Plugin architecture, provider isolation
- **memory** - Search patterns, embeddings, persistence

Without an argument, perform full analysis across all areas.

---

## Phase 1: Fetch Clawdbot Current State

### 1.1 Core Documentation
Fetch these from `github.com/clawdbot/clawdbot`:
- `README.md` - Overall structure and philosophy
- `CLAUDE.md` - System instructions (if exists)
- Check releases page for version info

### 1.2 Skill Structure
Explore the skills directory:
- List all available skills
- Sample key skills that overlap with Geoffrey's domains
- Note skill metadata patterns (`requires.bins`, `requires.config`, install methods)
- Check for new skills since last analysis

### 1.3 Hook System
Examine hook architecture:
- Event types (session, command, boot)
- Handler patterns (TypeScript)
- Compare to Geoffrey's hooks.json approach

### 1.4 Recent Changes
- Check recent commits for significant updates
- Look for new patterns or breaking changes
- Note any announcements or migration guides

---

## Phase 2: Analyze Geoffrey Current State

### 2.1 Core Architecture
Read these Geoffrey files:
- `CLAUDE.md` - Founding principles and guidelines
- `README.md` - Current capabilities
- `.claude-plugin/plugin.json` - Version info

### 2.2 Skills Inventory
```bash
# Glob for all skills
skills/*/SKILL.md
```
Create inventory of current skills and their purposes.

### 2.3 Pattern Identification
Identify Geoffrey's current patterns:
- Hook system usage (hooks.json)
- Knowledge storage approach (Obsidian vault)
- Skill structure conventions (SKILL.md frontmatter)
- Validation patterns

---

## Phase 3: Gap Analysis

Compare Geoffrey against Clawdbot across these dimensions:

### 3.1 Skill Coverage
- What Clawdbot skills do we lack equivalent skills for?
- Which skills would provide highest value for Geoffrey's use case?
- Are there redundant or outdated skills?

### 3.2 Skill Metadata System
- `requires.bins` - CLI dependency declarations
- `requires.config` - Configuration requirements
- Install methods - How skills auto-install dependencies
- Compare to Geoffrey's current skill structure

### 3.3 Hook System
- Clawdbot: Event-driven TypeScript handlers
- Geoffrey: hooks.json configuration
- What event types are missing?
- What patterns could we adopt?

### 3.4 Extension Architecture
- Plugin isolation patterns
- Multi-provider support (LLM providers, messaging channels)
- How Clawdbot handles modularity

### 3.5 Memory System
- Clawdbot: Hybrid vector + BM25 with SQLite-vec
- Geoffrey: Obsidian vault + knowledge-manager
- Embedding integration patterns
- Search and retrieval approaches

### 3.6 New Features
- Recent Clawdbot additions worth adopting
- Experimental features to watch

---

## Phase 4: Generate Report

Create a markdown report with this structure:

```markdown
# Clawdbot Monitor Report

**Geoffrey Version:** [from plugin.json]
**Clawdbot Version Analyzed:** [from releases]
**Analysis Date:** [today's date]

## Executive Summary
[2-3 sentence summary of key findings]

## Clawdbot Recent Changes
| Date | Change | Relevance to Geoffrey |
|------|--------|----------------------|
| ... | ... | ... |

## Features/Patterns to Adopt
| Priority | Feature | Purpose | Complexity | Notes |
|----------|---------|---------|------------|-------|
| High | ... | ... | ... | ... |
| Medium | ... | ... | ... | ... |
| Low | ... | ... | ... | ... |

## Pattern Improvements

### 1. [Pattern Name]
- **Clawdbot Implementation:** [how they do it]
- **Geoffrey Current:** [how we do it / missing]
- **Adoption Benefit:** [why adopt]
- **Files to Modify:** [list]

### 2. [Pattern Name]
...

## Skill Coverage Comparison
| Domain | Clawdbot Skill | Geoffrey Equivalent | Gap |
|--------|---------------|--------------------| ----|
| ... | ... | ... | ... |

## Recommended Actions

### Immediate (This Week)
- [ ] Action 1
- [ ] Action 2

### Short-Term (This Month)
- [ ] Action 1
- [ ] Action 2

### Long-Term (Explore)
- [ ] Action 1
- [ ] Action 2
```

---

## Key Clawdbot Areas to Monitor

Based on repo structure, these are the primary areas:

| Area | Description | Geoffrey Equivalent |
|------|-------------|-------------------|
| skills/ | 60+ modular skills | skills/ (26) |
| Hooks | Event-driven TypeScript | hooks.json |
| Extensions | Plugin architecture | (none currently) |
| Memory | Hybrid vector + BM25 | Obsidian vault |
| Channels | WhatsApp, Discord, etc. | N/A (Claude Code only) |

---

## Key Differences from PAI Monitor

| Aspect | PAI | Clawdbot |
|--------|-----|----------|
| Update frequency | Less frequent | Weekly releases |
| Architecture | Packs + CLI | Daemon + extensions |
| Skill count | 24 packs | 60+ skills |
| Memory model | File-based | Vector DB (SQLite-vec) |
| Target | Personal AI | Messaging hub |

---

## Execution Notes

1. **Start with Phase 1** - Always fetch fresh Clawdbot data, don't rely on cached knowledge
2. **Be thorough in Phase 2** - Accurate self-assessment is critical for gap analysis
3. **Prioritize in Phase 3** - Not all gaps need filling; focus on high-value opportunities for Geoffrey's use case
4. **Actionable Phase 4** - Every recommendation should have clear next steps
5. **Note Architecture Differences** - Clawdbot is a daemon, Geoffrey is a plugin; some patterns won't translate

When focusing on a specific area, still provide brief context from other phases but concentrate analysis on the requested focus.
