---
name: tool-dev
description: 专门用于开发 FastGPT 系统工具和工具集的技能，包含 Zod 类型安全验证、共享配置管理和完整测试工作流。适用于创建新的 FastGPT 工具、开发包含子工具的工具集、或实现带有正确配置和测试的 API 集成。
license: MIT
category: development
author: FastGPT Team
version: 2.0.0
---

# FastGPT 工具开发技能

为开发 FastGPT 系统工具提供简化的工作流程，包括类型安全、正确的配置管理和自动化测试。

## 何时使用此技能

在进行 FastGPT 工具开发任务时使用此技能：
- 创建新的独立工具或工具集
- 实现带有适当身份验证的 API 集成
- 开发具有 Zod 验证和 TypeScript 类型的工具
- 在工具集子工具之间设置共享配置
- 为工具功能编写全面的测试

## 核心能力

- **类型安全开发**: Zod schema 验证 + TypeScript 类型推导
- **配置管理**: 工具集内共享密钥配置，支持版本控制
- **系统化测试**: 自动化测试生成和验证
- **代码质量**: 内置代码审查和优化步骤
- **最佳实践**: 遵循 FastGPT 设计模式和规范

---

## 开发工作流

开发 FastGPT 工具时遵循此 4 阶段工作流程。每个阶段都有明确的目标、操作和质量标准。

### 阶段 1: 需求与设计

**目标**: 创建全面的需求文档

**操作步骤**:
1. 查看 `references/design_spec.md` 中的现有设计模式
2. 定义工具/工具集的范围和功能
3. 使用 Zod schemas 指定输入/输出配置
4. 记录 API 要求和测试凭证
5. 使用 `references/requirement_template.md` 作为起点

**质量标准**:
- ✅ 所有功能清晰定义
- ✅ 输入/输出类型已指定
- ✅ 边界情况和错误场景已记录

**交付物**: 完整的设计文档（参见 `references/requirement_template.md`）

---

### 阶段 2: 实现

**目标**: 按照 FastGPT 模式开发工具

**操作步骤**:
1. 创建目录结构（`tool/` 或 `toolset/children/`）
2. 实现 `config.ts`，包含正确的版本列表
3. 开发 `src/index.ts`，包含 Zod 验证的业务逻辑
4. 如需要，添加共享模块（`client.ts`、`utils.ts`）

**代码规范**:
- 采用 camelCase 命名规范
- 类型导入: `import { type Foo } from 'bar'`
- 最小化错误处理（让框架处理常见情况）
- 函数简洁、职责单一

**质量标准**:
- ✅ TypeScript 编译无错误
- ✅ 遵循现有项目模式
- ✅ 配置结构正确

---

### 阶段 3: 测试与验证

**目标**: 通过全面测试确保可靠性

**操作步骤**:
1. 安装依赖: `bun install`
2. 在 `test/index.test.ts` 中编写测试用例
3. 运行测试套件: `bun test`
4. 修复失败的测试和边界情况
5. 验证 TypeScript: `bun run tsc --noEmit`

**测试覆盖**:
- 输入验证（Zod schema 边界情况）
- 业务逻辑正确性
- 错误处理场景
- 资源清理（如适用）

**质量标准**:
- ✅ 所有测试通过
- ✅ 无 TypeScript 错误
- ✅ 构建成功: `bun run build`

---

### 阶段 4: 审查与优化

**目标**: 完成前优化代码质量

**操作步骤**:
1. 代码审查，寻找简化机会
2. 删除未使用的代码和依赖
3. 优化性能瓶颈
4. 最终集成测试
5. 更新文档

**质量标准**:
- ✅ 代码清晰且可维护
- ✅ 无不必要的复杂性
- ✅ 最终测试运行成功

---

## 快速参考

### 常用命令
```bash
# 安装依赖
bun install

# 运行测试
bun test

# 类型检查
bun run tsc --noEmit

# 构建
bun run build

# 测试特定文件
bun test test/index.test.ts
```

### 文件模板
访问详细的模板和规范：
- **需求模板**: `references/requirement_template.md`
- **完整设计规范**: `references/design_spec.md`
- **工具配置示例**: design_spec.md 第 4.1 节
- **工具集配置示例**: design_spec.md 第 5.1 节
- **Zod 验证模式**: design_spec.md 第 7.2 节
- **测试结构**: design_spec.md 第 9.1 节

### 关键设计原则
1. **关注点分离**: 配置 ≠ 逻辑 ≠ 工具
2. **类型安全**: Zod 验证 → TypeScript 类型推导
3. **共享配置**: 工具集密钥由子工具继承
4. **单一职责**: 一个工具 = 一个功能
5. **快速失败**: 让框架处理常见错误

---

## 绑定资源

### Scripts 目录
- `init_skill.py`: 初始化具有正确结构的新 skill
- `package_skill.py`: 验证并打包 skill 为可分发的 zip 文件
- `quick_validate.py`: 快速验证 skill 结构

### References 目录
- `design_spec.md`: 完整的 FastGPT 工具设计规范（10 个章节）
- `requirement_template.md`: 创建工具需求文档的模板

### 使用模式
1. 查看详细技术规范 → 阅读 `references/design_spec.md`
2. 创建新工具需求 → 使用 `references/requirement_template.md`
3. 管理 skill → 使用 `scripts/*.py` 工具

---

## 相关文档
- 工具类型: `@tool/type/tool` 中的 `ToolTypeEnum`
- 配置类型: `@tool/type` 中的 `ToolConfigType`、`ToolSetConfigType`
- FastGPT 类型: `WorkflowIOValueTypeEnum`、`FlowNodeInputTypeEnum`
