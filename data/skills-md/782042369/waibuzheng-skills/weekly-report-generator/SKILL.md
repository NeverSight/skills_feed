---
name: weekly-report-generator
description: "从Git提交记录生成专业工作周报。支持单周/多周批量生成、多项目汇总、自定义模板（Markdown/Word）。自动将技术术语转换为业务语言，补充下周计划/本周总结/问题和风险章节。使用场景：(1) 从Git日志生成本周工作汇报 (2) 将多个项目的提交记录汇总为一份周报 (3) 基于自定义Word模板生成领导要求的格式 (4) 批量生成一个月或多周的周报"
---

# 周报生成器

从Git提交记录自动生成专业工作周报，支持单周/多周批量生成。

## 核心原则

- **主子分离**：主智能体负责调度，子智能体负责实际生成
- **精简输出**：只输出提交消息数组，不包含冗余信息
- **只读Git日志**：禁止读取项目源代码文件
- **必须内容清洗**：技术术语转换为业务语言（AI执行，不可跳过）
- **任务管理**：使用 TodoWrite 工具创建任务清单，追踪每个周报的生成状态

## 快速开始

生成周报只需 **2 个步骤**：

```
Step 1: 运行编排脚本准备数据 → Step 2: 并行处理每个周报
```

### Step 1: 运行编排脚本（准备数据）

```bash
python scripts/orchestrate_reports.py \
  --paths "E:\项目1,E:\项目2" \
  --time "本月" \
  --output "E:\周报输出" \
  --template "E:\模板.docx" \
  --format docx \
  --naming "第一周周报,第二周周报,第三周周报,第四周周报"
```

**脚本自动完成**：
- 解析时间表达式（本周/本月/2025-1-1-2025-1-31）
- 验证项目路径和输出路径
- 分析模板文件（识别需要补充的章节）
- 为每个周生成独立任务配置文件
- 生成二次确认信息和 Claude Code 调用说明

**输出文件**（位于 `{输出路径}/tmp/`）：
- `time_result.json` - 时间解析结果
- `template_structure.json` - 模板结构（如果提供模板）
- `week_XX-task.json` - 每个周的任务配置
- `claude_instruction.md` - Claude Code 调用说明

### Step 2: 并行处理每个周报（AI 执行）

**创建任务清单**（必须）：
```python
# 使用 TodoWrite 工具创建任务清单
todos = [
  {"content": "读取调用说明和参考文档", "status": "pending", "activeForm": "读取调用说明和参考文档"},
  {"content": "为第1周启动子智能体", "status": "pending", "activeForm": "为第1周启动子智能体"},
  {"content": "为第2周启动子智能体", "status": "pending", "activeForm": "为第2周启动子智能体"},
  # ... 为每个周创建一个任务
  {"content": "汇总所有结果并清理临时文件", "status": "pending", "activeForm": "汇总所有结果并清理临时文件"}
]
```

**读取参考文档**：
- **需要脚本参数**：读取 `references/script-api-reference.md` 查看详细参数

**工作流程**：

1. **读取调用说明**：`{输出路径}/tmp/claude_instruction.md`（标记第一个任务为 in_progress）
2. **并行启动子智能体**：使用 Task 工具为每个周启动独立的 general-purpose 子智能体
   - 📘 **调用方法**：参考 `references/workflow.md` 第 2.2 节的详细示例
   - 在同一个响应中调用多次 Task 工具实现并行处理
   - 为每个子任务标记状态（启动时 → in_progress，完成时 → completed）
   - ⚠️ **重要**：子智能体必须只返回简短的成功/失败状态，不要输出详细报告
3. **汇总结果**：收集所有子任务的成功/失败状态（标记为 in_progress）
4. **清理临时文件**：删除成功的临时文件，保留失败的用于调试（标记为 completed）

**⚠️ 子智能体输出规范**（重要）：
- ✅ 只返回简短状态："✅ 第X周周报生成成功" 或 "❌ 第X周周报生成失败：[原因]"
- ❌ 不要输出详细的工作内容、数据统计、术语转换示例等
- ❌ 不要输出详细的执行步骤说明
- ✅ **严格按模板输出**：
  - 如果提供了模板（--template参数）：只输出模板格式的周报文件

**完整的工作流程和 Task 工具调用示例**：📘 **[workflow.md](references/workflow.md)**

## 参考文档

### 📘 [workflow.md](references/workflow.md)
完整的工作流程指南，包含：
- 详细的 Step 2 执行步骤
- 子智能体任务提示模板（可直接复制使用）
- 临时文件结构和清理规则

### 📘 [examples.md](references/examples.md)
常见使用场景示例：
- 示例1：生成本月周报（Markdown格式）
- 示例2：使用Word模板
- 示例3：批量生成多周周报
- 示例4：多项目汇总

### 📘 [script-api-reference.md](references/script-api-reference.md)
Python 脚本详细调用参数和使用示例：
- `parse_time.py` - 时间解析
- `analyze_template.py` - 模板分析
- `get_git_logs.py` - Git日志获取（精简模式）
- `fill_template.py` - 模板填充和导出
- `orchestrate_reports.py` - 编排所有步骤

## 参数说明

### orchestrate_reports.py 参数

- `--paths`（必须）：项目路径列表，逗号分隔
- `--time`（必须）：时间表达式
  - 相对时间：`本周`、`上周`、`本月`、`上月`、`本年`、`去年`
  - 绝对时间：`YYYY-MM-DD` 或 `YYYY-MM-DD-YYYY-MM-DD`
- `--output`（必须）：输出目录路径
- `--template`（可选）：模板文件路径（支持 .md 和 .docx）
- `--format`（可选，默认 md）：输出格式（`md` 或 `docx`）
- `--naming`（可选）：周报命名规则列表，逗号分隔
  - **推荐使用**：为每个周报指定自定义文件名
  - 示例：`--naming "华电第一周周报,华电第二周周报"`
  - 命名规则数量必须与生成的周报数量一致
  - 不提供时使用默认命名：`第X周周报.docx`

### 时间表达式示例

| 表达式 | 说明 | 生成的周报 |
|--------|------|-----------|
| `本周` | 当前周的周一到周五 | 1份 |
| `本月` | 本月1日到最后一日（按周划分） | 4-5份 |
| `2025-1-1-2025-1-31` | 指定时间范围 | 按周划分 |
| `2025-1-15` | 指定日期所在周 | 1份 |

## 常见问题

**Q: 临时文件保存在哪里？**
A: `{输出路径}/tmp/` 目录，成功后自动清理
