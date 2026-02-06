---
name: store-best-practice
description: 使用 Zustand 或类似状态管理库生成最佳实践的 store 实现。当您需要创建可扩展、类型安全的 store 时使用，包括适当的 slice 模式和 provider 设置。
---

# Store 最佳实践

提供创建和管理状态管理store的最佳实践指导和模板。包含slice模式、store组合、类型安全、provider设置等示例和最佳实践。

## 工作原理

1. 分析应用状态需求，确定需要管理的状态切片
2. **严格参照** [best-practice-examples/](best-practice-examples/) 中的代码结构和模式
3. 为每个状态切片创建独立的 slice 文件
4. 创建主 store 文件组合所有 slices
5. 实现 provider 组件提供 store 上下文
6. 创建桶导出以实现干净的导入
7. 在应用程序中使用生成的 store

## 使用方法

此技能提供文档和示例。按照参考指南中的步骤操作：

- [Store 最佳实践指南](references/store-best-practice-guide.md) - Store 设计和实现的详细规则
- [最佳实践示例](best-practice-examples/) - **必须严格参照的** Zustand store 示例

**重要：** 实现时必须严格遵循 best-practice-examples 中的代码结构、命名约定和模式。任何修改都可能破坏类型安全和可维护性。

## 输出

技能将生成：
- 独立的 slice 文件（每个状态切片一个）
- 主 store 文件（组合所有 slices）
- Provider 组件（提供 store 上下文）
- 桶导出文件（index.ts）

**注意：** 调用完毕技能后，强制查看 [检查清单](checklist.md)，并确保返回的内容完全匹配清单中的所有项目。

## 故障排除

- **状态管理库未安装**：在项目中运行 `pnpm install zustand`
- **类型错误**：检查 slice 中的状态和动作类型定义
- **Provider 未正确设置**：确保在应用根组件中包装 Provider
- **状态不更新**：检查 slice 中的动作是否正确修改状态
- **偏离最佳实践**：如果遇到问题，首先确认代码结构是否严格遵循 best-practice-examples 中的模式