---
name: content-retrieval
description: "Token-efficient retrieval using depth levels (L0-L5) and heading-based sections. Use for any file reads."
layer: 4
tech_stack: [agnostic]
topics: [retrieval, efficiency, tokens, grep, read, protocol]
depends_on: []
complements: [knowledge-discovery]
keywords: [retrieve, read, grep, lookup, tokens, efficient, partial, section]
auto_apply: true
---

# Content Retrieval Protocol

Token-efficient retrieval system using markdown-native section detection.

## Summary

**Core Principle**: Never read a full file when partial content suffices.

Choose retrieval depth by need:
- **Exists?** → Grep (files_with_matches)
- **Count?** → Grep (count)
- **Lookup?** → Grep (-C:2)
- **Overview?** → Read (limit:40)
- **Section?** → Grep heading → Read (offset, limit)
- **Full?** → Read (justify first)

---

## Quick Reference

### Depth Levels

| Level | Need | Method | Lines |
|-------|------|--------|-------|
| L0 | Exists? | `Grep(output: files_with_matches)` | ~1 |
| L1 | Count? | `Grep(output: count)` | ~1 |
| L2 | Lookup value | `Grep(pattern, -C:2)` | ~5 |
| L3 | Overview | `Read(limit: 40)` | ~40 |
| L4 | Section | Grep heading → Read(offset, limit) | ~50 |
| L5 | Full | `Read()` - justify first | All |

### Decision Tree

```
What do I need?
├─ Does X exist? ──────────► L0: Grep files_with_matches
├─ How many X? ────────────► L1: Grep count
├─ What is X's value? ─────► L2: Grep with context
├─ What does X do? ────────► L3: Read limit:40
├─ How to use X for Y? ────► L4: Section extraction
└─ Implement X fully? ─────► L5: Full read (target only)
```

### Tool Selection

| Scenario | Tool | Parameters |
|----------|------|------------|
| Check skill exists | Grep | `output: files_with_matches` |
| Count matches | Grep | `output: count` |
| Get specific row | Grep | `pattern, -C: 0-2` |
| Read frontmatter | Read | `limit: 25` |
| Read frontmatter+summary | Read | `limit: 40` |
| Extract section | Read | `offset: N, limit: 50` |
| Full understanding | Read | (no limit) |

---

## Section Extraction

### How Sections Work (Markdown-Native)

Sections are defined by **headings** and **horizontal rules**:

```markdown
## Section A
Content...

---                    ← Section A ends here (horizontal rule)

## Section B           ← Or section ends at next same-level heading
Content...
```

**No custom markers needed.** Standard markdown structure.

### Extraction Algorithm

```
1. Grep("^## Section Name$", file)     → line 15
2. Grep("^---|^## ", file, offset: 16) → next break at line 30
3. Read(file, offset: 15, limit: 15)   → lines 15-30
```

### Section End Detection

A section ends at the **first** of:
1. `---` (horizontal rule)
2. `## ` (same-level heading)
3. `# ` (higher-level heading)
4. EOF (end of file)

### Examples

```bash
# Extract Summary section
Grep("^## Summary$", file) → line 20
Grep("^---|^## ", file, offset: 21) → line 28
Read(file, offset: 20, limit: 8)

# Extract Quick Reference section
Grep("^## Quick Reference$", file) → line 30
Grep("^---|^## ", file, offset: 31) → line 55
Read(file, offset: 30, limit: 25)
```

---

## Retrieval Protocol

### Rule 1: Start at Lowest Depth

```
WRONG: Read entire SKILL-INDEX.md to find one skill
RIGHT: Grep("skill-name", SKILL-INDEX.md, -C:1)

WRONG: Read 5 skill files to understand what they do
RIGHT: Read each with limit:40 (frontmatter + summary)

WRONG: Read entire agent file to check if it has a skill
RIGHT: Grep("skills:.*skill-name", agent.md)
```

### Rule 2: Index First, Files Second

```
1. Check index file (SKILL-INDEX.md, AGENT-INDEX.md)
2. Extract needed info via grep
3. Only read source file if index insufficient
```

### Rule 3: Frontmatter Contains Metadata

All files have metadata in first 20 lines:

```yaml
---
name: identifier
description: "one-line summary"
layer: 1-4
keywords: [searchable, terms]
---
```

**To get metadata**: `Read(file, limit: 20)`

### Rule 4: Headings Define Sections

Standard markdown headings define extractable sections:

```markdown
## Summary          ← Grep target
Brief description.

---

## Quick Reference  ← Grep target
| Col | Col |
```

**To extract section**: Grep heading → find end → Read range

### Rule 5: Full Read Only for Targets

Full read justified when:
- File is the TARGET being modified/implemented
- L3 read confirmed full content needed
- Creating comprehensive documentation
- Debugging requires full context

---

## QMD File Structure

### Standard Layout

```markdown
---
name: identifier
description: "One-line (< 100 chars)"
layer: 1-4
keywords: [grep, targets]
---

# Title

## Summary

2-3 sentences. Key purpose.

---

## Quick Reference

| Pattern | Usage |
|---------|-------|

---

## Patterns

### Pattern 1
Content...

### Pattern 2
Content...

---

## Related

- [link](path)
```

### Reserved Headings

| Heading | Purpose | Required |
|---------|---------|----------|
| `## Summary` | Quick understanding (L3) | Yes |
| `## Quick Reference` | Lookup tables (L2-L3) | Yes |
| `## Patterns` | Implementation details | For skills |
| `## Scope` | Does/Does NOT | For agents |
| `## Related` | Cross-references | Recommended |

### Frontmatter Schema

```yaml
---
# Required
name: string           # Identifier (grep target)
description: string    # One-line (< 100 chars)
layer: number          # 1=foundation, 2=framework, 3=feature, 4=workflow

# Recommended
keywords: string[]     # Grep targets
depends_on: string[]   # Prerequisites
complements: string[]  # Often-used-with

# Optional
used_by: string[]      # Agents/commands using this
tech_stack: string[]   # Technologies
auto_apply: boolean    # Auto-trigger on match
---
```

---

## Index File Format

### Grep-Optimized Tables

```markdown
## Master Index

| Name | L | Keywords | Path |
|------|---|----------|------|
| skill-a | 2 | key1,key2 | skills/skill-a/SKILL.md |
| skill-b | 1 | key3,key4 | skills/skill-b/SKILL.md |

---

## Lookup by Keyword

| Keyword | Skills |
|---------|--------|
| entity | abp-framework, abp-entity, domain-modeling |
```

**Grep usage**:
```
Grep("skill-a", INDEX.md, output: content, -C: 0)
→ | skill-a | 2 | key1,key2 | skills/skill-a/SKILL.md |
```

---

## Examples

### Example 1: Analyze Agent

**Old approach** (2,434 lines):
```
Read(AGENT-QUICK-REF.md)        → 127 lines
Read(abp-developer.md)          → 144 lines
Read(SKILL-INDEX.md)            → 337 lines
Read(3 skill files)             → 1,283 lines
```

**Protocol approach** (~265 lines):
```
Read(abp-developer.md)                    → 108 lines (target)
Grep("abp-developer", AGENT-INDEX.md)     → 1 line
Grep(skills from agent, SKILL-INDEX.md)   → 11 lines
Read(3 skills, limit:40 each)             → 120 lines
```

**Savings: 89%**

### Example 2: Check Skill Exists

```bash
# L0: Just check existence
Grep("^name: xunit-testing", .claude/skills, output: files_with_matches)
→ .claude/skills/xunit-testing-patterns/SKILL.md
```

### Example 3: Extract Section

```bash
# L4: Section extraction (markdown-native)
Grep("^## Quick Reference$", skill.md) → line 30
Grep("^---|^## ", skill.md, offset: 31) → line 55
Read(skill.md, offset: 30, limit: 25)
→ Just the Quick Reference section
```

---

## Checklist

### For File Authors

- [ ] Frontmatter under 20 lines
- [ ] `description` is one line, under 100 chars
- [ ] `keywords` include grep targets
- [ ] `## Summary` section present (2-3 sentences)
- [ ] `## Quick Reference` has lookup tables
- [ ] `---` separators between major sections
- [ ] No critical info buried deep

### For Consumers

- [ ] Check index before reading files
- [ ] Use appropriate depth level (L0-L5)
- [ ] Start with L0-L2, escalate if needed
- [ ] Full read only for target files

---

## Related

- [knowledge-discovery](../knowledge-discovery/SKILL.md) - What skills to find
- [SKILL-INDEX.md](../../SKILL-INDEX.md) - Skill lookup tables
- [AGENT-INDEX.md](../../AGENT-INDEX.md) - Agent lookup tables
- [GUIDELINES.md](../../GUIDELINES.md) - Standards and protocols
