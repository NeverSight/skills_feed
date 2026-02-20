---
name: market-research
description: "銘柄・業界・マーケット・ビジネスモデルの深掘りリサーチ。Grok API (X/Web検索) と yfinance を統合して多角的な分析レポートを生成する。"
argument-hint: "[stock|industry|market|business] [対象]  例: stock 7203.T, industry 半導体, market 日経平均, business 7751.T"
allowed-tools: Bash(python3 *)
---

# 深掘りリサーチスキル

$ARGUMENTS を解析してリサーチタイプと対象を判定し、以下のコマンドを実行してください。

## 実行コマンド

```bash
python3 /Users/kikuchihiroyuki/stock-skills/.claude/skills/market-research/scripts/run_research.py <command> <target>
```

## 自然言語ルーティング

自然言語→スキル判定は [.claude/rules/intent-routing.md](../../rules/intent-routing.md) を参照。

## リサーチタイプ別の出力

### stock（銘柄リサーチ）
- 基本情報 + バリュエーション（yfinance）
- 最新ニュース（yfinance）
- Xセンチメント（Grok API）
- 深掘り分析: ニュース・業績材料・アナリスト見解・競合比較（Grok API）

### industry（業界リサーチ）
- トレンド・主要プレイヤー・成長ドライバー・リスク・規制動向（Grok API）

### market（マーケット概況）
- 値動き・マクロ要因・センチメント・注目イベント・セクターローテーション（Grok API）

### business（ビジネスモデル分析）
- 事業概要（何で稼いでいるか）
- 事業セグメント構成（セグメント名・売上比率・概要）
- 収益モデル（ストック型/フロー型/サブスク等）
- 競争優位性（参入障壁・ブランド・技術・moat）
- 重要KPI（投資家が注目すべき指標）
- 成長戦略（中期経営計画・M&A・新規事業）
- ビジネスリスク（構造的リスク・依存度）

## API について

### Grok API
- XAI_API_KEY 環境変数が設定されている場合のみ Grok API を利用
- 未設定時は yfinance データのみでレポート生成（stock の場合）

### 2層構成
1. **Layer 1 (yfinance)**: 常に利用可能（ファンダメンタルズ・株価データ）
2. **Layer 2 (Grok API)**: XAI_API_KEY 設定時（X投稿・Web検索による深掘り分析）

- industry / market / business は Layer 2 が必要。未設定時はその旨を表示

### APIステータスサマリー（KIK-431）

各レポートの末尾に Grok API の状態を表示する:

| 状態 | 表示 |
|:-----|:-----|
| 正常 | ✅ 正常 |
| 未設定 | 🔑 未設定 — XAI_API_KEY を設定すると利用可能 |
| 認証エラー | ❌ 認証エラー (401) — XAI_API_KEY を確認してください |
| レート制限 | ⚠️ レート制限 (429) — しばらく待ってから再試行 |
| タイムアウト | ⏱️ タイムアウト — ネットワーク接続を確認 |
| その他のエラー | ❌ エラー — 詳細は stderr を確認 |

## 出力の補足

スクリプトの出力をそのまま表示した後、Claudeが以下を補足してください:

### stock の場合
- ファンダメンタルズデータと Grok リサーチの整合性を確認
- バリュースコアと市場センチメントの乖離があれば指摘
- 投資判断に影響する追加コンテキストがあれば補足

### industry の場合
- 日本市場固有の事情を補足（規制環境、参入障壁等）
- 関連する銘柄スクリーニングの提案（/screen-stocks との連携）

### market の場合
- ポートフォリオへの影響を推定（/stock-portfolio との連携）
- 類似過去事例があれば言及

### business の場合
- セグメント構成と株価バリュエーションの関係を考察
- 収益モデルの持続性（ストック型は安定、フロー型は景気感応度高い等）
- 競争優位性が実際の財務指標（ROE、利益率等）に表れているか確認
- `/stock-report` の結果と合わせてファンダメンタルズとの整合性を補足

## 実行例

```bash
# 銘柄リサーチ
python3 .../run_research.py stock 7203.T
python3 .../run_research.py stock AAPL

# 業界リサーチ
python3 .../run_research.py industry 半導体
python3 .../run_research.py industry "Electric Vehicles"

# マーケットリサーチ
python3 .../run_research.py market 日経平均
python3 .../run_research.py market "S&P500"

# ビジネスモデル分析
python3 .../run_research.py business 7751.T
python3 .../run_research.py business AAPL
```
