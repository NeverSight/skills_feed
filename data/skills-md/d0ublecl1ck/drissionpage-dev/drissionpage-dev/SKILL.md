---
name: drissionpage-dev
description: Professional DrissionPage (Python) automation development workflow and troubleshooting using the bundled DrissionPage docs (v4.1.1.2); use when writing/debugging/refactoring DrissionPage scripts for ChromiumPage/WebPage/SessionPage, element locating and interaction, waits, downloads/uploads, network listening, and configuration.
---

# DrissionPage Dev

## Overview

Use this skill to build reliable DrissionPage automation in Python by following a consistent workflow and consulting the bundled official docs in `references/docs/`.

## Preferences

- Do not use DrissionPage native wait APIs for long “query waiting” flows; instead poll static HTML (`tab.html` / snapshot) and parse with `parsel.Selector` (or an equivalent HTML parser) to detect state transitions.
- Do not rely on DrissionPage native “ready” checks when they are unreliable; instead implement readiness checks by parsing the static DOM for stable page markers (e.g., main content mounted, captcha/overlay shown or gone).

## Workflow

### 1) Clarify the goal and choose a mode

- Prefer `SessionPage` when the target data is available via HTTP responses and JS rendering is not required.
- Prefer `ChromiumPage` when you must run a real Chromium browser (JS rendering, complex login, anti-bot flows, file dialogs, etc.).
- Prefer `WebPage` when you need both browser control and packet sending/receiving (mode switching) in the same object.

Docs:
- `references/docs/🌏 导入 - DrissionPage官网.md` (core classes and import paths)
- `references/docs/⭐ 模式切换 - DrissionPage官网.md` and `references/docs/🗺️ 模式切换 - DrissionPage官网.md` (mode switching)

### 2) Create objects and configure startup

- Use `ChromiumOptions` for browser startup parameters; remember: options only apply when launching the browser, not when attaching to an existing one.
- Use `SessionOptions` to configure `SessionPage` / `WebPage` s-mode.
- Use `Settings` for global behavior (e.g., whether to raise when an element is not found).

Docs:
- `references/docs/🌏 导入 - DrissionPage官网.md`
- `references/docs/🛩️ 创建页面对象 - DrissionPage官网.md`
- `references/docs/🛩️ 启动配置 - DrissionPage官网.md`
- `references/docs/⚙️ 全局设置 - DrissionPage官网.md`

### 3) Locate elements with the official syntax

- Use the locating syntax docs as the source of truth; avoid guessing selector formats.
- When refactoring, keep locators centralized and prefer explicit waits over sleeps.

Docs:
- `references/docs/🔦 概述 - DrissionPage官网.md`
- `references/docs/🔦 定位语法 - DrissionPage官网.md`
- `references/docs/🔦 语法速查表 - DrissionPage官网.md`
- `references/docs/🔦 相对定位 - DrissionPage官网.md`
- `references/docs/🔦 在结果列表中筛选 - DrissionPage官网.md`

### 4) Interact, wait, and handle frames/tabs

- Use the dedicated wait APIs for stability; treat timeouts as first-class.
- Handle `iframe` explicitly.
- Use tab management APIs when working with new windows/tabs.

Docs:
- `references/docs/🛰️ 元素交互 - DrissionPage官网.md`
- `references/docs/🛰️ 等待 - DrissionPage官网.md`
- `references/docs/🛰️ iframe 操作 - DrissionPage官网.md`
- `references/docs/🛰️ 标签页管理 - DrissionPage官网.md`

### 5) Downloads, uploads, and network debugging

- For downloads, use the documented `download` / browser download flows.
- For uploads, use the upload docs and prefer stable file selection approaches.
- For debugging flaky flows, use screenshots/recording, console logs, and network listening.

Docs:
- `references/docs/⭐ 下载文件 - DrissionPage官网.md`
- `references/docs/⤵️ download方法 - DrissionPage官网.md`
- `references/docs/⤵️ 浏览器下载 - DrissionPage官网.md`
- `references/docs/🛰️ 上传文件 - DrissionPage官网.md`
- `references/docs/🛰️ 截图和录像 - DrissionPage官网.md`
- `references/docs/🛰️ 获取控制台信息 - DrissionPage官网.md`
- `references/docs/🛰️ 监听网络数据 - DrissionPage官网.md`

### 6) Exceptions and troubleshooting

- Catch and handle DrissionPage exceptions intentionally; do not blanket-catch everything.
- Use the FAQ when behavior differs from expectations.

Docs:
- `references/docs/⚙️ 异常的使用 - DrissionPage官网.md`
- `references/docs/❓ 常见问题 - DrissionPage官网.md`

## Quick search recipes (for Codex)

- Search the bundled docs by keyword:
  - `rg -n -S "<keyword>" references/docs`
  - For case-insensitive English terms: `rg -n -i "<keyword>" references/docs`

- When the API name is known, search by identifier:
  - `rg -n -S "\\bChromiumPage\\b" references/docs`
  - `rg -n -S "\\bSessionPage\\b" references/docs`

## Minimal starter snippet

Use the docs as the source of truth for parameters and return values.

```python
from DrissionPage import ChromiumPage, WebPage, SessionPage
from DrissionPage import ChromiumOptions, SessionOptions
from DrissionPage.common import Settings
```
