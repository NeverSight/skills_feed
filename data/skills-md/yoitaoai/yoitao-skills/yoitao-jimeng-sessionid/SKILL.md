---
name: yoitao-jimeng-sessionid
description: 当需要获取或刷新即梦（jimeng.jianying.com）登录态中的 sessionid cookie 时使用。自动打开即梦网站检查登录状态，并在已登录时返回 sessionid 值给调用方。
---

# Jimeng SessionId

获取并返回即梦站点的 `sessionid` Cookie（只返回值，不写文件）。

## 依赖项

本技能依赖 **Playwright MCP**，需要运行环境中已注册 Playwright MCP 服务，并可调用以下浏览器工具：

- `browser_navigate`
- `browser_snapshot`（或同类页面状态读取工具）
- `browser_run_code`
- `browser_close`

如果缺少以上能力，本技能无法完成登录检查与 Cookie 提取流程。

## Playwright MCP 安装示例

建议显式指定 `profile`（通过 `--user-data-dir`），这样即梦登录态可以持久化，不用每次重新登录。

以下为常见安装方式（按你的客户端选择其一）：

### Claude Code

```bash
claude mcp add playwright npx @playwright/mcp@latest -- --user-data-dir "$HOME/.yoitao/mcp/playwright-jimeng-profile"
```

### Codex

```bash
codex mcp add playwright npx @playwright/mcp@latest -- --user-data-dir "$HOME/.yoitao/mcp/playwright-jimeng-profile"
```

安装后建议重启客户端，再执行本技能。

## 触发场景

- 用户要求获取即梦 `sessionid`
- 其他技能（如图片生成 skill）需要即梦认证凭据
- 已有 `sessionid` 过期，需要重新抓取

## 工作流

### 1) 打开即梦页面

导航到：

```text
https://jimeng.jianying.com/ai-tool/home
```

### 2) 检查登录状态

- 若页面出现“登录”按钮：提示用户先完成登录，并保持浏览器窗口不关闭
- 若页面出现会员信息（如“基础会员”“高级会员”）：继续下一步

### 3) 读取 Cookie

执行脚本读取 Cookie：

```javascript
async (page) => {
  const cookies = await page.context().cookies();
  const sessionCookie = cookies.find(
    (c) =>
      c.name === "sessionid" &&
      (c.domain.includes("jimeng.jianying.com") || c.domain.includes("jianying.com")),
  );
  return sessionCookie ? sessionCookie.value : null;
}
```

注意：Cookie 名是小写 `sessionid`，不是 `sessionId`。

### 4) 返回结果并清理

- 获取成功：直接返回 `sessionid` 值
- 获取失败：返回“未找到 sessionid，建议刷新后重试”
- 最后关闭浏览器资源

## 关键参数

| 项目 | 值 |
| --- | --- |
| 目标站点 | `https://jimeng.jianying.com/ai-tool/home` |
| Cookie 名 | `sessionid`（小写） |
| 域名匹配 | `jimeng.jianying.com` / `jianying.com` |

## 注意事项

1. `sessionid` 会过期，需要按需刷新。
2. 登录完成后如仍取不到 Cookie，先刷新页面再重试。
