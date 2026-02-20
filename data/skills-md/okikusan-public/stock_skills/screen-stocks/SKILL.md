---
name: screen-stocks
description: 割安株スクリーニング。EquityQuery で銘柄リスト不要のスクリーニング。PER/PBR/配当利回り/ROE等で日本株・米国株・ASEAN株・香港株・韓国株・台湾株等60地域から割安銘柄を検索する。
argument-hint: "[region] [preset] [--sector SECTOR]  例: japan value, us high-dividend, asean quality, hk value --sector Technology"
allowed-tools: Bash(python3 *)
---

# 割安株スクリーニングスキル

$ARGUMENTS を解析して region、preset、sector を判定し、以下のコマンドを実行してください。

## 実行コマンド

```bash
python3 /Users/kikuchihiroyuki/stock-skills/.claude/skills/screen-stocks/scripts/run_screen.py --region <region> --preset <preset> [--sector <sector>] [--top <N>] [--mode <query|legacy>]
```

## 自然言語ルーティング

自然言語→スキル判定は [.claude/rules/intent-routing.md](../../rules/intent-routing.md) を参照。

## 利用可能な地域コード（yfinance EquityQuery）

主要地域: jp, us, sg, th, my, id, ph, hk, kr, tw, cn, gb, de, fr, in, au, br, ca 等（約60地域）

## 利用可能な取引所コード

| 取引所 | コード |
|:------|:------|
| 東京証券取引所 | JPX |
| NASDAQ | NMS |
| NYSE | NYQ |
| シンガポール証券取引所 | SES |
| タイ証券取引所 | SET |
| マレーシア証券取引所 | KLS |
| インドネシア証券取引所 | JKT |
| フィリピン証券取引所 | PHS |
| 香港証券取引所 | HKG |
| 韓国証券取引所 | KSC/KOE |
| 台湾証券取引所 | TAI |

## スクリーニングモード

- `--mode query` (デフォルト): **EquityQuery方式**。yfinance の EquityQuery API を使い、銘柄リスト不要で条件に合う銘柄を直接検索する。全地域に対応。高速。
- `--mode legacy`: **銘柄リスト方式**。従来のValueScreenerを使用。事前定義した銘柄リスト（日経225、S&P500等）を1銘柄ずつ取得・評価。japan/us/asean のみ対応。
- `--with-pullback`: **押し目フィルタ追加**。任意のプリセット（value, high-dividend 等）にテクニカル押し目判定を追加適用する。`--preset pullback` との同時指定は不要（pullback プリセットが優先される）。出力は Pullback モードと同じ列形式。

## プリセット

- `value` : 伝統的バリュー投資（低PER・低PBR・ROE≧5%）
- `high-dividend` : 高配当株（配当利回り3%以上）
- `growth` : 純成長株（高ROE≧15%・売上成長≧10%。PER制約なし。割安度を問わず成長力で選別）
- `growth-value` : 成長バリュー（成長性＋割安度）
- `deep-value` : ディープバリュー（非常に低いPER/PBR）
- `quality` : クオリティバリュー（高ROE≧15%＋割安。value の ROE 閾値を5%→15%に厳格化した上位集合。収益力の高い割安株に限定）
- `pullback` : 押し目買い型（上昇トレンド中の一時調整でエントリー。EquityQuery→テクニカル→SR の3段パイプライン。実行に時間がかかります）
- `alpha` : アルファシグナル（割安＋変化の質＋押し目の3軸統合。EquityQuery→変化の質→押し目判定→2軸スコアリングの4段パイプライン。実行に時間がかかります）
- `trending` : Xトレンド銘柄（Grok API でX上の話題銘柄を発見→Yahoo Financeでファンダメンタルズ評価。`--theme` でテーマ絞り込み可。XAI_API_KEY 必須）
- `long-term` : 長期投資適性（高ROE≧15%・EPS成長≧10%・配当≧2%・PER≦25・PBR≦3・時価総額1000億以上。長期保有に適した安定成長銘柄を検索）
- `shareholder-return` : 株主還元重視（配当利回り+自社株買い利回りの総還元率でランキング。安定度評価付き: ✅安定/📈増加/⚠️一時的/📉低下）

## 出力

結果はMarkdown表形式で表示してください。EquityQuery モードではセクター列が追加される。

### EquityQuery モードの出力列
順位 / 銘柄 / セクター / 株価 / PER / PBR / 配当利回り / ROE / スコア

### Legacy モードの出力列
順位 / 銘柄 / 株価 / PER / PBR / 配当利回り / ROE / スコア

### Pullback モードの出力列
順位 / 銘柄 / 株価 / PER / 押し目% / RSI / 出来高比 / SMA50 / SMA200 / スコア

### Alpha モードの出力列
順位 / 銘柄 / 株価 / PER / PBR / 割安 / 変化 / 総合 / 押し目 / ア / 加速 / FCF / ROE趨勢

### Growth モードの出力列
順位 / 銘柄 / セクター / 株価 / PER / PBR / EPS成長 / 売上成長 / ROE

### Trending モードの出力列
順位 / 銘柄 / 話題の理由 / 株価 / PER / PBR / 配当利回り / ROE / スコア / 判定

### Shareholder Return モードの出力列
順位 / 銘柄 / 株価 / 配当利回り / 自社株買い利回り / 総還元率 / 安定度 / ROE / PER

## 実行例

```bash
# 日本の割安株（デフォルト）
python3 .../run_screen.py --region japan --preset value

# 米国の高配当テクノロジー株
python3 .../run_screen.py --region us --preset high-dividend --sector Technology

# 香港のバリュー株
python3 .../run_screen.py --region hk --preset value

# ASEAN の成長バリュー株（sg, th, my, id, ph を順次実行）
python3 .../run_screen.py --region asean --preset growth-value

# Legacy モードで米国株をスクリーニング
python3 .../run_screen.py --region us --preset value --mode legacy

# 日本株の押し目買い候補
python3 .../run_screen.py --region japan --preset pullback

# 日本株のアルファシグナル（割安＋変化＋押し目）
python3 .../run_screen.py --region japan --preset alpha

# 米国株のアルファシグナル
python3 .../run_screen.py --region us --preset alpha

# 日本の割安株 + 押し目フィルタ
python3 .../run_screen.py --region japan --preset value --with-pullback

# 米国の高配当株 + 押し目フィルタ
python3 .../run_screen.py --region us --preset high-dividend --with-pullback

# X (Twitter) で話題の日本株
python3 .../run_screen.py --region japan --preset trending

# X で話題のAI関連米国株
python3 .../run_screen.py --region us --preset trending --theme "AI"

# X で話題の半導体関連銘柄
python3 .../run_screen.py --region japan --preset trending --theme "半導体"

# 日本の長期投資候補
python3 .../run_screen.py --region japan --preset long-term

# 米国の長期投資候補
python3 .../run_screen.py --region us --preset long-term

# 日本の純成長株（割安制約なし）
python3 .../run_screen.py --region japan --preset growth

# 米国の純成長株
python3 .../run_screen.py --region us --preset growth

# 日本の高還元株
python3 .../run_screen.py --region japan --preset shareholder-return

# 米国の高還元株
python3 .../run_screen.py --region us --preset shareholder-return
```

## アノテーション機能 (KIK-418/419)

スクリーニング結果には投資メモと売却履歴に基づくマーカーが自動付与されます。

### マーカー凡例

| マーカー | 意味 | トリガー |
|:---:|:---|:---|
| ⚠️ | 懸念メモあり | 投資メモ type=concern |
| 📝 | 学びメモあり | 投資メモ type=lesson |
| 👀 | 様子見 | 投資メモ type=observation + 「見送り」「待ち」等キーワード |

### 売却済み銘柄の自動除外

直近90日以内に売却した銘柄はスクリーニング結果から自動除外されます。除外数はメッセージで表示されます。

### データソース

1. Neo4j ナレッジグラフ（優先）
2. JSON ファイル（Neo4j 未接続時のフォールバック）
