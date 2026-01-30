---
name: okane-skills
description: 家計簿の残高予測・シミュレーションスキル。「残高予測」「何ヶ月後にいくら」「この出費大丈夫？」「お金足りる？」「貯金シミュレーション」「ログ圧縮」「危険ポイント検出」などの依頼時に使用。okane-backup-*.json形式のファイルを読み込み、将来の残高推移予測、大きな出費の可否判定、残高不足警告を行う。
---

# Okane Skills - 残高予測・シミュレーション

## 概要

[okane](https://okane-nine.vercel.app/)のエクスポートJSONを分析し:
- **将来の残高予測** - Xヶ月後にいくらになるか
- **出費可否チェック** - 大きな出費が間に合うか
- **危険ポイント検出** - 残高不足になる日を警告
- **ログ圧縮** - 古いデータを月次サマリーに圧縮

## 主要機能

### 1. 残高予測 (`--forecast N`)

Nヶ月後までの残高推移と、各月の大きな出入り（10万円以上）を表示。

```bash
python scripts/okane_analyzer.py data.json --forecast 6
```

**出力例:**
| 月 | 残高 | 大きな出入り |
|----|------|-------------|
| 2026-01 | ¥1,500,000 | 給与(+¥300,000), カード(-¥150,000) |
| 2026-02 | ¥1,200,000 | 家賃(-¥100,000) |

### 2. 出費可否チェック (`--check AMOUNT`)

「この日にこの金額使って大丈夫？」を判定。

```bash
python scripts/okane_analyzer.py data.json --check 1000000 --date 2026-02-01
```

**出力:**
- 判定（✅可能 / ⚠️ギリギリ / ❌不足）
- 出費前後の残高
- その後の予定支出一覧

### 3. 危険ポイント検出 (`--danger`)

残高が閾値を下回る日を検出。

```bash
python scripts/okane_analyzer.py data.json --danger --threshold 100000
```

### 4. ログ圧縮 (`--compress`)

古い取引を月次サマリーに圧縮してファイルサイズを削減。

```bash
python scripts/okane_analyzer.py data.json --compress --keep-months 3 -o compressed.json
```

- `--keep-months N`: 直近Nヶ月は詳細を保持（デフォルト: 3）
- 圧縮前: 各取引が個別レコード
- 圧縮後: 月ごとの収入合計・支出合計に集約

### 5. グラフ生成 (`--chart`)

残高推移グラフをPNG画像で出力。

```bash
python scripts/okane_analyzer.py data.json --chart --chart-months 6 -o chart.png
```

**グラフの内容:**
- 青線: 残高推移
- 緑縦線: 今日
- ▲緑マーカー: 大きな収入（20万円以上）
- ▼赤マーカー: 大きな支出（20万円以上）

## JSONデータ形式

```json
{
  "version": "1.0",
  "initialBalance": 0,
  "transactions": [
    {
      "id": "unique-id",
      "date": "YYYY-MM-DD",
      "type": "income" | "expense",
      "amount": number,
      "description": "説明"
    }
  ]
}
```

## 典型的な使い方

1. **「3月に100万使いたいけど大丈夫？」**
   → `--check 1000000 --date 2026-03-01`

2. **「半年後の貯金いくら？」**
   → `--forecast 6`

3. **「お金やばくなる時ある？」**
   → `--danger`

4. **「JSONが重くなってきた」**
   → `--compress`

5. **「グラフで見せて」**
   → `--chart -o chart.png`
