---
name: refactor
description: Systematic refactoring skill with test coverage requirements. Supports scope analysis, test-first refactoring, and integration with DevDocs workflow. Use when users need to refactor code, improve code quality, or restructure existing implementations. Triggers on keywords like "refactor", "重构", "优化代码", "代码改造", "tech debt", "技术债".
allowed-tools: Read, Write, Glob, Grep, Edit, Bash, AskUserQuestion, TodoWrite
---

# Refactor

系统化重构 skill，确保重构过程安全、可追溯、符合质量标准。

## Language

- Accept questions in both Chinese and English
- Always respond in Chinese
- Generate all documents in Chinese

## Trigger Conditions

- 用户需要重构现有代码
- 用户要求优化代码质量
- 用户提到技术债、代码改造
- 用户要求审查并改进现有实现

## 核心原则

### 重构安全原则

```
┌─────────────────────────────────────────────────────────┐
│                    重构前必须满足                         │
├─────────────────────────────────────────────────────────┤
│  1. 有明确的重构范围                                      │
│  2. 有足够的测试覆盖（≥80%）                              │
│  3. 所有测试通过                                         │
├─────────────────────────────────────────────────────────┤
│                    重构过程中                             │
├─────────────────────────────────────────────────────────┤
│  1. 小步重构，每步可验证                                  │
│  2. 每步后运行测试                                        │
│  3. 不添加新功能                                         │
├─────────────────────────────────────────────────────────┤
│                    重构后必须满足                         │
├─────────────────────────────────────────────────────────┤
│  1. 所有测试通过                                         │
│  2. 覆盖率不降低                                         │
│  3. 生成重构报告                                         │
└─────────────────────────────────────────────────────────┘
```

### 与其他 Skills 的协作

| 场景 | 协作 Skill | 说明 |
|------|------------|------|
| 代码无法测试 | `/devdocs-retrofit` | 逆向分析后重写 |
| UI 重构 | `/ui-skills` | 应用 UI 约束规范 |
| 代码质量检查 | `/code-quality` | 应用 MTE 原则 |
| 需要文档化 | DevDocs 流程 | 生成规范文档 |
| **编写/补充测试** | `/testing-guide` | 测试质量约束（断言、Mock、变异测试） |

---

## Workflow

```
1. 确定重构范围
   │
   ├── 用户指定范围 → Step 2
   └── 未指定范围 → 系统审查 → 发现问题 → 用户确认范围
   │
   ▼
2. 评估测试状态
   │
   ├── 有测试且覆盖 ≥80% → Step 4
   ├── 有测试但覆盖 <80% → Step 3（补充测试）
   └── 无测试 → Step 3（新建测试）
   │
   ▼
3. 补充/新建测试
   │
   ├── 可测试 → 编写测试 → 确保覆盖率 ≥80% → Step 4
   └── 不可测试 → 标记为"需要重写" → Step 5
   │
   ▼
4. 执行重构
   │
   ├── 普通代码 → 应用 /code-quality
   └── UI 代码 → 应用 /ui-skills
   │
   ▼
5. 重写流程（如需要）
   │
   └── 调用 /devdocs-retrofit 逆向 → 生成文档 → 重新实现
   │
   ▼
6. 验证与报告
   │
   ├── 运行所有测试
   ├── 检查覆盖率
   └── 生成重构报告
```

---

## Step 1: 确定重构范围

### 1.1 用户指定范围

如果用户明确指定了重构范围，直接使用。

```
用户指定范围示例：
- "重构 src/services/user.ts"
- "重构用户认证模块"
- "优化 UserService 类"
```

### 1.2 系统审查（未指定范围时）

使用以下检查清单审查代码：

#### Code Smells 检查清单

| 问题类型 | 检测方法 | 优先级规则 |
|----------|----------|------------|
| 过长函数 | 行数 > 50 | P0 如果 > 100，P1 如果 > 50 |
| 过多参数 | 参数 > 5 | P1 |
| 过深嵌套 | 嵌套 > 3 层 | P1 |
| 重复代码 | 相似代码块 ≥ 3 处 | P0 |
| 上帝类 | 行数 > 500 或职责 > 3 | P0 |
| 特性依恋 | 频繁访问其他类数据 | P2 |
| 数据泥团 | 多参数总是一起出现 | P2 |

#### 审查报告模板

```markdown
# 代码审查报告

## 审查范围

- **目录**: <path>
- **文件数**: <count>
- **代码行数**: <lines>

## 发现的问题

### P0 - 必须修复

| # | 文件 | 问题 | 描述 |
|---|------|------|------|
| 1 | `src/services/user.ts` | 上帝类 | UserService 超过 800 行，包含 5 种职责 |
| 2 | `src/utils/helper.ts` | 重复代码 | processData 函数在 4 处有相似实现 |

### P1 - 建议修复

| # | 文件 | 问题 | 描述 |
|---|------|------|------|
| 1 | `src/api/handler.ts:45` | 过长函数 | handleRequest 函数 78 行 |
| 2 | `src/models/order.ts:120` | 过深嵌套 | validateOrder 嵌套 4 层 |

### P2 - 可选修复

| # | 文件 | 问题 | 描述 |
|---|------|------|------|
| 1 | `src/services/payment.ts` | 特性依恋 | 频繁访问 Order 对象属性 |

## 建议重构顺序

1. [ ] UserService 拆分（P0，影响范围大）
2. [ ] 消除 processData 重复（P0，多处引用）
3. [ ] handleRequest 拆分（P1）
4. [ ] validateOrder 简化（P1）

## 预计影响

- 涉及文件: 12
- 可能影响的测试: 45
- 风险评估: 中
```

### 1.3 用户确认

使用 AskUserQuestion 让用户确认重构范围：

```
发现以下问题，请选择要重构的范围：

1. **全部重构** - 按优先级依次处理所有问题
2. **仅 P0** - 只处理必须修复的问题
3. **指定范围** - 手动选择要重构的项目
4. **暂不重构** - 仅保存审查报告
```

---

## Step 2: 评估测试状态

### 2.1 检测测试覆盖率

```bash
# 检测测试框架
# Jest / Vitest / Mocha / pytest 等

# 运行覆盖率报告
npm run test:coverage  # 或对应命令

# 检查目标文件覆盖率
```

### 2.2 测试状态分类

| 状态 | 条件 | 下一步 |
|------|------|--------|
| 充分 | 行覆盖 ≥80%，分支覆盖 ≥80% | → Step 4 执行重构 |
| 不足 | 有测试但覆盖率 <80% | → Step 3 补充测试 |
| 无测试 | 目标范围无测试文件 | → Step 3 新建测试 |
| 不可测试 | 代码结构导致无法编写有效测试 | → Step 5 重写流程 |

### 2.3 可测试性评估

代码被判定为"不可测试"的条件：

```
不可测试的代码特征：
- [ ] 硬编码外部依赖（数据库、API、文件系统）
- [ ] 无法注入依赖（构造函数中 new 具体类）
- [ ] 业务逻辑与 IO 混合，无法分离
- [ ] 全局状态依赖
- [ ] 无法 Mock 的第三方库深度耦合

如果满足 2 个以上条件，标记为"不可测试"
```

---

## Step 3: 补充/新建测试

> **重要**: 编写测试时必须遵循 `/testing-guide` 的质量约束

### 3.1 测试策略

参考 `/testing-guide` 测试质量金字塔：

```
测试质量要求（从基础到高级）:
Level 1: 覆盖率 - 行/分支 ≥ 80%
Level 2: 断言质量 - 禁止弱断言，验证具体值
Level 3: 测试有效性 - 变异得分 ≥ 80%（推荐）
```

### 3.2 测试编写规范

遵循 `/testing-guide` 的约束：

- **测试依据来自需求，不是代码**
- **每个测试必须有具体断言**（禁止 toBeDefined, toBeTruthy 等弱断言）
- **测试名称描述预期行为**：`[方法] 应该 [行为] 当 [条件]`
- **Mock 只用于外部依赖**，不 Mock 内部实现

### 3.3 覆盖率验证

```bash
# 运行测试并检查覆盖率
npm run test:coverage -- --collectCoverageFrom='<target-path>'

# 确保满足：
# - 行覆盖率 ≥ 80%
# - 分支覆盖率 ≥ 80%
```

### 3.4 变异测试验证（推荐）

```bash
# 验证测试有效性
npx stryker run --mutate '<target-path>'

# 目标：变异得分 ≥ 80%
```

> 详细的测试编写指导、Mock 策略、变异测试配置请参考 `/testing-guide`

---

## Step 4: 执行重构

### 4.1 重构前检查

- [ ] 测试全部通过
- [ ] 覆盖率满足要求（≥80%）
- [ ] 已创建 Git 分支或可回滚

### 4.2 重构策略

#### 普通代码重构

应用 `/code-quality` MTE 原则：

| 问题 | 重构手法 | 验证 |
|------|----------|------|
| 过长函数 | 提取函数 | 每个函数 ≤50 行 |
| 过多参数 | 参数对象 | 参数 ≤5 个 |
| 过深嵌套 | 早返回、提取函数 | 嵌套 ≤3 层 |
| 重复代码 | 提取公共函数 | 无重复块 |
| 上帝类 | 拆分职责 | 每类单一职责 |

#### UI 代码重构

调用 `/ui-skills` 约束：

```
UI 重构检查点：
- [ ] 使用 Tailwind CSS 默认值
- [ ] 使用可访问组件原语（Base UI/Radix/React Aria）
- [ ] 动画只使用 transform/opacity
- [ ] 遵循 prefers-reduced-motion
- [ ] 空状态有明确的下一步操作
```

### 4.3 小步重构原则

```
每次重构步骤：
1. 执行一个重构操作
2. 运行测试
3. 测试通过 → 继续下一步
4. 测试失败 → 回滚，重新分析
5. 提交（可选，推荐频繁提交）
```

### 4.4 重构进度追踪

使用 TodoWrite 追踪重构进度：

```
重构任务示例：
1. [x] 提取 validateUser 函数
2. [x] 将 UserService 拆分为 UserQueryService
3. [ ] 将 UserService 拆分为 UserCommandService
4. [ ] 消除 processData 重复
```

---

## Step 5: 重写流程

当代码被判定为"不可测试"时，进入重写流程。

### 5.1 触发条件

```
进入重写流程的条件：
- 代码被评估为"不可测试"
- 重构后测试仍无法达到 80% 覆盖率
- 用户明确要求重写
```

### 5.2 重写流程

```
1. 调用 /devdocs-retrofit
   │
   ├── 模式：代码逆向推导
   ├── 输出：需求文档、系统设计
   │
   ▼
2. 基于 DevDocs 文档重新实现
   │
   ├── 遵循 /code-quality MTE 原则
   ├── UI 部分遵循 /ui-skills
   │
   ▼
3. 编写测试（测试先行）
   │
   ├── 覆盖率 ≥ 80%
   │
   ▼
4. 实现新代码
   │
   ▼
5. 迁移验证
   │
   ├── 功能对比测试
   ├── 性能对比（如适用）
   └── 回归测试
```

### 5.3 重写文档

重写时生成的文档：

```
docs/devdocs/
├── 01-requirements.md       # 从代码逆向的需求
├── 02-system-design.md      # 新设计（可测试）
├── 03-test-cases.md          # 测试方案
└── 05-refactor-rewrite.md   # 重写报告
```

---

## Step 6: 验证与报告

### 6.1 验证清单

- [ ] 所有测试通过
- [ ] 覆盖率 ≥ 80%（行和分支）
- [ ] 覆盖率未降低
- [ ] 无新增 lint 警告
- [ ] 功能行为不变

### 6.2 重构报告模板

```markdown
# 重构报告

## 概览

- **重构范围**: <scope>
- **重构时间**: <timestamp>
- **重构类型**: 普通重构 / 重写

## 重构前状态

| 指标 | 值 |
|------|-----|
| 文件数 | 5 |
| 代码行数 | 1,200 |
| 测试覆盖率（行） | 45% |
| 测试覆盖率（分支） | 38% |
| 主要问题 | 上帝类、过长函数 |

## 重构后状态

| 指标 | 值 | 变化 |
|------|-----|------|
| 文件数 | 8 | +3 |
| 代码行数 | 980 | -220 |
| 测试覆盖率（行） | 85% | +40% |
| 测试覆盖率（分支） | 82% | +44% |

## 重构内容

### 已完成

1. [x] UserService 拆分为 UserQueryService + UserCommandService
2. [x] 提取 validateUser、formatUser 函数
3. [x] 消除 processData 重复代码
4. [x] 补充单元测试 23 个

### 变更文件

| 文件 | 操作 | 说明 |
|------|------|------|
| `src/services/user.ts` | 修改 | 拆分职责 |
| `src/services/user-query.ts` | 新增 | 查询服务 |
| `src/services/user-command.ts` | 新增 | 命令服务 |
| `src/utils/user-utils.ts` | 新增 | 提取的工具函数 |
| `tests/services/user.test.ts` | 修改 | 补充测试 |

## 测试报告

```
Test Suites: 12 passed, 12 total
Tests:       89 passed, 89 total
Coverage:
  Lines:     85.2%
  Branches:  82.1%
  Functions: 88.5%
```

## 风险与注意事项

- `UserQueryService` 和 `UserCommandService` 需要分别注入
- 原 `UserService` 保留为门面类，后续可逐步迁移调用方

## 下一步建议

1. 更新调用方代码，逐步使用新的服务类
2. 监控生产环境，确保行为一致
3. 考虑删除原 UserService 门面类
```

---

## Output

### 输出文件

```
docs/devdocs/
├── 05-refactor-audit.md        # 代码审查报告（Step 1）
├── 05-refactor-plan.md         # 重构计划（Step 1 确认后）
├── 05-refactor-report.md       # 重构报告（Step 6）
└── 05-refactor-rewrite.md      # 重写报告（如适用）
```

### 文件命名规则

- 普通重构：`05-refactor-*.md`
- 如果是针对特定模块：`05-refactor-<module>-*.md`

---

## Constraints

### 范围约束

- [ ] **必须明确重构范围后才能开始**
- [ ] 未指定范围时必须先进行代码审查
- [ ] 用户必须确认重构范围

### 测试约束

- [ ] **重构前测试覆盖率必须 ≥80%**
- [ ] 无测试或覆盖不足时必须先补充测试
- [ ] 代码不可测试时必须进入重写流程
- [ ] **重构后所有测试必须通过**
- [ ] **重构后覆盖率不得降低**

### 过程约束

- [ ] **每步重构后必须运行测试**
- [ ] **不得在重构中添加新功能**
- [ ] 使用 TodoWrite 追踪重构进度
- [ ] 频繁提交，保持可回滚

### 协作约束

- [ ] UI 重构必须应用 `/ui-skills` 约束
- [ ] 代码重构必须应用 `/code-quality` MTE 原则
- [ ] 重写时必须使用 `/devdocs-retrofit` 生成文档

### 文档约束

- [ ] **必须生成重构报告**
- [ ] 重写时必须生成 DevDocs 文档
- [ ] 报告必须包含前后对比

---

## Error Handling

### 测试失败

```
重构后测试失败。

失败的测试:
- UserService.test.ts: validateUser should return false for invalid email

操作选项:
1. 回滚此次重构步骤
2. 查看失败详情并修复
3. 跳过此测试（不推荐）

建议：回滚到上一个通过的状态，重新分析重构方案。
```

### 覆盖率不足

```
当前测试覆盖率不满足重构要求。

目标范围: src/services/user.ts
当前覆盖率:
  - 行覆盖: 45% (要求 ≥80%)
  - 分支覆盖: 38% (要求 ≥80%)

操作选项:
1. **补充测试**（推荐）- 为未覆盖代码编写测试
2. 降低要求 - 以当前覆盖率开始重构（风险较高）
3. 标记为不可测试 - 进入重写流程
```

### 代码不可测试

```
目标代码被评估为"不可测试"。

原因:
- [x] 硬编码数据库连接
- [x] 业务逻辑与 IO 混合
- [ ] 全局状态依赖

建议进入重写流程:
1. 使用 /devdocs-retrofit 逆向分析代码
2. 生成需求和设计文档
3. 按照可测试的设计重新实现

是否进入重写流程？
```

---

## Integration with DevDocs

### 在 DevDocs 流程中的位置

```
DevDocs 工作流（含重构）:

新项目:
/devdocs-requirements → /devdocs-system-design → /devdocs-test-cases → /devdocs-dev-tasks
                                                                              │
                                                                              ▼
                                                                           开发实现
                                                                    ┌────────┼────────┐
                                                                    ▼        ▼        ▼
                                                              /code-quality /ui-skills /refactor
                                                                                        │
已有项目:                                                                               │
/devdocs-retrofit ←─────────────────────────────────────────────────────────────────────┘
       │                                                              (不可测试时)
       ▼
  标准化文档 → 重新实现
```

### 与其他 Skills 的调用关系

```
/refactor
    │
    ├── 代码审查 → /code-quality (MTE 原则)
    │
    ├── UI 重构 → /ui-skills (UI 约束)
    │
    ├── 不可测试 → /devdocs-retrofit (逆向分析)
    │                    │
    │                    ├── /devdocs-requirements
    │                    ├── /devdocs-system-design
    │                    └── /devdocs-test-cases
    │
    └── 测试编写 → /devdocs-test-cases (测试策略参考)
```
