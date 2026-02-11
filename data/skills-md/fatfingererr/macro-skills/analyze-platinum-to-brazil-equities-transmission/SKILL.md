---
name: analyze-platinum-to-brazil-equities-transmission
description: 使用公開市場資料量化驗證鉑/白金對巴西股市（EWZ）的長週期傳導/連動關係，輸出雙軸圖、領先落後分析、關聯強度分數與監控訊號。
---

<essential_principles>

<principle name="transmission_verification">
**傳導驗證而非預測**

本技能專注於「用數據驗證敘事」：
- 輸入：社群/新聞宣稱「白金走勢可能領先或驅動巴西股市」
- 輸出：長週期時間序列上的傳導假說檢驗結果

不做價格預測，只回答：「白金→巴西股市的傳導結構在數據上是否存在？」
</principle>

<principle name="lead_lag_cross_correlation">
**交叉相關判斷領先落後**

使用 Cross-Correlation 掃描 [-lead_lag_max, +lead_lag_max] 範圍：
- `corr(r_ewz, r_platinum.shift(lag))`
- **lag > 0**：白金領先 EWZ（platinum leads）
- **lag < 0**：EWZ 領先白金
- **lag ≈ 0**：同步移動

典型設定：週頻 lag max = 52（一年），找 |corr| 最大的 lag。
</principle>

<principle name="regime_awareness">
**Regime-Dependent 關聯**

白金與巴西股市的關聯具有週期性特徵：
- **linked_upcycle**：兩者趨勢同向上行，傳導結構穩固
- **decoupled**：關聯斷裂，各走各的
- **brazil_idiosyncratic**：巴西特有風險（政治/匯率/商品結構）主導

長期 regime 判斷使用 regime_window（預設 104 週 ≈ 2 年）內的趨勢一致性。
</principle>

<principle name="transmission_strength_score">
**傳導強度分數（0–100）**

綜合三個維度量化傳導可信度：

| 維度                   | 權重 | 說明                            |
|------------------------|------|---------------------------------|
| best_lead_lag_corr     | 30%  | 最佳領先落後相關係數            |
| rolling_corr_stability | 30%  | rolling corr > 0 的佔比與連續性 |
| trend_agreement        | 40%  | 長期趨勢一致程度                |

分數解讀：≥70 強傳導、50-69 中等、<50 弱/不穩定。
</principle>

<principle name="data_source">
**資料來源**

主要使用 Yahoo Finance（免費、無需 API key）：
- **白金期貨**：`PL=F`
- **巴西股市 ETF**：`EWZ`

頻率建議：1wk（週頻）用於長週期分析，避免日頻噪音干擾。
對齊方式：inner join（只保留共同交易日），避免補值造成假相關。
</principle>

</essential_principles>

<objective>
量化驗證「白金（Platinum）→ 巴西股市（EWZ）」的長週期傳導關係：

1. **數據取得**：從 Yahoo Finance 取得白金期貨與 EWZ 歷史價格
2. **雙軸圖與正規化圖**：Bloomberg 風格原值雙軸圖 + 正規化同軸對比
3. **領先落後分析**：交叉相關找出白金是否領先 EWZ 及滯後期數
4. **Rolling Correlation**：滾動相關觀察關聯的時變結構
5. **Regime 判斷**：長期趨勢一致性判斷當前處於哪種傳導體制
6. **傳導強度分數**：綜合評分（0-100）量化傳導可信度

輸出：傳導強度分數、領先落後判定、regime label、監控清單、Bloomberg 風格圖表。
</objective>

<quick_start>

**Step 1：安裝依賴**
```bash
pip install yfinance pandas numpy matplotlib scipy
```

**Step 2：執行完整分析**
```bash
cd scripts
python analyze.py --start 2003-01-01
```

**Step 3：生成 Bloomberg 風格視覺化圖表**
```bash
python visualize.py --start 2003-01-01
# 輸出到: output/platinum_vs_ewz_YYYY-MM-DD.png
```

**輸出範例**：
```json
{
  "signal": "transmission_moderate",
  "confidence": "medium",
  "transmission_strength_score": 74,
  "best_lead_lag": {
    "lag_weeks": 12,
    "meaning": "Platinum leads EWZ by ~12 weeks",
    "corr": 0.52
  },
  "rolling_corr": {
    "window": 52,
    "latest": 0.41,
    "positive_share_5y": 0.68
  },
  "regime_label": "linked_upcycle",
  "monitoring_notes": [
    "若 PL=F 突破長期區間，觀察 EWZ 在 8-16 週內是否趨勢翻多",
    "要求 52 週 rolling corr 維持正值至少 26 週作為確認",
    "若白金大漲而 EWZ 不動且 corr 轉負，視為 regime break"
  ]
}
```

</quick_start>

<intake>
需要進行什麼分析？

1. **快速檢查** - 查看白金與巴西股市目前的傳導狀態
2. **完整分析** - 執行完整傳導檢驗並生成報告
3. **視覺化圖表** - 生成 Bloomberg 風格雙軸圖與相關分析圖表
4. **方法論學習** - 了解傳導分析、交叉相關與 regime 判斷的原理

**請選擇或直接提供分析參數。**
</intake>

<routing>
| Response                     | Action                                       |
|------------------------------|----------------------------------------------|
| 1, "快速", "quick", "check"  | 閱讀 `workflows/analyze.md` 並以預設參數執行 |
| 2, "完整", "full", "analyze" | 閱讀 `workflows/analyze.md` 並執行           |
| 3, "視覺化", "chart", "plot" | 閱讀 `workflows/visualize.md` 並執行         |
| 4, "學習", "方法論", "why"   | 閱讀 `references/methodology.md`             |
| 提供參數 (如日期/ticker)     | 閱讀 `workflows/analyze.md` 並使用參數執行   |

**路由後，閱讀對應文件並執行。**
</routing>

<directory_structure>
```
analyze-platinum-to-brazil-equities-transmission/
├── SKILL.md                           # 本文件（路由器）
├── skill.yaml                         # 前端展示元數據
├── manifest.json                      # 技能元資料
├── workflows/
│   ├── analyze.md                     # 完整傳導分析工作流
│   └── visualize.md                   # 視覺化工作流
├── references/
│   ├── data-sources.md                # 資料來源與替代方案
│   ├── methodology.md                 # 傳導分析方法論
│   └── input-schema.md                # 完整輸入參數定義
├── templates/
│   ├── output-json.md                 # JSON 輸出模板
│   └── output-markdown.md             # Markdown 報告模板
├── scripts/
│   ├── analyze.py                     # 主分析腳本
│   ├── fetch_data.py                  # 數據抓取工具（Yahoo Finance）
│   └── visualize.py                   # Bloomberg 風格視覺化
└── examples/
    └── sample_output.json             # 範例輸出
```
</directory_structure>

<reference_index>

**方法論**: references/methodology.md
- 交叉相關領先落後分析
- Rolling Correlation 時變結構
- Regime 判斷邏輯
- 傳導強度分數計算

**資料來源**: references/data-sources.md
- Yahoo Finance（PL=F, EWZ）
- 頻率處理與對齊
- 備援數據源

**輸入參數**: references/input-schema.md
- 完整參數定義與預設值
- start_date, frequency, corr_window, lead_lag_max 等

</reference_index>

<workflows_index>
| Workflow     | Purpose        | 使用時機                  |
|--------------|----------------|---------------------------|
| analyze.md   | 完整傳導分析   | 需要驗證傳導敘事時        |
| visualize.md | 生成視覺化圖表 | 需要 Bloomberg 風格圖表時 |
</workflows_index>

<templates_index>
| Template           | Purpose           |
|--------------------|-------------------|
| output-json.md     | JSON 輸出結構定義 |
| output-markdown.md | Markdown 報告模板 |
</templates_index>

<scripts_index>
| Script        | Command                                  | Purpose              |
|---------------|------------------------------------------|----------------------|
| analyze.py    | `--start DATE [--end DATE] [--freq 1wk]` | 完整傳導分析         |
| fetch_data.py | `--start DATE [--end DATE] [--freq 1wk]` | 數據抓取與快取       |
| visualize.py  | `--start DATE [--end DATE]`              | Bloomberg 風格視覺化 |
</scripts_index>

<input_schema>

<parameter name="start_date" required="true">
**Type**: string (ISO YYYY-MM-DD)
**Description**: 分析起始日期
**Example**: "2003-01-01"
**Note**: EWZ 上市於 2000 年 7 月，建議不早於 2000-07-01
</parameter>

<parameter name="end_date" required="false">
**Type**: string (ISO YYYY-MM-DD)
**Description**: 分析結束日期（預設今日）
**Example**: "2026-01-28"
</parameter>

<parameter name="frequency" required="false">
**Type**: string
**Default**: "1wk"
**Options**: "1d" / "1wk" / "1mo"
**Description**: 資料頻率。建議 1wk 或 1mo 用於長週期分析
</parameter>

<parameter name="platinum_ticker" required="false">
**Type**: string
**Default**: "PL=F"
**Description**: 白金價格 ticker
</parameter>

<parameter name="brazil_ticker" required="false">
**Type**: string
**Default**: "EWZ"
**Description**: 巴西股市 proxy ticker
</parameter>

<parameter name="normalize_base" required="false">
**Type**: number
**Default**: 100
**Description**: 正規化基準
</parameter>

<parameter name="corr_window" required="false">
**Type**: int
**Default**: 52
**Description**: Rolling correlation 視窗（以 frequency 單位）
</parameter>

<parameter name="lead_lag_max" required="false">
**Type**: int
**Default**: 52
**Description**: 領先/落後最大掃描期數
</parameter>

<parameter name="regime_window" required="false">
**Type**: int
**Default**: 104
**Description**: 長期 regime 判斷窗口
</parameter>

<parameter name="output_mode" required="false">
**Type**: string
**Default**: "both"
**Options**: "markdown" / "json" / "both"
</parameter>

</input_schema>

<output_schema>
參見 `templates/output-json.md` 的完整結構定義。

**摘要**：
```json
{
  "signal": "transmission_strong | transmission_moderate | transmission_weak | inconclusive",
  "confidence": "high | medium | low",
  "transmission_strength_score": 74,
  "best_lead_lag": {
    "lag_weeks": 12,
    "corr": 0.52,
    "meaning": "Platinum leads EWZ by ~12 weeks"
  },
  "rolling_corr": {
    "window": 52,
    "latest": 0.41,
    "positive_share_5y": 0.68
  },
  "regime_label": "linked_upcycle | decoupled | brazil_idiosyncratic",
  "monitoring_notes": ["..."],
  "artifacts": {
    "charts": ["output/platinum_vs_ewz_YYYY-MM-DD.png"]
  }
}
```
</output_schema>

<success_criteria>
分析成功時應產出：

- [ ] 白金與 EWZ 的領先落後天（週）數與相關係數
- [ ] 52 週 Rolling Correlation 最新值與正值佔比
- [ ] 傳導強度分數（0-100）
- [ ] 當前 Regime Label（linked_upcycle / decoupled / brazil_idiosyncratic）
- [ ] 傳導結論與替代解釋
- [ ] 監控清單（非短線）
- [ ] **Bloomberg 風格雙軸圖**（output/platinum_vs_ewz_YYYY-MM-DD.png）
- [ ] 明確標註資料限制與假設
</success_criteria>
