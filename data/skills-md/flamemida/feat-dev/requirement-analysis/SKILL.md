---
name: requirement-analysis
description: 提供系统化的需求分析工作流，用于理解需求、探索代码库、澄清问题、使用深度分析并在编码前展示实施计划。适用于功能开发、API设计、数据库设计、模块开发和功能修改等场景。当用户提出功能开发、API设计、数据库设计等需求时自动触发此技能。根据用户设置和输入语言进行交互。
---

# 需求分析技能 (Requirement Analysis Skill)

本技能提供系统化的需求分析工作流，确保在实施前彻底理解需求。

---

## 快速开始

**9 阶段工作流概览**：
```
需求理解 → 代码探索 → 外部资源研究 → 澄清问题 → 深度分析 → 展示计划 → 实施开发 → 代码审查 → 总结
```

**核心特性**：
- 智能使用 ultrathink 进行深度分析
- 支持并行探索和审查模式
- 集成外部资源查询（context7、exa）
- 结构化输出和实施计划
- **Task list 自动管理：进度可视化、工作流透明化**
- **断点恢复：支持中断后继续执行**
- **任务可复用：任务列表可被引用**
- 自适应语言交互

**触发方式**：
- 自动触发：用户提出功能开发、API设计等需求
- 手动触发：`/requirement-analysis`、`使用需求分析skill`

---

## Task List 集成

本 skill 自动管理任务列表，提供进度可视化、工作流透明化、断点恢复和任务可复用功能。

**详细指南**：[Task List 管理](references/task-list-management.md)

## 工作流程概览

### 阶段 1: 需求理解

**目标**：全面理解用户需求

**任务管理**：
```markdown
# 开始阶段时
tasks = TaskList()
task = findTaskBySubject(tasks, "阶段 1: 需求理解")
TaskUpdate(task.id, status="in_progress", owner="requirement-analysis")

# 完成阶段时
TaskUpdate(task.id, status="completed")
```

**执行要点**：
- 识别核心功能、业务实体、API 端点、业务规则
- 根据复杂度决定是否使用 ultrathink
- 记录需求理解摘要

**何时使用 ultrathink**：
- 需求涉及多个模块或系统集成
- 需求包含复杂业务逻辑或工作流
- 需求描述模糊或不完整
- 简单 CRUD 或单一模块需求可跳过

---

### 阶段 2: 代码库探索

**目标**：全面探索代码库，理解项目架构和相关代码

**任务管理**：
```markdown
# 开始阶段时
tasks = TaskList()
task = findTaskBySubject(tasks, "阶段 2: 代码库探索")
TaskUpdate(task.id, status="in_progress", owner="requirement-analysis")
```

**首要任务**：查找并阅读 **CLAUDE.md** 文件

**基础模式**（简单需求）：
- 使用单个 Explore agent
- 快速定位相关代码

**并行模式**（复杂需求）：
- 同时启动 2-5 个 Explore agent
- 按架构层次、功能模块或关注点分解
- 必须在单个消息中发起所有 Task 调用
- **详细指南和示例**：[并行模式指南](references/parallel-patterns.md)

**查找内容**：
- CLAUDE.md 规范
- 相关实体和服务
- 现有模式和约定

**阶段完成**：
```markdown
# 完成阶段时
TaskUpdate(task.id, status="completed")
```

---

### 阶段 3: 外部资源研究（条件执行）

**目标**：根据需要研究外部资源，获取最新信息和最佳实践

**执行条件**（满足任一即执行）：
- 涉及新的第三方库或框架
- 需要了解行业最新实践
- 内部代码库示例不充分

**任务管理**：
```markdown
# 如果决定执行此阶段
tasks = TaskList()
task = findTaskBySubject(tasks, "阶段 3: 外部资源研究")
TaskUpdate(task.id, status="in_progress", owner="requirement-analysis")

# 如果跳过此阶段
TaskUpdate(task.id, status="completed")
# 添加说明：metadata: { note: "用户跳过" }
```

**工具使用**：
1. **网页搜索**：优先 exa MCP，降级到 WebSearch
2. **库文档**：优先 context7 MCP，降级到 WebSearch + Grep + Read

**何时跳过**：
- ⏭ 完全基于已有代码
- ⏭ 团队对技术已经熟悉
- ⏭ 时间紧急且需求简单

**跳过时的处理**：
```markdown
# 跳过时标记为 completed，解除对阶段4的阻塞
TaskUpdate(task.id, status="completed", metadata={note: "不满足执行条件，已跳过"})
```

---

### 阶段 4: 澄清问题

**目标**：解决所有不清楚、模糊或有歧义的需求点

**任务管理**：
```markdown
# 开始阶段时
tasks = TaskList()
task = findTaskBySubject(tasks, "阶段 4: 澄清问题")
TaskUpdate(task.id, status="in_progress", owner="requirement-analysis")
```

**重要**：对任何不清楚、模糊、有歧义的地方，必须使用 **AskUserQuestion 工具**。

**澄清内容**：
- 模糊或规格不足的需求
- 多个有效实施方法之间的选择
- 业务规则细节
- 技术选型或架构决策

**已收到用户输入/反馈**：
```markdown
# 用户回应后继续阶段
TaskUpdate(task.id, status="completed")
```

**阶段完成**：
```markdown
# 完成阶段时
TaskUpdate(task.id, status="completed")
```

---

### 阶段 5: 深度分析

**目标**：使用 ultrathink 进行深度分析，设计完整的技术方案

**任务管理**：
```markdown
# 开始阶段时
tasks = TaskList()
task = findTaskBySubject(tasks, "阶段 5: 深度分析")
TaskUpdate(task.id, status="in_progress", owner="requirement-analysis")
```

**必须使用 ultrathink**：使用 **mcp__sequential-thinking__sequentialthinking 工具**

**上下文注意事项**：
虽然 ultrathink 能够访问完整的对话历史，但在进行深度分析时，建议明确引用和总结之前阶段的关键发现，确保分析的连贯性和准确性。

**分析内容**：
1. **分析需求组件**
   - 回顾阶段 1 的需求理解结果
   - 分解为可实施的功能模块

2. **设计数据结构**（符合 CLAUDE.md 规范）
   - 基于阶段 2 的代码库探索发现
   - 遵循项目的数据库设计规范和模式

3. **设计 API 端点**（符合 CLAUDE.md 规范）
   - 参考项目现有的 API 设计模式
   - 遵循项目的路由命名和结构约定

4. **设计服务层**（符合 CLAUDE.md 规范）
   - 遵循项目的架构模式和分层约定
   - 复用项目中已有的设计模式和抽象

5. **识别风险和边缘情况**
   - 考虑阶段 4 中用户澄清的特殊情况
   - 分析潜在的技术和业务风险

6. **规划详细实施步骤**
   - 整合所有上述分析
   - 制定可执行的分步实施计划

**阶段完成**：
```markdown
# 完成阶段时
TaskUpdate(task.id, status="completed")
```

---

### 阶段 6: 展示实施计划

**目标**：向用户展示完整的实施计划，等待确认

**任务管理**：
```markdown
# 开始阶段时
tasks = TaskList()
task = findTaskBySubject(tasks, "阶段 6: 展示实施计划")
TaskUpdate(task.id, status="in_progress", owner="requirement-analysis")
```

向用户展示：
1. **需求总结** - 理解的核心要点
2. **代码库发现** - 相关代码和模式
3. **外部资源**（如适用）- 搜索结果和库文档
4. **技术设计** - 数据库、API、服务层
5. **实施步骤** - 编号的详细步骤
6. **风险和注意事项**

**重要**：在用户确认前，不要标记任务为 completed。

询问："这个实施计划看起来如何？我可以开始实施了吗？"

**已收到用户确认后**：
```markdown
# 用户确认后继续
TaskUpdate(task.id, status="completed")
# 阶段7自动解除阻塞，可以开始
```

**输出格式**：参见 [assets/output-template.md](assets/output-template.md)

---

### 阶段 7: 实施开发

**目标**：基于阶段6的架构设计，实施功能代码

**任务管理**：
```markdown
# 开始阶段时
tasks = TaskList()
task = findTaskBySubject(tasks, "阶段 7: 实施开发")
TaskUpdate(task.id, status="in_progress", owner="requirement-analysis")
```

**前提**：必须获得用户明确确认（阶段6完成）

**执行原则**：
1. 严格遵循 CLAUDE.md
2. 按照架构设计实施功能
3. 保持代码简洁，避免过度工程
4. 及时验证和测试
5. 遇到问题及时使用 AskUserQuestion

**阶段职责**：
- 编写功能代码
- 实现设计的 API、数据结构、服务层
- 编写单元测试（如需要）
- 不包含代码审查（审查在阶段8）

**完成标志**：
- 所有功能代码实现完成
- 代码通过基本测试
- 符合项目规范

**阶段完成**：
```markdown
# 完成阶段时
TaskUpdate(task.id, status="completed")
# 自动解除阶段8的阻塞
```

---

### 阶段 8: 代码审查

**目标**：独立的质量把关阶段，全面审查代码质量

**任务管理**：
```markdown
# 开始阶段时
tasks = TaskList()
task = findTaskBySubject(tasks, "阶段 8: 代码审查")
TaskUpdate(task.id, status="in_progress", owner="requirement-analysis")
```

**阶段职责**：
- 独立的质量把关阶段
- 检查代码质量、规范遵循
- 识别 bug 和潜在问题
- 提供改进建议

**审查模式选择**：

**单一审查模式**（简单需求）：
- 使用 1 个 code-reviewer agent
- 全面审查所有维度

**并行深度审查模式**（复杂需求）：
- 同时启动 3-5 个审查任务
- 每个聚焦于特定维度（功能正确性、代码风格、规范遵循、约定和抽象）
- 必须在单个消息中发起所有 Task 调用
- **详细指南和示例**：[并行模式指南](references/parallel-patterns.md)

**执行步骤**：
1. 选择审查模式（基于需求复杂度）
2. 启动审查 agents
3. 收集审查结果（使用 TaskOutput）
4. 整合问题列表
5. **使用 AskUserQuestion 询问处理方式**

**审查后必须**：
- 使用 **AskUserQuestion** 询问用户如何处理问题
- 不得自动修复，必须征求确认

**产出**：
- 审查报告（问题列表、严重性标注）
- 改进建议
- 修复后的代码（如用户确认）

**阶段完成**：
```markdown
# 完成阶段时
TaskUpdate(task.id, status="completed")
# 自动解除阶段9的阻塞
```

**输出格式**：参见 [assets/output-template.md](assets/output-template.md)

---

### 阶段 9: 总结

**目标**：总结整个需求分析流程，提供后续建议

**任务管理**：
```markdown
# 开始阶段时
tasks = TaskList()
task = findTaskBySubject(tasks, "阶段 9: 总结")
TaskUpdate(task.id, status="in_progress", owner="requirement-analysis")
```

**总结内容**：

1. **需求总结**
   - 核心功能回顾
   - 实现的关键特性

2. **成果清单**
   - 完成的功能模块
   - 创建的文件
   - 编写的代码

3. **质量指标**
   - 审查发现的问题数量
   - 修复情况
   - 代码质量评分

4. **后续建议**
   - 进一步优化建议
   - 潜在改进点
   - 文档更新建议

5. **经验教训**
   - 遇到的挑战
   - 解决方案
   - 最佳实践

**最终进度显示**：
```markdown
### [完成] 所有阶段完成！

需求分析项目 - 100% 完成

📝 阶段完成情况：
[完成] 阶段 1: 需求理解
[完成] 阶段 2: 代码库探索
[跳过] 阶段 3: 外部资源研究 (跳过)
[完成] 阶段 4: 澄清问题
[完成] 阶段 5: 深度分析
[完成] 阶段 6: 展示实施计划
[完成] 阶段 7: 实施开发
[完成] 阶段 8: 代码审查
[完成] 阶段 9: 总结

项目成功完成！
```

**阶段完成**：
```markdown
# 完成阶段时
TaskUpdate(task.id, status="completed")
# 所有任务完成！
```

---

## 重要原则

1. **自适应语言交互**：根据用户在 Claude 中的 response language 设置和输入消息的语言与用户沟通（技术术语和代码除外）
2. **严格遵循 CLAUDE.md**：必须阅读并遵守项目规范
3. **主动提问**：不清楚的地方必须澄清，不要假设
4. **合理使用 ultrathink**：
   - 阶段 1：根据复杂度决定
   - 阶段 5：必须使用
5. **善用外部资源**：需要时使用 context7、exa（带降级方案）
6. **合理使用并行化**：
   - 阶段 2：复杂需求使用并行探索
   - 阶段 8：大型改动使用并行审查
   - 必须在单个 message 中发起所有并行任务
7. **必须代码审查**：实施完成后必须执行阶段 8
8. **审查前征求确认**：使用 AskUserQuestion，不得自动修复
9. **切勿急躁**：计划确认前不要编码
10. **保持彻底**：考虑边缘情况、错误和性能
11. **善用 Task list**：自动管理任务状态，提供进度可视化和断点恢复能力

---

## 参考文档

### 详细指南
- [并行模式指南](references/parallel-patterns.md) - 并行探索和审查的详细策略
- [使用示例](references/examples.md) - 3 个完整的使用场景示例
- [输出格式模板](assets/output-template.md) - 标准化的输出格式


---

