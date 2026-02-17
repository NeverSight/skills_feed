---
name: suggest-agent-rules
description: Suggest agent rules analyzing the session history and the current repository.
---

# Suggest Agent Rules

あなたは「このリポジトリ専用のCoding Agentルール」を設計するテックリードです。
以下の情報を根拠に、エージェントが将来の作業で迷わず高品質に動けるよう、実務的で検証可能なルールを提案してください。

## セッション情報へのアクセス

### セッションファイルの場所

| Agent | Path | File Format |
|-------|------|-------------|
| Claude Code | `~/.claude/projects/<project-path-encoded>/` | `<UUID>.jsonl` |
| Codex CLI | `~/.codex/sessions/YYYY/MM/DD/` | `rollout-<datetime>-<UUID>.jsonl` |

**プロジェクトパスのエンコード**: `/Users/username/projects/myapp` → `-Users-username-projects-myapp`

### 提供ツール

このスキルでは以下のツールを利用できます（`tools/`ディレクトリ参照）:

1. **list-sessions.sh** - セッション一覧を取得
   ```bash
   ./tools/list-sessions.sh -p /path/to/project -n 10
   ```

2. **analyze-session.sh** - 単一セッションを詳細分析
   ```bash
   ./tools/analyze-session.sh <session-file> --all
   ```
   オプション: `--summary`, `--user-messages`, `--tools`, `--errors`, `--preferences`

3. **extract-patterns.sh** - 複数セッションからパターンを抽出
   ```bash
   ./tools/extract-patterns.sh -p /path/to/project -n 5
   ```

### セッションデータ構造の詳細

詳細は `references/session-structure.md` を参照。主要なポイント:

- **Claude Code**: `parentUuid`/`uuid`で会話ツリーを構築、`type`フィールドで`user`/`assistant`を判別
- **message.content**: `thinking`, `text`, `tool_use`, `tool_result`のブロックを含む
- **サブエージェント**: `<session-uuid>/subagents/agent-<id>.jsonl`に保存、`isSidechain: true`

### セッション解析で抽出すべき情報

1. **ユーザーの明示的な指示・好み** - 「必ず〜」「〜しないで」などのパターン
2. **繰り返し発生した手戻り** - エラー→修正の連続パターン
3. **よく使用されるツールとファイル** - 作業パターンの把握
4. **エラーパターン** - tool_resultでのエラー応答

## 利用できる情報源（優先順）
1. Agentのセッション履歴（直近の指示・好み・繰り返し発生した手戻り・決定事項）
   - 上記ツールを使用してセッションデータを分析
2. 現在のリポジトリの内容（README/CONTRIBUTING/ディレクトリ構造/設定ファイル/CI設定/テスト構成）
3. ローカルGit履歴（コミットメッセージ規約・変更頻度の高い領域・リバート/ホットフィックス傾向）
4. GitHub履歴（PR/Issue/レビューコメントの傾向、指摘が多い論点、CI落ちパターン）
   - `gh` が使えるなら `gh pr list/view`, `gh issue list/view` 等を用いて良い
   - 使えない場合はローカルで取れる範囲（git log等）で推定し、不確実性を明示する

## ゴール
- “一般論”ではなく **このリポジトリ固有の** ルールにする
- ルールは「守れば成果が上がる」ものだけに絞り、過剰に増やさない
- すべてのルールに **根拠** と **確認方法（verify）** を付ける
- 不明点は断定せず、最小の追加調査で確かめる手順を添える

---

## 作業手順（必ずこの順で）
### 1) リポジトリ概観の把握
- 主要言語/フレームワーク/ビルドツール/パッケージマネージャを推定
- ルート直下、`README` / `CONTRIBUTING` / `CODEOWNERS` / `Makefile` / `package.json` / `pyproject.toml` / `go.mod` / `Cargo.toml` / `.github/workflows` 等を優先して確認
- 既に「ルール」「コーディング規約」「レビュー観点」があるならそれを最優先で尊重（重複ルールは作らない）

### 2) 失敗パターン・手戻りパターンの抽出
- セッション履歴：繰り返し注意された点、好み（例：テスト先行、差分最小、ログ方針、命名規約）を抽出
- Git/PR/レビュー：同じ種類の指摘が複数回出る領域を優先（lint、境界条件、例外、型、N+1、依存更新、Migration等）

### 3) “エージェント向け”に翻訳してルール化
- 人間向け規約を、エージェントが実行できる行動（Do/Don’t）へ落とす
- ルールは次のいずれかに分類する：
  - 安全（破壊的操作・秘密情報・本番影響）
  - 変更方針（差分最小、リファクタ範囲、互換性、移行）
  - 品質（テスト、静的解析、型、例外、境界条件）
  - リポジトリ慣習（命名、ディレクトリ、レイヤー、依存、ログ）
  - PR運用（粒度、説明、チェックリスト、レビュー対応）

### 4) ルールの優先度付け
- 最重要（Must）: 破ると事故/大幅手戻りになる
- 重要（Should）: 品質や速度に効く
- 任意（Could）: 余裕がある時に

---

## 出力フォーマット（厳守）
以下の順番でMarkdownを出力してください。

### A. リポジトリの前提（短く）
- 推定スタック / 実行すべき基本コマンド（分かる範囲）
- CIの主要チェック（分かる範囲）
- 不明点（あれば）

### B. 観測された傾向（箇条書き・最大10個）
- セッション履歴由来 / Git由来 / PRレビュー由来 を区別して書く

### C. 提案ルール（最大12個、優先度順）
各ルールは必ず次のテンプレで書く：

- **[Priority: Must/Should/Could] ルール名（短く）**
  - **Rule:**（エージェントが取るべき行動を命令形で。曖昧語を避ける）
  - **Why (evidence):**（観測された根拠。ファイル名/設定/レビュー傾向など。推測なら推測と明記）
  - **Verify:**（実行コマンド、見るべきファイル、CIで確認、再現手順のいずれか）
  - **Scope:**（常に/特定条件のとき。例：DB変更時、API変更時、依存更新時）
  - **Confidence:**（High/Medium/Low）

### D. “貼り付け用”の最終ルール本文
- `.claude/agent-rules.md` 等に貼れる体裁で、Cのルールを簡潔版に再掲する
- 余計な解説は入れず、Do/Don’t中心にする

---

## 制約・禁止事項
- リポジトリで確認できないコマンドや規約を断定しない（例：存在しない `npm test` を推奨しない）
- 破壊的操作（reset/force push/大量削除/マイグレーション適用等）は “事前確認ルール” を必ず含める
- 秘密情報（鍵、トークン、顧客情報）を出力しない。ログや設定値を貼る場合はマスキングする
- ルール数は増やしすぎない（最大12）。必要なら「次点ルール（Optional）」として別枠にする

---

## Usage
このSkillは次のタイミングで使う：
- 初回オンボーディング時
- レビュー指摘が増えたとき
- リファクタや大規模移行の前
- CI/運用ルールが変わったとき

実行後、出力の「貼り付け用ルール本文」をリポジトリの所定ファイルに反映して運用する。
