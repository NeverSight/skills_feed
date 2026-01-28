---
name: github-workflow
description: GitHub 工作流程，包含帳號資訊、gh CLI 安裝狀態、建立 repo、push、多地同步
---

# GitHub 工作流程指南

## 帳號資訊

| 項目 | 值 |
|------|-----|
| GitHub 帳號 | bingo-taiwan |
| GitHub 網址 | https://github.com/bingo-taiwan |
| SSH 金鑰 | ~/.ssh/id_ed25519 |
| Git user.name | bingo-taiwan |

## 各環境 gh CLI 安裝狀態

啟動時先執行 `hostname` 判斷目前在哪台機器：

| 機器 | hostname | gh CLI | 路徑/備註 |
|------|----------|--------|-----------|
| 家裡 Windows | DESKTOP-J9CIIVU | ✅ 已安裝 v2.83.2 | `"/c/Program Files/GitHub CLI/gh.exe"` |
| 公司電腦 | （待補充） | ❓ 待確認 | 若無，用 `winget install GitHub.cli` 安裝 |
| GCP LMS | lms | ❌ 未安裝 | 通常不需要，用 SSH 方式 push |
| Linode 各主機 | booktest/goodins/lt1-4 | ❌ 未安裝 | 通常不需要 |

## gh CLI 快速安裝

### Windows
```powershell
winget install GitHub.cli
```

### Linux (Debian/Ubuntu)
```bash
curl -fsSL https://cli.github.com/packages/githubcli-archive-keyring.gpg | sudo dd of=/usr/share/keyrings/githubcli-archive-keyring.gpg
echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/githubcli-archive-keyring.gpg] https://cli.github.com/packages stable main" | sudo tee /etc/apt/sources.list.d/github-cli.list > /dev/null
sudo apt update
sudo apt install gh
```

### 登入（安裝後執行一次）
```bash
gh auth login
# 選擇：GitHub.com → SSH → Login with a web browser
```

## 常用 gh CLI 指令

### 建立新 repo 並 push
```bash
# 在專案目錄中執行
gh repo create REPO_NAME --public --source=. --push --description "描述"

# 若 remote 已存在，改用：
gh repo create REPO_NAME --public --description "描述"
git push -u origin master
```

### 其他常用指令
```bash
# 檢查登入狀態
gh auth status

# 列出自己的 repo
gh repo list

# Clone repo
gh repo clone bingo-taiwan/REPO_NAME

# 建立 PR
gh pr create --title "標題" --body "內容"

# 查看 PR
gh pr list
gh pr view 123
```

## 純 Git 操作（不用 gh CLI）

當機器沒有 gh CLI 時，用傳統方式：

### 1. 先在 GitHub 網頁建立 repo
https://github.com/new

### 2. 本地初始化並 push
```bash
git init
git add .
git commit -m "Initial commit"
git remote add origin git@github.com:bingo-taiwan/REPO_NAME.git
git push -u origin master
```

## 多地同步工作流

家裡 ↔ 公司 ↔ GCP ↔ Linode 多地透過 GitHub 同步

### ⚠️ 開工前必做檢查（重要！）

**問題**：如果在公司修改了程式碼但忘記 push，回家後直接開工會造成版本衝突或覆蓋對方的修改。

**Claude 執行規則**：在修改任何與遠端伺服器同步的專案前，必須先執行同步檢查：

```bash
# 1. 檢查本地是否有未提交的修改
git status

# 2. 檢查與 GitHub 的差異
git fetch origin
git log HEAD..origin/master --oneline  # 遠端有但本地沒有的 commit
git log origin/master..HEAD --oneline  # 本地有但遠端沒有的 commit

# 3. 如果遠端有更新，先 pull
git pull origin master
```

**如果發現差異**：
- 遠端有新 commit → 先 `git pull` 再開始工作
- 本地有未 push 的修改 → 先確認是否要 push，或需要 merge
- 兩邊都有修改 → 小心處理，可能需要 merge 或 rebase

### 同時檢查伺服器版本

如果專案部署在伺服器上，也要比對伺服器版本：

```bash
# 比較本地和伺服器的 webhook.php
ssh lt4 "cat /home/lt4.mynet.com.tw/public_html/linebot/webhook.php" > /tmp/server_webhook.php
diff webhook.php /tmp/server_webhook.php

# 如果有差異，確認哪個是最新版本再決定同步方向
```

### 開始工作前
```bash
git pull origin master
```

### 結束工作時
```bash
git add .
git commit -m "描述"
git push origin master
```

### 衝突處理
```bash
# 若 push 失敗，先 pull
git pull --rebase origin master

# 解決衝突後
git add .
git rebase --continue
git push origin master
```

## SSH 金鑰設定

SSH config 已設定 GitHub 連線（~/.ssh/config）：
```
Host github.com
    HostName github.com
    User git
    IdentityFile ~/.ssh/id_ed25519
    IdentitiesOnly yes
```

### 測試 SSH 連線
```bash
ssh -T git@github.com
# 應顯示：Hi bingo-taiwan! You've successfully authenticated...
```

## 常見問題

### 問題：gh: command not found
- 檢查是否已安裝
- Windows：用完整路徑 `"/c/Program Files/GitHub CLI/gh.exe"`
- 或重新開啟終端機讓 PATH 生效

### 問題：Permission denied (publickey)
- 檢查 SSH 金鑰：`ls -la ~/.ssh/`
- 測試連線：`ssh -T git@github.com`
- 確認公鑰已加到 GitHub：https://github.com/settings/keys

### 問題：remote origin already exists
```bash
# 查看現有 remote
git remote -v

# 移除後重新加
git remote remove origin
git remote add origin git@github.com:bingo-taiwan/REPO_NAME.git
```
