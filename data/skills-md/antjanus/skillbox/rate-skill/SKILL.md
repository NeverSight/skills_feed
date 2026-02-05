---
name: rate-skill
description: |
  Evaluate skill quality against best practices. Use when asked to "rate this skill", "review skill quality", "check skill formatting", "is this skill good", "evaluate SKILL.md", "grade this skill", or when validating skill files before publishing.
license: MIT
metadata:
  author: Antonin Januska
  version: "1.0.0"
  argument-hint: "<path/to/SKILL.md>"
tags: [quality, auditing, validation, skills]
---
# Rate Skill

## Overview

Audit SKILL.md files against quality standards from generate-skill best practices. Provides letter grade (A-F) and actionable recommendations.

**Core principle:** Measure skill quality objectively to improve activation reliability and context efficiency.

## When to Use

**Always use when:**
- Reviewing skills before publishing
- Validating skill structure and formatting
- Checking if skill meets quality standards
- User asks to "rate", "grade", or "review" a skill

**Useful for:**
- Skill authors validating their work
- Maintainers reviewing PRs with new skills
- Quality audits of skill repositories
- Before submitting skills to marketplaces

**Avoid when:**
- Evaluating non-skill documentation
- Reviewing code (not skill definitions)
- General code quality auditing

## How It Works

1. Read specified SKILL.md file
2. Evaluate against quality criteria
3. Calculate scores per category
4. Generate letter grade (A-F)
5. Output findings with priorities
6. Provide actionable recommendations

## Quality Criteria

| Category | Weight | Criteria |
|----------|--------|----------|
| **Length** | 20% | Under 500 lines (or progressive disclosure) |
| **Conciseness** | 20% | Clear, scannable, no fluff |
| **Repetitiveness** | 15% | No redundant content |
| **Structure** | 15% | Required sections present and ordered |
| **Triggers** | 15% | 3-5+ specific activation phrases |
| **Examples** | 10% | Good/Bad code comparisons |
| **Troubleshooting** | 5% | Common issues addressed |

### Length (20%)

**Scores:** A: <500 or progressive disclosure | B: 500-600 | C: 600-800 | D: 800-1000 | F: >1000

**Checks:** Line count, reference/ directory, progressive disclosure links

### Conciseness (20%)

**Scores:** A: High info density, scannable | B: Mostly concise | C: Some wordiness | D: Verbose | F: Excessive

**Red flags:** Long paragraphs (>5 sentences), redundant explanations, flowery language

### Repetitiveness (15%)

**Scores:** A: Zero redundancy | B: 1-2 overlaps | C: 3-4 overlaps | D: 5+ overlaps | F: Heavy redundancy

**Common:** Format in section AND example, repeated "use when", duplicate trigger phrases

### Structure (15%)

**Scores:** A: All required sections | B: Missing 1 optional | C: Missing 2-3 | D: Missing required | F: Severely lacking

**Required:** Frontmatter, Overview, When to Use, Main content, Examples (Good/Bad), Troubleshooting, Integration

### Triggers (15%)

**Scores:** A: 5+ specific | B: 3-4 good | C: 2 phrases | D: 1 vague | F: None

**Quality:** User language ("when asked to X"), specific situations, multiple contexts, concrete not abstract

### Examples (10%)

**Scores:** A: 3+ with Good/Bad | B: 2 with comparisons | C: 1 comparison | D: No comparisons | F: None

**Quality:** Uses tags, includes explanations, real scenarios, syntax highlighting

### Troubleshooting (5%)

**Scores:** A: 5+ pairs | B: 3-4 pairs | C: 1-2 basic | D: Vague | F: None

**Quality:** Clear problem, cause identified, solution with code, explanation

## Output Format

```markdown
# Skill Rating: [Letter Grade]

## Summary
- **File:** path/to/SKILL.md
- **Lines:** XXX lines
- **Overall Grade:** [A/B/C/D/F] ([Score]/100)
- **Status:** [Production Ready / Needs Work / Not Ready]

## Category Scores

| Category | Score | Grade | Status |
|----------|-------|-------|--------|
| Length | XX/20 | [A-F] | [✅/⚠️/❌] |
| Conciseness | XX/20 | [A-F] | [✅/⚠️/❌] |
| Repetitiveness | XX/15 | [A-F] | [✅/⚠️/❌] |
| Structure | XX/15 | [A-F] | [✅/⚠️/❌] |
| Triggers | XX/15 | [A-F] | [✅/⚠️/❌] |
| Examples | XX/10 | [A-F] | [✅/⚠️/❌] |
| Troubleshooting | XX/5 | [A-F] | [✅/⚠️/❌] |

## Findings by Priority

### ❌ Critical Issues (Fix Before Publishing)
1. [Issue description]
   - Impact: [Why this matters]
   - Fix: [Specific action to take]

### ⚠️ Important Issues (Should Fix)
1. [Issue description]
   - Impact: [Why this matters]
   - Fix: [Specific action to take]

### 📋 Recommendations (Nice to Have)
1. [Suggestion]
   - Benefit: [Why this helps]

## Strengths
- [What this skill does well]
- [Another strength]

## Recommendations
1. [Priority 1 action]
2. [Priority 2 action]
3. [Priority 3 action]

## Estimated Improvements
- Fix critical issues: +[X] points
- Address important issues: +[X] points
- Potential grade: [Current] → [Target]
```

## Usage

**Basic rating:**
```bash
/rate-skill skills/example-skill/SKILL.md
```

**Rate after changes:**
```bash
# Make improvements
[edit SKILL.md]

# Re-rate
/rate-skill skills/example-skill/SKILL.md
```

**Compare before/after:**
```bash
# Rate original
/rate-skill skills/track-session/SKILL.md

# Make improvements
[condense, remove redundancy]

# Rate again to see improvement
/rate-skill skills/track-session/SKILL.md
```

## Grading Scale

| Grade | Score | Meaning |
|-------|-------|---------|
| A | 90-100 | Excellent - Production ready |
| B | 80-89 | Good - Minor improvements recommended |
| C | 70-79 | Acceptable - Needs work before publishing |
| D | 60-69 | Poor - Significant issues to address |
| F | 0-59 | Failing - Major overhaul needed |

**Status mapping:**
- A-B: Production Ready ✅
- C: Needs Work ⚠️
- D-F: Not Ready ❌

## Examples

### Example 1: High-Quality Skill

**Input:**
```bash
/rate-skill skills/track-session/SKILL.md
```

**Output:**
```markdown
# Skill Rating: A

## Summary
- **File:** skills/track-session/SKILL.md
- **Lines:** 489 lines
- **Overall Grade:** A (92/100)
- **Status:** Production Ready ✅

## Category Scores

| Category | Score | Grade | Status |
|----------|-------|-------|--------|
| Length | 20/20 | A | ✅ |
| Conciseness | 18/20 | A | ✅ |
| Repetitiveness | 14/15 | A | ✅ |
| Structure | 15/15 | A | ✅ |
| Triggers | 15/15 | A | ✅ |
| Examples | 9/10 | A | ✅ |
| Troubleshooting | 5/5 | A | ✅ |

## Strengths
- Excellent progressive disclosure with reference/VERIFICATION.md
- Highly concise mode descriptions
- 10+ diverse trigger phrases
- Strong examples with Good/Bad comparisons
- Comprehensive troubleshooting (9 entries)

## Recommendations
1. Consider adding one more example for edge cases (optional)

## Estimated Improvements
- Already at A grade - no critical improvements needed
```

### Example 2: Needs Improvement

**Input:**
```bash
/rate-skill skills/problematic-skill/SKILL.md
```

**Output:**
```markdown
# Skill Rating: C

## Summary
- **File:** skills/problematic-skill/SKILL.md
- **Lines:** 742 lines
- **Overall Grade:** C (74/100)
- **Status:** Needs Work ⚠️

## Category Scores

| Category | Score | Grade | Status |
|----------|-------|-------|--------|
| Length | 14/20 | C | ⚠️ |
| Conciseness | 12/20 | D | ❌ |
| Repetitiveness | 9/15 | C | ⚠️ |
| Structure | 13/15 | B | ✅ |
| Triggers | 9/15 | C | ⚠️ |
| Examples | 8/10 | B | ✅ |
| Troubleshooting | 3/5 | C | ⚠️ |

## Findings by Priority

### ❌ Critical Issues
1. **Length: 742 lines without progressive disclosure**
   - Impact: High context usage, harder to scan
   - Fix: Move detailed content to reference/ directory

2. **Only 2 trigger phrases in description**
   - Impact: Poor activation reliability
   - Fix: Add 3-5 specific user phrases and situations

### ⚠️ Important Issues
1. **Verbose mode descriptions (30+ lines each)**
   - Impact: Reduced scannability
   - Fix: Condense to 2-3 lines per mode

2. **Redundant format in examples**
   - Impact: Wastes context tokens
   - Fix: Reference Format section instead of repeating

### 📋 Recommendations
1. Add 2-3 more troubleshooting entries
2. Improve paragraph breaks for scannability

## Strengths
- Good structure with required sections
- Examples use Good/Bad pattern correctly

## Recommendations
1. Implement progressive disclosure (move 200+ lines to reference/)
2. Add 3+ trigger phrases to description
3. Condense verbose sections
4. Remove redundant content

## Estimated Improvements
- Fix critical issues: +12 points → 86 (B)
- Address important issues: +4 points → 90 (A)
- Potential grade: C → A
```

## Troubleshooting

### Problem: Can't find SKILL.md file

**Cause:** Path incorrect or file doesn't exist.

**Solution:**
```bash
# Verify file exists
ls skills/skill-name/SKILL.md

# Use correct path
/rate-skill skills/skill-name/SKILL.md
```

### Problem: Rating seems too harsh

**Cause:** Standards are strict for good reason - quality matters for activation.

**Solution:**
- Review specific findings
- Compare to high-quality skills
- Focus on critical issues first
- Remember: B grade is still "good"

### Problem: Grade improved but still low

**Cause:** Multiple categories need attention.

**Solution:**
- Focus on highest-weight categories first (Length, Conciseness)
- Fix critical issues before nice-to-haves
- Re-rate after each major change
- Use "Estimated Improvements" as roadmap

### Problem: Don't know how to fix an issue

**Cause:** Fix recommendation unclear.

**Solution:**
- Check generate-skill examples for patterns
- Review high-rated skills for reference
- Ask for specific help on that issue
- Consult CLAUDE.md for SkillBox guidelines

## Integration

**This skill works with:**
- **generate-skill** - Use after generating to validate quality
- **Skill development workflow** - Rate before committing/publishing
- **Quality control** - Gate for accepting skills into repositories
- **Continuous improvement** - Track quality metrics over time

**Workflow:**
```bash
# Create skill
/generate-skill new-feature

# Rate it
/rate-skill skills/new-feature/SKILL.md

# Fix issues
[make improvements]

# Re-rate
/rate-skill skills/new-feature/SKILL.md

# When A or B grade, publish
git add skills/new-feature/
git commit -m "Add new-feature skill"
```

**Quality gates:**
- A-B: Merge to main ✅
- C: Request changes ⚠️
- D-F: Reject until improved ❌

## Scoring Algorithm

**Category scores:**
1. Length: Line count + progressive disclosure
2. Conciseness: Paragraph length + info density
3. Repetitiveness: Duplicate content detection
4. Structure: Section presence + organization
5. Triggers: Count + quality of trigger phrases
6. Examples: Count + Good/Bad presence
7. Troubleshooting: Entry count + completeness

**Weight application:**
```
Total = (Length × 0.20) + (Conciseness × 0.20) + (Repetitiveness × 0.15)
      + (Structure × 0.15) + (Triggers × 0.15) + (Examples × 0.10)
      + (Troubleshooting × 0.05)
```

**Grade assignment:**
- 90-100: A
- 80-89: B
- 70-79: C
- 60-69: D
- 0-59: F

## References

**Based on:**
- generate-skill best practices
- SkillBox CLAUDE.md guidelines
- obra/superpowers patterns
- Vercel agent-skills standards

**Related:**
- [generate-skill](../generate-skill/SKILL.md)
- [SkillBox CLAUDE.md](../../CLAUDE.md)
