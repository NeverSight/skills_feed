---
name: chris-stock-master
description: 分析上市公司财报（美/日/港/A股），生成估值分析和投资报告
---

# Stock Master

分析全球上市公司财报，生成结构化报告。

## 触发条件

当用户请求以下内容时使用此 Skill：

- "分析美股AAPL"/ "分析苹果公司"
- "看看港股腾讯的财报" / "分析 0700.HK"
- "茅台估值如何" / "分析 600519.SH"
- 任何关于股票财报、估值、财务分析的请求

## 支持市场

| 市场 | 代码格式 | 示例 |
|------|----------|------|
| 美股 | `SYMBOL` | AAPL, MSFT, GOOGL |
| 日股 | `CODE.T` | 7203.T (丰田) |
| A股 | `CODE.SH/SZ` | 600519.SH (茅台) |
| 港股 | `CODE.HK` | 0700.HK (腾讯) |

## 执行流程

### 1. 环境检查（首次）

```bash
cd "$SKILL_DIR"
if [ ! -d "scripts/.venv" ]; then
  python3 -m venv scripts/.venv
  scripts/.venv/bin/pip install -r scripts/requirements.txt
fi
```

### 2. 运行分析

```bash
cd "$SKILL_DIR"
scripts/.venv/bin/python scripts/run_report.py --symbol <SYMBOL>
```

### 3. 读取并呈现结果

分析完成后，读取生成的报告文件并向用户呈现关键信息：

```bash
SYMBOL="<SYMBOL>"
SYMBOL_SAFE="${SYMBOL//./_}"
cat output/${SYMBOL_SAFE}_*/report.md
```

## 参数说明

| 参数 | 说明 | 默认值 |
|------|------|--------|
| `--symbol` | 股票代码 | 必填 |
| `--years` | 财报年数 | 1 |
| `--output` | 输出根目录（公司子目录会自动创建） | `$SKILL_DIR/output` |
| `--refresh` | 强制刷新缓存 | false |

如需改输出位置，显式传参覆盖默认值：

```bash
cd "$SKILL_DIR"
scripts/.venv/bin/python scripts/run_report.py --symbol <SYMBOL> --output /path/to/output
```

如需尽可能使用最新披露数据，建议：

```bash
cd "$SKILL_DIR"
scripts/.venv/bin/python scripts/run_report.py --symbol <SYMBOL> --years 2 --refresh
```

## 输出文件

每个公司的文件放在独立文件夹中：`output/<SYMBOL>_<MARKET>/`

```
output/
└── AAPL_US/                # 公司文件夹（代码_市场）
    ├── report.md           # 主报告（呈现给用户）
    ├── data.json           # 原始数据
    ├── analysis.json       # 分析结果
    ├── valuation.json      # 估值数据
    └── analyst.json        # 分析师预期
```

## 呈现指南

向用户呈现结果时：

1. 先输出报告开篇结论（增长趋势 + 估值状态）
2. 按“财务亮点 → 产品研究 → 竞争格局 → 管理层指引”呈现核心信息
3. 估值分析必须包含分位区间与币种说明
4. 投资建议需给出明确结论（偏积极 / 中性 / 偏谨慎）
5. 风格对齐 `report_example.md`：少堆指标，多给可读结论

## 常见问题

| 问题 | 解决方案 |
|------|----------|
| A股数据获取失败 | 检查网络，akshare 需要访问国内数据源 |
| 缓存数据过旧 | 使用 `--refresh` 强制刷新 |

## 注意事项

- 数据缓存 24 小时，使用 `--refresh` 强制更新
- 本 Skill 仅提供分析参考，不构成投资建议
- A股使用 AkShare，其他市场使用 yfinance
