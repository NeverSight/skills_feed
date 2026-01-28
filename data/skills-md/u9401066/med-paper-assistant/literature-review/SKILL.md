---
name: literature-review
description: 系統性文獻搜尋、篩選、下載、整理。觸發：文獻回顧、找論文、搜尋文獻、systematic review、literature search、PubMed、找文章、搜paper、review、reference、citation、引用、參考文獻、背景調查、background。
---

# 系統性文獻回顧

## 適用情境
- 開始新研究專案 | 撰寫 Introduction 前調查 | 系統性回顧 | PICO 臨床問題
- **不適用**：快速查一篇 → 直接 `search_literature` | 只需整理 → `format_references`

---

## 工具速查

### pubmed-search MCP

| 類別 | 工具 | 說明 |
|------|------|------|
| **搜尋** | `search_literature` | 基本 PubMed 搜尋 |
| | `generate_search_queries` | MeSH + 同義詞材料 |
| | `parse_pico` | 解析 PICO 臨床問題 |
| | `merge_search_results` | 合併去重 |
| **探索** | `find_related_articles` | 相似文章 |
| | `find_citing_articles` | 引用此文的後續研究 |
| | `get_article_references` | 此文的參考文獻 |
| | `get_citation_metrics` | iCite RCR 指標 |
| **Session** | `get_session_pmids` | 取回搜尋結果 PMID |
| | `get_session_summary` | 查看 session 狀態 |
| **匯出** | `prepare_export` | RIS/BibTeX/CSV |
| | `analyze_fulltext_access` | PMC 全文可用性 |

### mdpaper MCP 儲存文獻

| 方法 | 優先級 | 說明 |
|------|--------|------|
| `save_reference_mcp(pmid)` | **PRIMARY** ✅ | MCP-to-MCP 驗證 |
| `save_reference(article)` | FALLBACK ⚠️ | 僅當 API 不可用 |

```
✅ save_reference_mcp(pmid="12345678", agent_notes="...")
❌ save_reference(article={metadata})  # Agent 可能幻覺
```

---

## 工作流程

### Phase 0: 環境準備
```
get_current_project()  # 確認專案
讀取：projects/{slug}/.memory/activeContext.md  # 了解之前做了什麼
```

### Phase 1: 建立搜尋策略

**關鍵字搜尋**（一般主題）：
```
generate_search_queries(topic="remimazolam sedation ICU", strategy="comprehensive")
```

**PICO 搜尋**（比較性問題）：
```
# Step 1: 解析 PICO
parse_pico(description="remimazolam 在 ICU 鎮靜比 propofol 好嗎？")
→ P=ICU patients, I=remimazolam, C=propofol, O=sedation

# Step 2: 並行取得各元素 MeSH（同時呼叫！）
generate_search_queries(topic="ICU patients")
generate_search_queries(topic="remimazolam")
generate_search_queries(topic="propofol")
```

### Phase 2: 並行搜尋執行
```
# 同時多組搜尋（並行呼叫！）
search_literature(query='"Intensive Care Units"[MeSH] AND remimazolam', limit=50)
search_literature(query='remimazolam AND propofol AND sedation', limit=50)

# 合併結果
merge_search_results(results_json='[{"query_id": "q1", "pmids": ["123"]}, ...]')
```

### Phase 3: 結果評估
```
# 結果太少 (<20) → 擴展
expand_search_queries(topic="...", current_results=15)

# 對種子文獻做引用網路探索
find_citing_articles(pmid="12345678")   # forward
find_related_articles(pmid="12345678")  # similar
get_article_references(pmid="12345678") # backward

# 取得引用指標排序
get_citation_metrics(pmids="last", sort_by="relative_citation_ratio", min_rcr=1.0)
```

### Phase 4: 篩選與儲存
```
# 呈現篩選清單給用戶（標題、年份、期刊、RCR）

# ✅ PRIMARY：使用 MCP-to-MCP 驗證
save_reference_mcp(pmid="12345678", agent_notes="Key paper on...")

# ⚠️ FALLBACK：僅當 API 不可用
save_reference(article={metadata}, project="...")
```

### Phase 5: 匯出
```
format_references(style="vancouver")
prepare_export(pmids="last", format="ris")
analyze_fulltext_access(pmids="last")
```

### Phase 6: ⭐ 更新專案記憶
```
# 必須更新！
寫入：projects/{slug}/.memory/activeContext.md
- Current Focus: 文獻回顧進度
- Key References: 關鍵文獻及重要性
- Memo / Notes: Agent 對文獻的觀察
```

---

## 決策點

| 時機 | 選擇 |
|------|------|
| 建立專案 or 探索？ | 先探索熟悉文獻 |
| 關鍵字 or PICO？ | 比較性問題用 PICO |
| 結果數量 | 50-300 繼續，<20 擴展，>500 限縮 |
| 篩選方式 | <30 逐篇，>30 用 RCR 排序 |

---

## 常見問題

| 問題 | 解法 |
|------|------|
| 結果太多 | 加 MeSH、article_type、縮小年份 |
| 結果太少 | `expand_search_queries`、移除 Comparator |
| 用哪個儲存？ | **永遠優先 `save_reference_mcp`** |
| Session 用途？ | `get_session_pmids(-1)` 取回最近搜尋 |

---

## 相關技能
- `concept-development` - 發展研究概念
- `parallel-search` - 並行搜尋細節
