---
name: vox
description: "Vox 单入口语音编排技能。用于自然语言完成 profile 管理、样本添加、ASR 转写、TTS（克隆 / CustomVoice / VoiceDesign）、pipeline 执行、模型管理与故障排查。缺依赖时再自动引导安装。用户只描述目标且未给具体命令时使用。"
---

# Vox

用一个入口覆盖 Vox CLI 全流程能力。默认优先执行业务操作，不把安装流程当作主流程。

先切到 skill 根目录（`SKILL.md` 所在目录）再运行下面脚本，避免相对路径错误。

## 总流程（业务优先）

1. 意图识别：
   - 先按 `references/intents.md` 映射到业务场景。
2. 执行业务命令：
   - 默认直接按对应 playbook 执行（见下方 references）。
   - 涉及重操作时，模型校验只走 `scripts/ensure_model.sh`（单路径）。
3. 缺依赖处理（按需）：
   - 仅当业务命令报依赖缺失/命令不存在时，先跑 `bash scripts/bootstrap.sh --check`。
   - 仍缺依赖再跑 `bash scripts/bootstrap.sh`，然后重试业务命令。
4. 交付前自检：
   - 强制执行 `health_gate`（优先用缓存状态，必要时才跑全量自检）。
   - `health_gate` 只做环境/输出门禁，不重复执行模型拉取或 verify。
5. 失败回写：
   - 记录失败样本到用户本地日志。

## 缺依赖时预检与安装

```bash
# 仅在业务命令出现依赖问题时执行
# 1) 无副作用预检
bash scripts/bootstrap.sh --check

# 2) 仍缺依赖时再执行安装
bash scripts/bootstrap.sh
```

## 模型确保（唯一模型校验路径）

```bash
bash scripts/ensure_model.sh <model_id|asr-auto|tts-default>
```

## 交付前自检

```bash
# 推荐：带状态缓存（默认 24h TTL）
bash scripts/health_gate.sh [--require-file <...>]

# 强制全量自检（忽略缓存）
bash scripts/health_gate.sh --force [--require-file <...>]
```

## 失败回写

```bash
bash scripts/log_failure.sh --stage "<stage>" --command "<cmd>" --error "<msg>" [--retry "<retry-cmd>"]
bash scripts/failure_digest.sh
```

状态文件：

- 健康状态：`~/.vox/agent/state/health.json`
- 失败日志：`~/.vox/agent/failures.jsonl`
- 失败报告：`~/.vox/agent/state/failure_report.md`
- 失败报告（JSON）：`~/.vox/agent/state/failure_report.json`

## 必读 References（按场景加载）

1. 意图路由：`references/intents.md`
2. 模型管理：`references/model-playbook.md`
3. Profile/采样：`references/profile-playbook.md`
4. ASR 转写：`references/asr-playbook.md`
5. TTS 合成（克隆/CustomVoice/VoiceDesign）：`references/tts-playbook.md`
6. Pipeline：`references/pipeline-playbook.md`
7. 输出模板：`references/response-contract.md`
8. 失败闭环：`references/failure-loop.md`
9. 交付硬标准：`references/checklist.md`（唯一标准来源）

## 交付硬标准

以 `references/checklist.md` 为唯一标准来源，不在本文件重复维护。

## 执行规则

1. 优先使用 JSON 输出（`--json` 或 `--format ndjson`）。
2. 执行前声明将要运行的命令；执行后回报关键结果。
3. 若命令失败，先给重试命令，再调用 `log_failure.sh`。
4. 只有预检失败或命令缺失时才进入安装流程。
5. 禁止跳过模型校验直接执行重操作（TTS clone/custom/design、pipeline、流式转写）。

## 常用命令模板

```bash
# 健康检查
scripts/vox_cmd.sh doctor --json

# 模型状态
scripts/vox_cmd.sh model status --json

# ASR 离线
scripts/vox_cmd.sh asr transcribe --audio ./speech.wav --lang zh --model auto --json

# TTS 克隆
scripts/vox_cmd.sh tts clone --profile narrator --text "你好" --out ./out.wav --model qwen-tts-1.7b --json

# TTS Custom Voice
scripts/vox_cmd.sh tts custom --text "你好" --speaker Vivian --out ./out.wav --model qwen-tts-1.7b-customvoice-8bit --json

# TTS Voice Design
scripts/vox_cmd.sh tts design --text "你好" --instruct "沉稳男声，播音腔" --out ./out.wav --model qwen-tts-1.7b-voicedesign-8bit --json

# Pipeline
scripts/vox_cmd.sh pipeline run --profile narrator --audio ./input.wav --clone-text "把这段内容读出来" --lang zh --json
```

## 依赖与发布约定

1. 安装优先使用 `uv`。
2. 默认安装系统依赖：`ffmpeg`、`portaudio`。
3. CLI 来源：
   - 优先 `VOX_CLI_PACKAGE_SPEC`（显式指定包）。
   - 若设置 `VOX_CLI_GIT_URL`，使用 `git+<url>` 安装。
   - 默认回退到 `git+https://github.com/catoncat/vox-cli.git`。
