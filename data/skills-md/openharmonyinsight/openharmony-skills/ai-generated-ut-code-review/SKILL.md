---
name: ai-generated-ut-code-review
description: Use when reviewing or scoring AI-generated unit tests/UT code, especially when coverage, assertion effectiveness, or test quality is in question and a numeric score, risk level, or must-fix checklist is needed
---

# AI UT Code Review

## Overview
Review AI-generated unit tests for effectiveness, coverage, assertions, negative cases, determinism, and maintainability. Output a 0-10 score, a risk level, and a must-fix checklist. Overall line coverage **must be >= 80%**; otherwise risk is at least High.

## When to Use
- AI-generated UT/test code review or quality evaluation
- Need scoring, risk level, or must-fix checklist
- Questions about coverage or assertion validity

## Workflow
1. Confirm tests target the intended business code and key paths.
2. Check overall line coverage (>= 80% required).
3. Inspect assertions for behavioral validity; flag missing/ineffective assertions.
4. Verify negative/edge cases and determinism (no env/time dependency).
5. Score by rubric, assign risk, list must-fix items with evidence.

## Scoring (0-10)
Each dimension 0-2 points. Sum = total score.

| Dimension | 0 | 1 | 2 |
| --- | --- | --- | --- |
| Coverage | < 80% | 80%+ but shallow | 80%+ and meaningful |
| Assertion Quality | No/invalid assertions | Some weak assertions | Behavior-anchored assertions |
| Negative & Edge | Missing | Partial | Comprehensive |
| Data & Isolation | Flaky/env-dependent | Mixed | Deterministic, isolated |
| Maintainability | Hard to read/modify | Mixed quality | Clear structure & naming |

## Risk Levels
- **Blocker**: Coverage < 80% AND key paths untested, or tests have no meaningful assertions
- **High**: Coverage < 80% OR assertions largely ineffective
- **Medium**: Coverage OK but weak edge cases or fragile design
- **Low**: Minor improvements

## Must-Fix Checklist
- Overall line coverage >= 80%
- Each test has at least one behavior-relevant assertion
- Negative/exception cases exist for core logic
- Tests are deterministic and repeatable

## AI-Generated Test Pitfalls (Check Explicitly)
- No assertions or assertions unrelated to behavior (e.g., only not-null)
- Over-mocking hides real behavior
- Only happy-path coverage
- Tests depend on time/network/env
- Missing verification of side effects

## Output Format (Required, Semi-fixed)
- `Score`: x/10 — Coverage x, Assertion Quality x, Negative & Edge x, Data & Isolation x, Maintainability x
- `Risk`: Low/Medium/High/Blocker — 简述原因（1 行）
- `Must-fix`:
  - [动作 + 证据]
  - [动作 + 证据]
- `Key Evidence`:
  - 引用具体测试用例名或覆盖率报告摘要（1-2 条）
- `Notes`:
  - 最小修复建议或替代方案（1-2 行）

**Rules:**
- 覆盖率 < 80% 风险至少 High，并必须列入 `Must-fix`
- 无断言/无效断言直接提升风险级别，必须列入 `Must-fix`
- 至少 2 条证据；证据不足需说明并降分

## Common Mistakes
- 仅报告覆盖率，不评价断言有效性
- 把日志输出当成断言
- 忽略失败路径/异常路径

## Example (Concise)
Score: 5/10 (Coverage 1, Assertion 0, Negative 1, Data 2, Maintainability 1)
Risk: High
Must-fix:
- Tests for `parseConfig()` contain no behavior assertions (only logs)
- No negative cases for malformed input
Key Evidence:
- `parseConfig()` tests only assert no crash
- Coverage report shows 62% lines
Notes:
- Add assertions on outputs and side effects; add invalid input tests.
