---
name: srt-to-structured-data
description: |
  将 SRT 字幕文件转换为结构化 JSON 数据。
  触发场景：
  (1) 需要解析 SRT 字幕文件
  (2) 需要将字幕转为 JSON/结构化格式
  (3) 需要提取字幕时间码和文本
  (4) 视频字幕数据处理和分析
  (5) 生成字幕纯文本或统计信息
metadata:
  author: nanmi
  version: "1.0.0"
---

# SRT 字幕转结构化数据

将 SRT 字幕文件解析为结构化 JSON 格式，支持提取时间码、计算时长、生成统计信息。

## 快速开始

### 基础用法

```bash
# 解析 SRT 文件，输出到终端
python <skill_path>/scripts/parse_srt.py input.srt

# 输出到文件
python <skill_path>/scripts/parse_srt.py input.srt -o output.json

# 包含统计信息
python <skill_path>/scripts/parse_srt.py input.srt --stats

# 仅输出纯文本（去除时间码）
python <skill_path>/scripts/parse_srt.py input.srt --text-only
```

**注意：** `<skill_path>` 是此 skill 的安装路径，通常为 `~/.claude/plugins/srt-to-structured-data@claude-code-skills/skills/srt-to-structured-data`

## 输出格式

### JSON 结构化数据

```json
{
  "subtitles": [
    {
      "index": 1,
      "start_time": "00:00:00,000",
      "end_time": "00:00:02,566",
      "start_ms": 0,
      "end_ms": 2566,
      "duration_ms": 2566,
      "text": "Clawdbot真的太火太火太火了"
    },
    {
      "index": 2,
      "start_time": "00:00:02,633",
      "end_time": "00:00:04,766",
      "start_ms": 2633,
      "end_ms": 4766,
      "duration_ms": 2133,
      "text": "Github一天直接涨了5万星"
    }
  ],
  "statistics": {
    "total_count": 2,
    "total_duration_ms": 4699,
    "total_duration_formatted": "00:04",
    "avg_duration_ms": 2349
  }
}
```

### 纯文本输出

使用 `--text-only` 参数时，仅输出字幕文本，每条一行：

```
Clawdbot真的太火太火太火了
Github一天直接涨了5万星
```

## 命令行参数

| 参数 | 说明 |
|------|------|
| `input.srt` | 输入的 SRT 字幕文件路径 |
| `-o, --output` | 输出文件路径（默认输出到终端） |
| `--stats` | 在 JSON 输出中包含统计信息 |
| `--text-only` | 仅输出纯文本，去除时间码和序号 |

## 字段说明

| 字段 | 类型 | 说明 |
|------|------|------|
| `index` | int | 字幕序号 |
| `start_time` | string | 开始时间（原始格式） |
| `end_time` | string | 结束时间（原始格式） |
| `start_ms` | int | 开始时间（毫秒） |
| `end_ms` | int | 结束时间（毫秒） |
| `duration_ms` | int | 持续时长（毫秒） |
| `text` | string | 字幕文本内容 |

## 使用示例

### 场景 1：分析字幕文件

```bash
python <skill_path>/scripts/parse_srt.py video.srt --stats -o analysis.json
```

### 场景 2：提取纯文本用于翻译

```bash
python <skill_path>/scripts/parse_srt.py video.srt --text-only -o transcript.txt
```

### 场景 3：在 Python 中直接使用

```python
import subprocess
import json

result = subprocess.run(
    ['python', '<skill_path>/scripts/parse_srt.py',
     'input.srt', '--stats'],
    capture_output=True, text=True
)
data = json.loads(result.stdout)
```
