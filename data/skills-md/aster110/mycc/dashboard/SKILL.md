---
name: dashboard
description: 可视化查看 cc 能力看板。触发词："/dashboard"、"看看能力看板"、"cc 能力"、"技能看板"
---

# cc 能力看板可视化

生成好看的 HTML 页面展示 cc 的技能、开发中能力、规划想法。

## 触发词

- `/dashboard`
- "看看能力看板"
- "cc 能力"
- "技能看板"

## 执行

```bash
python3 .claude/skills/dashboard/scripts/visualize.py
```

脚本会：
1. 读取 `.claude/DASHBOARD.md`
2. 解析内容生成 HTML
3. 自动在浏览器打开

## 完成后

告知用户：看板已在浏览器打开。
