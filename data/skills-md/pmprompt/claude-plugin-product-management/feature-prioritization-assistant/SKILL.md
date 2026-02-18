---
name: feature-prioritization-assistant
description: Calculate RICE scores and prioritize features systematically. Use when building your product roadmap and need to make data-driven prioritization decisions.
argument-hint: [features to evaluate]
---

# Feature Prioritization Assistant

## When to Use
- Building your product roadmap
- Need to choose between multiple feature ideas
- Stakeholders are debating which features to build first
- Want to make data-driven prioritization decisions
- Need to justify prioritization decisions to leadership

## What This Skill Does
Helps you systematically evaluate and prioritize features using the RICE framework (Reach, Impact, Confidence, Effort), providing scores and recommendations.

## Instructions
Help me prioritize these features using the RICE framework. For each feature, help me estimate:

1. **Reach**: How many users will this impact per month?
2. **Impact**: How much will this impact each user? (Scale: 0.25=minimal, 0.5=low, 1=medium, 2=high, 3=massive)
3. **Confidence**: How confident are we in our estimates? (Scale: 0-100%)
4. **Effort**: How many person-months will this take to build?

Then calculate the RICE score: (Reach × Impact × Confidence) / Effort

Features to evaluate:
[List your features with any context you have]

## Best Practices
- Gather data on current user behavior before estimating Reach
- Base Impact on user research and pain point severity
- Be honest about Confidence levels - lower confidence for assumptions
- Include design, development, and testing time in Effort estimates
- Revisit estimates after initial discovery work
- Consider dependencies between features

## Example
**Input:** 5 features (notifications, dark mode, API access, mobile app, analytics dashboard)
**Output:** RICE scores calculated for each, ranked list with reasoning, recommendations on which to prioritize, and suggestions for validating assumptions on low-c...
