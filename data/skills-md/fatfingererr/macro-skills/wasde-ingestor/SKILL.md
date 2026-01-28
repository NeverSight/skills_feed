---
name: wasde-ingestor
description: 下載並解析 USDA 每月發布的 WASDE 報告，擷取所有主要商品（穀物、油籽、棉花、畜產品、糖）的供需平衡表。輸出標準化、可版本化的資料集，作為即時預測（nowcasting）的錨定基準。
---

<essential_principles>
**WASDE Ingestor 核心原則**

**1. 商品範圍**

WASDE 涵蓋三大類商品，每類有不同的表格結構與單位：

| 類別      | 商品                                     | US 單位                   | World 單位           |
|-----------|------------------------------------------|---------------------------|----------------------|
| Grains    | Wheat, Corn, Rice, Barley, Sorghum, Oats | million bushels / cwt     | million metric tons  |
| Oilseeds  | Soybeans, Soybean Oil, Soybean Meal      | million bushels / pounds  | million metric tons  |
| Cotton    | Upland, Pima                             | million 480-lb bales      | million 480-lb bales |
| Livestock | Beef, Pork, Poultry, Eggs, Dairy         | million lbs / dozen / lbs | - (US only)          |
| Sugar     | Sugar                                    | 1,000 short tons          | - (US + Mexico only) |

**2. 表格結構一致性**

所有供需表遵循相同的平衡公式：
```
Ending Stocks = Beginning Stocks + Production + Imports - Total Use - Exports
```

**3. 版本控制**

- 每月報告可能修正前期數據
- 使用 `content_hash` 追蹤數據變化
- 保留 `revision_flag` 標記修正值

**4. 解析優先級**

1. PDF 結構化解析（優先）
2. HTML 表格解析（fallback）
3. TXT 固定寬度解析（legacy）
</essential_principles>

<intake>
**您想要執行什麼操作？**

1. **Ingest** - 抓取並解析最新或指定月份的 WASDE 報告
2. **Backfill** - 批量回補歷史 WASDE 數據
3. **Validate** - 驗證現有數據與最新報告的一致性
4. **Configure** - 配置商品範圍、輸出路徑等參數

**等待回應後再繼續。**
</intake>

<routing>
| Response                                | Workflow               | Description         |
|-----------------------------------------|------------------------|---------------------|
| 1, "ingest", "fetch", "parse", "latest" | workflows/ingest.md    | 抓取解析 WASDE 報告 |
| 2, "backfill", "historical", "batch"    | workflows/backfill.md  | 批量回補歷史數據    |
| 3, "validate", "check", "verify"        | workflows/validate.md  | 驗證數據一致性      |
| 4, "configure", "config", "setup"       | workflows/configure.md | 配置參數            |

**讀取工作流程後，請完全遵循其步驟。**
</routing>

<reference_index>
**商品參考文件** (`references/`)

| 文件                    | 內容                                               |
|-------------------------|----------------------------------------------------|
| commodities-overview.md | 所有商品總覽與單位對照                             |
| grains.md               | 穀物類（Wheat, Corn, Rice, Barley, Sorghum, Oats） |
| oilseeds.md             | 油籽類（Soybeans, Soybean Oil, Soybean Meal）      |
| cotton.md               | 棉花（US & World）                                 |
| livestock.md            | 畜產品（Beef, Pork, Poultry, Eggs, Dairy）         |
| sugar.md                | 糖（US & Mexico）                                  |
| validation-rules.md     | 驗證規則與合理性檢查                               |
| failure-modes.md        | 失敗模式與緩解策略                                 |
</reference_index>

<workflows_index>
| Workflow     | Purpose                       |
|--------------|-------------------------------|
| ingest.md    | 抓取解析單一或多個 WASDE 報告 |
| backfill.md  | 批量回補歷史數據              |
| validate.md  | 驗證數據一致性與修正追蹤      |
| configure.md | 配置商品範圍與輸出設定        |
</workflows_index>

<templates_index>
| Template                  | Purpose             |
|---------------------------|---------------------|
| config.yaml               | 標準配置文件模板    |
| us-balance-schema.yaml    | US 供需表 schema    |
| world-balance-schema.yaml | World 供需表 schema |
</templates_index>

<scripts_index>
| Script               | Purpose                   |
|----------------------|---------------------------|
| discover_releases.py | 發現 WASDE 發布日期與 URL |
| fetch_report.py      | 下載 PDF/HTML 報告        |
| parse_tables.py      | 解析表格提取數據          |
| validate_data.py     | 執行驗證檢查              |
</scripts_index>

<examples_index>
**範例輸出** (`examples/`)

| 文件                       | 內容                   |
|----------------------------|------------------------|
| corn_us_balance.json       | 美國玉米供需平衡表範例 |
| wheat_world_balance.json   | 世界小麥供需平衡表範例 |
| ingest_status_success.json | 成功執行的狀態報告範例 |
| backfill_result.json       | 批量回補作業結果範例   |
</examples_index>

<quick_start>
**CLI 快速開始：**

```bash
# 抓取最新報告的所有商品
macro-skills wasde ingest --commodities=all --out=./data

# 只抓取穀物類
macro-skills wasde ingest --commodities=grains --out=./data

# 回補過去 24 個月的大豆數據
macro-skills wasde backfill --commodity=soybeans --months=24 --out=./data

# 驗證現有數據
macro-skills wasde validate --data-dir=./data
```

**Library 快速開始：**

```python
from macro_skills.wasde import WASDEIngestor

ingestor = WASDEIngestor(
    commodities=["wheat", "corn", "soybeans"],
    scope=["us", "world"],
    output_dir="./data/wasde"
)

result = ingestor.ingest_latest()
print(result.status)
```
</quick_start>

<success_criteria>
Skill 成功執行時：
- [ ] 正確識別商品類別與對應表格
- [ ] 解析所有指定商品的供需數據
- [ ] 單位正確轉換與標記
- [ ] 通過平衡公式驗證
- [ ] 輸出標準化 parquet 數據集
- [ ] 生成 ingest_status 報告
</success_criteria>

<detailed_usage_examples>
**詳細使用範例**

**範例 1：抓取最新玉米與大豆數據**
```
User: 幫我抓取最新 WASDE 的玉米和大豆供需數據

Assistant 執行步驟:
1. 讀取 workflows/ingest.md
2. 呼叫 discover_releases.py 找到最新發布 (2025-01-10)
3. 下載 PDF 報告
4. 解析 corn_us, corn_world, soybeans_us, soybeans_world 表格
5. 驗證平衡公式
6. 輸出 parquet 檔案
7. 回報 ingest_status

預期輸出:
- ./data/wasde/curated/corn_us_balance.parquet
- ./data/wasde/curated/corn_world_balance.parquet
- ./data/wasde/curated/soybeans_us_balance.parquet
- ./data/wasde/curated/soybeans_world_balance.parquet
```

**範例 2：回補歷史小麥數據並追蹤修正**
```
User: 回補過去 12 個月的小麥數據，我想追蹤 USDA 的修正歷程

Assistant 執行步驟:
1. 讀取 workflows/backfill.md
2. 確定日期範圍 (2024-01 至 2024-12)
3. 依序處理 12 期報告
4. 比對每期數據，標記修正值
5. 輸出包含 revision_flag 的完整歷史數據

預期輸出:
- 12 期小麥數據
- 修正追蹤報告
```

**範例 3：驗證現有數據一致性**
```
User: 檢查我現有的 WASDE 數據是否與最新報告一致

Assistant 執行步驟:
1. 讀取 workflows/validate.md
2. 載入現有 parquet 檔案
3. 抓取最新報告
4. 逐欄位比對
5. 標記差異與修正
6. 輸出驗證報告

預期輸出:
- validation_report.json (差異列表)
- 修正建議
```
</detailed_usage_examples>

<data_pipeline_architecture>
**數據流水線架構**

```
[USDA WASDE Website]
         |
         v
+-------------------+
| discover_releases |  --> 找到 PDF URL 與發布日期
+-------------------+
         |
         v
+-------------------+
|   fetch_report    |  --> 下載 PDF (fallback: HTML)
+-------------------+
         |
         v
+-------------------+
|   parse_tables    |  --> 提取供需表格數據
+-------------------+
         |
         v
+-------------------+
|   normalize_data  |  --> 標準化欄位與單位
+-------------------+
         |
         v
+-------------------+
|   validate_data   |  --> 平衡公式與範圍檢查
+-------------------+
         |
         v
+-------------------+
|   write_output    |  --> Parquet / JSON
+-------------------+
         |
         v
[Curated Dataset]
```

**目錄結構：**
```
data/wasde/
├── raw/                    # 原始 PDF 檔案
│   └── 2025-01-10/
│       └── wasde0125.pdf
├── intermediate/           # 中間解析結果
│   └── 2025-01-10/
│       ├── tables.json
│       └── ingest_status.json
└── curated/                # 最終標準化數據
    ├── corn_us_balance.parquet
    ├── corn_world_balance.parquet
    ├── wheat_us_balance.parquet
    └── ...
```
</data_pipeline_architecture>
