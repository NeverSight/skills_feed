---
name: academic-writing-cs
description: Comprehensive toolkit for writing high-quality computer science research papers (conference, journal, thesis). Provides narrative construction guidance, sentence-level clarity principles (Gopen & Swan), academic phrasebank, CS-specific conventions, and section-by-section quality checklists. Use when assisting with academic paper writing, revision, or structure planning across all stages from drafting to submission.
---

# Academic Writing for Computer Science

## Overview

This skill provides end-to-end support for writing high-quality computer science research papers. It focuses on constructing clear, compelling technical narratives while adhering to field-specific conventions.

**Core Philosophy:**
- Academic papers are **narrative arcs** (Problem → Solution → Evidence → Implications), not template fill-ins
- Clarity comes from structure: place familiar information first, new information last
- Every design choice must be justified; every claim must be supported

**Scope:**
- Conference papers (6-12 pages, competitive venues)
- Journal articles (15-30 pages, comprehensive)
- Thesis chapters (flexible length, deep coverage)
- All CS subfields: AI/ML, Systems, Theory, HCI, Security, etc.

---

## When to Use This Skill

Invoke this skill when:
- Planning paper structure and narrative flow
- Drafting any section (Abstract, Introduction, Methods, Results, Discussion, Conclusion)
- Revising for clarity, coherence, or compliance with venue requirements
- Reviewing sentence-level writing for clarity issues
- Seeking CS-specific conventions (notation, figures, citations)
- Checking completeness with section-by-section quality checklists
- Responding to reviewer comments

---

## Workflow Decision Tree

### Stage 1: Planning and Structure

**When starting a new paper or major revision:**

1. **Define the Narrative Arc**
   - What problem does this solve, and why does it matter? (1-2 sentences)
   - What is the single main contribution? (1 sentence)
   - What are the 3 key results that support the contribution?
   - What are the main limitations?

   **Reference:** `references/narrative_framework.md` — Read the "Core Principle" and "Section-Level Narrative Structure" sections to understand how to structure the paper's story.

2. **Identify Target Venue and Constraints**
   - Conference or journal?
   - Page limits, formatting requirements, anonymization rules?
   - Subfield conventions (ML vs. Systems vs. Theory)?

   **Reference:** `references/cs_conventions.md` (Section 8: Venue-Specific Guidelines, Section 5: Subfield-Specific Conventions)

3. **Outline Section-by-Section**
   - For each major section, define:
     - What is the purpose of this section?
     - What are the 2-3 key points to convey?
     - What figures/tables will support this?

   **Tool:** Use `assets/section_checklists.md` (Quick Pre-Draft Planning Checklist) to ensure all key questions are answered before writing begins.

---

### Stage 2: Drafting

**For each section, follow this process:**

#### Abstract
1. Use the **4-sentence structure**: Context → Gap → Contribution → Impact
2. Check against `assets/section_checklists.md` (Abstract Checklist)
3. Ensure it's self-contained and within word limit (150-250 words)

**Common mistakes:**
- Vague contribution: "We improve X" → Be specific: "We achieve 15% higher accuracy"
- No concrete results: Always include numbers/metrics

---

#### Introduction
1. Follow the **funnel structure**: Broad → Narrow → Specific
   - Para 1: Problem domain and importance
   - Para 2-3: Specific problem, motivation, why existing work falls short
   - Para 4: Gap statement ("However, existing approaches lack...")
   - Para 5: Contribution overview (what this paper provides)
   - Para 6: Results summary (2-3 concrete findings)
   - Para 7: Paper organization (optional)

2. **Key requirement:** By the end of paragraph 4-5, the reader must clearly understand the contribution.

3. Include at least one figure (architecture or key result) for ML/systems papers.

4. Check against `assets/section_checklists.md` (Introduction Checklist)

**Reference:** `references/narrative_framework.md` (Introduction section) for detailed guidance and examples.

---

#### Related Work
1. **Organize thematically** (not chronologically): Group into 3-5 categories
2. For each category:
   - Describe the general approach
   - Cite 3-5 representative works with 1-sentence descriptions
   - Point out limitations relevant to your contribution

3. **End with positioning paragraph**: "In contrast to [X], our approach..."
   - Clearly articulate differences and advantages

4. Check against `assets/section_checklists.md` (Related Work Checklist)

**Common mistakes:**
- Laundry list of citations without synthesis
- Failing to position your work relative to prior work
- Being dismissive (respect prior work while differentiating)

---

#### Methodology
1. **Dual objectives:**
   - Reproducibility: Enough detail for reimplementation
   - Intuition: Explain why the approach works

2. **Structure varies by paper type:**
   - **ML/AI papers**: Problem Formulation → Overview + Figure → Detailed Design → Implementation → Complexity
   - **Systems papers**: Architecture Overview → Component Design → Key Mechanisms → Implementation
   - **Theory papers**: Formal Definitions → Main Results (theorems) → Proof Sketch

3. **Always include:**
   - Clear notation (define all symbols on first use)
   - High-level overview before diving into details
   - Justification for design choices (or defer to Ablations)

4. Check against `assets/section_checklists.md` (Methodology Checklist)

**Reference:** `references/narrative_framework.md` (Methodology section) and `references/cs_conventions.md` (Section 1: Notation and Mathematical Writing)

---

#### Experiments/Results
1. **Experimental Setup** (subsection):
   - Datasets: Size, splits, preprocessing
   - Baselines: What you compare against (with citations)
   - Metrics: What you measure and why
   - Hardware/Software: Infrastructure and versions
   - Hyperparameters: How selected

2. **Main Results** (subsection):
   - Table/figure showing primary comparison
   - Text: "Table 1 shows that our method outperforms..."
   - Highlight key findings with concrete numbers
   - Report statistical significance (confidence intervals, p-values, or std dev)

3. **Ablation Studies** (subsection, critical):
   - Demonstrate necessity of each component
   - Table: effect of removing/modifying components

4. **Analysis** (subsection):
   - Where does the method excel? Where does it fail?
   - Qualitative analysis, error analysis, failure cases

5. **Computational Cost** (if relevant):
   - Training time, inference time, memory usage
   - Comparison with baselines

6. Check against `assets/section_checklists.md` (Experiments/Results Checklist)

**Reference:** `references/narrative_framework.md` (Experiments/Results section)

---

#### Discussion
1. **Summarize findings** (1 para): Restate key results
2. **Interpret results** (1-2 paras): Why does the method work? What insights?
3. **Acknowledge limitations** (0.5-1 para): Be honest about scope and failure cases
4. **Broader implications** (0.5-1 para): Impact on the field, applications, future directions

5. Check against `assets/section_checklists.md` (Discussion Checklist)

**Tone:** Balanced—confident but not overselling. Limitations increase credibility.

---

#### Conclusion
1. **Restate contribution** (1 para): Recap problem, solution, key findings
2. **Broader impact** (0.5 para): Significance and applications
3. **Future work** (0.5 para): Open questions and extensions
   - Phrase as opportunities: "An interesting direction is..." (not "In future work, we will...")

4. Check against `assets/section_checklists.md` (Conclusion Checklist)

**Do NOT:** Introduce new ideas, copy-paste Abstract, or be vague.

---

### Stage 3: Revision for Clarity

**After drafting, apply sentence-level clarity principles:**

#### The Three Golden Rules (Gopen & Swan)

1. **Old Before New**: Start sentences with familiar information; end with new information
   - This creates coherent flow where each sentence builds on what came before

2. **Subject-Verb Proximity**: Keep the verb close to the subject
   - Long gaps between subject and verb strain comprehension

3. **Stress Position Power**: Place the most important information at sentence end
   - Readers remember and emphasize what comes at the end

**Apply these rules systematically:**
- For each paragraph, check that sentences flow (old-to-new)
- For each sentence, check that:
  - Topic position (start) contains familiar info
  - Stress position (end) contains important new info
  - Verb appears soon after subject

**Reference:** `references/sentence_clarity.md` — Read this in full for detailed principles, examples, and common anti-patterns.

**Practical Checklist:**
- [ ] Familiar information at sentence start (topic position)
- [ ] Important new information at sentence end (stress position)
- [ ] Verb close to subject
- [ ] Active voice (unless passive is intentionally better)
- [ ] Parallel structures for parallel ideas

**Common anti-patterns to fix:**
- "Buried Verb" Syndrome: Converting verbs to nouns (nominalization)
  - ❌ "The comparison of the methods is shown..."
  - ✅ "Table 1 compares the methods..."
- "Throat-Clearing": Weak starts like "It is important to note that..."
  - ❌ "It is important to note that our method improves accuracy."
  - ✅ "Our method improves accuracy."
- "Dangling Emphasis": Ending sentences with weak elements
  - ❌ "This approach significantly improves performance, as shown in [23]."
  - ✅ "As shown in [23], this approach significantly improves performance."

---

### Stage 4: Polishing and Compliance

#### Language and Phrasing

When writing or revising specific academic functions, consult `references/phrasebank.md`:

- **Introducing work**: Establishing territory, identifying gaps, stating contributions
- **Referring to sources**: Integral vs. non-integral citations
- **Describing methods**: Sequential actions, conditional logic, implementation details
- **Reporting results**: Presenting findings, comparing baselines, interpreting
- **Discussing findings**: Explaining success, acknowledging limitations, stating implications
- **Writing conclusions**: Summarizing, broader impact, future work

**General language functions:**
- Being cautious (hedging): "may", "appears to", "likely"
- Being critical: Identifying weaknesses, questioning validity
- Compare and contrast: Similarity, difference
- Describing trends: Increasing, decreasing, stability
- Explaining causality: Causes, effects, conditions

**Usage:** Adapt templates to your context; don't copy verbatim. Vary expressions to maintain natural flow.

---

#### CS-Specific Conventions

Ensure compliance with field norms:

1. **Notation**:
   - Define all symbols on first use
   - Use consistent conventions (bold for vectors, italic for scalars, etc.)
   - Integrate equations into sentences with punctuation

2. **Figures and Tables**:
   - Reference all figures/tables in text before they appear
   - Self-contained captions
   - High-resolution, readable fonts (≥8pt)
   - Colorblind-friendly palettes

3. **Citations**:
   - Follow venue citation style (author-year or numbered)
   - Cite all prior work you build on or compare against
   - Accurate and complete bibliography

4. **Code and Reproducibility**:
   - State code availability
   - Provide sufficient implementation details
   - Report hyperparameters, random seeds, number of runs

5. **Subfield-Specific Variations**:
   - **ML/AI**: Emphasis on ablations, statistical significance, computational cost
   - **Systems**: Architecture diagrams, throughput/latency, scalability
   - **Theory**: Formal definitions, theorems, proofs, complexity bounds
   - **HCI**: User studies, qualitative feedback, interface screenshots
   - **Security**: Threat models, attack scenarios, defense mechanisms

**Reference:** `references/cs_conventions.md` — Comprehensive guide covering notation, figures, citations, code, subfield norms, and venue requirements.

---

#### Quality Assurance

Before submission, use `assets/section_checklists.md`:

1. **Section-by-Section Review**:
   - Run through each section's checklist
   - Ensure all required elements are present
   - Check for common pitfalls

2. **Pre-Submission Checklist**:
   - Content completeness (all sections, figures, citations)
   - Formatting (venue template, page limits, margins)
   - Anonymization (if double-blind)
   - Reproducibility (sufficient detail, code availability)
   - Final quality checks (spell-check, grammar, co-author review)

3. **Emergency Checklist** (if deadline is imminent):
   - Prioritize: Abstract, Introduction contribution statement, Main results table, At least one ablation, Readable figures, Correct bibliography

---

### Stage 5: Responding to Reviews

**After receiving reviewer feedback:**

1. **Analyze comments systematically:**
   - Categorize: Major issues (experiments, clarity, claims) vs. Minor issues (typos, formatting)
   - Prioritize: Address major issues first

2. **Plan revisions:**
   - List all changes to be made
   - If experiments are requested, plan them carefully
   - If clarifications are needed, identify which sections to revise

3. **Revise and respond:**
   - Address every comment (in rebuttal or revision)
   - Use respectful, professional tone
   - Clearly mark changes (if required by venue)

4. **Check revised version:**
   - Ensure all changes are integrated
   - Re-run relevant checklists from `assets/section_checklists.md` (Revision Checklist)
   - Verify still within page limits

**Reference:** `assets/section_checklists.md` (Revision Checklist)

---

## Key Resources Summary

### Narrative and Structure
- **`references/narrative_framework.md`**: Core paper structure (Abstract, Introduction, Related Work, Methods, Results, Discussion, Conclusion). Use for understanding the narrative arc and section-specific guidance.

### Sentence-Level Clarity
- **`references/sentence_clarity.md`**: Gopen & Swan principles (topic position, stress position, old-to-new flow). Use for revising individual sentences and paragraphs for maximum clarity.

### Academic Phrases
- **`references/phrasebank.md`**: Templates for common academic writing functions (introducing work, citing sources, reporting results, discussing findings). Use when drafting or seeking variation in phrasing.

### CS Conventions
- **`references/cs_conventions.md`**: Field-specific norms (notation, figures, citations, code, subfield variations, venue requirements). Use for ensuring compliance with CS writing standards.

### Quality Checklists
- **`assets/section_checklists.md`**: Comprehensive checklists for every section, plus pre-submission, revision, and emergency checklists. Use for planning, reviewing, and final quality assurance.

---

## Example Workflows

### Workflow 1: Starting from Scratch

**User:** "I need to write a conference paper on my new semi-supervised learning method."

**Process:**
1. **Planning** (Stage 1):
   - Define narrative arc: Problem (labeled data is expensive) → Solution (our semi-supervised method) → Evidence (experiments on 3 datasets) → Implications (reduces labeling cost)
   - Read `references/narrative_framework.md` (Core Principle)
   - Use `assets/section_checklists.md` (Quick Pre-Draft Planning Checklist)

2. **Drafting** (Stage 2):
   - Abstract: 4-sentence structure (Context: deep learning needs data; Gap: labeling is expensive; Contribution: our method STCR; Impact: 82% accuracy with 10% labels)
   - Introduction: Funnel (broad: DL success → narrow: labeling cost → gap: existing semi-supervised methods lack X → contribution: STCR leverages consistency → results: 7% improvement)
   - Check each section against `assets/section_checklists.md`

3. **Revision** (Stage 3):
   - Apply `references/sentence_clarity.md` principles to every paragraph
   - Ensure old-to-new flow, stress position usage

4. **Polishing** (Stage 4):
   - Use `references/phrasebank.md` for varied phrasing
   - Ensure compliance with `references/cs_conventions.md` (ML/AI conventions)
   - Run Pre-Submission Checklist from `assets/section_checklists.md`

---

### Workflow 2: Revising for Clarity

**User:** "My introduction is confusing. Reviewers said they couldn't understand the contribution."

**Process:**
1. **Diagnose issue**:
   - Check against `assets/section_checklists.md` (Introduction Checklist)
   - Is the contribution stated clearly by paragraph 4-5?
   - Is the funnel structure followed (broad → narrow)?

2. **Restructure if needed**:
   - Read `references/narrative_framework.md` (Introduction section)
   - Ensure: Opening → Background → Gap → Contribution → Results → Organization
   - Explicitly state: "In this paper, we present [X], which addresses [Y] by [Z]."

3. **Revise at sentence level**:
   - Apply `references/sentence_clarity.md` principles
   - Check that each sentence flows from the previous one (old-to-new)
   - End key sentences with the important information (stress position)

---

### Workflow 3: Drafting the Results Section

**User:** "How should I present my experimental results?"

**Process:**
1. **Structure**:
   - Read `references/narrative_framework.md` (Experiments/Results section)
   - Follow: Setup → Main Results → Ablations → Analysis → Cost

2. **Create tables/figures**:
   - Main results table: Methods (rows) vs. Metrics (columns)
   - Bold best results; include standard deviations
   - Check `references/cs_conventions.md` (Figures and Tables section)

3. **Write accompanying text**:
   - "Table 1 shows that our method achieves X, outperforming the strongest baseline by Y%."
   - Use `references/phrasebank.md` (Section 4: Reporting Results) for phrasing

4. **Quality check**:
   - Run through `assets/section_checklists.md` (Experiments/Results Checklist)
   - Ensure: Statistical significance, Ablations present, Analysis included

---

### Workflow 4: Ensuring CS Compliance

**User:** "Is my notation and citation style correct for ICML?"

**Process:**
1. **Check venue requirements**:
   - Read `references/cs_conventions.md` (Section 8: Venue-Specific Guidelines)
   - ICML uses numbered citations [1], double-blind review, LaTeX template

2. **Notation**:
   - Read `references/cs_conventions.md` (Section 1: Notation and Mathematical Writing)
   - Ensure: Vectors are bold, scalars are italic, all symbols defined

3. **Citations**:
   - Read `references/cs_conventions.md` (Section 3: Citations and References)
   - Use numbered format: "Method X [1] achieves..."
   - Anonymize self-citations for double-blind

4. **Final check**:
   - `assets/section_checklists.md` (Pre-Submission Checklist → Compliance section)

---

## Common Pitfalls and How to Avoid Them

### Pitfall 1: Vague Contributions
**Problem:** "We improve performance on X."
**Solution:** Be specific. "We achieve 15% higher accuracy than the strongest baseline on ImageNet."

### Pitfall 2: Missing Ablations
**Problem:** Claiming design choices are important without evidence.
**Solution:** Include ablation studies. Remove each component and measure the performance drop.

### Pitfall 3: Poor Information Flow
**Problem:** Sentences feel disjointed; readers get lost.
**Solution:** Apply old-to-new flow. Each sentence should start with information from the previous sentence.
**Reference:** `references/sentence_clarity.md`

### Pitfall 4: Weak Stress Position
**Problem:** Sentences end with citations or minor details.
**Example:** ❌ "This approach significantly improves performance, as shown in [23]."
**Solution:** ✅ "As shown in [23], this approach significantly improves performance."

### Pitfall 5: Ignoring Limitations
**Problem:** Overselling without acknowledging scope or failure cases.
**Solution:** Dedicate a paragraph in Discussion to honest limitations. This increases credibility.

### Pitfall 6: Inconsistent Notation
**Problem:** Using `x` for input in one section, `X` in another.
**Solution:** Define all notation upfront. Create a notation table (appendix) if needed.
**Reference:** `references/cs_conventions.md` (Section 1)

---

## Tips for Efficient Writing

1. **Draft quickly, revise thoroughly:**
   - Don't aim for perfection in the first draft
   - Get ideas down, then refine structure and clarity

2. **Write sections out of order:**
   - Start with Methods and Results (most concrete)
   - Then Introduction and Related Work
   - Finally Abstract and Conclusion

3. **Use figures early:**
   - Create key figures (architecture, main results) before writing
   - Figures clarify your thinking and guide the narrative

4. **Get feedback early:**
   - Share drafts with co-authors and colleagues
   - Mock reviews identify issues before submission

5. **Iterate on structure:**
   - If a section feels wrong, revisit the narrative arc
   - Ensure every section advances Problem → Solution → Evidence → Implications

6. **Use the checklists proactively:**
   - Before drafting a section, read the checklist to know what to include
   - After drafting, use the checklist to verify completeness

---

## Advanced: Handling Special Cases

### Writing for Top-Tier Venues
- **Higher bar for novelty and rigor**: Ensure the contribution is significant, not incremental
- **Strong baselines**: Compare against state-of-the-art, not just simple methods
- **Comprehensive evaluation**: Multiple datasets, extensive ablations, sensitivity analyses
- **Polished presentation**: High-quality figures, clear writing, consistent notation

### Writing Rebuttals
- **Address all concerns**: Even if you disagree, engage respectfully
- **Provide evidence**: If reviewers doubt a claim, provide additional results or citations
- **Be concise**: Rebuttals have strict length limits; prioritize major issues
- **Highlight changes**: "We added an experiment (Table 3) showing..."

### Writing Thesis Chapters
- **More comprehensive**: Deeper background, extended related work, lessons learned
- **Narrative continuity**: Ensure chapters connect (e.g., Chapter 3 builds on Chapter 2)
- **Broader scope**: Can include negative results and explorations that didn't pan out
- **Use `assets/section_checklists.md` (Long-Form Paper Checklist)**

---

## Summary: The Golden Workflow

1. **Plan the narrative**: Problem → Solution → Evidence → Implications
2. **Draft section-by-section**: Use structure guidelines from `references/narrative_framework.md`
3. **Revise for clarity**: Apply principles from `references/sentence_clarity.md`
4. **Polish and comply**: Use `references/phrasebank.md` and `references/cs_conventions.md`
5. **Quality check**: Run through `assets/section_checklists.md`

**Remember:**
- Papers are stories, not templates
- Clarity comes from structure (old-to-new, topic/stress positions)
- Every claim needs evidence; every design choice needs justification
- Honest limitations increase credibility

**When in doubt, ask:**
- "Does this advance the narrative arc?"
- "Can a reader reproduce this?"
- "Is this claim supported?"
- "Is this the simplest, clearest way to express this?"

---

## Getting Started

**For a new paper:**
1. Read `references/narrative_framework.md` (Core Principle)
2. Use `assets/section_checklists.md` (Quick Pre-Draft Planning Checklist)
3. Outline your paper's narrative arc in 4 sentences (Problem, Solution, Evidence, Implications)
4. Draft section-by-section, checking checklists as you go

**For revising an existing draft:**
1. Identify the issue (structure, clarity, compliance)
2. Consult the relevant reference file
3. Apply fixes systematically
4. Re-check with the appropriate checklist

**For sentence-level issues:**
1. Read `references/sentence_clarity.md` (Three Golden Rules)
2. Apply to each problematic paragraph
3. Check: Old-to-new flow, stress position usage, subject-verb proximity

**Ready to write? Let's build a clear, compelling paper together.**
