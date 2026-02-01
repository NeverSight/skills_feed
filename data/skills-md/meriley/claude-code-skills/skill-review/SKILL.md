---
name: skill-review
description: Audit Claude Code skills against quality criteria including structure, descriptions, content clarity, testing, and best practices compliance. Use when reviewing skills before release or during PR reviews.
version: 1.0.0
---

# Skill Review

## Purpose

Systematically audit Claude Code skills against official best practices to ensure quality, discoverability, and maintainability before release or merge.

## Review Workflow

### Step 1: Structure Validation

Check the basic structural requirements:

```bash
# Navigate to skill directory
cd ~/.claude/skills/skill-name

# Verify file structure
ls -la
# Expected:
# - Skill.md (capital S)
# - REFERENCE.md (optional, all caps)
# - TEMPLATE.md (optional, all caps)
# - scripts/ (optional, lowercase)
```

**Validation checklist:**

- [ ] Directory name matches skill name
- [ ] Directory name uses gerund form (verb + -ing)
- [ ] Directory name lowercase-with-hyphens
- [ ] Skill.md exists (capital S, not skill.md)
- [ ] Supporting files use ALL CAPS (REFERENCE.md, not reference.md)
- [ ] No deeply nested directories
- [ ] No files with underscores or wrong extensions

### Step 2: Frontmatter Audit

Validate YAML frontmatter quality:

```bash
# Extract frontmatter
head -n 10 Skill.md
```

**Validation checklist:**

- [ ] Has valid YAML frontmatter (between --- markers)
- [ ] `name` field present and matches directory name
- [ ] `name` uses gerund form (verb + -ing)
- [ ] `name` max 64 characters
- [ ] `name` lowercase-with-hyphens only
- [ ] `description` field present
- [ ] `description` in third person (not first/second)
- [ ] `description` includes specific capabilities
- [ ] `description` includes WHEN to use triggers
- [ ] `description` includes key terms for discovery
- [ ] `description` max 1024 characters
- [ ] `description` avoids vague language
- [ ] `version` field present in SemVer format (X.Y.Z)
- [ ] `dependencies` field if external packages needed

**Common frontmatter issues:**

```yaml
# ❌ BLOCKER: First person
description: I can help you process PDFs...

# ❌ BLOCKER: Second person
description: You can use this to extract text...

# ❌ CRITICAL: Too vague
description: Helps with documents.

# ❌ CRITICAL: No triggers
description: Processes PDF files efficiently.

# ✅ GOOD: Third person, specific, with triggers
description: Extract text, tables, and forms from PDF files including scanned documents. Use when working with PDFs or document extraction tasks.
```

### Step 3: Content Quality Check

Review the main skill content:

```bash
# Check file length
wc -l Skill.md
# Should be under 500 lines for optimal performance
```

**Core content validation:**

- [ ] Main file under 500 lines
- [ ] Has clear "Purpose" section
- [ ] Has "When to Use" section with specific scenarios
- [ ] Has structured workflow or quick start
- [ ] Provides 2-3 concrete examples minimum
- [ ] Uses consistent terminology throughout
- [ ] Avoids general knowledge Claude already has
- [ ] Provides ONE default approach (not too many options)
- [ ] Includes validation/verification steps
- [ ] Has troubleshooting section for common issues
- [ ] Uses progressive disclosure (details in reference files)
- [ ] Reference files are one level deep only
- [ ] No time-sensitive information
- [ ] No marketing language or vague confidence claims

**Progressive disclosure validation:**

- [ ] SKILL.md under 500 lines (target: under 300 for complex skills)
- [ ] Uses references/ directory for detailed content
- [ ] Detailed workflows extracted to references/WORKFLOW-STEPS.md
- [ ] Troubleshooting content in references/TROUBLESHOOTING.md
- [ ] Templates/examples in references/TEMPLATE-EXAMPLES.md
- [ ] Domain-specific checks in references/[DOMAIN]-CHECKS.md
- [ ] No nested references (SKILL.md → references/A.md only)
- [ ] Clear loading guidance format:
  ```markdown
  **For detailed [topic]:**
  \`\`\`
  Read `~/.claude/skills/[skill]/references/FILE.md`
  \`\`\`
  Use when: [specific scenario]
  ```
- [ ] Each reference has "Use when:" context
- [ ] Reference files are standalone (no cross-references)

**Example quality validation:**

- [ ] At least 2-3 concrete examples provided
- [ ] Examples show input AND expected output
- [ ] Code examples are complete (not pseudocode)
- [ ] Examples cover common use cases
- [ ] Examples include validation steps

### Step 4: Instruction Clarity Audit

Verify instructions are clear and actionable:

**Sequential workflows:**

- [ ] Steps numbered clearly (Step 1, Step 2, etc.)
- [ ] Each step has concrete action
- [ ] Code blocks show exact commands
- [ ] Expected outputs documented
- [ ] Validation checkpoints provided

**Example pattern:**

```markdown
### Step 1: Validate Input

\`\`\`bash

# Check file exists

test -f document.pdf || echo "File not found"
\`\`\`

### Step 2: Extract Text

\`\`\`python
import pdfplumber
with pdfplumber.open('document.pdf') as pdf:
text = pdf.pages[0].extract_text()
\`\`\`

### Step 3: Verify Output

Expected format:
\`\`\`json
{
"pages": 5,
"text": "extracted content..."
}
\`\`\`
```

**Terminology consistency:**

- [ ] Same concept uses same term throughout
- [ ] No switching between synonyms
- [ ] Terms defined before use
- [ ] Technical terms used correctly

### Step 5: Testing Verification

Validate testing and evaluation quality:

**Testing checklist:**

- [ ] Has evaluations or test cases
- [ ] At least 3 test scenarios created
- [ ] Tests cover common use cases
- [ ] Tests cover edge cases
- [ ] Tested with fresh Claude instances
- [ ] Tested across multiple models (Haiku, Sonnet, Opus)
- [ ] Real-world validation completed
- [ ] Team feedback incorporated

**Code quality (if applicable):**

- [ ] Scripts have explicit error handling
- [ ] Configuration values commented (WHY, not WHAT)
- [ ] Required packages available and version-specified
- [ ] Forward slashes in all paths (not backslashes)
- [ ] Validation for critical operations
- [ ] No hardcoded credentials or secrets

## Severity Levels

Use these severity levels to prioritize issues:

### BLOCKER (Must fix before release)

- First/second person in description
- Skill.md over 750 lines
- No description or completely vague
- No examples provided
- Missing critical frontmatter fields
- Broken/invalid YAML
- Skill name doesn't match directory
- Major structural issues

### CRITICAL (Should fix before release)

- Description missing key triggers
- Skill.md 500-750 lines (over recommended)
- Fewer than 2 examples
- Deeply nested references (>1 level)
- Inconsistent terminology
- Too many options without default
- Missing validation steps
- No testing performed

### MAJOR (Should fix soon)

- Description could be more specific
- Missing troubleshooting section
- Examples lack expected outputs
- No progressive disclosure
- Includes general knowledge Claude has
- Missing error handling in scripts
- No version number in dependencies
- Inconsistent file naming

### MINOR (Nice to have)

- Could add more examples
- Could improve comments
- Could add table of contents
- Could extract more to reference files
- Could add more test scenarios

## Review Report Template

```markdown
# Skill Review: [skill-name]

**Reviewer:** [name]
**Date:** [YYYY-MM-DD]
**Version Reviewed:** [X.Y.Z]

## Summary

[1-2 sentences on overall quality]

**Recommendation:** [PASS | NEEDS WORK | FAIL]

## Findings by Category

### Structure [PASS/FAIL]

- [ ] Directory structure correct
- [ ] File naming conventions followed
- [ ] Under 500 lines

**Issues:**

- [SEVERITY] Issue description
- [SEVERITY] Issue description

### Frontmatter [PASS/FAIL]

- [ ] Valid YAML
- [ ] All required fields present
- [ ] Description quality

**Issues:**

- [SEVERITY] Issue description

### Content Quality [PASS/FAIL]

- [ ] Clear purpose and workflows
- [ ] Concrete examples provided
- [ ] Progressive disclosure used
- [ ] Consistent terminology

**Issues:**

- [SEVERITY] Issue description

### Instruction Clarity [PASS/FAIL]

- [ ] Clear sequential steps
- [ ] Code examples complete
- [ ] Validation steps included

**Issues:**

- [SEVERITY] Issue description

### Testing [PASS/FAIL]

- [ ] Test scenarios created
- [ ] Fresh instance testing done
- [ ] Multi-model testing done

**Issues:**

- [SEVERITY] Issue description

## Blockers (must fix)

1. [Issue]
2. [Issue]

## Critical Issues (should fix)

1. [Issue]
2. [Issue]

## Major Issues (fix soon)

1. [Issue]
2. [Issue]

## Minor Issues (nice to have)

1. [Issue]
2. [Issue]

## Positive Highlights

- [What the skill does well]
- [What the skill does well]

## Recommendations

1. [Specific actionable recommendation]
2. [Specific actionable recommendation]

## Next Steps

- [ ] Address blockers
- [ ] Address critical issues
- [ ] Re-review after fixes
- [ ] Approve for merge
```

## Anti-Pattern Detection

Watch for these common anti-patterns:

### Anti-Pattern: Too Many Options

**Problem:**

```markdown
You can use pypdf, pdfplumber, PyMuPDF, pdf2image, camelot, tabula,
or pytesseract depending on your needs. Each has pros and cons...
[200 lines comparing libraries]
```

**Solution:**

```markdown
Use pdfplumber for text and tables. For scanned PDFs, use pytesseract with pdf2image.
See REFERENCE.md for alternative libraries.
```

### Anti-Pattern: General Knowledge

**Problem:**

```markdown
## Python Basics

Python is a programming language. To install Python, visit python.org...
[100 lines of Python installation]
```

**Solution:**

```markdown
# Remove entirely - Claude already knows this
```

### Anti-Pattern: Vague Instructions

**Problem:**

```markdown
1. Do the thing
2. Check if it worked
3. Fix any issues
```

**Solution:**

```markdown
### Step 1: Extract Text

\`\`\`python
import pdfplumber
with pdfplumber.open('document.pdf') as pdf:
text = pdf.pages[0].extract_text()
\`\`\`

### Step 2: Validate Extraction

\`\`\`python
assert text is not None, "Extraction failed"
assert len(text) > 0, "Empty result"
\`\`\`
```

### Anti-Pattern: Nested References

**Problem:**

```
Skill.md → REFERENCE.md → ADVANCED.md → EXPERT.md
```

**Solution:**

```
Skill.md → REFERENCE.md
Skill.md → ADVANCED.md
Skill.md → EXPERT.md
```

### Anti-Pattern: Bloated Main File

**Problem:**

```
Skill.md: 1,247 lines
```

**Solution:**

```
Skill.md: 342 lines
REFERENCE.md: 400 lines (detailed API)
EXAMPLES.md: 300 lines (additional examples)
TEMPLATE.md: 205 lines (output templates)
```

## Quality Gates

Skills should pass these gates before release:

### Gate 1: Structure ✅

- Directory/file naming correct
- Frontmatter valid and complete
- Under 500 lines

### Gate 2: Description ✅

- Third person
- Specific capabilities
- Clear triggers
- Key terms included

### Gate 3: Content ✅

- Clear purpose and workflows
- 2-3 concrete examples
- One default approach
- Validation steps

### Gate 4: Clarity ✅

- Sequential steps
- Complete code examples
- Expected outputs
- Troubleshooting section

### Gate 5: Testing ✅

- Test scenarios created
- Fresh instance testing
- Multi-model validation

## Quick Reference

```bash
# Run full review
1. Check structure (file naming, organization)
2. Validate frontmatter (YAML, description quality)
3. Audit content (length, examples, clarity)
4. Verify instructions (workflows, code, validation)
5. Check testing (scenarios, coverage, feedback)
6. Generate report with severity levels
7. Provide actionable recommendations

# Pass criteria
- All BLOCKERS resolved
- All CRITICAL issues resolved
- At least 80% of MAJOR issues resolved
- Clear path to resolve remaining issues
```

## Resources

- [Skill Best Practices](/Users/mriley/.claude/skills/skill-writing/Skill.md)
- [Review Checklist](CHECKLIST.md)
- [Example Reviews](EXAMPLES.md)
- [Official Documentation](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/best-practices)
