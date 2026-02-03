---
name: winjs-huipro
description: WinJS HuiPro 模板（企业级 Web）开发指南。包含自定义 Router、Vuex、TabsManagement、权限控制、主子系统。适用于：(1) create-win huipro 模板创建的项目 (2) 修改 config/ 配置 (3) 维护 src/router 自定义路由 (4) 使用 TabsManagement 页签管理 (5) 配置权限/菜单 (6) 主子系统开发与构建 (7) Vue 2 + HUI 企业级后台项目。
---

# WinJS HuiPro 模板开发指南

面向企业级后台应用（Vue 2.6 + Vue Router 3.x + Vuex + HUI），支持自定义 Router、TabsManagement 页签管理、主子系统与权限控制。

---

## 模板概览

- **技术栈**：Vue 2.6 + Vue Router 3.x + Vuex，hash 路由
- **构建**：WinJS + Webpack，Less，`@winner-fed/preset-vue2`、`@winner-fed/plugin-build-huipro`
- **UI**：HUI（h_ui）企业级组件库
- **路由**：自定义 Router 实例（`src/router/`），通过 `app.js` 传入
- **状态**：Vuex（`src/stores`），通过 `modifyClientRenderOpts` 传入
- **特色**：主子系统、TabsManagement 页签、国际化、权限/菜单、config 目录配置
- **代码质量**：Biome、StyleLint、F2ELint + Husky

---

## 核心配置（config/）

⚠️ 配置在 `config/config.ts`（非根目录 `.winrc`）

关键配置项：

- **routes**: 设为 `[]`，路由由 `src/router/routes.js` 定义
- **plugins**: 含 `@winner-fed/plugin-hui`、`@winner-fed/plugin-build-huipro`、`@winner-fed/plugin-hui-micro-app` 等
- **appConfig**: 多环境配置，从 `config/appConfig.ts` 引入，注入 `window.LOCAL_CONFIG`
- **proxy**: 从 `config/proxy.ts` 引入
- **hui/huipro/microApp**: HuiPro 与微前端配置（`routePrefix`、`prefix` 等）
- **lessLoader**: 全局变量（`ROOT_CLASS`）、`modifyVars` 注入样式

完整配置见 [详细用法参考](./references/usage-reference.md) 或 [官方文档](https://winjs-dev.github.io/winjs-docs/config/config)。

---

## 应用入口（src/app.js）

关键导出：

- **modifyClientRenderOpts(memo)**: ⚠️ 必须返回新对象 `{ ...memo, router, store }`，传入自定义 router 和 store
- **onRouterCreated({ router })**: 注册守卫（`router.beforeEach`），避免模块顶层调用
- **onMounted({ app, router })**: 初始化 TabsManagement（`initTabsManagement(router)`）
- **request**: 若使用 request 插件，配置方式同 App 模板

⚠️ **Vue 2 注意**: 先 `Vue.use(Router)`，再 `new Router(...)`；动态路由用 `router.addRoutes([...])`，不是 `addRoute()`。

详见 [详细用法参考](./references/usage-reference.md)。

---

## 目录结构（src）

- **router/index.js**: 创建并导出 router（先 `Vue.use(Router)`，再 `new Router({ mode: 'hash', routes })`）
- **router/routes.js**: 导出 routes 数组（Vue Router 3 格式）
- **router/router.interceptor.js**: 路由守卫，通过 `onRouterCreated` 调用注册
- **stores/**: Vuex store，在 app.js 中传入
- **layouts/index.vue**: 全局布局
- **pages/**: 页面组件，对应 routes 配置
- **components/TabsManagement**: 页签管理组件
- **services/**: 请求封装、`autoMatchBaseUrl`、权限（`menuAuth`、`customerRouter`）等
- **index.pro.js**: ⚠️ **子系统入口**，导出 router、store、utils、directives、components、i18n、bootstrap

**临时路由**: 使用 `router.addRoutes()`，meta 中配置 `enableTempRoute`。

详见 [HuiPro 模板速查](./references/app-reference.md)。

---

## 常用命令

| 命令 | 说明          |
|------|-------------|
| `win dev` | 开发服务器       |
| `win build` | 生产构建        |
| `win preview` | 预览构建        |
| `win see` | 构建SEE包      |
| `win huipro` / `npm run child` | 子系统构建       |
| `npm run lint` / `lint:fix` | Biome 检查/修复 |
| `win cache` | 清缓存         |

---

## 快速排错

常见问题：

- **路由不工作**: 确认 `src/router/index.js` 先 `Vue.use(Router)` 再 `new Router()`
- **守卫不触发**: 在 `onRouterCreated` 中注册，非 `router.interceptor.js` 顶层
- **clientRoutes 只有 globalLayout**: 确认 `modifyClientRenderOpts` 返回了 `{ ...memo, router: customRouter }`
- **动态路由报错**: Vue 2 用 `router.addRoutes([...])`，非 `addRoute()`
- **useAppData/getRoute 报错**: 仅在组件生命周期中调用

详见 [常见问题与排错](./references/troubleshooting.md)。

---

## 参考文档

**本技能随模板下发，可独立使用：**

- [HuiPro 模板速查](./references/app-reference.md) — config、app.js、router、TabsManagement 速查
- [详细用法参考](./references/usage-reference.md) — 配置、钩子、路由、Vue 2/3 差异等
- [常见问题与排错](./references/troubleshooting.md) — AppContext、clientRoutes、守卫等排错
- [官方文档索引](./references/docs-index.md) — 快速定位官方文档主题

**在线资源：**

- [WinJS 官方文档](https://winjs-dev.github.io/winjs-docs/)
- 项目 README.md — 自定义 Router、TabsManagement、权限与部署说明
