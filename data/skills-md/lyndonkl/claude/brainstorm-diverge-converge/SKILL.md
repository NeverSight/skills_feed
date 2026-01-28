---
name: brainstorm-diverge-converge
description: Use when you need to generate many creative options before systematically narrowing to the best choices. Invoke when exploring product ideas, solving open-ended problems, generating strategic alternatives, developing research questions, designing experiments, or when you need both breadth (many ideas) and rigor (principled selection). Use when user mentions brainstorming, ideation, divergent thinking, generating options, or evaluating alternatives.
---

# Brainstorm Diverge-Converge

## Table of Contents

- [Purpose](#purpose)
- [When to Use This Skill](#when-to-use-this-skill)
- [What is Brainstorm Diverge-Converge?](#what-is-brainstorm-diverge-converge)
- [Workflow](#workflow)
  - [1. Gather Requirements](#1--gather-requirements)
  - [2. Diverge (Generate Ideas)](#2--diverge-generate-ideas)
  - [3. Cluster (Group Themes)](#3--cluster-group-themes)
  - [4. Converge (Evaluate & Select)](#4--converge-evaluate--select)
  - [5. Document & Validate](#5--document--validate)
- [Common Patterns](#common-patterns)
- [Guardrails](#guardrails)
- [Quick Reference](#quick-reference)

## Purpose

Apply structured divergent-convergent thinking to generate many creative options, organize them into meaningful clusters, then systematically evaluate and narrow to the strongest choices. This balances creative exploration with disciplined decision-making.

## When to Use This Skill

- Generating product or feature ideas
- Exploring solution approaches for open-ended problems
- Developing research questions or hypotheses
- Creating marketing or content strategies
- Identifying strategic initiatives or opportunities
- Designing experiments or tests
- Naming products, features, or projects
- Developing interview questions or survey items
- Exploring design alternatives (UI, architecture, process)
- Prioritizing from a large possibility space
- Overcoming creative blocks
- When you need both quantity (many options) and quality (best options)

**Trigger phrases:** "brainstorm", "generate ideas", "explore options", "what are all the ways", "divergent thinking", "ideation", "evaluate alternatives", "narrow down choices"

## What is Brainstorm Diverge-Converge?

A three-phase creative problem-solving method:

- **Diverge (Expand)**: Generate many ideas without judgment or filtering. Focus on quantity and variety. Defer evaluation.

- **Cluster (Organize)**: Group similar ideas into themes or categories. Identify patterns and connections. Create structure from chaos.

- **Converge (Select)**: Evaluate ideas against criteria. Score, rank, or prioritize. Select strongest options for action.

**Quick Example:**

```markdown
# Problem: How to improve customer onboarding?

## Diverge (30 ideas)
- In-app video tutorials
- Interactive walkthroughs
- Email drip campaign
- Live webinar onboarding
- 1-on-1 concierge calls
- ... (25 more ideas)

## Cluster (6 themes)
1. **Self-serve content** (videos, docs, tooltips)
2. **Interactive guidance** (walkthroughs, checklists)
3. **Human touch** (calls, webinars, chat)
4. **Motivation** (gamification, progress tracking)
5. **Timing** (just-in-time help, preemptive)
6. **Social** (community, peer examples)

## Converge (Top 3)
1. Interactive walkthrough (high impact, medium effort) - 8.5/10
2. Email drip campaign (medium impact, low effort) - 8.0/10
3. Just-in-time tooltips (medium impact, low effort) - 7.5/10
```

## Workflow

Copy this checklist and track your progress:

```
Brainstorm Progress:
- [ ] Step 1: Gather requirements
- [ ] Step 2: Diverge (generate ideas)
- [ ] Step 3: Cluster (group themes)
- [ ] Step 4: Converge (evaluate and select)
- [ ] Step 5: Document and validate
```

**Step 1: Gather requirements**

Clarify topic/problem (what are you brainstorming?), goal (what decision will this inform?), constraints (must-haves, no-gos, boundaries), evaluation criteria (what makes an idea "good" - impact, feasibility, cost, speed, risk, alignment), target quantity (suggest 20-50 ideas), and rounds (single session or multiple rounds, default: 1).

**Step 2: Diverge (generate ideas)**

Generate 20-50 ideas without judgment or filtering. Suspend criticism (all ideas valid during divergence), aim for quantity and variety (different types, scales, approaches), and use creative prompts: "What if unlimited resources?", "What would competitor do?", "Simplest approach?", "Most ambitious?", "Unconventional alternatives?". Output: Numbered list of raw ideas. For simple topics → generate directly. For complex topics → Use `resources/template.md` for structured prompts.

**Step 3: Cluster (group themes)**

Organize ideas into 4-8 distinct clusters by identifying patterns, creating categories (mechanism, user/audience, timeline, effort, risk, strategic objective), naming clusters clearly, and checking coverage (distinct approaches). Fewer than 4 = not enough variety, more than 8 = too fragmented. Output: Ideas grouped under cluster labels.

**Step 4: Converge (evaluate and select)**

Define criteria (from step 1), score ideas on criteria (1-10 or Low/Med/High scale), rank by total/weighted score, select top 3-5 options, and document tradeoffs (why chosen, what deprioritized). Evaluation patterns: Impact/Effort matrix, weighted scoring, must-have filtering, pairwise comparison. See [Common Patterns](#common-patterns) for domain-specific approaches.

**Step 5: Document and validate**

Create `brainstorm-diverge-converge.md` with: problem statement, diverge (full list), cluster (organized themes), converge (scored/ranked/selected), and next steps. Validate using `resources/evaluators/rubric_brainstorm_diverge_converge.json`: verify 20+ ideas with variety, distinct clusters, explicit criteria, consistent scoring, top selections clearly better, actionable next steps. Minimum standard: Score ≥ 3.5.

## Common Patterns

**For product/feature ideation:**
- Diverge: 30-50 feature ideas
- Cluster by: User need, use case, or feature type
- Converge: Impact vs. effort scoring
- Select: Top 3-5 for roadmap

**For problem-solving:**
- Diverge: 20-40 solution approaches
- Cluster by: Mechanism (how it solves problem)
- Converge: Feasibility vs. effectiveness
- Select: Top 2-3 to prototype

**For research questions:**
- Diverge: 25-40 potential questions
- Cluster by: Research method or domain
- Converge: Novelty, tractability, impact
- Select: Top 3-5 to investigate

**For strategic planning:**
- Diverge: 20-30 strategic initiatives
- Cluster by: Time horizon or strategic pillar
- Converge: Strategic value vs. resource requirements
- Select: Top 5 for quarterly planning

## Guardrails

**Do:**
- Generate at least 20 ideas in diverge phase (quantity matters)
- Suspend judgment during divergence (criticism kills creativity)
- Create distinct clusters (avoid overlap and confusion)
- Use explicit, relevant criteria for convergence (not vague "goodness")
- Score consistently across all ideas
- Document why top ideas were selected (transparency)
- Include "runner-up" ideas (for later consideration)

**Don't:**
- Filter ideas during divergence (defeats the purpose)
- Create clusters that are too similar or overlapping
- Use vague evaluation criteria ("better", "more appealing")
- Cherry-pick scores to favor pet ideas
- Select ideas without systematic evaluation
- Ignore constraints from requirements gathering
- Skip documentation of the full process

## Quick Reference

- **Template**: `resources/template.md` - Structured prompts and techniques for diverge-cluster-converge
- **Quality rubric**: `resources/evaluators/rubric_brainstorm_diverge_converge.json`
- **Output file**: `brainstorm-diverge-converge.md`
- **Typical idea count**: 20-50 ideas → 4-8 clusters → 3-5 selections
- **Common criteria**: Impact, Feasibility, Cost, Speed, Risk, Alignment
