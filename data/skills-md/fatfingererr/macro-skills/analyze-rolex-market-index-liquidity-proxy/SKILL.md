---
name: analyze-rolex-market-index-liquidity-proxy
description: 用勞力士市場指數（WatchCharts Rolex Market Index）作為高 β 的風險偏好／流動性代理，判讀「流動性改善但未到投機狂熱」的狀態
---

<essential_principles>
**以勞力士指數分析流動性投機程度 核心原則**

<principle name="rolex_as_liquidity_proxy">
**勞力士市場指數是全球流動性與財富效應的高 β 代理**
勞力士二級市場價格對流動性環境極為敏感。當全球流動性擴張時，勞力士二手錶價格率先上漲；當流動性收縮時，也率先下跌。其波動幅度（β）遠高於傳統金融資產，是觀察流動性週期的敏感指標。
</principle>

<principle name="grinding_vs_fever">
**區分「緩慢磨高」與「投機狂熱」**
- **Grinding Higher（緩慢磨高）**：斜率為正、價格在均線之上、但距離歷史峰值仍遠。代表流動性改善的早中期階段。
- **Speculative Fever（投機狂熱）**：z-score 極端（≥2.0）、實質利率為負或大幅下行、流動性加速擴張。代表 2021/22 式的泡沫頂部。
</principle>

<principle name="net_liquidity_formula">
**Fed 淨流動性公式**
```
Net Liquidity ≈ WALCL − RRPONTSYD − WTREGEN
```
- WALCL：Fed 資產負債表總資產
- RRPONTSYD：隔夜逆回購（ON RRP）
- WTREGEN：美國財政部一般帳戶（TGA）

淨流動性上升 → 金融體系實際可用資金增加 → 風險資產與勞力士二級市場受益
</principle>

<principle name="real_yield_regime">
**實質利率區間決定 β 強度**
在不同 DFII10（10Y TIPS 實質利率）區間下，勞力士市場指數對流動性的敏感度不同：
- DFII10 < 0（負實質利率）：高 β，最容易出現投機狂熱
- DFII10 ≈ 0~1%（接近零）：中 β，改善中但未到狂熱
- DFII10 > 1.5%（正高檔）：低 β，流動性改善效果被高利率壓制
</principle>

<principle name="data_provenance">
**數據可重現性優先**
勞力士市場指數透過 Chrome CDP 自動從 WatchCharts 頁面抓取，本地快取 TTL 24 小時。FRED 數據（DFII10、WALCL、RRPONTSYD、WTREGEN）透過公開 CSV endpoint 取得，確保完全可重現。
</principle>
</essential_principles>

<objective>
**分析目標**

以勞力士市場指數為核心，對照 Fed 淨流動性與實質利率，完成以下判斷：

1. **確認參數**：時間範圍、頻率、流動性模型
2. **取得數據**：從 FRED 取得流動性與利率數據，透過 CDP 抓取勞力士市場指數
3. **計算指標**：z-score、滾動斜率、滾動 β、距峰值距離
4. **判讀狀態**：grinding_higher（緩慢磨高）或 speculative_fever（投機狂熱）
5. **產出報告**：結構化 JSON + Markdown 摘要
6. **提供建議**：下一步監控重點與交叉驗證方向
</objective>

<quick_start>
**快速開始**

```bash
# 1. 安裝依賴
pip install pandas numpy requests websocket-client matplotlib

# 2. 啟動 Chrome 調試模式並開啟 WatchCharts 頁面
#    Windows:
#      "C:\Program Files\Google\Chrome\Application\chrome.exe" ^
#        --remote-debugging-port=9222 ^
#        --remote-allow-origins=* ^
#        --user-data-dir="%USERPROFILE%\.chrome-debug-profile" ^
#        "https://watchcharts.com/watches/brand_index/rolex"
#
#    macOS:
#      /Applications/Google\ Chrome.app/Contents/MacOS/Google\ Chrome \
#        --remote-debugging-port=9222 \
#        --remote-allow-origins=* \
#        --user-data-dir="$HOME/.chrome-debug-profile" \
#        "https://watchcharts.com/watches/brand_index/rolex"

# 3. 等待頁面完全載入（圖表顯示），然後執行分析
python scripts/rolex_market_index_analyzer.py \
  --start-date 2019-01-01 \
  --end-date 2026-01-29 \
  --freq W \
  --liquidity-model fed_net_liquidity \
  --cdp-port 9222 \
  --output result.json
```
</quick_start>

<intake>
**您想要分析什麼？**

1. **完整分析** - 從數據取得到狀態判讀的完整流程（推薦）
2. **僅取得數據** - 只取得 FRED 數據與透過 CDP 抓取勞力士市場指數
3. **僅計算指標** - 假設數據已備妥，直接計算所有指標
4. **僅判讀狀態** - 假設指標已計算，判讀 grinding/fever 狀態

**等待回應後再繼續。**
</intake>

<routing>
| Response                         | Workflow             | Description                         |
|----------------------------------|----------------------|-------------------------------------|
| 1, "完整分析", "full", "analyze" | workflows/analyze.md | 完整的端到端分析流程                |
| 2, "取得數據", "fetch", "data"   | workflows/analyze.md | 執行 Step 1~2（數據取得與載入）     |
| 3, "計算指標", "compute"         | workflows/analyze.md | 執行 Step 3~4（指標計算與狀態判讀） |
| 4, "判讀狀態", "interpret"       | workflows/analyze.md | 執行 Step 4~5（狀態判讀與報告產出） |

**讀取工作流程後，請完全遵循其步驟。**
</routing>

<directory_structure>
```
skills/analyze-rolex-market-index-liquidity-proxy/
├── SKILL.md                          # 本檔案（路由與核心原則）
├── skill.yaml                        # 前端展示設定
├── manifest.json                     # 技能元資料
├── workflows/
│   └── analyze.md                    # 主要分析工作流（6 步驟）
├── references/
│   ├── methodology.md                # 方法論（公式、規則、判讀邏輯）
│   ├── input-schema.md               # 輸入參數定義
│   └── data-sources.md               # 數據來源文檔
├── templates/
│   ├── output-json.md                # JSON 輸出模板
│   └── output-markdown.md            # Markdown 報告模板
├── scripts/
│   ├── fetch_rolex_index.py           # CDP 爬蟲（WatchCharts Rolex Index）
│   ├── rolex_market_index_analyzer.py # 主要分析腳本
│   └── rolex_market_index_plotter.py  # 視覺化腳本（選配）
└── examples/
    └── sample-output.json            # 範例輸出
```
</directory_structure>

<reference_index>
**參考文件** (`references/`)

| 文件            | 內容                                                       |
|-----------------|------------------------------------------------------------|
| methodology.md  | 方法論：z-score、滾動斜率、滾動 β、grinding/fever 判讀規則 |
| input-schema.md | 所有輸入參數的定義、型別、預設值、可選值                   |
| data-sources.md | FRED 系列代碼、WatchCharts CDP 抓取、fallback 方案         |
</reference_index>

<workflows_index>
| Workflow   | Purpose                                                                   |
|------------|---------------------------------------------------------------------------|
| analyze.md | 完整分析流程（6 步驟：確認參數→取得數據→計算指標→判讀狀態→產出報告→建議） |
</workflows_index>

<templates_index>
| Template           | Purpose                                                           |
|--------------------|-------------------------------------------------------------------|
| output-json.md     | 結構化 JSON 輸出模板（含 summary、metrics、signals、diagnostics） |
| output-markdown.md | Markdown 報告模板（含 TL;DR、依據、風險、下一步）                 |
</templates_index>

<scripts_index>
| Script                         | Purpose                                                          |
|--------------------------------|------------------------------------------------------------------|
| fetch_rolex_index.py           | CDP 爬蟲：從 WatchCharts 自動抓取 Rolex Market Index             |
| rolex_market_index_analyzer.py | 主要分析腳本：FRED 數據取得、CDP 抓取、指標計算、狀態判讀        |
| rolex_market_index_plotter.py  | 視覺化腳本：雙軸圖（勞力士市場指數 vs 淨流動性）、z-score 熱力圖 |

**執行範例：**
```bash
# 完整分析（需先啟動 Chrome 調試模式並開啟 WatchCharts 頁面）
python scripts/rolex_market_index_analyzer.py \
  --start-date 2019-01-01 \
  --end-date 2026-01-29 \
  --freq W \
  --liquidity-model fed_net_liquidity \
  --cdp-port 9222 \
  --output result.json

# 視覺化（選配）
python scripts/rolex_market_index_plotter.py \
  --input result.json \
  --output-dir output/
```
</scripts_index>

<input_schema_summary>
**輸入參數摘要**

| 參數               | 型別    | 必要 | 預設值              | 說明                     |
|--------------------|---------|------|---------------------|--------------------------|
| start_date         | string  | ✅    | -                   | 分析起始日（YYYY-MM-DD） |
| end_date           | string  | ✅    | -                   | 分析結束日（YYYY-MM-DD） |
| frequency          | string  | ❌    | "W"                 | 頻率：D/W/M              |
| liquidity_scope    | string  | ❌    | "US"                | US 或 GLOBAL             |
| include_real_yield | boolean | ❌    | true                | 是否加入 DFII10          |
| real_yield_series  | string  | ❌    | "DFII10"            | FRED 實質利率代號        |
| liquidity_model    | string  | ❌    | "fed_net_liquidity" | 流動性模型               |
| benchmark_assets   | array   | ❌    | []                  | 參考資產代號             |
| fever_threshold_z  | number  | ❌    | 2.0                 | 投機狂熱 z-score 閾值    |
| grind_window       | int     | ❌    | 13                  | 斜率/均線滾動窗口        |

完整定義請見 `references/input-schema.md`。
</input_schema_summary>

<output_schema_summary>
**輸出結構摘要**

```json
{
  "skill": "analyze_veblen_goods_liquidity_proxy",
  "inputs": { "..." },
  "summary": {
    "state": "grinding_higher | speculative_fever | neutral | declining",
    "interpretation": ["..."]
  },
  "metrics": {
    "latest_index": 28400,
    "pct_below_peak": -0.33,
    "grind_slope": 12.4,
    "rolex_zscore": 0.6,
    "dfii10_level": 1.9,
    "net_liquidity_change": 2.1e10,
    "rolling_beta_vs_net_liquidity": 1.8
  },
  "signals": {
    "grinding_higher": true,
    "speculative_fever": false
  },
  "diagnostics": { "..." }
}
```

完整模板請見 `templates/output-json.md`。
</output_schema_summary>

<success_criteria>
Skill 成功執行時：
- [ ] FRED 數據（DFII10、WALCL、RRPONTSYD、WTREGEN）成功取得
- [ ] WatchCharts Rolex Market Index CDP 自動抓取成功且缺值比例 < 5%
- [ ] 所有頻率對齊完成（resample + forward-fill）
- [ ] z-score、滾動斜率、滾動 β 計算完成
- [ ] grinding_higher / speculative_fever 狀態判讀完成
- [ ] JSON 輸出包含 summary、metrics、signals、diagnostics
- [ ] Markdown 報告包含 TL;DR、依據、風險、下一步
- [ ] 距峰值百分比（pct_below_peak）正確反映當前位置
</success_criteria>
