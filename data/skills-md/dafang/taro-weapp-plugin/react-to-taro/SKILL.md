---
name: react-to-taro
description: Transpile React Web applications (v18+) into Taro 4.x code optimized for WeChat Mini Program. Use this skill when converting React components, pages, or utilities to Taro-compatible code with proper JSX element mapping, event handler transformation, navigation/routing conversion, and API shim layer.
license: MIT
compatibility: Taro 4.x, React 18+, WeChat Mini Program, weapp-tailwindcss
metadata:
  version: "1.0.0"
  target-platform: weapp
  source-framework: react
  output-framework: taro
allowed-tools: Read Edit Write Glob Grep Bash
---

# React to Taro WeChat Mini Program Compiler

You are an advanced autonomous agent skill designed to transpile React Web applications into **Taro 4.x** code optimized for WeChat Mini Program. You possess deep knowledge of Taro 4.x architecture, performance patterns, component APIs, and weapp-tailwindcss integration.

## Scripts (辅助脚本)

此 Skill 提供三个辅助脚本用于分析和验证转换工作:

### 1. analyze.js - 代码分析器
扫描 React 源代码，生成转换报告，标记需要处理的位置。

```bash
node scripts/analyze.js <file-or-directory>
# 输出: taro-migration-report.json
```

**检测内容:**
- JSX 元素 (div, span, img, input 等)
- 事件处理器 (onChange, onKeyDown 等)
- 路由代码 (react-router-dom)
- Web API (axios, localStorage, DOM)

### 2. generate-transforms.js - 转换指令生成器
读取分析报告，生成具体的转换指令供 Agent 执行。

```bash
node scripts/generate-transforms.js taro-migration-report.json
# 输出: taro-transforms.json
```

### 3. validate.js - 代码验证器
检查转换后的 Taro 代码是否符合规范。

```bash
node scripts/validate.js <file-or-directory>
# 验证通过返回 0，失败返回 1
```

**验证规则:**
- 无 Web 原生元素
- 无 react-router-dom
- 无 DOM API / localStorage
- 无 e.target.value (应为 e.detail.value)
- 无 undefined state

### 推荐工作流

```bash
# 1. 分析源代码
node scripts/analyze.js ./src

# 2. 生成转换指令
node scripts/generate-transforms.js taro-migration-report.json

# 3. Agent 根据指令执行转换 (手动)

# 4. 验证转换结果
node scripts/validate.js ./src-taro
```

---

## Input Context

You will receive React Web source code for transformation. Identify the file type:
- **component**: React functional/class component
- **page**: React page with routing
- **app_entry**: App entry point with routes
- **utility**: Helper functions/hooks

## Operational Protocol

Your output must be **production-ready code** only. Do not provide markdown explanations unless specifically asked for "analysis".

---

# RULESET A: IMPORT TRANSFORMATION

## Destroy List (Remove These)

```typescript
// React Router
import { Link, useNavigate, useLocation, useParams, Outlet, NavLink } from 'react-router-dom'

// Web Animation Libraries
import { motion, AnimatePresence } from 'framer-motion'

// Direct Axios
import axios from 'axios'

// Browser APIs
import { createPortal } from 'react-dom'
```

## Inject List (Add These)

```typescript
// Core Taro (Always)
import Taro, { useLoad, useDidShow, useReady } from '@tarojs/taro'

// Components (As Needed)
import {
  View, Text, Image, Button, Input, Textarea,
  ScrollView, Swiper, SwiperItem, RichText,
  CustomWrapper, Form, Navigator
} from '@tarojs/components'

// Types (TypeScript)
import type { CommonEvent, ITouchEvent } from '@tarojs/components'
```

---

# RULESET B: JSX ELEMENT MAPPING

## Container Elements → View

| React | Taro |
|-------|------|
| `<div>`, `<section>`, `<article>`, `<main>` | `<View>` |
| `<nav>`, `<aside>`, `<header>`, `<footer>` | `<View>` |
| `<ul>`, `<ol>`, `<li>` | `<View>` |

## Text Elements → Text

| React | Taro | Constraint |
|-------|------|------------|
| `<span>`, `<p>`, `<h1>`-`<h6>` | `<Text>` | Pure text only |
| `<label>`, `<strong>`, `<em>` | `<Text>` | No block elements inside |

**Critical**: Text cannot contain View. Split if needed:
```tsx
// INVALID
<Text><View>Block</View></Text>

// VALID
<View><Text>Text</Text><View>Block</View></View>
```

## Media Elements → Image

| React | Taro | Default |
|-------|------|---------|
| `<img src alt>` | `<Image src mode>` | `mode="widthFix"` |

**Mode Selection**:
- Width-constrained: `mode="widthFix"`
- Fixed height/square: `mode="aspectFill"`

**In loops**: Add `lazyLoad` prop

## Form Elements

### Input
```tsx
// BEFORE
<input type="text" value={v} onChange={e => set(e.target.value)} />

// AFTER
<Input type="text" value={v} onInput={e => set(e.detail.value)} />
```

### Password
```tsx
// BEFORE
<input type="password" />

// AFTER
<Input type="text" password />
```

### Keyboard Submit
```tsx
// BEFORE
onKeyDown={e => e.key === 'Enter' && submit()}

// AFTER
onConfirm={() => submit()}
```

---

# RULESET C: EVENT TRANSFORMATION

## Event Mapping

| React | Taro | Detail |
|-------|------|--------|
| `onClick` | `onClick` | `ITouchEvent` |
| `onChange` (input) | `onInput` | `e.detail.value` |
| `onKeyDown` (Enter) | `onConfirm` | `e.detail.value` |
| `onFocus` | `onFocus` | `e.detail` |
| `onBlur` | `onBlur` | `e.detail` |
| `onScroll` | `onScroll` | `scrollTop, scrollLeft` |

## Critical Pattern

```tsx
// React: e.target.value
onChange={e => setValue(e.target.value)}

// Taro: e.detail.value
onInput={e => setValue(e.detail.value)}
```

## Event Propagation

```tsx
// Use e.stopPropagation() - NOT catchTap
onClick={e => { e.stopPropagation(); action() }}
```

## Custom Events Must Start with `on`

```tsx
// INVALID
<Component handleClick={fn} callback={fn} />

// VALID
<Component onClick={fn} onCallback={fn} />
```

---

# RULESET D: NAVIGATION & ROUTING

## Hook Replacement

```tsx
// BEFORE
const navigate = useNavigate()
const location = useLocation()
const { id } = useParams()

// AFTER
import Taro, { useLoad } from '@tarojs/taro'

useLoad((params) => {
  const { id } = params
})

// Or anywhere:
const params = Taro.getCurrentInstance().router?.params
```

## Navigation Actions

| React Router | Taro |
|--------------|------|
| `navigate('/path')` | `Taro.navigateTo({ url: '/pages/path/index' })` |
| `navigate('/path', { replace: true })` | `Taro.redirectTo({ url: '/pages/path/index' })` |
| `navigate(-1)` | `Taro.navigateBack()` |
| TabBar route | `Taro.switchTab({ url: '/pages/tab/index' })` |

## Path Convention

```
React: /products/:id
Taro:  /pages/products/index?id=xxx
```

## Link Transformation

```tsx
// BEFORE
<Link to="/about">About</Link>

// AFTER - Option 1
<Navigator url="/pages/about/index"><Text>About</Text></Navigator>

// AFTER - Option 2
<View onClick={() => Taro.navigateTo({ url: '/pages/about/index' })}>
  <Text>About</Text>
</View>
```

---

# RULESET E: API SHIM LAYER

## HTTP Requests

```tsx
// BEFORE (axios)
const { data } = await axios.get('/api/users', { params: { page: 1 } })

// AFTER (Taro)
const res = await Taro.request({
  url: 'https://api.example.com/api/users',
  method: 'GET',
  data: { page: 1 }
})
const data = res.data  // Note: res.statusCode, not res.status
```

## Storage

```tsx
// BEFORE
localStorage.setItem('key', JSON.stringify(data))
const data = JSON.parse(localStorage.getItem('key'))

// AFTER
Taro.setStorageSync('key', data)
const data = Taro.getStorageSync('key')
```

## Feedback

```tsx
// BEFORE
alert('Message')
confirm('Sure?')

// AFTER
Taro.showToast({ title: 'Message', icon: 'none' })
const { confirm } = await Taro.showModal({ title: 'Confirm', content: 'Sure?' })
```

## DOM Query

```tsx
// BEFORE
document.getElementById('el').getBoundingClientRect()

// AFTER
Taro.createSelectorQuery().select('#el').boundingClientRect().exec()
```

---

# RULESET F: STYLE & LAYOUT

## Tailwind CSS with weapp-tailwindcss

官方文档: https://tw.icebreaker.top/docs/quick-start/frameworks/taro

### 安装依赖

```bash
npm install weapp-tailwindcss tailwindcss autoprefixer postcss -D
```

### Webpack5 配置 (config/index.ts)

```typescript
const { UnifiedWebpackPluginV5 } = require('weapp-tailwindcss/webpack')

export default defineConfig<'webpack5'>(async (merge) => {
  const baseConfig = {
    compiler: {
      type: 'webpack5',
      prebundle: { enable: false }  // 建议关闭
    },
    mini: {
      webpackChain(chain, webpack) {
        chain.merge({
          plugin: {
            install: {
              plugin: UnifiedWebpackPluginV5,
              args: [{ rem2rpx: true }]
            }
          }
        })
      }
    }
  }
})
```

### Vite 配置 (替代方案)

```typescript
import type { Plugin } from 'vite'
import tailwindcss from 'tailwindcss'
import { UnifiedViteWeappTailwindcssPlugin as uvtw } from 'weapp-tailwindcss/vite'

const baseConfig: UserConfigExport<'vite'> = {
  compiler: {
    type: 'vite',
    vitePlugins: [
      {
        name: 'postcss-config-loader-plugin',
        config(config) {
          if (typeof config.css?.postcss === 'object') {
            config.css?.postcss.plugins?.unshift(tailwindcss())
          }
        },
      },
      uvtw({
        rem2rpx: true,
        disabled: process.env.TARO_ENV === 'h5' || process.env.TARO_ENV === 'harmony',
        injectAdditionalCssVarScope: true,
      })
    ] as Plugin[]
  }
}
```

### 注意事项

- 关闭微信开发者工具的"代码自动热重载"功能，否则样式可能不生效
- 与 NutUI 或 @tarojs/plugin-html 一起使用时需查看官方注意事项
- 建议关闭 prebundle 功能 (`prebundle: { enable: false }`)

### 使用方式

保持 `className` 字符串不变，weapp-tailwindcss 会自动转换:
```tsx
<View className="flex items-center p-4 bg-white">
```

## Viewport Fixes

```tsx
// 100vh doesn't work correctly
// BEFORE
<div className="h-screen">

// AFTER
<View className="min-h-screen">
```

## Safe Area (iPhone X+)

```tsx
// Fixed bottom elements need safe area padding
<View style={{ paddingBottom: 'env(safe-area-inset-bottom)' }}>
```

---

# RULESET G: PERFORMANCE OPTIMIZATION

## CustomWrapper for Lists

```tsx
// Wrap list items to isolate updates
{items.map(item => (
  <CustomWrapper key={item.id}>
    <ItemCard item={item} />
  </CustomWrapper>
))}
```

## Image Lazy Loading

```tsx
// In ScrollView or loops
<Image src={url} lazyLoad mode="widthFix" />
```

## ScrollView for Scrollable Lists

```tsx
// BEFORE
<div className="overflow-y-auto h-96">

// AFTER
<ScrollView scrollY className="h-96" onScrollToLower={loadMore}>
```

## App Config

```typescript
// Enable lazy loading for large apps
export default defineAppConfig({
  lazyCodeLoading: 'requiredComponents'
})
```

---

# RULESET H: PLATFORM CONSTRAINTS

## JSX Limitations

```tsx
// INVALID: Only .map() allowed
{items.filter(x => x.active).map(...)}

// VALID: Pre-process
const activeItems = items.filter(x => x.active)
{activeItems.map(...)}
```

## Props Restrictions

- Function props MUST start with `on`
- Don't use `undefined` in state (use `null`)
- Don't use `id`, `class`, `style` as custom prop names
- Set `defaultProps` for all optional props

## Code Style

```tsx
// USE single quotes
const name = 'John'
<View className='container'>

// DON'T destructure process.env
if (process.env.NODE_ENV === 'development') {}
```

## Null Safety

```tsx
// Components may render before data loads
// ALWAYS use optional chaining
<Text>{data?.name || 'Loading...'}</Text>
```

---

# QUICK REFERENCE

## Import Template
```tsx
import Taro, { useLoad, useDidShow } from '@tarojs/taro'
import { View, Text, Image, Button, Input, ScrollView } from '@tarojs/components'
import type { CommonEvent, ITouchEvent } from '@tarojs/components'
```

## Event Template
```tsx
onInput={(e) => setValue(e.detail.value)}
onClick={(e) => { e.stopPropagation(); action() }}
onConfirm={(e) => submit(e.detail.value)}
```

## Navigation Template
```tsx
Taro.navigateTo({ url: '/pages/target/index?id=' + id })
Taro.redirectTo({ url: '/pages/target/index' })
Taro.navigateBack()
Taro.switchTab({ url: '/pages/tab/index' })
```

## API Template
```tsx
const res = await Taro.request({ url, method: 'GET', data })
Taro.showToast({ title: 'Message', icon: 'none' })
Taro.setStorageSync('key', value)
```
