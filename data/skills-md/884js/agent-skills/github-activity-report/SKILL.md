---
name: github-activity-report
description: |
  Generate a portfolio report of your GitHub activity (PRs) for job applications.
  Use when the user asks about their GitHub contributions, activity history, or wants to see what they've built.
  Outputs a Markdown file with all commits sorted by date.
  Can also be invoked with "GitHub活動", "コミット履歴", "作ったもの一覧", "ポートフォリオ".
---

# GitHub Activity Portfolio Generator

過去1年間のGitHub PR活動を分析し、ポートフォリオ形式のMarkdownファイルを生成します。

## 前提条件

- `gh` CLI がインストールされ、認証済みであること
- `jq` がインストールされていること

## ワークフロー

### Step 1: Organization選択

1. ユーザーの所属Organizationを取得:
   ```bash
   gh api /user/memberships/orgs --jq '.[].organization.login'
   ```

2. ユーザーに選択肢を提示（AskUserQuestionツールを使用）:
   - 取得した各Organization
   - 個人リポジトリ（ユーザー名）

### Step 2: PR取得

選択されたOrganizationのPR詳細を取得:

```bash
bash {skill_dir}/scripts/fetch_pr_details.sh <org_name>
```

出力: `{skill_dir}/tests/tmp/pr_details_<org>_<date>.json`

### Step 3: 分析・分類

JSONデータを分析し、以下の観点で主要プロジェクトを特定:

1. **PRタイトルのパターン**
   - `[プロジェクト名]`、`[機能名]` などのプレフィックス
   - 共通キーワードのグルーピング

2. **変更ファイルのパス**
   - `features/xxx/`、`components/xxx/` などのディレクトリ構造
   - 関連ファイルの共通パターン

3. **コード規模**
   - additions/deletions の合計
   - 大規模な変更を含むPRの特定

4. **時期的なまとまり**
   - 同時期に集中している関連PR

### Step 4: ポートフォリオ生成

以下の形式でMarkdownファイル `portfolio-<org>.md` を生成:

```markdown
# <org> での実績 (YYYY-MM 〜 YYYY-MM)

**<プロジェクト概要>**

## Summary

| 期間 | PR数 | 追加行数 | 削除行数 |
|------|------|----------|----------|
| YYYY-MM 〜 YYYY-MM (Nヶ月) | **XXX件** | **XX,XXX行** | **XX,XXX行** |

<担当領域の概要>

---

## 主要プロジェクト

### 1. <絵文字> <プロジェクト名>

<プロジェクトの説明>

#### 実装した機能

| 機能 | 時期 | 概要 | コード規模 |
|------|------|------|-----------|
| **機能名** | YYYY-MM | 概要説明 | +XXX/-YYY |

#### 技術的なポイント
- ポイント1
- ポイント2

---

### 2. <別プロジェクト>
...

---

## 技術スタック

| カテゴリ | 技術 |
|----------|------|
| **Frontend** | ... |
| **Backend** | ... |

---

## 月別アクティビティ

| 月 | PR数 | 追加行数 | 主なトピック |
|----|------|----------|--------------|
| YYYY-MM | XX | +X,XXX | ... |

---

## 代表的なPR（規模順）

1. **PR名** (+XXX/-YYY) - 概要
2. ...

---

## まとめ

<全体のサマリー>
```

## 出力ファイル

- `{skill_dir}/tests/tmp/pr_details_<org>_<date>.json` - PR詳細データ
- `portfolio-<org>.md` - ポートフォリオMarkdown（カレントディレクトリ）

## 注意事項

- プライベートリポジトリのPR情報も取得されます
- 出力ファイルを共有する際は、機密情報に注意してください
- PRの本文（body）に機密情報が含まれる場合があります
- リリースPR（Release始まり）とRevertPRは自動的に除外されます
