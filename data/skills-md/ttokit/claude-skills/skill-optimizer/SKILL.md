---
name: skill-optimizer
description: |
  Analyzes and optimizes existing skills based on official best practices.
  Evaluates quality score, proposes structural improvements (Progressive Disclosure),
  description enhancement, and error handling additions.
  Use when: "improve skill", "optimize skill", "follow best practices",
  "review skill", "check SKILL.md", "analyze SKILL.md quality".
allowed-tools:
  - Read
  - Write
  - Edit
  - Glob
  - Grep
  - Bash
  - AskUserQuestion
  - Task
---

# Skill Optimizer

Analyze and optimize skills based on official Anthropic best practices.

## Workflow

### Phase 1: Skill Identification

**With argument**: Use specified skill path directly.

**Without argument**:
1. Scan `skills/` directory for SKILL.md files
2. List found skills with names
3. Let user select via AskUserQuestion

### Phase 2: Analysis

1. Read the target SKILL.md
2. **Auto-detect language** from content (Japanese/English)
3. Analyze from these perspectives:

| Category | Points | Check Items |
|----------|--------|-------------|
| Frontmatter | 20 | YAML syntax, name/description required, security constraints |
| Description | 25 | Trigger phrases, specificity, includes both WHAT and WHEN |
| Structure | 20 | Progressive Disclosure, SKILL.md size (under 5000 words) |
| Content | 20 | Error handling, examples, clear instructions |
| Additional | 15 | references/ usage, MCP integration (if applicable) |

4. Calculate quality score:
   - **A**: 90-100 (Almost no issues)
   - **B**: 75-89 (Minor improvements available)
   - **C**: 60-74 (Improvement recommended)
   - **D**: 40-59 (Needs improvement)
   - **F**: 0-39 (Fundamental issues)

5. Organize improvement proposals by category

**Reference files for analysis criteria:**
- `./references/yaml-frontmatter.md` - YAML spec & constraints
- `./references/description-writing.md` - Description field best practices
- `./references/progressive-disclosure.md` - Structure design guide
- `./references/patterns.md` - Workflow patterns
- `./references/mcp-integration.md` - MCP integration guidance
- `./references/troubleshooting.md` - Common issues & solutions
- `./references/checklist.md` - Quality checklist

### Phase 3: User Confirmation

Display analysis results and confirm with AskUserQuestion.

**Output language**: Follow detected skill language.

```
## Analysis Result

**Skill**: {skill_name}
**Quality Score**: {score} ({grade})

### Issues Found

#### Frontmatter ({points}/20)
- {issue_1}
- {issue_2}

#### Description ({points}/25)
- {issue_1}

...

### Improvement Proposals

Select categories to apply:
- [ ] Structure improvements (split to references/)
- [ ] Trigger improvements (description field)
- [ ] Error handling additions
- [ ] MCP integration improvements
```

### Phase 4: Execution

For selected categories:
1. **Maintain original style** (writing style, terminology, tone)
2. **Output in detected language**
3. **Overwrite original directory** (git recovery possible)
4. Display updated score after execution

## Edge Cases

| Case | Response |
|------|----------|
| YAML error | Propose fix as "improvement" |
| Wrong filename | Propose rename as "improvement" |
| No improvement needed | Show score only, report "no issues" |
| Mixed Japanese/English | Detect main language, unify output |
| Multiple language templates | Optimize each in respective language |

## Analysis Details

### Frontmatter Checks (20 points)

- [ ] `---` delimiters present
- [ ] `name` field exists and is kebab-case
- [ ] `description` field exists
- [ ] No XML tags (< >)
- [ ] No "claude" or "anthropic" prefix in name
- [ ] Valid YAML syntax

### Description Checks (25 points)

- [ ] Includes WHAT (what the skill does)
- [ ] Includes WHEN (trigger conditions)
- [ ] Under 1024 characters
- [ ] Contains specific trigger phrases
- [ ] Not too vague ("Helps with projects" is bad)
- [ ] Mentions relevant file types if applicable

### Structure Checks (20 points)

- [ ] SKILL.md under 5000 words
- [ ] Uses Progressive Disclosure (references/ for detailed docs)
- [ ] Critical instructions at top
- [ ] Uses clear headers (## Important, ## Critical)
- [ ] Bullet points and numbered lists for clarity

### Content Checks (20 points)

- [ ] Error handling included
- [ ] Examples provided
- [ ] Instructions are specific and actionable
- [ ] References clearly linked
- [ ] No ambiguous language

### Additional Checks (15 points)

- [ ] references/ used appropriately for large skills
- [ ] MCP tool names correct (if applicable)
- [ ] Validation steps included (if applicable)
