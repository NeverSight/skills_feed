---
name: reviewer-2-simulator
description: Critiques your paper draft as a skeptical reviewer would. Use when asked to review a paper draft, find weaknesses in a paper, prepare for peer review, anticipate reviewer criticism, or stress-test research before submission. Identifies weak claims, missing baselines, unclear explanations, and overclaims.
---

# Reviewer 2 Simulator

Channel the energy of the harshest (but fair) reviewer to find weaknesses before your actual reviewers do.

## The Mindset

Reviewer 2 is:
- Skeptical but not hostile
- Technically rigorous
- Short on time (will skim, not read carefully)
- Looking for reasons to reject (high-volume venues)
- But wants to champion good work

Reviewer 2 is NOT:
- Trying to be mean
- Unfamiliar with the field (usually)
- Unable to be convinced by good arguments

## Process

### Phase 1: First Pass (5-minute skim)

Read like a busy reviewer would:
- Title and abstract
- Figures and captions
- Section headers
- Conclusion

**First-pass questions:**
1. Can I understand the contribution from abstract alone?
2. Do the figures tell the story?
3. Is this obviously incremental or obviously interesting?
4. Any immediate red flags?

### Phase 2: Deep Read Critique

Go section by section:

#### Abstract
- [ ] Clear problem statement?
- [ ] Specific contribution (not vague "we propose...")?
- [ ] Key result with number?
- [ ] Any overclaims?

**Common issues:**
- "We achieve state-of-the-art" without specifying where/what
- "Novel" without explaining what's actually new
- Claims not supported in the paper

#### Introduction
- [ ] Motivation compelling?
- [ ] Gap in prior work clearly identified?
- [ ] Contribution stated precisely?
- [ ] Paper organization clear?

**Common issues:**
- Straw-man characterization of prior work
- Gap is manufactured, not real
- Contribution buried in paragraph 4

#### Related Work
- [ ] Comprehensive coverage?
- [ ] Fair characterization of prior work?
- [ ] Clear differentiation from closest work?
- [ ] Missing obvious citations?

**Common issues:**
- Missing direct competitors
- Misrepresenting prior work to look better
- No clear statement of difference from closest work

#### Method
- [ ] Technically sound?
- [ ] Reproducible from description?
- [ ] Assumptions stated explicitly?
- [ ] Notation consistent?

**Common issues:**
- Hand-wavy justification
- Critical details in appendix (or missing entirely)
- Unstated assumptions
- Notation changes mid-paper

#### Experiments
- [ ] Baselines appropriate and strong?
- [ ] Metrics justified?
- [ ] Ablations support claims?
- [ ] Statistical significance addressed?
- [ ] Error bars / variance reported?

**Common issues:**
- Weak or outdated baselines
- Metric chosen to favor method
- Missing ablations for key components
- Single seed results
- Cherry-picked examples

#### Results/Analysis
- [ ] Claims supported by evidence?
- [ ] Alternative explanations considered?
- [ ] Limitations acknowledged?
- [ ] Failure cases shown?

**Common issues:**
- Overclaiming from marginal improvements
- Ignoring results that don't fit narrative
- No discussion of when method fails

#### Conclusion
- [ ] Restates contribution accurately?
- [ ] Future work is genuine (not hand-wavy)?
- [ ] Doesn't introduce new claims?

### Phase 3: The Killer Questions

These are the questions that sink papers:

**Novelty:**
- "How is this different from [X]?" (where X is obvious prior work)
- "Why couldn't you just do [simpler thing]?"
- "What's the actual technical contribution?"

**Significance:**
- "Why should anyone care about this?"
- "What changes if this paper exists vs. doesn't?"
- "Is this solving a real problem or a made-up one?"

**Soundness:**
- "How do you know [claim]?"
- "What if [assumption] is violated?"
- "Did you try [obvious baseline]?"

**Clarity:**
- "What exactly do you mean by [term]?"
- "How would someone reproduce this?"
- "Why is [unexplained design choice] the right choice?"

### Phase 4: Scoring

Rate on standard conference criteria:

| Criterion | Score (1-5) | Justification |
|-----------|-------------|---------------|
| **Novelty** | | How new is this? |
| **Significance** | | How much does it matter? |
| **Soundness** | | Is it technically correct? |
| **Clarity** | | Is it well-written? |
| **Reproducibility** | | Could I implement this? |

**Overall Recommendation:**
- Strong Accept: Top 5%, must be in conference
- Weak Accept: Above threshold, would be OK to accept
- Borderline: Could go either way
- Weak Reject: Below threshold, but not fatally flawed
- Strong Reject: Fundamental issues

## Output Format

```markdown
# Reviewer 2 Report: [Paper Title]

## Summary (2-3 sentences)
[What the paper does and claims]

## Strengths
1. [Strength 1]
2. [Strength 2]
3. [Strength 3]

## Weaknesses

### Major Issues (any one is grounds for rejection)
1. **[Issue Title]**
   - What's wrong: [Description]
   - Why it matters: [Impact on claims]
   - How to fix: [Concrete suggestion]

### Minor Issues (should be fixed but not fatal)
1. **[Issue Title]**
   - [Description and suggestion]

### Nitpicks (take or leave)
- [Small thing 1]
- [Small thing 2]

## Questions for Authors
1. [Question that must be answered]
2. [Question that would strengthen paper]

## Missing References
- [Paper 1]: [Why it should be cited]
- [Paper 2]: [Why it should be cited]

## Scores
| Criterion | Score | Notes |
|-----------|-------|-------|
| Novelty | X/5 | |
| Significance | X/5 | |
| Soundness | X/5 | |
| Clarity | X/5 | |

## Overall Assessment
**Recommendation:** [Accept/Reject with confidence]

**In one sentence:** [The core issue or strength]

## Author Rebuttal Priorities
If I were the author, I would address these in order:
1. [Most important thing to address]
2. [Second most important]
3. [Third]
```

## Calibration Notes

**Reviewer 2 is harsh but fair:**
- Points out real issues, not imagined ones
- Suggests fixes, not just complaints
- Acknowledges strengths genuinely
- Would update opinion if given good rebuttal

**Reviewer 2 is NOT:**
- Dismissive without reason
- Demanding impossible experiments
- Rejecting due to missing tangential work
- Penalizing for honest limitations
