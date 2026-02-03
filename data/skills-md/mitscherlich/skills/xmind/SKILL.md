---
name: xmind
description: 当用户要求"解析 xmind"、"打开思维导图"、"创建 xmind"、"新建思维导图"、"更新 xmind"、"修改思维导图"、"xmind 转 markdown"、"查看 xmind 内容"时，应使用此技能。此技能提供 XMind 思维导图文件的解析、创建和更新能力，支持 XMind 8 和 XMind Zen/2020+ 两种格式，并将内容转换为 Markdown 作为会话记忆，方便持续交流。
version: 0.2.0
---

# XMind 思维导图处理技能

此技能提供 XMind 文件（`.xmind`）的完整处理能力：解析、创建和更新。通过配套的 Python 工具脚本实现文件操作，将思维导图内容转换为 Markdown 格式作为会话级记忆，便于用户与模型持续交流和编辑。

## 工具脚本

本技能依赖 `scripts/xmind_tool.py`（相对于本技能目录），使用 Python 标准库（零第三方依赖）。执行方式：

```bash
python skills/xmind/scripts/xmind_tool.py --session <session-id> <command> [args...]
```

### 会话管理

所有命令都需要 `--session <id>` 参数，用于隔离不同会话的记忆文件。

**会话 ID 获取规则（按优先级）：**
1. 从上下文中获取：如果当前对话上下文中已存在之前使用过的 session ID，直接复用
2. 生成新 ID：如果上下文中没有可用的 session ID，在首次调用前生成一个 UUID v4 格式的字符串（例如 `f47ac10b-58cc-4372-a567-0e02b2c3d479`），并在后续调用中持续复用
- 记忆文件存储路径：`/tmp/skills-xmind-parsed/<session-id>/<filename>.md`

## 支持的格式

| 格式 | 版本 | 内部结构 | 检测方式 |
|------|------|---------|---------|
| Zen | XMind Zen / 2020+ | ZIP 内含 `content.json` | 自动检测 |
| Legacy | XMind 8 | ZIP 内含 `content.xml` | 自动检测 |

创建新文件时默认使用 Zen 格式；更新已有文件时保留原格式。

## Markdown 表示规范

解析后的 Markdown 使用缩进列表式结构，格式如下：

```markdown
# Sheet: 工作表标题

## 中心主题

> Labels: 标签1, 标签2
> Link: https://example.com
> Markers: priority-1
> 这里是中心主题的备注内容

- 分支1  {labels: 重要}  {link: https://example.com}
  > 这是分支1的备注
  > 备注可以有多行
  - 子节点1.1  {markers: task-done, priority-1}
    - 子子节点1.1.1
  - 子节点1.2
- 分支2
  - 子节点2.1
  - 子节点2.2
```

**格式说明：**
- `# Sheet: 标题` — 工作表标题（多工作表之间用 `---` 分隔）
- `## 标题` — 中心主题
- `- 内容` — 节点，使用 2 空格缩进表示层级
- `{labels: ...}` — 行内标签元数据
- `{link: ...}` — 行内超链接元数据
- `{markers: ...}` — 行内标记/图标元数据
- `> 内容` — 节点备注（blockquote 形式，紧跟在节点下方）
- 中心主题的元数据使用顶层 blockquote（`> Labels:`, `> Link:`, `> Markers:`）

## 核心流程

### 场景一：解析 XMind 文件

**触发词**："解析 xmind"、"打开思维导图"、"查看 xmind 内容"、"xmind 转 markdown"

**步骤：**

1. **确认文件路径**：确认用户提供的 `.xmind` 文件路径是否存在
2. **执行解析**：运行工具脚本

   ```bash
   python skills/xmind/scripts/xmind_tool.py --session <session-id> parse <file.xmind>
   ```

3. **展示结果**：将输出的 Markdown 内容展示给用户，包括：
   - 思维导图的整体结构概览
   - 各节点的层级关系
   - 附带的标签、备注、链接等元数据
4. **记录记忆路径**：输出末尾的 `<!-- memory_file: ... -->` 注释包含记忆文件路径，记住该路径以便后续操作使用
5. **引导交互**：提示用户可以继续对思维导图内容进行提问、修改或导出

### 场景二：创建 XMind 文件

**触发词**："创建 xmind"、"新建思维导图"、"生成 xmind"

**步骤：**

1. **收集需求**：与用户交流，明确思维导图的结构：
   - 中心主题是什么？
   - 有哪些主要分支？
   - 各分支下有哪些子节点？
   - 是否需要添加标签、备注、链接等？
2. **生成 Markdown**：根据用户描述，按照上述 Markdown 规范生成内容
3. **写入临时 Markdown 文件并执行创建**：

   ```bash
   # 将 markdown 内容写入临时文件，然后执行创建
   python skills/xmind/scripts/xmind_tool.py --session <session-id> create <output.xmind> <temp.md> [--format zen|legacy]
   ```

4. **确认创建结果**：向用户报告文件创建成功，展示文件路径
5. **保持记忆**：记忆文件已自动创建，后续可继续编辑

**格式选择：**
- 默认创建 Zen 格式（现代格式，兼容性更好）
- 如果用户明确要求 XMind 8 兼容格式，使用 `--format legacy` 参数

### 场景三：更新 XMind 文件

**触发词**："更新 xmind"、"修改思维导图"、"编辑 xmind"

**步骤：**

1. **加载当前内容**：
   - 首先尝试读取记忆文件（如果之前已解析过）：

     ```bash
     python skills/xmind/scripts/xmind_tool.py --session <session-id> memory <file.xmind>
     ```

   - 如果没有记忆文件，先执行解析：

     ```bash
     python skills/xmind/scripts/xmind_tool.py --session <session-id> parse <file.xmind>
     ```

2. **理解修改需求**：与用户确认要进行的修改，例如：
   - 添加新分支或子节点
   - 删除某个节点
   - 修改节点内容、标签或备注
   - 调整节点层级关系
3. **修改 Markdown**：在记忆文件的基础上进行修改，确保格式符合规范
4. **写入修改后的 Markdown**：将修改后的内容写入临时文件
5. **执行更新**：

   ```bash
   python skills/xmind/scripts/xmind_tool.py --session <session-id> update <file.xmind> <modified.md>
   ```

6. **确认结果**：向用户报告更新成功，展示变更摘要

### 场景四：基于记忆继续交流

当用户在同一会话中再次提到已解析的 xmind 文件时：

1. **读取记忆文件**：使用 `memory` 命令获取之前解析的内容
2. **基于内容回答**：根据 Markdown 内容回答用户问题
3. **支持操作**：
   - 总结思维导图要点
   - 搜索特定节点
   - 分析结构和层级关系
   - 提出改进建议
   - 将内容转换为其他格式（大纲、表格等）

## 注意事项

- 解析和创建操作涉及文件 I/O，执行前确认路径有效
- 更新操作会覆盖原文件，如用户未明确要求，建议先备份或另存为新文件
- 记忆文件存储在 `/tmp/skills-xmind-parsed/<session-id>/`，会话结束后可能被系统清理
- 如遇到损坏的 xmind 文件（非有效 ZIP 或缺少关键内容文件），向用户报告具体错误
- XMind 文件中的图片附件不会包含在 Markdown 中，仅处理文本结构和元数据
- 整个流程中使用中文与用户交互
