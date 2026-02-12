---
name: page-best-practice
description: 基于标准化解剖学规范（Anatomy）生成前端页面结构；主动询问用户选择生成模式（无监督/有监督），支持自动生成 Wrapper、Content 和 Optional Store 模块
---

# 页面生成器 (Page Generator Skill)

## 任务目标
- 本 Skill 用于：在 `apps/web/src/pages` 目录下快速生成符合项目架构规范的新页面。
- 核心理念：**架构先行**。先生成符合规范的代码骨架（脚手架），再由开发者或 AI 填充业务逻辑。

## 工作原理

1. 分析页面需求，确定UI复杂度和状态管理需求
2. **严格参照** [best-practice-examples/](best-practice-examples/) 中的代码结构和模式
3. 根据UI复杂度生成相应的Content组件
4. 如果需要Store，判断是生成新Store还是使用现有Store；如果生成新Store，使用store-best-practice技能生成Store模块
5. 创建Wrapper组件处理依赖注入
6. 实现Index文件提供干净的导出接口
7. 在应用程序中注册路由并使用生成的页面
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

## 使用方法

此技能提供文档和示例。按照参考指南中的步骤操作：

- [页面最佳实践指南](references/page-best-practice-guide.md) - 页面设计和实现的详细规则
- [最佳实践示例](best-practice-examples/) - **必须严格参照的** 页面结构和代码示例
  - [standard-with-store/](best-practice-examples/standard-with-store/) - 带Store的标准复杂度页面示例
  - [simple-no-store/](best-practice-examples/simple-no-store/) - 无Store的简单复杂度页面示例

**重要：** 实现时必须严格遵循 best-practice-examples 中的代码结构、命名约定和模式。任何修改都可能破坏架构一致性和可维护性。

## 使用示例 (Usage Examples)

### 典型使用场景

**用户输入**：创建一个用户管理页面，需要显示用户列表、支持搜索和筛选。

**Skill 响应**：
1. **主动询问生成模式**：显示模式选择界面，要求用户选择无监督或有监督生成
2. 根据用户选择，自动分析需求，判断需要 Store 和标准复杂度
3. 生成完整的页面结构和代码
4. 提供路由注册指导

具体配置示例请参考 [TEMPLATE_VIEW.md](references/TEMPLATE_VIEW.md) 中的配置示例部分。

## 输出

技能将生成：
- Index 文件（index.ts，提供干净的导出接口）
- Wrapper 组件（[PageName].tsx，处理依赖注入）
- Content 组件（[PageName]Content.tsx，实现UI和交互）
- 可选的 Store 模块（_store/，如果需要状态管理）

### 生成结果示例
请参考 [ANATOMY.md](references/ANATOMY.md) 的目录结构树部分。

## 核心规范 (Knowledge Base)

### 输入参数规范
- `pageName`: 页面名称，必须为 PascalCase 格式
- `features.hasStore`: 是否需要状态管理（系统自动判断）
- `features.useExistingStore`: 如果需要store，是否使用现有store（true/false，系统自动判断）
- `features.existingStorePath`: 如果使用现有store，指定store的导入路径（例如 "@/pages/UserPage/_store"）
- `features.uiComplexity`: UI 复杂度等级（simple/standard/complex，系统自动判断）
- `description`: 页面功能描述，用于智能判断复杂度

本 Skill 的执行完全依赖以下规范文档，请在生成代码时仔细参考：
1.  **整体结构**: [references/ANATOMY.md](references/ANATOMY.md) (目录结构、命名规范)
2.  **页面最佳实践指南**: [references/page-best-practice-guide.md](references/page-best-practice-guide.md) (页面设计和实现的详细规则)
3.  **最佳实践示例**: [best-practice-examples/](best-practice-examples/) (必须严格参照的页面结构和代码示例)
4.  **输入规范**: [references/schema.ts](references/schema.ts) (参数校验)
5.  **Store判断逻辑**: [references/judgeHasStore.ts](references/judgeHasStore.ts) (智能判断是否需要Store)
6.  **UI复杂度判断**: [references/judgeUIComplexity.ts](references/judgeUIComplexity.ts) (智能判断UI复杂度等级)
7.  **Index模版**: [references/TEMPLATE_INDEX.md](references/TEMPLATE_INDEX.md) (入口文件写法)
8.  **Wrapper模版**: [references/TEMPLATE_WRAPPER.md](references/TEMPLATE_WRAPPER.md) (依赖注入层写法)
9.  **View模版**: [references/TEMPLATE_VIEW.md](references/TEMPLATE_VIEW.md) (UI层写法)

*💡 Store 相关规范请参考 `store-best-practice` 技能*

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

**注意：** 调用完毕技能后，强制查看 [检查清单](references/checklist.md)，并确保返回的内容完全匹配清单中的所有项目。

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
- **自动生成页面名称**：根据用户描述和指令，自动生成 PascalCase 格式的页面名称（例如，用户说"创建用户管理页面"则生成"UserManagementPage"）

### 1.1. Store 判断逻辑
- **无监督模式**：直接调用 `judgeHasStoreFromDescription()` 自动判断是否需要store，如果需要，进一步调用 `judgeUseExistingStoreFromDescription()` 判断是否使用现有store，如果使用现有store，调用 `inferExistingStorePath()` 推导路径
- **有监督模式**：调用 `judgeHasStoreSupervised()` 获取推荐，询问用户确认是否采纳；如果需要store，进一步调用 `judgeUseExistingStoreSupervised()` 询问是否使用现有store，如果使用，询问用户指定路径或使用推导路径
- **重要**：如果判断需要新Store，请使用 `store-best-practice` 技能生成相应的 Store 模块；如果使用现有store，则无需生成

### 1.2. UI 复杂度判断
- **无监督模式**：直接调用 `judgeUIComplexity()` 自动判断
- **有监督模式**：调用 `judgeUIComplexitySupervised()` 获取推荐，询问用户确认

### 2. 规划文件列表
根据 `ANATOMY.md` 和 `hasStore`、`useExistingStore` 参数，规划需要创建的文件路径。
- 基础文件：`index.ts`, `[PageName].tsx`, `[PageName]Content.tsx`
- 可选文件：`_store/index.ts`, `_store/provider.tsx`, `_store/[camelCase]Slice.ts`, `_store/[camelCase]Store.ts` (仅当 `hasStore=true` 且 `useExistingStore=false`，通过 `store-best-practice` 技能生成)

### 3. 代码生成 (按顺序)

请复用 References 中的模版，将 `{{PageName}}` 和 `{{camelCasePageName}}` 替换为实际值。

**步骤 3.1: Store 模块处理**
- 如果 `hasStore=true` 且 `useExistingStore=false`，使用 `store-best-practice` 技能生成相应的 Store 模块
- 如果 `hasStore=true` 且 `useExistingStore=true`，使用指定的 `existingStorePath` 导入现有 Store
- Store 文件将放置在 `_store/` 目录下（仅当生成新Store时）

**步骤 3.2: 生成 UI 视图 (Content)**
- 参考 [TEMPLATE_VIEW.md](references/TEMPLATE_VIEW.md)。
- 根据 `uiComplexity` 参数选择合适的UI复杂度：
  - **simple**: 基础布局，无搜索/排序功能，仅基础展示
  - **standard**: 添加搜索和排序功能，适合数据管理页面
  - **complex**: 添加标签页、高级过滤、批量操作等，适合功能丰富的页面
- 如果 `hasStore=true`，替换 `{{StoreImport}}` 为相应的import语句：
  - 如果 `useExistingStore=false`：`import { useStore } from "zustand"; import { use{{PageName}}Store } from "./_store";`
  - 如果 `useExistingStore=true`：`import { useStore } from "zustand"; import { use{{PageName}}Store, {{PageName}}StoreProvider } from "{{existingStorePath}}";`
- 如果 `hasStore=true`，替换 `{{StoreConnection}}` 为 `const { loading, searchQuery, selectedSort, viewMode } = use{{PageName}}Store();`，否则替换为空
- 使用 `cn` 和 Flex 布局生成基础骨架。
- **重要**: 避免过度设计，只生成实际需要的功能

**步骤 3.3: 生成 包装器 (Wrapper)**
- 参考 [TEMPLATE_WRAPPER.md](references/TEMPLATE_WRAPPER.md)。
- **关键**: 如果需要 Store，Wrapper 必须正确引入并嵌套 `<StoreProvider>`：
  - 如果 `useExistingStore=false`：引入 `{{PageName}}StoreProvider` from "./_store"
  - 如果 `useExistingStore=true`：引入 `{{PageName}}StoreProvider` from "{{existingStorePath}}"
- 如果不需要 Store，则不要引入。
- **布局处理**: 优先使用路由层面的统一布局，仅在页面需要独特布局时在 Wrapper 中包含布局组件。

**步骤 3.4: 生成 入口 (Index)**
- 参考 [TEMPLATE_INDEX.md](references/TEMPLATE_INDEX.md)。
- 只导出包装器组件，不导出Content组件

**步骤 3.5: 质量验证**
- 验证生成的代码是否符合项目规范
- 检查类型安全和代码质量
- 确认依赖注入正确

### 4. 输出确认
- 告知用户页面已生成至指定路径。
- 提醒用户需在路由文件（如 `routeTree` 或 `router.tsx`）中注册该页面。
- 提供生成的组件使用示例。
- 建议运行测试验证生成代码。
