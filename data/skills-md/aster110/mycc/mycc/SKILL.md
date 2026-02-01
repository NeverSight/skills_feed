---
name: mycc
description: 启动 mycc 小程序后端服务（后台运行）。触发词："/mycc"、"启动 mycc"、"启动小程序后端"、"检查 mycc 状态"
---

# mycc

启动 mycc 小程序本地后端，连接网页版/小程序与本地 Claude Code。

## 环境要求

| 要求 | 说明 |
|------|------|
| Claude Code | **必须是官方原版**，fork 版本可能不兼容 |
| 网络 | **需要 VPN/代理**（cloudflared 需要访问外网） |
| 系统 | ✅ macOS、✅ Linux、❌ Windows、⚠️ WSL（不稳定） |

> ⚠️ **Windows/WSL 用户注意**：目前 Windows 原生和 WSL 环境都存在兼容性问题，建议使用 macOS 或 Linux。
>
> 💡 **关于第三方 Claude Code**：目前仅测试了官方原版，第三方 fork 版本的兼容性支持在规划中。

## 依赖

- **cloudflared**：`brew install cloudflare/cloudflare/cloudflared`（macOS）或参考 [官方文档](https://developers.cloudflare.com/cloudflare-one/connections/connect-networks/downloads/)

## 触发词

- "/mycc"
- "启动 mycc"
- "启动小程序后端"
- "检查 mycc 状态"

## 执行步骤

### 1. 安装依赖（首次）

```bash
cd .claude/skills/mycc/scripts && npm install && cd -
```

### 2. 启动后端

```bash
.claude/skills/mycc/scripts/node_modules/.bin/tsx .claude/skills/mycc/scripts/src/index.ts start
```

使用 `run_in_background: true` 让后端在后台持续运行。

> 代码会自动检测项目根目录（向上查找 `.claude/` 或 `claude.md`），无需手动指定 cwd。

### 3. 读取连接信息

等待几秒后读取：
```bash
sleep 5 && cat .claude/skills/mycc/current.json
```

### 4. 告知用户

- 连接码（routeToken）
- 配对码（pairCode）
- 访问 https://mycc.dev 输入配对

## 关键说明

- **后台运行**：后端会在后台持续运行，不阻塞当前会话
- **自动检测 cwd**：会向上查找项目根目录，确保 hooks 能正确加载
- **连接信息**：保存在 `.claude/skills/mycc/current.json`
- **停止服务**：`lsof -i :8080 -t | xargs kill`

## 遇到问题？

**让 AI 自己解决。** 代码都在 `scripts/src/` 目录下，AI 可以：
1. 读取错误日志
2. 检查代码逻辑
3. 修复问题并重试

常见问题：
- **端口被占用**：`lsof -i :8080 -t | xargs kill`
- **cloudflared 未安装**：按上面的依赖说明安装
- **tunnel 启动失败**：检查网络，重试即可

---

## 连接信息格式

启动后保存在 `.claude/skills/mycc/current.json`：
```json
{
  "routeToken": "XXXXXX",
  "pairCode": "XXXXXX",
  "tunnelUrl": "https://xxx.trycloudflare.com",
  "mpUrl": "https://api.mycc.dev/XXXXXX",
  "cwd": "/path/to/project",
  "startedAt": "2026-01-27T06:00:00.000Z"
}
```

## API 端点

| 端点 | 方法 | 说明 |
|------|------|------|
| `/{token}/health` | GET | 健康检查 |
| `/{token}/pair` | POST | 配对验证 |
| `/{token}/chat` | POST | 发送消息 |
| `/{token}/history/list` | GET | 历史记录列表 |
| `/{token}/history/{sessionId}` | GET | 对话详情 |
