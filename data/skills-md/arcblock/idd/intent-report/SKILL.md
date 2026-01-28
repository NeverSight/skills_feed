---
name: intent-report
description: Generate human-readable report from Intent files. Converts technical Intent specs into readable documents for stakeholders, team members, or documentation. Supports multiple output formats.
---

# Intent Report

将技术性的 Intent 文件转换成人类可读的报告文档。

## 用途

- **给 Stakeholder**：项目概览、进度、关键决策
- **给新成员**：快速了解项目架构和设计理由
- **给文档**：生成 README、设计文档、架构说明
- **给会议**：项目汇报、技术评审

## 工作流程

```
/intent-report [options]
        ↓
┌───────────────────────────────────┐
│  读取 Intent 文件                  │
│  - 项目级 + 模块级                 │
│  - 解析结构和元数据                │
└─────────────┬─────────────────────┘
              ↓
┌───────────────────────────────────┐
│  确定报告类型                      │
│  - overview / architecture /      │
│    progress / full                │
└─────────────┬─────────────────────┘
              ↓
┌───────────────────────────────────┐
│  生成报告                          │
│  - 重组内容结构                    │
│  - 转换技术语言                    │
│  - 添加可视化                      │
└─────────────┬─────────────────────┘
              ↓
┌───────────────────────────────────┐
│  输出                              │
│  - Markdown / HTML / PDF          │
│  - 写入文件 or 直接展示            │
└───────────────────────────────────┘
```

## 报告类型

### 1. Overview (概览)

```
/intent-report --type overview
```

一页纸项目概览，适合快速了解：

```markdown
# [Project] Overview

## What is this?
[一句话说明]

## Problem
[要解决的问题]

## Solution
[解决方案概述]

## Architecture
[简化的架构图]

## Key Modules
| Module | Purpose |
|--------|---------|

## Status
[当前状态和下一步]
```

### 2. Architecture (架构)

```
/intent-report --type architecture
```

详细架构文档，适合技术评审：

```markdown
# [Project] Architecture

## System Overview
[架构图]

## Module Dependencies
[依赖关系图]

## Data Flow
[数据流图]

## Key Design Decisions
| Decision | Choice | Rationale |

## Boundary Rules
[模块边界规则]

## API Reference
[核心 API 列表]
```

### 3. Progress (进度)

```
/intent-report --type progress
```

项目进度报告，适合汇报：

```markdown
# [Project] Progress Report

> Generated: YYYY-MM-DD

## Intent Coverage
[覆盖率图表]

## Module Status
| Module | Intent | Impl | Status |
|--------|--------|------|--------|
| core   | ✓      | 80%  | 🟡     |

## Recent Updates
[最近的 Intent 变更]

## Approval Status
- Locked: N sections
- Reviewed: M sections
- Draft: K sections

## Blockers & Risks
[风险和阻塞项]

## Next Steps
[下一步计划]
```

### 4. Full (完整)

```
/intent-report --type full
```

完整技术文档，包含所有内容。

## 输出格式

### Markdown (默认)

```
/intent-report -o report.md
```

### HTML

```
/intent-report --format html -o report.html
```

带样式的 HTML 文档，可直接在浏览器查看。

### Console (直接显示)

```
/intent-report
```

不指定输出文件时，直接在终端展示。

## 使用示例

### 生成项目概览

```
/intent-report --type overview
```

### 生成架构文档给新成员

```
/intent-report --type architecture -o docs/ARCHITECTURE.md
```

### 生成进度报告给 stakeholder

```
/intent-report --type progress -o reports/progress-2026-01.md
```

### 生成单模块报告

```
/intent-report src/core/ --type full
```

## 内容转换规则

### 技术语言 → 人类语言

| Intent 中 | 报告中 |
|-----------|--------|
| `## 职责` | "What this module does" |
| `## 非目标` | "Out of scope" |
| `## 约束` | "Constraints & Rules" |
| `::: locked` | "Core Architecture (frozen)" |
| `::: reviewed` | "Approved Design" |
| `::: draft` | "Work in Progress" |

### ASCII 图 → 可视化

- 保留 ASCII 图（兼容性好）
- 可选：转换为 Mermaid 图（`--mermaid` 选项）

## 与其他命令配合

```
/intent-init              # 初始化
    ↓
/intent-interview         # 创建 Intent
    ↓
/intent-review            # 审批
    ↓
/intent-report            # ← 生成报告（本命令）
    ↓
分享给 stakeholder / 团队
```

## 高级选项

```
/intent-report
  --type <type>           # overview | architecture | progress | full
  --format <format>       # markdown | html
  --output <path>         # 输出文件路径
  --module <path>         # 指定模块
  --include-draft         # 包含 draft sections
  --mermaid               # 转换为 Mermaid 图
  --lang <lang>           # 输出语言 (en | zh)
```
