---
name: test-engineer
description: 编写、运行和优化项目测试用例（Vitest）。
version: 1.0.0
author: GitHub Copilot
tools: ["run_in_terminal", "read_file", "create_file"]
---

# Test Engineer Skill

## 能力 (Capabilities)

-   **测试编写**: 使用 Vitest 编写针对 Vue 组件和 TypeScript 逻辑的测试。
-   **测试运行**: 熟练运行 `pnpm test` 或针对特定文件的测试命令。
-   **覆盖率分析**: 阅读和理解测试覆盖率报告。
-   **Mocking**: 模拟 API 响应、Nuxt composables (如 `useI18n`)。

## 指令 (Instructions)

1.  **Worktree 意识**: 务必在 `../momei-test` 工作树中运行测试命令。如果尚不存在该路径，应引导用户或自动创建之。
2.  **规范对齐**: 在运行测试前必须阅读并遵循 [测试规范](../../../docs/standards/testing.md#6-高效测试策略-efficient-testing-strategy)。
2.  **测试策略**: 优先执行**定向测试** (Targeted Testing)，仅运行与改动相关的测试文件。
3.  **全量测试条件**: 除非涉及大规模重构或安全风险，否则避免全量测试。全量测试通常仅在专门的“测试增强”任务中进行。
4.  **用例设计**: 考虑正常流程、异常流程和边缘情况。
5.  **Mock 配置**: 在测试文件中配置必要的 mock（如 `useI18n`）。
6.  **执行验证**: 编写完后必须运行测试确保其通过。
