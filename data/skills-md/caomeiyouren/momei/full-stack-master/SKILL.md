---
name: full-stack-master
description: 全局一体化开发与协作工作流技能，覆盖需求评估、开发、测试、质量、文档、提交、发布等全链路阶段，可集成所有基础原子技能，实现 PDTFC+ 循环自动化及分工合作优化。
version: 1.1.0
author: CaoMeiYouRen & Copilot
appliesTo: "**/*"
---

# Full Stack Master Workflow Skill

## 一、能力定位 (Capability)

- **工作流自动编排**：串联需求设计开发测试质量文档提交审核发布的全链路。
- **Git Worktree 编排**：根据任务维度（dev/test/fix/docs）自动选择物理隔离的工作目录，加速并行开发。
- **技能聚合**：集成所有核心原子技能（Todo Manager、Technical Planning、Backend Logic Expert、Vue Frontend Expert、Database Expert、Code Quality Auditor、Test Engineer、UI Validator、Conventional Committer）。
- **可复用与可拓展**：可合并新场景（如数据库迁移、API 变更、运营发布等），支持多项目切换。
- **分阶段接棒/派单**：可手动或脚本分配阶段任务给对应技能或专项 agent。

## 二、强制参考文档 (Mandatory Documentation)

在执行任何写操作 or 决策前，必须确保已读取并理解以下文档的最新内容：

- **全周期基石**：[AGENTS.md](../../../AGENTS.md) (安全红线与身份)、[AI 协作规范](../../../docs/standards/ai-collaboration.md)、[Git 规范](../../../docs/standards/git.md)
- **规划与任务**：[项目规划](../../../docs/plan/roadmap.md)、[待办事项](../../../docs/plan/todo.md)、[项目规划规范](../../../docs/standards/planning.md)
- **开发与设计**：[开发规范](../../../docs/standards/development.md)、[API 规范](../../../docs/standards/api.md)、[UI 设计](../../../docs/design/ui.md)
- **安全与质量**：[安全规范](../../../docs/standards/security.md)、[测试规范](../../../docs/standards/testing.md)

## 三、标准 PDTFC+ 2.0 工作流 (Standard Workflow)

1. **P (Plan) - 需求分析与规划**
    1. **读取文档**：确认 `todo.md` 和 `roadmap.md`。
    2. **意图抽离**：启动采访追问程序同步需求。
    3. **方案设计**：使用 `technical-planning` 规划改动清单，并使用 `todo-manager` 更新状态。
    - **技能**：`requirement-analyst`、`todo-manager`、`technical-planning`

2. **D (Do) - 开发实现**
    1. **核心实现**：遵循 [开发规范](../../../docs/standards/development.md)；若涉及持久化，优先开发 `database-expert` 实体。
    2. **自检修复**：开发完成通过 `code-quality-auditor` 消除 Lint 和类型报错。
    - **技能**：`database-expert`、`backend-logic-expert`、`vue-frontend-expert`、`code-quality-auditor`

3. **A (Audit) - 代码审计**
    1. **安全审计**：扫描注入、越权与敏感信息。
    2. **规范审计**：对比 `todo.md` 确认功能点与规划一致。
    - **技能**：`code-quality-auditor`、`security-guardian`

4. **C1 (Commit) - 功能提交**
    1. **原子提交**：使用 `conventional-committer` 执行第一次提交。消息描述统一使用**中文**或用户的语言。

5. **V (Validate) - UI 验证**
    1. **视觉准则**：浏览器验证实际渲染效果。若自动化工具失效，应向用户展示截图或请求人工验证。
    - **技能**：`ui-validator`

6. **T (Test) - 自动化测试**
    1. **定向测试**：编写并运行 Vitest 用例（测试代码也需过审计）。
    - **技能**：`test-engineer`

7. **C2 (Commit) - 测试提交**
    1. **最终交付**：提交测试代码。消息描述统一使用**中文**或用户的语言。

8. **F (Finish) - 任务完结**
    1. **文档更新**：更新 `todo.md` 状态，并归并项目变更文档。
    - **技能**：`todo-manager`、`documentation-specialist`

4. **质量检测与审查 (Test/Review)**
    - **要求**：执行测试前，**必须读取** [测试规范](../../../docs/standards/testing.md)。
    - **任务**：运行 `pnpm lint`, `pnpm typecheck` 以及**定向/按需测试**。
    - **策略**: 遵循 [高效测试策略](../../../docs/standards/testing.md#6-高效测试策略-efficient-testing-strategy)，除非必要否则不执行全量测试。
    - **技能**：`quality-guardian`、`test-engineer`、`code-reviewer`

5. **问题修复 (Fix)**
    - **目标**：消除上阶段发现的所有缺陷。
    - **技能**：`nuxt-code-editor`

6. **功能提交 (Commit - Phase 1)**
    - **目标**：在通过核心质量检查后提交业务逻辑。
    - **任务**：使用 Conventional Commits 规范（中文）提交。
    - **要求**: 遵循 [提交规模与原子化改动](../../../docs/standards/development.md#27-提交规模与原子化改动-commit-scale--atomic-changes)，确保一次提交对应一个 Todo，文件数 < 10。
    - **技能**：`conventional-committer`

7. **测试增强 (Enhance)**
    - **目标**：补齐测试用例，提升代码覆盖率。
    - **任务**：为新功能补齐正向、反向及边缘场景的 Vitest 用例。
    - **技能**：`test-engineer`

8. **测试提交 (Commit - Phase 2)**
    - **目标**：将增强后的测试代码入库。
    - **技能**：`conventional-committer`

## 四、需求挖掘方法论 (Intent Extraction Methodology)

1. **逐级递进**：先锁定整体结构和目标，再深入到具体实现细节。
2. **单点突破**：一次仅问一个问题，待用户回答后再进行下一步追问。
3. **循环校验**：当用户回答不清晰时，尝试换一种表述方式进行确认。
4. **意图抽离**：分析用户想要什么背后的为什么，提供更优专业建议。

## 五、技能引用（Each Sub-Skill Reference）

- [context-analyzer](../context-analyzer/SKILL.md)
- [nuxt-code-editor](../nuxt-code-editor/SKILL.md)
- [test-engineer](../test-engineer/SKILL.md)
- [quality-guardian](../quality-guardian/SKILL.md)
- [documentation-specialist](../documentation-specialist/SKILL.md)
- [code-reviewer](../code-reviewer/SKILL.md)
- [conventional-committer](../conventional-committer/SKILL.md)
- [ui-validator](../ui-validator/SKILL.md)

## 六、编写规范 (Authoring Rules)

1. **Imperative & Structured**
   - 用动词+目标描述标准化每一步/每个技能的 usage section。
   - 禁止冗长废话和流程介绍型文字。

2. **明确输入输出**
   - 每步须说明本阶段输入依赖、输出产物（如文件路径、文档链接）。
   - 例：输入：docs/plan/，输出：docs/design/xx.md。

3. **可链式组合**
   - 每步技能应允许独立、或作为全局 master 调用链局部片段。
   - 部分技能支持多角色协同（如测试、文档可并行）。

4. **安全检查与通用异常处理**
   - 强行插入 typecheck、lint 等质量关卡，禁止在未检测前进入提交/发布环节。
   - 明确安全等级和数据保护点。

5. **国际化与文档优先**
   - 所有工作流/技能创建应默认兼容 i18n 和标准文档同步动作。

## 七、模板用法 (Usage Example)

```yaml
workflow:
  - step: "需求分析"        # context-analyzer, documentation-specialist
  - step: "功能开发"        # nuxt-code-editor
  - step: "UI 验证"         # ui-validator
  - step: "质量检测"        # quality-guardian, code-reviewer
  - step: "功能提交"        # conventional-committer
  - step: "测试补充"        # test-engineer
  - step: "测试提交"        # conventional-committer
```
