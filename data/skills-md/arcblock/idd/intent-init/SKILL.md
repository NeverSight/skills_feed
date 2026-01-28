---
name: intent-init
description: Initialize IDD structure in a project. Checks existing state, creates directory structure, and generates templates. Use /intent-init to set up Intent-driven development in current project.
---

# Intent Init

初始化项目的 IDD (Intent Driven Development) 结构。

## 功能

1. **检查现状** - 扫描项目，识别已有的 intent 文件或类似结构
2. **创建目录** - 建立标准 IDD 目录结构
3. **生成模板** - 创建入口 INTENT.md 和模块级模板
4. **配置建议** - 根据项目类型给出配置建议

## 工作流程

```
/intent-init
    ↓
┌───────────────────────────────────┐
│  Phase 1: 扫描现状                │
│  - 查找 intent/, specs/, docs/   │
│  - 识别 README, DESIGN 等文档    │
│  - 检测项目类型 (monorepo/单模块) │
└─────────────┬─────────────────────┘
              ↓
┌───────────────────────────────────┐
│  Phase 2: 展示发现                │
│  - 已有文档列表                   │
│  - 项目结构分析                   │
│  - 推荐的 IDD 结构                │
└─────────────┬─────────────────────┘
              ↓
┌───────────────────────────────────┐
│  Phase 3: 确认并创建              │
│  - AskUserQuestion 确认结构       │
│  - 创建目录和模板文件             │
│  - 可选：迁移现有文档             │
└───────────────────────────────────┘
```

## 标准 IDD 目录结构

### 单模块项目

```
project/
├── intent/
│   └── INTENT.md           # 项目 Intent（入口）
├── src/
└── ...
```

### Monorepo / 多模块项目

```
project/
├── intent/
│   ├── INTENT.md           # 项目概述（入口）
│   └── architecture/
│       ├── DEPENDENCIES.md # 模块依赖图
│       └── BOUNDARIES.md   # 边界规则
│
├── src/
│   ├── module-a/
│   │   └── intent/
│   │       └── INTENT.md   # 模块 Intent
│   └── module-b/
│       └── intent/
│           └── INTENT.md
└── ...
```

## 模板内容

### 项目级 INTENT.md

```markdown
# [Project Name] Intent

> 一句话描述项目目标

状态: draft
最后更新: YYYY-MM-DD

## 愿景

[项目要解决的问题和目标]

## 架构概览

[ASCII 架构图]

## 模块索引

| 模块 | 职责 | Intent |
|------|------|--------|
| xxx | ... | [link] |

## 非目标

- [明确不做什么]

## 约束

- [技术约束]
- [业务约束]
```

### 模块级 INTENT.md

```markdown
# [Module] Intent

> 模块职责一句话

状态: draft
最后更新: YYYY-MM-DD

## 职责

[模块做什么]

## 非目标

[模块不做什么]

## 数据结构

[核心数据结构定义]

## API

[对外接口定义]

## 示例

[输入 → 输出 示例]
```

## 检测逻辑

### 识别已有 Intent 结构

```javascript
// 检查路径
const intentPaths = [
  'intent/INTENT.md',
  'INTENT.md',
  'docs/INTENT.md',
  'specs/',
  'design/',
];

// 检查内容特征
const intentMarkers = [
  '## 职责',
  '## 非目标',
  '::: locked',
  '::: reviewed',
];
```

### 项目类型识别

```javascript
// Monorepo 特征
const monorepoMarkers = [
  'packages/',
  'apps/',
  'src/modules/',
  'lerna.json',
  'pnpm-workspace.yaml',
];
```

## 选项

```
/intent-init              # 交互式初始化
/intent-init --dry-run    # 只展示计划，不执行
/intent-init --minimal    # 最小化结构
/intent-init --migrate    # 尝试迁移现有文档
```

## 与其他命令配合

```
/intent-init              # 初始化结构
    ↓
/intent-interview         # 填充 Intent 内容
    ↓
/intent-review            # 审批关键 sections
    ↓
[开发]
    ↓
/intent-check             # 检查一致性
```
