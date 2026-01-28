---
name: spec-interview
description: 通过系统性访谈完善技术规格文档，访谈完成后自动创建 OpenSpec proposal。适用于需求细化、技术方案设计、规范驱动开发等场景。
license: MIT
category: documentation
tags: [spec, interview, openspec, requirements, design]
---

# 规格访谈技能

## 概述

通过深入的苏格拉底式访谈，将草稿规格说明转化为完整、可执行的技术文档。访谈完成后自动创建 OpenSpec proposal，实现规范驱动开发（Spec-Driven Development）。

## 核心功能

- 系统性需求访谈与细化
- 工程原则审查（KISS、YAGNI、DRY、SOLID）
- 技术方案设计与权衡分析
- 自动生成 OpenSpec proposal
- 风险识别与缓解策略制定

## 工作流程

### 1. 文档读取与分析

读取 `plan.md` 或用户指定的文档，分析：
- 核心业务目标和价值主张
- 现有技术方案的完整性
- 模糊或缺失的关键信息
- 潜在的技术债务和风险点

### 2. 系统性访谈

使用 `AskUserQuestionTool` 进行多维度深度访谈：

#### A. 工程原则审查（必须）

**简单性检查（KISS & YAGNI）**
- 该功能是否为 MVP 必需？是否可延后至后续迭代？
- 是否存在更简单的方案能达到 80% 的效果？
- 当前抽象层次是否合理？是否存在过度设计？

**重复性识别（DRY）**
- 识别相似逻辑模式，评估抽象为通用模块的可行性
- 配置模式是否会在项目中重复出现？
- 是否可以通过代码生成或模板减少重复？

**架构健壮性（SOLID）**
- 模块职责是否单一？是否承担过多责任？
- 接口设计是否支持未来扩展？
- 依赖关系是否合理？是否存在循环依赖风险？

#### B. 技术实现细节

- 技术栈选型依据与替代方案对比
- 数据结构与算法选择的性能影响
- 性能瓶颈预测与优化策略
- 第三方依赖的必要性、许可证与维护风险
- 测试策略（单元测试、集成测试、E2E、性能测试）

#### C. API 设计（如适用）

- API 标题与描述的清晰性
- 资源路径与操作的逻辑分组
- 请求/响应模型的完整性
- 认证与授权机制
- 错误处理与状态码设计
- 版本控制策略
- 分页、过滤、排序规范
- 幂等性与并发控制

#### D. UI/UX 设计（如适用）

- 用户交互流程的完整性与一致性
- 边界情况的 UI 反馈（加载、错误、空状态、网络异常）
- 响应式设计与跨设备兼容性
- 可访问性（WCAG 标准）
- 国际化与本地化需求

#### E. 风险与权衡

- 技术债务的可接受程度与偿还计划
- 安全性考量（认证、授权、数据加密、输入验证）
- 可维护性 vs 开发速度的平衡
- 成本估算（开发时间、基础设施、运维成本）
- 供应商锁定风险

#### F. 边缘情况与异常处理

- 网络异常、超时、重试机制
- 并发冲突与数据一致性保证
- 降级方案与容错设计
- 日志记录与监控策略
- 灾难恢复与业务连续性

#### G. 项目约定与规范

- Shell 脚本跨平台兼容性（Bash/PowerShell）
- 文档格式与元数据规范（Markdown frontmatter）
- 目标平台部署要求（Claude Code/Codex CLI）
- 代码风格与 Lint 规则
- Git 工作流与分支策略

### 3. 高风险操作检测

如规格涉及以下操作，将主动提醒：

```
⚠️ 高风险操作检测
操作类型：[文件删除 / Git 强制推送 / 环境变量修改 / 数据库结构变更 / 批量依赖更新]
影响范围：[具体描述]
建议措施：
  - 回滚方案：[具体步骤]
  - 备份策略：[备份内容与频率]
  - 测试要求：[测试环境与验证标准]
请确认是否继续执行。
```

### 4. 创建 OpenSpec Proposal

访谈完成后，系统将自动调用 OpenSpec 工作流创建 proposal：

#### 调用方式

根据用户使用的 AI 工具，使用相应的命令：

**Claude Code / Codex / Qoder / RooCode**:
```
/openspec:proposal
```

**Cursor / Continue / GitHub Copilot / Windsurf**:
```
/openspec-proposal
```

**其他工具（AGENTS.md 兼容）**:
```
请创建一个 OpenSpec proposal
```

#### OpenSpec 输出结构

```
openspec/
├── changes/
│   └── <change-name>/
│       ├── proposal.md          # 变更提案
│       ├── tasks.md             # 任务清单
│       └── specs/               # 规格差异（delta）
│           └── <spec-name>/
│               └── spec.md      # 规格变更
└── specs/                       # 当前规格（归档后更新）
    └── <spec-name>/
        └── spec.md
```

#### 生成的文件内容

**1. Proposal** (`openspec/changes/<change-name>/proposal.md`)
- 变更概述与业务价值
- 技术方案与架构决策
- 工程原则审查结果
- 风险评估与缓解措施
- 成功指标与验收标准

**2. Tasks** (`openspec/changes/<change-name>/tasks.md`)
- 实施任务清单（基于访谈结果）
- 优先级排序（高/中/低）
- 任务依赖关系
- 预估工作量

**3. Spec Deltas** (`openspec/changes/<change-name>/specs/*/spec.md`)

使用 delta 格式标记变更：

```markdown
## 新增功能

+++ 新增的内容描述
+++ 包括接口定义、数据模型等

## 修改功能

--- 删除的旧内容
+++ 新增的替代内容

## 删除功能

--- 删除的内容描述
```

### 5. 后续工作流

创建 proposal 后，用户可以：

1. **审查与细化**
   - 检查生成的 proposal 和 specs
   - 根据需要进行调整和补充

2. **实施变更**
   - 使用 `/openspec:apply` 或 `/openspec-apply` 命令
   - 系统将根据 tasks.md 逐步实施

3. **归档变更**
   - 实施完成后使用 `/openspec:archive` 或 `/openspec-archive`
   - 将 spec deltas 合并到 `openspec/specs/` 中

## 技术约束

- **路径表示**: 使用双引号和正斜杠 `/`
- **搜索工具**: 优先使用 `rg` 而非 `grep`
- **Git 策略**: 除非明确要求，否则不执行 commit 或分支操作
- **代码理解**: 遵循先读后写（Read-before-Write）原则

## 提问原则

1. **深度优先**: 避免显而易见的问题，挖掘隐藏假设与风险
2. **结构化**: 按工程原则 → 技术细节 → 风险权衡的顺序提问
3. **引导式**: 帮助用户思考"为什么"而非仅仅"是什么"
4. **务实性**: 关注可落地性，避免过度理论化
5. **上下文感知**: 根据项目类型调整访谈重点（API/CLI/库/应用）

## 使用示例

### 触发方式

- "帮我完善这个 plan"
- "对这个技术方案进行深度访谈"
- "创建规格提案"
- "spec-driven development"

### 典型对话流程

**步骤 1: 启动访谈**

> **用户**: 帮我完善这个 plan
> 
> **系统**: 已读取 `plan.md`。该项目计划构建一个用户管理 API。在开始访谈前，请确认：这是一个面向公网的 API 还是内部服务？

**步骤 2: 深度提问**

> **用户**: 内部服务
> 
> **系统**: 明白。关于认证机制，内部服务通常有几种选择：
> 1. 服务间共享密钥（简单但安全性较低）
> 2. mTLS（高安全性但配置复杂）
> 3. 内部 OAuth 2.0（灵活但需要额外基础设施）
> 
> 考虑到您的团队规模和运维能力，倾向于哪种方案？或者是否已有统一的内部认证标准？

**步骤 3: 工程原则审查**

> **系统**: 关于用户角色管理，计划支持多少种角色？这是 MVP 必需的功能吗？
> 
> 根据 YAGNI 原则，如果初期只需要管理员和普通用户两种角色，建议先实现简单的二元权限模型，后续再扩展为 RBAC。这样可以减少 30-40% 的开发时间。您的看法如何？

**步骤 4: 创建 OpenSpec Proposal**

> **系统**: 访谈完成！现在为您创建 OpenSpec proposal...
> 
> [调用 /openspec:proposal 或等效命令]
> 
> ✅ 已创建 proposal: `openspec/changes/user-management-api/`
> 
> 后续步骤：
> 1. 审查 `proposal.md` 和 `tasks.md`
> 2. 使用 `/openspec:apply` 开始实施
> 3. 完成后使用 `/openspec:archive` 归档

## 与 OpenSpec 的集成优势

1. **需求锁定**: 访谈结果固化为 proposal，避免需求在聊天历史中丢失
2. **可追溯性**: 所有决策和权衡都记录在 proposal 中
3. **可审查性**: 团队成员可以审查 proposal 而无需阅读代码
4. **增量开发**: 通过 spec deltas 清晰展示每次变更的影响范围
5. **文档同步**: 归档后自动更新 living specs，保持文档与代码一致

## 最佳实践

- **准备充分**: 在访谈前准备好业务上下文和约束条件
- **诚实回答**: 对不确定的问题，可以要求提供多个选项及其权衡分析
- **迭代细化**: proposal 创建后可以继续访谈进行细化
- **团队协作**: 将 proposal 分享给团队成员进行 review
- **持续归档**: 完成的变更及时归档，保持 specs 目录的准确性

## 参考资源

- [OpenSpec 官方文档](https://github.com/Fission-AI/OpenSpec)
- [OpenSpec 网站](https://openspec.dev/)
- [Spec-Driven Development 指南](https://redreamality.com/garden/notes/openspec-guide)
