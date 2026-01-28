---
name: dedsi-vue3-project
description: Vue 3 project architecture overview with specific tech stack and development guidelines
---

# Dedsi Vue3 项目技能

本文档概述了项目的架构、技术栈和开发指南。

## 1. 技术栈

- **框架**: Vue 3 (Composition API)
- **构建工具**: Vite (使用 `rolldown-vite`)
- **语言**: TypeScript
- **状态管理**: Pinia
- **路由**: Vue Router
- **样式**: UnoCSS
- **HTTP 客户端**: Axios
- **可视化**: AntV G2
- **图标**: @ant-design/icons-vue
- **工具库**: Day.js, QRCode

## 2. 项目结构

源代码位于 `src` 目录下，组织结构如下：

| 目录 | 描述 |
| :--- | :--- |
| `src/apiServices` | API 集成和服务层（Axios 封装）。 |
| `src/components` | 可复用的 UI 组件。 |
| `src/configs` | 项目级配置。 |
| `src/layouts` | 页面布局（例如：BasicLayout 基本布局）。|
| `src/router` | 路由配置。`index.ts` 为入口，子模块位于 `modules` 目录。 |
| `src/stores` | 用于全局状态管理的 Pinia stores。 |
| `src/utils` | 辅助函数和工具类。 |
| `src/views` | 对应路由的页面组件。 |
| `src/App.vue` | Vue 根组件。 |
| `src/main.ts` | 应用程序入口点。 |

## 3. 配置亮点

### UnoCSS (`uno.config.ts`)

项目使用 UnoCSS 进行原子化样式开发，包含以下预设：
- `presetUno`: 默认 UnoCSS 工具集。
- `presetAttributify`: 支持属性化模式。
- `presetIcons`: 纯 CSS 图标。
- `presetTypography`: 排版预设。
- `presetWebFonts`: 网络字体（例如：'Inter'）。

**自定义快捷方式 (Shortcuts):**
- `flex-center`: `flex items-center justify-center` (弹性布局居中)
- `flex-between`: `flex items-center justify-between` (两端对齐)
- `glass-card-base`: `bg-white/70 backdrop-blur-md border border-white/30 rounded-16 shadow-lg` (毛玻璃卡片基类)

**主题:**
- 主色调 (Primary Color): `#1677ff`

### 脚本 (`package.json`)

- `dev`: 启动开发服务器 (`vite`).
- `build`: 类型检查并构建生产版本 (`vue-tsc -b && vite build`).
- `preview`: 本地预览生产构建 (`vite preview`).

## 4. 开发指南

### 核心原则
- **组件优先**: 研发时**优先使用 `src/components` 下的现有组件**，避免重复开发。
- **样式优先**: CSS 布局**必须优先使用 UnoCSS**，仅在必要时编写自定义 CSS。

### 状态管理
使用 **Pinia** 进行全局状态管理。Store 文件位于 `src/stores`。

### API 调用
所有 API 逻辑应封装在 `src/apiServices` 中。避免在组件通过 Axios 直接调用接口。

### 样式
使用 **UnoCSS** 工具类。对于复杂或重复的样式，请使用已定义的快捷方式或在 `uno.config.ts` 中创建新的快捷方式。
示例：
```html
<div class="flex-center glass-card-base">
  内容
</div>
```

### 脚本设置
所有 Vue 组件都应使用 `<script setup lang="ts">`，以利用组合式 API 和 TypeScript 支持。

### 路由管理
路由采用模块化管理，定义在 `src/router/modules` 目录下。
- **模块化**: 每个业务功能模块（如 Dashboard, AI Chat, User）应有独立的路由配置文件。
- **配置**: 在 `src/router/index.ts` 中导入并聚合这些模块。
- **结构**: 保持 `index.ts` 简洁，仅包含核心路由配置和守卫逻辑。
