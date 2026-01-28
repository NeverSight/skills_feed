---
name: verification-loop
description: 验证闭环提醒。当代码修改完成、Story完成、准备PR时自动激活。确保每次变更都经过验证，效率提升2-3倍。
allowed-tools: Bash, Read, Grep
---

# 验证闭环

## 核心理念

> "没有验证闭环，AI输出永远不可靠。" —— Boris Cherny (Claude Code之父)

拥有反馈回路后，最终产出质量可提升**2-3倍**。

## 验证层级

### Level 1: 即时验证（每次代码变更后）

```bash
# TypeScript项目
pnpm lint
pnpm typecheck

# Python项目
ruff check .
mypy .
```

**触发时机**：PostToolUse Hook自动执行

### Level 2: 阶段验证（Story/任务完成后）

```bash
# 单元测试
pnpm test

# 集成测试
pnpm test:integration
```

**触发方式**：
- 手动调用 `/mmo:verify`
- 或让Claude使用后台agent验证

### Level 3: 交付验证（PR前）

- 使用 `reviewer` agent（独立SESSION，客观视角）
- 运行E2E测试
- 检查CI状态

```bash
# E2E测试
pnpm test:e2e

# 或使用Playwright
npx playwright test
```

## 验证失败处理

```
┌─────────────────────────────────────┐
│          验证失败？                 │
└─────────────────────────────────────┘
                │
                ▼
┌─────────────────────────────────────┐
│  1. 不继续下一阶段                  │
│  2. 记录失败原因                    │
│  3. 分析根因                        │
│  4. 修复问题                        │
│  5. 重新验证                        │
└─────────────────────────────────────┘
                │
                ▼
        ┌──────┴──────┐
        │   通过？     │
        └──────┬──────┘
               │
        Yes ───┴─── No（循环）
               │
               ▼
        继续下一阶段
```

## 与BMAD集成

| BMAD工作流 | 验证检查点 |
|-----------|-----------|
| dev-story | 每个subtask完成后 |
| code-review | PR前必须通过 |
| sprint-status | 检查所有Story验证状态 |

## Stop Hook提醒

会话结束时自动提醒：
> "✅ 会话结束。建议运行 `/mmo:verify` 进行验证。"
