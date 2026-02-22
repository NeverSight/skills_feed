---
name: openspec
description: Use when planning new features, starting spec-driven development workflows, or when the user mentions OpenSpec, SDD, or spec-driven development. Also triggers when user asks about feature specifications, change proposals, or wants to organize development workflow.
source: custom
updated: 2026-01-17
---

# OpenSpec - Spec-Driven Development

## Overview

OpenSpec 是一個規格驅動開發 (Spec-Driven Development, SDD) 框架，讓你在寫程式碼之前先寫規格，確保開發方向正確、減少返工。

## When to Use

- 規劃新功能時
- 需要記錄功能規格時
- 變更提案管理
- 團隊協作開發
- 使用者提到 "spec"、"規格"、"SDD" 時

## Quick Reference

### CLI 指令 (dash spec)

| 指令 | 功能 |
|------|------|
| `dash spec init .` | 初始化 OpenSpec |
| `dash spec list .` | 列出活動變更 |
| `dash spec view .` | 互動式儀表板 |
| `dash spec show . <name>` | 顯示變更詳情 |
| `dash spec validate . <name>` | 驗證規格格式 |
| `dash spec archive . <name>` | 歸檔完成的變更 |
| `dash spec status .` | 快速狀態總覽 |

### OpenSpec 原生指令

| 指令 | 功能 |
|------|------|
| `openspec init` | 初始化 |
| `openspec list` | 列出變更 |
| `openspec view` | 互動式儀表板 |
| `openspec show <name>` | 顯示詳情 |
| `openspec validate <name>` | 驗證格式 |
| `openspec archive <name>` | 歸檔變更 |

## SDD Workflow (五步循環)

```
1. SPEC (規格化)
   └── 定義功能規格 → openspec/specs/feature-name.md

2. PROPOSE (提案)
   └── 建立變更提案 → openspec/changes/change-name.md

3. IMPLEMENT (實作)
   └── 根據規格實作程式碼

4. VERIFY (驗證)
   └── 確認實作符合規格

5. ARCHIVE (歸檔)
   └── 完成後歸檔變更 → dash spec archive . change-name
```

## File Structure

```
project/
└── openspec/
    ├── specs/           # 功能規格
    │   ├── auth.md
    │   └── dashboard.md
    ├── changes/         # 活動變更提案
    │   └── add-login-feature.md
    └── archive/         # 已歸檔的變更
        └── 2026-01-setup-project.md
```

## Spec File Format

```markdown
---
title: 使用者認證
status: active
created: 2026-01-17
---

# 使用者認證

## 概述
實作使用者登入/登出功能。

## 功能需求
1. 支援 Email + 密碼登入
2. 支援 Google OAuth
3. 記住登入狀態

## API 規格
- POST /api/auth/login
- POST /api/auth/logout
- GET /api/auth/me

## 相關變更
- [[add-login-feature]]
```

## Change File Format

```markdown
---
title: 新增登入功能
type: feature
status: in-progress
spec: auth
created: 2026-01-17
---

# 新增登入功能

## 變更內容
實作 Email + 密碼登入功能。

## 影響範圍
- `src/auth/` 目錄
- `src/api/routes/auth.ts`

## 測試計畫
1. 單元測試: 登入邏輯
2. 整合測試: API 端點
3. E2E 測試: 登入流程

## Checklist
- [ ] 實作登入表單
- [ ] 實作 API 端點
- [ ] 撰寫測試
- [ ] 更新文件
```

## Best Practices

### 1. 先寫規格再寫程式碼
- 規格是開發的藍圖
- 減少返工和誤解
- 便於團隊溝通

### 2. 保持規格更新
- 實作後更新規格
- 記錄變更歷史
- 定期審視過期規格

### 3. 善用變更提案
- 每個功能一個變更
- 明確定義範圍
- 完成後及時歸檔

### 4. 使用 dash-devtools 整合
- `dash validate .` 自動驗證規格
- `dash health .` 顯示規格健康度
- `dash spec status .` 快速總覽

## Integration with dash-devtools

### 驗證整合
```bash
# 自動偵測 openspec/ 並驗證
dash validate .

# 檢查項目:
# - 目錄結構完整性
# - 規格檔案格式
# - 過期變更提醒
```

### 健康評分
```bash
# 顯示規格健康度
dash health .

# 評分項目:
# - 規格覆蓋率
# - 變更處理率
# - 格式正確性
```

## Installation

```bash
# 安裝 OpenSpec CLI
npm install -g @fission-ai/openspec@latest

# 驗證安裝
openspec --version

# 在專案中初始化
cd your-project
dash spec init .
```

## Troubleshooting

### openspec 未安裝
```bash
npm install -g @fission-ai/openspec@latest
```

### 規格格式錯誤
確保每個 .md 檔案都有 YAML frontmatter:
```markdown
---
title: 規格標題
status: active
---

# 內容...
```

### 過期變更警告
使用 `dash spec archive . <name>` 歸檔已完成的變更。

## Related Resources

- [OpenSpec GitHub](https://github.com/fission-ai/openspec)
- [Spec-Driven Development](https://spec-driven.dev)
- [dash-devtools](https://github.com/dash/dash-devtools)
