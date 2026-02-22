---
name: agentbay-monitor-skills
description: 舆情监控技能，最终产出舆情报告。当用户问「某事件/话题舆情如何」「舆论怎么样」「做舆情分析」「运行舆情分析」或按关键词/平台爬取并生成舆情报告时，使用本技能。约定：凡舆情相关意图即执行全流程（爬取→情感分析→生成报告）。爬取由本技能完成；情感分析由主 Agent 按提示词自主判断；报告由 generate_report 生成。
---

# AgentBay 舆情监控 Skill

## ⚠️ 舆情分析 = 全流程（必读）

**用户说「运行舆情分析」「做舆情分析」「舆情分析 主题是 XXX」时，必须执行完整三步，不能只跑爬取就结束。**

| 步骤 | 动作 | 说明 |
|------|------|------|
| 1. 爬取 | `crawl.py` 或 `crawl_for_sentiment(...)` | 得到 `raw_output_path`（爬取结果 JSON） |
| 2. 情感分析 | 读 `scripts/sentiment/sentiment_instruction.md` → 对爬取 JSON 逐条判定 → 写情感结果小 JSON → 运行 `write_processed.py` | 得到 processed JSON（如 `output/processed.json`） |
| 3. 生成报告 | `report.py --input <processed 路径>` 或 `generate_report(...)` | 得到 Markdown/JSON（及可选 PDF） |

**禁止行为**：只运行 `crawl.py` 后就说「爬取完成，情感分析由主 Agent 完成」并结束。这是错误用法——主 Agent 就是你自己，你必须继续完成步骤 2 和 3，直到产出最终报告文件。

## 何时使用

用户出现以下任一意图时，**必须**使用本技能并执行全流程（爬取→情感分析→生成报告）：

- 问「**某事件/话题舆情如何**」「XX 舆论怎么样」「想了解 XX 的舆情」
- 「运行舆情分析」「做舆情分析」「舆情分析 主题是 XXX」
- 舆情监控、情感分析、舆情报告、按关键词/平台爬取并生成报告（中英文场景均可）

**意图为舆情相关即默认使用本技能**，不可仅用联网搜索代替。

**重要约定**：凡提到「舆情分析」（或「运行舆情分析」「做舆情分析」等等价表述），即视为执行**全流程**——爬取 → 情感分析 → 生成报告。必须按该完整流程执行，不可只做爬取；最终产出须包含 Markdown/JSON（及可选 PDF）报告。

## 前置条件

工作目录为技能目录（本 SKILL 所在目录）；已安装依赖；已配置 `AGENTBAY_API_KEY`。

## 依赖

```bash
pip install wuying-agentbay-sdk pandas numpy pyyaml markdown
```

可选（PDF 报告）：`brew install cairo pango gdk-pixbuf` 后 `pip install weasyprint`。不装则仅无 PDF，.md/.json 正常。

## API Key

仅需配置 `AGENTBAY_API_KEY`。环境变量：`export AGENTBAY_API_KEY=你的key`（Windows PowerShell：`$env:AGENTBAY_API_KEY="你的key"`）。或直接写文件：`mkdir -p ~/.config/agentbay && echo -n '你的key' > ~/.config/agentbay/api_key`。获取：https://agentbay.console.aliyun.com/service-management 。未配置时运行脚本会报错。其余参数由主 Agent 传参/命令行传入。

## 整体流程

**舆情分析 = 全流程**：爬取 → 情感分析 → 生成报告（见上文「⚠️ 舆情分析 = 全流程」）。用户要求「舆情分析」时，三步都必须执行，不能只做第 1 步。

1. **爬取**：`crawl.py` 或 `crawl_for_sentiment(...)` → 得到 `raw_output_path`（爬取结果 JSON）。
2. **情感分析**：主 Agent 读提示词 `scripts/sentiment/sentiment_instruction.md`，对爬取 JSON 逐条判定情感，产出情感结果小 JSON；再运行 `write_processed.py` 合并得到 processed JSON（如 `output/processed.json`）。提示词可定制。
3. **生成报告**：`report.py --input <processed 路径>` 或 `generate_report(processed_results, ...)` → Markdown/JSON（及可选 PDF）。

## 运行方式

**步骤 0：登录（仅非搜索引擎）**
xhs/weibo/douyin/zhihu 须先登录；百度、Bing 不需要。`python scripts/login.py --platform xhs [--context-name sentiment-analysis]` → 浏览器中登录后终端按 Enter，状态持久化。非搜索引擎爬取时 `--context-name` 须与登录一致。

**步骤 1：爬取**

```bash
python scripts/crawl.py --keywords "关键词1,关键词2" [--platform baidu] [--max-results N] [--output-dir output]
```

参数：`-k` 必需；`-p` 默认 baidu（可选 xhs/weibo/douyin/zhihu/bing）；`--max-results`、`-o`、`--report-title`、`--context-name`、`--crawl-timeout`。百度/Bing 仅抓资讯列表页（不点进链接），百度用资讯 URL（tn=news）。

**爬取超时（必读）**：执行环境（如 run_terminal_cmd）的**超时须 ≥ 10 分钟**（600 秒或 600000 毫秒），否则会中断。约 1 条/分钟，10 条约 10 分钟；建议超时略大于估算（如 15 分钟）。脚本内 `--crawl-timeout` 不传时会自动按条数计算，一般无需手传。

**步骤 2：情感分析**
主 Agent 读 `scripts/sentiment/sentiment_instruction.md`，对爬取 JSON 逐条判定情感并按规定格式写 processed JSON（无需在技能中配置 LLM）。

**步骤 3：生成报告**

```bash
python scripts/report.py --input <processed JSON 路径> [--output-dir output] [--title "报告标题"]
```

## 输出

爬取 → `raw_output_path`、`crawl_results`。情感分析 → processed JSON（含 `sentiment_statistics`、每条 `sentiment`，格式见提示词）。报告 → `markdown_path`、`json_path`、可选 `pdf_path`。

## Agent 调用要点

**舆情分析必跑全流程**：用户说「舆情分析」「运行舆情分析」或类似意图时，**必须**完成「爬取 → 情感分析 → 合并（write_processed.py）→ 生成报告」，产出最终报告文件。**不可**只运行爬取后就说「情感分析由主 Agent 完成」并结束——主 Agent 即当前 Agent，必须由你继续完成情感分析与报告。

- **登录**：非搜索引擎前先 `login.py --platform <平台>`；百度/Bing 免登录。
- **爬取**：`crawl.py` 或 `crawl_for_sentiment(...)`，默认平台 baidu；**执行超时 ≥ 10 分钟**（见上文「爬取超时」）；非搜索引擎时 `context_name` 与登录一致。
- **情感分析**：读 `scripts/sentiment/sentiment_instruction.md`；对爬取 JSON（`raw_output_path`）逐条判定情感；写情感结果小 JSON（如 `output/sentiment_only.json`）；运行 `python scripts/sentiment/write_processed.py --raw <爬取JSON> --sentiment <情感结果JSON> --output output/processed.json`。
- **报告**：`report.py --input output/processed.json` 或 `generate_report(...)`。
- **失败**：未配置 Key、未登录或执行失败 → `success: False`、`error`。

## 代码示例

```python
import asyncio, sys, json
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent / "scripts"))
from crawl import crawl_for_sentiment, generate_report

async def main():
    result = await crawl_for_sentiment(platform="baidu", keywords=["产品名"], max_results_per_keyword=10, output_dir="output")
    if not result.get("success"): return
    raw_path = result.get("raw_output_path")
    # 主 Agent：读 sentiment_instruction.md → 对 raw_path 做情感分析 → 写 output/processed.json（或先用 write_processed.py 合并）
    processed_path = Path("output") / "processed.json"
    with open(processed_path, "r", encoding="utf-8") as f:
        report = generate_report(json.load(f), output_dir="output", title="舆情报告")
    print("报告:", report.get("markdown_path"))
asyncio.run(main())
```

## 常见问题

- **只跑了爬取怎么办**：若已运行 `crawl.py` 得到 `raw_output_path`，必须继续做情感分析（读 `sentiment_instruction.md`、写情感结果 JSON、运行 `write_processed.py`）再运行 `report.py --input <processed路径>`，直到产出报告。
- **processed JSON**：title/content 常含未转义双引号，手写易导致 `report.py` JSON 解析失败。主 Agent 只产出「情感结果」小 JSON，再运行 `python scripts/sentiment/write_processed.py --raw <爬取JSON> --sentiment <情感结果JSON> --output <processed路径>`。详见 `sentiment_instruction.md` 第 4 节。
- **登录失效**：重跑 `python scripts/login.py --platform <平台> [--context-name ...]`。
- **爬取超时**：执行环境超时须 ≥ 10 分钟（见上文）；需更长时显式传 `--crawl-timeout`（秒）。

## 文件结构

`SKILL.md` · `scripts/`：`crawl.py`（爬取/报告入口）、`report.py`、`login.py`、`crawler/`、`sentiment/`（`sentiment_instruction.md`、`write_processed.py`）、`reporter/` · `output/`
