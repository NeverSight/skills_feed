---
name: reviewing-skills
description: Review skill files for best practices compliance (naming, description, structure, size). Use when checking SKILL.md quality or getting feedback before publishing. Static analysis only - does NOT execute the skill.
license: Apache-2.0
metadata:
  author: Softgraphy GK
  version: "0.2.0"
---

# Reviewing Skills

Comprehensive review of agent skills against Claude's official best practices.

## Quick Start

To review a skill:

1. Ask user for skill path (e.g., `.claude/skills/skill-name/`)
2. Read SKILL.md and analyze structure
3. Check against best practices
4. Provide detailed feedback with priorities

**Example review output**:
```
## Compliance Score
- Naming: ✓ Excellent - `processing-pdfs` (gerund form)
- Description: ⚠ Needs work - Missing "when to use"
- Size: ✓ Good - 234 lines

## Important Issues
- Add "Use when..." to description for better triggering
```

## Review Process

### Step 1: Initial Analysis

Read and analyze:
- SKILL.md (frontmatter and body)
- Directory structure
- Reference files (if any)
- Scripts/assets (if any)

### Step 2: Core Compliance Checks

**Naming** (gerund form preferred):
- ✓ Good: `processing-pdfs`, `analyzing-data`, `managing-workflows`
- ✗ Avoid: `helper`, `utils`, `tools`, `anthropic-*`, `claude-*`
- Requirements: max 64 chars, lowercase/numbers/hyphens only, no XML tags

**Description** (third person, what + when):
- ✓ Specific with key terms
- ✓ Includes both what it does and when to use it
- ✗ Vague ("helps with documents")
- Requirements: non-empty, max 1024 chars, no XML tags, third person only

**SKILL.md Size**:
- Target: <500 lines (ideally 200-400)
- If >500 lines: suggest moving content to references

**Progressive Disclosure**:
- Level 1: Metadata (name + description) always loaded
- Level 2: SKILL.md body loaded when triggered
- Level 3: References loaded as needed
- Check: Are details properly split into reference files?

**Single Responsibility**:
- Does skill focus on one clear purpose?
- Or does it try to be a multi-purpose helper?

**allowed-tools** (if present):
- ✗ Too broad: `Bash(git:*)` (includes destructive operations)
- ✓ Specific: `Bash(git status:*) Bash(git diff:*) Bash(git log:*)`
- ✗ Unnecessary: `Read`, `Glob` (already allowed by default)
- ✗ Dangerous: `Edit`, `Write`, `Bash(rm:*)` (destructive tools should not be pre-approved)
- Check: Are only non-destructive commands allowed?
- Check: Are subcommands specified explicitly?

### Step 3: Detailed Structure Review

**File Organization**:
- Required: SKILL.md, tests/scenarios.md
- Optional: README.md (human-facing), references/, scripts/, assets/
- Should NOT exist: CHANGELOG.md, INSTALLATION_GUIDE.md

**Reference Depth**:
- References should be one level deep from SKILL.md
- Avoid: SKILL.md → ref1.md → ref2.md (too nested)
- Good: SKILL.md → ref1.md, ref2.md, ref3.md

**Reference Files**:
- Files >100 lines should have table of contents
- **Check TOC presence**: If reference file >100 lines, verify table of contents exists at top
- Descriptive file names (not `doc1.md`, `misc.md`)
- Domain-specific organization when appropriate

**Content Quality**:
- Concise (only what Claude doesn't know)
- No time-sensitive information
- Consistent terminology
- Concrete examples
- Clear workflows

**Workflows and Validation** (see checklist.md for detailed criteria):
- [ ] Complex workflows include checklists for progress tracking
- [ ] Validation patterns used appropriately (plan-validate-execute, validate script, feedback loop)
- [ ] Validation scripts have clear, actionable error messages
- [ ] Workflows explain recovery steps when validation fails
- [ ] Validation level matches task risk (high-risk tasks should have validation)

**README.md** (optional but recommended):
- [ ] If exists, includes installation instructions and required permissions
- [ ] Explains file structure (especially `tests/scenarios.md` as self-evaluation scenarios)
- [ ] Clearly human-facing (not duplicating SKILL.md content)
- [ ] Provides overview and usage guidance

### Step 4: Generate Feedback

Organize feedback by priority:

**Critical Issues** (must fix):
- Name violates requirements
- Description missing or invalid
- SKILL.md >500 lines without good reason

**Important Issues** (should fix):
- Poor naming (not gerund form, too vague)
- Weak description (missing "when to use", too vague)
- Duplicate information between SKILL.md and references
- Deeply nested references
- Missing progressive disclosure
- Missing tests/scenarios.md (required for multi-model testing)

**Suggestions** (nice to have):
- Could be more concise
- Could improve examples
- Could reorganize for clarity
- Could add reference files for long sections

### Step 5: Provide Actionable Feedback

For each issue:
1. Explain the problem
2. Show why it matters
3. Suggest specific fix
4. Provide example if helpful

Format:
```markdown
## Critical Issues
- **Issue**: [Problem description]
  - **Why it matters**: [Impact explanation]
  - **Fix**: [Specific action]
  - **Example**: [If applicable]

## Important Issues
[Same format]

## Suggestions
[Same format]
```

## Output Format

Structure review with these sections:
- **Summary**: Overall assessment, key strengths, areas for improvement
- **Compliance Score**: Naming, Description, Size, Progressive Disclosure, Structure (each with ✓/⚠/✗)
- **Critical Issues**: Must fix (with explanations and fixes)
- **Important Issues**: Should fix (with explanations and fixes)
- **Suggestions**: Nice to have (with improvements)
- **Next Steps**: Prioritized actions

See [references/checklist.md](references/checklist.md) for detailed criteria.
