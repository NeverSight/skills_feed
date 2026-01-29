---
schema: "1.0"
name: claude-domain-skills
version: "1.0.0"
description: 非技術領域專業知識集合，包含商業、金融、創意、專業服務、生活、方法論等 18 個領域
triggers: [領域, domain, 專業, 知識, 商業, 金融, 創意, 生活]
keywords: [domain, skills, knowledge, business, finance, creative, professional, lifestyle]
author: miles990
---

# Claude Domain Skills

> 讓 AI 具備各領域專業知識的 skill 集合

## 概述

這是一個非技術領域的專業知識庫，設計用於：
- 搭配 `/evolve` skill 使用，自動識別任務所需領域
- 透過 skillpkg 按需載入特定領域知識
- 提供各領域的框架、方法論、最佳實踐

## 可用領域 (18)

### 💰 Finance (金融)
| 領域 | 觸發詞 | 說明 |
|------|--------|------|
| `finance/quant-trading` | 量化, backtest, 策略 | 量化交易策略開發 |
| `finance/investment-analysis` | 財報, 投資, 估值, ROE | 投資分析與估值 |
| `finance/strategy-optimization` | 策略優化, 勝率, 報酬, 回測 | 交易策略優化方法論 |

### 💼 Business (商業)
| 領域 | 觸發詞 | 說明 |
|------|--------|------|
| `business/marketing` | 行銷, SEO, 漏斗, CAC | 數位行銷策略 |
| `business/sales` | 銷售, 電商, CRM | 銷售與電商營運 |
| `business/product-management` | PRD, OKR, 路線圖 | 產品管理 |
| `business/project-management` | Scrum, Sprint, 甘特圖 | 專案管理 |
| `business/strategy` | 策略, 藍海, 差異化, 商業模式 | 商業策略 |

### 🎨 Creative (創意)
| 領域 | 觸發詞 | 說明 |
|------|--------|------|
| `creative/game-design` | 遊戲, 關卡, 平衡, GDD | 遊戲設計 |
| `creative/ui-ux-design` | UI, UX, 無障礙, WCAG | 介面體驗設計 |
| `creative/brainstorming` | 靈感, 頭腦風暴, 創意, SCAMPER | 創意發想 |
| `creative/storytelling` | 小說, 劇本, 角色, 三幕劇 | 故事創作 |
| `creative/visual-media` | 攝影, 影片, 動畫, 分鏡 | 影像創作 |

### 🔬 Professional (專業服務)
| 領域 | 觸發詞 | 說明 |
|------|--------|------|
| `professional/research-analysis` | 研究, 競品, 調研, 分析 | 研究分析 |
| `professional/knowledge-management` | 筆記, PKM, 第二大腦, Zettelkasten | 知識管理 |

### 🌱 Lifestyle (生活)
| 領域 | 觸發詞 | 說明 |
|------|--------|------|
| `lifestyle/personal-growth` | 人生規劃, 個人品牌, 時間管理 | 個人成長 |
| `lifestyle/side-income` | 副業, 被動收入, 財務自由 | 副業投資 |

### 🧠 Methodology (方法論)
| 領域 | 觸發詞 | 說明 |
|------|--------|------|
| `methodology/knowledge-acquisition-4c` | 學習, 研究, 新領域, 知識習得 | 從未知到專業的系統化學習 |

## 使用方式

### 方式 1: 自動識別 (推薦)

搭配 `/evolve` skill 使用時，會自動根據任務關鍵詞載入對應領域：

```
User: /evolve 分析台積電財報，評估投資價值

Agent:
🔍 Auto Domain Detection
→ 關鍵詞: 財報, 分析, 投資
→ 載入: finance/investment-analysis
→ 使用投資分析框架執行任務
```

### 方式 2: 手動安裝

```python
# 安裝特定領域
mcp__skillpkg__install_skill({
    "source": "github:miles990/claude-domain-skills#finance/quant-trading"
})

# 載入使用
mcp__skillpkg__load_skill({ "id": "quant-trading" })
```

### 方式 3: 使用 claude-starter-kit

```bash
npx claude-starter-kit
# 互動式選擇所需領域
```

## 領域 Skill 結構

每個領域 skill 包含：

```markdown
## 適用場景
何時使用這個領域知識

## 核心框架
該領域的標準方法論和思維模型

## 最佳實踐
經過驗證的做法

## 常見錯誤
避免踩坑的指南

## 工具推薦
領域相關的實用工具

## 參考資源
進一步學習的資源
```

## 多語言支援 (i18n)

支援多種語言版本：

| 代碼 | 語言 | 狀態 |
|------|------|------|
| `zh-TW` | 繁體中文 | ✅ 預設 |
| `en` | English | 🚧 進行中 |

### 使用英文版

```python
# 安裝英文版 skill
mcp__skillpkg__install_skill({
    "source": "github:miles990/claude-domain-skills#i18n/en/skills/investment-analysis"
})
```

詳見 [i18n/README.md](./i18n/README.md)

## 貢獻指南

歡迎貢獻新領域或翻譯！請參考 [CONTRIBUTING.md](./CONTRIBUTING.md)

## 相關專案

- [self-evolving-agent](https://github.com/miles990/self-evolving-agent) - 自動載入領域 skills
- [claude-starter-kit](https://github.com/miles990/claude-starter-kit) - 快速建立 Claude Code 專案
