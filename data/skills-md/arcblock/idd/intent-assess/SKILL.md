---
name: intent-assess
description: Assess if IDD fits your project and learn about Intent-Driven Development. Use /intent-assess to evaluate project suitability or /intent-assess --learn for IDD education.
---

# Intent Assess

评估项目是否适合 IDD，并教育 IDD 方法论。

## 两个模式

### 1. 评估模式 (Assessment)

```
/intent-assess
```

分析当前项目，评估是否适合采用 IDD。

### 2. 学习模式 (Learning)

```
/intent-assess --learn
```

教育 IDD 方法论，解释核心概念。

---

## 评估模式

### 工作流程

```
/intent-assess
        ↓
┌───────────────────────────────────┐
│  Phase 1: 项目分析                │
│  - 项目类型识别                   │
│  - 代码库规模                     │
│  - 现有文档情况                   │
│  - 团队协作模式                   │
└─────────────┬─────────────────────┘
              ↓
┌───────────────────────────────────┐
│  Phase 2: 适配度评估              │
│  - 计算匹配分数                   │
│  - 识别优势和挑战                 │
└─────────────┬─────────────────────┘
              ↓
┌───────────────────────────────────┐
│  Phase 3: 建议                    │
│  - 是否推荐 IDD                   │
│  - 如何开始                       │
│  - 替代方案（如不适合）           │
└───────────────────────────────────┘
```

### 评估维度

| 维度 | 有利于 IDD | 不利于 IDD |
|------|-----------|-----------|
| **项目类型** | 系统软件、框架、库 | 简单脚本、一次性项目 |
| **代码规模** | 中大型 (>5k LOC) | 小型 (<1k LOC) |
| **团队协作** | 多人协作、AI 辅助 | 单人独立开发 |
| **架构复杂度** | 多模块、需要边界 | 单模块、简单结构 |
| **迭代方式** | 持续迭代、长期维护 | 一次性交付 |
| **AI 工具使用** | 使用 Claude/Copilot | 纯人工开发 |

### 评估报告示例

```markdown
# IDD Assessment Report

> Project: ainecore
> Date: 2026-01-19

## 适配度评分: 85/100 ⭐⭐⭐⭐

## 项目特征

| 特征 | 当前状态 | IDD 契合度 |
|------|---------|-----------|
| 项目类型 | 框架/平台 | ✅ 高 |
| 代码规模 | ~15k LOC | ✅ 高 |
| 模块数量 | 12 个 | ✅ 高 |
| 团队规模 | 3 人 + AI | ✅ 高 |
| 现有文档 | 部分 | 🟡 中 |

## 优势

- ✅ 多模块架构，需要清晰边界定义
- ✅ 使用 AI 辅助开发，Intent 可指导 AI
- ✅ 长期维护项目，文档价值高
- ✅ 已有部分设计文档，可迁移

## 挑战

- ⚠️ 需要建立 Intent 编写习惯
- ⚠️ 现有代码需要补充 Intent
- ⚠️ 团队需要学习 IDD 方法

## 建议

### 推荐: 采用 IDD ✅

该项目非常适合 IDD：
1. 多模块架构需要清晰的边界和契约
2. AI 辅助开发可以直接使用 Intent 作为上下文
3. 长期维护价值高

### 启动建议

1. **从核心模块开始**
   - 先为 `src/core/` 编写 Intent
   - 建立 Intent 模板和规范

2. **渐进式推广**
   - 新功能必须先写 Intent
   - 老代码逐步补充

3. **工具配套**
   - 安装 IDD plugin
   - 配置 CI/CD 集成

### 预期收益

- 🎯 AI 编码效率提升 ~30%
- 🎯 架构边界更清晰
- 🎯 新成员 onboard 更快
- 🎯 减少 "文档过时" 问题
```

---

## 学习模式

### 交互式教学

```
/intent-assess --learn
```

通过问答方式教授 IDD：

```
┌───────────────────────────────────┐
│  欢迎学习 IDD！                   │
│                                   │
│  我将介绍：                        │
│  1. 什么是 IDD                    │
│  2. IDD vs TDD vs SDD             │
│  3. Intent 文件结构               │
│  4. 实际案例                       │
│                                   │
│  你想从哪个话题开始？              │
└───────────────────────────────────┘
```

### 核心概念讲解

#### 1. 什么是 IDD

```
开发方法论演进：

Traditional:  Code → Test → Docs
              (文档经常过时)

SDD:          Spec → Code → Test
              (Spec 分散，难以维护)

TDD:          Test → Code → Docs
              (测试不能捕捉设计理由)

IDD:          Intent → Test → Code → Sync
              (Intent 作为唯一真相来源)
```

#### 2. Intent 三层结构

```
┌─────────────────────────────────────┐
│  Layer 1: 结构图 (Structure)        │
│  - 目录结构、数据结构、模块关系      │
│  - ASCII 图优先                     │
├─────────────────────────────────────┤
│  Layer 2: 约束规则 (Constraints)    │
│  - 依赖方向、边界规则、不变式        │
│  - 可转化为测试断言                  │
├─────────────────────────────────────┤
│  Layer 3: 行为示例 (Examples)       │
│  - 输入 → 输出 示例                 │
│  - 边界情况                         │
└─────────────────────────────────────┘
```

#### 3. IDD vs SDD 对比

```markdown
| 维度 | SDD | IDD |
|------|-----|-----|
| 组织方式 | 按类型 (功能/UX/技术) | 按模块 |
| 核心载体 | 文字描述 | 结构图 |
| 粒度 | 细分 User Story | 完整 Pattern |
| Task 管理 | 独立 Task 文件 | AI 自主分解 |
| LLM 友好度 | 需要拼装上下文 | 一次理解完整 |
```

#### 4. 实际案例

展示一个真实的 Intent 文件，解释各部分作用。

### 快速参考

```
/intent-assess --learn --topic <topic>
```

可选 topic：
- `what` - 什么是 IDD
- `vs-sdd` - IDD vs SDD 对比
- `vs-tdd` - IDD vs TDD 对比
- `structure` - Intent 文件结构
- `workflow` - IDD 工作流程
- `approval` - Section 审批机制
- `best-practices` - 最佳实践

---

## 与其他命令配合

```
/intent-assess                # 评估项目
    ↓ (如果适合)
/intent-assess --learn        # 学习 IDD
    ↓
/intent-init                  # 初始化 IDD
    ↓
/intent-interview             # 创建 Intent
```
