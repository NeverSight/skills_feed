---
name: lib-docs-generator
description: |
  Generates skills from library documentation automatically.
  Use when creating a skill from external documentation, fetching docs to local storage, or crawling documentation with curl.
  Can also be invoked directly with "ライブラリドキュメント", "/lib-docs-generator".
disable-model-invocation: true
argument-hint: "[url] [スキル名]"
allowed-tools: WebFetch, WebSearch, Read, Bash, Task, Write
---

# ライブラリドキュメント生成ガイド

## 概要

ライブラリのドキュメントからスキルを自動生成する。

**方針:**
1. llms.txtがあれば → そのまま使う（リンク先はクロールしない、llms-full.txtは無視）
2. llms.txtがなければ → 自前でllms.txt形式のファイルを自動生成
3. スキル発動時 → 都度WebFetchで詳細取得（常に最新）

## 実行フロー

```
┌─────────────────────────────────────────────────┐
│ Phase 1: URL解析                                 │
├─────────────────────────────────────────────────┤
│ 1. /llms.txt を確認                              │
│    ├── あり → curlでダウンロード                  │
│    │         （llms-full.txtは無視）              │
│    │         → Phase 4 へ                        │
│    └── なし → Phase 1.5 へ                       │
└─────────────────────────────────────────────────┘
                    ↓ (llms.txtなし)
┌─────────────────────────────────────────────────┐
│ Phase 1.5: URL収集 + ユーザー確認                │
├─────────────────────────────────────────────────┤
│ - サイトマップ/ナビゲーションからURL収集          │
│ - 収集URLリストを提示                            │
│ - ユーザー承認を待つ                             │
└─────────────────────────────────────────────────┘
                    ↓
┌─────────────────────────────────────────────────┐
│ Phase 2: ドキュメント収集                        │
├─────────────────────────────────────────────────┤
│ - 各URLをWebFetchで取得                          │
│ - タイトル + 概要 + コード例 + API情報を抽出     │
│ - カテゴリ分け                                   │
└─────────────────────────────────────────────────┘
                    ↓
┌─────────────────────────────────────────────────┐
│ Phase 3: docs.md生成                             │
├─────────────────────────────────────────────────┤
│ - template.mdを参照                              │
│ - 詳細形式で整形（概要+コード例+API情報）        │
│ - 品質チェックリストを確認                       │
│ - references/docs.mdとして保存                   │
└─────────────────────────────────────────────────┘
                    ↓
┌─────────────────────────────────────────────────┐
│ Phase 4: SKILL.md生成                            │
├─────────────────────────────────────────────────┤
│ - スキルディレクトリ作成                          │
│ - SKILL.md生成（WebFetch都度取得方式）           │
└─────────────────────────────────────────────────┘
```

---

## Phase 1: URL解析

### llms.txtの確認（最優先）

1. `/llms.txt` をWebFetchで確認
   ```
   WebFetch(url="https://example.com/llms.txt", prompt="Check if this is a valid llms.txt file")
   ```

2. **存在する場合:**
   - `docs.md` として保存（`llms.md` は作らない）
   ```bash
   mkdir -p .claude/skills/{library}/references
   curl -s https://example.com/llms.txt -o .claude/skills/{library}/references/docs.md
   ```
   - **Phase 4（ファイル生成）へ直接進む**（ユーザー確認不要）

3. **存在しない場合:**
   - Phase 1.5へ進む

### llms.txtの一般的なパターン

| サイト | llms.txt URL |
|--------|--------------|
| Expo | https://docs.expo.dev/llms.txt |
| Vercel | https://vercel.com/llms.txt |
| Tamagui | https://tamagui.dev/llms.txt |
| その他 | `/llms.txt` を確認 |

---

## Phase 1.5: URL収集 + ユーザー確認

**llms.txtがない場合のみ実行**

### 1. URL収集

**サイトマップ確認:**
```bash
curl -s https://example.com/sitemap.xml -o sitemap.xml
```

**ナビゲーション解析:**
```
WebFetch(
  url="https://example.com/docs",
  prompt="Extract all documentation page URLs from the navigation/sidebar. Return as a list of URLs."
)
```

### 2. ユーザー確認

収集したURLリストを提示し、承認を待つ:

```
以下のURLを収集対象として検出しました:

Getting Started:
- https://example.com/docs/getting-started
- https://example.com/docs/installation

API Reference:
- https://example.com/docs/api/hooks
- https://example.com/docs/api/components
...

このリストで収集を開始してよろしいですか？
除外したいURLや追加したいURLがあれば教えてください。
```

---

## Phase 2: ドキュメント収集

**目的:** 各URLから包括的な情報を抽出（概要、コード例、API情報を含む）

### 取得する情報

各URLから以下を抽出:

1. **基本情報**
   - ページタイトル
   - 概要（最初の1-2文）

2. **主要コンテンツ**
   - セクション見出し
   - 重要な説明文（箇条書き）

3. **コード例**
   - 基本的な使用例（最初のコードブロック）
   - インポート文

4. **API情報**（APIリファレンスページの場合）
   - 関数/コンポーネント名
   - パラメータと型
   - 戻り値

### WebFetchプロンプト（詳細版）

```
WebFetch(
  url="[URL]",
  prompt="Extract the following from this documentation page:
  1. Page title
  2. Brief description (1-2 sentences)
  3. Main content summary (key points as bullet list)
  4. First code example with imports
  5. API signatures if present (function name, parameters, return type)
  Format as structured markdown."
)
```

### 並列取得

ページ数が多い場合はTaskエージェントを並列起動:

```
Task(subagent_type="Explore", prompt="以下のURLから詳細情報を抽出: [URLリストA]")
Task(subagent_type="Explore", prompt="以下のURLから詳細情報を抽出: [URLリストB]")
```

### カテゴリ分け

URLパターンで自動分類:

| パターン | カテゴリ |
|----------|----------|
| `/getting-started`, `/quickstart`, `/intro` | Getting Started |
| `/installation`, `/setup` | Getting Started |
| `/api`, `/reference` | API Reference |
| `/concepts`, `/fundamentals` | Core Concepts |
| `/guides`, `/how-to` | Guides |
| `/examples`, `/tutorials` | Examples |
| `/advanced`, `/configuration` | Optional |

---

## Phase 3: docs.md生成

### 生成手順

1. **収集情報の整理**
   - Phase 2で取得した全情報を整理
   - 重複・無効URLを除外
   - 情報の欠落がないか確認

2. **カテゴリ分類**
   - URLパターンと内容に基づいて分類
   - Getting Started / Core Concepts / API Reference / Guides / Examples

3. **構造化**
   - 各ページごとにサブセクションを作成
   - 概要 → 主要ポイント → コード例 → API情報 の順で記載

4. **品質チェック**
   - 下記チェックリストを確認

5. **保存**
   - `references/docs.md` として保存

### template.mdを参照

[templates/docs.md](templates/docs.md) を参照して、詳細な出力形式で整形する。

### 出力形式（詳細版）

```markdown
# {Library}

> {ライブラリの概要を1-2文で}

## Getting Started

### Installation
- **URL**: https://...
- **概要**: インストール方法
- **手順**:
  - npm install {package}
  - 設定ファイルの作成

### Quick Start
- **URL**: https://...
- **概要**: 基本的な使い方
- **コード例**:
  ```tsx
  import { useQuery } from '@tanstack/react-query'

  function Example() {
    const { data } = useQuery({ queryKey: ['todos'], queryFn: fetchTodos })
  }
  ```

## API Reference

### useQuery
- **URL**: https://...
- **概要**: データ取得用フック
- **シグネチャ**: `useQuery(options: UseQueryOptions): UseQueryResult`
- **主要パラメータ**:
  - `queryKey`: クエリの一意識別子
  - `queryFn`: データ取得関数
- **コード例**:
  ```tsx
  const { data, isLoading, error } = useQuery({
    queryKey: ['user', userId],
    queryFn: () => fetchUser(userId),
  })
  ```
```

### 品質チェックリスト

生成後、以下を確認:

- [ ] **必須セクション**: Library名、Description、Getting Started が含まれている
- [ ] **URL検証**: 全URLがアクセス可能
- [ ] **コード例**: 主要機能にコード例がある
- [ ] **API情報**: API Referenceページにはシグネチャがある
- [ ] **重複なし**: 同じ内容が複数回出現していない
- [ ] **網羅性**: 主要なドキュメントページが含まれている

### 良い例・悪い例

**良い例:**
```markdown
### useQuery
- **URL**: https://tanstack.com/query/latest/docs/react/reference/useQuery
- **概要**: サーバーからのデータ取得・キャッシュ・再検証を行うフック
- **シグネチャ**: `useQuery(options): UseQueryResult`
- **主要パラメータ**:
  - `queryKey: QueryKey` - クエリの一意識別子
  - `queryFn: QueryFunction` - データ取得関数
- **コード例**:
  ```tsx
  const { data, isLoading } = useQuery({
    queryKey: ['todos'],
    queryFn: fetchTodos,
  })
  ```
```

**悪い例:**
```markdown
- [useQuery](URL): フック
```

### 保存

```bash
# references/docs.md として保存
Write to: .claude/skills/{library}/references/docs.md
```

---

## Phase 4: SKILL.md生成

### ファイル構成

```
{library}/
├── SKILL.md              # メインスキルファイル
└── references/
    └── docs.md           # llms.txt形式（リンク集 + 概要）
```

### SKILL.mdテンプレート

[templates/skill.md](templates/skill.md) を参照して、SKILL.mdを生成する。

プレースホルダーを実際の値に置き換える:
- `{library}`: スキル名（小文字、ハイフン区切り）
- `{Library}`: ライブラリの表示名
- `{package-name}`: メインパッケージ名
- `{日本語キーワード}`: 日本語での呼び出しキーワード

### descriptionの書き方

**ルール:**
- 1024文字以内
- 英語（最終行の日本語キーワード部分を除く）
- 三人称・動詞で始める

**トリガー条件を含める:**
1. import文のパターン: `imports "package-name"`
2. ワイルドカード: `any "@tanstack/*" packages`
3. ユーザーの質問パターン: `asks about {Library}`
4. 関連キーワード: 主要なAPI名、関数名、コンポーネント名

**良い例:**
```yaml
description: |
  Provides documentation for TanStack Query (React Query).
  Use when working with code that imports "useQuery", "useMutation", "@tanstack/react-query", or any "@tanstack/query-*" packages.
  Use when the user asks about data fetching, caching, or shows code with React Query hooks.
  Can also be invoked directly with "React Query", "TanStack Query", "データフェッチ".
```

---

## 生成されるスキルの動作

```
スキル発動時:
  1. references/docs.md を読む
  2. 質問に関連するセクション/URLを特定
  3. WebFetchで該当URLの詳細を取得
  4. 回答を生成
```

**メリット:**
- スキル生成が高速（全文クロール不要）
- 常に最新情報（都度Fetch）
- ストレージ節約
- llms.txtありなしで同じ使い勝手

---

## クロールのベストプラクティス

技術的な詳細は [crawling-guide.md](references/crawling-guide.md) を参照。

---

## トラブルシューティング

### SPAサイトで取得できない

- 静的なドキュメントページを探す
- GitHubリポジトリのドキュメントを確認
- 代替ドキュメントソース（MDN、DevDocs等）を検討

### 構造が複雑

- 手動でdocs.mdを調整
- 目次を追加して参照しやすくする
