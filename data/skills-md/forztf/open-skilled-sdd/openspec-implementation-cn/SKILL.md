---
name: openspec-implementation-cn
description: 以测试与验证为先的方式，按序执行并实现已批准的规范提案。用于实施变更、应用提案、执行规范任务或按已批准计划构建。触发词包括 "openspec开发", "开发", "实施" "实现提案", "应用变更", "执行规范", "按顺序完成任务", "构建功能", "开始实施"。
---

# 规范实施

以任务为单位，循序执行并进行充分测试与验证，系统性地实现已批准的规范提案。

## 快速开始

实施遵循每个任务的 读 → 执行 → 测试 → 验证 循环：
1. 阅读完整提案与任务清单
2. 按顺序逐个执行任务
3. 为每个完成的任务进行测试
4. 仅在验证通过后标记完成

**关键规则**：使用 TodoWrite 跟踪进度。切勿跳过任务或将未完成工作标记为完成。

## 工作流

复制此清单并跟踪进度：

```
开发进度:
- [ ] 第 1 步：加载并理解提案
- [ ] 第 2 步：设置 TodoWrite 任务跟踪
- [ ] 第 3 步：按序执行任务
- [ ] 第 4 步：为每个任务进行测试与验证
- [ ] 第 5 步：更新常驻规范（如果适用）
- [ ] 第 6 步：标记提案为实施完成
```

### 第 1 步：加载并理解提案

开始之前，读取全部上下文：

```bash
# 读取提案
cat spec/changes/{change-id}/proposal.md

# 读取所有任务
cat spec/changes/{change-id}/tasks.json

# 读取规范差异以理解需求
find spec/changes/{change-id}/specs -name "*.md" -exec cat {} \;
```

**理解**：
- 变更的动因（来自 proposal.md）
- 预期结果是什么
- 哪些规范将被影响
- 验收标准（来自场景）

### 第 2 步：设置 TodoWrite 进行任务跟踪

在开始工作之前，将 tasks.json 中的task和step加载到 TodoWrite：

```markdown
**模式**：
读取 tasks.json → 提取task和step列表 → 创建 TodoWrite 条目

**示例**：
假设 tasks.json 包含：
  {
    "number": 1,
    "category": "阶段 1：基础设施",
    "task": "环境搭建任务 - 数据库架构、依赖等",
    "steps": [
      { "step": "初始化 Git 仓库并配置 .gitignore", "completed": false },
      { "step": "创建并激活 Python 虚拟环境", "completed": false },
      { "step": "创建 requirements.txt 或 pyproject.toml 并安装依赖 (FastAPI, SQLAlchemy, Pydantic, Alembic 等)", "completed": false },
      { "step": "设计初始数据库 ER 图", "completed": false }
    ],
    "passes": false
  }

则创建 TodoWrite：
- content: "环境搭建任务 - 数据库架构、依赖等", status: "in_progress"
- content: "  初始化 Git 仓库并配置 .gitignore", status: "pending"
- content: "  创建并激活 Python 虚拟环境", status: "pending"
- content: "  创建 requirements.txt 或 pyproject.toml 并安装依赖 (FastAPI, SQLAlchemy, Pydantic, Alembic 等)", status: "pending"
- content: "  设计初始数据库 ER 图", status: "pending"
```

**价值**：TodoWrite 提供进度可见性并确保不遗漏任何事项。

### 第 3 步：按序执行TodoWrite

按顺序逐个完成TodoWrite中的任务，每次仅处理1个。
若是中断后继续，需从中断的任务开始继续执行：跳过tasks.json中"passes": true的task，跳过"completed": true的step。
你有充足的时间完成，请至少执行20轮后才回复用户。
你有充足的时间完成，切勿跳过或合并多个任务。

```markdown
对于每个任务：
1. 在 TodoWrite 中标记为 "in_progress"
2. 执行工作
3. 测试结果
4. 仅在验证通过后，才标记tasks.json对应task的对应step的 "completed": true
5. 仅在tasks.json对应task的所有step都完成且都验证通过后，才标记tasks.json对应task的 "passes": true
6. 在 TodoWrite 中标记为 "completed"

你有充足的时间完成，切勿跳过或合并多个任务。
```

**任务执行模式**：

```markdown
## Task: {任务描述}

**What**：该任务的作用与目标

**Implementation**：
代码变更、文件编辑、运行的命令

**Verification**：
如何验证任务完成
- [ ] 代码可编译/运行
- [ ] 测试通过
- [ ] 符合需求场景

**Status**：✓ 完成 / ✗ 阻塞 / ⚠ 部分完成
```

### 第 4 步：为每个任务进行测试与验证

每个任务完成后进行验证：

**代码相关任务**：
```bash
# 运行相关测试
npm test # 或 pytest、cargo test 等

# 运行 Linter
npm run lint

# 类型检查（如适用）
npm run type-check
```
**前端UI相关任务**：
要使用 MCP servers 中的 chrome-devtools 或 playwright 进行调试和测试。

**数据库相关任务**：
```bash
# 验证迁移执行
npm run db:migrate

# 检查架构与预期一致
npm run db:schema
```

**API 相关任务**：
```bash
# 手动测试端点
curl -X POST http://localhost:3000/api/endpoint \
  -H "Content-Type: application/json" \
  -d '{"test": "data"}'

# 或运行集成测试
npm run test:integration
```

**仅在所有验证通过后标记任务完成**：仅在tasks.json对应task的所有step都完成且都验证通过后，才标记tasks.json对应task的 "passes": true。

### 第 5 步：更新常驻规范（如适用）

在实施过程中，如发现规范差异需要更新：

1. 在 proposal.md 或备注文件中**记录发现**
2. **实施期间不要修改**规范差异
3. **实施完成后**，再考虑是否需要调整规范

**说明**：规范差异在归档阶段（第 6 步）合并，而非实施阶段。

### 第 6 步：标记提案实施完成

在所有任务完成后：

```bash
# 创建完成标记
echo "Implementation completed: $(date)" > spec/changes/{change-id}/IMPLEMENTED
```

**告知用户**：
```markdown
## 实现提案

**提案**：{change-id}
**完成任务**：{数量}
**完成测试**：全部通过

**下一步**：将该变更归档以合并规范差异到常驻文档。
准备好后可回复 "openspec归档 {change-id}" 或 "归档提案"。
```

## 最佳实践

### 模式 1：任务被阻塞

若任务无法完成：

```markdown
**标记为阻塞**：
- 状态保持 "in_progress"（不要标记为 "completed"）
- 清晰记录阻塞原因
- 创建新的任务以解决阻塞
- 立即告知用户

**示例**：
任务："实现支付处理"
阻塞："缺少支付网关 API 凭据"
行动：创建新任务 "获取支付网关凭据"
```

### 模式 2：任务依赖

若任务存在依赖，先验证先决条件：

```bash
# 示例：数据库迁移必须在 API 代码之前
# 检查迁移状态
npm run db:status

# 仅在迁移成功后继续 API 任务
```

### 模式 3：增量测试

不要在最后一次性测试，应当逐步测试：

**好**：
```
任务 1：创建模型 → 测试模型 → 标记完成
任务 2：创建 API → 测试 API → 标记完成
任务 3：添加校验 → 测试校验 → 标记完成
任务 4：创建页面 → 测试校验 → 标记完成
```

**坏**：
```
任务 1、2、3、4 → 全部实现 → 一次性测试 → 调试失败
```

### 模式 4：常驻文档

**及时**更新 README、API 文档与注释：

```markdown
添加新 API 端点时，同时：
- 更新 API 文档
- 添加请求/响应示例
- 更新 OpenAPI/Swagger 规范
- 添加内联代码注释
```

## 进阶主题

**并行工作**：若任务确实互不依赖（如不同模块），可并行进行，但每项必须独立测试。

**集成点**：存在依赖关系时，使用集成测试验证连接有效。

**回滚策略**：对于高风险变更，部署前创建回滚任务。

## 常见模式

### 模式 1：数据库 + API + UI

典型顺序：
1. 数据库架构/迁移
2. 数据访问层（模型）
3. 业务逻辑层（服务）
4. API 端点（控制器）
5. UI 集成
6. 端到端测试

### 模式 2：功能开关

渐进式发布：
1. 在开关后实现功能
2. 开启开关进行测试
3. 部署时默认关闭开关
4. 逐步启用开关
5. 完全发布后移除开关

### 模式 3：破坏性 API 变更

对于 API 破坏性变更：
1. 实现新版本（v2）
2. 保持旧版本（v1）运行
3. 在 v1 中添加弃用提示
4. 迁移用户至 v2
5. 单独提案移除 v1

## 反模式避免

**不要**：
- 跳过单个任务的测试
- 在验证前标记任务完成
- 忽视失败测试（不要“以后再修”）
- 在测试前批量合并多个任务
- 在实施阶段修改常驻规范
- 打乱任务顺序（破坏依赖）

**要**：
- 立刻测试每个任务
- 在继续前修复失败测试
- 实时更新 TodoWrite
- 清晰记录阻塞项
- 及时同步进度与用户
- 保持原子且具描述性的提交

## 故障排查

### 问题：任务完成后测试失败

**解决方案**：
```markdown
1. 不要标记任务完成
2. 调试失败原因
3. 修复代码
4. 重新运行测试
5. 仅在通过后标记完成
```

### 问题：任务过大

**解决方案**：
```markdown
1. 拆分为子任务
2. 在 TodoWrite 中登记子任务
3. 依序完成子任务
4. 在全部子任务完成后标记父任务完成
```

### 问题：依赖未满足

**解决方案**：
```markdown
1. 暂停当前任务
2. 先完成依赖任务
3. 测试依赖项
4. 恢复原任务
```

## 参考资料

- [TASK_PATTERNS.md](reference/TASK_PATTERNS.md) - 常见任务执行模式
- [TESTING_STRATEGIES.md](reference/TESTING_STRATEGIES.md) - 按任务类型的测试方法

---

**Token 预算**：此 SKILL.md 约 350 行，低于建议的 500 行上限。