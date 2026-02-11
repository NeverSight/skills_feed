---
name: vimax-video-prompts
description: ViMax 多Agent视频生成系统的 Prompt 参考库。包含从创意构思到视频生成全流程的 13 组专业 prompt（编剧、分镜、角色、画面生成等）。当需要参考专业视频生成 prompt 的写法、构建短片创作工作流、或设计多 Agent 协作的视频制作 pipeline 时使用。
metadata:
  tags: vimax, video, prompt, screenwriting, storyboard, character, multi-agent
---

# ViMax Video Prompts 参考库

## 系统概述

ViMax 是一个多 Agent 协作的 AI 视频生成系统，能够将一个简单的创意想法（basic idea）自动转化为完整的短片视频。系统包含 13 个专业 Agent，覆盖从创意构思到画面生成的全部环节。

### 核心架构

- **LLM 驱动**：所有 Agent 基于 LangChain + Pydantic 构建，使用 System/Human prompt 对模式
- **结构化输出**：每个 Agent 通过 `PydanticOutputParser` 输出结构化数据
- **双流水线**：
  - **短脚本流水线**（Idea → Script → Storyboard → Images）：适合原创短片
  - **小说改编流水线**（Novel → Compress → Events → Scenes → Storyboard → Images）：适合长文本改编

## 完整生产流程

```
┌─────────────────────────────────────────────────────────────────────┐
│                     短脚本流水线 (Short Script)                       │
│                                                                     │
│  Idea ──→ [01 ScriptPlanner] ──→ [03 ScriptEnhancer] ──→ Script    │
│             (叙事/动作/蒙太奇)        (剧本润色)                      │
│                                                                     │
│  或:                                                                 │
│  Idea ──→ [02 Screenwriter] ──→ Story ──→ Script (按场景分割)        │
│             (develop_story → write_script)                           │
└──────────────────────────────┬──────────────────────────────────────┘
                               │
                               ▼
┌─────────────────────────────────────────────────────────────────────┐
│                     小说改编流水线 (Novel Pipeline)                    │
│                                                                     │
│  Novel ──→ [08 NovelCompressor] ──→ Compressed Novel                │
│              (分块压缩 + 聚合)                                        │
│                    │                                                 │
│                    ▼                                                 │
│            [06 EventExtractor] ──→ Events (因果事件链)               │
│                    │                                                 │
│                    ▼                                                 │
│            [07 SceneExtractor] ──→ Scenes (含角色+环境+剧本)         │
└──────────────────────────────┬──────────────────────────────────────┘
                               │
                               ▼
┌─────────────────────────────────────────────────────────────────────┐
│                     角色与一致性管理                                   │
│                                                                     │
│  Script/Scenes ──→ [04 CharacterExtractor] ──→ 角色列表              │
│                          │                                           │
│                          ▼                                           │
│                    [09 GlobalInfoPlanner] ──→ 全局角色合并            │
│                      (跨场景合并 + 跨事件合并到小说级别)                │
│                          │                                           │
│                          ▼                                           │
│                    [05 CharacterPortraits] ──→ 角色肖像图             │
│                      (正面/侧面/背面 三视角)                          │
└──────────────────────────────┬──────────────────────────────────────┘
                               │
                               ▼
┌─────────────────────────────────────────────────────────────────────┐
│                     分镜与画面生成                                     │
│                                                                     │
│  Script + Characters ──→ [10 StoryboardArtist]                      │
│                             │                                        │
│                             ├──→ design_storyboard (分镜设计)        │
│                             └──→ decompose_visual_description        │
│                                   (FF/LF/Motion 三段分解)            │
│                                        │                             │
│                                        ▼                             │
│                    [11 CameraImageGenerator] ──→ 机位树构建           │
│                             │                                        │
│                             ▼                                        │
│                    [12 ReferenceImageSelector] ──→ 参考图筛选         │
│                      (文本预筛选 + 多模态精筛)                         │
│                             │                                        │
│                             ▼                                        │
│                    [13 BestImageSelector] ──→ 最佳图选择              │
│                      (角色一致性 + 空间一致性 + 描述准确性)            │
└─────────────────────────────────────────────────────────────────────┘
```

## 子文件索引

| # | 文件 | 对应 Agent | 说明 | Prompt 数量 |
|---|------|-----------|------|------------|
| 01 | [01-script-planner.md](prompts/01-script-planner.md) | `ScriptPlanner` | 将基本创意扩展为完整剧本（叙事/动作/蒙太奇 3 种模式 + 意图路由） | 5 |
| 02 | [02-screenwriter.md](prompts/02-screenwriter.md) | `Screenwriter` | 两阶段创作：想法→故事→剧本 | 4 |
| 03 | [03-script-enhancer.md](prompts/03-script-enhancer.md) | `ScriptEnhancer` | 剧本润色：增加感官细节、统一术语、优化对话 | 2 |
| 04 | [04-character-extractor.md](prompts/04-character-extractor.md) | `CharacterExtractor` | 从剧本中提取角色列表（含静态/动态特征） | 2 |
| 05 | [05-character-portraits.md](prompts/05-character-portraits.md) | `CharacterPortraitsGenerator` | 生成角色正面/侧面/背面肖像的图片生成提示词 | 3 |
| 06 | [06-event-extractor.md](prompts/06-event-extractor.md) | `EventExtractor` | 从小说中逐个提取事件（含因果链） | 2 |
| 07 | [07-scene-extractor.md](prompts/07-scene-extractor.md) | `SceneExtractor` | 将事件改编为电影剧本场景（含 RAG 上下文） | 2 |
| 08 | [08-novel-compressor.md](prompts/08-novel-compressor.md) | `NovelCompressor` | 小说分块压缩 + 段落聚合去重 | 4 |
| 09 | [09-global-info-planner.md](prompts/09-global-info-planner.md) | `GlobalInformationPlanner` | 跨场景/跨事件的角色一致性管理与合并 | 4 |
| 10 | [10-storyboard-artist.md](prompts/10-storyboard-artist.md) | `StoryboardArtist` | 分镜设计 + 视觉描述 FF/LF/Motion 三段分解 | 4 |
| 11 | [11-camera-image-generator.md](prompts/11-camera-image-generator.md) | `CameraImageGenerator` | 机位树构建（父子包含关系推理） | 2 |
| 12 | [12-reference-image-selector.md](prompts/12-reference-image-selector.md) | `ReferenceImageSelector` | 参考图智能选择（文本预筛选 + 多模态精筛） | 3 |
| 13 | [13-best-image-selector.md](prompts/13-best-image-selector.md) | `BestImageSelector` | 多维度最佳图片选择（角色/空间/描述一致性） | 2 |

**总计：39 个 prompt 模板**

## 与 Dreamina 现有 Skills 的对接点

| ViMax 环节 | 对应 Dreamina Skill | 说明 |
|-----------|-------------------|------|
| FF/LF 分解 (`10-storyboard-artist.md` decompose) | `dreamina-video-first-end-frame` | ViMax 的 first-frame / last-frame 分解逻辑可直接用于 Dreamina 的首尾帧视频生成 |
| 角色肖像生成 (`05-character-portraits.md`) | `dreamina-character-consistency` | 肖像提示词模板可配合 Dreamina 角色一致性功能 |
| 分镜设计 (`10-storyboard-artist.md` design) | `storyboard-creator` / `storyboard-generator` | ViMax 的分镜设计 prompt 可作为 storyboard skill 的参考 |
| 图片生成提示词 | `dreamina-gen-image` / `dreamina-prompt-writing` | 参考图选择和画面描述的 prompt 写法可提升图片生成质量 |
| 视频描述 | `dreamina-video-description` | ViMax 的 motion description 可配合视频描述生成 |
