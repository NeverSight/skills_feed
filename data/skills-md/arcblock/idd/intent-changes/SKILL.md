---
name: intent-changes
description: Manage structured change proposals for design documents with PR-like review experience. Use /intent-changes start <file> to begin, /intent-changes propose to suggest changes, /intent-changes accept/reject to decide, /intent-changes finalize to apply.
---

# Intent Changes

设计文档的结构化变更提案与协作 Review 工具。

## 核心概念

### Change Proposal

每个变更是一个独立提案：

| 字段 | 说明 |
|------|------|
| **ID** | 唯一标识 (C001, C002...) |
| **Type** | ADD / MODIFY / REPLACE / DELETE |
| **Status** | PENDING / ACCEPTED / REJECTED |
| **Target** | 变更位置 |
| **Before/After** | 变更内容 |
| **Decision** | 决策记录 (reviewer, timestamp, comment) |

### 状态流

```
PENDING ──accept──> ACCEPTED ──finalize──> Applied
    │
    └──reject──> REJECTED
```

## 命令

| 命令 | 说明 |
|------|------|
| `/intent-changes start <file>` | 启动或恢复 review |
| `/intent-changes propose` | 提出变更建议 |
| `/intent-changes accept <id>` | 接受变更 |
| `/intent-changes reject <id>` | 拒绝变更 |
| `/intent-changes status` | 查看当前状态 |
| `/intent-changes finalize` | 交互式 apply |

## 工作流程

```
/intent-changes start <file>
        ↓
┌───────────────────┐
│  检查 .reviews/   │
│  有则恢复         │
│  无则创建         │
└─────────┬─────────┘
          ↓
/intent-changes propose
        ↓
┌───────────────────────────────────────┐
│  读取源文档                            │
│  与用户讨论变更内容                     │
│  生成 Change Proposal (C001, C002...)  │
│  写入 .reviews/{name}.review.md        │
└─────────┬─────────────────────────────┘
          ↓
/intent-changes accept/reject
        ↓
┌───────────────────┐
│  更新 status      │
│  记录 reviewer    │
│  记录 timestamp   │
└─────────┬─────────┘
          ↓
/intent-changes finalize
        ↓
┌───────────────────────────────────────┐
│  逐个显示 ACCEPTED 变更               │
│  交互确认: Apply? [Y/n/view]          │
│  Apply 到源文档                        │
│  生成变更摘要                          │
└───────────────────────────────────────┘
```

## 执行步骤

### 命令: start

**输入**: 文件路径

**步骤**:

1. 验证源文件存在
2. 确定 review 文件路径: `.reviews/{basename}.review.md`
3. 如果 review 文件存在:
   - 读取并解析
   - 显示当前状态概览
4. 如果不存在:
   - 创建 `.reviews/` 目录（如不存在）
   - 创建 review 文件，写入 frontmatter
5. 设置当前 session 的 source 和 review 路径

**输出**:
```
Review session started.

Source: intent/specs/kind-system-spec.md
Review: .reviews/kind-system-spec.review.md

Status: 3 PENDING, 2 ACCEPTED, 1 REJECTED

Commands:
  /intent-changes propose  - 提出新变更
  /intent-changes status   - 查看详情
  /intent-changes finalize - 应用变更
```

### 命令: propose

**前置条件**: 已执行 start

**步骤**:

1. 读取源文档内容
2. 读取当前 review 文件，获取已有提案
3. 计算下一个 ID (如已有 C001-C005，下一个是 C006)
4. 与用户讨论：
   - 展示源文档结构
   - 使用 AskUserQuestion 询问变更类型和位置
   - 收集变更内容
5. 生成 Change Proposal 块
6. 追加到 review 文件

**交互流程**:

```
使用 AskUserQuestion:
- question: "你想对哪个部分提出变更？"
- header: "变更位置"
- options:
  - "## Kind 定义" - 第一个 section
  - "## Actions" - 第二个 section
  - "## 示例" - 第三个 section
  - "其他位置" - 手动指定
```

```
使用 AskUserQuestion:
- question: "变更类型是什么？"
- header: "变更类型"
- options:
  - "ADD" - 新增内容
  - "MODIFY" - 修改现有内容
  - "REPLACE" - 替换整个 section
  - "DELETE" - 删除内容
```

然后收集具体内容，生成提案。

### 命令: accept / reject

**输入**: 提案 ID，可选 comment/reason

**语法**:
```
/intent-changes accept C001
/intent-changes accept C001 --comment "LGTM"
/intent-changes reject C002 --reason "不同意这个改法"
```

**步骤**:

1. 读取 review 文件
2. 找到对应 ID 的提案
3. 验证当前状态是 PENDING
4. 更新状态为 ACCEPTED 或 REJECTED
5. 添加 Decision 记录:
   - reviewer: 从 git config user.name 或 $USER 获取
   - timestamp: 当前日期
   - comment: 用户提供的评论
6. 写回 review 文件

**Decision 格式**:
```markdown
**Decision:**
- ✓ @robmao (2026-01-21): "LGTM"
```

或拒绝时:
```markdown
**Decision:**
- ✗ @robmao (2026-01-21): "不同意这个改法"
```

### 命令: status

**输出详情**:

```
Review: kind-system-spec.md
Source: intent/specs/kind-system-spec.md
Reviewers: @robmao, @claude

─────────────────────────────────

PENDING (2):
  C002 [MODIFY] 修改 Kind 定义的措辞
  C004 [ADD] 新增性能章节

ACCEPTED (3):
  C001 [ADD] 新增 Action 分类说明
       ✓ @robmao (2026-01-21)
  C003 [MODIFY] 调整示例代码
       ✓ @claude (2026-01-21)
  C005 [DELETE] 删除过时章节
       ✓ @robmao (2026-01-21)

REJECTED (1):
  C006 [REPLACE] 重写整个文档
       ✗ @robmao (2026-01-21): "改动太大"

─────────────────────────────────

Next: /intent-changes finalize (3 changes ready)
```

### 命令: finalize

**前置条件**: 至少有一个 ACCEPTED 的提案

**步骤**:

1. 读取 review 文件，筛选 ACCEPTED 提案
2. 按 Target 位置排序（从文档末尾往前，避免位置偏移）
3. 对每个提案交互确认:

```
[1/3] C001 [ADD]: 新增 Action 分类说明

Target: After "## Actions"

Content to add:
┌────────────────────────────────────────┐
│ Actions 分为三类：                      │
│ - Inline: 同步执行，决定 commit 成功与否 │
│ - Deferred: 异步执行，失败不影响 commit  │
│ - Observational: 只读，可以慢           │
└────────────────────────────────────────┘

Apply this change? [Y/n/view/quit]
```

用户选项:
- `Y` (默认): Apply 并继续
- `n`: Skip 此变更（保持 ACCEPTED 状态但不 apply）
- `view`: 显示完整的 before/after diff
- `quit`: 中止 finalize

4. Apply 变更到源文档
5. 更新 review 文件:
   - 已 apply 的标记为 `[APPLIED]`
   - 更新 frontmatter status 为 `finalized`（如果全部处理完）
6. 输出摘要

**Apply 摘要**:
```
Finalize complete.

Applied: 2
  C001 - 新增 Action 分类说明
  C003 - 调整示例代码

Skipped: 1
  C005 - 删除过时章节 (user chose to skip)

Source updated: intent/specs/kind-system-spec.md
Review archived: .reviews/kind-system-spec.review.md
```

## Review 文件格式

### Frontmatter

```yaml
---
source: intent/specs/kind-system-spec.md
created: 2026-01-21
reviewers:
  - robmao
  - claude
status: active
---
```

status 值:
- `active`: 进行中
- `finalized`: 已完成 apply
- `abandoned`: 已放弃

### Change Proposal 块

```markdown
---

## C001 [ADD] [PENDING]

> 简短描述

**Target:** After "## Actions"

**After:**
```markdown
新增的内容...
```

---

## C002 [MODIFY] [ACCEPTED]

> 简短描述

**Target:** Section "## Kind 定义"

**Before:**
```markdown
原内容...
```

**After:**
```markdown
新内容...
```

**Reason:** 变更理由

**Decision:**
- ✓ @robmao (2026-01-21): "LGTM"
```

## 获取 Reviewer 名称

按优先级:
1. 命令参数 `--reviewer`
2. `git config user.name`
3. 环境变量 `$USER`

```bash
# 获取方式
git config user.name || echo $USER
```

## 边界

### 做什么

- ✓ 结构化管理变更提案
- ✓ 追踪决策过程
- ✓ 支持多 reviewer 署名
- ✓ 交互式 apply

### 不做什么

- ✗ 格式校验 → intent-validate
- ✗ Section 审批 → intent-review
- ✗ 设计质量判断 → intent-critique
- ✗ 实现一致性 → intent-sync

## 与其他工具配合

```
intent-interview → 创建 Intent
        ↓
intent-critique → 质疑设计
        ↓
/intent-changes → 管理变更提案  ← 本 Skill
        ↓
intent-review → 锁定 sections
        ↓
intent-plan → 开始实现
```

## 示例

### 独立 Review

```bash
# 开始
/intent-changes start intent/specs/tools-spec.md

# 提出建议
/intent-changes propose

# 决策
/intent-changes accept C001
/intent-changes reject C002 --reason "不需要"

# 应用
/intent-changes finalize
```

### 协作 Review

```bash
# A 启动并提建议
/intent-changes start spec.md
/intent-changes propose  # C001-C003

# B 来 review
/intent-changes accept C001 --comment "Good"
/intent-changes reject C002 --reason "换个方式"

# A 提新方案
/intent-changes propose  # C004 替代 C002

# B 接受
/intent-changes accept C004

# 最终 apply
/intent-changes finalize
```
