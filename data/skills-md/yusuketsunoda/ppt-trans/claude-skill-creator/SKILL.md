---
name: claude-skill-creator
description: Provides guidance for creating effective Claude Code skills with proper YAML frontmatter, directory structure, and best practices. Activates when user mentions "create skill", "new skill", "スキル作成", "SKILL.md", "skill development".
allowed-tools: Read, Grep, Glob, Edit, Write
user-invocable: true
model: haiku
---

# Claude Skill Creator Guide

スキル作成のガイド。Claude Codeの機能を拡張するスキルを効果的に作成する方法を説明。

## When to Use This Skill

- 新規スキルを作成する時
- 既存スキルを更新・改善する時
- スキルが正しく発動しない問題を調査する時
- ドキュメントをスキル形式に変換する時

## What Are Skills?

スキルはClaudeの機能を拡張するフォルダ構造。**モデル自動発見**—Claudeがリクエストに基づいて自動的に使用を判断する（スラッシュコマンドとは異なり明示的な呼び出し不要）。

## Directory Structure

```
Personal:  ~/.claude/skills/skill-name/SKILL.md
Project:   .claude/skills/skill-name/SKILL.md
Plugin:    パッケージに同梱
```

## Creating a New Skill

### Step 1: ディレクトリ作成

```bash
mkdir -p .claude/skills/my-skill-name
```

### Step 2: SKILL.md作成（YAML frontmatter必須）

```yaml
---
name: skill-identifier          # 必須: 小文字/数字/ハイフンのみ、64文字以内
description: 何をするか + いつ使うか  # 必須: 1024文字以内、トリガーキーワード含む
allowed-tools: Read, Grep, Edit  # オプション: ツール制限
---
```

**name規則**:
- 小文字、数字、ハイフンのみ
- 64文字以内
- 例: `api-docs-writer`, `db-migration-helper`

**description規則**:
- 「何をするか」+「いつ使うか」を両方含める
- トリガーキーワードを含める
- 1024文字以内

```yaml
# ✅ GOOD
description: E2Eテストの作成・デバッグ・失敗修正を支援。Playwrightテスト失敗時、新規テスト作成時に使用。

# ❌ BAD
description: テストを手伝う
```

### Step 3: 本文の推奨構造

```markdown
# Skill Title

概要（1-2文）

## When to Use This Skill

- シナリオ1
- シナリオ2

## Instructions

1. **Step 1**: 最初にやること
2. **Step 2**: 次にやること
3. **Step 3**: 最後にやること

## Examples

### Example 1: [シナリオ]
[コード例]

## Troubleshooting

**Issue**: 問題
**Solution**: 解決方法

## AI Assistant Instructions

このスキルが有効化された時:
1. まず○○を確認
2. 次に○○を実行

Always:
- 常に○○する

Never:
- ○○しない
```

## Optional: ツール制限

```yaml
allowed-tools: Read, Grep, Glob  # 読み取り専用
```

## Optional: 補助ファイル

```
my-skill-name/
├── SKILL.md              # メイン（必須、500行以下）
├── reference.md          # 詳細リファレンス（必要時読み込み）
└── templates/            # テンプレート
```

SKILL.mdから参照:
```markdown
詳細は [reference.md](reference.md) を参照。
```

## Best Practices

### 1. スキルは1機能に絞る

```yaml
# ✅ DO
- api-docs-writer: API文書生成
- test-strategy: テスト実装

# ❌ DON'T
- developer-helper: 何でも（曖昧）
```

### 2. トリガーキーワードを含める

```yaml
# ✅ GOOD
description: OpenAPI/Swagger文書をExpress/FastAPIから生成。API文書作成時に使用。

# ❌ BAD
description: API文書を手伝う
```

### 3. 具体例を提供

ユーザーもClaudeも例から学ぶ。実際のコード例を含める。

### 4. AI Assistant Instructionsを明示

```markdown
## AI Assistant Instructions

When this skill is activated:
1. まずコードベースを分析
2. 必要なら質問
3. 初期バージョンを生成

Always:
- TypeScriptで型安全に
- エラーハンドリングを含める

Never:
- 検証をスキップしない
```

### 5. コンテキストウィンドウを意識

- SKILL.mdは500行以下
- Claudeの基礎知識は説明不要
- 詳細は参照ファイルに分離

### 6. Progressive Disclosure

```
my-skill-name/
├── SKILL.md          # コア（< 500行）
├── reference.md      # 詳細（必要時のみ読込）
└── examples.md       # 拡張例（必要時のみ読込）
```

## Common Pattern: Code Generation

```yaml
---
name: component-generator
description: React/Vue/Angularコンポーネントを生成。新規コンポーネント作成時に使用。
---

# Component Generator

## Instructions

1. コンポーネント種別を確認（React/Vue/Angular）
2. 名前とpropsを取得
3. 生成: コンポーネント + テスト + Storybook
4. プロジェクト規約に従う
```

## Troubleshooting

### スキルが発動しない

| 原因 | 解決 |
|------|------|
| トリガーキーワード不足 | descriptionに具体的キーワード追加 |
| name形式が不正 | 小文字/数字/ハイフンのみに修正 |
| YAML不正 | `---` デリミタ確認、タブ→スペース |
| ファイル名が違う | `SKILL.md` に統一（大文字小文字注意） |

### 意図しないタイミングで発動

| 原因 | 解決 |
|------|------|
| descriptionが広すぎる | より具体的なキーワードに変更 |
| 他スキルとキーワード重複 | ユニークなキーワードを使用 |

### 指示に従わない

| 原因 | 解決 |
|------|------|
| 指示が曖昧 | 番号付きステップで明示化 |
| AI Instructions欠如 | セクション追加 |

## Team Sharing

```bash
# プロジェクトスキル
git add .claude/skills/skill-name/
git commit -m "feat: add [skill-name] skill"
git push
# チームメンバーは git pull で取得
```

## Quick Checklist

- [ ] ディレクトリ: `.claude/skills/skill-name/`
- [ ] ファイル名: `SKILL.md`（大文字小文字注意）
- [ ] YAML frontmatter: `---` で囲む
- [ ] `name`: 小文字/ハイフン、64文字以内
- [ ] `description`: 何 + いつ、トリガーキーワード含む
- [ ] "When to Use This Skill" セクション
- [ ] ステップバイステップ Instructions
- [ ] 具体的な Examples
- [ ] AI Assistant Instructions
- [ ] 500行以下

## AI Assistant Instructions

このスキルが有効化された時:

1. **要件確認**: 新規作成か更新かを確認
2. **テンプレート提供**: 上記の推奨構造に従う
3. **検証**: チェックリストで確認

Always:
- description に「何をするか」+「いつ使うか」を含める
- AI Assistant Instructionsセクションを含める
- 500行以下を維持する

Never:
- nameにアンダースコアやスペースを使用しない
- descriptionを曖昧にしない
- 基礎的なプログラミング概念を説明しない（Claudeは知っている）
