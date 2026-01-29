---
name: git-workflow
description: |
  Git 分支命名與工作流程規範，確保團隊協作一致性和版本控制最佳實踐。包含分支命名格式、提交規範、Pull Request 流程，以及防止直接修改 main 分支的安全機制。適用於所有涉及檔案修改、新增功能、bug 修復的開發任務。

  ⚠️ 關鍵規則 - 必須遵守：
  1. 絕對不可以直接在 main 分支上進行任何修改或提交
  2. 任何變更都必須先建立功能分支（格式：<type>/<name>/<description>）
  3. 完成後透過 Pull Request 合併
  4. 本技能適用於所有涉及檔案修改、新增功能、bug 修復的任務

  觸發時機：任何需要修改專案檔案的操作（包括新增、編輯、刪除檔案）都必須參考此規範。
license: MIT
---

# ⚠️ 核心規則 - 開始任何工作前必讀

## 🚫 絕對禁止的操作

**在開始任何程式碼修改前，必須先檢查目前分支！**

```bash
# 檢查目前分支
git branch

# 如果在 main 分支，立即建立新分支
git checkout -b <type>/<name>/<description>
```

### 禁止清單

❌ **絕對不可以直接在 main 分支上修改檔案**  
❌ 不可以在 main 分支上執行 `git add`  
❌ 不可以在 main 分支上執行 `git commit`  
❌ 不可以在 main 分支上編輯、新增或刪除任何檔案

### 正確流程

✅ 先確認目前在 main 分支  
✅ 建立新的功能分支  
✅ 在功能分支上進行修改  
✅ 提交到功能分支  
✅ 透過 Pull Request 合併

---

## 我的功能

- 提供標準化的 Git 分支命名規範
- 確保分支類型、開發者名稱和功能描述的一致性
- 協助團隊遵循最佳的 Git 工作流程

## 何時使用我

在以下情況下使用此技能：

- 建立新的 Git 分支時
- 需要確認分支命名是否符合規範
- 團隊協作需要統一的分支管理策略
- 進行 code review 時檢查分支命名

## 分支命名規範

### 標準格式

```
<type>/<developer-name>/<feature-description>
```

### 分支類型 (type)

- **feat**: 新功能開發
  - 例如: `feat/lip/user-authentication`
  - 用於: 開發全新的功能或特性

- **fix**: 錯誤修復
  - 例如: `fix/lip/login-button-error`
  - 用於: 修復現有功能的 bug

- **refactor**: 程式碼重構
  - 例如: `refactor/lip/optimize-state-management`
  - 用於: 改善程式碼結構，但不改變功能

- **docs**: 文件更新
  - 例如: `docs/lip/update-readme`
  - 用於: 更新專案文件、README、註解等

- **style**: 樣式調整
  - 例如: `style/lip/improve-button-design`
  - 用於: UI/UX 改進、CSS 調整

- **test**: 測試相關
  - 例如: `test/lip/add-unit-tests`
  - 用於: 新增或修改測試

- **chore**: 雜項任務
  - 例如: `chore/lip/update-dependencies`
  - 用於: 依賴更新、建置配置等

### 命名原則

1. **使用小寫字母**: 所有分支名稱使用小寫
2. **使用連字符**: 單詞之間使用 `-` 連接
3. **簡潔明確**: 功能描述應簡短但具描述性
4. **英文命名**: 統一使用英文命名
5. **避免特殊字符**: 只使用字母、數字和連字符

### 實際範例

```bash
# ✅ 正確範例
git checkout -b feat/lip/add-language-selector
git checkout -b fix/lip/fix-search-modal-crash
git checkout -b refactor/lip/improve-jotai-structure
git checkout -b docs/lip/update-api-documentation

# ❌ 錯誤範例
git checkout -b new-feature              # 缺少類型和開發者名稱
git checkout -b feat/AddFeature          # 使用大寫字母
git checkout -b feat/lip/新增功能     # 使用中文
git checkout -b feat-lip-feature      # 格式錯誤
```

## 工作流程

### 1. 建立新分支

```bash
# 從 main 分支建立新分支
git checkout main
git pull origin main
git checkout -b <type>/<name>/<description>
```

### 2. 開發過程

```bash
# 定期提交變更
git add .
git commit -m "feat: implement user authentication"

# 定期同步主分支
git fetch origin main
git rebase origin/main
```

### 3. 準備合併

```bash
# 推送分支到遠端
git push -u origin <branch-name>

# 建立 Pull Request
# 使用 GitHub/GitLab 介面建立 PR
```

### 4. 合併後清理

```bash
# 刪除本地分支
git branch -d <branch-name>

# 刪除遠端分支
git push origin --delete <branch-name>
```

## 提交訊息規範

### 格式

```
<type>: <subject>

<body>

<footer>
```

### 類型 (type)

與分支類型相同: `feat`, `fix`, `refactor`, `docs`, `style`, `test`, `chore`

### ⚠️ 重要：語言使用規範

**預設使用繁體中文撰寫 commit message**

除非有特別要求（如國際協作專案），否則 commit message 的 subject 和 body 都應該使用**繁體中文**撰寫。

#### 原則

1. **Type 使用英文**: `feat`, `fix`, `refactor` 等類型標籤保持英文
2. **Subject 使用中文**: 主要描述使用繁體中文
3. **Body 使用中文**: 詳細說明使用繁體中文
4. **Footer 依情況**: issue 編號等可使用英文

### 範例

```bash
# ✅ 正確：使用中文
git commit -m "feat: 新增語言選擇器元件"

# ✅ 正確：詳細提交使用中文
git commit -m "feat: 新增語言選擇器元件

- 實作包含 5 種語言選項的下拉選單
- 新增語言設定持久化到 localStorage
- 更新 i18n 配置

Closes #123"

# ✅ 正確：修復 bug
git commit -m "fix: 修正登入按鈕點擊無反應的問題"

# ✅ 正確：重構程式碼
git commit -m "refactor: 重構 Jotai 狀態管理結構

- 拆分 dataAtoms 為多個模組
- 優化 atom 命名和組織
- 改善型別定義"

# ❌ 錯誤：使用英文（除非有特別要求）
git commit -m "feat: add language selector component"

# ❌ 錯誤：中英混用不當
git commit -m "feat: 新增 language selector 元件"
```

### 特殊情況

**何時使用英文？**

1. 國際協作專案明確要求
2. 開源專案的國際貢獻
3. 團隊特別指定使用英文

**如果不確定，預設使用中文。**

## 注意事項

1. **絕不直接在 main 分支開發**: 永遠從 main 建立新分支
2. **保持分支生命週期短**: 盡快完成並合併分支
3. **定期同步主分支**: 避免合併衝突
4. **使用有意義的名稱**: 讓他人能理解分支目的
5. **一個分支一個功能**: 避免在單一分支混合多個不相關的變更

## ⚠️ 重要：測試與提交流程

### 每次修改後必須測試

**這是強制性規則！任何程式碼修改都必須立即測試。**

```bash
# 修改程式碼後，立即執行測試
lsof -ti:3000 | xargs kill -9 2>/dev/null
sleep 2
pnpm dev
```

**檢查項目：**

- ✅ 專案能否成功啟動
- ✅ 無編譯錯誤
- ✅ 功能正常運作
- ✅ 無執行錯誤

### 完成後的提交流程

**⚠️ 絕不直接推送！必須等待使用者確認。**

```bash
# 1. 提交到本地分支
git add .
git commit -m "type: description"

# 2. ⏸️ 停止！告知使用者已完成
# 說明：「修改已完成並測試通過，請檢查後再推送」

# 3. ⏸️ 等待使用者檢查確認

# 4. ✅ 使用者確認後才推送
git push origin branch-name
```

### 推送前最終檢查清單

- [ ] 所有修改都已測試通過
- [ ] 完整功能測試已完成
- [ ] 無編譯錯誤和執行錯誤
- [ ] 變更已提交到本地
- [ ] **已通知使用者檢查**
- [ ] **等待使用者確認**
- [ ] 確認後才執行 push

### 錯誤示範 vs 正確示範

```bash
# ❌ 錯誤：直接推送
git add .
git commit -m "feat: add feature"
git push origin feature-branch  # 錯誤！未經確認就推送

# ✅ 正確：等待確認
git add .
git commit -m "feat: add feature"
# 告知使用者：「修改完成，已測試通過，請檢查」
# 等待使用者回覆確認
# 收到確認後才執行：
git push origin feature-branch
```

## 常見問題

### Q: 如何處理長期開發的功能？

A: 建立 feature 分支，定期從 main rebase，完成後再合併。

### Q: 可以在分支名稱中使用 issue 編號嗎？

A: 可以，格式: `feat/ponpon/add-feature-#123`

### Q: 如何處理緊急修復？

A: 使用 `hotfix` 類型: `hotfix/ponpon/critical-bug-fix`

### Q: 為什麼不能直接推送？

A: 使用者需要在本地環境檢查功能、測試效果、確認無誤後才能推送到遠端。這可以防止將問題程式碼推送到遠端儲存庫。

### Q: 每次修改都要測試嗎？

A: 是的，絕對需要！任何程式碼修改（無論大小）都必須立即測試，確保沒有破壞現有功能。

## 參考資源

- [Git Flow](https://nvie.com/posts/a-successful-git-branching-model/)
- [Conventional Commits](https://www.conventionalcommits.org/)
- [GitHub Flow](https://guides.github.com/introduction/flow/)
