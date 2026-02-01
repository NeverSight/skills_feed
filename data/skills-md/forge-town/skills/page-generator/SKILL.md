---
name: page-generator
description: 基于标准化解剖学规范（Anatomy）生成前端页面结构；主动询问用户选择生成模式（无监督/有监督），支持自动生成 Wrapper、Content 和 Optional Store 模块
---

# 页面生成器 (Page Generator Skill)

## 任务目标
- 本 Skill 用于：在 `apps/web/src/pages` 目录下快速生成符合项目架构规范的新页面。
- 核心理念：**架构先行**。先生成符合规范的代码骨架（脚手架），再由开发者或 AI 填充业务逻辑。
- 触发条件：当用户要求“创建新页面”、“增加路由页面”或“生成页面脚手架”时。

## 生成模式 (Generation Modes)

本 Skill 支持两种生成模式，用户可在开始时选择：

### 无监督生成 (Unsupervised)
- **适用场景**：Anatomy 规范足够完备，AI 可自动推导完整结构。
- **特点**：全自动运行，无需人工干预。
- **流程**：直接使用 [judgeHasStore.ts](references/judgeHasStore.ts) 的逻辑判断所有选项，生成完整结构。

### 有监督生成 (Supervised)
- **适用场景**：存在选项判断的不确定性，需要人工确认。
- **特点**：在关键节点（如是否需要 Store）提问确认，AI 提供推荐但由用户决策。
- **流程**：使用 [judgeHasStore.ts](references/judgeHasStore.ts) 的逻辑判断提供推荐值，提问用户确认是否采纳。

## 主动模式选择 (Active Mode Selection)

**重要行为要求**：本技能必须在开始任何生成工作前主动询问用户选择生成模式。

### 询问时机
- **触发条件**：当用户请求创建新页面时
- **询问位置**：在所有分析和判断之前
- **强制要求**：不能跳过此步骤或默认选择模式

### 选择界面
提供清晰的选择界面，包含：
- **模式名称**：无监督生成 / 有监督生成
- **简要描述**：每种模式的特点和适用场景
- **推荐建议**：基于页面复杂度的智能推荐（可选）

### 用户决策
- **等待确认**：必须等待用户明确选择后再继续
- **不可跳过**：如果用户未选择，不得继续执行
- **可取消**：允许用户取消操作

## UI 复杂度控制 (UI Complexity Control)

### 复杂度等级
- **简单模式 (Simple)**: 基础布局 + 基础组件，适合展示型页面
- **标准模式 (Standard)**: 搜索/过滤 + 列表展示，适合数据管理页面  
- **复杂模式 (Complex)**: 多标签页 + 高级交互，适合功能丰富的页面

### 功能适配原则
- **基于需求生成**: 根据页面实际需求选择合适的UI复杂度
- **避免过度设计**: 不要添加用户不需要的功能
- **保持一致性**: 遵循现有页面的设计模式和交互方式

### 复杂度判断逻辑
- 使用 [judgeUIComplexity.ts](references/judgeUIComplexity.ts) 智能判断UI复杂度等级
- 基于页面名称、描述和功能需求自动推导
- 支持手动指定复杂度覆盖自动判断

## 使用示例 (Usage Examples)

### 典型使用场景

**用户输入**：创建一个用户管理页面，需要显示用户列表、支持搜索和筛选。

**Skill 响应**：
1. **主动询问生成模式**：显示模式选择界面，要求用户选择无监督或有监督生成
2. 根据用户选择，自动分析需求，判断需要 Store 和标准复杂度
3. 生成完整的页面结构和代码
4. 提供路由注册指导

具体配置示例请参考 [TEMPLATE_VIEW.md](references/TEMPLATE_VIEW.md) 中的配置示例部分。

### 生成结果示例
请参考 [ANATOMY.md](references/ANATOMY.md) 的目录结构树部分。

## 核心规范 (Knowledge Base)

### 输入参数规范
- `pageName`: 页面名称，必须为 PascalCase 格式
- `features.hasStore`: 是否需要状态管理（系统自动判断）
- `features.uiComplexity`: UI 复杂度等级（simple/standard/complex，系统自动判断）
- `description`: 页面功能描述，用于智能判断复杂度

本 Skill 的执行完全依赖以下规范文档，请在生成代码时仔细参考：
1.  **整体结构**: [references/ANATOMY.md](references/ANATOMY.md) (目录结构、命名规范)
2.  **输入规范**: [references/schema.ts](references/schema.ts) (参数校验)
3.  **Store判断逻辑**: [references/judgeHasStore.ts](references/judgeHasStore.ts) (智能判断是否需要Store)
4.  **UI复杂度判断**: [references/judgeUIComplexity.ts](references/judgeUIComplexity.ts) (智能判断UI复杂度等级)
5.  **Index模版**: [references/TEMPLATE_INDEX.md](references/TEMPLATE_INDEX.md) (入口文件写法)
6.  **Wrapper模版**: [references/TEMPLATE_WRAPPER.md](references/TEMPLATE_WRAPPER.md) (依赖注入层写法)
7.  **View模版**: [references/TEMPLATE_VIEW.md](references/TEMPLATE_VIEW.md) (UI层写法)
8.  **Store模版**: [references/TEMPLATE_STORE.md](references/TEMPLATE_STORE.md) (状态层写法)

## 质量保证 (Quality Assurance)

### 代码生成原则
- **类型安全**: 所有生成的代码必须通过 TypeScript 编译
- **性能优化**: 强制使用 Zustand selectors，避免不必要的重渲染
- **架构一致性**: 严格遵循项目的技术栈和模式
- **可维护性**: 生成的代码应易于理解和扩展

### 错误处理
- 生成前验证目标路径不存在，避免覆盖
- 提供清晰的错误信息和修复建议
- 支持回滚机制（如果生成失败）

## 操作步骤 (Workflow)

### 0. 模式选择 (Mode Selection) - 必须主动询问
**重要**：在开始任何生成工作前，必须主动询问用户选择哪种生成模式。不要默认使用无监督模式。

- **主动询问**：显示清晰的选择界面，让用户选择生成模式
- **选项说明**：
  - **无监督生成 (Unsupervised)**: 全自动判断所有参数，适合标准场景
  - **有监督生成 (Supervised)**: 在关键决策点询问用户确认，适合不确定或复杂场景
- **用户决策**：等待用户明确选择后再继续

### 0.1. 现有代码分析 (Existing Code Analysis)
- 检查目标路径是否已存在页面文件
- 如果存在，分析现有代码结构、样式和组件使用
- 询问用户是否要：
  - **重构现有代码**：保留业务逻辑与样式，只规范化架构
  - **重新生成**：完全替换为新架构
  - **增量改进**：在现有基础上添加缺失的架构元素

### 1. 意图解析与校验
- 读取用户指令，确定生成模式
- 使用 `schema.ts` 中的规则校验参数

### 1.1. Store 判断逻辑
- **无监督模式**：直接调用 `judgeHasStoreFromDescription()` 自动判断
- **有监督模式**：调用 `judgeHasStoreSupervised()` 获取推荐，询问用户确认

### 1.2. UI 复杂度判断
- **无监督模式**：直接调用 `judgeUIComplexity()` 自动判断
- **有监督模式**：调用 `judgeUIComplexitySupervised()` 获取推荐，询问用户确认

### 2. 规划文件列表
根据 `ANATOMY.md` 和 `hasStore` 参数，规划需要创建的文件路径。
- 基础文件：`index.ts`, `[PageName].tsx`, `[PageName]Content.tsx`
- 可选文件：`_store/index.ts`, `_store/provider.tsx`, `_store/[camelCase]Slice.ts`, `_store/[camelCase]Store.ts` (仅当 `hasStore=true`)

### 3. 代码生成 (按顺序)

请复用 References 中的模版，将 `{{PageName}}` 和 `{{camelCasePageName}}` 替换为实际值。

**步骤 3.1: 生成 Store 模块 (可选)**
- 如果 `hasStore=true`，参考 [TEMPLATE_STORE.md](references/TEMPLATE_STORE.md) 生成 4 个文件（Slice 模式）。
- 注意 `provider.tsx` 中必须包含 `@/hooks/useInit` 的引用。
- **重要验证**：确保 Store 仅存储 UI 状态，不存储业务实体数据。

**步骤 3.2: 生成 UI 视图 (Content)**
- 参考 [TEMPLATE_VIEW.md](references/TEMPLATE_VIEW.md)。
- 根据 `uiComplexity` 参数选择合适的UI复杂度：
  - **simple**: 基础布局，无搜索/排序功能，仅基础展示
  - **standard**: 添加搜索和排序功能，适合数据管理页面
  - **complex**: 添加标签页、高级过滤、批量操作等，适合功能丰富的页面
- 如果有 Store，保留 Store 连接的 TODO 注释。
- 使用 `cn` 和 Flex 布局生成基础骨架。
- **重要**: 避免过度设计，只生成实际需要的功能

**步骤 3.3: 生成 包装器 (Wrapper)**
- 参考 [TEMPLATE_WRAPPER.md](references/TEMPLATE_WRAPPER.md)。
- **关键**: 如果生成了 Store，Wrapper 必须正确引入并嵌套 `<StoreProvider>`。如果没生成 Store，则不要引入。
- **布局处理**: 优先使用路由层面的统一布局，仅在页面需要独特布局时在 Wrapper 中包含布局组件。

**步骤 3.4: 生成 入口 (Index)**
- 参考 [TEMPLATE_INDEX.md](references/TEMPLATE_INDEX.md)。
- 只导出包装器组件，不导出Content组件

**步骤 3.5: 质量验证 (新增)**
- 验证 Store 模块是否符合 [TEMPLATE_STORE.md](references/TEMPLATE_STORE.md) 的规范
- 检查是否仅存储 UI 状态，不存储业务数据
- 确认依赖注入和类型安全

### 4. 输出确认
- 告知用户页面已生成至指定路径。
- 提醒用户需在路由文件（如 `routeTree` 或 `router.tsx`）中注册该页面。
- 提供生成的组件使用示例。
- 建议运行测试验证生成代码。
