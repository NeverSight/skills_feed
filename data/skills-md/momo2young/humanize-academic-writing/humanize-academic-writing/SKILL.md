---
name: humanize-academic-writing
description: Transform AI-generated academic text into natural, human-like scholarly writing for social sciences. Detects AI patterns (repetitive structures, abstract language, mechanical flow) and rewrites with authentic academic voice. Use when revising AI-drafted papers, improving writing naturalness, reducing AI detection markers, or when user mentions humanizing text, academic writing quality, or social science writing for non-native English speakers.
---

# Humanize Academic Writing for Social Sciences

## Academic Integrity Statement

**Purpose**: This skill helps researchers improve the quality and naturalness of their **own original ideas** expressed through AI-assisted writing tools.

**Ethical Use**:
- ✅ Revising AI-drafted text based on your own research and ideas
- ✅ Improving writing quality for non-native English speakers  
- ✅ Learning better academic writing patterns
- ❌ Using AI to generate ideas you don't understand
- ❌ Submitting work that doesn't represent your intellectual contribution

**Principle**: The goal is authentic scholarly communication, not deception.

---

## Target Audience

Non-native English speakers in social sciences (sociology, anthropology, political science, education, psychology) who:
- Have original ideas and research
- Used AI tools to draft their text
- Need to humanize the writing style
- Want to reduce obvious AI patterns

---

## When to Use This Skill

- User has AI-generated draft based on their own ideas
- Text feels "too perfect," mechanical, or repetitive
- Need to reduce AI detection markers
- Want authentic academic voice for social science writing
- Paragraph transitions feel robotic
- Language is overly abstract without concrete examples

---

## Core Workflow

### Step 1: Analyze the Text

First, run the AI detection analyzer to identify problematic patterns:

```bash
python scripts/ai_detector.py input.txt
```

The analyzer identifies:
- Repetitive sentence structures and lengths
- Overused AI transition phrases (Moreover, Furthermore, Additionally)
- Abstract/vague language patterns ("various aspects", "in terms of")
- Mechanical paragraph transitions
- Unnatural word choices for social sciences
- Low vocabulary diversity (Type-Token Ratio)
- Excessive passive voice
- Consecutive sentence similarity

**Output**: AI probability score + specific issues marked per paragraph

### Step 2: Apply Targeted Rewriting Strategies

Based on detected issues, apply these fixes:

#### Strategy 1: Vary Sentence Rhythm (Fix Uniformity)

**AI Pattern**: All sentences are similar length (15-20 words)

**Human Fix**: Mix short (5-10), medium (15-20), and long (25-35) sentences

Example:
- AI: "This study examines social media impact. The research focuses on young adults. The analysis considers multiple factors."
- Human: "This study examines social media's impact on young adults, considering factors ranging from identity formation to civic engagement."

#### Strategy 2: Reduce Abstract Scaffolding

**AI Pattern**: Vague placeholder phrases that say little

Common culprits:
- "various aspects"
- "in terms of"
- "it is important to note that"
- "multiple factors"
- "different perspectives"

**Human Fix**: Replace with specific concepts, named theories, concrete examples

Example:
- AI: "In terms of the various aspects of social interaction, multiple factors play important roles."
- Human: "Social interaction depends on trust, reciprocity, and shared norms—factors that vary across cultural contexts."

#### Strategy 3: Eliminate Mechanical Transitions

**AI Pattern**: Overusing formal connectors at sentence starts

Overused words:
- Moreover,
- Furthermore,
- Additionally,
- In addition,
- It is important to note that

**Human Fix**: Use diverse transition strategies:
- Direct logical flow (no connector needed)
- "This pattern echoes..."
- "Building on this insight..."
- "Yet" / "Still" / "However" (sparingly)
- Implicit connections through content

#### Strategy 4: Add Scholarly Voice

**AI Pattern**: Generic academic tone without personality or critical engagement

**Human Fix**:
- Include appropriate hedging ("may suggest", "appears to", "potentially")
- Show critical engagement with sources
- Use disciplinary language naturally
- Demonstrate genuine intellectual grappling

Example:
- AI: "The data shows a correlation between X and Y."
- Human: "The data suggest a correlation between X and Y, though the causal mechanism remains unclear and warrants further investigation."

#### Strategy 5: Ground in Specificity

**AI Pattern**: Generic statements without grounding

**Human Fix**:
- Name specific theories/scholars
- Include concrete examples
- Reference particular contexts
- Cite actual studies with details

Example:
- AI: "Research has shown various effects of social media on society."
- Human: "Recent ethnographic work documents how Instagram reshapes young women's body image practices (Tiidenberg 2018), while experimental studies reveal minimal effects on political polarization (Guess et al. 2023)."

### Step 3: Rewrite with Rationale

For each paragraph, follow this format:

**Original (AI-generated):**
[Paste the original text]

**Revised (Humanized):**
[Your rewritten version]

**Rationale:**
Explain in 1-2 sentences what AI patterns you fixed. Examples:
- "Removed repetitive 'Moreover/Additionally' transitions and varied sentence rhythm (added one short sentence, one long); replaced 'various aspects' with specific concepts (trust, reciprocity, norms)."
- "Eliminated abstract scaffolding ('in terms of', 'multiple factors'); added concrete citation (Smith 2022) and specific research finding; included scholarly hedging ('suggests' rather than 'shows')."
- "Broke uniform 18-word sentences into varied lengths (8, 24, 15 words); removed mechanical 'Furthermore' openers; grounded claims in named theory (social capital) and specific context (urban China)."

---

## Key Principles for Humanizing Text

### 1. Perplexity (Unpredictability)
- **Problem**: AI text is too predictable
- **Fix**: Add unexpected (but academically appropriate) word choices; vary syntactic structures

### 2. Burstiness (Rhythm Variation)
- **Problem**: AI uses uniform sentence lengths
- **Fix**: Mix short punchy sentences with longer complex ones; create natural reading rhythm

### 3. Specificity over Abstraction
- **Problem**: AI defaults to vague abstractions
- **Fix**: Use concrete examples, specific data, named theories; ground claims in particular contexts

### 4. Authentic Academic Voice
- **Problem**: Generic formal tone without personality
- **Fix**: Show genuine engagement with ideas; include appropriate hedging; demonstrate critical thinking

### 5. Natural Flow
- **Problem**: Mechanical transitions and paragraph connections
- **Fix**: Let content drive connections; use implicit logic; minimize formal connectors

---

## Social Science Specifics

### Disciplinary Language

**Sociology**:
- Key concepts: stratification, agency, habitus, capital, institutions, inequality
- Theoretical traditions: functionalist, conflict, symbolic interactionist, practice theory
- Common methods: ethnography, surveys, interviews, archival analysis

**Anthropology**:
- Key concepts: culture, ritual, kinship, liminality, positionality, thick description
- More reflexive voice acceptable
- Ethnographic detail valued

**Political Science**:
- Key concepts: institutions, power, legitimacy, governance, state capacity
- Causal inference language
- Hypothesis testing frameworks

**Education**:
- Key concepts: pedagogy, curriculum, equity, achievement gaps, learning outcomes
- Mixed methods common
- Policy relevance emphasized

**Psychology (Social)**:
- Key concepts: cognition, behavior, attitudes, interventions, mechanisms
- Operational definitions critical
- Experimental designs prominent

### Non-Native Speaker Considerations

**Common AI Crutches**:
1. Over-reliance on intensifiers ("very", "really", "quite")
2. Repetitive sentence starters
3. Overuse of formal connectors to signal logic

**Strengths to Preserve**:
- Clear logical structure (maintain this)
- Formal register (appropriate for academic writing)
- Careful grammar (don't over-casualize)

**Areas to Humanize**:
- Vary clause structures and sentence types
- Use field-specific terminology confidently
- Add appropriate scholarly hedging
- Include critical engagement with sources
- Ground abstractions in concrete examples

---

## Additional Resources

For detailed guidance, see:

- **[docs/rewriting-principles.md](docs/rewriting-principles.md)**: Comprehensive rewriting techniques with extended examples
- **[docs/examples.md](docs/examples.md)**: Full before/after rewrites of different section types (intro, methods, findings, discussion)
- **[docs/social-science-patterns.md](docs/social-science-patterns.md)**: Discipline-specific conventions and terminology

---

## Scripts and Tools

### ai_detector.py
Analyzes text for AI patterns and provides detailed scoring

```bash
# Basic analysis
python scripts/ai_detector.py input.txt

# Detailed output with paragraph-by-paragraph breakdown
python scripts/ai_detector.py input.txt --detailed

# JSON output for programmatic use
python scripts/ai_detector.py input.txt --json > analysis.json
```

### text_analyzer.py
Provides quantitative metrics on text quality

```bash
# Analyze text metrics
python scripts/text_analyzer.py input.txt

# Compare before/after versions
python scripts/text_analyzer.py original.txt revised.txt --compare
```

**Metrics provided**:
- Sentence length distribution and variance
- Vocabulary diversity (Type-Token Ratio)
- Academic word usage frequency
- Transition word density
- Passive voice percentage
- Average sentence complexity

---

## Example Workflow

1. **User provides AI-generated text**: "Can you help humanize this paragraph from my paper?"

2. **Analyze first**:
   - Run `ai_detector.py` or manually identify patterns
   - Note specific issues (e.g., "repetitive sentence structure, 3x 'Moreover', abstract language")

3. **Rewrite strategically**:
   - Apply relevant strategies from above
   - Maintain the user's core ideas and arguments
   - Preserve accurate citations and data

4. **Explain changes**:
   - Show original → revised
   - Provide rationale explaining what AI patterns were fixed
   - Help user learn for future writing

5. **Verify improvements**:
   - Optionally run `text_analyzer.py` to confirm metrics improved
   - Check that meaning and accuracy preserved

---

## Tips for Effective Use

### Do:
- ✅ Preserve the user's original ideas and arguments
- ✅ Maintain citation accuracy
- ✅ Keep the appropriate academic register
- ✅ Focus on patterns, not just individual words
- ✅ Explain your changes so users learn

### Don't:
- ❌ Change the meaning or argument
- ❌ Add information not in the original
- ❌ Over-casualize academic language
- ❌ Remove all formal connectors (some are needed)
- ❌ Make text deliberately grammatically incorrect

### Balance:
Academic writing should be:
- **Clear but not simplistic**
- **Formal but not robotic**
- **Structured but not mechanical**
- **Precise but not pedantic**

---

## Common Pitfalls to Avoid

1. **Over-correcting**: Don't make every sentence wildly different in length. Natural variation exists within a range.

2. **Removing all connectors**: Some transitions are necessary for clarity, especially in complex arguments.

3. **Adding colloquialisms**: Academic writing should remain formal; avoid casual expressions.

4. **Losing precision**: Don't sacrifice technical accuracy for "naturalness."

5. **Ignoring discipline**: Social science subfields have different conventions—respect them.

---

## Summary Checklist

After rewriting, verify:

- [ ] Sentence lengths vary (mix of short, medium, long)
- [ ] Mechanical transitions (Moreover, Furthermore, Additionally) removed or reduced
- [ ] Abstract placeholder phrases replaced with specific concepts
- [ ] At least one concrete example or named theory added
- [ ] Scholarly hedging included where appropriate
- [ ] Original meaning and arguments preserved
- [ ] Citations remain accurate
- [ ] Disciplinary language sounds natural
- [ ] Rationale provided explaining AI patterns fixed

---

This skill emphasizes **authentic scholarly communication** while respecting the intellectual work of non-native English speakers using AI tools responsibly.
