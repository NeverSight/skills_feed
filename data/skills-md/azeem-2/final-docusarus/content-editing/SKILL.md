---
name: content-editing
description: Comprehensive editing checklist and procedures covering grammar and style rules, fact-checking, consistency verification, and readability metrics. Use when reviewing drafts, ensuring quality, or preparing content for publication.
version: 1.3.0
tags: [editing, grammar, style, fact-checking, consistency, quality-assurance, visual-formatting]
changelog:
  - 1.3.0 (2025-11-27): Dynamic Flesch targets by content type, contextual visual formatting rules
  - 1.2.0 (2025-11-27): Added Pass 5 (Visual Formatting Audit), expanded to six-pass system
  - 1.1.0 (2025-11-26): Expanded to five-pass system, added Grep examples, detailed templates
  - 1.0.0 (2025-11-26): Initial release optimized for rapid book editing
---

# Content Editing Skill

Systematic procedures for reviewing and improving book content to meet professional publication standards.

## When to Use This Skill

- Reviewing completed drafts for quality
- Checking grammar, style, and mechanics
- Verifying factual accuracy and citations
- Ensuring terminology and voice consistency
- Preparing content for final formatting
- Conducting multi-pass editorial reviews

## Editorial Workflow (Six-Pass System)

### Pass 1: Structural Review (Macro Level)

**Focus**: Document organization and architecture

**Checklist**:
- [ ] Document follows outline structure
- [ ] All sections have clear, distinct purposes
- [ ] Logical flow between sections
- [ ] Appropriate section lengths (no extreme outliers)
- [ ] Heading hierarchy consistent (H2 → H3 → H4, no skips)
- [ ] Chapter/section breakdown matches plan
- [ ] TOC-worthy headings properly formatted

**Questions to Ask**:
- Does each section serve a clear purpose?
- Are topics in the most logical order?
- Are any sections too long and need splitting?
- Are any sections too short and should be combined?

### Pass 2: Content Quality (Micro Level)

**Focus**: Sentence and paragraph quality

**Grammar & Mechanics**:
- [ ] Subject-verb agreement correct
- [ ] Verb tense consistent within sections
- [ ] Pronoun antecedents clear
- [ ] No sentence fragments (unless intentional)
- [ ] No run-on sentences
- [ ] No comma splices
- [ ] Proper punctuation throughout

**Clarity & Concision**:
- [ ] Every sentence has clear meaning
- [ ] No unnecessary words or phrases
- [ ] Complex ideas broken into manageable chunks
- [ ] Technical jargon defined or eliminated
- [ ] Ambiguous pronouns resolved

**Style & Voice**:
- [ ] Active voice predominates (target: >80%)
- [ ] Consistent perspective (you/we/one)
- [ ] Consistent tone (formal/balanced/conversational)
- [ ] Parallel structure in lists
- [ ] Varied sentence structure for rhythm

**Readability Assessment** (dynamic based on content type):
- [ ] Flesch Reading Ease appropriate for audience (see table below)
- [ ] Average sentence length matches complexity level
- [ ] Paragraph lengths appropriate (4-6 sentences typical)

| Content Type | Target Flesch | Sentence Length |
|--------------|---------------|-----------------|
| General audience | 65-80 | 12-18 words |
| Business/professional | 60-70 | 15-20 words |
| Introductory technical | 55-65 | 15-22 words |
| Advanced technical | 35-55 | 18-28 words |
| Specialized (ML, compilers) | 30-50 | 20-30 words |

> **📝 Note:** Lower Flesch scores are acceptable for advanced topics. The goal is clarity for the intended audience, not a universal threshold.

### Pass 3: Citation Verification (Accuracy Check)

**Focus**: Citation completeness and accuracy

**Citation Coverage**:
- [ ] Every factual claim has citation
- [ ] Every statistic cited
- [ ] Every direct quote cited
- [ ] Every date/historical fact cited
- [ ] Every technical specification cited

**Citation Format**:
- [ ] Consistent format throughout (APA/MLA/Chicago)
- [ ] In-text citations match reference list
- [ ] All citation elements present (author, year, title, source, URL, access date)
- [ ] Page numbers for quotes and specific claims

**Citation Quality**:
- [ ] Sources are authoritative (academic, reputable news, official docs)
- [ ] Sources are current (< 5 years unless historical)
- [ ] Multiple sources for major claims
- [ ] Primary sources used where possible

**Cross-Reference with Research**:
- [ ] Every cited source exists in research notes
- [ ] Source details match research documentation
- [ ] No "dead" citations (source cannot be located)

### Pass 4: Consistency Audit (Uniformity Check)

**Focus**: Terminology, style, and format uniformity

**Terminology Consistency** (Use Grep to identify variations):

```bash
# Check AI terminology consistency
grep -E "(AI|artificial intelligence|Artificial Intelligence|A.I.)" content/

# Check website spelling
grep -E "(web site|website|web-site)" content/

# Check hyphenation patterns
grep -E "(e-mail|email|Email)" content/
```

**Create Terminology Glossary**:

| Term | Approved Form | Avoid |
|------|---------------|-------|
| Artificial Intelligence | AI (after first mention) | A.I., artificial intelligence (subsequent) |
| Website | website | web site, web-site |
| Email | email | e-mail, E-mail |

**Style Guide Compliance**:
- [ ] Number style consistent (spell out 1-10 or always numerals)
- [ ] Date format consistent (Month Day, Year)
- [ ] Time format consistent (12-hour with am/pm or 24-hour)
- [ ] Oxford comma usage consistent
- [ ] Capitalization consistent (job titles, headings)
- [ ] Hyphenation consistent (compound modifiers, prefixes)

**Voice & Perspective**:
- [ ] Same perspective throughout (you/we/one)
- [ ] Same tone level maintained
- [ ] Same formality level

### Pass 5: Visual Formatting Audit

**Focus**: Ensuring content is visually engaging and properly formatted

> **📝 Note:** Visual formatting rules are contextual, not rigid. Technical content benefits from more frequent visual breaks; conceptual/philosophical content may flow better with fewer interruptions. The goal is **cognitive clarity**, not arbitrary quotas.

**Text Wall Detection** (contextual):
- [ ] Visual breaks inserted where they aid comprehension
- [ ] Technical content: more frequent breaks (code, tables, lists)
- [ ] Conceptual content: longer prose passages acceptable if flow is maintained
- [ ] Long explanations broken up with lists, callouts, or code blocks where helpful
- [ ] White space used effectively between logical groups

**Callout Box Verification**:
- [ ] Appropriate callouts per section (2-4 for technical, fewer for conceptual)
- [ ] Callout types match content (💡 for insights, ⚠️ for warnings, etc.)
- [ ] Callouts not overused (losing impact)
- [ ] Callout formatting consistent throughout

**Code Block Quality** (for technical content):
- [ ] All code blocks have language specification (```python, ```javascript, etc.)
- [ ] Code includes explanatory comments
- [ ] Code is properly indented and formatted
- [ ] No orphaned code without surrounding explanation

**Table Usage**:
- [ ] Tables used for comparisons and structured data
- [ ] Table headers are clear and descriptive
- [ ] Table formatting consistent (alignment, borders)
- [ ] No tables with only 1-2 rows (use list instead)

**List Formatting**:
- [ ] Bullet points for unordered items
- [ ] Numbered lists for sequential steps
- [ ] Parallel grammatical structure in list items
- [ ] List items have consistent punctuation

**Emphasis Consistency**:
- [ ] **Bold** used for key terms and emphasis
- [ ] *Italics* used for foreign terms and subtle emphasis
- [ ] `inline code` used for technical terms and commands
- [ ] No mixing of emphasis styles for same purpose

**Visual Diagram Review** (where applicable):
- [ ] ASCII diagrams properly aligned
- [ ] Diagrams have clear labels
- [ ] Complex relationships visualized, not just described

**Section Separators**:
- [ ] Horizontal rules (---) used between major sections
- [ ] Visual breathing room between topics
- [ ] Consistent separator usage throughout

**Common Visual Issues to Flag**:
```markdown
⚠️ TEXT WALL: [location] - Dense passage may benefit from visual break (consider context)
⚠️ MISSING CALLOUT: [section] - Key insight not highlighted (if appropriate for content type)
⚠️ UNSPECIFIED CODE: [line] - Code block missing language
⚠️ POOR TABLE: [location] - Consider converting to list
⚠️ INCONSISTENT EMPHASIS: [term] - Bold in some places, not others
⚠️ OVER-FORMATTED: [section] - Too many visual breaks disrupting narrative flow
```

---

### Pass 6: Factual Accuracy (Truth Verification)

**Focus**: Fact-checking against research sources

**Verification Requirements**:
- [ ] All statistics match source data exactly
- [ ] All quotes are verbatim (no paraphrasing in quotes)
- [ ] All dates and names spelled correctly
- [ ] All technical specifications accurate
- [ ] No unsupported generalizations

**Cross-Reference Method**:
1. Identify claim in draft
2. Locate cited source in research notes
3. Verify claim matches source exactly
4. Check for context (is claim misrepresented?)
5. Flag discrepancies for writer review

**Confidence Levels**:
- **High**: 3+ authoritative sources agree
- **Medium**: 2 sources agree, or 1 highly authoritative source
- **Low**: Single source of moderate authority
- **Unverified**: No source found or sources conflict

Flag Low/Unverified claims for additional research.

## Grammar and Style Rules Reference

### Common Grammar Errors

**Subject-Verb Agreement**:
- Wrong: "The team of editors review drafts."
- Correct: "The team of editors reviews drafts."

**Comma Splices**:
- Wrong: "The edit is complete, the draft is ready."
- Correct: "The edit is complete; the draft is ready."

**Misplaced Modifiers**:
- Wrong: "She only edited three chapters."
- Correct: "She edited only three chapters."

### Style Preferences (Configurable per Project)

**Numbers**: Spell out 1-10, numerals for 11+ (or choose consistent alternative)
**Dates**: Month Day, Year (January 15, 2025)
**Oxford Comma**: Choose one style and apply consistently
**Hyphenation**: Compound modifiers before noun hyphenate, after noun no hyphen
**Capitalization**: Job titles capitalize before name, lowercase after

## Readability Metrics

### Flesch Reading Ease Score

**Score Interpretation**:
- **90-100**: Very Easy (5th grade) - Children's books
- **80-89**: Easy (6th grade) - Conversational writing
- **70-79**: Fairly Easy (7th grade) - General audience
- **60-69**: Standard (8th-9th grade) - Business writing
- **50-59**: Fairly Difficult (10th-12th grade) - Academic
- **40-49**: Difficult - Advanced technical
- **30-39**: Very Difficult - Highly specialized (compilers, physics, ML theory)
- **Below 30**: Expert only - Mathematical proofs, research papers

**Target for Book Generation** (dynamic by content type):

| Content Type | Target Flesch | Acceptable Range |
|--------------|---------------|------------------|
| General audience | 65-80 | 60-85 |
| Business/professional | 60-70 | 55-75 |
| Introductory technical | 55-65 | 50-70 |
| Intermediate technical | 45-60 | 40-65 |
| Advanced technical | 35-55 | 30-60 |
| Specialized/theoretical | 30-50 | 25-55 |

> **⚠️ Warning:** Do NOT force higher Flesch scores on advanced technical content. Simplifying specialized terminology can reduce precision and accuracy. The goal is **appropriate clarity for the intended audience**.

**When to Improve Score** (general audience only):
- Shorten sentences (< 20 words average)
- Use simpler words (fewer syllables)
- Break complex sentences into multiple sentences
- Replace jargon with plain language

**When NOT to Simplify** (technical content):
- Technical terminology is necessary for precision
- Audience expects domain vocabulary
- Simplification would lose meaning or accuracy

### Passive Voice Percentage

**Target**: < 20%

**Detection Pattern**: [form of "to be"] + [past participle]

**How to Fix**:
1. Identify actor: WHO performs the action?
2. Rewrite with actor as subject
   - Passive: "The draft was reviewed by the editor."
   - Active: "The editor reviewed the draft."

## Edit Summary Report Template

```markdown
# Edit Summary: [Document Title]

**Edited**: [YYYY-MM-DD]
**Word Count**: [original] → [revised] ([+/- change])
**Total Changes**: [number]

## Changes by Category

### Grammar & Mechanics: [count]
### Citations: [count]
### Clarity & Flow: [count]
### Consistency: [count]
### Visual Formatting: [count]
### Factual Corrections: [count]

## Quality Metrics

| Metric | Before | After | Target | Status |
|--------|--------|-------|--------|--------|
| Flesch Reading Ease | [score] | [score] | [per content type] | ✅/❌ |
| Citation Coverage | [%] | [%] | 100% | ✅/❌ |
| Passive Voice % | [%] | [%] | <20% | ✅/❌ |
| Avg Sentence Length | [words] | [words] | [per content type] | ✅/❌ |
| Text Walls Fixed | [count] | 0 | 0 | ✅/❌ |
| Callouts Per Section | [avg] | [avg] | 2-4 | ✅/❌ |
| Code Blocks w/ Language | [%] | [%] | 100% | ✅/❌ |

**Content Type**: [general/business/intro-tech/advanced-tech/specialized]

## Visual Formatting Summary
- **Callouts added**: [count] (💡: [n], ⚠️: [n], 🎯: [n], etc.)
- **Tables created**: [count]
- **Lists converted**: [count] (from run-on sentences)
- **ASCII diagrams added**: [count]
- **Text walls broken up**: [count]

## Issues Requiring Author Review
- [Unverifiable claims, technical accuracy questions]

## Recommendations
- [Patterns to watch in future writing]
```

## Common Editing Pitfalls

1. **Over-Editing**: Edit for correctness and clarity, not personal preference
2. **Missing Context**: Read surrounding paragraphs before making changes
3. **Inconsistent Application**: Use Grep to find ALL instances, apply rule uniformly
4. **Citation Overload**: Distinguish common knowledge from factual claims
5. **Ignoring Readability**: Balance formal correctness with reader comprehension

## Quality Assurance

Before marking edit complete:
- [ ] All six editorial passes completed
- [ ] 100% citation coverage verified
- [ ] Readability target achieved (Flesch > 60)
- [ ] Consistency issues resolved
- [ ] Visual formatting standards met
- [ ] Edit summary report generated
- [ ] Flagged issues documented for author

---

**Skill Version**: 1.3.0
**Last Updated**: 2025-11-27
**Maintained By**: Universal Pedagogical Engine Team
