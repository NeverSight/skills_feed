---
name: intent-normalize
description: Scan and normalize existing intent/planning files to IDD standard. Auto-fixes mechanical issues (frontmatter, directory structure), tags content issues for pickup. Use /intent-normalize to scan current project, or /intent-normalize <path> for specific directory.
---

# Intent Normalize

扫描现有项目，将 intent 和 planning 文件规范化到 IDD 标准。能自动修的直接修，不能修的打上状态让 TeamSwarm pickup。

## 设计原则

1. **格式先行** — 所有文件先有 frontmatter，让系统能识别
2. **能修则修** — 机械性问题直接修复（frontmatter、目录结构、命名）
3. **不能修则标记** — 内容问题打上状态，后续由 TeamSwarm 或人处理
4. **幂等** — 多次运行结果一致，已规范的文件不会被改动

## 工作流程

```
/intent-normalize [path]
        ↓
┌───────────────────────────────────┐
│  1. 扫描 intent/ 和 planning/     │
│     发现所有 .md 和 .yaml 文件     │
└─────────────┬─────────────────────┘
              ↓
┌───────────────────────────────────┐
│  2. 分析每个文件的合规状态         │
│     - 有无 frontmatter?           │
│     - 有无 Anchor?                │
│     - 目录结构是否完整?            │
└─────────────┬─────────────────────┘
              ↓
┌───────────────────────────────────┐
│  3. 自动修复机械问题               │
│     - 补 frontmatter              │
│     - 创建 records/ + INDEX.md    │
│     - 创建 _archive/, _data/      │
│     - 规范化文件命名               │
└─────────────┬─────────────────────┘
              ↓
┌───────────────────────────────────┐
│  4. 标记内容问题                   │
│     - 缺 Anchor → status: draft   │
│     - 超预算 → 标记 needs_critique │
│     - 无法分类 → status: draft     │
└─────────────┬─────────────────────┘
              ↓
┌───────────────────────────────────┐
│  5. 输出规范化报告                 │
└───────────────────────────────────┘
```

## 检查项与修复策略

### 自动修复（机械性，无需判断）

| 检查项 | 条件 | 修复动作 |
|--------|------|----------|
| Intent frontmatter | INTENT.md 没有 frontmatter | 添加 `status: active`（或根据内容推断） |
| Planning frontmatter | planning/ 下 .md 没有 frontmatter | 添加 `type:` (从内容推断: idea/research/feedback/analysis) |
| Anchor 格式 | Anchor 存在但格式不对（不是 blockquote） | 修正为 `> Anchor: ...` 格式 |
| records/ 目录 | intent 目录下没有 records/ | 创建 `records/` + 空 `INDEX.md` |
| _archive/ 目录 | intent/ 下没有 _archive/ | 创建 `intent/_archive/` |
| _data/ 目录 | intent/ 下没有 _data/ | 创建 `intent/_data/` |
| TASK.yaml 格式 | TASK.yaml 缺少 type 字段 | 添加 `type: one-shot`（默认） |

### 标记 pickup（需要内容判断）

| 检查项 | 条件 | 标记动作 |
|--------|------|----------|
| 缺少 Anchor | INTENT.md 没有 Anchor 行 | frontmatter 加 `needs: [anchor]` |
| 超预算 | 行数 > 500 | frontmatter 加 `needs: [critique]` |
| 预算警告 | 300 < 行数 ≤ 500 | frontmatter 加 `needs: [review]` |
| 无 Assumes | 内容中引用了其他 intent 但没有 Assumes 标签 | frontmatter 加 `needs: [assumes]` |
| 分类不明 | planning 文件无法自动判断类型 | `type: idea`（默认最安全） |

### `needs` 字段

`needs` 是 frontmatter 中的 pickup 信号，表示该文件需要后续处理：

```yaml
---
status: active
needs: [anchor, critique]
---
```

TeamSwarm 扫描 `needs` 字段来自动调度后续 skill：
- `needs: [anchor]` → 安排 `/intent-interview` 补充
- `needs: [critique]` → 安排 `/intent-critique` 精简
- `needs: [review]` → 安排 `/intent-review`
- `needs: [assumes]` → 安排人工补充依赖声明

处理完成后，对应的 `needs` 项被移除。`needs` 为空时可以删掉整个字段。

## Planning 类型推断

自动从文件内容推断 `type:`：

| 关键词/模式 | 推断类型 |
|-------------|----------|
| idea, concept, proposal, brainstorm, what if | `idea` |
| research, analysis, comparison, benchmark, study | `research` |
| feedback, user, complaint, request, survey | `feedback` |
| code analysis, refactor, migration, legacy, improvement | `analysis` |
| 无法判断 | `idea`（最安全的默认值） |

## 执行细节

### 1. 扫描范围

```
默认扫描当前项目根目录下的：
- intent/           → 所有 INTENT.md 文件（递归，跳过 _archive/ 和 _data/）
- planning/         → 所有 .md 文件
- **/intent/        → 模块级 intent 目录
```

### 2. Frontmatter 注入

对没有 frontmatter 的文件，在文件头部插入：

**Intent 文件：**
```yaml
---
status: active
---
```

如果文件看起来已经实现（有对应的代码目录和测试），推断为：
```yaml
---
status: implemented
---
```

**Planning 文件：**
```yaml
---
type: research
---
```

### 3. 推断 status 的启发式规则

| 信号 | 推断 status |
|------|-------------|
| 有 TASK.yaml 且 status: done | `implemented` |
| 有对应的 src/ 目录且文件最近没修改 | `implemented` |
| 文件内容很少（< 50 行）或明显不完整 | `active`（+ `needs: [anchor]`） |
| 默认 | `active` |

### 4. 幂等保证

- 已有正确 frontmatter 的文件不修改
- 已有 records/ 的不重建
- `needs` 字段只添加不覆盖（合并已有的）
- 每次运行结果相同

## 输出

### 规范化报告

```markdown
# Intent Normalize Report

> 项目: my-project
> 扫描时间: 2026-02-06

## 统计

| 类型 | 扫描 | 已规范 | 自动修复 | 需 pickup |
|------|------|--------|----------|-----------|
| Intent 文件 | 15 | 8 | 5 | 2 |
| Planning 文件 | 7 | 2 | 4 | 1 |
| 目录结构 | — | — | 3 | — |

## 自动修复（已完成）

1. ✅ `intent/kernel/proc/INTENT.md` — 添加 frontmatter `status: active`
2. ✅ `intent/kernel/afs/INTENT.md` — 添加 frontmatter `status: implemented`
3. ✅ `planning/v2-ideas.md` — 添加 frontmatter `type: idea`
4. ✅ `planning/legacy-analysis.md` — 添加 frontmatter `type: analysis`
5. ✅ `intent/kernel/proc/records/` — 创建目录 + INDEX.md
6. ✅ `intent/_archive/` — 创建目录
7. ✅ `intent/_data/` — 创建目录

## 需要 Pickup（已标记）

| 文件 | needs | 建议 |
|------|-------|------|
| `intent/ash/INTENT.md` | `[anchor, critique]` | 缺少 Anchor，612 行超预算 |
| `intent/surfaces/INTENT.md` | `[anchor]` | 缺少 Anchor |
| `planning/random-notes.md` | — | 无法分类，默认 type: idea |
```

## 使用

### 基本用法

```
/intent-normalize
```

扫描并规范化当前项目。

### 指定路径

```
/intent-normalize intent/kernel/
```

只规范化特定目录。

### Dry run

```
/intent-normalize --dry-run
```

只报告，不做任何修改。

## 与其他命令配合

```
/intent-normalize       # 先规范化格式（本命令）
    ↓
TeamSwarm pickup        # 自动调度 needs 中的后续 skill
    ↓
/intent-interview       # 处理 needs: [anchor]
/intent-critique        # 处理 needs: [critique]
/intent-review          # 处理 needs: [review]
    ↓
/intent-check           # 最终合规检查
```
