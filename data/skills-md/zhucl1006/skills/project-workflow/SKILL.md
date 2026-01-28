---
name: project-workflow
description: |
  文档驱动的项目开发工作流。智能判断任务类型，执行已有计划或使用 feature-dev 生成新计划。

  **使用场景：**
  - 已有完整项目文档，需要执行开发任务
  - 用户指定执行某个计划（如"执行 plan 001"）
  - 用户请求开发新功能（自动使用 feature-dev 生成计划）

  **前置条件：**
  - 项目应该已有 docs/ 文档结构（PRD、SAD 等）
  - 如果是新项目，建议先使用 project-docs-setup skill 创建完整文档

  **触发方式：**
  - "执行 plan 001" / "继续 001-user-authentication"
  - "开始开发" / "执行计划" / "继续上次的任务"
  - "实现用户认证功能" / "添加 XXX 模块"
---

# Project Workflow

文档驱动的项目开发工作流，确保每次开发任务都有据可循、可追溯。

**重要提示**：本 skill 假设项目已有完整的文档结构（docs/README.md、PRD.md、SAD.md 等）。如果是新项目或缺少文档，强烈建议先使用 **project-docs-setup** skill 创建完整文档。

## 前置要求

### 项目文档

本 skill 依赖完整的项目文档体系。如果项目缺少文档：

**推荐做法**：
```
使用 project-docs-setup skill：
  /project-docs-setup
  或告诉我："创建项目文档"

该 skill 会：
- 通过多轮对话了解项目需求
- 提供专业的产品和架构分析
- 生成完整的 PRD、SAD、开发指南等文档
```

**快速模式**：
如果只是简单测试，Phase 0 可以创建最小化目录结构，但**不包含文档内容**。

### feature-dev 插件

本 skill 依赖 Claude Code 的 **feature-dev** 插件来自动生成和执行新功能的开发计划。

**检查是否已安装：**
- 运行 `/feature-dev` 命令，如果能正常调用则已安装

**如未安装：**
- 参考安装文档：https://github.com/anthropics/claude-code/blob/main/plugins/feature-dev/README.md
- 或者使用简化模式（手动制定计划，skill 会提示）

**feature-dev 提供什么：**
- 7 阶段的系统化功能开发流程
- 自动代码探索、架构设计、实现、质量审查
- 适用于复杂功能、多文件改动、需要架构决策的场景

### Code Review Agent

本 skill 使用 **general-purpose** agent 进行代码质量检查和优化。

**Code Review 功能：**
- 代码质量审查（代码规范、最佳实践）
- Bug 和安全漏洞检测
- 性能优化建议
- 可读性和可维护性分析

**使用方式：**
```
使用 Task 工具调用：
  subagent_type="general-purpose"
  description="Code review for recent changes"
  prompt="详细的代码审查提示..."
```

**审查流程：**
1. 调用 general-purpose agent 分析代码变更
2. agent 生成详细的审查报告
3. 根据报告修复问题
4. 重新运行审查直到没有重大问题

---

## 核心流程

```
0. 初始化文档结构 → 1. 读取文档 → 2. 判断任务类型
   ├─ 指定 plan → 3a. 执行已有计划 → Code Review → 修复优化 → 4. 更新文档
   └─ 功能描述 → 3b. feature-dev 生成并执行 → Code Review → 修复优化 → 4. 更新文档
```

---

## Phase 0: 检查文档结构

**在开始执行前自动检查。**

### 0.1 检查必需的文档

检查项目是否存在标准文档结构：

```bash
# 检查必需的目录和文件
- docs/README.md           # 文档索引（必需）
- docs/plans/              # 计划文件目录
- docs/specs/              # 规格文档
```

### 0.2 文档缺失处理

如果检测到文档结构不完整：

```
1. 显示检测结果：
   "检测到项目缺少文档结构"

2. 提供建议：
   "建议使用 project-docs-setup skill 创建完整的项目文档：
   - 该 skill 会通过多轮对话了解项目需求
   - 自动生成 PRD、SAD、开发指南等完整文档
   - 提供最佳实践建议和架构分析

   运行方式：
   /project-docs-setup
   或
   告诉我：'创建项目文档'"

3. 询问用户选择：
   "你希望如何处理？
   a) 先创建完整文档（推荐）- 我可以帮你调用 project-docs-setup
   b) 创建最小化结构继续 - 只创建空目录，无文档内容
   c) 跳过检查继续执行 - 假设文档在其他位置"

4. 根据用户选择：
   - 选择 a：调用 project-docs-setup skill 或提示用户运行
   - 选择 b：执行 0.3 创建最小化结构
   - 选择 c：跳过 Phase 0，进入 Phase 1
```

### 0.3 创建最小化结构（仅在用户选择时）

```bash
# 只创建目录结构，不创建任何文件
mkdir -p docs/plans
mkdir -p docs/specs
mkdir -p docs/guides
mkdir -p docs/modules
mkdir -p docs/database
mkdir -p docs/api

echo "已创建基础目录结构。"
echo "注意：目录为空，建议后续使用 project-docs-setup 补充完整文档。"
```

### 0.4 文档已存在

如果文档结构完整，显示确认信息并跳过此阶段：

```
✓ 检测到完整的文档结构
✓ 直接进入 Phase 1
```

---

## Phase 1: 读取项目文档

**每次执行前必须完成。**

```
1. 读取 docs/README.md 获取文档索引
2. 根据索引读取任务相关的文档：
   - 规格文档 (specs/)
   - 模块文档 (modules/)
   - 开发指南 (guides/)
3. 读取 AGENTS.md（如存在）了解项目约定
```

**关键文档优先级：**
- 架构设计 (SAD.md) > 需求文档 (PRD.md) > 模块文档 > 指南

---

## Phase 2: 判断任务类型

根据用户输入判断是执行已有计划还是创建新计划。

### 2.1 识别任务类型

**执行已有计划的标志：**
- 用户明确指定 plan 编号："执行 plan 001"、"继续 001-user-authentication"
- 用户说"执行计划"、"继续上次的任务"且有进行中的计划

**创建新计划的标志：**
- 用户描述功能需求："实现用户认证"、"添加 OCR 模块"
- 用户说"开始开发 XXX 功能"

### 2.2 路由逻辑

```
if 用户指定了 plan 编号 or 有明确的进行中计划:
    → Phase 3a: 执行已有计划
else:
    → Phase 3b: 使用 feature-dev 生成并执行计划
```

### 2.3 使用示例

**场景 1：执行已有计划**
```
用户："执行 plan 001"
或
用户："继续 001-user-authentication 的开发"

→ 路由到 Phase 3a，读取并执行该计划
```

**场景 2：新功能开发**
```
用户："实现用户认证功能"
或
用户："添加 API 速率限制"

→ 路由到 Phase 3b，调用 feature-dev 生成计划并执行
```

---

## Phase 3a: 执行已有计划

当用户指定了具体的 plan 文件时，直接执行该计划。

### 3a.1 读取计划

```
1. 根据用户指定的编号定位 plan 文件（如 docs/plans/001-user-authentication.md）
2. 读取计划文件完整内容
3. 检查计划状态（待执行/进行中/已完成）
```

### 3a.2 创建任务列表

```
1. 使用 TodoWrite 将计划中的任务转为 todos
2. 将计划状态更新为"进行中"
```

### 3a.3 逐步执行

```
对于每个任务：
  1. 标记 todo 为 in_progress
  2. 参考相关文档执行任务
  3. 运行测试/验证
  4. 标记 todo 为 completed
  5. 更新计划文件中的任务状态 [x]
  6. 在执行记录表格中添加记录
```

**执行原则：**
- 遵循项目 AGENTS.md 中的 CONVENTIONS 和 ANTI-PATTERNS
- 遵循 TDD：先写测试，再实现
- 每完成一个任务立即更新计划文件

### 3a.4 完成验证

```
1. 确认所有任务完成
2. 运行完整测试套件
3. 执行 Code Review
4. 修复优化循环
5. 将计划状态更新为"已完成"
6. 进入 Phase 4 更新文档
```

### 3a.5 Code Review 和修复循环

使用 general-purpose agent 进行代码质量检查：

```
循环执行直到没有重大问题：
  1. 调用 general-purpose agent
     使用 Task 工具：
       subagent_type="general-purpose"
       description="Code review for recent changes"
       prompt="
         Please review the code changes for this feature/task.

         Focus on the following areas:
         1. Code Quality and Best Practices
            - Code style and consistency
            - Adherence to project conventions (check AGENTS.md if exists)
            - SOLID principles and design patterns

         2. Bugs and Security
            - Potential bugs or edge cases
            - Security vulnerabilities (SQL injection, XSS, etc.)
            - Error handling completeness

         3. Performance
            - Performance bottlenecks
            - Inefficient algorithms or queries
            - Memory leaks or resource management issues

         4. Maintainability
            - Code readability and clarity
            - Documentation and comments (where needed)
            - Test coverage

         Please categorize issues by severity:
         - BLOCKER: Critical issues that must be fixed (security, serious bugs)
         - MAJOR: Important issues that should be fixed (performance, code quality)
         - MINOR: Suggestions for improvement (readability, minor optimizations)

         Provide specific file paths and line numbers for each issue.
       "

  2. 分析审查报告
     - 代码规范问题
     - 潜在 Bug 和安全漏洞
     - 性能优化建议
     - 可维护性问题

  3. 根据严重程度分类
     - 阻塞性问题（必须修复）：安全漏洞、严重 Bug
     - 重要问题（应该修复）：性能问题、代码规范
     - 建议性优化（可选）：可读性改进、小优化

  4. 修复阻塞性和重要问题
     - 修改代码
     - 运行测试确保修复有效
     - 更新相关文档

  5. 重新运行 code review
     - 验证问题已解决
     - 检查是否引入新问题

  6. 确认完成
     - 没有阻塞性问题
     - 重要问题已修复或有计划处理
     - 用户确认可以继续
```

**Code Review 原则：**
- 阻塞性问题必须在此阶段解决
- 重要问题应该尽量解决
- 建议性优化可以记录到技术债务，后续处理
- 每次修复后重新运行 code review
- 最多迭代 3-5 轮，避免过度优化

---

## Phase 3b: 使用 feature-dev 生成并执行计划

当用户提出新的功能需求时，使用 feature-dev 插件生成计划并执行。

### 3b.1 检查 feature-dev 可用性

尝试调用 feature-dev 插件：

```
使用 Skill 工具调用：skill="feature-dev", args="{用户需求}"
```

**如果调用失败（插件不可用）：**
- 提示用户："feature-dev 插件未安装或不可用"
- 提供安装指引："请参考 https://github.com/anthropics/claude-code/blob/main/plugins/feature-dev/README.md 安装"
- 询问用户是否手动制定计划（回退到简化流程）

### 3b.2 调用 feature-dev

使用 Skill 工具调用 feature-dev：

```
skill="feature-dev", args="{用户的功能需求描述}"
```

或者简化调用（让 feature-dev 交互式询问）：

```
skill="feature-dev"
```

**feature-dev 会自动完成：**
1. **Discovery** - 明确功能需求
2. **Codebase Exploration** - 理解相关代码（并行运行 2-3 个 agent）
3. **Clarifying Questions** - 解决需求歧义
4. **Architecture Design** - 设计多个实现方案，供用户选择
5. **Implementation** - 用户批准后实现功能
6. **Quality Review** - 代码质量检查
7. **Summary** - 总结完成的工作

### 3b.3 保存计划到 docs/plans/

feature-dev 完成后，将其输出整理成 project-workflow 的计划格式：

```
1. 确定计划编号：查看 docs/plans/ 目录，使用最大编号 +1
2. 创建计划文件：docs/plans/{序号}-{功能名}.md
3. 将 feature-dev 的设计决策和实现步骤写入计划
4. 标记计划状态为"已完成"（因为 feature-dev 已经实现）
5. 记录执行日期和主要变更
```

**计划文件内容包括：**
- 功能描述（来自 Discovery 阶段）
- 架构设计（来自 Architecture Design 阶段）
- 已完成的任务列表（来自 Implementation 阶段）
- 质量检查结果（来自 Quality Review 阶段）
- 执行记录（Summary）

### 3b.4 后续步骤

```
1. 确认 feature-dev 执行成功
2. 执行 Code Review（补充审查）
3. 修复优化循环
4. 将生成的计划保存到 docs/plans/
5. 进入 Phase 4 更新文档
```

### 3b.5 补充 Code Review

feature-dev 自带 Quality Review，但可以进行补充审查：

```
1. 评估 feature-dev 的 Quality Review 结果
   - 如果 Quality Review 已全面覆盖，可跳过
   - 如果需要补充审查，继续以下步骤

2. 使用 general-purpose agent 补充审查
   使用 Task 工具：
     subagent_type="general-purpose"
     description="Supplementary code review for feature-dev output"
     prompt="
       Review the code implemented by feature-dev, focusing on:

       1. Project-specific conventions (check AGENTS.md)
          - Naming conventions
          - Module structure
          - Error handling patterns

       2. Integration concerns
          - Compatibility with existing code
          - API consistency
          - Database schema compatibility

       3. Missing edge cases
          - Input validation
          - Error scenarios
          - Boundary conditions

       Categorize by severity (BLOCKER/MAJOR/MINOR).
       Focus on issues that feature-dev's Quality Review might have missed.
     "

3. 按 Phase 3a.5 的流程执行修复循环
   - 分析审查报告
   - 修复阻塞性和重要问题
   - 重新运行审查
   - 确认完成
```

**注意：**
- feature-dev 的 Quality Review 已经很全面
- 补充审查主要针对项目特定规范
- 避免重复审查，浪费时间

---

## Phase 4: 更新文档

任务完成后，更新受影响的文档。

**必须检查并更新的文档：**

| 变更类型 | 需更新的文档 |
|----------|-------------|
| 新增模块 | docs/modules/{module}.md, docs/specs/SAD.md |
| API 变更 | docs/api/*.md |
| 数据库变更 | docs/database/SCHEMA.md |
| 新增功能 | docs/specs/PRD.md |
| 架构调整 | docs/specs/SAD.md, AGENTS.md |

**更新 AGENTS.md：**
- 如有新的约定或反模式，添加到对应章节
- 更新 CHANGELOG 记录变更

---

## 异常处理

| 场景 | 处理方式 |
|------|----------|
| 无 docs/ 目录 | 自动创建文档结构（Phase 0） |
| 无 docs/plans/ 目录 | 自动创建 docs/plans/ 目录 |
| feature-dev 未安装 | 提示安装，或询问用户是否手动制定计划 |
| feature-dev 执行失败 | 检查错误信息，尝试重新执行或回退到手动模式 |
| code review agent 执行失败 | 检查错误信息，尝试重新执行或跳过 code review |
| code review 发现阻塞性问题 | 必须修复后才能继续，记录到执行记录 |
| code review 迭代超过 5 轮 | 与用户讨论，决定是否继续优化或接受当前状态 |
| 计划执行中断 | 恢复时读取计划文件，从未完成任务继续 |
| 任务执行失败 | 记录失败原因到执行记录，询问用户处理方式 |
| 需求变更 | 更新计划文件，标记原任务状态，添加新任务 |

---

## 附录

### 计划文件命名规范

```
docs/plans/
├── 001-user-authentication.md
├── 002-llm-service-integration.md
├── 003-ocr-module.md
└── ...
```

**命名规则：**
- 格式：`{三位数字序号}-{功能名称}.md`
- 序号从 001 开始，递增
- 功能名称使用小写字母和连字符，简洁明确

### feature-dev 计划文件格式

当使用 feature-dev 生成计划后，保存为以下格式：

```markdown
# {功能名称}

## 状态

- 状态：已完成
- 创建日期：YYYY-MM-DD
- 完成日期：YYYY-MM-DD

## 功能描述

{来自 feature-dev Discovery 阶段的需求描述}

## 架构设计

{来自 feature-dev Architecture Design 阶段的设计决策}

### 选择的方案

{用户批准的实现方案}

## 已完成任务

- [x] 任务 1
- [x] 任务 2
- [x] 任务 3

{来自 feature-dev Implementation 阶段的实现步骤}

## 质量检查

{来自 feature-dev Quality Review 阶段的审查结果}

## 执行记录

| 日期 | 操作 | 说明 |
|------|------|------|
| YYYY-MM-DD | 创建计划 | 使用 feature-dev 生成 |
| YYYY-MM-DD | 完成实现 | feature-dev 自动执行 |
| YYYY-MM-DD | 通过测试 | 所有测试通过 |

## 相关文档

- 更新的文档列表
- 新增的文档列表
```

### 手动制定计划（备选方案）

如果 feature-dev 不可用，可以手动制定计划：

1. 与用户确认需求：
   - 功能边界：具体要实现什么？
   - 技术约束：有特殊技术要求吗？
   - 验收标准：怎样算完成？
   - 优先级：哪些是必须的，哪些可以后续迭代？

2. 使用计划模板创建计划文件
   - **模板位置**：[references/plan-template.md](references/plan-template.md)
   - **文件路径**：`docs/plans/{序号}-{功能名}.md`

3. 将状态设为"待执行"

4. 按 Phase 3a 的流程执行
