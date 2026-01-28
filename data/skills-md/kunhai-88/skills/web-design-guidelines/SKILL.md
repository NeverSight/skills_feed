---
name: web-design-guidelines
description: "按 Web 界面指南审查 UI 代码。当用户要求「审查我的 UI」「检查无障碍」「审计设计」「审查 UX」或「按最佳实践检查站点」时使用。"
license: MIT
---

# Web 界面指南

按 Web 界面指南对文件进行合规性审查。

## 工作流程

1. 从下方来源 URL 获取最新指南
2. 读取指定文件（或向用户索要文件/匹配模式）
3. 按指南中的全部规则进行检查
4. 以简洁的 `文件:行号` 格式输出结果

## 指南来源

每次审查前获取最新指南：

```
https://raw.githubusercontent.com/vercel-labs/web-interface-guidelines/main/command.md
```

使用 WebFetch 拉取最新规则。拉取内容包含所有规则及输出格式说明。

## 使用方式

当用户提供文件或模式参数时：
1. 从上述来源 URL 拉取指南
2. 读取指定文件
3. 应用拉取到的全部规则
4. 按指南规定的格式输出结果

若未指定文件，向用户询问要审查哪些文件。
