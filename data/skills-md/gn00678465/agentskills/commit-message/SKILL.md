---
name: commit-message
description: 分析 git staged changes 並根據 Conventional Commits 規範自動生成繁體中文 commit message。適用於需要生成符合規範的 commit 訊息時，例如「幫我寫 commit message」、「產生 commit」、「提交變更」等請求。會自動檢查是否在 main/master 分支並提供適當建議。
version: 0.1.0
---

# 慣例式提交訊息生成器

根據 [Conventional Commits 1.0.0-beta.4](https://www.conventionalcommits.org/zh-hant/v1.0.0-beta.4/) 規範，分析 git staged changes 並自動生成繁體中文 commit message。

## 使用時機

- 需要為 staged changes 生成 commit message
- 想要符合慣例式提交規範的提交訊息
- 需要繁體中文描述的 commit message

## 慣例式提交規範

> 完整規範請參考 `references/conventional-commits-spec.md`

### 組成結構

```
<類型>[可選的作用範圍]: <描述>

[可選的正文]

[可選的頁腳]
```

### 類型（Type）

根據官方規範，以下兩種類型具有語意化版本意義：

| 類型 | SemVer | 說明 |
|------|--------|------|
| `feat` | MINOR | 新增功能 |
| `fix` | PATCH | 修正臭蟲 |

以下類型由 [@commitlint/config-conventional](https://github.com/conventional-changelog/commitlint/tree/master/%40commitlint/config-conventional) 推薦使用：

| 類型 | 說明 |
|------|------|
| `docs` | 文件更新 |
| `style` | 程式碼格式調整（不影響功能） |
| `refactor` | 重構程式碼 |
| `perf` | 效能優化 |
| `test` | 測試相關 |
| `build` | 建置系統或外部相依性 |
| `ci` | CI 設定檔案 |
| `chore` | 其他雜項（工具、配置等） |
| `revert` | 撤銷先前的 commit |

### 作用範圍（Scope）- 可選

- 作用範圍**必須**由描述程式區段的名詞組成，並用括號包覆
- 範例：`feat(parser):`、`fix(api):`、`chore(eslint):`

### 描述（Subject）

- **必須**緊接在類型/作用範圍的冒號與空格之後
- **本 Skill 要求使用繁體中文撰寫**
- 限制在 50 字元以內
- 使用祈使句（如：「新增」、「修正」、「更新」）
- 不加句號
- 清楚描述變更的核心內容

### 正文（Body）- 可選

- **必須**在描述後的一個空行之後開始
- **本 Skill 要求使用繁體中文撰寫**
- 使用項目符號列表（`-` 開頭）
- 每個項目描述一個具體變更
- 優先說明做了什麼，必要時補充原因
- 使用台灣常用技術詞彙（如：「套件」、「設定」、「腳本」）

### 頁腳（Footer）- 可選

- 包含關於提交的詮釋資訊
- 範例：相關的拉取請求、審核者、重大變更
- 每個詮釋資訊一行

### 重大變更（Breaking Changes）

根據官方規範，重大變更對應到 SemVer 的 `MAJOR` 版本。標示方式：

**方式一：在類型後加 `!`**

```
feat(api)!: 變更使用者認證機制

BREAKING CHANGE: 移除舊版 API 端點，所有用戶端需更新至新版 SDK
```

**方式二：僅在頁腳標示**

```
feat: 變更使用者認證機制

- 實作新版 OAuth 2.0 流程
- 移除舊版 session 認證

BREAKING CHANGE: 移除舊版 API 端點，所有用戶端需更新至新版 SDK
```

**規範要求：**
- `BREAKING CHANGE` **必須**大寫
- 使用 `!` 提示時，正文或頁腳內**必須**包含 `BREAKING CHANGE: description`

## 執行步驟

### 步驟 1：取得變更資訊

```bash
# 檢查當前狀態與分支
git status

# 查看已 staged 的變更統計
git diff --staged --stat

# 查看已 staged 的變更內容
git diff --staged
```

### 步驟 2：檢查分支

**判斷當前分支是否為 `main` 或 `master`：**

**情況 A（安全分支）：** 若當前**不是** `main` 或 `master` 分支
- 繼續執行步驟 3

**情況 B（主分支）：** 若當前**是** `main` 或 `master` 分支
- **停止**後續操作
- 依據變更內容，建議符合規範的**新分支名稱**
  - 範例：`feat/login-form-validation`、`fix/payment-bug`
- **回報錯誤**：`請先切換至建議的分支（或自訂分支）後，再執行 commit。`

### 步驟 3：分析複雜度

根據 `git diff --staged --stat` 輸出，使用以下評分系統計算複雜度：

#### 複雜度評分表

起始分數為 0，符合條件則加分：

| 類別 | 條件 | 分數 |
|------|------|------|
| **變更量** | 變更行數 > 200 | +3 |
| | 變更檔案數 > 5 | +2 |
| **高風險檔案** | 涉及 lock 檔案（`package-lock.json`、`yarn.lock`、`pnpm-lock.yaml`） | +5（強制複雜模式） |
| | 涉及資料庫 Schema 或 Migration | +3 |
| | 涉及認證或安全邏輯（`auth`、`security`、`permission`） | +3 |
| **架構變更** | 涉及設定檔（`*.config.*`、`.env*`） | +2 |
| | 涉及 CI/CD 設定（`.github/`、`.gitlab-ci.yml`） | +2 |

### 步驟 4：選擇提交模式

根據總分選擇提交模式：

#### 情況 A：簡單模式（分數 < 4）

- 直接使用 `-m` 參數生成 commit message
- 適用於小型、低風險的變更

```bash
git commit -m "feat: 新增使用者登入功能"
```

多行訊息：

```bash
git commit -m "feat: 新增使用者登入功能" -m "- 實作 JWT 認證機制
- 新增登入表單驗證"
```

#### 情況 B：複雜模式（分數 >= 4）

- 使用檔案方式生成詳細的 commit message
- 適用於大型、高風險或需要詳細說明的變更

```bash
# 將訊息寫入 .git/COMMIT_EDITMSG
git commit -F .git/COMMIT_EDITMSG
```

或使用獨立檔案（提交後需清理）：

```bash
# macOS/Linux
git commit -F commit-message.txt && rm -f commit-message.txt

# Windows
git commit -F commit-message.txt
# 提交後手動刪除 commit-message.txt
```

### 步驟 5：生成 Commit Message 並確認

1. 分析變更類型和影響範圍
2. 根據變更內容決定最適合的 commit type
3. 依據步驟 4 選擇的模式，輸出完整的 Commit Message
4. 輸出對應的 `git commit` 指令
5. **詢問使用者**：是否需要協助執行 commit？
   - **是**：執行 `git commit` 指令完成提交
   - **否**：由使用者自行複製指令執行

## 範例

詳細範例請參考 `references/examples.md`，涵蓋：

- **基礎範例**：feat、fix、docs、style、refactor、perf、test、build、ci、chore、revert
- **進階範例**：含作用範圍、破壞性變更、問題編號、共同作者、複雜變更
- **不良範例**：常見錯誤寫法與修正建議

**快速參考：**

```
feat: 新增使用者登入功能

- 實作 JWT 認證機制
- 新增登入表單驗證
```

```
fix(cart): 修正購物車金額計算錯誤

- 修正折扣碼套用順序問題
```

## 注意事項

- **只有 staged 狀態的變更會被考慮**
- 未 staged 的變更不會包含在 commit message 分析中
- 建議先使用 `git add` 選擇性地 stage 要提交的變更
- 若變更過於複雜，建議拆分為多個獨立的 commit
- 當提交符合一或多種提交類型時，應盡可能切成多個提交

## 常用技術詞彙對照

| 英文 | 繁體中文（台灣慣用） |
|------|---------------------|
| package | 套件 |
| config/configuration | 設定 |
| script | 腳本 |
| dependency | 相依性 |
| component | 元件 |
| module | 模組 |
| function | 函式 |
| variable | 變數 |
| parameter | 參數 |
| implement | 實作 |
| initialize | 初始化 |
| optimize | 優化 |
| refactor | 重構 |
| validate | 驗證 |
| authentication | 認證 |
| authorization | 授權 |
| bug | 臭蟲 |
| pull request | 拉取請求 |

## 參考資料

- `references/conventional-commits-spec.md` - 慣例式提交 1.0.0-beta.4 完整規範
- `references/examples.md` - 各類型 commit message 範例集
- [Conventional Commits 官方網站](https://www.conventionalcommits.org/zh-hant/v1.0.0-beta.4/)
- [SemVer 語意化版本](https://semver.org/lang/zh-TW/)
- [@commitlint/config-conventional](https://github.com/conventional-changelog/commitlint/tree/master/%40commitlint/config-conventional)
