---
name: report
description: 生成日报/周报/月报的技能。适用于“生成日报/周报/月报”“从 Git 提交生成报告”“将报告 JSON 渲染为 Word”等需求；支持多仓库扫描、按日/周/月统计、输出 JSON 与 Word。
---

# 工作流

## 1) 确定范围与配置
- 统计范围：按日/周/月
- 仓库范围：单仓库或多仓库
- 作者：可指定 user.name 或 user.email（支持逗号分隔或数组）
- 运行环境：需要 Node.js 18+
- 当用户明确要求“生成日报/周报/月报”时，请分别设置 `stat_mode=day/week/month`

**全局配置文件**（用于覆盖脚本默认值）：
- 读取顺序：
  1. 环境变量 `REPORT_CONFIG`
  2. 当前目录 `report.config.json`
  3. `~/.config/report/config.json`
  4. `~/.report.json`
- 字段示例见 `resources/config.example.json`
- 还可用 `REPORT_REPO_ROOTS` 临时指定仓库根目录列表（用系统路径分隔符分隔）
- 首次运行若未找到配置，会自动生成默认配置到 `~/.config/report/config.json`（`repo_roots` 默认当前目录），并立即退出（不会继续执行统计）
- 当输出包含 `CONFIG_INIT_REQUIRED` 时，必须停止后续流程，仅提示用户去修改配置后再运行
- 关键字段：
  - `stat_mode`: `day` / `week` / `month`
  - `day_offset`: 0=今天，1=昨天

## 2) 生成原始 JSON
- 在任意目录执行以下命令（`<skill_root>` 为本 SKILL.md 所在目录）：

```bash
node <skill_root>/scripts/weekly.js --stat-mode day|week|month
```

- 也支持中文：`日报` / `周报` / `月报`

- 输出文件形如：`本日/本周/本月工作日报/周报/月报_YYYY-MM-DD.json`
- 输出目录：默认输出到桌面（`~/Desktop`），若不存在则输出到当前目录
- 不要覆盖或修改原始 JSON

## 3) 生成优化版 JSON（必做）
- 使用 `resources/prompt.txt` 对原始 JSON 进行报告化与中文化
- 必须将 commit message 转为中文并润色为适合给老板汇报的表达
- 输出新文件，例如：`本日/本周/本月工作日报/周报/月报_ai.json`

## 4) 渲染 Word

```bash
node <skill_root>/scripts/weekly_render.js -i <优化后的JSON> -o <输出文件>.docx
```
## 5) 回复结果
- 直接渲染 Word，不要询问用户是否继续
- 返回最终 Word 文件的完整路径
- 同时返回优化后的 JSON 文件路径

# 注意事项
- 若未找到仓库，优先配置 `repo_paths` 或 `repo_roots`
- 如需多仓库统计，建议设置 `repo_roots` 并结合 `company_git_patterns` 过滤
- 依赖安装与编译请参考 `skills/report/README.md`
