---
name: learn
description: >-
  Extracts lessons learned from conversations and persists them to AI assistant
  config files (CLAUDE.md, GEMINI.md, AGENTS.md, Cursor, Copilot, Windsurf,
  Continue). Use when: debugging revealed issues, commands failed then succeeded,
  assumptions proved wrong, workarounds were discovered, undocumented behavior
  found, or user says "remember this".
license: MIT
compatibility: Requires bash shell and file system write access
metadata:
  author: Gregory Murray
  repository: github.com/whatifwedigdeeper/agent-skills
  version: "0.3"
---

# Learn from Conversation

Analyze the conversation to extract lessons learned, then persist them to AI assistant configuration files.

## Supported Assistants

| Assistant | Config File | Format |
|-----------|-------------|--------|
| Claude Code | `CLAUDE.md` | Markdown |
| Gemini | `GEMINI.md` | Markdown |
| AGENTS.md | `AGENTS.md` | Markdown |
| Cursor | `.cursorrules` or `.cursor/rules/*.mdc` | Markdown/MDC |
| GitHub Copilot | `.github/copilot-instructions.md` | Markdown |
| Windsurf | `.windsurf/rules/rules.md` | Markdown |
| Continue | `.continuerc.json` | JSON |

See [references/assistant-configs.md](references/assistant-configs.md) for format details.

## Process

### 1. Detect and Assess Configurations

Scan for config files and check their sizes:

```bash
for f in CLAUDE.md GEMINI.md AGENTS.md .cursorrules .github/copilot-instructions.md \
  .windsurf/rules/rules.md .continuerc.json; do
  [ -f "$f" ] && wc -l "$f"
done
find .cursor/rules -name "*.mdc" -exec wc -l {} \; 2>/dev/null
```

**Behavior based on detection:**

| Scenario | Action |
|----------|--------|
| Single config found | Update it automatically |
| Multiple configs found | Prompt user to select which to update |
| No configs found | Display init commands from [assistant-configs.md](references/assistant-configs.md), then exit |

#### Size Thresholds

| Lines | Status | Action |
|-------|--------|--------|
| < 400 | Healthy | Add learnings directly |
| 400-500 | Warning | Add carefully, suggest cleanup |
| > 500 | Oversized | [Refactor](references/refactoring.md) before adding new content |

#### Discover Existing Skills

List skills for routing decisions:

```bash
find . -name "SKILL.md" -type f 2>/dev/null | grep -v node_modules | \
  xargs grep -l "^name:" | while read -r f; do
  grep -m1 "^name:" "$f" | sed 's/name: //'
done
```

### 2. Analyze Conversation

Scan for:
- **Corrections**: Commands retried, assumptions proven wrong, missing prerequisites
- **Discoveries**: Undocumented patterns, integration quirks, environment requirements
- **Improvements**: Steps that should be automated or validated earlier

### 3. Categorize and Route Each Learning

| Category | Primary Destination | Fallback When Oversized |
|----------|---------------------|------------------------|
| Project facts | Config file | Extract to new skill |
| Prerequisites | Config file | Extract to `project-setup` skill |
| Environment | Config file | Extract to `environment-setup` skill |
| Workflow pattern | Existing related skill | Create new skill |
| Automated workflow | New skill | New skill (always) |

#### Routing Decision Tree

For each learning, evaluate in order:

1. **Is this a multi-step automated workflow (>5 steps)?**
   - YES → Create new skill (proceed to Step 5, Route C)
   - NO → Continue

2. **Does an existing skill cover this topic?**
   - YES → Update that skill
   - NO → Continue

3. **Is the target config file oversized (>500 lines)?**
   - YES → Create new skill OR offer refactoring (see Step 4)
   - NO → Continue

4. **Is this learning situation-specific (applies to narrow context)?**
   - YES → Create new skill with `globs` or context constraints
   - NO → Add to config file

#### Size-Based Rules

| Learning Size | Preferred Destination |
|---------------|----------------------|
| < 3 lines | Config file (even if near threshold) |
| 3-30 lines | Follow decision tree above |
| > 30 lines | Strongly prefer skill creation |

#### Skill Relevance Matching

Match learnings to existing skills using these criteria:

| Learning Topic | Matching Skill Indicators |
|----------------|--------------------------|
| Testing patterns | Skill name contains: test, spec, e2e, unit |
| Build/compile issues | Skill name contains: build, compile, bundle |
| Dependencies | Skill name contains: package, dependency, npm, yarn |
| API patterns | Skill name contains: api, http, fetch, request |
| Database | Skill name contains: db, database, migration, schema |
| Deployment | Skill name contains: deploy, release, ci, cd |

Also check skill `description` field for keyword overlap with the learning topic.

### 4. Present and Confirm

For each learning, show:
```
**[Category]**: [Brief description]
- Source: [What happened in conversation]
- Proposed change: [Exact text or file to add]
- Destination: [Config file] ([current] → [projected] lines)
```

#### Handle Size Threshold

If adding the learning would push a config file over threshold:

```
Adding this learning would bring [filename] to [X] lines (threshold: [Y]).

Options:
1. Add learning anyway (not recommended)
2. [Refactor](references/refactoring.md) existing content to skills first, then add
3. Create a new skill for this learning instead
4. Skip this config file
```

Ask for confirmation before applying each change.

### 5. Apply Changes

Apply changes based on routing decision from Step 3:

#### Route A: Add to Config File

**Markdown configs** (CLAUDE.md, GEMINI.md, AGENTS.md, Copilot, Windsurf):
- Find appropriate section, preserve existing structure
- Append to relevant section or create new section if needed

**Cursor rules**:
- Legacy `.cursorrules`: Treat like markdown, append content
- Modern `.cursor/rules/*.mdc`: See [references/format-cursor-mdc.md](references/format-cursor-mdc.md)

**Continue** (`.continuerc.json`):
- Update `customInstructions` field, preserving existing content
- See [references/format-continue.md](references/format-continue.md)

#### Route B: Update Existing Skill

When adding to an existing skill:

1. Read the skill file: `skills/[name]/SKILL.md`
2. Find appropriate section or create new one
3. Append learning, maintaining the skill's existing structure
4. If skill has references, consider adding to reference file instead

**Skill update format:**
```markdown
## [New Section or append to existing]

[Learning content formatted as guidance or workflow step]
```

#### Route C: Create New Skill

Create in `skills/[name]/SKILL.md` with this template:

```markdown
---
name: [learning-topic]
description: [What this handles and when to use it - triggers belong here, not in body]
---

# [Learning Topic]

[Learning content structured as workflow]

## Process

### 1. [First Step]
[Details]
```

### 6. Verify Changes

After applying each change, confirm success by showing:
```
✓ Added to [file path]:
  [Section name]
  > [First 2-3 lines of added content...]
```

If a write failed, report the error and offer to retry or skip.

### 7. Summarize

List:
- Config files modified (with full paths)
- Sections updated in each file
- Any skills created

## Examples

| Situation | Learning |
|-----------|----------|
| "e2e tests failed because API wasn't running" | Add prerequisite to selected config(s) |
| "Parse SDK doesn't work with Vite out of the box" | Document workaround in selected config(s) |
| "Build failed because NODE_ENV wasn't set" | Add required env var to selected config(s) |
| "Every component needs tests, lint, build..." | Create `add-component` skill |

## Edge Cases

| Scenario | Handling |
|----------|----------|
| No configs detected | Guide user to initialize one first, exit early |
| Multiple configs found | Prompt user to select which to update |
| Malformed config file | Warn and skip that file |
| Duplicate content exists | Check before adding, warn if similar learning exists |
| Config file already oversized | Offer refactoring before adding (Step 4) |
| Learning matches multiple skills | Present options, let user choose which skill to update |
| Skill file also oversized | Suggest creating sub-skills or reference files |
| Learning is very small (<3 lines) | Prefer config file even if near threshold |
| Learning is very large (>30 lines) | Strongly suggest skill creation |
| No existing skills found | Skip skill matching, proceed with config or new skill |

## Guidelines

See [references/guidelines.md](references/guidelines.md) for learning quality principles.
