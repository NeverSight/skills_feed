---
name: skill-to-linebot
description: Convert any AI skill into a deployable LINE Bot service. Triggers on requests like "幫我把 XXX 變成 LINE Bot", "將這個 skill 部署成 LINE Bot", "create LINE Bot from skill".
---

# Skill to LINE Bot 轉換技能

將任意 AI Skill 轉換成可部署的 LINE Bot 服務。

---

## 使用時機

當用戶提出以下請求時啟用此技能：
- 「幫我把 XXX skill 變成 LINE Bot」
- 「將這個 skill 部署成 LINE Bot」
- 「我想讓這個 skill 能在 LINE 上使用」
- 「create a LINE Bot from this skill」

---

## 核心功能

1. **Skill 分析** — 解析目標 skill 的結構、功能與用途
2. **程式碼生成** — 生成完整的 Google Apps Script 專案
3. **部署指南** — 產生詳細的部署步驟說明

---

## 工作流程

### Step 1: 確認目標 Skill

詢問或確認用戶想要轉換的 skill：

```
請告訴我你想轉換的 skill 路徑，例如：
- .agent/skills/meihua-yishu
- .agent/skills/bazi

或者直接告訴我 skill 的名稱，我會幫你找到它。
```

### Step 2: 分析 Skill 結構

讀取並分析目標 skill 的以下內容：

#### 2.1 必讀檔案
- `SKILL.md` — 提取 name、description、核心功能、使用流程

#### 2.2 選讀檔案
- `scripts/*.py` — 識別計算邏輯（如有）
- `references/*.md` — 識別知識庫內容（如有）
- `ETHICS.md` — 提取倫理規範（如有）

#### 2.3 分析要點

從 SKILL.md 中提取：
1. **Skill 名稱** — 用於 Config.BOT_NAME
2. **功能描述** — 用於生成歡迎訊息
3. **核心功能** — 用於設計對話邏輯
4. **輸入類型** — 用戶可能輸入的資料類型（文字、數字、時間等）
5. **輸出格式** — 回應的內容結構

### Step 3: 生成 GAS 專案

在用戶指定的目錄（或預設為 `{skill-name}-line-bot/`）建立以下檔案：

#### 3.1 直接複製的模板（無需修改）

從 `templates/` 目錄複製以下檔案：

| 模板檔案 | 目標檔案 |
|----------|----------|
| `appsscript.json` | `appsscript.json` |
| `LineBot.gs.template` | `LineBot.gs` |
| `Database.gs.template` | `Database.gs` |

#### 3.2 需要填充的模板

##### Config.gs

替換以下佔位符：
- `{{SKILL_NAME}}` → Skill 技術名稱（如 `meihua-yishu`）
- `{{SKILL_DISPLAY_NAME}}` → Skill 顯示名稱（如 `梅花易數占卜`）
- `{{WELCOME_MESSAGE}}` → 歡迎訊息

##### Main.gs

直接複製 `Main.gs.template`，無需修改。

##### OpenAI.gs

直接複製 `OpenAI.gs.template`，無需修改。

##### SkillCore.gs（最重要！）

這是需要根據 Skill 內容客製化的核心檔案。

替換以下佔位符：

**`{{SYSTEM_PROMPT}}`**

根據 Skill 的 SKILL.md 內容生成系統提示詞，應包含：
- Skill 的角色定義
- 核心功能說明
- 回應格式要求
- 注意事項與限制

範例（以梅花易數為例）：
```javascript
SYSTEM_PROMPT: `你是一位專業的梅花易數占卜師。

【核心功能】
- 時間起卦：根據當前時間進行占卜
- 數字起卦：根據用戶提供的數字進行占卜
- 卦象解讀：分析體用關係並提供建議

【回應要求】
1. 使用繁體中文回答
2. 先說明卦象，再給出解讀
3. 提供具體可行的建議
4. 語氣溫和、正面

【注意事項】
- 卦象僅供參考，不代表絕對結果
- 不預測具體死亡或極端不幸
- 鼓勵用戶獨立思考`,
```

**`{{PROCESS_MESSAGE_LOGIC}}`**

根據 Skill 的功能生成處理邏輯。常見模式：

**模式 A：純 AI 對話型**
```javascript
// 直接呼叫 OpenAI
const response = OpenAI.chat(userMessage, this.SYSTEM_PROMPT);
return response;
```

**模式 B：帶有計算邏輯型**
```javascript
// 先處理輸入，再呼叫 AI
const processedInput = this.preprocessInput(userMessage);
const enhancedPrompt = this.SYSTEM_PROMPT + '\n\n【用戶輸入分析】\n' + processedInput;
const response = OpenAI.chat(userMessage, enhancedPrompt);
return response;
```

**模式 C：使用 Vector Store 型**
```javascript
// 使用 Responses API 搜尋知識庫
const response = OpenAI.responsesWithSearch(userMessage, this.SYSTEM_PROMPT);
return response;
```

**`{{HELPER_FUNCTIONS}}`**

根據需要添加輔助函數，例如：
- 輸入預處理
- 數字提取
- 時間處理
- 格式化輸出

### Step 4: 生成部署指南

在專案目錄中建立 `README.md`，包含：

```markdown
# {Skill 名稱} LINE Bot 部署指南

## 📋 快速開始

### 1. 建立 Google Sheets

1. 開啟 [Google Sheets](https://sheets.google.com)
2. 建立新試算表，命名為「{Skill 名稱} 資料庫」
3. 複製試算表 ID（網址中 `/d/` 和 `/edit` 之間的字串）

### 2. 建立 Google Apps Script 專案

1. 開啟 [Google Apps Script](https://script.google.com)
2. 點擊「新專案」
3. 將專案命名為「{Skill 名稱} LINE Bot」
4. 將以下檔案內容複製到 GAS 專案中：
   - `Config.gs`
   - `Main.gs`
   - `LineBot.gs`
   - `Database.gs`
   - `OpenAI.gs`
   - `SkillCore.gs`

### 3. 設定 Script Properties

在 GAS 中點擊 ⚙️「專案設定」 > 「指令碼屬性」，新增：

| 屬性名稱 | 說明 |
|----------|------|
| `LINE_CHANNEL_SECRET` | LINE Messaging API Channel Secret |
| `LINE_CHANNEL_ACCESS_TOKEN` | LINE Messaging API Access Token |
| `OPENAI_API_KEY` | OpenAI API Key |
| `SPREADSHEET_ID` | Google Sheets 試算表 ID |

### 4. 部署為網頁應用程式

1. 點擊「部署」→「新增部署作業」
2. 選擇類型：「網頁應用程式」
3. 設定：
   - 執行身分：我
   - 存取權限：任何人
4. 點擊「部署」
5. 複製產生的 **網頁應用程式網址**

### 5. 設定 LINE Developers

1. 開啟 [LINE Developers Console](https://developers.line.biz/console/)
2. 建立 **Messaging API Channel**
3. 在「Messaging API」設定中：
   - 將 GAS 網址貼到 **Webhook URL**
   - 啟用 **Use webhook**
   - 關閉 **Auto-reply messages**
4. 取得 **Channel Secret** 和 **Channel Access Token**

## 🧪 測試

設定 `TEST_USER_ID` 後，在 GAS 中執行：
- `testLineSend()` — 測試 LINE 連接
- `testSkillCore()` — 測試功能邏輯

## 📱 使用

掃描 LINE 官方帳號 QR Code 加為好友，即可開始使用！
```

### Step 5: 產生輸出摘要

完成後，向用戶報告：

```
✅ LINE Bot 專案已生成！

📁 專案位置：{output_directory}

📄 生成的檔案：
- appsscript.json — GAS 設定
- Config.gs — 設定管理
- LineBot.gs — LINE API 封裝
- Database.gs — 資料庫操作
- OpenAI.gs — AI 整合
- Main.gs — Webhook 入口
- SkillCore.gs — {Skill 名稱} 核心邏輯
- README.md — 部署指南

📖 下一步：
1. 閱讀 README.md 中的部署指南
2. 建立 Google Sheets 和 GAS 專案
3. 設定 LINE Developers
4. 部署並測試

需要我幫你升級到 Flex Message 版本嗎？
```

---

## 進階功能（Phase 2）

### Flex Message 升級

當用戶要求升級 Flex Message 時：

1. 生成 `LineMessages.gs`，包含：
   - 歡迎訊息 Flex 模板
   - 結果顯示 Flex 模板
   - 按鈕選單模板

2. 修改 `Main.gs` 中的回覆邏輯

⚠️ **注意**：Flex Message 在 GAS 中除錯困難，建議先確保純文字版本運作正常後再升級。

### Vector Store 整合

如果 Skill 有 `references/` 目錄：

1. 建議用戶使用 `scripts/upload-skills.js` 上傳知識庫到 OpenAI Vector Store
2. 取得 `OPENAI_VECTOR_STORE_ID` 並填入 Script Properties
3. SkillCore 將自動使用 Responses API 進行 RAG

---

## 模板位置

所有模板檔案位於：
```
.agent/skills/skill-to-linebot/templates/
├── appsscript.json
├── Config.gs.template
├── LineBot.gs.template
├── Database.gs.template
├── OpenAI.gs.template
├── Main.gs.template
└── SkillCore.gs.template
```

---

## 常見問題

### Q: Webhook 返回 404
A: 確認已部署為「網頁應用程式」，而非「API 執行檔」。

### Q: LINE 沒有回應
A: 檢查 Script Properties 中的 `LINE_CHANNEL_ACCESS_TOKEN` 是否正確。

### Q: OpenAI 錯誤
A: 確認 `OPENAI_API_KEY` 正確且有足夠額度。

### Q: 如何除錯？
A: 在 GAS 中點擊「執行項目」>「執行記錄」查看 Logger 輸出。

---

## 版本資訊

- **版本**：1.0
- **更新日期**：2026年1月
- **特點**：
  - 純文字優先，穩定易除錯
  - 模組化設計，通用模組無需修改
  - 支援 OpenAI Chat Completions 和 Responses API
  - 簡化的 Google Sheets 資料庫操作
