---
name: feat-dev
description: 提供 7 阶段功能开发工作流（需求理解、代码探索、澄清问题、架构设计、实施、质量审查、总结）。适用于新功能实施、API/数据库/服务架构设计、代码重构和多模块开发。当用户提出功能开发、架构设计或代码重构需求时触发。
---

# 功能开发技能

提供系统化的 7 阶段功能开发工作流，确保从需求理解到质量交付的完整过程。

---

## 快速开始

**工作流** (阶段 1-7)：
```
需求理解 → 代码探索 → 澄清问题 → 架构设计 → 实施 → 质量审查 → 总结
```

**核心特性**：
- 深度分析：复杂需求使用 sequential-thinking
- 并行 agents：code-explorer、code-architect、code-reviewer
- Task List 管理：进度可视化、断点恢复
- MCP 工具：优先使用 context7、exa，自动降级

**与 requirement-analysis 的区别**：
- 本技能：完整实施流程，从需求到代码交付
- requirement-analysis：专注分析和规划，不包含代码实施

---

## Task List 管理

本技能自动管理任务列表，提供进度可视化和断点恢复能力。

**详细指南**：[Task List 管理](references/task-list-management.md)

**基础模式**：
```markdown
# 开始阶段时
tasks = TaskList()
task = findTaskBySubject(tasks, "阶段 X: 阶段名称")
TaskUpdate(task.id, status="in_progress", owner="feat-dev")

# 完成阶段时
TaskUpdate(task.id, status="completed")
```

---

## Ultrathink 使用指南

**工具**：`mcp__sequential-thinking__sequentialthinking`

**何时使用**：
- ✅ 阶段1：需求涉及多个模块、复杂业务逻辑、描述模糊
- ✅ 阶段4（模式1）：简单/中等需求，主进程必须使用
- ❌ 阶段4（模式2）：复杂需求多方案设计，不使用主进程 ultrathink
- ❌ 简单 CRUD 或字段添加可跳过

**使用方法**：
```markdown
阶段1使用时：
- 分解需求组件、识别依赖关系、分析潜在风险

阶段4（模式1）使用时：
- 分析可能的实现路径
- 做出关键架构决策
- 识别主要风险和权衡点
- 确定推荐的架构方向
```

---

## 专门化 Agents

本技能使用三个专门化 agents 提升效率：
- **code-explorer**：深入探索代码库
- **code-architect**：设计详细架构方案
- **code-reviewer**：全面审查代码质量

**详细指南**：[专门化 Agents](references/specialized-agents.md)

---

## 工作流程

### 阶段 1: 需求理解

**目标**：全面理解用户需求

**执行要点**：
- 识别核心功能、业务实体、API 端点、业务规则、集成点
- 根据复杂度决定是否使用 ultrathink
- 可选：搜索类似实现案例（exa/WebSearch）

**产出**：需求理解摘要

**详细指南**：[阶段 1: 需求理解](references/phase-1-discovery.md)

---

### 阶段 2: 代码库探索

**目标**：深入理解现有代码库

**执行要点**：
1. **首要任务**：查找并阅读项目根目录的 CLAUDE.md 文件
2. **并行启动 2-3 个 code-explorer agents**：
   - 必须在单个消息中发起所有 Task 调用
   - 每个 Task 设置 `run_in_background: true`
   - Agent 分工：数据层、业务逻辑层、API 层
3. **读取所有 agent 识别的文件** - 主进程必须亲自阅读
4. **整合发现**：汇总探索结果、识别设计模式、梳理技术栈
5. 可选：使用 context7 查询依赖库文档

**产出**：代码库探索报告

**详细指南**：[阶段 2: 代码库探索](references/phase-2-exploration.md)

**并行示例**：[并行模式指南](../requirement-analysis/references/parallel-patterns.md)

---

### 阶段 3: 澄清问题

**目标**：填补需求空白，解决模糊和歧义

**执行要点**：
- 识别需要澄清的情况：模糊需求、多实施方法、业务规则细节、技术选型
- **必须**使用 AskUserQuestion 工具
- 记录用户反馈，更新需求理解

**产出**：澄清结果或"无需澄清"

**详细指南**：[阶段 3: 澄清问题](references/phase-3-clarify.md)

---

### 阶段 4: 架构设计

**目标**：设计详细的实施方案

**关键检查点**：最关键检查点 - 必须等待用户明确确认后才能开始实施

**步骤 1: 准备结构化上下文**
- 整理阶段 1-3 的结果（需求、探索发现、用户澄清）
- 使用结构化模板确保完整性

**步骤 2: 判断需求复杂度**

**简单/中等需求** → **模式1：单方案设计**
- 单一功能或 2-3 个模块
- 实现路径清晰
- 不涉及重大架构变更

**复杂需求** → **模式2：多方案设计**
- 多种明显不同的实现路径
- 重大架构权衡
- 影响 3 个以上核心模块
- 引入新技术或架构模式

**步骤 3: 执行对应设计模式**

**模式1：单方案设计**
1. 主进程使用 ultrathink 深度分析
2. 启动单个 code-architect agent 细化设计
3. 读取推荐的架构文件
4. 向用户展示单一方案并请求确认

**模式2：多方案设计**
1. 并行启动 2-3 个 code-architect agents（必须在单个消息中）
2. 读取所有 agents 推荐的架构文件
3. 整合所有方案，对比优劣势
4. 向用户展示多方案对比并请求选择

**产出**：
- 模式1：主进程 ultrathink 分析 + 单个详细设计方案
- 模式2：多方案对比 + 权衡分析 + 推荐意见

**详细指南**：[阶段 4: 架构设计](references/phase-4-design.md)

---

### 阶段 5: 实施

**目标**：按照架构设计实施功能

**前置条件**：用户已确认架构方案

**执行要点**：
- 按阶段 4 规划的步骤实施（数据层 → 数据访问层 → 服务层 → DTO → API 层 → 验证）
- 严格遵循 CLAUDE.md 规范和现有模式
- 每完成一个模块及时测试
- 可选：使用 context7 查询 API 文档

**实施原则**：
- 保持代码简洁，避免过度设计
- 安全第一（防止注入、XSS、认证授权等）
- 遵循项目现有模式

**产出**：完整的功能实现代码

**详细指南**：[阶段 5: 实施](references/phase-5-implement.md)

---

### 阶段 6: 质量审查

**目标**：确保代码质量

**执行要点**：
1. **并行启动 3 个 code-reviewer agents**：
   - 必须在单个消息中发起所有 Task 调用
   - 每个 Task 设置 `run_in_background: true`
   - Reviewer 分工：Bug/逻辑、代码风格、规范遵循
2. **整合审查结果**：收集发现、去重、按严重性分类
3. **向用户展示发现并询问决策**：
   - 选项 A：立即修复所有高严重性问题（推荐）
   - 选项 B：立即修复高置信度 bug，其他稍后处理
   - 选项 C：按现状继续，记录问题供后续处理
4. **根据用户决策执行**：按选择的策略修复问题

**修复策略**：
- 必须修复：高置信度 bug（≥80%）、严重规范违反
- 应该修复：中置信度 bug（60-79%）、严重质量问题
- 可选修复：一般质量问题、低置信度 bug（<60%）

**产出**：审查报告、修复记录、质量评分

**详细指南**：[阶段 6: 质量审查](references/phase-6-review.md)

---

### 阶段 7: 总结

**目标**：全面总结实施成果

**输出内容**：
1. **变更摘要**：实现了什么功能
2. **修改文件列表**：所有新增和修改的文件
3. **API 变更**：新增的 API 端点
4. **数据库变更**：新增或修改的表/字段
5. **后续建议**：测试计划、部署注意事项、CHANGELOG、优化建议
6. **工具使用情况**：MCP 工具和 agents 使用记录

**产出**：完整总结文档

**详细指南**：[阶段 7: 总结](references/phase-7-summary.md)

---

## 工作流控制

**关键执行规则**：
- 必须严格按照 1→2→3→4→5→6→7 的顺序执行
- 每个阶段必须完整执行，禁止跳过
- 在关键检查点（阶段3→4，阶段4→5）必须等待用户输入

**关键检查点**：
- **阶段 3 → 4**：如使用 AskUserQuestion，必须等待用户回应
- **阶段 4 → 5**：最关键检查点 - 必须等待用户明确确认架构方案
- **阶段 5 → 6**：实施完成后进入审查

**详细指南**：[工作流控制](references/workflow-control.md)

---

## 重要原则

1. **自适应语言交互**：根据用户的 Claude 语言设置和输入语言沟通
2. **严格遵循 CLAUDE.md**：必须阅读并遵守项目规范
3. **主动提问**：不清楚的地方必须澄清（阶段 3）
4. **善用 ultrathink**：复杂分析必须使用 Sequential Thinking
5. **并行执行**：探索和审查阶段并行启动多个 agents
6. **等待确认**：架构设计确认后才开始实施（阶段 4 → 5）
7. **质量把关**：实施后必须进行代码审查（阶段 6）
8. **不中断工作流**：MCP 工具不可用时立即使用降级方案

---

## 参考文档

### 阶段详细指南
- [阶段 1: 需求理解](references/phase-1-discovery.md)
- [阶段 2: 代码库探索](references/phase-2-exploration.md)
- [阶段 3: 澄清问题](references/phase-3-clarify.md)
- [阶段 4: 架构设计](references/phase-4-design.md)
- [阶段 5: 实施](references/phase-5-implement.md)
- [阶段 6: 质量审查](references/phase-6-review.md)
- [阶段 7: 总结](references/phase-7-summary.md)

### 辅助文档
- [Task List 管理](references/task-list-management.md)
- [专门化 Agents](references/specialized-agents.md)
- [Ultrathink 使用](references/ultrathink-usage.md)
- [MCP 工具集成](references/mcp-tools.md)
- [工作流控制](references/workflow-control.md)
- [快速参考](references/quick-reference.md)
- [故障排查](references/troubleshooting.md)
- [输出格式模板](assets/output-template.md)
