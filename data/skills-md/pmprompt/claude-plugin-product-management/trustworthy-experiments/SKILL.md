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

- **You don't have enough users** — Need tens of thousands minimum
- **The decision is one-time** — Can't A/B test mergers or acquisitions
- **There's no real user choice** — Employer-mandated software
- **You need immediate decisions** — Experiments need time
- **The metric can't be measured** — No experiment without observable outcomes

## Resources

**Book:**
- *Trustworthy Online Controlled Experiments* by Ronny Kohavi, Diane Tang, and Ya Xu
