---
name: nuxt-code-editor
description: 遵循项目标准生成和修改 Vue 3、TypeScript 和 SCSS 代码。
version: 1.0.0
author: GitHub Copilot
applyTo: "**/*.{ts,vue,scss}"
---

# Nuxt Code Editor Skill (Nuxt 代码编辑技能)

## 能力 (Capabilities)

-   **Vue 3 Composition API**: 生成 `<script setup lang="ts">` 组件。
-   **PrimeVue 集成**: 根据 `utils/` 或现有的 `components/` 用法正确使用 PrimeVue 组件。
-   **Better-Auth 集成**: 正确使用 `authClient` (前端) 和 `auth` (服务端) 进行身份验证和权限控制。
-   **类型安全**: 确保所有后端代码使用在 `server/database/entities` 或 `types/` 中定义的 TypeORM 实体和 DTO。
-   **Zod 校验**: 使用 Zod 进行 API 请求参数校验 (参考 `utils/schemas/`)。
-   **增量编辑**: 优先修补 (patch) 而非重写整个文件，以保留上下文。

## 指令 (Instructions)

1.  **路径与工作树意识**: 所有的文件创建与修改操作必须在当前任务所属的工作树中执行。如果是主功能开发，应在 `dev` 或 `fix` 分支对应的目录进行。
2.  **代码风格指南**: 遵守 ESLint 和 Prettier 配置。样式使用 SCSS，并适用 BEM 命名约定。
2.  **组件标准**: 使用 `defineProps`, `defineEmits` 并配合 TypeScript 接口/类型。
3.  **后端标准**:
    -   确保 `server/api` 处理程序使用 `defineEventHandler` 并返回标准化响应 (参考 `docs/standards/api.md`)。
    -   **禁止使用 PATCH 方法**，所有更新操作应使用 PUT 方法。
    -   列表类接口必须返回统一的分页格式：`items` (数据列表), `total` (总条数), `page`, `limit`, `totalPages`。
4.  **国际化 (I18n)**: 所有 UI 字符串必须包裹在 `$t()` 中。
    - **Key 命名规范**: 必须遵循 [开发规范](../../../docs/standards/development.md#25-代码生成准则-code-generation-guidelines) 要求的 **snake_case** (小写+下划线) 命名（现有 kebab-case 字段除外）。
5.  **文件**: 创建文件时，确保它们位于正确的 Nuxt 目录 (`components`, `composables`, `server/api` 等) 中。
6.  **依赖约束**: 遵循 `docs/standards/development.md` 中的依赖关系约束，避免循环依赖。

## 使用示例 (Usage Example)

输入: "创建一个按钮组件。"
动作: 使用 PrimeVue Button 生成 `components/base/AppButton.vue`，并在 TS 接口中定义 props。

输入: "创建一个获取文章列表的 API。"
动作: 在 `server/api/posts.get.ts` 中使用 `defineEventHandler` 和 `typeorm` 的 Repository 获取数据。
