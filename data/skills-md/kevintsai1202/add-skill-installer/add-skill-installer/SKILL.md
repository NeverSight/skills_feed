---
name: add-skill-installer
description: 安裝 Agent Skills 到本機。當用戶想要「安裝技能」、「新增 skill」、「從 GitHub 安裝 skill」、或「install skill from repo」時觸發此技能。
metadata:
  author: kevin
  version: "1.1.0"
  argument-hint: <github-repo-or-url>
---

# Add Skill Installer

透過 `npx add-skill` 從任何 Git 儲存庫安裝 Agent Skills。

## 支援的 Agents

| Agent | 識別名稱 | 全域技能目錄 |
|-------|----------|--------------|
| **Antigravity** | `antigravity` | `~/.gemini/antigravity/skills/` |
| **Claude Code** | `claude-code` | `~/.claude/skills/` |
| **Cursor** | `cursor` | `.cursor/skills/` |
| **Codex** | `codex` | `.codex/skills/` |
| **OpenCode** | `opencode` | `.opencode/skills/` |
| **GitHub Copilot** | `github-copilot` | `.github/copilot/skills/` |
| **Roo Code** | `roo` | `.roo/skills/` |

## CLI 完整用法

```
Usage: add-skill [options] <source>

Install skills onto coding agents

Arguments:
  source                   Git repo URL, GitHub shorthand (owner/repo), or direct path to skill

Options:
  -V, --version            輸出版本號
  -g, --global             全域安裝（user-level）而非專案級
  -a, --agent <agents...>  指定目標 Agent（可指定多個）
  -s, --skill <skills...>  指定要安裝的技能名稱（可指定多個）
  -l, --list               列出儲存庫中可用的技能（不安裝）
  -y, --yes                跳過確認提示（非互動模式）
  -h, --help               顯示說明
```

## 來源格式

```bash
# GitHub 簡寫
npx add-skill vercel-labs/agent-skills

# 完整 GitHub URL
npx add-skill https://github.com/vercel-labs/agent-skills

# 指定 Repo 中的特定路徑
npx add-skill https://github.com/vercel-labs/agent-skills/tree/main/skills/frontend-design

# GitLab URL
npx add-skill https://gitlab.com/org/repo

# SSH Git URL
npx add-skill git@github.com:vercel-labs/agent-skills.git
```

## 常用指令範例

### 列出可用技能
```bash
npx add-skill vercel-labs/agent-skills --list
```

### 安裝所有技能到 Antigravity 全域
```bash
npx add-skill vercel-labs/agent-skills -g -a antigravity -y
```

### 安裝到多個 Agents
```bash
npx add-skill vercel-labs/agent-skills -g -a antigravity claude-code cursor -y
```

### 安裝特定技能
```bash
npx add-skill vercel-labs/agent-skills --skill frontend-design -g -a antigravity -y
```

### 安裝多個特定技能
```bash
npx add-skill vercel-labs/agent-skills --skill frontend-design nextjs-expert -g -a antigravity -y
```

### 安裝到當前專案（非全域）
```bash
npx add-skill vercel-labs/agent-skills -a antigravity -y
```

### 互動式安裝（會提示選擇）
```bash
npx add-skill vercel-labs/agent-skills
```

## 執行步驟

當用戶請求安裝技能時：

1. **確認來源**：詢問用戶想從哪個 Git 儲存庫安裝
2. **列出技能**：執行 `npx add-skill <source> --list` 顯示可用技能
3. **確認範圍**：詢問要安裝到全域 (`-g`) 或專案級
4. **確認目標 Agent**：詢問要安裝到哪些 Agent（可多選）
5. **執行安裝**：執行安裝命令並回報結果
6. **驗證安裝**：檢查技能目錄確認安裝成功

## 技能儲存庫推薦

| 來源 | 說明 |
|------|------|
| `vercel-labs/agent-skills` | Vercel 官方技能集 |
| [skillsmp.com](https://skillsmp.com/) | Skills Marketplace |
| [agentskills.io](https://agentskills.io/) | Agent Skills 社群 |

## 注意事項

- 需要安裝 Node.js 18+ 和 npm
- 首次執行會提示安裝 `add-skill` 套件
- 全域技能安裝後會立即生效，無需重啟 Agent
- 使用 `-y` 參數可跳過所有確認提示，適用於 CI/CD
