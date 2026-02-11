---
name: track-equity-cumulative-return
version: 1.1.0
updated: 2026-01-28
description: Track cumulative return of stocks/indices with multi-ticker comparison, index Top N ranking, and visualization. All comparisons use S&P 500 as the fixed benchmark.
---

<essential_principles>

<principle name="sp500_benchmark">
**S&P 500 Fixed Benchmark (Core Methodology)**

All cumulative return analyses use S&P 500 (^GSPC) as the fixed benchmark. This is a core methodology decision:

- S&P 500 represents the broad US equity market
- Provides consistent, comparable baseline across all analyses
- "vs Benchmark" = Stock Return - S&P 500 Return
- Positive vs Benchmark indicates outperformance (Alpha)

**This is hardcoded and cannot be changed.**
</principle>

<principle name="base_date_methodology">
**Base Date Methodology**

For cumulative return calculation, the base date is the **last trading day of the previous year**:

```
Cumulative Return = ((Final Price / Base Price) - 1) × 100%
```

**Key methodology**:
- Analyzing 2024 → Base date is 2023-12-29 (last trading day of 2023)
- This captures the true return from year-end investment to period end

All tickers are aligned to common trading days with data.
</principle>

<principle name="four_scenarios">
**Four Analysis Scenarios**

This skill supports 4 distinct scenarios:

| Scenario | Mode                       | Description                                     | Example                             |
|----------|----------------------------|-------------------------------------------------|-------------------------------------|
| **1.a**  | Stock(s), Year Only        | Analyze specific tickers for a single full year | NVDA, AMD in 2024 only              |
| **1.b**  | Stock(s), Year to Today    | Analyze specific tickers from a year to today   | NVDA, AMD from 2022 to today        |
| **2.a**  | Index Top N, Year Only     | Rank index components for a single full year    | Nasdaq 100 Top N in 2024 only       |
| **2.b**  | Index Top N, Year to Today | Rank index components from a year to today      | Nasdaq 100 Top N from 2022 to today |

Use `--year-only` flag to switch between "Year Only" (a) and "Year to Today" (b) modes.
</principle>

<principle name="supported_indices">
**Supported Index Components**

| Index Code | Name                             | Components |
|------------|----------------------------------|------------|
| nasdaq100  | Nasdaq 100 Index                 | ~100       |
| sp100      | S&P 100 Index                    | 100        |
| dow30      | Dow Jones 30 Index               | 30         |
| sox        | Philadelphia Semiconductor Index | 30         |

Top N analysis fetches all component stocks and ranks by return.
</principle>

</essential_principles>

<objective>
Track cumulative return performance of stocks and indices:

1. **Fetch Data**: Get historical prices from Yahoo Finance (with caching)
2. **Calculate Returns**: Cumulative return
3. **Benchmark Comparison**: Compare against S&P 500 (fixed)
4. **Rank Analysis**: Index component Top N performance ranking
5. **Visualization**: dark theme PNG charts

Output: Cumulative return time series chart, performance ranking table, JSON data, Markdown report.
</objective>

<quick_start>

**Quick Start: Analyze Stock Cumulative Returns**

```bash
cd skills/track-equity-cumulative-return/scripts
pip install pandas numpy yfinance matplotlib  # First time only

# Scenario 1.a: Stock(s), 2024 Year Only
python cumulative_return_analyzer.py --ticker NVDA AMD --year 2024 --year-only

# Scenario 1.b: Stock(s), 2022 to Today
python cumulative_return_analyzer.py --ticker NVDA AMD GOOGL --year 2022

# Scenario 2.a: Nasdaq 100 Top 10, 2024 Year Only
python index_component_analyzer.py --index nasdaq100 --year 2024 --year-only --top 10

# Scenario 2.b: Nasdaq 100 Top 20, 2022 to Today
python index_component_analyzer.py --index nasdaq100 --year 2022 --top 20

# Visualization (with charts)
python visualize_cumulative.py --ticker NVDA AMD --year 2024 --year-only
python visualize_cumulative.py --mode top20 --index nasdaq100 --year 2022 --top 20
```

Sample output:
```json
{
  "skill": "track-equity-cumulative-return",
  "as_of": "2026-01-28",
  "mode": "year_to_today",
  "parameters": {
    "tickers": ["NVDA", "AMD"],
    "start_year": 2022,
    "year_only": false
  },
  "benchmark": {
    "ticker": "^GSPC",
    "name": "S&P 500",
    "cumulative_return_pct": 45.2
  },
  "summary": {
    "best_performer": "NVDA",
    "best_return": 542.2,
    "beat_benchmark_count": 2
  }
}
```

</quick_start>

<intake>
What analysis do you need?

**Scenario Selection**:

1. **Scenario 1.a** - Analyze stock(s) for a specific year only (e.g., "NVDA in 2024 full year")
2. **Scenario 1.b** - Analyze stock(s) from a year to today (e.g., "NVDA from 2022 to today")
3. **Scenario 2.a** - Index Top N for a specific year only (e.g., "Nasdaq 100 Top N in 2024")
4. **Scenario 2.b** - Index Top N from a year to today (e.g., "Nasdaq 100 Top N since 2022")
5. **Methodology** - Learn about cumulative return calculation

**Provide your analysis parameters or select a scenario.**
</intake>

<routing>
| User Input                         | Scenario | Command                                                                                 |
|------------------------------------|----------|-----------------------------------------------------------------------------------------|
| "NVDA 2024 full year", "2024 only" | **1.a**  | `python cumulative_return_analyzer.py --ticker NVDA --year 2024 --year-only`            |
| "NVDA from 2022", "since 2022"     | **1.b**  | `python cumulative_return_analyzer.py --ticker NVDA --year 2022`                        |
| "Nasdaq 100 top 10 2024 only"      | **2.a**  | `python index_component_analyzer.py --index nasdaq100 --year 2024 --year-only --top 10` |
| "Nasdaq 100 top 20 since 2022"     | **2.b**  | `python index_component_analyzer.py --index nasdaq100 --year 2022 --top 20`             |
| "chart", "visualization"           | Add      | `python visualize_cumulative.py` with same parameters                                   |
| "methodology", "how"               | Info     | Read `references/methodology.md`                                                        |

**Key flags**:
- `--year-only`: Analyze only the specified year (scenarios a)
- Without `--year-only`: Analyze from year to today (scenarios b)
- `--top N`: Select Top N for index analysis

**All scripts use Yahoo Finance real data with caching. Benchmark is always S&P 500.**
</routing>

<reference_index>
**Reference Documents** (`references/`)

| File                | Content                                  |
|---------------------|------------------------------------------|
| methodology.md      | Cumulative return calculation methodology |
| data-sources.md     | Yahoo Finance data source documentation   |
| input-schema.md     | Complete input parameter definitions      |
| index-components.md | Supported index component lists           |
</reference_index>

<workflows_index>
| Workflow       | Scenario | Use Case                  |
|----------------|----------|---------------------------|
| quick-check.md | 1.a/1.b  | Quick check single ticker |
| compare.md     | 1.a/1.b  | Compare multiple tickers  |
| top20.md       | 2.a/2.b  | Index Top N analysis      |
</workflows_index>

<templates_index>
| Template           | Purpose                          |
|--------------------|----------------------------------|
| output-json.md     | JSON output structure definition |
| output-markdown.md | Markdown report template         |
</templates_index>

<scripts_index>
| Script                        | Command Example                    | Purpose                                 |
|-------------------------------|------------------------------------|-----------------------------------------|
| fetch_price_data.py           | `--ticker NVDA --start 2022-01-01` | Yahoo Finance data fetching             |
| cumulative_return_analyzer.py | `--ticker NVDA AMD --year 2022`    | Cumulative return calculation (1.a/1.b) |
| index_component_analyzer.py   | `--index nasdaq100 --year 2022`    | Index component analysis (2.a/2.b)      |
| visualize_cumulative.py       | `--ticker NVDA AMD --year 2022`    | visualization                           |
</scripts_index>

<input_schema_summary>

**Required Parameters**

| Parameter | Type   | Description                       |
|-----------|--------|-----------------------------------|
| ticker    | string | Stock ticker(s) - can be multiple |
| year      | int    | Start year                        |

**Optional Parameters**

| Parameter | Type   | Default   | Description                             |
|-----------|--------|-----------|-----------------------------------------|
| year-only | flag   | false     | If set, analyze only the specified year |
| index     | string | nasdaq100 | Index type (for Top N mode)             |
| top       | int    | 20        | Top N to select                         |
| output    | string | auto      | Output file path                        |
| mode      | string | compare   | Mode (compare/top20)                    |

**Note**: Benchmark is hardcoded to S&P 500 (^GSPC) and cannot be changed.

See `references/input-schema.md` for complete parameter definitions.

</input_schema_summary>

<visualization>

**Chart Specifications**

Charts follow `thoughts/shared/guide/bloomberg-style-chart-guide.md`:

- **Background**: `#1a1a2e` (dark blue-black)
- **Grid**: `#2d2d44` (dark gray-purple)
- **Primary lines**: `#ff6b35` (orange-red), `#ffaa00` (orange-yellow)
- **Benchmark line**: `#004E89` (deep blue dashed)
- **Zero line**: `#666666` (gray dotted)

**X-axis format**:
- January: Show year (e.g., "2024")
- February-December: Show month number (e.g., "2", "3", ... "12")

Output specs:
- Size: 14×8 inches (compare) / 16×10 inches (top20)
- Resolution: 150 dpi
- Format: PNG

</visualization>

<output_schema_summary>
```json
{
  "skill": "track-equity-cumulative-return",
  "as_of": "2026-01-28",
  "mode": "year_to_today",
  "parameters": {
    "tickers": ["NVDA", "AMD"],
    "start_year": 2022,
    "year_only": false
  },
  "period": {
    "start_date": "2021-12-31",
    "end_date": "2026-01-28",
    "years_held": 4.08
  },
  "benchmark": {
    "ticker": "^GSPC",
    "name": "S&P 500",
    "cumulative_return_pct": 45.2
  },
  "summary": {
    "best_performer": "NVDA",
    "best_return": 542.2,
    "benchmark_return": 45.2,
    "beat_benchmark_count": 2
  },
  "results": [
    {
      "ticker": "NVDA",
      "name": "NVIDIA (NVDA)",
      "cumulative_return_pct": 542.2,
      "vs_benchmark": 497.0
    }
  ],
  "chart_path": "output/cumulative_return_2026-01-28.png"
}
```

See `templates/output-json.md` for complete output structure.
</output_schema_summary>

<success_criteria>
Successful execution should produce:

- [ ] Cumulative return time series data
- [ ] Cumulative return for each ticker
- [ ] Comparison against S&P 500 benchmark (vs benchmark)
- [ ] Performance ranking (sorted by return descending)
- [ ] Beat benchmark statistics
- [ ] visualization chart (output/*.png)
- [ ] JSON result output (optional)

**Chart X-axis**: Year shown in January, month numbers (2-12) for other months.
</success_criteria>

<extended_examples>

**Example 1: Single Stock Full Year Analysis (Scenario 1.a)**

Analyze NVIDIA's performance in 2024:

```bash
cd skills/track-equity-cumulative-return/scripts
python cumulative_return_analyzer.py --ticker NVDA --year 2024 --year-only
```

Expected output:
```
==========================================================================================
Cumulative Return Analysis Report
==========================================================================================
Period: 2024 Full Year (2023-12-29 ~ 2024-12-31)
Benchmark: S&P 500
==========================================================================================

Rank  Ticker  Name                 Cum. Return   vs Bench
----------------------------------------------------------------------
1     NVDA    NVIDIA (NVDA)          +185.52%  +160.97% ✓
----------------------------------------------------------------------
Bench ^GSPC   S&P 500                 +24.54%
==========================================================================================

Statistics:
  - Best performer: NVDA (+185.52%)
  - Beat benchmark: 1 / 1
```

**Example 2: Multi-Stock Long-Term Comparison (Scenario 1.b)**

Compare FAANG stocks from 2020 to today:

```bash
python cumulative_return_analyzer.py --ticker META AAPL AMZN NFLX GOOGL --year 2020
python visualize_cumulative.py --ticker META AAPL AMZN NFLX GOOGL --year 2020
```

**Example 3: Semiconductor Index Top 10 (Scenario 2.a)**

Find top 10 semiconductor performers in 2024:

```bash
python index_component_analyzer.py --index sox --year 2024 --year-only --top 10
python visualize_cumulative.py --mode top20 --index sox --year 2024 --year-only --top 10
```

**Example 4: Dow 30 Long-Term Analysis (Scenario 2.b)**

Analyze Dow 30 components from 2020:

```bash
python index_component_analyzer.py --index dow30 --year 2020 --top 30
```

</extended_examples>

<error_handling>

**Input Validation**

The skill includes comprehensive input validation:

- **Ticker validation**: Checks format, applies corrections (e.g., `BRK.B` → `BRK-B`, `FB` → `META`)
- **Year validation**: Must be between 1970 and current year
- **Index validation**: Must be one of: `nasdaq100`, `sp100`, `dow30`, `sox`
- **Top N validation**: Must be positive integer ≤ 100

**Network Retry Logic**

Yahoo Finance API calls include automatic retry:

- Up to 3 retry attempts
- Exponential backoff (2s, 3s, 4.5s delays)
- Clear error messages on failure

**Data Quality Checks**

- Minimum data points required (5 rows)
- NaN percentage threshold (max 10%)
- Invalid price detection (non-positive values)
- Automatic data cleaning with warnings

</error_handling>

<testing>

**Running Tests**

```bash
cd skills/track-equity-cumulative-return/scripts/tests
python test_calculations.py
```

**Test Coverage**:

1. **Cumulative return formula** - Validates calculation accuracy
2. **Cumulative return series** - Validates time series generation
3. **Validators** - Tests all input validation functions
4. **Golden cases** - Structure validation of expected results

**Golden Cases**

Located in `scripts/tests/golden_cases.json`:

- NVDA 2024 full year (expected: 170-190% return)
- AMD 2024 full year (expected: -20% to -10% return)
- S&P 500 2024 benchmark (expected: 20-28% return)

</testing>

<data_governance>

**Data Sources**

| Source        | Type    | Caching       | Notes            |
|---------------|---------|---------------|------------------|
| Yahoo Finance | Primary | 12-hour cache | Free, public API |

**Caching**

- Cache directory: `scripts/cache/`
- Cache format: Parquet (efficient storage)
- Cache validity: 12 hours
- Clear cache: `python fetch_price_data.py --clear-cache`

**Known Limitations**

1. **Survivorship bias**: Index components are current, not historical
2. **Price-only returns**: Does not include dividends
3. **Yahoo Finance rate limits**: Heavy usage may be throttled

</data_governance>
