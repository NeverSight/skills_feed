---
name: openspec-proposal-creation-cn
description: 通过openspec规范驱动的方法创建结构化的变更提案与规范差异。用于规划功能、创建提案、编写规范、引入新能力或启动开发流程。触发词包括 "openspec提案", "规划", "创建提案", "规划变更", "规范功能", "新功能", "新特性", "新需求", "添加功能规划", "设计规范"。
---

# 规范提案创建

遵循规范驱动开发方法，生成完整的变更提案。

## 快速开始

创建规范提案包含三类输出：
1. **proposal.md** - 为什么、做什么、影响摘要
2. **tasks.json** - 编号的实施清单
3. **spec-delta.md** - 正式的需求变更（ADDED/MODIFIED/REMOVED）

**基本流程**：生成变更 ID → 脚手架目录 → 起草提案 → 编写规范差异 → 验证结构

## 工作流

复制此清单并跟踪进度：

```
规划进度:
- [ ] 第 1 步：审阅现有规范
- [ ] 第 2 步：生成唯一的变更 ID
- [ ] 第 3 步：生成目录结构
- [ ] 第 4 步：起草 proposal.md（为什么、做什么、影响摘要）
- [ ] 第 5 步：创建 tasks.json 实施清单
- [ ] 第 6 步：编写 spec-delta.md 规范差异（ADDED/MODIFIED/REMOVED）
- [ ] 第 7 步：验证提案结构
- [ ] 第 8 步：向用户展示并请求审批
```

### 第 1 步：审阅现有规范

在创建提案前，了解当前状态：

```bash
# 列出所有现有规范
find spec/specs -name "spec.md" -type f

# 列出进行中的变更以避免冲突
find spec/changes -maxdepth 1 -type d -not -path "*/archive"

# 搜索相关需求
grep -r "### Requirement:" spec/specs/
```

### 第 2 步：生成唯一的变更 ID

选择具描述性、URL 安全的标识符：

**格式**：`add-<feature>`、`fix-<issue>`、`update-<component>`、`remove-<feature>`

**示例**：
- `add-user-authentication`
- `fix-payment-validation`
- `update-api-rate-limits`
- `remove-legacy-endpoints`

**校验**：检查是否冲突：
```bash
ls spec/changes/ | grep -i "<proposed-id>"
```

### 第 3 步：生成目录结构

按标准结构创建变更目录：

```bash
# 将 {change-id} 替换为实际 ID
mkdir -p spec/changes/{change-id}/specs/{capability-name}
```

**示例**：
```bash
mkdir -p spec/changes/add-user-auth/specs/authentication
```

### 第 4 步：起草 proposal.md

以 [templates/proposal.md](templates/proposal.md) 为起点。

**必需章节**：
- **Why**：驱动变更的问题或机会
- **What Changes**：修改项清单
- **Impact**：受影响的规范、代码、API、用户

**语气**：清晰、简洁、面向决策。避免不必要背景。

### 第 5 步：创建 tasks.json 实施清单

将实现拆分为具体、可测试的任务。使用 [templates/tasks.json](templates/tasks.json)。

**格式**：
```markdown
# 实施任务
```json
[
  {
    "number": 1,
    "category": "阶段 1：基础设施",
    "task": "环境搭建任务 - 数据库架构、依赖等",
    "steps": [
      { "step": "初始化 Git 仓库并配置 .gitignore", "completed": false },
      { "step": "创建并激活 Python 虚拟环境", "completed": false },
      { "step": "创建 requirements.txt 或 pyproject.toml 并安装依赖 (FastAPI, SQLAlchemy, Pydantic, Alembic 等)", "completed": false },
      { "step": "设计初始数据库 ER 图", "completed": false },
      { "step": "配置数据库连接字符串和环境变量 (.env)", "completed": false },
      { "step": "初始化 Alembic 迁移环境", "completed": false }
    ],
    "passes": false
  }
]


**最佳实践**：
- 每个任务可独立完成
- 为每个主要组件添加测试任务
- 为每个主要组件添加测试任务
- 包含测试与验证任务
- 按依赖排序（数据库先于 API 等）
- 通常 5-15 个任务；更多时应拆分
- 每次仅处理1个step

```

### 第 6 步：以 EARS 格式编写规范差异

这是最关键步骤。规范差异使用 **EARS 格式**（易于需求语法）。

**完整 EARS 指南**见 [reference/EARS_FORMAT.md](reference/EARS_FORMAT.md)

**差异操作**：
- `## ADDED Requirements` - 新增能力
- `## MODIFIED Requirements` - 行为变更（包含完整更新文本）
- `## REMOVED Requirements` - 弃用功能

**基本需求结构**：
```markdown
## ADDED Requirements

### Requirement: 用户登录
WHEN 用户提交有效凭据,
系统 SHALL 认证用户并创建会话。

#### Scenario: 登录成功
GIVEN 用户邮箱为 "user@example.com" 且密码为 "correct123"
WHEN 用户提交登录表单
THEN 系统创建已认证会话
AND 重定向至仪表盘
```

**用于验证的模式**见 [reference/VALIDATION_PATTERNS.md](reference/VALIDATION_PATTERNS.md)

### 第 7 步：验证提案结构

在展示给用户前运行以下检查：

```markdown
结构清单：
- [ ] 目录存在：`spec/changes/{change-id}/`
- [ ] proposal.md 包含 Why/What/Impact
- [ ] tasks.json 含编号任务列表（5-15 项）
- [ ] 规范差异包含操作标题（ADDED/MODIFIED/REMOVED）
- [ ] 需求遵循 `### Requirement: <name>` 格式
- [ ] 场景使用 `#### Scenario:` 格式（四个井号）
```

**自动化检查**：
```bash
# 统计差异操作（应 > 0）
grep -c "## ADDED\|MODIFIED\|REMOVED" spec/changes/{change-id}/specs/**/*.md

# 验证场景格式（显示行号）
grep -n "#### Scenario:" spec/changes/{change-id}/specs/**/*.md

# 检查需求标题
grep -n "### Requirement:" spec/changes/{change-id}/specs/**/*.md
```

### 第 8 步：提交用户评审

清晰总结提案：

```markdown
## Proposal Summary

**Change ID**：{change-id}
**Scope**：{简要描述}

**创建的文件**：
- spec/changes/{change-id}/proposal.md
- spec/changes/{change-id}/tasks.json
- spec/changes/{change-id}/specs/{capability}/spec-delta.md

**下一步**：
请评审提案。如认可或修正后，请回复 "openspec开发" 或 "按顺序完成任务" 开始实施。
```

## 进阶主题

**EARS 格式细节**：见 [reference/EARS_FORMAT.md](reference/EARS_FORMAT.md)
**验证模式**：见 [reference/VALIDATION_PATTERNS.md](reference/VALIDATION_PATTERNS.md)
**完整示例**：见 [reference/EXAMPLES.md](reference/EXAMPLES.md)

## 常见模式

### 模式 1：新增功能提案

新增能力时：
- 使用 `ADDED Requirements` 差异
- 同时包含正向场景与错误处理
- 在场景中考虑边界情况

### 模式 2：破坏性变更提案

修改既有行为时：
- 使用 `MODIFIED Requirements` 差异
- 包含完整更新后的需求文本
- 在 proposal.md 中说明变更内容与原因
- 在 tasks.json 中考虑迁移任务

### 模式 3：弃用提案

移除功能时：
- 使用 `REMOVED Requirements` 差异
- 在 proposal.md 中记录移除理由
- 在 tasks.json 中包含清理任务
- 在影响部分考虑用户迁移

## 反模式避免

**不要**：
- 跳过验证检查（务必运行 grep 模式）
- 未先审阅现有规范就创建提案
- 使用含糊的任务描述（如"修一下"）
- 编写不含场景的需求
- 忽略错误处理场景
- 在一个提案中混合多个无关变更

**要**：
- 在创建变更 ID 前检查冲突
- 编写具体、可测试的任务
- 同时包含正向与负向场景
- 一个提案只处理一个关注点
- 在展示前验证结构

## 文件模板

所有模板位于 `templates/` 目录：
- [proposal.md](templates/proposal.md) - 提案结构
- [tasks.json](templates/tasks.json) - 任务清单格式
- [spec-delta.md](templates/spec-delta.md) - 规范差异模板

## 参考资料

- [EARS_FORMAT.md](reference/EARS_FORMAT.md) - 完整 EARS 语法指南
- [VALIDATION_PATTERNS.md](reference/VALIDATION_PATTERNS.md) - Grep/bash 验证
- [EXAMPLES.md](reference/EXAMPLES.md) - 真实提案示例

---

**Token 预算**：此 SKILL.md 约 250 行，低于建议的 500 行上限。引用文件按需加载以逐步呈现。