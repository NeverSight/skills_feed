---
name: stock-portfolio
description: "ポートフォリオ管理。保有銘柄の一覧表示・売買記録・構造分析。ストレステストの入力データ基盤。"
argument-hint: "[command] [args]  例: snapshot, buy 7203.T 100 2850, sell AAPL 5, analyze, list"
allowed-tools: Bash(python3 *)
---

# ポートフォリオ管理スキル

$ARGUMENTS を解析してコマンドを判定し、以下のコマンドを実行してください。

## 実行コマンド

```bash
python3 /Users/kikuchihiroyuki/stock-skills/.claude/skills/stock-portfolio/scripts/run_portfolio.py <command> [args]
```

## コマンド一覧

### snapshot -- PFスナップショット

現在価格・損益・通貨換算を含むポートフォリオのスナップショットを生成する。

```bash
python3 .../run_portfolio.py snapshot
```

### buy -- 購入記録追加

```bash
python3 .../run_portfolio.py buy --symbol <sym> --shares <n> --price <p> [--currency JPY] [--date YYYY-MM-DD] [--memo テキスト] [--yes]
```

`--yes` (`-y`) を省略すると購入内容の確認プレビューを表示して終了する。`--yes` を指定すると確認をスキップして直接記録する（KIK-444）。

### sell -- 売却記録

```bash
python3 .../run_portfolio.py sell --symbol <sym> --shares <n> [--price <売却単価>] [--date YYYY-MM-DD] [--yes]
```

`--yes` (`-y`) を省略すると売却内容の確認プレビュー（取得単価・推定実現損益）を表示して終了する。`--yes` を指定すると確認をスキップして直接記録する（KIK-444）。

`--price` を指定すると実現損益・損益率・税引後概算を計算して表示し、`data/history/trade/*.json` に保存する（KIK-441）。

### review -- 売買パフォーマンスレビュー (KIK-441)

過去の売却記録（`--price` 付きで記録したもの）から損益統計を集計して表示する。

```bash
python3 .../run_portfolio.py review [--year 2026] [--symbol NVDA]
```

**出力内容:**
- 取引履歴テーブル（銘柄・売却日・株数・取得単価・売却単価・保有日数・実現損益・損益率）
- 統計（取引件数・勝率・平均リターン・平均保有期間・合計実現損益）

### analyze -- 構造分析

地域/セクター/通貨のHHI（ハーフィンダール指数）を算出し、ポートフォリオの偏りを分析する。

```bash
python3 .../run_portfolio.py analyze
```

### health -- ヘルスチェック

保有銘柄の投資仮説がまだ有効かをチェックする。テクニカル（SMA50/200, RSI, **ゴールデンクロス/デッドクロス検出**）とファンダメンタル（変化スコア、**株主還元安定度**）の多軸で3段階アラートを出力。

```bash
python3 .../run_portfolio.py health
```

**テクニカル分析（KIK-356/374）:**
- SMA50/200 のトレンド判定（上昇/横ばい/下降）
- **ゴールデンクロス/デッドクロス検出**: 60日 lookback でクロスイベントを検出し、発生日と経過日数を表示

**株主還元安定度（KIK-403）:**
- 配当+自社株買いの総還元率から安定度を評価（✅安定高還元/📈増加傾向/⚠️一時的高還元/📉減少傾向）
- 一時的高還元（temporary）→ 早期警告に昇格
- 減少傾向（decreasing）→ アラート詳細に理由追加
- 長期適性判定に総還元率（配当+自社株買い）を使用

**アラートレベル:**
- **早期警告**: SMA50割れ / RSI急低下 / 変化スコア1指標悪化 / **一時的高還元**
- **注意**: SMA50がSMA200に接近 + 指標悪化 / 変化スコア複数悪化
- **撤退**: **デッドクロス検出** / トレンド崩壊 + 変化スコア悪化

### rebalance -- リバランス提案

現在のポートフォリオ構造を分析し、集中リスクの低減と目標配分への調整案を提示する。

```bash
python3 .../run_portfolio.py rebalance [options]
```

CLIオプション:
- `--strategy defensive|balanced|aggressive` (デフォルト: balanced)
- `--reduce-sector SECTOR` (例: Technology)
- `--reduce-currency CURRENCY` (例: USD)
- `--max-single-ratio RATIO` (例: 0.15)
- `--max-sector-hhi HHI` (例: 0.25)
- `--max-region-hhi HHI` (例: 0.30)
- `--additional-cash AMOUNT` (円, 例: 1000000)
- `--min-dividend-yield YIELD` (例: 0.03)

### forecast -- 推定利回り

保有銘柄ごとにアナリスト目標価格 or 過去リターン分布から12ヶ月の期待リターンを3シナリオ（楽観/ベース/悲観）で推定する。バリュートラップ警告・TOP/BOTTOM ランキング付き。

```bash
python3 .../run_portfolio.py forecast
```

**推定手法:**
- **アナリスト法**: アナリスト目標株価 + 配当利回り + 自社株買い利回り（株主還元込み）
- **過去リターン法**: ETF等アナリストカバレッジなし銘柄は過去CAGR + 標準偏差で推定
- **業界カタリスト調整**（KIK-433, Neo4j 接続時）: 同セクターの直近 `growth_driver` カタリスト数 × 1.7% を楽観シナリオに加算、`risk` カタリスト数 × 1.7% を悲観シナリオから減算（上限各 10%）

**出力構成（KIK-390）:**
1. ポートフォリオ全体の3シナリオ利回り・損益額テーブル
2. 注意銘柄セクション（バリュートラップ警告のある銘柄を集約）
3. 期待リターン TOP 3 / BOTTOM 3 ランキング
4. 銘柄別詳細（アナリスト目標/Forward PER/ニュース件数/Xセンチメント/3シナリオ）

### what-if -- What-Ifシミュレーション

指定した銘柄を追加した場合のポートフォリオへの影響をBefore/After比較で表示する。

```bash
python3 .../run_portfolio.py what-if --add "SYMBOL:SHARES:PRICE[,SYMBOL:SHARES:PRICE,...]"
```

CLIオプション:
- `--add` : 追加銘柄リスト（必須）。形式: `SYMBOL:SHARES:PRICE` をカンマ区切り

**出力:**
- Before/After のセクターHHI・地域HHI・通貨HHI比較
- 追加銘柄の基本情報（PER/PBR/配当利回り/ROE）
- 集中度の変化と改善/悪化の判定

### backtest -- バックテスト

蓄積されたスクリーニング結果からリターンを検証し、ベンチマーク（日経225/S&P500）と比較する。

```bash
python3 .../run_portfolio.py backtest [options]
```

CLIオプション:
- `--preset PRESET` : 検証対象のスクリーニングプリセット（例: alpha, value）
- `--region REGION` : 検証対象の地域（例: jp, us）
- `--days N` : 取得後N日間のリターンを検証（デフォルト: 90）

**出力:**
- スクリーニング日別の平均リターン
- ベンチマーク比較（超過リターン）
- 勝率・平均リターン・最大リターン/最大損失

### simulate -- 複利シミュレーション

現在のポートフォリオを基に、複利計算で将来の資産推移をシミュレーションする。forecast の期待リターン + 配当再投資 + 毎月積立を複利で計算し、楽観/ベース/悲観の3シナリオで表示。

```bash
python3 .../run_portfolio.py simulate [options]
```

CLIオプション:
- `--years N` (シミュレーション年数, デフォルト: 10)
- `--monthly-add AMOUNT` (月額積立額, 円, デフォルト: 0)
- `--target AMOUNT` (目標額, 円, 例: 15000000)
- `--reinvest-dividends` (配当再投資する, デフォルト: ON)
- `--no-reinvest-dividends` (配当再投資しない)

### list -- 保有銘柄一覧

portfolio.csv の内容をそのまま表示する。

```bash
python3 .../run_portfolio.py list
```

## 自然言語ルーティング

自然言語→スキル判定は [.claude/rules/intent-routing.md](../../rules/intent-routing.md) を参照。

## 制約事項

- 日本株: 100株単位（単元株）
- ASEAN株: 100株単位（最低手数料 3,300円）
- 楽天証券対応（手数料体系）
- portfolio.csv のパス: `.claude/skills/stock-portfolio/data/portfolio.csv`

## 出力

結果はMarkdown形式で表示してください。

### snapshot の出力項目
- 銘柄 / 名称 / 保有数 / 取得単価 / 現在価格 / 評価額 / 損益 / 損益率 / 通貨

### analyze の出力項目
- セクターHHI / 地域HHI / 通貨HHI
- 各軸の構成比率
- リスクレベル判定

### health の出力項目
- 銘柄 / 損益率 / トレンド（上昇/横ばい/下降） / **クロスイベント**（ゴールデンクロス/デッドクロス） / 変化の質（良好/1指標↓/複数悪化） / アラート / **長期適性** / **還元安定度**
- アラートがある銘柄の詳細（理由、SMA/RSI値、クロス発生日・経過日数、変化スコア、株主還元安定度、推奨アクション）

### forecast の出力項目
- ポートフォリオ全体: 3シナリオ利回り（楽観/ベース/悲観）+ 損益額 + 総評価額
- 注意銘柄セクション: バリュートラップ警告のある銘柄一覧
- TOP 3 / BOTTOM 3: 期待リターンランキング（アナリスト数付き）
- 銘柄別: アナリスト目標価格 / Forward PER / ニュース件数 / Xセンチメント / 3シナリオ

### what-if の出力項目
- Before/After のHHI比較（セクター/地域/通貨）
- 追加銘柄のファンダメンタルズ
- 集中度変化の判定

### backtest の出力項目
- スクリーニング日別リターン
- ベンチマーク比較（超過リターン）
- 勝率・統計値

### rebalance の出力項目
- 現状のHHI（セクター/地域/通貨）と目標HHI
- 売却候補（銘柄・株数・理由）
- 購入候補（銘柄・株数・理由・配当利回り）
- リバランス後のHHI予測値

### simulate の出力項目
- 年次推移テーブル（年/評価額/累計投入/運用益/配当累計）
- 3シナリオ比較（楽観/ベース/悲観の最終年）
- 目標達成分析（到達年/必要積立額）
- 配当再投資の複利効果

## 実行例

```bash
# スナップショット
python3 .../run_portfolio.py snapshot

# 購入記録
python3 .../run_portfolio.py buy --symbol 7203.T --shares 100 --price 2850 --currency JPY --date 2025-06-15 --memo トヨタ

# 売却記録
python3 .../run_portfolio.py sell --symbol AAPL --shares 5

# 構造分析
python3 .../run_portfolio.py analyze

# 一覧表示
python3 .../run_portfolio.py list

# ヘルスチェック
python3 .../run_portfolio.py health

# 推定利回り
python3 .../run_portfolio.py forecast

# リバランス提案
python3 .../run_portfolio.py rebalance
python3 .../run_portfolio.py rebalance --strategy defensive
python3 .../run_portfolio.py rebalance --reduce-sector Technology --additional-cash 1000000

# What-Ifシミュレーション
python3 .../run_portfolio.py what-if --add "7203.T:100:2850,AAPL:10:250"

# バックテスト
python3 .../run_portfolio.py backtest --preset alpha --region jp --days 90
```
