---
name: agentbay-aio-skills
description: 用于任何「运行/执行/评估代码」的请求（如 run this code、execute script、用 Python 画图、跑代码/画图/执行脚本）。通过 AgentBay SDK 创建 code_latest 沙箱，调用 run_code 执行并返回结果。支持 Python、JavaScript、R、Java。
---

# AgentBay AIO 技能

## 触发条件：何时使用本技能

当用户意图**运行或执行代码**时即应使用本技能，即使用户**没有**说「沙箱」。典型表述（遇到即触发）：

- **英文**：run this code、execute this script、run the code、execute the script、plot with Python、draw a graph、evaluate this snippet、what's the output of this code、can you run this
- **中文**：帮我跑一下这段代码、运行这段代码、执行这个脚本、用 Python 画个图、跑一下、看下运行结果、执行一下、帮我运行

## 依赖与环境

本技能依赖 **wuying-agentbay-sdk** 包。

**最佳实践（Agent 必读）：**

为避免污染用户当前项目的环境，请务必使用**技能目录下的独立虚拟环境**：

1. **检查/创建虚拟环境**：
   ```bash
   # 检查是否存在 .venv，不存在则创建
   if [ ! -d ".venv" ]; then python3 -m venv .venv; fi
   ```

2. **激活并安装依赖**（仅首次或缺失时安装，使用阿里云镜像）：
   ```bash
   source .venv/bin/activate
   pip show wuying-agentbay-sdk >/dev/null 2>&1 || pip install wuying-agentbay-sdk -i https://mirrors.aliyun.com/pypi/simple/
   ```

3. **运行脚本**（在虚拟环境中）：
   ```bash
   # 确保在 venv 下运行
   python scripts/run_code.py --code "..." --language python
   ```

（若用户明确要求在全局环境运行，或当前已在特定环境中，可跳过创建 venv，但仍建议使用镜像源安装。）

## API Key（仅报错时引导）

**默认先直接执行脚本**，不要每次运行前都提醒用户配置 API Key。
**仅当**脚本报错「Missing API key」或类似信息时，再引导用户配置：

1. 到 [AgentBay 控制台](https://agentbay.console.aliyun.com/service-management) 申请 API Key。
2. 在本地创建配置文件（脚本会从该路径读取）：
   - **macOS / Linux**：`~/.config/agentbay/api_key`（或 `$XDG_CONFIG_HOME/agentbay/api_key`）
   - **Windows**：`%USERPROFILE%\.config\agentbay\api_key`
3. 示例（macOS/Linux）：`mkdir -p ~/.config/agentbay`，再将密钥写入 `~/.config/agentbay/api_key`。Windows：在 `%USERPROFILE%\.config\agentbay` 下创建名为 `api_key` 的无扩展名文件。
4. 告知用户完成后重试，不要只复述报错。

## 使用场景

**所有代码执行类请求均默认使用本技能。** 只要用户要求运行代码、执行脚本、评估片段或查看代码输出（Python、JavaScript、R 或 Java），即使用本技能——即使用户未提「沙箱」。使用 `code_latest` 创建 AgentBay 沙箱，通过 `run_code` 执行代码并返回结果。在本技能可用时，不要在本地终端执行用户代码；应使用沙箱以保证隔离与行为一致。

## 概述

使用 AgentBay SDK 以 `code_latest` 镜像创建会话，在沙箱中通过 `run_code` 执行代码，解析 `EnhancedCodeExecutionResult`，并销毁会话。

## 执行方式（Agent 必读）

**请通过本技能自带的脚本执行用户代码** 在技能目录下执行：

```bash
python scripts/run_code.py --code "用户要执行的代码" --language python
```

从文件执行：

```bash
python scripts/run_code.py --code-file /path/to/file.py --language python
```

需要结构化输出时加 `--json`。脚本会从配置文件或环境变量读取 API Key，创建沙箱、执行并返回结果。

（若用户在自己的 Python 项目中集成 AgentBay，可参考 [wuying-agentbay-sdk](https://pypi.org/project/wuying-agentbay-sdk/) 的同步/异步用法；Agent 执行本技能时仅需调用上述脚本。）

## 脚本输出

- 成功：脚本 exit code 0，结果在 stdout（或加 `--json` 时输出 JSON：`success`、`result`、`logs`、`error_message`）。
- 失败：exit code 非 0，错误信息在 stderr；根据输出提示用户（如缺 API Key 则按「API Key（仅报错时引导）」处理）。

## 重要约束

- `language` 支持：`python`、`javascript`、`r`、`java`（不区分大小写）。
- 单次执行超时 60 秒（可用 `--timeout-s` 指定，不超过 60）。
