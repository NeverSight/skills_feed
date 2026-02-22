---
name: cc-usage
description: 查看 Claude Code 的 token 用量统计。按日期×模型维度拆分，支持按天数、项目过滤。触发词："/cc-usage"、"看看用量"、"token 消耗"、"用量统计"
---

# cc-usage — Token 用量统计

扫描本地 Claude Code 日志（`~/.claude/projects/`），按 **日期 × 模型** 维度统计 token 消耗和 API 等价费用。

纯 Python 3 脚本，无需安装任何依赖，跨平台（Mac / Linux / Windows）。

## 触发词

- "/cc-usage"
- "看看用量"
- "token 消耗"
- "用量统计"

## 执行步骤

1. 根据用户需求确定参数（天数、项目、输出格式）
2. 运行分析脚本
3. 把结果整理成**易读的 Markdown 表格**返回给用户

## 脚本位置

```
.claude/skills/cc-usage/scripts/analyzer.py
```

## 用法

```bash
# 默认：全部历史，所有项目
python3 .claude/skills/cc-usage/scripts/analyzer.py

# 最近 N 天
python3 .claude/skills/cc-usage/scripts/analyzer.py --days 7

# 只看某项目（模糊匹配目录名）
python3 .claude/skills/cc-usage/scripts/analyzer.py --project mylife

# 输出 CSV（可导入 Excel）
python3 .claude/skills/cc-usage/scripts/analyzer.py --csv

# 只看模型汇总
python3 .claude/skills/cc-usage/scripts/analyzer.py --summary
```

## 默认行为

用户没指定天数时，默认跑 `--days 7`（最近 7 天）。

## 输出要求

脚本跑完后，AI 应该：
1. 把关键数据整理成 Markdown 表格（按天 × 模型）
2. 给出日小计和总计
3. 附上模型汇总（哪个模型最费钱）
4. 如有异常（某天突然暴涨），主动指出

## 跨平台说明

- 路径：使用 `os.path.expanduser('~')` 自动适配
- 时区：使用 `datetime.astimezone()` 自动检测系统本地时区
- 依赖：仅 Python 3 标准库，无需 pip install

## 维护提示

新模型上线时需更新脚本里的 `MODEL_SHORT` 和 `PRICING` 字典。
