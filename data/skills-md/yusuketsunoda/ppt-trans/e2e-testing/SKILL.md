---
name: e2e-testing
description: Supports E2E test creation, debugging, and failure fixes for Playwright tests. Activates when user mentions "test failed", "flaky test", "E2Eが落ちた", "テストが動かない", "Playwright error", "新規テスト作成", "テストメンテナンス".
allowed-tools: Read, Grep, Glob, Bash, Edit, Write
user-invocable: true
---

# E2E Testing Skill

E2Eテストの作成・デバッグ・メンテナンスを支援する。テスト失敗の調査・修正に特に有効。

## When to Use This Skill

- Playwrightテストが失敗した時
- 新規E2Eテストを作成する時
- 既存テストをメンテナンス・リファクタリングする時
- テストがflaky（不安定）な時
- テストのタイムアウトやセレクタエラーを修正する時

---

## ワークフロー: 新規テスト作成 (MANDATORY)

> "Build evaluations FIRST before writing extensive documentation. This ensures your Skill solves real problems rather than documenting imagined ones."
> — [Anthropic Skill Best Practices](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/best-practices)

**新規テスト作成時は、以下の検証フローを必ず実行してください。**

### Step 1: 機能の実装状況を確認

テスト対象の機能が実際に実装されているか確認します。

```bash
# Server Actionsの確認
ls src/app/actions/
grep -r "対象関数名" src/app/actions/

# API Routesの確認（必要な場合）
ls src/app/api/

# コンポーネントの確認
grep -r "data-testid" src/components/ | grep "対象要素"
```

**確認項目:**
- [ ] Server Action/API Routeが存在する
- [ ] UIコンポーネントが実装されている
- [ ] data-testid属性が定義されている

### Step 2: 実装コードを読む

テスト対象の実装を理解してからテストを書く：

```bash
# 例: 翻訳機能のテスト
Read src/app/actions/translate.ts
Read src/app/[locale]/preview/[id]/hooks/use-translation.ts

# 例: アップロード機能のテスト
Read src/app/actions/upload/index.ts
Read src/components/upload/upload-dropzone.tsx
```

**確認項目:**
- [ ] 実装の動作を理解した
- [ ] エラーハンドリングを確認した
- [ ] 期待する戻り値/状態遷移を把握した

### Step 3: MVP範囲の確認

テスト対象がMVP機能に含まれるか確認します。

**MVP機能一覧（テスト対象）:**
| 機能 | 実装場所 | テスト優先度 |
|------|---------|-------------|
| 認証 | `src/app/actions/auth.ts` | 高 |
| アップロード | `src/app/actions/upload/` | 高 |
| プレビュー | `src/app/[locale]/preview/` | 高 |
| 翻訳 | `src/app/actions/translate.ts` | 高 |
| ダウンロード | `src/app/api/files/[id]/download/` | 高 |
| 決済 | `src/app/actions/payment.ts` | 中 |

**上記以外の機能は、明確な要件がない限りテストしないでください。**

### Step 4: 既存テストとの重複確認

同じ機能をテストする既存テストがないか確認します。

```bash
grep -r "テスト対象機能" e2e/
grep -r "該当data-testid" e2e/
```

### Step 5: テスト設計の妥当性確認

テストを書く前の最終チェック：

```
妥当性チェックリスト:
- [ ] 実装コードを読んで動作を理解した
- [ ] テストするセレクタ（data-testid等）が実装に存在する
- [ ] 期待する動作が実装されている
- [ ] 推測や仮定に基づいていない
- [ ] MVP範囲内の機能である
```

### 禁止事項

| パターン | 説明 | 回避策 |
|---------|------|--------|
| 推測テスト | 「こうあるべき」という仮定 | 実装を確認してから書く |
| 未実装機能テスト | 存在しない機能のテスト | 実装完了後に書く |
| 過剰テスト | MVP範囲外の機能 | MVP範囲に限定 |

---

## ワークフロー: テスト失敗の修正

### Step 1: 失敗の特定
- [ ] エラーメッセージを確認
- [ ] スクリーンショット/トレースを確認（`test-results/*/`）
- [ ] 失敗したテストファイルを読む

```bash
# 失敗テストのログ確認
npm run test:e2e:smoke 2>&1 | tail -100

# スクリーンショット確認
ls -la test-results/*/
```

### Step 2: 関連ファイルを確認
- [ ] `e2e/config/unified-test-config.ts` - 設定値
- [ ] `e2e/page-objects/*.ts` - ページオブジェクト
- [ ] 失敗したテストファイル自体

### Step 3: 原因分析と修正
- [ ] 失敗パターンを特定（→ [failure-patterns.md](./failure-patterns.md) 参照）
- [ ] 修正を適用
- [ ] 単一テストで検証

```bash
npx playwright test e2e/path/to/test.spec.ts --headed
```

### Step 4: 回帰確認
- [ ] 関連テストを実行
- [ ] スモークテストで全体確認

```bash
npm run test:e2e:smoke
```

## 修正時の判断基準

**テスト修正時は `.claude/rules/testing.md` の「テスト修正ガイドライン」セクションを必ず参照すること。**

核心原則: テストを通すことが目的ではない。実装が正しく動作することが目的。

## 必須ルール

### ハードコード禁止
```typescript
// ❌ WRONG
await page.fill("input[name='email']", "test@example.com");

// ✅ CORRECT
import { UNIFIED_TEST_CONFIG } from "../config/unified-test-config";
await page.fill("input[name='email']", UNIFIED_TEST_CONFIG.users.standard.email);
```

### 認証状態ファイル
```typescript
// ❌ WRONG
storageState: "playwright-auth.json"

// ✅ CORRECT
storageState: UNIFIED_TEST_CONFIG.paths.authState  // .auth/user.json
```

### ログイン待機
```typescript
// ❌ WRONG - /api/auth/login は存在しない
await page.waitForResponse(r => r.url().includes("/api/auth/login"));

// ✅ CORRECT - ナビゲーション待機
await page.click('button[type="submit"]');
await page.waitForURL("**/dashboard", { timeout: 15000 });
```

## テストコマンド

| コマンド | 用途 |
|---------|------|
| `npm run test:e2e:smoke` | スモークテスト (~2min) |
| `npm run test:e2e:critical` | クリティカルフロー (~5min) |
| `npm run test:e2e:ui` | UIモード (デバッグ) |
| `npm run test:e2e:debug` | DevTools付きデバッグ |

## 環境変数

```bash
CSRF_RELAXED_IN_E2E=true              # CSRF緩和
DISABLE_RATE_LIMIT_IN_E2E=true        # Rate limit無効
NEXT_PUBLIC_TEST_MODE=true            # テストモード
ENABLE_TRANSLATION_TEST_FAST_PATH=true # ダミー翻訳（100倍高速）
```

## 参照ドキュメント

- [failure-patterns.md](./failure-patterns.md) - 失敗パターンと解決策
- [page-objects.md](./page-objects.md) - ページオブジェクトの使い方
- [e2e/config/unified-test-config.ts](../../../e2e/config/unified-test-config.ts) - 設定値

## ディレクトリ構造

```
e2e/                              # 計61個のテスト
├── config/                        # テスト設定
│   ├── projects.ts               # プロジェクト設定
│   └── unified-test-config.ts    # 統一設定（CRITICAL）
├── smoke/                         # スモークテスト（2個）
├── core/                          # コアテスト（18個）
├── features/                      # 機能テスト（20個）
├── auth/                          # 認証テスト（4個）
├── admin/                         # 管理者テスト（4個）
├── payment/                       # 決済テスト（2個）
├── security/                      # セキュリティテスト（2個）
├── accessibility/                 # アクセシビリティテスト（1個）
├── i18n/                          # 国際化テスト（1個）
├── performance/                   # パフォーマンステスト（2個）
├── regression/                    # リグレッションテスト（3個）
├── server-actions/                # Server Actionsテスト（2個）
├── fixtures/                      # テストフィクスチャ（10個）
├── helpers/                       # ヘルパー関数（11個）
├── page-objects/                  # ページオブジェクト（5個）
└── test-files/                    # テスト用ファイル
```

## AI Assistant Instructions

このスキルが有効化された時:

### 新規テスト作成時 (CRITICAL)

1. **実装を確認する**: テスト対象の機能が実装されているか確認
2. **コードを読む**: 実装の動作を理解してからテストを書く
3. **MVP範囲を確認**: テスト対象がMVP機能に含まれるか確認
4. **セレクタを確認**: data-testid属性が実装に存在するか確認

### テスト修正時

1. **まず失敗を理解する**: エラーメッセージとスクリーンショットを確認
2. **設定を確認する**: `UNIFIED_TEST_CONFIG` の値を参照
3. **既存パターンに従う**: page-objectsとhelpersを活用
4. **段階的に修正する**: 単一テストで検証してから全体確認

### Always

- `UNIFIED_TEST_CONFIG` から設定値を取得する
- ハードコードされた値を使用しない
- 修正後は必ず単一テストで検証する
- **新規テスト作成前に実装コードを読む**

### Never

- `/api/auth/login` を待機しない（存在しない）
- `playwright-auth.json` をハードコードしない
- タイムアウトを過度に長くしない（最大30秒）
- **実装を確認せずにテストを書かない**
- **「こうあるべき」という推測でテストを書かない**
- **MVP範囲外の機能をテストしない**
