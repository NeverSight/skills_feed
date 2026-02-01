---
name: setup
description: 首次使用引导。交互式帮助用户完成 MyCC 初始化配置。触发词："/setup"、"帮我配置"、"初始化"、首次使用时自动触发。
---

# MyCC 初始化引导

> 这是一个交互式配置向导，帮助用户完成 MyCC 的初始化设置。

## 触发条件

- 用户输入 `/setup`
- 用户说"帮我配置"、"初始化"
- **首次使用时自动触发**：检测到 `{{YOUR_NAME}}` 未替换时，主动询问是否需要引导

---

## 配置进度清单

> 每完成一步就打勾 ✅，支持中断后继续。
> 这个清单会被更新，用于追踪进度。

- [ ] 1. 检查前置条件
- [ ] 2. 复制配置文件
- [ ] 3. 收集用户信息
- [ ] 4. 替换模板变量
- [ ] 5. 验证配置生效
- [ ] 6. 完成初始化

---

## 执行步骤

### 步骤 1：检查前置条件

**检查项**：
1. Claude Code 是否已安装（能运行 `claude --version`）
2. 当前目录是否是 mycc 项目根目录（存在 `CLAUDE.md`）

**执行方式**：
```bash
# 检查 Claude Code
claude --version

# 检查目录
ls CLAUDE.md
```

**如果失败**：
- Claude Code 未安装 → 引导用户去 https://docs.anthropic.com/en/docs/claude-code 安装
- 不在项目目录 → 提示用户 `cd` 到 mycc 目录

**完成后**：更新清单，标记步骤 1 为 ✅

---

### 步骤 2：复制配置文件

**需要复制的文件**：

| 源文件 | 目标文件 | 说明 |
|--------|----------|------|
| `.claude/settings.local.json.example` | `.claude/settings.local.json` | Hooks 配置 |
| `0-System/status.md.example` | `0-System/status.md` | 短期记忆模板 |
| `0-System/context.md.example` | `0-System/context.md` | 中期记忆模板 |

**执行方式**：
```bash
cp .claude/settings.local.json.example .claude/settings.local.json
cp 0-System/status.md.example 0-System/status.md
cp 0-System/context.md.example 0-System/context.md
```

**检查点**：确认三个文件都存在

**完成后**：更新清单，标记步骤 2 为 ✅

---

### 步骤 3：收集用户信息

**需要收集**：
- 用户的名字（用于替换 `{{YOUR_NAME}}`）

**交互方式**：
> 问用户："你希望我怎么称呼你？（这个名字会出现在 CLAUDE.md 里）"

**存储**：记住用户回答，用于下一步替换

**完成后**：更新清单，标记步骤 3 为 ✅

---

### 步骤 4：替换模板变量

**需要替换的文件**：
- `CLAUDE.md`：把所有 `{{YOUR_NAME}}` 替换为用户的名字

**执行方式**：
```bash
sed -i '' 's/{{YOUR_NAME}}/用户名字/g' CLAUDE.md
```

**检查点**：确认 `CLAUDE.md` 中不再包含 `{{YOUR_NAME}}`

**完成后**：更新清单，标记步骤 4 为 ✅

---

### 步骤 5：验证配置生效

**验证项**：
1. `.claude/settings.local.json` 存在且格式正确
2. `0-System/status.md` 存在
3. `CLAUDE.md` 中的名字已替换

**执行方式**：
```bash
# 检查文件存在
ls -la .claude/settings.local.json
ls -la 0-System/status.md
ls -la 0-System/context.md

# 检查变量已替换
grep "{{YOUR_NAME}}" CLAUDE.md || echo "✅ 变量已全部替换"
```

**如果有问题**：告诉用户哪里出错，并提供修复建议

**完成后**：更新清单，标记步骤 5 为 ✅

---

### 步骤 6：完成初始化

**输出完成消息**：

```
🎉 MyCC 初始化完成！

已完成：
✅ 配置文件已复制
✅ 名字已设置为「{用户名字}」
✅ Hooks 已配置

接下来你可以：
1. 重启 Claude Code（让 Hooks 生效）
2. 开始使用！试试说"今天有什么安排"

提示：
- 编辑 `0-System/status.md` 记录你的每日状态
- 编辑 `0-System/about-me/` 让我更了解你
- 输入 `/dashboard` 查看所有可用能力
```

**更新清单**：标记步骤 6 为 ✅，所有项目完成

---

## 中断与继续

如果用户中途离开：
1. 进度清单会保留当前状态
2. 下次触发 `/setup` 时，检查清单，从未完成的步骤继续
3. 告诉用户："上次配置到步骤 X，要继续吗？"

---

## 常见问题处理

### Q: Hooks 没生效
A:
1. 确认 `.claude/settings.local.json` 存在
2. 重启 Claude Code
3. 检查文件路径是否正确

### Q: 想重新配置
A:
1. 删除 `.claude/settings.local.json`
2. 重新运行 `/setup`

### Q: 想改名字
A: 直接编辑 `CLAUDE.md`，把名字改成你想要的
