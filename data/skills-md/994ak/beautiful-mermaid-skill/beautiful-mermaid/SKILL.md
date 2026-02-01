---
name: beautiful-mermaid
description: Skill for using the beautiful-mermaid TypeScript library to render Mermaid diagrams to SVG or ASCII/Unicode, apply themes (including Shiki), and integrate in Node or browser contexts.
---

# Beautiful Mermaid

## Overview
Enable fast, themeable Mermaid rendering in Node, browser, or CLI outputs using the `beautiful-mermaid` package. Use this skill to generate SVG diagrams, ASCII/Unicode diagrams, and consistent theming.

## When To Use
- Render Mermaid diagrams to SVG or ASCII/Unicode.
- Add or customize themes (two-color base, enrichment colors, or Shiki themes).
- Integrate `beautiful-mermaid` in Node, browser, or CLI tooling.
- Troubleshoot diagram rendering, spacing, or theme output.

## Scenario Map (Use-Case Examples)
- Terminal/CLI 输出图：Use `renderMermaidAscii()` with `useAscii: true` for pure ASCII.
- 终端更美观：Use `renderMermaidAscii()` default Unicode for box-drawing.
- Web 页面/React 组件：Use `renderMermaid()` to get SVG and inject into DOM.
- 需要主题一致：Use `THEMES['...']` to apply a built-in theme.
- 需要公司品牌色：Provide `bg` + `fg` (mono) or add `accent/muted/surface`.
- 需要跟 VS Code 主题一致：Use Shiki + `fromShikiTheme()`.
- CDN/无打包环境：Use the browser global bundle via `<script>` tag.
- 需要实时换肤：Update SVG CSS variables (`--bg`, `--fg`) without re-render.

## 场景举例（按人群）

### 程序员/工程师
- CLI/终端输出图：Use `renderMermaidAscii()` + ASCII 兼容
```ts
import { renderMermaidAscii } from 'beautiful-mermaid'
const ascii = renderMermaidAscii('graph LR; A-->B', { useAscii: true })
```
- Web/React 内嵌 SVG：Use `renderMermaid()` 生成 SVG 字符串
```ts
import { renderMermaid } from 'beautiful-mermaid'
const svg = await renderMermaid('graph TD; A-->B')
```
- CI/文档生成：批量渲染 SVG 文件
```ts
import { renderMermaid } from 'beautiful-mermaid'
const svg = await renderMermaid('sequenceDiagram\nA->>B: ping')
```
- 主题统一：Use 内置主题或自定义颜色
```ts
import { renderMermaid, THEMES } from 'beautiful-mermaid'
const svg = await renderMermaid('graph TD; A-->B', THEMES['tokyo-night'])
```

### 非技术用户
- 运营/产品文档：导出 SVG 嵌入文档
```ts
import { renderMermaid } from 'beautiful-mermaid'
const svg = await renderMermaid('graph TD; A-->B')
```
- 会议/汇报统一风格：用主题色保持一致
```ts
import { renderMermaid } from 'beautiful-mermaid'
const svg = await renderMermaid('graph TD; A-->B', { bg: '#0f0f0f', fg: '#e0e0e0' })
```
- 课程/演示：终端内展示 ASCII/Unicode
```ts
import { renderMermaidAscii } from 'beautiful-mermaid'
const unicode = renderMermaidAscii('graph LR; A-->B')
```
- 设计一致性：用 Shiki 主题映射编辑器风格
```ts
import { getSingletonHighlighter } from 'shiki'
import { renderMermaid, fromShikiTheme } from 'beautiful-mermaid'
const highlighter = await getSingletonHighlighter({ themes: ['vitesse-dark'] })
const colors = fromShikiTheme(highlighter.getTheme('vitesse-dark'))
const svg = await renderMermaid('graph TD; A-->B', colors)
```

## Quick Start
1. Install `beautiful-mermaid` in the target project.
2. Use `renderMermaid()` for SVG or `renderMermaidAscii()` for terminal output.
3. Apply a built-in theme or custom colors.

```ts
import { renderMermaid, renderMermaidAscii, THEMES } from 'beautiful-mermaid'

const svg = await renderMermaid('graph TD; A-->B', THEMES['tokyo-night'])
const ascii = renderMermaidAscii('graph LR; A-->B', { useAscii: true })
```

## Tasks

### Render SVG
- Import `renderMermaid` from the package.
- Pass Mermaid source text (auto-detects diagram type).
- Provide optional `RenderOptions` for colors, font, and transparency.

```ts
import { renderMermaid } from 'beautiful-mermaid'

const svg = await renderMermaid(`
  sequenceDiagram
    Alice->>Bob: Hello
`, {
  bg: '#1a1b26',
  fg: '#a9b1d6',
  accent: '#7aa2f7',
  transparent: false,
  font: 'Inter'
})
```

### Render ASCII/Unicode
- Import `renderMermaidAscii`.
- Use `useAscii: true` for pure ASCII compatibility.
- Adjust `paddingX`, `paddingY`, and `boxBorderPadding` to tune spacing.

```ts
import { renderMermaidAscii } from 'beautiful-mermaid'

const unicode = renderMermaidAscii('graph LR; A-->B')
const ascii = renderMermaidAscii('graph LR; A-->B', { useAscii: true })
```

### Theme With Two Colors
- Provide only `bg` and `fg` to use mono mode.
- Let the library derive all other colors with `color-mix()`.

```ts
const svg = await renderMermaid('graph TD; A-->B', {
  bg: '#0f0f0f',
  fg: '#e0e0e0'
})
```

### Theme With Enrichment Colors
- Add any of: `line`, `accent`, `muted`, `surface`, `border` to override derivations.
- Supply only the enrichments that matter.

```ts
const svg = await renderMermaid('graph TD; A-->B', {
  bg: '#1a1b26',
  fg: '#a9b1d6',
  accent: '#7aa2f7',
  line: '#3d59a1',
  muted: '#565f89',
  surface: '#292e42',
  border: '#3d59a1'
})
```

### Use Built-in Themes
- Import `THEMES` and pass one of the 15 preset themes.

```ts
import { renderMermaid, THEMES } from 'beautiful-mermaid'

const svg = await renderMermaid('graph TD; A-->B', THEMES['tokyo-night'])
```

### Use Shiki Themes
- Load a Shiki theme with `getSingletonHighlighter`.
- Convert it with `fromShikiTheme`.
- Pass converted colors to `renderMermaid`.

```ts
import { getSingletonHighlighter } from 'shiki'
import { renderMermaid, fromShikiTheme } from 'beautiful-mermaid'

const highlighter = await getSingletonHighlighter({
  themes: ['vitesse-dark']
})

const colors = fromShikiTheme(highlighter.getTheme('vitesse-dark'))
const svg = await renderMermaid('graph TD; A-->B', colors)
```

### Browser Script Tag Usage
- Use the CDN global bundle.
- Access exports on `beautifulMermaid`.

```html
<script src="https://unpkg.com/beautiful-mermaid/dist/beautiful-mermaid.browser.global.js"></script>
<script>
  const { renderMermaid, THEMES } = beautifulMermaid
  renderMermaid('graph TD; A-->B', THEMES['tokyo-night']).then(svg => {
    // use svg
  })
</script>
```

### Live Theme Switching
- Update SVG CSS custom properties (no re-render required).

```js
svg.style.setProperty('--bg', '#282a36')
svg.style.setProperty('--fg', '#f8f8f2')
```

### Troubleshooting
- If render fails, validate Mermaid syntax and diagram type.
- For terminal alignment, prefer Unicode or set `preserveDisplayWidth: true`.
- For browser usage, ensure the global bundle is loaded before use.

## Resources
- Reference API details and theme lists in `references/beautiful-mermaid-reference.md`.
- `references/api-render.md`: renderMermaid 参数表、误区与示例
- `references/api-ascii.md`: renderMermaidAscii 参数表、误区与示例
- `references/themes-and-shiki.md`: 主题模型、内置主题与 Shiki 集成
