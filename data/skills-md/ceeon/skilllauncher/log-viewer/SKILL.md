---
name: log-viewer
description: |
  查看和分析应用日志，帮助排查问题。当用户提到以下场景时触发：
  - 查日志、看日志、日志在哪
  - 查一下问题、排查错误、debug
  - 刚才执行了什么、历史记录
  - SkillLauncher 日志、应用日志
---

# Log Viewer

查看 SkillLauncher 日志，快速定位问题。

## 日志位置

```
~/Library/Logs/SkillLauncher/app.log
```

## 日志格式

```
[ISO8601时间戳] 消息
```

示例：
```
[2026-01-27T08:17:44Z] 发送: /todo-hub Anthropic mcpUI方案
```

## 日志类型

| 日志内容 | 含义 |
|----------|------|
| `========== SkillLauncher 启动 ==========` | 应用启动 |
| `加载了 N 个 skills` | 扫描到的 skills 数量 |
| `发送: /skill-name 参数` | 用户执行的命令 |

## 常用查询

```bash
# 最近 50 条
tail -50 ~/Library/Logs/SkillLauncher/app.log

# 搜索特定命令
grep "发送:" ~/Library/Logs/SkillLauncher/app.log | tail -20

# 搜索错误
grep -i "error\|fail\|❌" ~/Library/Logs/SkillLauncher/app.log

# 今天的日志
grep "$(date -u +%Y-%m-%d)" ~/Library/Logs/SkillLauncher/app.log

# 实时监控
tail -f ~/Library/Logs/SkillLauncher/app.log
```

## 排查指南

| 问题 | 检查方法 |
|------|----------|
| 命令没执行 | 看是否有 `发送:` 日志 |
| Skills 没显示 | 检查 `加载了 N 个 skills` 数量 |
| 流式不工作 | 确认 Claude CLI 支持 `--output-format stream-json` |
