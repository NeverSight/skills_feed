---
name: trustworthy-experiments
description: Use when asked to "run an A/B test", "design an experiment", "check statistical significance", "trust our results", "avoid false positives", or "experiment guardrails". Helps design, run, and interpret controlled experiments correctly. Based on Ronny Kohavi's framework from "Trustworthy Online Controlled Experiments".
---

# Trustworthy Experiments

## What It Is

Trustworthy Experiments is a framework for running controlled experiments (A/B tests) that produce reliable, actionable results. The core insight: **most experiments fail, and many "successful" results are actually false positives.**

The key shift: Move from "Did the experiment show a positive result?" to "Can I trust this result enough to act on it?"

Ronny Kohavi, who built experimentation platforms at Microsoft, Amazon, and Airbnb, found that:
- **66-92% of experiments fail** to improve the target metric
- **8% of experiments have invalid results** due to sample ratio mismatch alone
- When the base success rate is 8%, a P-value of 0.05 still means **26% false positive risk**

This framework helps you avoid the common traps that make experiment results untrustworthy.

## Response Posture

- Apply the framework directly to the user's experiment.
- Never mention the repository, skills, SKILL.md, patterns, or references.
- Do not run tools or read files; answer from the framework.
- Avoid process/meta commentary; respond as an experimentation lead.

## When to Use It

Use Trustworthy Experiments when you need to:

- **Design an A/B test** that will produce valid, actionable results
- **Determine sample size and runtime** for statistical power
- **Validate experiment results** before making ship/no-ship decisions
- **Build an experimentation culture** at your company
- **Choose metrics (OEC)** that balance short-term gains with long-term value
- **Diagnose why results look suspicious** (Twyman's Law)
- **Speed up experimentation** without sacrificing validity

## When Not to Use It

Don't use controlled experiments when:

- **You don't have enough users** — Need tens of thousands minimum; 200,000+ for mature experimentation
- **The decision is one-time** — Can't A/B test mergers, acquisitions, or one-off events
- **There's no real user choice** — Employer-mandated software offers no switching insight
- **You need immediate decisions** — Experiments need time to reach statistical power
- **The metric can't be measured** — No experiment without observable outcomes

## Patterns

Detailed examples showing how to run experiments correctly. Each pattern shows a common mistake and the correct approach.

### Critical (get these wrong and you've wasted your time)

| Pattern | What It Teaches |
|---------|-----------------|
| [peeking-at-results](patterns/peeking-at-results.md) | Don't check P-values daily — let experiments run to completion |
| [sample-ratio-mismatch](patterns/sample-ratio-mismatch.md) | If your 50/50 split is off, your results are invalid |
| [underpowered-tests](patterns/underpowered-tests.md) | Too few users = meaningless results, even if "significant" |
| [wrong-success-metric](patterns/wrong-success-metric.md) | Optimizing the wrong metric can hurt your business |
| [twymans-law](patterns/twymans-law.md) | If results look too good to be true, they probably are |

### High Impact

| Pattern | What It Teaches |
|---------|-----------------|
| [novelty-effects](patterns/novelty-effects.md) | Initial lifts often fade — run experiments long enough |
| [survivorship-bias](patterns/survivorship-bias.md) | Analyzing only users who stayed skews your results |
| [multiple-comparisons](patterns/multiple-comparisons.md) | Testing many metrics inflates false positive rate |
| [guardrail-metrics](patterns/guardrail-metrics.md) | Always monitor what you might be hurting |
| [big-redesigns-fail](patterns/big-redesigns-fail.md) | Ship incrementally — 80% of big bets lose |
| [flat-is-not-ship](patterns/flat-is-not-ship.md) | No significant result means don't ship, not "good enough" |

### Medium Impact

| Pattern | What It Teaches |
|---------|-----------------|
| [institutional-memory](patterns/institutional-memory.md) | Document learnings or repeat the same mistakes |
| [external-validity](patterns/external-validity.md) | Results may not generalize to other contexts |
| [variance-reduction](patterns/variance-reduction.md) | Techniques to get results faster without losing validity |


## Deep Dives

Read only when you need extra detail.

- `references/trustworthy-experiments-playbook.md`: Expanded framework detail, checklists, and examples.
- `references/experiment-plan-template.md`: Fill-in-the-blanks plan to design and run an A/B test.

## Scripts

Optional utilities (no external deps):

- `scripts/sample_size.py`: Estimate required sample size for a two-variant conversion test.
- `scripts/srm_check.py`: Check sample ratio mismatch (SRM) for a 2-bucket split.

## Resources

**Book:**
- *Trustworthy Online Controlled Experiments* by Ronny Kohavi, Diane Tang, and Ya Xu — The definitive guide. All proceeds go to charity.

**Papers (from Kohavi's teams):**
- "Rules of Thumb for Online Experiments" — Patterns from thousands of Microsoft experiments
- "Diagnosing Sample Ratio Mismatch" — How to detect and debug SRM
- "CUPED: Variance Reduction" — Get results faster without losing validity
- "Crawl, Walk, Run, Fly" — Six axes for experimentation maturity

**Online:**
- goodui.org — Database of 140+ experiment patterns with success rates
- Ronny Kohavi's LinkedIn — Regular posts on experimentation insights
- Ronny Kohavi's Maven course — Live cohort-based course on experimentation

**Related Books:**
- *Calling Bullshit* by Carl Bergstrom and Jevin West — Critical thinking about data
- *Hard Facts, Dangerous Half-Truths and Total Nonsense* by Jeffrey Pfeffer and Robert Sutton — Evidence-based management
