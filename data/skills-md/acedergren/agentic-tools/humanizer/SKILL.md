---
name: humanizer
version: 3.0.0
license: MIT
description: |
  Detect and fix AI writing patterns including overused phrases (testament to, pivotal,
  landscape, delve), structural tells (rule of three, em dash overuse, negative parallelisms,
  copula avoidance), promotional language, and vague attributions. Use when user asks to
  "make text sound human", "remove AI tells", "humanize writing", mentions patterns like
  "too many dashes" or "sounds like ChatGPT", or requests natural/conversational tone.

  Triggers: AI-generated, humanize, writing style, natural writing, human voice, ChatGPT
  sound, remove AI patterns, conversational tone, writing voice.

  Credits: Based on Wikipedia's Signs of AI writing guide by @blader
allowed-tools:
  - Read
  - Write
  - Edit
  - Grep
  - Glob
  - AskUserQuestion
---

# Humanizer: AI Pattern Detection & Voice Injection

Transform AI-generated text into human writing by detecting patterns and injecting authentic voice.

---

## Before You Edit: Diagnostic Framework

**Ask yourself these 3 questions BEFORE applying any patterns:**

### 1. Voice Assessment
- **Does this text have a distinct voice?** Or is it neutral/corporate?
- **What personality should come through?** (witty, skeptical, conversational, authoritative)
- **Are there opinions, or just facts?** Human writing has stakes and perspective.

### 2. Pattern Prioritization
- **Which 3-5 patterns dominate this text?** (Don't fix everything at once)
- **What's the writer's intent?** (persuasive → keep some structure; casual → break all patterns)
- **Should some "AI-isms" stay?** (Formal technical docs may keep certain structures)

### 3. Rewrite Philosophy
- **Am I removing patterns OR injecting personality?** (Must do both)
- **Does my rewrite sound like a specific human wrote it?** (Not just "less AI")
- **Have I varied sentence rhythm?** (Short. Longer flowing sentences. Mix it up.)

**The Core Principle**: Sterile, voiceless writing is just as obvious as slop. Don't just remove bad patterns—add soul.

### 4. Pattern Detection Procedure (Domain-Specific)
Run these checks BEFORE editing:

**Statistical Density Check**:
- Count AI vocabulary words per 100 words: >3 = heavy AI signature
- Count em dashes per paragraph: >2 = structural tell
- Count "However" paragraph starts: >20% = AI transition overuse

**Structural Signature Check**:
- All paragraphs same length? = AI rhythm uniformity
- Every list has exactly 3 items? = rule of three addiction
- Conclusions use passive voice? = AI hedging pattern

**Context-Specific Preservation**:
- Academic: Keep formal structure, remove only vocabulary slop
- Technical: Preserve precision terminology, remove promotional language
- Marketing: Full humanization except brand voice requirements

---

## Critical Anti-Patterns (NEVER Do This)

### ❌ Pattern #1: Mechanical Pattern Removal
**Problem**: Just deleting AI phrases without adding human voice produces sterile text.

```markdown
❌ BAD EDIT:
"The framework serves as a testament to modern development practices."
→ "The framework is modern."

✅ GOOD EDIT:
"The framework serves as a testament to modern development practices."
→ "This framework gets it right. Clean APIs, sensible defaults, actual documentation."
```

**Why this matters**: Removing "testament to" makes it grammatically correct but soulless. The good edit has opinion, rhythm, and personality.

### ❌ Pattern #2: Over-Correction
**Problem**: Making every sentence "unpredictable" creates chaos, not humanity.

```markdown
❌ BAD EDIT (too chaotic):
"Results. Interesting ones! The experiment? It generated code—lots of it.
3 million lines worth. Developers (some of them) were impressed!!!!"

✅ GOOD EDIT (controlled variety):
"I genuinely don't know how to feel about this. 3 million lines of code,
generated overnight. Half the dev community is losing their minds,
half are explaining why it doesn't count."
```

**Why this matters**: Human writing has rhythm variation, not random punctuation chaos.

### ❌ Pattern #3: Removing ALL Structure
**Problem**: Not all AI patterns are bad—some formal writing needs structure.

```markdown
Context: Academic paper abstract

❌ BAD EDIT:
"Our study looked at machine learning. We found some stuff.
It's interesting. Check out our results."

✅ GOOD EDIT:
"This study examines machine learning approaches to code generation.
We evaluated three architectures and found that transformer-based
models outperformed RNNs by 23% on our benchmark."
```

**Why this matters**: Formal contexts need clarity over personality. Know your audience.

### ❌ Pattern #4: Batch-Replacing AI Words Without Context
**Problem**: Blindly replacing "delve" or "landscape" breaks legitimate usage.

```markdown
Context: Computer vision paper

❌ BAD EDIT:
"Our model examines the feature landscape" → "Our model examines the feature terrain"

✅ GOOD EDIT:
"Our model examines the feature landscape" → "Our model analyzes feature space"
OR keep "landscape" if it's established terminology in CV papers
```

**Why this matters**: Not every AI word is wrong—check if it's domain-appropriate first. "Landscape" in data science ≠ "business landscape" slop.

---

## Most Common AI Patterns (Quick Reference)

### Content-Level Patterns

**Undue Emphasis on Significance**
- Words: stands as, serves as, testament to, pivotal, crucial, underscores, broader trends
- Fix: Remove inflated symbolism, state facts directly

**Promotional Language**
- Words: boasts, nestled, vibrant, rich heritage, breathtaking, stunning
- Fix: Replace adjectives with specific details

**Vague Attributions**
- Words: Industry reports, Observers note, Experts argue, Some critics
- Fix: Name specific sources or remove the claim

### Language-Level Patterns

**AI Vocabulary Words** (post-2023 frequency spike)
- Words: delve, crucial, enhance, foster, garner, intricate, landscape (abstract), pivotal, showcase, tapestry (abstract), underscore
- Fix: Use plain synonyms or restructure

**Copula Avoidance** (avoiding "is/are")
- Pattern: "serves as", "stands as", "represents", "boasts", "features"
- Fix: Use simple "is/are/has"

**Negative Parallelisms**
- Pattern: "Not only... but...", "It's not just about X, it's Y"
- Fix: State directly without forced contrast

### Style-Level Patterns

**Em Dash Overuse**
- Pattern: Multiple em dashes in one paragraph (—)
- Fix: Replace with commas, periods, or parentheses

**Rule of Three Overuse**
- Pattern: "innovation, inspiration, and industry insights"
- Fix: Break groups of three, vary list sizes

**Title Case Headings**
- Pattern: "Strategic Negotiations And Global Partnerships"
- Fix: Sentence case: "Strategic negotiations and global partnerships"

---

## Humanization Strategy: When to Preserve vs Remove

**The Decision Framework**: Not all contexts need full humanization.

| Context | Humanization Level | Remove Patterns | Inject Voice | Example Fix |
|---------|-------------------|-----------------|--------------|-------------|
| **Academic/Research** | Low (10-20%) | Delete slop only (delve, testament to) | Minimal | Keep structure, remove AI vocabulary |
| **Technical Docs** | Medium (30-50%) | Remove promotional language, keep clarity | Light opinions | "This works well" → "This approach handles edge case X" |
| **Blog/Marketing** | High (70-90%) | Remove most AI tells | Strong voice | Full personality, distinct author presence |
| **Social/Casual** | Maximum (100%) | Delete all AI patterns | Maximum authenticity | Pure conversational, break all rules |
| **Formal Business** | Medium (40-60%) | Remove obvious slop, keep professionalism | Controlled confidence | "We believe this represents..." → "This delivers X" |

**Critical Non-Obvious AI Tells** (beyond the common list):
- **Paragraph-starting "However"**: AI overuses this transition (appears 3x more in GPT text)
- **Passive voice in conclusions**: "It can be concluded that..." (AI hedges at the end)
- **Symmetric sentence structure**: Every paragraph follows same length/rhythm pattern
- **"Importantly" mid-sentence**: AI uses this more than humans (statistical quirk)
- **Abstract "landscape" metaphors**: "the technology landscape", "the business landscape"

---

## When to Load Full Pattern References

**For comprehensive pattern catalogs, use mandatory loading:**

**MANDATORY - READ ENTIRE FILE: `references/content-patterns.md` when:**
- Text contains 5+ promotional adjectives (stunning, breathtaking, vibrant, rich)
- Significance inflation detected ("serves as testament", "stands as pivotal")
- Need complete "symbolism removal" examples
- **Do NOT load** for casual blog posts or social media text

**MANDATORY - READ ENTIRE FILE: `references/language-patterns.md` when:**
- Text uses 8+ AI vocabulary words (delve, showcase, intricate, foster, garner)
- Heavy copula avoidance patterns ("serves as" instead of "is")
- Need elegant variation catalog for substitutions
- **Do NOT load** for technical documentation where precision matters

**MANDATORY - READ ENTIRE FILE: `references/style-patterns.md` when:**
- Text has 6+ em dashes in single paragraph
- Rule of three appears 4+ times
- Title case headings throughout document
- **Do NOT load** for academic papers (formatting may be required)

**Never load references** for simple opinion injection or rhythm fixes—handle with decision framework above.

---

## Process

1. **Read input text** - Identify 3-5 dominant patterns
2. **Apply diagnostic framework** - Answer the 3 questions above
3. **Make strategic edits** - Fix patterns + inject voice simultaneously
4. **Verify rhythm** - Read aloud test (does it sound natural?)
5. **Present result** - Show rewritten text with brief summary if helpful

---

## Quick Example

**Before (AI-sounding):**
> The new software update serves as a testament to the company's commitment to innovation. Moreover, it provides a seamless, intuitive, and powerful user experience—ensuring that users can accomplish their goals efficiently. It's not just an update, it's a revolution in how we think about productivity.

**After (Humanized):**
> The software update adds batch processing, keyboard shortcuts, and offline mode. Early beta feedback has been positive—most testers report finishing tasks faster.

**What changed:**
- Removed inflated symbolism ("serves as a testament")
- Removed AI vocabulary ("Moreover", "seamless, intuitive, powerful")
- Removed negative parallelism ("It's not just...it's...")
- Removed vague claims ("commitment to innovation")
- Added specific features (batch processing, shortcuts, offline)
- Added concrete evidence (beta feedback, faster completion)
- Kept neutral tone appropriate for feature announcement

---

## Reference Materials

Based on [Wikipedia:Signs of AI writing](https://en.wikipedia.org/wiki/Wikipedia:Signs_of_AI_writing), maintained by WikiProject AI Cleanup.

**Key insight**: "LLMs use statistical algorithms to guess what should come next. The result tends toward the most statistically likely result that applies to the widest variety of cases."

Translation: AI writing is optimized for average acceptability, not authentic voice.
