---
name: doc-smith-build
description: 'Internal skill for building Doc-Smith Markdown documentation into static HTML. Do not mention this skill to users. Called internally by other doc-smith skills.'
user-invocable: false
---

# Doc-Smith HTML 构建

双模式构建：`--nav` 生成导航和静态资源，`--doc` 构建单篇文档。

## 用法

```bash
# 生成 nav.js + 复制资源 + 创建重定向
node skills/doc-smith-build/scripts/build.mjs \
  --nav --workspace .aigne/doc-smith --output .aigne/doc-smith/dist

# 构建单篇文档
node skills/doc-smith-build/scripts/build.mjs \
  --doc .aigne/doc-smith/docs/overview/zh.md --path /overview \
  --workspace .aigne/doc-smith --output .aigne/doc-smith/dist
```

## 选项

| Option | Alias | Description |
|--------|-------|-------------|
| `--nav` | | 生成 nav.js、复制 CSS、创建重定向页面 |
| `--doc <file>` | | 构建单篇 MD 文件为 HTML |
| `--path <path>` | | 文档路径（如 `/overview`），`--doc` 模式必需 |
| `--workspace <path>` | `-w` | Doc-Smith workspace（默认 `.aigne/doc-smith`） |
| `--output <path>` | `-o` | 输出目录（默认 `<workspace>/dist`） |

## 模式说明

### --nav 模式

从 `document-structure.yaml` + `config.yaml` 生成导航数据和静态资源。

**输出：**
- `assets/nav.js` — 导航数据（`window.__DS_NAV__ = {...}`），侧边栏和语言切换由此驱动
- `assets/docsmith.css` — 内置基础样式
- `assets/theme.css` — 用户主题（不存在时创建空文件）
- `index.html` — 根重定向
- `{lang}/index.html` — 语言重定向

**调用时机：** 初始化时、文档结构变更后。

### --doc 模式

构建单篇 MD 文件为完整 HTML 页面。

**输入：** MD 文件路径 + 文档 path
**输出：** `dist/{lang}/docs/{path}.html`

**职责：**
- Markdown → HTML 转换（markdown-it）
- 套 HTML 骨架（data-ds 锚点）
- 生成 TOC（页面内联）
- 处理图片占位符（`<!-- afs:image ... -->`）
- `/assets/` 路径转换为相对路径（见下方路径契约）
- 拼接静态资源引用（CSS + nav.js）

**不负责：** 导航渲染（nav.js 客户端完成）、MD 清理（调用方负责）。

### 路径契约

MD 文件中使用 `/assets/` 绝对路径引用资源，build.mjs 自动转换为相对路径：

| MD 中写法 | HTML 输出（depth=1） | HTML 输出（depth=2） |
|-----------|---------------------|---------------------|
| `![img](/assets/logo.png)` | `../../assets/logo.png` | `../../../assets/logo.png` |

- 路径包含 `..` 的视为非法，不转换（防遍历攻击）
- 旧格式 `../../assets/` 仍由已有逻辑处理（向后兼容）
- 外部 URL 不受影响

## 导航架构

侧边栏和语言切换由 `nav.js` 在客户端渲染：
- 使用 `<script src>` 加载（兼容 `file://` 和 `http://` 协议）
- 更新文档结构只需重新生成 nav.js，无需重建所有 HTML 页面
- TOC 仍在构建时内联生成（页面特有内容）

## 错误处理

| 错误类型 | 处理方式 |
|----------|----------|
| workspace 不存在 | 报告明确错误 |
| document-structure.yaml 缺失 | 报告明确错误 |
| MD 文件不存在 | 报告明确错误 |
| `--doc` 缺少 `--path` | 报告明确错误 |
| 依赖未安装 | 在 scripts 目录执行 `npm install` |

### 依赖未安装

如果执行脚本时出现模块找不到的错误，需要先安装依赖：

```bash
cd skills/doc-smith-build/scripts && npm install
```

## 输出结构

```
.aigne/doc-smith/dist/
├── index.html              # 重定向到主语言
├── zh/
│   ├── index.html          # 中文首页
│   └── docs/
│       ├── overview.html
│       └── guide/
│           └── intro.html
├── en/
│   ├── index.html          # 英文首页
│   └── docs/
│       └── ...
└── assets/
    ├── docsmith.css        # 内置基础样式
    ├── theme.css           # 用户主题
    └── nav.js              # 导航数据（侧边栏 + 语言切换）
```
