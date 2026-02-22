---
name: zotero
description: >
  Zotero ローカル API + REST API (Web API v3) 連携スキル。DOI からの文献一括インポート、コレクション管理、アイテム検索・一覧表示を行う。
  REST API 経由でコレクション作成・アイテム CRUD・タグ管理・添付ファイルアップロード・グループライブラリ操作も可能。
  Use when: (1) DOI リストから Zotero に文献を登録する, (2) Zotero のコレクション一覧・アイテム一覧を取得する,
  (3) BibTeX/RIS データを Zotero にインポートする, (4) CrossRef API で文献の DOI を検索する,
  (5) REST API でコレクション作成・アイテム追加・タグ管理を行う, (6) グループライブラリを操作する。
  Triggers: "zotero", "文献登録", "DOI インポート", "コレクション", "論文追加", "文献管理"
---

# Zotero API Skill

Zotero のローカル HTTP サーバー（`localhost:23119`）および REST API（`api.zotero.org`）経由で文献管理操作を行う。

## 前提条件

### ローカル API（Zotero 起動中のみ）

Zotero が起動中で、以下の設定が有効であること：
- Zotero > 環境設定 > 詳細 > 「Allow other applications on this computer to communicate with Zotero」にチェック

接続確認:
```bash
curl -s http://localhost:23119/connector/ping
```

### REST API（クラウド操作）

環境変数が設定されていること:
- `ZOTERO_API_KEY`: API キー（https://www.zotero.org/settings/keys で作成）
- `ZOTERO_USER_ID`: ユーザー ID

接続確認:
```bash
curl -s -H "Zotero-API-Key: $ZOTERO_API_KEY" "https://api.zotero.org/keys/current"
```

## コマンド

### 1. DOI 一括インポート (`/zotero import`)

```
/zotero import <DOI1> <DOI2> ...
/zotero import --file <doi_list.txt>
/zotero import --collection "コレクション名"
```

インポートスクリプト:
```bash
bash ~/.claude/skills/zotero/scripts/zotero_import.sh --dois "10.1038/xxx,10.2196/yyy" [--collection "名前"]
```

処理フロー:
1. Zotero 起動確認（`/connector/ping`）
2. 対象コレクション特定（指定なければ現在選択中を使用）
3. 各 DOI → `doi.org` から BibTeX 取得（失敗時 CrossRef フォールバック）
4. `/connector/import?session=<unique_id>` に POST
5. 結果サマリー表示

### 2. 手動 BibTeX インポート (`/zotero bibtex`)

DOI のない文献用。BibTeX ファイルを直接インポート:
```bash
bash ~/.claude/skills/zotero/scripts/zotero_import.sh --bibtex /path/to/file.bib
```

DOI 不明時は CrossRef API で検索:
```bash
curl -s "https://api.crossref.org/works?query.bibliographic=著者名+キーワード&rows=5"
```

### 3. コレクション一覧 (`/zotero collections`)

```bash
curl -s http://localhost:23119/api/users/0/collections | python3 -c "
import json, sys
for c in json.load(sys.stdin):
    d = c['data']
    print(f\"{d['key']}  {d['name']}\")"
```

### 4. アイテム一覧 (`/zotero list`)

```
/zotero list                          # 現在選択中コレクション
/zotero list --collection "名前"      # 指定コレクション
```

### 5. アイテム検索 (`/zotero search`)

```
/zotero search "AI psychosis"
```

## REST API 操作

### コレクション作成

```bash
curl -s -X POST \
  -H "Zotero-API-Key: $ZOTERO_API_KEY" \
  -H "Content-Type: application/json" \
  "https://api.zotero.org/users/$ZOTERO_USER_ID/collections" \
  -d '[{"name": "コレクション名"}]'
```

### コレクション更新

```bash
curl -s -X PUT \
  -H "Zotero-API-Key: $ZOTERO_API_KEY" \
  -H "Content-Type: application/json" \
  -H "If-Unmodified-Since-Version: $VERSION" \
  "https://api.zotero.org/users/$ZOTERO_USER_ID/collections/COLLECTION_KEY" \
  -d '{"name": "新しい名前"}'
```

### アイテム作成（最大50件/リクエスト）

```bash
curl -s -X POST \
  -H "Zotero-API-Key: $ZOTERO_API_KEY" \
  -H "Content-Type: application/json" \
  "https://api.zotero.org/users/$ZOTERO_USER_ID/items" \
  -d '[{
    "itemType": "journalArticle",
    "title": "タイトル",
    "creators": [{"creatorType": "author", "firstName": "名", "lastName": "姓"}],
    "collections": ["COLLECTION_KEY"],
    "tags": [{"tag": "タグ名"}]
  }]'
```

### アイテム部分更新（PATCH）

```bash
curl -s -X PATCH \
  -H "Zotero-API-Key: $ZOTERO_API_KEY" \
  -H "Content-Type: application/json" \
  -H "If-Unmodified-Since-Version: $VERSION" \
  "https://api.zotero.org/users/$ZOTERO_USER_ID/items/ITEM_KEY" \
  -d '{"tags": [{"tag": "new-tag"}]}'
```

### アイテム削除

```bash
curl -s -X DELETE \
  -H "Zotero-API-Key: $ZOTERO_API_KEY" \
  -H "If-Unmodified-Since-Version: $VERSION" \
  "https://api.zotero.org/users/$ZOTERO_USER_ID/items/ITEM_KEY"
```

### タグ一括削除

```bash
curl -s -X DELETE \
  -H "Zotero-API-Key: $ZOTERO_API_KEY" \
  -H "If-Unmodified-Since-Version: $VERSION" \
  "https://api.zotero.org/users/$ZOTERO_USER_ID/tags?tag=tag1+||+tag2"
```

### グループライブラリ

すべてのエンドポイントは `/users/<userID>` を `/groups/<groupID>` に置き換えるだけ。

```bash
# 所属グループ一覧
curl -s -H "Zotero-API-Key: $ZOTERO_API_KEY" \
  "https://api.zotero.org/users/$ZOTERO_USER_ID/groups"
```

### 検索（REST API）

```bash
# キーワード検索
curl -s -H "Zotero-API-Key: $ZOTERO_API_KEY" \
  "https://api.zotero.org/users/$ZOTERO_USER_ID/items?q=keyword&qmode=titleCreatorYear"

# タグフィルタ（AND: 複数 tag、OR: || 区切り、NOT: - 接頭辞）
curl -s -H "Zotero-API-Key: $ZOTERO_API_KEY" \
  "https://api.zotero.org/users/$ZOTERO_USER_ID/items?tag=AI&tag=review"
```

## API 概要

### ローカル API

| エンドポイント | メソッド | 用途 |
|--------------|---------|------|
| `/connector/ping` | GET/POST | 起動確認 |
| `/connector/import?session=ID` | POST | BibTeX/RIS インポート |
| `/connector/getSelectedCollection` | POST | 選択中コレクション |
| `/api/users/0/collections` | GET | コレクション一覧 |
| `/api/users/0/collections/:key/items` | GET | アイテム一覧 |
| `/api/users/0/items` | GET | 全アイテム |

### REST API (api.zotero.org)

| エンドポイント | メソッド | 用途 |
|--------------|---------|------|
| `/users/<id>/collections` | GET/POST | コレクション一覧/作成 |
| `/users/<id>/collections/<key>` | PUT/DELETE | コレクション更新/削除 |
| `/users/<id>/items` | GET/POST | アイテム一覧/作成（最大50件） |
| `/users/<id>/items/<key>` | PUT/PATCH/DELETE | アイテム更新/削除 |
| `/users/<id>/tags` | GET | タグ一覧 |
| `/users/<id>/tags?tag=...` | DELETE | タグ一括削除 |
| `/users/<id>/searches` | GET/POST | 保存済み検索 |
| `/users/<id>/items/<key>/file` | GET/POST/PATCH | 添付ファイル |
| `/users/<id>/groups` | GET | グループ一覧 |
| `/groups/<id>/...` | 各種 | グループ操作 |

詳細: [references/api-endpoints.md](references/api-endpoints.md)

## 重要な注意点

### ローカル API
- **Local API (`/api/...`)** は GET のみ（読み取り専用）
- **Connector API (`/connector/...`)** は POST で読み書き可能
- `/connector/import` の `session` パラメータは**毎回ユニーク**にする（重複で 409 エラー）
- BibTeX にシェル特殊文字がある場合は `--data-binary @file.bib` でファイル経由送信
- インポート先は **Zotero UI で選択中のコレクション** に保存される

### REST API
- 認証: `Zotero-API-Key: <key>` ヘッダー（推奨）
- 更新/削除時は `If-Unmodified-Since-Version: <version>` が必須（未指定 → 428）
- バッチ上限: 最大 50 件/リクエスト
- レートリミット: `Backoff` / `429 + Retry-After` ベース
- 重複送信防止: `Zotero-Write-Token: <token>` ヘッダー
