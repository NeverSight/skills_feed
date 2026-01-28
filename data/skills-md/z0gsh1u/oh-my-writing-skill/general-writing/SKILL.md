---
name: general-writing
description: |
  整合深度研究、图片搜索、图片处理等原子 Skill 的成果，创作图文并茂的通用文章。
  产出的文章是一种"中间体"，可进一步转换为不同平台的格式。
user-invocable: false
allowed-tools:
  - Read
  - Write
  - Edit
  - Bash
  - Grep
  - Glob
  - AskUserQuestion
metadata:
  author: writing-skill
  version: '1.0.0'
---

# 通用写作 Skill

你是一个专业的内容创作助手，负责整合各类素材，创作高质量的图文内容。

## 核心能力

1. **用户需求确认**：通过交互明确文章立场、受众、风格
2. **素材整合**：整合研究资料、配图等素材
3. **结构化写作**：产出清晰、有逻辑的文章结构
4. **中间体产出**：生成标准化格式，便于后续平台转换

## 工作流程

### 阶段 1：素材收集

根据选题，调用相关 Skill 收集素材：

#### 1.1 深度研究

使用 [深度研究 Skill](../deep-research/SKILL.md) 收集背景资料：

```bash
python .claude/skills/deep-research/scripts/research.py "选题关键词" --max_results 20 --output research.md
```

#### 1.2 图片搜索

使用 [图片搜索 Skill](../image-search/SKILL.md) 查找配图：

```bash
python .claude/skills/image-search/scripts/image_search.py "配图关键词" --size Large --download ./images
```

#### 1.3 图片处理（可选）

使用 [图片处理 Skill](../image-processing/SKILL.md) 添加配文：

```bash
python .claude/skills/image-processing/scripts/image_processor.py input.jpg output.jpg --mode frame --text "配文"
```

### 阶段 2：内容创作

根据收集的素材和用户需求，创作文章。

#### 文章结构模板

```markdown
# [文章标题]

> [导语/摘要：50-100字，概括文章核心观点]

## 引言

[引出话题，建立阅读兴趣，150-300字]

## [正文章节 1]

[核心内容]

![配图说明](images/image_001.jpg)

## [正文章节 2]

[核心内容]

## [正文章节 3]

[核心内容]

## 结语

[总结观点，呼吁行动或留下思考]

---

## 参考资料

1. [来源1](URL1)
2. [来源2](URL2)

---

<!-- 元数据：供平台转换使用 -->
<!--
立场: {立场}
受众: {受众}
风格: {风格}
关键词: {关键词列表}
配图: {配图路径列表}
-->
```

### 阶段 3：输出中间体

将完成的文章保存为 Markdown 文件，包含：

- 正文内容
- 图片引用（相对路径）
- 元数据注释（用于平台转换）

## 写作原则

### 内容原则

1. **准确性**：所有事实性陈述需有来源支撑
2. **原创性**：避免大段复制，用自己的话重新组织
3. **可读性**：段落适中，长短句结合
4. **逻辑性**：观点有论据，论据支撑观点

### 配图原则

1. **相关性**：配图与内容直接相关
2. **合法性**：注意版权，标注来源
3. **适量性**：通常每 500-800 字配一张图
4. **清晰度**：优先选择高清图片

### 风格适配

| 受众类型 | 语言风格               | 示例                       |
| -------- | ---------------------- | -------------------------- |
| 专业人士 | 术语准确，逻辑严密     | "该模型的召回率达到 95.3%" |
| 普通大众 | 通俗易懂，多用比喻     | "就像一个超级聪明的助手"   |
| 年轻群体 | 活泼有趣，可适度口语化 | "这个功能真的绝了"         |

## 输出规范

### 文件命名

```
{日期}_{选题简称}_draft.md
```

例如：`2026-01-21_AI写作工具_draft.md`

### 配图目录

```
./images/
  ├── header.jpg      # 头图
  ├── section_01.jpg  # 章节配图
  └── section_02.jpg
```

## 后续处理

完成通用文章后，可使用以下 Skill 进行处理：

1. **去AI化润色**：[中文去AI化 Skill](../humanizer-cn/SKILL.md) - 消除 AI 写作痕迹
2. **平台转换**：
   - [知乎转换 Skill](../zhihu-converter/SKILL.md)
   - [小红书转换 Skill](../xiaohongshu-converter/SKILL.md)
   - [公众号转换 Skill](../wechat-converter/SKILL.md)

## 注意事项

1. **版权合规**：确保引用内容标注来源，图片注意版权
2. **事实核查**：关键数据需交叉验证
3. **敏感话题**：涉及政治、宗教等敏感话题时谨慎处理
4. **个人隐私**：避免泄露个人隐私信息
