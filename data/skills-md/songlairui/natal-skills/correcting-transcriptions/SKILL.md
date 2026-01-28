---
name: correcting-transcriptions
description: Use when user requests to clean up, correct, or improve speech-to-text transcripts that contain filler words, repetitions, self-corrections, or conversational artifacts from voice notes, recordings, or transcribed audio.
---

# Correcting Transcriptions (洗髓)

## 剑意 (Purpose)
将杂乱无章的语音转录文本清理为易读的书面笔记，洗去冗余口语，保留核心意图。**核心原则：去除冗余，保留精华；清理口语，但不过度正式化。**

## 触发条件 (When to Use)
- 用户明确要求"清理"、"矫正"、"优化"转录文本
- 文本包含明显的语音转录特征：大量语气词、重复表达、自我纠正、破碎的句子结构或说话框架。

## 剑招 (Instructions)

### 1. 斩断乱麻 (Standard Processing)
1. **清理元评论**: 坚决删除 "记录一下"、"我先说一下"、"你再补充" 等说话框架。这些是元评论，非实际内容。
2. **剔除语气词**: 扫描并删除 "嗯"、"啊"、"那个"、"就是"、"然后" 等。
3. **处理纠正**: 识别并只保留纠正后的内容（如："不对，是2019年" -> "2019年"）。

### 2. 存神守一 (Preservation)
- **保留口语风**: 保持自然，不要过度正式（如：保留 "我觉得"，不改为 "本人认为"）。
- **守住专业术语**: 准确识别并规范化 To B/C、API、SDK 等术语。
- **不失毫厘**: 确保数字、日期、人名、公司名等关键信息绝对准确。

## 输出格式 (Output)
- 默认仅输出矫正后的净文本。
- 仅在用户明确要求对比或标注时，才提供 Before/After 或修改说明。