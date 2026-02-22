---
name: vue-frontend-expert
description: 专注于 Vue 3 (Nuxt 4)、SCSS (BEM) 和 I18n 前端实现。
version: 1.0.0
author: GitHub Copilot
applyTo: "**/*.{vue,ts,scss}"
---

# Vue Frontend Expert Skill (Vue 前端专家技能)

## 能力 (Capabilities)

-   **Composition API**: 编写模式一致的 `<script setup lang="ts">`。
-   **SCSS BEM**: 遵循 BEM (Block Element Modifier) 命名规范编写高度解耦合的样式。
-   **I18n 驱动**: 强制使用 `$t()` 或 `useI18n()`。
-   **PrimeVue 应用**: 熟练使用项目的 UI 组件库。
-   **暗色模式适配**: 编写自适应暗色模式的样式。

## 指令 (Instructions)

1.  **样式规范**: 严禁使用内联样式和 `!important`。必须引用全局变量和 Mixins。
2.  **响应式设计**: 确保组件在移动端和桌面端表现正常。
3.  **SEO 优化**: 页面级组件必须包含 `useHead` 或 `definePageMeta`。
4.  **UI 文本**: 禁止硬编码中文/英文。

## 使用示例 (Usage Example)

输入: "创建一个文章卡片组件。"
动作: 编写 `article-card.vue`，使用 BEM 编写 SCSS，并为标题和按钮设置 i18n key。
