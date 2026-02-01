---
name: project-referee
description: Critiques ML conference papers with reviewer-style feedback. Use when users want to anticipate reviewer concerns, identify weaknesses, check claim-evidence gaps, or find missing citations.
---

# Project Referee

## Review Workflow

### Step 1: Assess Manuscript Stage

Ask or determine the manuscript stage:
- **Early draft**: Focus on novelty, feasibility, relevance, structure
- **Mid-stage draft**: Focus on development trajectory, completeness, preliminary results
- **Final submission**: Apply full review criteria (see [references/reviewer-instructions.md](references/reviewer-instructions.md))

### Step 2: Stage-Specific Review

**Early Draft Protocol:**
1. Assess core contribution novelty and significance
2. Evaluate method feasibility with current technology
3. Check alignment with venue scope
4. Review logical structure and completeness
5. Identify major missing components
6. Suggest high-level direction

**Mid-Stage Protocol:**
1. Evaluate development progress
2. Check section completeness
3. Assess preliminary results against claims
4. Review literature coverage
5. Identify specific weaknesses
6. Provide targeted refinements

**Final Submission Protocol:**
Apply complete review process. See [references/reviewer-instructions.md](references/reviewer-instructions.md) for the full reviewer form.

### Step 3: Search for Related Work

Proactively search for missing citations:
- Recent work in the paper's domain
- Papers with similar methods or contributions
- Relevant benchmarks and baselines
- Use WebSearch to find recent publications

### Step 4: Provide Structured Feedback

Use the output format in [references/reviewer-instructions.md](references/reviewer-instructions.md):
- Summary, Strengths, Weaknesses, Questions
- Soundness (1-4), Presentation (1-4), Contribution (1-4)
- Overall Score (1-10), Confidence (1-5)

## Neuro-Symbolic Papers

For papers combining LLMs with symbolic reasoning, see [references/neuro-symbolic-review-criteria.md](references/neuro-symbolic-review-criteria.md) for additional criteria:
- Symbolic formulation quality
- Solver selection and integration
- Faithfulness and verification
- Comparison to baselines (Logic-LM, LINC)

## References

- [references/reviewer-instructions.md](references/reviewer-instructions.md) - Full reviewer form
- [references/neuro-symbolic-review-criteria.md](references/neuro-symbolic-review-criteria.md) - Neuro-symbolic specific criteria
