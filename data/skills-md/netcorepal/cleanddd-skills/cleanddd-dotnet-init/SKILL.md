---
name: cleanddd-dotnet-init
description: 初始化 CleanDDD dotnet 项目（netcorepal-web 模板）；在创建新项目或为客户演示快速拉起解决方案时使用，可直接调用 dotnet new 或包装脚本
---

# cleanddd dotnet init

使用 `dotnet new netcorepal-web` 快速创建 CleanDDD dotnet 项目。脚本仅作为可选包装，代理/非交互场景可直接调用 dotnet。

## 使用时机
- 从零新建 CleanDDD 解决方案，或需要在新目录快速生成可运行样板。
- 已有旧模板需升级时，可在新目录重新生成后迁移代码。

## 前置输入

- `Framework` (default `net10.0`): 可选 `net8.0` / `net9.0` / `net10.0`
- `Database` (default `MySql`): 可选 `MySql` / `SqlServer` / `PostgreSQL` / `Sqlite` / `GaussDB` / `DMDB` / `MongoDB`
- `MessageQueue` (default `RabbitMQ`): 可选 `RabbitMQ` / `Kafka` / `AzureServiceBus` / `AmazonSQS` / `NATS` / `RedisStreams` / `Pulsar`
- `UseAspire` (default `true`): `true` / `false`
- `IncludeCopilotInstructions` (default `false`): `true` / `false`
- `ProjectName` (default 当前目录名，自动转 PascalCase，`-` 替换为 `.`)
- `OutputDir` (default 当前目录路径)

在执行命令前：展示参数汇总及可选项，获得用户确认后再继续。

## 运行方式（dotnet）

1) 安装模板（如未安装/需更新）

```bash
dotnet new install NetCorePal.Template
```

2) 创建项目（示例参数，可按需替换）

```bash
dotnet new netcorepal-web \
  --Framework net10.0 \
  --Database MySql \
  --MessageQueue RabbitMQ \
  --UseAspire true \
  --name My.Project \
  --IncludeCopilotInstructions false \
  --output /path/to/target
```

在执行 `dotnet new` 前，请先向用户展示上述参数的汇总同时给出可选参数并获得明确确认，确认后再执行命令。

## 可选脚本（交互）

如需参数校验/交互式收集，可用包装脚本：

```bash
python3 scripts/interactive_init.py [同上参数，可省略进入交互]
```

- 省略参数时进入交互模式，运行前会显示命令预览。
- 默认自动安装/更新 `NetCorePal.Template`，如已安装可加 `--skip-template-install`。
- 无论脚本或 agent 调用，都应在执行前展示参数汇总并请用户确认。

## 参数确认提示（示例）
- "准备执行 cleanddd 模板：Framework=net10.0, Database=MySql, MessageQueue=RabbitMQ, UseAspire=true, IncludeCopilotInstructions=false, ProjectName=My.Project, OutputDir=/path。是否继续？"
