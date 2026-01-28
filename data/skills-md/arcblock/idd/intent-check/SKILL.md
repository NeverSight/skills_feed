---
name: intent-check
description: Run Intent validation and sync checks. Triggers intent-validate and intent-sync agents. Use /intent-check for full check, or /intent-check --validate/--sync for specific checks.
---

# Intent Check

触发 Intent 检查流程，是 intent-validate 和 intent-sync agents 的用户友好入口。

## 功能

1. **格式验证** (intent-validate) - 检查 Intent 文件是否符合 IDD 规范
2. **代码同步** (intent-sync) - 检查代码实现与 Intent 的一致性
3. **综合报告** - 汇总两项检查结果

## 工作流程

```
/intent-check [options]
        ↓
┌───────────────────────────────────┐
│  确定检查范围                      │
│  - 指定路径 or 当前目录            │
│  - 单模块 or 全项目                │
└─────────────┬─────────────────────┘
              ↓
┌───────────────────────────────────┐
│  调用 intent-validate agent       │
│  → 格式合规报告                    │
└─────────────┬─────────────────────┘
              ↓
┌───────────────────────────────────┐
│  调用 intent-sync agent           │
│  → 代码一致性报告                  │
└─────────────┬─────────────────────┘
              ↓
┌───────────────────────────────────┐
│  汇总报告                          │
│  - 问题列表                        │
│  - 修复建议                        │
│  - 行动项                          │
└───────────────────────────────────┘
```

## 使用方法

### 完整检查

```
/intent-check
```

检查当前目录的 Intent，包括格式验证和代码同步。

### 指定路径

```
/intent-check src/core/
```

检查指定模块。

### 仅格式验证

```
/intent-check --validate
```

只运行 intent-validate，检查 Intent 文件格式。

### 仅代码同步

```
/intent-check --sync
```

只运行 intent-sync，检查代码与 Intent 一致性。

### 全项目检查

```
/intent-check --all
```

扫描并检查项目中所有 Intent 文件。

### Git 差异检查

```
/intent-check --git-diff origin/main
```

只检查相对于基准分支有变更的模块。

## 输出示例

```markdown
# Intent Check Report

> 检查时间: 2026-01-19 14:30
> 检查范围: src/core/

## 概览

| 检查项 | 状态 | 问题数 |
|--------|------|--------|
| 格式验证 | ⚠️ | 3 |
| 代码同步 | ❌ | 5 |

## 格式问题 (intent-validate)

### ⚠️ 警告

1. `src/core/intent/INTENT.md:45`
   - 缺少 ASCII 结构图

2. `src/core/intent/INTENT.md:78`
   - API 定义缺少返回值说明

### ❌ 错误

1. `src/core/intent/INTENT.md:12`
   - Section 标记语法错误: `::: lock` → `::: locked`

## 同步问题 (intent-sync)

### 新增未记录

| API | 文件 | 建议 |
|-----|------|------|
| `getChamberStats()` | chamber.js:89 | 添加到 Intent |

### 签名不一致

```diff
# deleteChamber
- Intent: deleteChamber(app, name)
+ Code:   deleteChamber(app, name, options)
```

### 边界违规

| 规则 | 位置 | 说明 |
|------|------|------|
| 禁止直接拼接路径 | routes/apps.js:45 | 应使用 chamber.getPath() |

## 行动建议

### 立即修复 (P0)
1. 修复 Section 标记语法错误
2. 修复边界违规

### 建议修复 (P1)
1. 更新 Intent: 添加 `getChamberStats()` API
2. 更新 Intent: `deleteChamber` 添加 options 参数

### 可选改进 (P2)
1. 添加 ASCII 结构图
2. 补充 API 返回值说明
```

## 退出码

| 码 | 含义 |
|----|------|
| 0 | 全部通过 |
| 1 | 有警告 |
| 2 | 有错误 |

可用于 CI/CD 集成：

```bash
/intent-check || exit 1
```

## 与其他命令配合

```
/intent-init              # 初始化
    ↓
/intent-interview         # 创建 Intent
    ↓
/intent-review            # 审批
    ↓
[开发实现]
    ↓
/intent-check             # ← 检查（本命令）
    ↓
修复问题 or 更新 Intent
    ↓
/intent-check             # 再次检查直到通过
```
