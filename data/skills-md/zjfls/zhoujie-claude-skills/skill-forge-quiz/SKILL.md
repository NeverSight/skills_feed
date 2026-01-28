---
name: skill-forge-quiz
description: Skill Forge 试卷生成工具。支持 AI 生成和 JSON 导入。
---

# Skill Forge Quiz - 内容生成

此 Skill 提供为 Skill Forge 系统 **生成试卷内容** 的工具。它直接写入共享数据库，但不管理运行环境。

## 核心能力

1.  **导入试卷**：从 JSON 文件导入试卷。
2.  **生成试卷**：（规划中）AI 驱动的试卷生成。

## 使用说明

### 1. 导入试卷
从 JSON 文件导入试卷：

```bash
# 标准导入
node scripts/import_quiz.js <JSON文件路径>

# 示例
node scripts/import_quiz.js ./quiz_template.json
```

### JSON 模板格式
参考项目中的 `quiz_template.json` 文件：

```json
{
    "topic": "主题名称",
    "topic_detail": "详细描述（可选）",
    "difficulty": "beginner|intermediate|advanced",
    "questions": [
        {
            "content": "题目内容",
            "type": "choice|essay|code",
            "options": ["A. 选项1", "B. 选项2"],
            "correct_answer": "正确答案",
            "explanation": "解析",
            "knowledge_points": ["知识点1"],
            "score": 10
        }
    ]
}
```

## 交互流程规范

### 1. 试卷生成流程
当用户请求"生成试卷"或"创建测验"时，Agent 必须遵循以下流程：

1.  **参数确认**：主动询问并确认以下 4 个关键参数：
    *   **主题 (Topic)**: 测验的核心知识点或技术栈（例如：React Hooks, HTTP 协议）。
    *   **难度 (Difficulty)**: `beginner` (初级), `intermediate` (中级), 或 `advanced` (高级)。
    *   **题目数量 (Question Count)**: 建议 5-20 题。
    *   **题目来源 (Source)**: 明确内容的来源:
        *   **纯 AI 生成**: (`ai_generated`) 完全由模型根据知识库生成。
        *   **用户提供**: (`manual`) 基于用户提供的文档或文本。
        *   **网络搜索**: Agent 使用 `search_web` 工具搜索相关资料，可细分为：
            *   *官方文档* (`official_doc`): 技术官网、规范文档。
            *   *社区讨论* (`community`): StackOverflow, GitHub, 技术博客。
            *   *面试真题* (`interview`): LeetCode, 牛客网, 面经网站。
            *   *考试题库* (`exam`): 认证考试、学术试题。
            *   *考试题库* (`exam`): 认证考试、学术试题。
        *   **注意**: 
            *   生成 JSON 时请将对应的类型填入 `source_type` 字段。
            *   如使用 **Brave Search**，请务必在两次搜索之间间隔 **1秒** 以上，以避免 429 Too Many Requests 错误。
    *   **题型占比 (Distribution)**: 询问用户希望的题型分布（例如："全是单选" 或 "一半单选，一半代码题"）。支持的题型包括：
        *   `choice`: 单项选择题
        *   `multiple_choice`: 多项选择题
        *   `essay`: 问答/简答题
        *   `code`: 编程题（支持代码高亮）

2.  **内容生成**：
    *   Agent 根据确认的参数，使用自身的 LLM 能力生成符合 `quiz_template.json` 格式的 JSON 数据。
    *   **注意**：在 JSON 的 `questions` 数组中，应为每个问题设置 `source_type`（如 `ai_generated` 或 `official_doc`）。

3.  **写入与导入**：
    *   将生成的 JSON 保存为临时文件（例如 `temp_quiz_<timestamp>.json`）。
    *   使用 `node scripts/import_quiz.js <temp_file>` 导入数据库。
    *   导入成功后，**必须**删除临时文件。

4.  **反馈**：
    *   告知用户导入成功。
    *   提供 Dashboard 的访问链接（通常是 `http://localhost:3457`）以便用户开始测验。

### 2. 试卷导入流程
当用户提供现成的 JSON 文件进行导入时：

1.  **格式验证**：检查文件是否符合 `quiz_template.json` 的结构（必须包含 `topic` 和 `questions` 数组）。
2.  **执行导入**：直接运行 `node scripts/import_quiz.js <filepath>`。

## 常用命令

- **导入试卷**: `node scripts/import_quiz.js <path_to_json>`
- **查看帮助**: `node scripts/import_quiz.js --help`

## 依赖
- **Node.js**: >= 14.0.0
- **SQLite3**: 数据库访问
- **前置条件**: 需要 `~/.skill-forge/skill-forge.db` 已由 `skill-forge-base` 初始化。
