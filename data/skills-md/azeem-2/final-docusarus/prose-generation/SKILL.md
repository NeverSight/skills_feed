---
name: prose-generation
description: Guidelines for generating coherent book prose including voice and tone, paragraph structure, transition techniques, and chapter flow patterns. Use when writing book content, structuring chapters, or maintaining narrative consistency.
version: 1.3.0
tags: [writing, prose, chapters, voice, tone, flow, transitions, visual-formatting]
changelog:
  - 1.3.0 (2025-11-27): Dynamic Flesch targets, contextual visual formatting, realistic timeline expectations
  - 1.2.0 (2025-11-27): Added Visual Formatting Standards section with callouts, tables, diagrams
  - 1.1.0 (2025-11-26): Removed examples, shortened descriptions for agent consumption
  - 1.0.0 (2025-11-26): Initial release optimized for rapid book generation
---

# Prose Generation Skill

Practical guidelines for writing clear, engaging book prose with consistent voice and logical flow, optimized for 1-week book generation timelines.

## When to Use This Skill

- Drafting new book chapters or sections
- Revising content for clarity and flow
- Ensuring voice and tone consistency across chapters
- Creating effective transitions between ideas
- Structuring chapter narratives for coherence
- Maintaining readability and engagement

## Voice and Tone Guidelines

### Perspective Selection

**Choose ONE perspective and maintain throughout the entire book**:

1. **Second Person ("You")**
   - Use for: Instructional, how-to, self-help, tutorials, practical guides
   - Effect: Direct, engaging, immediate connection
   - Readability: High (Flesch 70-80)

2. **First Person Plural ("We")**
   - Use for: Collaborative learning, exploration, inclusive teaching
   - Effect: Partnership with reader, shared journey
   - Readability: Medium-High (Flesch 65-75)

3. **Third Person ("Readers", "One", "People")**
   - Use for: Academic, formal, general audience non-fiction, objective analysis
   - Effect: Professional, objective, universal
   - Readability: Medium (Flesch 55-65)

**CRITICAL**: Never mix perspectives within a book. Decide in planning phase.

### Tone Spectrum

**Conversational** (Flesch 70-80):
- Use contractions (can't, won't, it's)
- Short sentences (12-18 words average)
- Active voice (90%+)
- Best for: Popular non-fiction, self-help, general audience

**Balanced** (Flesch 60-70):
- Selective contractions (natural speech patterns only)
- Mixed sentence length (15-22 words average)
- Active voice (80%+)
- Best for: Business books, technical writing for non-experts

**Formal** (Flesch 50-60):
- No contractions
- Longer sentences (20-28 words average)
- Active voice (70%+)
- Best for: Academic writing, scholarly works, technical treatises

**Advanced Technical** (Flesch 35-55):
- Technical vocabulary expected and necessary
- Complex sentence structures for precise meaning
- Active voice (60%+)
- Best for: Compilers, neural networks, quantum computing, advanced mathematics

> **📝 Note:** Flesch scores are guidelines, not rigid requirements. Advanced topics naturally require lower scores due to specialized terminology. **Prioritize clarity for your target audience over hitting a specific number.**

### Technical Level Calibration

- **General Audience**: Define all specialized terms, use analogies, assume no prior knowledge (Flesch 65-80)
- **Intermediate**: Assume foundational knowledge, define advanced concepts only (Flesch 55-70)
- **Expert**: Use technical vocabulary freely, reference shared knowledge base (Flesch 35-60)

**First Mention Rule**: Always define specialized terms on first use with parenthetical abbreviation if applicable.

### Dynamic Readability Adjustment

Flesch targets should adapt to content complexity:

| Content Type | Target Flesch | Rationale |
|--------------|---------------|-----------|
| Self-help, general how-to | 70-80 | Broad accessibility |
| Business, productivity | 60-70 | Professional but accessible |
| Introductory technical | 55-65 | Some terminology expected |
| Intermediate technical | 45-60 | Precision matters |
| Advanced technical | 35-55 | Necessary complexity |
| Highly specialized (math, physics, theory) | 30-50 | Domain expertise assumed |

**The goal is comprehension by the intended audience, not a universal score.**

## Paragraph Structure Rules

### Standard Paragraph Pattern

**4-Part Structure** (use for 80% of paragraphs):

1. **Topic Sentence**: State the paragraph's main idea clearly and directly
2. **Supporting Details**: Provide 2-4 sentences with evidence, examples, or explanation
3. **Analysis**: Explain significance, implications, or connections to broader themes
4. **Transition**: Connect to next paragraph (explicit or implicit bridge)

### Paragraph Length Guidelines

- **Short** (2-3 sentences): Emphasis, transitions, dramatic effect, chapter breaks
- **Standard** (4-6 sentences): Default for most content—80% of paragraphs
- **Long** (7-9 sentences): Complex ideas requiring extended explanation—use sparingly

**Avoid**:
- Single-sentence paragraphs (except for strategic emphasis)
- Paragraphs exceeding 10 sentences (always split into multiple paragraphs)
- Long unbroken blocks of text (readers lose focus)

### Sentence Structure Variation

**Create rhythm through length variation**:

- **Short** (5-12 words): Impact, emphasis, dramatic effect
- **Medium** (13-25 words): Standard explanation and description
- **Long** (26-40 words): Complex synthesis, multi-part ideas

**Target Average**: 15-20 words per sentence

**Rhythm Rule**: Never write more than 3 consecutive sentences of similar length.

## Transition Techniques

### Between Sentences (Micro-Transitions)

1. **Pronoun Reference**: Use pronouns to refer back to subjects from previous sentence
2. **Repetition of Key Terms**: Repeat important terms from previous sentence in new sentence
3. **Transitional Words and Phrases**:

| Purpose | Transitions |
|---------|-------------|
| **Addition** | furthermore, moreover, additionally, also, besides, in addition |
| **Contrast** | however, nevertheless, conversely, on the other hand, in contrast, yet |
| **Cause/Effect** | therefore, consequently, as a result, thus, hence, accordingly |
| **Example** | for instance, specifically, namely, such as, for example, to illustrate |
| **Time** | subsequently, previously, meanwhile, simultaneously, finally, next |
| **Emphasis** | indeed, in fact, notably, significantly, especially, particularly |

**Use sparingly**: No more than 30% of sentences should start with transitional words.

### Between Paragraphs (Macro-Transitions)

1. **Explicit Transition Sentences**: Use transitional words to connect ideas
2. **Question-Answer Pattern**: End paragraph with question, begin next with answer
3. **Bridge Sentences**: Final sentence of paragraph A connects to opening of paragraph B
4. **Thematic Echo**: Repeat key phrase from previous paragraph in opening of next

### Between Sections (Chapter Architecture)

**Section Summary + Preview Pattern**: End section with brief summary, begin next section with preview of what's coming

## Chapter Flow Patterns

### Chapter Opening Strategies

Choose ONE approach per chapter:

1. **Anecdotal Hook**: Start with compelling story or scenario
2. **Problem Statement**: Open with clear question or problem
3. **Bold Claim**: Begin with provocative statement
4. **Statistical Impact**: Lead with compelling data

### Chapter Body Architecture

**Standard 5-Part Structure**:

1. **Introduction** (2-3 paragraphs): Context, scope, chapter roadmap
2. **Main Content** (3-7 sections): Core concepts with supporting evidence
3. **Synthesis** (1-2 paragraphs): Connect ideas across sections
4. **Practical Application** (1-2 paragraphs, optional): Real-world examples
5. **Conclusion** (1-2 paragraphs): Key takeaways, bridge to next chapter

**Section Count Guidelines**:
- **Introductory chapters**: 3-4 sections
- **Core content chapters**: 5-7 sections
- **Synthesis chapters**: 2-4 sections
- **Concluding chapters**: 2-3 sections

### Chapter Closing Strategies

1. **Summary + Forward Bridge**: Summarize key points, preview next chapter
2. **Reflective Question**: End with thought-provoking question
3. **Full Circle Callback**: Reference opening and show how chapter addressed it

## Maintaining Narrative Consistency

### Voice Consistency Protocol

**Establish in Planning Phase**:
- Perspective choice (you/we/readers/one)
- Tone level (conversational/balanced/formal)
- Technical complexity (general/intermediate/expert)
- Contraction usage (yes/selective/no)
- Average sentence length target

**Check Every Section**:
- Perspective maintained
- Tone consistent with target Flesch score
- Technical terms defined on first use
- Contraction usage matches established pattern

### Terminology Management

**Rules**:
1. Choose ONE term for each concept
2. Define on first use with parenthetical abbreviation
3. Use consistently throughout book
4. Track in term registry to avoid drift

### Style Consistency Rules

**Numbers**: Spell out one through ten, numerals for 11+
**Dates**: Month Day, Year (January 15, 2025)
**Lists**: Parallel grammatical structure, consistent punctuation
**Acronyms**: Spell out on first use, abbreviate thereafter

## Visual Formatting Standards (Mandatory)

Content MUST be visually engaging. Plain text walls reduce comprehension and reader engagement. Apply these formatting elements throughout all prose.

### Callout Boxes

Use blockquote-based callouts to highlight important information:

```markdown
> **💡 Key Insight:** [Important realization that deepens understanding]

> **⚠️ Warning:** [Critical information about potential problems or mistakes]

> **🎯 Core Concept:** [Fundamental idea the reader must understand]

> **🔧 Practical Tip:** [Actionable advice for real-world application]

> **📝 Note:** [Additional context or clarification]

> **🧠 Remember:** [Information worth memorizing or internalizing]

> **📖 Definition:** [Formal definition of a key term]
```

**Usage Guidelines:**
- Include 2-4 callouts per major section
- Don't overuse—callouts lose impact if every paragraph has one
- Match callout type to content purpose

### Code Blocks (for Technical Content)

**Always specify the language** for syntax highlighting:

```markdown
```python
def example_function():
    return "Always specify language"
```
```

**Add explanatory comments** in code:

```markdown
```python
# Step 1: Initialize the connection
connection = create_connection(host, port)

# Step 2: Send the request
response = connection.send(request)  # Returns Response object
```
```

### Tables for Structured Information

Use tables when presenting:
- Comparisons between options
- Feature lists
- Specifications
- Before/after scenarios

```markdown
| Approach | Pros | Cons | Best For |
|----------|------|------|----------|
| **Option A** | Fast, simple | Limited features | Quick projects |
| **Option B** | Full-featured | Complex setup | Enterprise |
```

### Lists for Clarity

**Bullet points** for unordered items:
```markdown
Key benefits include:
- **Improved readability** - Readers scan faster
- **Better retention** - Visual breaks aid memory
- **Professional appearance** - Matches publication standards
```

**Numbered lists** for sequential steps or ranked items:
```markdown
Follow these steps:
1. **Analyze** the current structure
2. **Identify** areas needing visual breaks
3. **Apply** appropriate formatting elements
4. **Review** for visual balance
```

### Emphasis Hierarchy

Apply consistently:
- **Bold** for key terms being introduced or emphasized
- *Italics* for emphasis within sentences or foreign terms
- `inline code` for technical terms, file names, commands
- ALL CAPS sparingly for critical warnings only

### Visual Diagrams (ASCII)

Use ASCII diagrams for:
- Process flows
- Hierarchies
- Relationships
- Architecture

```markdown
```
Input → Process → Output
  ↓         ↓        ↓
 Raw     Transform  Final
 Data      Data     Result
```
```

### Section Separators

Use horizontal rules (`---`) to create visual breathing room:
- Between major topic shifts
- Before and after important callouts
- To separate chapter sections

### Visual Balance Rules

1. **No text walls** - Insert visual breaks where they aid comprehension (guideline: ~4-6 sentences, but varies by content type)
2. **Content-appropriate density** - Technical content may need more code blocks; conceptual content may flow with fewer breaks
3. **Purposeful use** - Every visual element serves comprehension, not decoration
4. **White space** - Blank lines between logical groups
5. **Narrative flow priority** - Philosophical or conceptual passages may require longer unbroken prose; don't force visuals where they disrupt flow

> **📝 Note:** Visual formatting guidelines are flexible. Highly conceptual or philosophical writing may benefit from fewer interruptions. The goal is cognitive clarity, not arbitrary formatting quotas.

### Format Selection Guide

| Content Type | Best Format |
|--------------|-------------|
| Step-by-step process | Numbered list |
| Multiple options/features | Bullet list or table |
| Important warning | ⚠️ Warning callout |
| Key concept | 🎯 Core Concept callout |
| Technical code | Fenced code block with language |
| Comparison | Table |
| Hierarchy/flow | ASCII diagram |
| Term definition | 📖 Definition callout or bold + explanation |

---

## Common Writing Pitfalls to Avoid

1. **Passive Voice Overuse**: Target <20% passive voice overall
2. **Nominalization**: Convert zombie nouns back to verbs
3. **Hedge Word Overuse**: Reduce: possibly, probably, somewhat, rather, quite
4. **Clichés**: Eliminate: paradigm shift, think outside the box, at the end of the day
5. **Vague Language**: Replace general statements with specific details
6. **Unclear Antecedents**: Ensure pronouns clearly refer to specific nouns
7. **Modifier Misplacement**: Place modifiers immediately before the word they modify
8. **Text Walls**: Break up long passages with visual elements (lists, callouts, tables)

## Rapid Writing Workflow

### Timeline Expectations (Realistic)

> **⚠️ Important:** 1-week book generation is achievable ONLY with:
> - Highly automated pipeline (agents running in parallel)
> - Pre-existing research and outlines
> - Single author/agent focus (no context switching)
> - Quality gates that don't bottleneck

**Realistic Timeline by Book Type:**

| Book Type | Realistic Timeline | 1-Week Feasibility |
|-----------|-------------------|-------------------|
| Short technical guide (20-30K words) | 1-2 weeks | ✅ Achievable |
| Standard non-fiction (50-60K words) | 2-4 weeks | ⚠️ Aggressive |
| Comprehensive textbook (80K+ words) | 4-8 weeks | ❌ Unrealistic |

**If quality gates bottleneck**, adjust by:
- Running research and writing in parallel for different chapters
- Using editor review asynchronously (don't block writer)
- Accepting first-draft quality for initial pass, then iterating

### Daily Chapter Production

**Per Chapter Target** (4,000-6,000 words):
1. **Outline first** (30 minutes): Section headings, key points, transitions
2. **Draft rapidly** (2-3 hours): Write without editing, maintain flow
3. **Edit systematically** (1 hour): Check voice, transitions, clarity
4. **Fact-check** (30-60 minutes): Verify claims, citations

**Don't**: Edit while drafting, aim for perfection on first draft
**Do**: Write complete sections in single sessions, mark uncertain facts with [VERIFY]

## Quality Self-Check Protocol

**Voice & Consistency**:
- [ ] Perspective consistent throughout (you/we/one)
- [ ] Tone matches target Flesch score
- [ ] Technical level appropriate for audience
- [ ] Contraction usage consistent with style choice

**Structure**:
- [ ] Every paragraph has clear topic sentence
- [ ] 80% of paragraphs are 4-6 sentences
- [ ] No paragraphs exceed 10 sentences
- [ ] Sentence length varies for rhythm

**Transitions**:
- [ ] Ideas connect logically within paragraphs
- [ ] Clear transitions between paragraphs
- [ ] Section transitions smooth and purposeful
- [ ] Chapter opening hooks reader
- [ ] Chapter closing connects to next chapter

**Language Quality**:
- [ ] Active voice >80% of sentences
- [ ] Technical terms defined on first use
- [ ] No clichés or empty phrases
- [ ] Specific, concrete language (no vague claims)

**Readability**:
- [ ] Flesch Reading Ease matches target audience
- [ ] Average sentence length 15-20 words
- [ ] No sentences exceed 40 words

**Visual Formatting** (contextual, not rigid):
- [ ] Visual breaks where they aid comprehension (no arbitrary sentence count)
- [ ] 2-4 callout boxes per major section (fewer for conceptual/philosophical content)
- [ ] All code blocks have language specification
- [ ] Tables used for comparisons and structured data
- [ ] Lists used for multiple items (not run-on sentences)
- [ ] Bold/italics/inline code used appropriately
- [ ] Section separators (---) create visual breathing room
- [ ] ASCII diagrams for complex relationships (where applicable)
- [ ] Narrative flow preserved in conceptual passages (don't force visuals)

## Quick Reference

### Voice Decision Matrix

| Book Type | Perspective | Tone | Flesch Target |
|-----------|------------|------|---------------|
| Self-help, How-to | Second (You) | Conversational | 70-80 |
| Business, Professional | First plural (We) | Balanced | 60-70 |
| Academic, Technical | Third (Readers) | Formal | 50-60 |
| Popular non-fiction | Second (You) or We | Conversational-Balanced | 65-75 |
| Advanced Technical | We or Third | Formal/Technical | 35-55 |
| Specialized (compilers, ML, physics) | Third | Advanced Technical | 30-50 |

### Paragraph Length Distribution

- **Short (2-3 sentences)**: 10% of paragraphs
- **Standard (4-6 sentences)**: 80% of paragraphs
- **Long (7-9 sentences)**: 10% of paragraphs

### Chapter Length Guidelines

- **Introductory chapters**: 2,500-4,000 words
- **Core content chapters**: 4,000-6,000 words
- **Synthesis chapters**: 3,000-5,000 words
- **Concluding chapters**: 2,000-3,500 words

---

**Skill Version**: 1.3.0
**Last Updated**: 2025-11-27
**Maintained By**: Universal Pedagogical Engine Team
**Optimized For**: Rapid book generation (1 week timeline)
