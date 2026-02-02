---
name: provenance
description: 'Trace knowledge artifact lineage and sources. Find orphans, stale citations. Triggers: "where did this come from", "trace this learning", "knowledge lineage".'
---

# Provenance Skill

Trace knowledge artifact lineage to sources.

## Execution Steps

Given `/provenance <artifact>`:

### Step 1: Read the Artifact

```
Tool: Read
Parameters:
  file_path: <artifact-path>
```

Look for provenance metadata:
- Source references
- Session IDs
- Dates
- Related artifacts

### Step 2: Trace Source Chain

```bash
# Check for source metadata in the file
grep -i "source\|session\|from\|extracted" <artifact-path>

# Search for related transcripts
ao forge search "<artifact-name>" 2>/dev/null
```

### Step 3: Build Lineage Chain

```
Transcript (source of truth)
    ↓
Forge extraction (candidate)
    ↓
Human review (promotion)
    ↓
Pattern recognition (tier-up)
    ↓
Skill creation (automation)
```

### Step 4: Write Provenance Report

```markdown
# Provenance: <artifact-name>

## Current State
- **Tier:** <0-3>
- **Created:** <date>
- **Citations:** <count>

## Source Chain
1. **Origin:** <transcript or session>
   - Line/context: <where extracted>
   - Extracted: <date>

2. **Promoted:** <tier change>
   - Reason: <why promoted>
   - Date: <when>

## Related Artifacts
- <related artifact 1>
- <related artifact 2>
```

### Step 5: Report to User

Tell the user:
1. Artifact lineage
2. Original source
3. Promotion history
4. Related artifacts

## Finding Orphans

```bash
/provenance --orphans
```

Find artifacts without source tracking:
```bash
# Files without "Source:" or "Session:" metadata
for f in .agents/learnings/*.md; do
  grep -L "Source\|Session" "$f" 2>/dev/null
done
```

## Finding Stale Artifacts

```bash
/provenance --stale
```

Find artifacts where source may have changed:
```bash
# Artifacts older than their sources
find .agents/ -name "*.md" -mtime +30 2>/dev/null
```

## Key Rules

- **Every insight has a source** - trace it
- **Track promotions** - know why tier changed
- **Find orphans** - clean up untracked knowledge
- **Maintain lineage** - provenance enables trust
