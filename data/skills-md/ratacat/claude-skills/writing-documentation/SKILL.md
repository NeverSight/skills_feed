---
name: writing-documentation
description: Produces concise, clear documentation by applying Elements of Style principles. Use when writing or improving any technical documentation (READMEs, guides, API docs, architecture docs). Not for code comments.
---

# Writing Documentation Skill

Apply Strunk & White's *Elements of Style* principles to produce concise, clear technical documentation.

## When to Use This Skill

**Use this skill when:**
- Writing new documentation (README, API docs, guides, tutorials, architecture docs)
- Improving existing documentation
- Reviewing documentation for quality
- User asks to "make this more concise" or "improve clarity"
- User mentions: documentation, docs, README, guide, tutorial, API docs

**Do NOT use this skill for:**
- Code comments (different context, separate skill needed)
- Marketing copy (requires persuasive voice, not neutral clarity)
- Personal blog posts (requires individual voice)

## Workflows

### Workflow 1: Write New Documentation

**Steps:**

1. **Understand the purpose**
   - [ ] What is the primary goal of this documentation?
   - [ ] Who is the target audience?
   - [ ] What do readers need to accomplish after reading?

2. **Load writing principles**
   - [ ] Read `reference/strunk-white-principles.md` to internalize core principles

3. **Determine documentation type**
   - [ ] Read `reference/doc-types.md` to select appropriate type
   - [ ] Identify essential sections based on guidelines

4. **Draft the documentation**
   - [ ] Apply Strunk & White principles while writing

5. **Validate quality**
   - [ ] Run through Quality Checklist (below)
   - [ ] Verify all essential information is present
   - [ ] Confirm document achieves its purpose

### Workflow 2: Improve Existing Documentation

**Steps:**

1. **Read the current documentation**
   - [ ] Understand its purpose and audience
   - [ ] Note specific problems (verbosity, unclear sections, missing info)

2. **Load writing principles**
   - [ ] Read `reference/strunk-white-principles.md`
   - [ ] Review `reference/examples.md` for before/after patterns

3. **Apply improvements**
   - [ ] Remove needless words
   - [ ] Convert passive to active voice
   - [ ] Strengthen vague statements
   - [ ] Eliminate redundancy
   - [ ] Improve organization if needed

4. **Validate improvements**
   - [ ] Run through Quality Checklist
   - [ ] Verify no information was lost
   - [ ] Confirm clarity improved

### Workflow 3: Review Documentation

**Steps:**

1. **Load writing principles**
   - [ ] Read `reference/strunk-white-principles.md`
   - [ ] Review relevant guidelines in `reference/doc-types.md`

2. **Assess against quality criteria**
   - [ ] Run through Quality Checklist (below)
   - [ ] Note specific violations with examples

3. **Provide feedback**
   - [ ] List specific issues found
   - [ ] Reference violated principles
   - [ ] Suggest concrete improvements

## Decision Framework

### When to Write vs Improve

**Write new documentation when:**
- No documentation exists
- Existing documentation is fundamentally wrong or outdated
- Complete restructuring needed (cheaper to rewrite)

**Improve existing documentation when:**
- Core structure and information are sound
- Style or clarity issues can be fixed incrementally
- Specific sections need enhancement

### Choosing Documentation Type

See `reference/doc-types.md` for detailed guidelines. Quick reference:

- **README**: Project overview, quick start, primary entry point
- **API Documentation**: Reference for function/endpoint signatures and behavior
- **Tutorial/Guide**: Step-by-step learning path for accomplishing specific goals
- **Architecture/Design Doc**: Explain system structure, decisions, and tradeoffs
- **CLI Tool Documentation**: Command reference with options and examples

### Prioritizing Conciseness vs Comprehensiveness

**Prioritize conciseness when:**
- Documentation type is reference (README, API docs, CLI docs)
- Readers need to scan quickly
- Getting started / quick start sections

**Prioritize comprehensiveness when:**
- Documentation type is learning-focused (tutorials, guides)
- Complex concepts require detailed explanation
- Architecture decisions need thorough justification

**Balance both:**
- Use concise overview sections with detailed subsections
- Link to comprehensive resources rather than embedding everything
- Apply progressive disclosure pattern

## Quality Checklist

### Content
- [ ] Purpose is clear
- [ ] Essential information is present
- [ ] No unnecessary information
- [ ] Correct and accurate

### Writing (Core Principles)
- [ ] Active voice predominates
- [ ] Definite statements (not hedging)
- [ ] Positive form
- [ ] Specific, concrete language
- [ ] Concise (no needless words)

### Structure
- [ ] Logical organization
- [ ] Clear headings
- [ ] Scannable
- [ ] Examples where helpful

### Technical Documentation
- [ ] Code examples are executable
- [ ] Commands include full context
- [ ] Prerequisites are stated
- [ ] Error cases are covered

## Reference Files

### When to Load Each Reference

**Load `reference/strunk-white-principles.md`:**
- At the start of EVERY documentation writing/improvement task
- When reviewing documentation

**Load `reference/doc-types.md`:**
- When choosing what type of documentation to write
- When unsure about essential sections for a doc type
- When reviewing documentation structure

**Load `reference/examples.md`:**
- When improving existing documentation (see patterns)
- When you want concrete before/after examples

## Common Pitfalls

**Skipping Principle Loading**: ALWAYS load `reference/strunk-white-principles.md` before writing.

**Following Guidelines Rigidly**: Adapt to the specific project's needs. Some projects don't need all sections; some need additional ones.

**Over-Editing**: "Omit needless words" means remove words that add no value. Keep all information that serves the reader's purpose.

**Sacrificing Accuracy for Brevity**: Accuracy always wins. Express explanations concisely, but never misleadingly.

**Inconsistent Terminology**: Choose one term for each concept and use it consistently.

## Notes

- This skill works iteratively - you can run it multiple times on the same document without degrading quality (idempotent)
- Quality over quantity - a short, clear document is better than a comprehensive, confusing one
