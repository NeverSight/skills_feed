---
name: pai-monitor
description: Monitor Personal AI Infrastructure repo for updates and identify improvement opportunities for Geoffrey. Use when you want to sync Geoffrey with PAI's latest patterns, packs, or architectural decisions.
triggers:
  - "pai monitor"
  - "check pai"
  - "compare to pai"
  - "sync with pai"
  - "pai updates"
  - "personal ai infrastructure"
argument-hint: "[optional: focus area - packs|hooks|skills|patterns]"
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

# PAI Monitor

Monitor the [Personal AI Infrastructure](https://github.com/danielmiessler/Personal_AI_Infrastructure) repository and identify opportunities to improve Geoffrey.

## Focus Areas

When invoked with an argument, focus analysis on that area:
- **packs** - Deep dive on PAI pack additions/changes
- **hooks** - Hook system evolution and patterns
- **skills** - Skill structure and patterns
- **patterns** - Architectural patterns (memory, validation, etc.)

Without an argument, perform full analysis across all areas.

---

## Phase 1: Fetch PAI Current State

### 1.1 Core Documentation
Fetch these from `github.com/danielmiessler/Personal_AI_Infrastructure`:
- `README.md` - Overall structure and philosophy
- `CLAUDE.md` - System instructions and principles
- Check releases for version info

### 1.2 Pack Structure
Explore the Packs/ directory:
- List all available packs
- Sample key packs: hooks, algorithm, memory, skills
- Note any new packs since last analysis

### 1.3 Recent Changes
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
- Hook system usage
- Knowledge storage approach
- Skill structure conventions
- Validation patterns

---

## Phase 3: Gap Analysis

Compare Geoffrey against PAI across these dimensions:

### 3.1 Pack/Skill Coverage
- What PAI packs do we lack equivalent skills for?
- Which packs would provide highest value?
- Are there redundant or outdated skills?

### 3.2 Architectural Patterns
- Hook system: How does PAI's compare to our hooks.json?
- Memory system: Knowledge persistence patterns
- Validation: Secret prevention, protected files

### 3.3 Documentation Patterns
- Does PAI use VERIFY.md, INSTALL.md, or other conventions?
- Are there documentation patterns we should adopt?

### 3.4 Principles Alignment
Check Geoffrey's adherence to PAI founding principles:
- Scaffolding > Model
- Code Before Prompts
- Deterministic Output
- Goal → Code → CLI → Prompts
- Test First

### 3.5 New Features
- Recent PAI additions worth adopting
- Experimental features to watch

---

## Phase 4: Generate Report

Create a markdown report with this structure:

```markdown
# PAI Monitor Report

**Geoffrey Version:** [from plugin.json]
**PAI Version Analyzed:** [from releases or README]
**Analysis Date:** [today's date]

## Executive Summary
[2-3 sentence summary of key findings]

## PAI Recent Changes
| Date | Change | Relevance to Geoffrey |
|------|--------|----------------------|
| ... | ... | ... |

## Packs/Features We Could Adopt
| Priority | Pack/Feature | Purpose | Complexity | Notes |
|----------|-------------|---------|------------|-------|
| High | ... | ... | ... | ... |
| Medium | ... | ... | ... | ... |
| Low | ... | ... | ... | ... |

## Pattern Improvements

### 1. [Pattern Name]
- **PAI Implementation:** [how they do it]
- **Geoffrey Current:** [how we do it / missing]
- **Adoption Benefit:** [why adopt]
- **Files to Modify:** [list]

### 2. [Pattern Name]
...

## Principles Alignment Check
| PAI Principle | Geoffrey Status | Gap |
|--------------|-----------------|-----|
| Scaffolding > Model | [status] | [gap if any] |
| Code Before Prompts | [status] | [gap if any] |
| ... | ... | ... |

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

## Key PAI Areas to Monitor

Based on repo structure, these are the primary areas:

| Area | Description | Geoffrey Equivalent |
|------|-------------|-------------------|
| Packs/ | 24+ modular capability packages | skills/ |
| Releases/ | Full system snapshots | plugin versions |
| Hook System | 14+ event types | hooks.json |
| Memory System | Knowledge persistence | Obsidian vault |
| Algorithm System | ISC tracking, metrics | compound learnings |
| Validation | `.pai-protected.json` | (none currently) |

---

## Execution Notes

1. **Start with Phase 1** - Always fetch fresh PAI data, don't rely on cached knowledge
2. **Be thorough in Phase 2** - Accurate self-assessment is critical for gap analysis
3. **Prioritize in Phase 3** - Not all gaps need filling; focus on high-value opportunities
4. **Actionable Phase 4** - Every recommendation should have clear next steps

When focusing on a specific area, still provide brief context from other phases but concentrate analysis on the requested focus.
