---
name: review
description: >-
  Performs comprehensive PR code review from 5 perspectives (quality/performance/tests/docs/security)
  in parallel, providing Blockers/Suggestions/Nice-to-have and merge decision.
  Args: /review [owner/repo] [pr-number] [--focus all|security|perf|qa|docs|types]
  Activates when user mentions "review", "PR確認", "コードレビュー", "マージ判定".
allowed-tools: Bash, Grep, Glob, Read, Task
user-invocable: true
context: fork
agent: general-purpose
---

# /review Skill (PR Comprehensive Review)

## Purpose
Next.js 16 + Supabase + Stripe + Playwright コードベースのPRを包括レビューし、
マージ可否を判定する。

## Invocation
```
/review [owner/repo] [pr-number] [--focus <aspect>]
```

### 引数

| 引数 | 必須 | 説明 |
|------|------|------|
| `owner/repo` | Yes | GitHubリポジトリ（例: `my-org/ppt-trans`）|
| `pr-number` | Yes | PRの番号 |
| `--focus` | No | 実行するレビュー観点を限定（デフォルト: `all`）|

### --focus オプション

| 値 | 実行されるエージェント | ユースケース |
|----|----------------------|-------------|
| `all` | 全5エージェント | 通常のPRレビュー（デフォルト） |
| `security` | security-code-reviewer | 認証/認可/Stripe変更時 |
| `perf` | performance-reviewer | N+1/キャッシュ/PPTX処理変更時 |
| `qa` | test-coverage-reviewer | テストファイル変更時 |
| `docs` | documentation-accuracy-reviewer | env/README/CLAUDE.md変更時 |
| `types` | code-quality-reviewer | 型定義/API変更時 |

### 例
```bash
# 全観点レビュー（デフォルト）
/review my-org/ppt-trans 123

# セキュリティのみ
/review my-org/ppt-trans 123 --focus security

# パフォーマンスのみ
/review my-org/ppt-trans 123 --focus perf
```

## Output Contract（必須出力）
1. Summary（2-4行）
2. Blockers（各: why + where + fix）
3. Suggestions
4. Nice-to-have
5. Merge decision:
   - ✅ Merge
   - ⚠️ Merge with follow-ups（follow-up一覧）
   - ❌ Needs changes（blockers一覧）

## Guardrails
- 秘密情報（env値、keys、tokens）をログ/コメントに出さない
- Blockersは「実際にバグ/脆弱性/データ損失/課金エラー/flaky CI」を引き起こすものに限定
- 大規模リファクタはfollow-up issueとして提案

---

## Workflow

### Phase 0: 事前情報収集

1. **プロジェクトルール読み込み**
   - `CLAUDE.md` を Read
   - 抽出項目:
     - スタック（Next.js 16, React 19, Supabase, Stripe, Playwright）
     - コーディング規約（any禁止、Server Actions優先、Schema-First）
     - セキュリティ方針（RLS、Rate Limiting、CSRF）
     - テスト方針（UNIFIED_TEST_CONFIG、MVP範囲）

2. **PR情報取得**
   ```bash
   gh pr view <PR_NUMBER> --repo <REPO> --json title,body,author,labels,files,additions,deletions,url
   gh pr diff <PR_NUMBER> --repo <REPO>
   ```

3. **PR要約作成**
   - 変更目的（1-2行）
   - 影響範囲（UI/API/DB/Billing/Auth/PPTX/E2E）
   - リスクフラグ（スキーマ変更、認証変更、課金変更、ファイル処理）

### Phase 1: エージェント並列実行

**--focus オプションに応じてエージェントを選択**:

| --focus | 実行エージェント |
|---------|------------------|
| `all`（デフォルト）| 全5エージェント並列 |
| `security` | security-code-reviewer のみ |
| `perf` | performance-reviewer のみ |
| `qa` | test-coverage-reviewer のみ |
| `docs` | documentation-accuracy-reviewer のみ |
| `types` | code-quality-reviewer のみ |

**全エージェント一覧**:

| エージェント | subagent_type | 責務 |
|-------------|---------------|------|
| code-quality-reviewer | code-quality-reviewer | コード品質・設計・型安全 |
| performance-reviewer | performance-reviewer | パフォーマンス・N+1・キャッシュ |
| security-code-reviewer | security-code-reviewer | RLS・Webhook・IDOR・XSS |
| test-coverage-reviewer | test-coverage-reviewer | Playwright決定論・モック・カバレッジ |
| documentation-accuracy-reviewer | documentation-accuracy-reviewer | env・手順・文言の整合性 |

**実装時の注意**:
- `--focus all` または未指定の場合、全5エージェントを **並列で** Task実行
- `--focus <aspect>` 指定時、該当エージェントのみ実行

**各エージェントへのプロンプト共通部分:**
```
## コンテキスト
- スタック: Next.js 16 + React 19 + TypeScript + Supabase + Stripe + Playwright
- プロジェクトルール: [CLAUDE.md要約]
- PR要約: [Phase 0の要約]
- 変更ファイル: [ファイル一覧]

## 重点チェック（ppt-trans固有）
- Next.js 16: params: Promise<T> の正しい実装
- Server Actions vs API Routes の使い分け
- Schema-First開発（openapi.yaml先行）
- Supabase RLS、snake_case型、型再生成
- E2E: UNIFIED_TEST_CONFIG参照、ハードコード禁止
```

### Phase 2: 自動チェック（推奨）

実行可能なら以下を実行し、結果をレビュー本文に記載:
```bash
npm run type-check  # 型チェック
npm run lint        # リント
npm run test        # 影響範囲のテスト
```

結果形式:
- ✅成功
- ❌失敗（エラー内容）
- ⏭️未実行（理由）

### Phase 3: フィードバック統合（review-aggregator使用）

**review-aggregator エージェント**（`.claude/agents/review-aggregator.md`）を呼び出し、
各reviewerの出力を統合する。

**aggregatorの処理**:
1. **パース**: 各reviewer出力から `[confidence=XX]` タグを抽出
2. **フィルタリング**:
   - Blockers: 全て残す（confidence<60 は「⚠️ 要確認」ラベル）
   - Important: confidence>=70 のみ（<70 は「要確認」に降格）
   - Suggestions: confidence>=80 のみ（<80 は省略）
3. **重複排除**: 同一 file:line の指摘をマージ、最高confidence採用
4. **Merge Decision判定**:
   - Blockers 0件 → ✅ Merge
   - Blockers 全て「要確認」かつ<=2件 → ⚠️ Merge with follow-ups
   - Blockers に confidence>=60 が1件以上 → ❌ Needs changes

**入力フォーマット**: 各reviewerは統一フォーマットで出力（`.claude/agents/shared/reviewer-output-format.md` 参照）

### Phase 4: PR投稿

**Top-level comment（必須）:**
```bash
gh pr comment <PR_NUMBER> --repo <REPO> --body "$(cat <<'EOF'
## Code Review Summary

### Summary
[2-4行の要約]

### 🔴 Blockers
- [なければ「なし」]

### 🟡 Suggestions
- [箇条書き]

### 🟢 Nice-to-have
- [箇条書き]

### Automated Checks
- Type check: [✅/❌/⏭️]
- Lint: [✅/❌/⏭️]
- Tests: [✅/❌/⏭️]

### Merge Decision
[✅/⚠️/❌ + 理由]

---
🤖 Reviewed by Claude Code (5-domain parallel review)
EOF
)"
```

**Inline comment（選択的）:**
- 特定ファイル・行に明確にアンカーできる場合のみ
- スパム回避のため最小限に

---

## Agent Prompt Templates

### code-quality-reviewer prompt
```
このPRのコード品質をレビューしてください。

Context:
- Stack: Next.js 16 + React 19 + TypeScript + Supabase + Stripe + Playwright
- Rules: [CLAUDE.md summary]
- PR Map: [short PR map]
- Files: [changed file list]

ppt-trans固有のチェック:
- Next.js 16: params: Promise<T> → await params
- Server Actions優先（API RoutesはWebhook/SSE/バイナリのみ）
- Schema-First開発（openapi.yaml → generate:types → 実装）
- any禁止、!禁止、@/*エイリアス必須

Output format:
Summary / Blockers / Suggestions / Nice-to-have
```

### performance-reviewer prompt
```
このPRのパフォーマンスリスクをレビューしてください。

Context:
- Stack: Next.js 16 + React 19 + TypeScript + Supabase + Stripe + Playwright
- Rules: [CLAUDE.md summary]
- PR Map: [short PR map]
- Files: [changed file list]

ppt-trans固有のチェック:
- N+1クエリ、不要なSELECT
- PPTX処理の同期ブロック、プレビューキャッシュ
- Python subprocess呼び出しの効率

Output format:
Summary / Hotspots / Recommendations
```

### security-code-reviewer prompt
```
このPRのセキュリティ問題をレビューしてください。

Context:
- Stack: Next.js 16 + React 19 + TypeScript + Supabase + Stripe + Playwright
- Rules: [CLAUDE.md summary]
- PR Map: [short PR map]
- Files: [changed file list]

ppt-trans固有のチェック:
- Supabase RLS有効確認、Service Role Key漏えい
- Stripe Webhook署名検証、冪等性（stripe_events）
- Rate Limiting: 認証10/15min、翻訳50/hour、アップロード20/hour

Output format:
Summary / Blockers / Findings / Follow-ups
```

### test-coverage-reviewer prompt
```
このPRのテスト（unit/E2E）をレビューしてください。

Context:
- Stack: Next.js 16 + React 19 + TypeScript + Supabase + Stripe + Playwright
- Rules: [CLAUDE.md summary]
- PR Map: [short PR map]
- Files: [changed file list]

ppt-trans固有のチェック:
- UNIFIED_TEST_CONFIG参照必須（ハードコード禁止）
- 認証状態パス: .auth/user.json
- /api/auth/loginは存在しない（ナビゲーション待機を使用）

Output format:
Summary / Flaky risks / Missing scenarios / Improvements
```

### documentation-accuracy-reviewer prompt
```
このPRのドキュメント整合性をレビューしてください。

Context:
- Stack: Next.js 16 + React 19 + TypeScript + Supabase + Stripe + Playwright
- Rules: [CLAUDE.md summary]
- PR Map: [short PR map]
- Files: [changed file list]

ppt-trans固有のチェック:
- .env.example / READMEのenv一覧が最新か
- Schema-First: openapi.yaml更新、generate:types実行
- CLAUDE.md / .claude/rules/ との整合

Output format:
Summary / Docs to update / Inconsistencies / Proposed edits
```

---

## 注意事項

1. **Phase 2の自動チェック結果をレビュー本文に記載**
   - 成功/失敗/未実行を明示

2. **Merge with follow-upsのfollow-upはIssue化前提の粒度**
   - 例: "RLSテスト追加", "429復帰のE2E安定化"

3. **Inlineコメントは差分にアンカーできる時だけ**
   - スパム回避、top-levelコメントに集約

4. **gh CLI前提**
   - `gh`がインストール・認証されている必要あり
