---
name: omo-agents
description: |
  oh-my-opencode 风格的多代理编排系统。提供 7 个专业代理协同工作：Sisyphus（主编排）、Oracle（架构顾问）、Librarian（文档研究）、Explore（代码搜索）、Frontend Engineer（UI/UX）、Document Writer（文档撰写）、Multimodal Looker（多模态分析）。当需要复杂开发任务、多角度问题解决、或特定专业领域帮助时使用。
category: ai-orchestration
tags: [multi-agent, orchestration, omo, sisyphus, oracle, omo-skills]
---

# OMO Agents - 多代理编排系统

基于 oh-my-opencode 理念的多代理协作系统，让不同专业代理各司其职，协同完成复杂任务。

## 代理一览

| 代理 | 角色 | 何时调用 |
|------|------|----------|
| **@sisyphus** | 主编排者 | 复杂任务规划、多步骤开发、协调其他代理 |
| **@oracle** | 架构顾问 | 架构决策、代码审查、技术选型、调试指导 |
| **@librarian** | 研究员 | 查找文档、研究开源实现、最佳实践挖掘 |
| **@explore** | 搜索专家 | 在代码库中定位代码、追踪依赖、理解结构 |
| **@frontend-engineer** | UI/UX 专家 | 界面设计实现、组件开发、动画交互 |
| **@document-writer** | 文档专家 | README、API 文档、架构文档、注释 |
| **@multimodal-looker** | 视觉分析师 | 图片分析、PDF 提取、图表解读 |

## 使用方式

### 直接调用

```
@oracle 这个架构设计合理吗？[附上架构图或代码]

@librarian Next.js 14 的 Server Actions 怎么处理错误？

@explore 找到处理支付的代码在哪里

@frontend-engineer 创建一个带动画的订阅表单组件

@document-writer 给这个 API 写文档

@multimodal-looker 分析这个错误截图
```

### 编排模式

对于复杂任务，使用 @sisyphus 自动编排：

```
@sisyphus 我要给这个电商项目添加用户评价功能

Sisyphus 会：
1. 分析任务，拆解子任务
2. 启动 @explore 搜索现有相关代码
3. 咨询 @oracle 确定架构方案
4. 请 @librarian 研究评价系统最佳实践
5. 委派 @frontend-engineer 实现评价 UI
6. 安排 @document-writer 编写文档
7. 并行执行独立任务，串行执行依赖任务
```

## 代理详情

### @sisyphus - 主编排者

**擅长**:
- 复杂功能开发的任务拆解
- 多代理协调和并行执行
- TODO 驱动的进度追踪
- 在必要时挑战用户需求

**工作流程**:
```
Phase 0: 意图判断 → 分类请求类型
Phase 1: 代码库评估 → 理解现有结构
Phase 2A: 探索研究 → 委派 @explore/@librarian
Phase 2B: 实现 → 创建 TODO，并行执行
```

### @oracle - 架构顾问

**擅长**:
- 架构设计评审和建议
- 技术选型分析
- 代码审查和质量评估
- 复杂问题的调试指导

**输出风格**:
- 第一层：直接回答（必须）
- 第二层：理由和权衡（按需）
- 第三层：边缘情况（相关时）

### @librarian - 研究员

**擅长**:
- 官方文档和 API 参考查找
- 开源项目实现研究
- GitHub issues/PRs 历史追溯
- 最佳实践总结

**三种模式**:
- TYPE A: 概念性问题
- TYPE B: 实现参考
- TYPE C: 上下文与历史

### @explore - 搜索专家

**擅长**:
- 在代码库中定位特定代码
- 追踪函数定义和引用
- 理解项目结构
- 搜索特定模式

**工具箱**:
- glob (文件搜索)
- grep (内容搜索)
- LSP (符号搜索)
- ast-grep (AST 模式搜索)
- git log/blame (历史追溯)

### @frontend-engineer - UI/UX 专家

**擅长**:
- 创建美观的界面组件
- 实现流畅的动画交互
- 响应式设计
- 即使没有设计稿也能创造精美 UI

**设计原则**:
- 像素级完美
- 动效是灵魂
- 直觉优先
- 大胆而克制

### @document-writer - 文档专家

**擅长**:
- README 编写
- API 文档
- 架构文档
- 用户指南
- JSDoc/注释

**写作原则**:
- 准确性第一
- 读者导向
- 代码即真相
- 渐进披露

### @multimodal-looker - 视觉分析师

**擅长**:
- 截图分析和信息提取
- PDF 内容解读
- 图表数据提取
- 架构图/流程图解析
- 设计稿分析

**核心价值**:
- 精准提取关键信息
- 避免上下文 token 浪费
- 结构化输出

## 最佳实践

### 1. 选择合适的代理

```
❌ 问 @frontend-engineer 架构问题
✅ 问 @oracle 架构问题

❌ 让 @oracle 搜索代码
✅ 让 @explore 搜索代码

❌ 让 @librarian 写文档
✅ 让 @document-writer 写文档
```

### 2. 提供足够上下文

```
❌ "@explore 找到那个函数"
✅ "@explore 找到处理用户认证的函数，可能在 auth 或 user 目录下"

❌ "@oracle 这样好吗"
✅ "@oracle 用 Redux 还是 Zustand 管理这个中等规模 React 项目的状态？"
```

### 3. 复杂任务用 @sisyphus

```
简单任务 → 直接调用专业代理
复杂任务 → @sisyphus 编排协调
不确定 → @sisyphus 会帮你判断
```

## 代理协作示例

**任务**: "重构用户模块，改进代码质量"

```
1. @sisyphus 接收任务，分析范围

2. @sisyphus → @explore
   "搜索所有 user 相关的代码文件和依赖"

3. @sisyphus → @oracle
   "评审当前用户模块架构，指出问题和改进方向"

4. @sisyphus → @librarian
   "研究类似规模项目的用户模块最佳实践"

5. @sisyphus 综合信息，制定重构计划

6. @sisyphus 执行重构
   - 核心逻辑：自己处理
   - UI 相关：委派 @frontend-engineer
   
7. @sisyphus → @document-writer
   "更新用户模块的 API 文档"

8. 完成，提交 TODO 清单和变更摘要
```
