---
name: academic-writing-standards
description: Expert knowledge of academic writing standards for peer-reviewed papers, including citation integrity, style compliance, clarity, and scientific writing best practices. Use when reviewing or editing academic manuscripts, papers, or research documentation.
---

# Academic Writing Standards

This skill provides expertise in academic writing standards for peer-reviewed research papers, ensuring clarity, rigour, and adherence to scientific writing conventions.

## Core Writing Principles

### Clarity and Directness

**Prioritise:**
- Clarity over eloquence
- Precision over persuasion
- Simple constructions over complex ones
- Active voice wherever possible

**Avoid:**
- Unnecessary adjectives and adverbs
- Overstatement and hyperbole
- Excessive qualification ("very", "clearly", "significantly", "novel")
- Complex punctuation where simpler alternatives work

### Style Transformations

**Examples of preferred style:**

```
Wordy: "The results clearly demonstrate that the novel approach significantly outperforms existing methods"
Better: "The approach outperforms existing methods"

Complex: "The model—which incorporates multiple data sources; including case counts, hospitalisations, and genomic data—provides insights"
Better: "The model incorporates case counts, hospitalisations, and genomic data. It provides insights"

Passive: "It was found that the infection rate was increasing"
Active: "We found the infection rate increased"

Hedged: "It appears that the results seem to suggest that there might be a relationship"
Direct: "The results suggest a relationship"
```

### Punctuation Simplification

**Avoid semicolons** when possible:
```
Avoid: "The model includes three components; case counts, delays, and reporting rates"
Better: "The model includes three components: case counts, delays, and reporting rates"
Or: "The model includes three components. These are case counts, delays, and reporting rates"
```

**Avoid excessive em-dashes:**
```
Avoid: "The approach—which we developed over three years—shows promise"
Better: "The approach shows promise. We developed it over three years"
```

**Simplify nested clauses:**
```
Avoid: "The method, which incorporates data from multiple sources, including surveillance systems, which track cases daily, and laboratory reports, provides estimates"
Better: "The method incorporates data from surveillance systems and laboratory reports. It provides estimates"
```

## Formatting Standards

### Document Structure

- **One sentence per line** in markdown format
- **Maximum 80 characters per line**
- **UK English** spelling (favour, colour, modelling, analyse)
- No trailing whitespace
- No spurious blank lines

### Mathematical Notation

- Use proper LaTeX formatting in appropriate contexts
- Define all notation clearly on first use
- Keep mathematical exposition accessible

## Citation and Reference Standards

### Citation Format Checking

**Common formats to verify:**
- Pandoc markdown: `[@author2024]`, `[@author2024; @other2023]`
- Multiple citations: `[@first2024; @second2024]`
- In-text citations: `@author2024 showed that...`

### Reference Integrity

**Check for:**
- Placeholder citations: `[@placeholder]`, `[@TODO]`, `[@CITE]`
- Malformed citations: Missing brackets, typos in citation keys
- Dangling references: Citations in text without corresponding bibliography entries
- Unused references: Bibliography entries never cited

**Citation consistency:**
- Verify citation keys follow consistent naming (e.g., `authorYear`, `author_year`)
- Check citation formatting matches throughout document
- Ensure proper use of et al. in multi-author citations

### Bibliography Verification

**When .bib file available:**
- Cross-reference every citation against bibliography
- Check for missing entries
- Verify citation keys match exactly
- Note any formatting inconsistencies in bibliography

**When .bib file unavailable:**
- Flag that references cannot be fully verified
- Suggest author independently verify all citations
- Check citation formatting consistency in text

## Originality and Attribution

### Identifying Potential Issues

**Flag text that:**
- Uses distinctive phrasing that may be borrowed
- Contains technical descriptions matching common sources
- Includes sequences of concepts in specific order suggesting copying
- Lacks clear paraphrasing when discussing others' work

**Not plagiarism checking:**
- Cannot definitively identify plagiarism
- Flags passages requiring author verification
- Suggests paraphrasing where appropriate
- Encourages proper attribution

### Proper Paraphrasing Guidance

**Poor paraphrasing:**
```
Original: "The model incorporates a hierarchical Bayesian structure with conjugate priors"
Poor: "The approach uses a hierarchical Bayesian framework with conjugate priors"
```

**Good paraphrasing:**
```
Better: "We used Bayesian hierarchical modelling with conjugate prior distributions"
```

## Common Writing Issues

### Overused Qualifiers

**Remove or replace:**
- "clearly", "obviously", "evidently" → Often unnecessary, let evidence speak
- "very", "quite", "rather" → Use stronger base word
- "significantly" → Reserve for statistical significance
- "novel", "new" → Show novelty through comparison, don't claim it
- "state-of-the-art" → Demonstrate through benchmarking

### Vague Language

**Replace with specifics:**
```
Vague: "The model performed well"
Specific: "The model achieved 95% accuracy"

Vague: "We used a large dataset"
Specific: "We used a dataset of 10,000 cases"

Vague: "Results improved substantially"
Specific: "Accuracy improved from 80% to 92%"
```

### Redundancy

**Common redundancies to fix:**
- "past history" → "history"
- "future plans" → "plans"
- "end result" → "result"
- "basic fundamentals" → "fundamentals"
- "completely finished" → "finished"

## Field-Specific Conventions

### Epidemiology and Public Health

- Use "infection" not "case" when referring to true infections
- Distinguish "reported cases" from "infections"
- Use "reproduction number" not "R value" in formal writing
- Define abbreviations on first use: "reproduction number (R)"

### Statistical Reporting

- Report confidence/credible intervals: "estimate (95% CI: lower, upper)"
- Use "uncertainty interval" for Bayesian analyses
- Report p-values accurately: "p < 0.001" not "p = 0.000"
- Distinguish statistical significance from practical importance

### Computational Methods

- Use "implementation" not "coding"
- "Algorithm" for theoretical description, "implementation" for code
- Report computational resources when relevant
- Specify software versions and packages

## Review Structure

When reviewing academic writing, structure feedback as:

1. **Reference Issues**
   - Citation formatting problems
   - Placeholder citations
   - Missing bibliography entries
   - Inconsistencies in citation style

2. **Attribution Concerns**
   - Passages requiring verification
   - Suggestions for better paraphrasing
   - Unclear sourcing of ideas

3. **Style Improvements**
   - Clarity and conciseness suggestions
   - Active voice conversions
   - Simplified sentence structures
   - Removed unnecessary qualifiers

4. **Formatting Issues**
   - Line length violations
   - Formatting inconsistencies
   - Spelling (UK vs US English)

## When to Apply This Skill

Use these standards when:
- Reviewing academic manuscripts
- Editing research papers
- Preparing submissions to journals
- Writing methods sections
- Drafting discussion sections
- Revising based on reviewer comments

Maintain scientific rigour whilst improving readability.
Always provide specific, actionable feedback with examples.
