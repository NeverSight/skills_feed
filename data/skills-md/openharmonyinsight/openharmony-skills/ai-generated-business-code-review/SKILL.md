---
name: ai-generated-business-code-review
description: Use when reviewing or scoring AI-generated business/application code quality in any language, especially when a numeric score, risk level, or must-fix checklist is requested, or when C++ code must comply with OpenHarmony C++ and security standards
---

# AI Business Code Review

## Overview
Review AI-generated business/application code for correctness, robustness, maintainability, performance, and security. Output a 0-10 score, a risk level, and a must-fix checklist. For C++ code, **REQUIRED**: use `openharmony-cpp` and `openharmony-security-review` as hard constraints.

## When to Use
- AI-generated business/app code review or quality evaluation
- Need scoring, risk level, or must-fix checklist
- C++ business code must meet OpenHarmony coding/security requirements

## Workflow
1. Identify language and code type (business vs test). If test code, use `ai-generated-ut-code-review` instead.
2. For C++: load and apply `openharmony-cpp` + `openharmony-security-review` as mandatory constraints.
3. Inspect behavior vs requirements, edge cases, error handling, resource management, and security.
4. Score by rubric, assign risk level, list must-fix items with concrete evidence (file/line or snippet).

## Scoring (0-10)
Each dimension 0-2 points. Sum = total score.

| Dimension | 0 | 1 | 2 |
| --- | --- | --- | --- |
| Correctness | Wrong/missing key behavior | Partial/assumptions | Meets requirements |
| Robustness | Crashes/leaks/unchecked errors | Some edge handling | Solid edge/error handling |
| Maintainability | Hard to read/modify | Mixed quality | Clear structure & naming |
| Performance | Inefficient hot paths | Acceptable but improvable | Efficient for expected load |
| Security | Clear vulnerabilities | Weak validation/unsafe | Safe-by-default, validated |

## Risk Levels
- **Blocker**: security漏洞、严重逻辑错误、或违反 C++ 强制规范
- **High**: 关键路径缺失、异常处理不完整、明显资源泄漏
- **Medium**: 维护性或性能风险显著
- **Low**: 轻微问题或风格一致性

## Must-Fix Checklist
- 外部输入有明确校验与错误反馈
- 关键异常路径可达且可观测（日志/错误码/异常）
- 资源释放或 RAII 保证（C++）
- C++ 场景满足 `openharmony-cpp` 与 `openharmony-security-review`

## AI-Generated Code Pitfalls (Check Explicitly)
- 需求误解、隐含前提错误
- 只覆盖 happy-path，忽略异常/边界
- 吞异常或默认值不合理
- 复制粘贴造成重复与不一致
- 过度复杂化或抽象错误

## Output Format (Required, Semi-fixed)
- `Score`: x/10 — Correctness x, Robustness x, Maintainability x, Performance x, Security x
- `Risk`: Low/Medium/High/Blocker — 简述风险原因（1 行）
- `Must-fix`:
  - [动作 + 证据]
  - [动作 + 证据]
- `Key Evidence`:
  - 引用具体函数/类/路径（1-2 条）
- `Notes`:
  - 最小修复建议或替代方案（1-2 行）

**Rules:**
- C++ 必须在 `Key Evidence` 或 `Must-fix` 中明确指出违反 `openharmony-cpp`/`openharmony-security-review` 的点
- 至少 2 条证据；证据不足需说明并降分
- 禁止只给总体评价

## Common Mistakes
- 只给总体评价，不给证据
- 忽略 C++ 强制规范
- 将风格问题当作阻断风险

## Example (Concise)
Score: 6/10 (Correctness 1, Robustness 1, Maintainability 1, Performance 1, Security 2)
Risk: High
Must-fix:
- Missing input validation in `createUser()` (null/empty, length, format)
- Error path swallows exceptions without logging
Key Evidence:
- `createUser()` accepts raw input without checks
- `catch` block is empty in `persistUser()`
Notes:
- Add explicit validation and return structured errors.
