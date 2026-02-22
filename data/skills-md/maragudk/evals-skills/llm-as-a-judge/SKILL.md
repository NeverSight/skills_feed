---
name: llm-as-a-judge
description: >
  Build, validate, and deploy LLM-as-Judge evaluators for automated quality assessment of LLM pipeline outputs.
  Use this skill whenever the user wants to: create an automated evaluator for subjective or nuanced failure modes,
  write a judge prompt for Pass/Fail assessment, split labeled data for judge development, measure judge alignment
  (TPR/TNR), estimate true success rates with bias correction, or set up CI evaluation pipelines. Also trigger when
  the user mentions "judge prompt", "automated eval", "LLM evaluator", "grading prompt", "alignment metrics",
  "true positive rate", or wants to move from manual trace review to automated evaluation. This skill covers the
  full lifecycle: prompt design → data splitting → iterative refinement → success rate estimation.
---

# LLM-as-a-Judge

Build reliable automated evaluators that use an LLM to judge the outputs of another LLM pipeline. Each judge targets a single, binary (Pass/Fail) failure mode identified during error analysis.

## When to Use LLM-as-Judge vs. Code

Choose the right evaluator type for each failure mode:

**Use code-based evaluators** when the failure is objective and deterministic:
- JSON/SQL syntax validity, regex/string matching, structural constraints, execution errors, logical checks.
- These are fast, cheap, deterministic, and interpretable.

**Use LLM-as-Judge** when the failure requires interpretation or nuance:
- Tone appropriateness, summary faithfulness, response helpfulness, explanation clarity, creative quality.
- These require a separate LLM (distinct from the application) to judge outputs.

Each failure mode gets its own dedicated evaluator. Never combine multiple criteria into a single judge prompt—this introduces ambiguity and makes diagnosis harder.

## The Full Workflow

```
1. Write Prompt Template
2. Split Labeled Data (Train / Dev / Test)
3. Iteratively Refine Prompt (measure TPR/TNR on Dev)
4. Estimate & Correct Success Rate (on Test + Unlabeled)
```

---

## Step 1: Write the Judge Prompt

A well-structured judge prompt has four essential components. Read `references/prompt-template.md` for a complete annotated example.

### 1. Clear Task and Evaluation Criterion

Focus on ONE well-scoped failure mode. Vague tasks lead to unreliable judgments.

- ❌ "Is this email good?"
- ✅ "Is the tone appropriate for a luxury buyer persona?"

### 2. Precise Pass/Fail Definitions

Define what counts as Pass (failure absent) and Fail (failure present), grounded in the failure descriptions from error analysis. Be specific about boundary conditions.

### 3. Few-Shot Examples

Include labeled examples that clearly Pass and clearly Fail. These calibrate the judge's decision boundary. Best drawn from human-labeled traces.

- Use clear-cut cases, not edge cases, for initial examples.
- For binary judgments, include at least one Pass and one Fail example.
- If using finer-grained scales (e.g., 1–3 severity), include examples for every point on the scale.

### 4. Structured Output Format

The judge responds in a consistent, machine-readable format:

```json
{
  "reasoning": "1-2 sentence explanation for the decision.",
  "answer": "Pass"
}
```

The `reasoning` field comes first—this induces chain-of-thought before the verdict, improving accuracy.

---

## Step 2: Split Labeled Data

Designing a judge resembles training a classifier, except "training" happens through prompt engineering. Split your human-labeled traces into three disjoint sets:

| Set | Purpose | Typical Allocation |
|---|---|---|
| **Training** | Pool of candidates for few-shot examples in the prompt | 10–20% |
| **Dev** | Iteratively refine the prompt; measure agreement with human labels | 40–45% |
| **Test** | Final, unbiased measurement of judge accuracy (TPR/TNR) | 40–45% |

Key rules:
- **Dev examples must never appear in the prompt.** This ensures generalization measurement.
- **Test examples are held out until the prompt is finalized.** Never look at them during development.
- In-context learning typically saturates after 1–8 well-chosen examples. Allocate more data to evaluation.
- Both Dev and Test should contain enough Pass and Fail examples—ideally 30–50 of each.
- Reusing examples across splits leads to overfitting and inflated accuracy.

If you have ~100 labeled traces (50 Pass, 50 Fail), a reasonable split: 10 training, 40 dev, 50 test.

---

## Step 3: Iteratively Refine the Prompt

This is the core loop. Think of it as tuning a classifier, but by revising text instead of adjusting parameters.

### The Refinement Loop

1. **Write a baseline prompt** using the four components above, with a few examples from the Training set.
2. **Run the judge on the Dev set.** Compare each judgment to human ground truth.
3. **Measure agreement** using TPR and TNR:
   - **TPR** = (actual Passes correctly judged Pass) / (total actual Passes)
   - **TNR** = (actual Fails correctly judged Fail) / (total actual Fails)
4. **Inspect disagreements.** Review false passes (judge said Pass, human said Fail) and false fails. Identify ambiguous criteria or missing edge cases.
5. **Refine the prompt:** Clarify Pass/Fail definitions, swap in better few-shot examples from Training, add representative edge cases.
6. **Repeat** until TPR and TNR stabilize at acceptable levels.

### Why TPR and TNR (Not Precision/Recall)

The end goal is estimating the true pass rate of the pipeline. A judge can only mis-estimate this in two ways: missing real Passes (lowers the observed rate) or passing real Fails (inflates it). TPR and TNR capture these two error modes directly.

### When to Stop

Stop when TPR and TNR reach satisfactory levels (typically >90%). Missing a real failure may be costlier than flagging a false one—adjust thresholds to your application's risk tolerance.

### If Alignment Stalls

- **Use a more capable LLM** — a larger model may resolve subtle errors.
- **Decompose the criterion** — break a complex failure into smaller, atomic checks.
- **Improve labeled data** — add diverse, high-quality examples, especially edge cases.
- **Verify label quality** — sometimes the issue is inconsistent or incorrect human labels.

Manual iteration is recommended before automation (e.g., DSPy). It builds intuition about both the failure mode and the judge's behavior. Writing the prompt forces you to externalize your specification.

---

## Step 4: Estimate True Success Rates

After finalizing the prompt, freeze it and run on the Test set to get TPR and TNR. Then use the judge on unlabeled production traces with bias correction.

Read `references/success-rate-estimation.md` for the full procedure, formula, Python code, and confidence interval calculation.

### Quick Reference

1. **Measure judge accuracy** on Test set → TPR, TNR
2. **Observe raw success rate** on unlabeled data → p_obs = k/m
3. **Correct for bias** using Rogan-Gladen formula:
   ```
   θ̂ = (p_obs + TNR - 1) / (TPR + TNR - 1)    [clipped to 0,1]
   ```
4. **Bootstrap confidence interval** — resample Test set labels B times, recompute corrected rate each time, take 2.5th/97.5th percentiles.

If TPR + TNR - 1 ≈ 0, the judge is no better than random chance and correction is invalid.

### Key Insight

Improving TPR (the judge's ability to identify true successes) narrows the confidence interval the most. Judge errors mainly inflate uncertainty rather than shifting the corrected estimate.

---

## Common Pitfalls

1. **Omitting examples from the prompt.** Without concrete examples, the judge lacks grounding. This is the most common mistake.

2. **Evaluating multiple criteria in a single prompt.** Break complex metrics into narrower, specific prompts for better alignment and diagnosability.

3. **Skipping alignment validation.** Don't assume the judge "just works." Domain-specific criteria require prompt refinement and human-labeled validation.

4. **Overfitting to labeled traces.** If few-shot examples also appear in the evaluation set, TPR/TNR will be inflated. Any trace used in the prompt must be excluded from Dev and Test.

5. **Never revisiting the judge.** Production data drifts, new failure modes emerge, and LLM updates shift behavior. Periodically re-validate.

6. **Not pinning the judge model version.** In CI pipelines, pin the exact model version (e.g., `claude-sonnet-4-5-20250929`) to prevent results from fluctuating due to unannounced updates.

---

## Long-Document Considerations

When judging outputs from long-document pipelines:
- Don't feed the full document into the judge — use only the relevant portion (e.g., the source paragraph a summary came from).
- Consider chunk-level evaluation with aggregated per-chunk judgments.
- Make rubrics especially clear about what "correct" means since the judge won't see the full context.

---

## CI Integration

For continuous integration, build a golden dataset of curated input examples with reference outputs. On each pipeline change:
1. Run all golden inputs through the pipeline.
2. Evaluate outputs with your suite of automated evaluators (code-based + LLM-as-Judge).
3. Pin the judge model version to prevent CI flicker.
4. Include examples covering core features, known failure modes, and edge cases.

This catches regressions but does not predict overall production accuracy — its purpose is stability as the pipeline evolves.
