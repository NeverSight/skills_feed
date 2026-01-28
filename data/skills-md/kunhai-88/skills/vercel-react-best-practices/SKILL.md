---
name: vercel-react-best-practices
description: "Vercel 出品的 React 与 Next.js 性能优化指南。在编写、评审或重构 React/Next.js 代码时使用，确保采用最优性能模式。触发场景：React 组件、Next.js 页面、数据获取、打包优化、性能改进等任务。"
license: MIT
---

# Vercel React 最佳实践

面向 React 和 Next.js 应用的性能优化指南，由 Vercel 维护。包含 8 大类共 57 条规则，按影响程度排序，用于指导自动化重构与代码生成。

## 何时使用

在以下场景参考本指南：
- 编写新的 React 组件或 Next.js 页面
- 实现数据获取（客户端或服务端）
- 评审性能问题
- 重构现有 React/Next.js 代码
- 优化打包体积或加载时间

## 规则类别与优先级

| 优先级 | 类别 | 影响 | 前缀 |
|--------|------|------|------|
| 1 | 消除瀑布请求 | 关键 | `async-` |
| 2 | 打包体积优化 | 关键 | `bundle-` |
| 3 | 服务端性能 | 高 | `server-` |
| 4 | 客户端数据获取 | 中高 | `client-` |
| 5 | 重渲染优化 | 中 | `rerender-` |
| 6 | 渲染性能 | 中 | `rendering-` |
| 7 | JavaScript 性能 | 低中 | `js-` |
| 8 | 高级模式 | 低 | `advanced-` |

## 速查

### 1. 消除瀑布请求（关键）
- `async-defer-await` - 将 await 移到实际使用的分支内
- `async-parallel` - 独立操作用 Promise.all()
- `async-dependencies` - 部分依赖用 better-all
- `async-api-routes` - API 路由中早创建 promise、晚 await
- `async-suspense-boundaries` - 用 Suspense 流式输出内容

### 2. 打包体积优化（关键）
- `bundle-barrel-imports` - 直接导入，避免 barrel 文件
- `bundle-dynamic-imports` - 重型组件用 next/dynamic
- `bundle-defer-third-party` - hydration 后再加载分析/日志
- `bundle-conditional` - 仅在该功能激活时加载模块
- `bundle-preload` - hover/focus 时预加载，提升感知速度

### 3. 服务端性能（高）
- `server-auth-actions` - Server Actions 像 API 路由一样做鉴权
- `server-cache-react` - 用 React.cache() 做请求级去重
- `server-cache-lru` - 跨请求缓存用 LRU
- `server-dedup-props` - 避免 RSC props 重复序列化
- `server-serialization` - 传给 Client 组件的数据尽量精简
- `server-parallel-fetching` - 调整组件结构以并行请求
- `server-after-nonblocking` - 非阻塞操作用 after()

### 4. 客户端数据获取（中高）
- `client-swr-dedup` - 用 SWR 自动请求去重
- `client-event-listeners` - 全局事件监听去重
- `client-passive-event-listeners` - 滚动用 passive 监听
- `client-localstorage-schema` - localStorage 数据版本化并精简

### 5. 重渲染优化（中）
- `rerender-defer-reads` - 不在仅用于回调的 state 上订阅
- `rerender-memo` - 昂贵逻辑抽到 memo 组件
- `rerender-memo-with-default-value` - 非原始类型默认 props 提升
- `rerender-dependencies` - effect 依赖用原始类型
- `rerender-derived-state` - 订阅派生布尔值而非原始值
- `rerender-derived-state-no-effect` - 在 render 中派生，不用 effect
- `rerender-functional-setstate` - 用函数式 setState 保持回调稳定
- `rerender-lazy-state-init` - 昂贵初始值用函数传 useState
- `rerender-simple-expression-in-memo` - 简单原始类型不必 memo
- `rerender-move-effect-to-event` - 交互逻辑放进事件处理
- `rerender-transitions` - 非紧急更新用 startTransition
- `rerender-use-ref-transient-values` - 瞬态频繁值用 ref

### 6. 渲染性能（中）
- `rendering-animate-svg-wrapper` - 动画作用在 div 包裹层，别动 SVG
- `rendering-content-visibility` - 长列表用 content-visibility
- `rendering-hoist-jsx` - 静态 JSX 提到组件外
- `rendering-svg-precision` - 降低 SVG 坐标精度
- `rendering-hydration-no-flicker` - 仅客户端数据用内联 script
- `rendering-hydration-suppress-warning` - 预期不一致时压制警告
- `rendering-activity` - 显隐用 Activity 组件
- `rendering-conditional-render` - 条件渲染用三元而非 &&
- `rendering-usetransition-loading` - 加载态优先 useTransition

### 7. JavaScript 性能（低中）
- `js-batch-dom-css` - 通过 class 或 cssText 批量改 CSS
- `js-index-maps` - 重复查找用 Map
- `js-cache-property-access` - 循环内缓存对象属性
- `js-cache-function-results` - 模块级 Map 缓存函数结果
- `js-cache-storage` - 缓存 localStorage/sessionStorage 读取
- `js-combine-iterations` - 合并多次 filter/map 为一次循环
- `js-length-check-first` - 昂贵比较前先查 length
- `js-early-exit` - 函数内尽早 return
- `js-hoist-regexp` - RegExp 提到循环外
- `js-min-max-loop` - min/max 用循环代替 sort
- `js-set-map-lookups` - O(1) 查找用 Set/Map
- `js-tosorted-immutable` - 不可变排序用 toSorted()

### 8. 高级模式（低）
- `advanced-event-handler-refs` - 事件处理存 ref
- `advanced-init-once` - 应用级只初始化一次
- `advanced-use-latest` - useLatest 稳定回调 ref

## 使用方式

阅读单条规则文件获取说明与示例：

```
rules/async-parallel.md
rules/bundle-barrel-imports.md
```

每条规则包含：为何重要、错误示例、正确示例、补充说明与参考。

完整展开版见 `rules/` 目录下各 .md 规则文件。
