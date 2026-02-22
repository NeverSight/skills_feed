---
name: system-watchdog
description: 深度审计 OpenClaw 系统健康状态，分析 Gateway 重启原因、LLM Fallback 记录以及定时任务运行实况。使用中文汇报。
---

# System Watchdog

本技能专门用于从底层日志和 CLI 数据中提取真实的系统运行状态，确保汇报内容"有据可查"，杜绝幻觉。

## 🚨 安全红线 (Security Policy)

**严禁在报告中暴露以下敏感信息**：

| 敏感类型 | 示例 | 处理规则 |
|----------|------|----------|
| **API Key** | `sk-abc123...`, `Bearer token` | ❌ 完全禁止 |
| **Provider 账号标识** | `moonshot:default` | ❌ 禁止，只保留 provider 名称 |
| **密钥文件路径** | `~/.openclaw/secrets/...` | ❌ 完全禁止 |
| **模型名称** | `moonshot/kimi-k2.5` | ✅ 允许显示 |
| **Provider 名称** | `moonshot`, `google`, `anthropic` | ✅ 允许显示 |

## 核心职责

1. **日志穿透**：读取 `gateway.log` 和 `gateway.err.log` 获取重启、错误和模型切换记录。
2. **LLM 健康追踪**：捕获 provider 冷却、auth 失败、rate limit、failover 链路等详细信息。
3. **任务追踪**：准确汇报 Cron 任务的最近运行结果（成功/失败、耗时）。
4. **中文输出**：所有汇报内容必须使用中文，采用适合手机端阅读的排版风格。

## 工作流

1. **数据获取**：运行脚本 `health_fetcher.py` 获取过去 2 小时的 JSON 概览。
2. **状态判断**：
    - 如果有 Gateway 重启，分析是 `SIGUSR1`（配置重载）还是异常崩溃。
    - 如果有 LLM Fallback，分析失败代码（如 429, 500）。
3. **生成报告**：按照固定模板输出中文审计报告。

## 手机端排版规范

- **单级列表**：禁止嵌套。
- **Emoji 导航**：
    - 🛰️ Gateway 状态
    - 🧠 模型路由审计
    - 🕒 定时任务追踪
    - 🛡️ 自愈事件 (Watchdog)
    - ⚠️ 异常预警
- **精简文字**：每条目不超过 3 行。

## 报告模板

### 🧠 LLM 路由健康
- **受影响 Providers**：列出所有受影响的 provider
- **冷却事件**：按时间列出 provider 和状态
- **错误统计**：Auth 失败、Rate limit、Timeout 次数
- **Failover 链**：展示模型切换路径

### 🛡️ 自愈事件
- 如果有配置恢复 → 列出恢复时间和来源版本
- 如果有 Gateway 重启 → 列出重启时间、原因和结果
- 如果都无 → 显示 "过去2小时无自愈事件"

### 🕒 定时任务追踪
- 列出所有任务：名称、执行计划、启用状态
- 显示上次运行时间和状态
- 如果 `enabled: false` → 标注为「已禁用」
