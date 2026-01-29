---
name: uniapp
description: 用于编辑 .vue 文件、创建 uni-app 组件、编写 composables - 提供 Composition API 模式、props/emits 最佳实践、VueUse 集成以及响应式解构指导
license: MIT
---

# uni-app 开发指南

uni-app Composition API 模式、组件架构实践的参考指南。

**当前稳定版本：** uni-app 基于 Vue 3.4.21，不要使用 Vue 3.5+ 的新特性。

## 概述

uni-app 项目的渐进式参考系统。仅加载与当前任务相关的文件，以最小化上下文使用（基础约 250 tokens，每个子文件 500-1500）。

## 使用场景

**使用此技能当：**

- 编写 `.vue` 组件
- 创建 composables（`use*` 函数）
- 构建客户端工具
- 简洁易懂，复杂的代码配上中文注释

## 快速参考

| 正在处理...              | 加载文件                   |
| ------------------------ | -------------------------- |
| `components/` 中的 `.vue` | references/components.md   |
| `composables/` 中的文件  | references/composables.md  |
| `utils/` 中的文件        | references/utils-client.md |
| `.spec.ts` 或 `.test.ts` | references/testing.md      |

## 加载文件

**根据文件上下文一次加载一个文件：**

- 组件工作 → [references/components.md](references/components.md)
- Composable 工作 → [references/composables.md](references/composables.md)
- Utils 工作 → [references/utils-client.md](references/utils-client.md)
- 测试 → [references/testing.md](references/testing.md)

**不要一次加载所有文件** - 会浪费上下文在不相关的模式上。

## 可用指导

**[references/components.md](references/components.md)** - 响应式解构的 Props、emits 模式、defineModel 用于 v-model、slots 简写

**[references/composables.md](references/composables.md)** - Composition API 结构、VueUse 集成、生命周期钩子、异步模式

**[references/utils-client.md](references/utils-client.md)** - 纯函数、格式化器、验证器、转换器、何时不使用 utils

## 示例

`resources/examples/` 中的工作示例：

- `component-example.vue` - 包含所有模式的完整组件
- `composable-example.ts` - 可复用的组合函数
