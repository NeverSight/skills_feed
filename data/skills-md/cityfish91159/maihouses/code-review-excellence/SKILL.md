---
name: code-review-excellence
description: 程式碼審查最佳實踐指南。當進行 PR review、代碼審查或用戶提到「review」、「審查」時使用。
allowed-tools: Read, Grep
---

# Code Review Excellence Skill

本地快取版本，來源：[wshobson/agents](https://github.com/wshobson/agents)

## 核心原則

### 審查心態

- 目標：抓 bugs、確保可維護性、知識分享、執行標準
- **非**目標：炫技、無意義阻擋

### 有效回饋

- 具體且可執行
- 教育性，非批判性
- 聚焦代碼，非個人
- 平衡（也要讚美好的部分）
- 優先級標示

## 審查流程

1. **Context Gathering** (2-3 min): 理解 PR 需求與範圍
2. **High-Level Review** (5-10 min): 架構、檔案組織、測試策略
3. **Line-by-Line Review** (10-20 min): 邏輯、安全、性能、可維護性
4. **Summary & Decision** (2-3 min): 明確結論與建設性摘要

## 優先級標籤

| 標籤            | 意義                 |
| --------------- | -------------------- |
| 🔴 [blocking]   | 必須修復才能 merge   |
| 🟡 [important]  | 應該修復，可討論     |
| 🟢 [nit]        | 可有可無，不阻擋     |
| 💡 [suggestion] | 替代方案建議         |
| 📚 [learning]   | 教育性說明，無需動作 |
| 🎉 [praise]     | 做得好！             |

## 安全審查重點

- Input validation?
- SQL injection risks?
- XSS vulnerabilities?
- Sensitive data exposure?
- Authentication/Authorization checks?

## 常見陷阱

- 完美主義（過度挑剔）
- 範圍蔓延（超出 PR 範圍）
- 不一致標準
- 延遲審查
- 橡皮圖章（不認真看）
