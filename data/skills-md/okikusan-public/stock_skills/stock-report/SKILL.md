---
name: stock-report
description: 個別銘柄の詳細レポート。ティッカーシンボルを指定して財務分析レポートを生成する。バリュエーション・割安度判定・株主還元率（配当+自社株買い）を表示。
argument-hint: "[ticker]  例: 7203.T, AAPL, D05.SI"
allowed-tools: Bash(python3 *)
---

# 個別銘柄レポートスキル

$ARGUMENTS からティッカーシンボルを取り出し、以下のコマンドを実行してください。

```bash
python3 /Users/kikuchihiroyuki/stock-skills/.claude/skills/stock-report/scripts/generate_report.py $ARGUMENTS
```

## 出力内容

- **セクター・業種**
- **株価情報**: 現在値、時価総額
- **バリュエーション**: PER, PBR, 配当利回り, ROE, ROA, 利益成長率
- **割安度判定**: 0-100点スコア + 判定（割安/やや割安/適正/割高）
- **株主還元**（KIK-375）: 配当利回り + 自社株買い利回り = **総株主還元率**
- **業界コンテキスト**（KIK-433, Neo4j 接続時）: 同セクターの直近業界リサーチから追い風・リスクを自動表示

結果をそのまま表示してください。
