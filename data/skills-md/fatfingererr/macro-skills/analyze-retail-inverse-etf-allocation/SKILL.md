---
name: analyze-retail-inverse-etf-allocation
description: 以槓桿反向 ETF（做空）相對槓桿正向 ETF（做多）的交易占比，作為散戶風險偏好代理指標，評估 SPX 後續下行風險。
---

<essential_principles>
**散戶槓桿反向 ETF 做空配置分析 核心原則**

<principle name="dollar_volume_ratio_as_proxy">
**以美元成交量比率作為散戶做空配置代理**
槓桿 ETF 交易以短線散戶為主，反向群組（SPXU/SDS/SH）的美元成交量占比越低，代表散戶避險/看空參與度越低，市場越自滿（complacency）。公式：`short_alloc = inv_dollar_vol / (inv_dollar_vol + long_dollar_vol)`。
</principle>

<principle name="percentile_normalization">
**分位數標準化**
將做空配置比率以滾動分位數標準化（預設回看 260 週 ≈ 5 年），轉為 0~1 的分位數。分位數 ≤ 5% 為「極低做空配置」觸發條件，代表自滿程度極高。
</principle>

<principle name="event_study_forward_risk">
**事件研究與前瞻風險評估**
找出歷史上做空配置極低的事件日期，計算每次事件後的前瞻報酬、最大回撤、波動率。彙總命中率（如 63 天內最大回撤 ≤ -8% 的比例）與中位數風險，作為當前風險分布的參考。
</principle>

<principle name="analog_matching">
**歷史類比匹配**
取最近 N 次（預設 4 次）歷史觸發事件作為類比案例，比較當前狀態與歷史情境的相似度，評估前瞻下行風險的一致性。
</principle>

<principle name="signal_not_timing">
**風險分布訊號，非精準擇時**
此指標反映「散戶自滿程度偏高時，下行風險的條件分布偏差」，不是精準的頂部擇時工具。結論必須附帶 caveat：proxy 可能混入機構對沖/做市流量。
</principle>

<principle name="data_transparency">
**資料透明度**
所有資料來源為公開市場行情（Yahoo Finance），使用美元成交量（Close × Volume）重建。若使用 AUM proxy 需額外資料。明確標示資料覆蓋率與 ETF 上市日期限制。
</principle>
</essential_principles>

<objective>
**目標**：量化散戶透過槓桿反向 ETF 的做空參與度，偵測「自滿」極端值，並以事件研究法評估 SPX 後續下行風險。

**步驟**：
1. 下載反向/正向槓桿 ETF 與基準指數的 OHLCV 資料
2. 計算美元成交量比率（或 AUM proxy）作為做空配置指標
3. 以滾動分位數標準化，偵測極低做空配置事件
4. 找出歷史類比事件，計算前瞻風險統計
5. 產生結論與圖表

**不適用情境**：
- 非美股市場（ETF 標的不同）
- 極短期日內交易擇時
- 機構級避險策略監控（本指標偏散戶行為）
</objective>

<quick_start>
**快速開始**

```bash
# 安裝依賴
pip install yfinance pandas numpy matplotlib

# 完整分析（預設參數）
python scripts/inverse_etf_analyzer.py --start 2012-01-01 --end 2026-02-01

# 快速檢查當前狀態
python scripts/inverse_etf_analyzer.py --start 2012-01-01 --end 2026-02-01 --quick

# 自訂 ETF 清單
python scripts/inverse_etf_analyzer.py --start 2012-01-01 --end 2026-02-01 \
  --inverse SPXU SDS SH --long UPRO SSO SPY
```
</quick_start>

<intake>
**您想要執行什麼分析？**

1. **完整分析** - 計算做空配置比率、偵測極端值、事件研究、前瞻風險統計
2. **視覺化** - 產生 SPX + 做空配置 + 事件標記圖表
3. **歷史事件對照** - 列出歷史上做空配置極低的事件及後續市場表現
4. **快速檢查** - 僅查看當前做空配置狀態與分位數

**等待回應後再繼續。**
</intake>

<routing>
| Response                              | Workflow                          | Description                              |
|---------------------------------------|-----------------------------------|------------------------------------------|
| 1, "完整分析", "full", "analyze"      | workflows/analyze.md              | 完整分析流程：資料→指標→事件→風險→結論   |
| 2, "視覺化", "chart", "visualize"     | workflows/visualize.md            | 產生圖表：SPX + 做空配置 + 事件標記      |
| 3, "歷史", "episodes", "history"      | workflows/historical-episodes.md  | 歷史事件對照與前瞻表現統計               |
| 4, "快速", "quick", "check"           | workflows/analyze.md              | 快速模式：僅當前狀態                     |

**讀取工作流程後，請完全遵循其步驟。**
</routing>

<reference_index>
**參考文件** (`references/`)

| 文件 | 內容 |
|------|------|
| methodology.md | 做空配置比率計算方法、分位數標準化、事件研究框架 |
| data-sources.md | 資料來源說明（Yahoo Finance ETF OHLCV）、fallback、授權 |
| input-schema.md | 所有輸入參數定義、型別、預設值、驗證規則 |
</reference_index>

<workflows_index>
| Workflow | Purpose |
|----------|---------|
| analyze.md | 完整分析工作流（資料取得→指標計算→事件偵測→風險統計→結論生成） |
| visualize.md | 圖表生成工作流（SPX + 做空配置雙軸圖 + 事件垂直線） |
| historical-episodes.md | 歷史事件對照工作流（列出過去觸發事件與後續表現） |
</workflows_index>

<templates_index>
| Template | Purpose |
|----------|---------|
| output-json.md | JSON 輸出模板（程式/儀表板消費） |
| output-markdown.md | Markdown 輸出模板（人類閱讀/社群分享） |
</templates_index>

<scripts_index>
| Script | Purpose |
|--------|---------|
| inverse_etf_analyzer.py | 主分析腳本：資料取得、指標計算、事件偵測、風險統計 |
| visualize_allocation.py | 視覺化腳本：雙軸圖表生成 |
</scripts_index>

<success_criteria>
Skill 成功執行時：
- [ ] 成功下載所有指定 ETF 的 OHLCV 資料
- [ ] 計算出做空配置比率（short_alloc）與分位數
- [ ] 偵測出歷史觸發事件（若存在）
- [ ] 計算每次事件的前瞻風險統計
- [ ] 產生 JSON + Markdown 結論輸出
- [ ] 結論包含 caveat（風險分布訊號，非擇時工具）
</success_criteria>

<examples_index>
**範例輸出** (`examples/`)

| 文件 | 內容 |
|------|------|
| sample_output.json | 完整分析的 JSON 範例輸出 |
</examples_index>
