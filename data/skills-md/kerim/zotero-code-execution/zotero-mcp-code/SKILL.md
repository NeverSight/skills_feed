---
name: zotero-mcp-code
description: Search Zotero library using code execution for efficient multi-strategy searches without crash risks. Use this skill when the user needs comprehensive Zotero searches with automatic deduplication and ranking.
---

# Zotero MCP Code Execution Skill

Search your Zotero library using code execution for safe, efficient, comprehensive searches.

## 🎯 Core Concept

Instead of calling MCP tools directly (which loads all results into context and risks crashes), **write Python code** that:
1. Fetches large datasets (50-100+ items per strategy)
2. Filters and ranks in code execution environment
3. Returns only top N results to context

**Benefits:**
- ✅ No crash risk (large data stays in code)
- ✅ Automatic multi-strategy search
- ✅ Automatic deduplication
- ✅ Automatic ranking
- ✅ One function call instead of 5-10

## ⚠️ Critical Notes

### Multi-Term Searches
**Zotero treats multi-word queries as AND conditions!**

❌ **Wrong:** `comprehensive_search("Atyal Atayal 泰雅族")` → finds 0 results (needs ALL terms)
✅ **Right:** Search each term separately and merge results (see Pattern 6 below)

**When to use multi-term OR search:**
- Multiple spellings (Atayal, Atyal)
- Multiple languages (Atayal, 泰雅族)
- Synonyms (skill transfer, transfer of learning)

### Semantic Search Status
**Semantic search is now working correctly** (fixed 2025-01-08). However, you may see 404 error messages in output from the semantic search engine itself - these can be ignored as our wrapper handles them correctly.

## 🚀 Basic Usage

For **90% of Zotero searches**, use this simple pattern:

```python
import sys
sys.path.append('/Users/niyaro/Documents/Code/zotero-code-execution')
import setup_paths

from zotero_lib import SearchOrchestrator, format_results

# Single comprehensive search
orchestrator = SearchOrchestrator()
results = orchestrator.comprehensive_search(
    "user's query here",
    max_results=20,  # Return top 20 most relevant
    use_semantic=True  # Semantic search now works correctly
)

# Format and display
print(format_results(results, include_abstracts=True))
```

**This automatically:**
- Performs semantic search (vector similarity)
- Performs keyword search (qmode="everything" + "titleCreatorYear")
- Performs tag-based search
- Fetches 100+ items total
- Deduplicates results
- Ranks by relevance
- Returns only top 20 to context

## 📋 Common Patterns

### Pattern 1: Simple Search (Most Common)

**User asks:** "Find papers about embodied cognition"

```python
import sys
sys.path.append('/Users/niyaro/Documents/Code/zotero-code-execution')
import setup_paths
from zotero_lib import SearchOrchestrator, format_results

orchestrator = SearchOrchestrator()
results = orchestrator.comprehensive_search("embodied cognition", max_results=20)
print(format_results(results))
```

### Pattern 2: Filtered Search

**User asks:** "Find recent journal articles about machine learning"

```python
import sys
sys.path.append('/Users/niyaro/Documents/Code/zotero-code-execution')
import setup_paths
from zotero_lib import ZoteroLibrary, SearchOrchestrator, format_results

library = ZoteroLibrary()
orchestrator = SearchOrchestrator(library)

# Fetch broadly (safe - filtering happens in code)
items = library.search_items("machine learning", limit=100)

# Filter in code
filtered = orchestrator.filter_by_criteria(
    items,
    item_types=["journalArticle"],
    date_range=(2020, 2025)
)

print(format_results(filtered[:15]))
```

### Pattern 3: Author Search

**User asks:** "What papers do I have by Kahneman?"

```python
import sys
sys.path.append('/Users/niyaro/Documents/Code/zotero-code-execution')
import setup_paths
from zotero_lib import ZoteroLibrary, format_results

library = ZoteroLibrary()
results = library.search_items(
    "Kahneman",
    qmode="titleCreatorYear",
    limit=50
)

# Sort by date
sorted_results = sorted(results, key=lambda x: x.date, reverse=True)
print(format_results(sorted_results))
```

### Pattern 4: Tag-Based Search

**User asks:** "Show me papers tagged with 'learning' and 'cognition'"

```python
import sys
sys.path.append('/Users/niyaro/Documents/Code/zotero-code-execution')
import setup_paths
from zotero_lib import ZoteroLibrary, format_results

library = ZoteroLibrary()
results = library.search_by_tag(["learning", "cognition"], limit=50)
print(format_results(results[:20]))
```

### Pattern 5: Recent Papers

**User asks:** "What did I recently add?"

```python
import sys
sys.path.append('/Users/niyaro/Documents/Code/zotero-code-execution')
import setup_paths
from zotero_lib import ZoteroLibrary, format_results

library = ZoteroLibrary()
results = library.get_recent(limit=20)
print(format_results(results))
```

### Pattern 6: Multi-Term OR Search (Multiple Spellings/Languages)

**User asks:** "Find papers about Atyal or 泰雅族" (alternate spellings/languages)

**IMPORTANT:** Zotero treats multi-word queries as AND conditions. For OR searches, search each term separately and merge.

```python
import sys
sys.path.append('/Users/niyaro/Documents/Code/zotero-code-execution')
import setup_paths
from zotero_lib import SearchOrchestrator, format_results

orchestrator = SearchOrchestrator()

# Search each term separately
all_results = {}
for term in ['Atayal', '泰雅族']:
    results = orchestrator.comprehensive_search(term, max_results=50, use_semantic=True)
    for item in results:
        all_results[item.key] = item  # Deduplicate by key

# Re-rank combined results
ranked = orchestrator._rank_items(list(all_results.values()), 'Atayal 泰雅族')

# Optional: Filter for specific content
filtered = [item for item in ranked
            if any(term in (item.title + item.abstract).lower()
                   for term in ['atyal', 'atayal', '泰雅'])]

print(format_results(filtered[:25], include_abstracts=True))
```

### Pattern 7: Multi-Topic AND Search

**User asks:** "Find papers about both cognition and learning"

```python
import sys
sys.path.append('/Users/niyaro/Documents/Code/zotero-code-execution')
import setup_paths
from zotero_lib import SearchOrchestrator, format_results

orchestrator = SearchOrchestrator()

# Search both topics
results1 = orchestrator.comprehensive_search("cognition", max_results=30)
results2 = orchestrator.comprehensive_search("learning", max_results=30)

# Find intersection
keys1 = {item.key for item in results1}
keys2 = {item.key for item in results2}
common_keys = keys1 & keys2

if common_keys:
    common_items = [item for item in results1 if item.key in common_keys]
    print("Papers about both topics:")
    print(format_results(common_items))
else:
    print("No papers found on both topics.")
    print("\nCognition results:")
    print(format_results(results1[:10]))
    print("\nLearning results:")
    print(format_results(results2[:10]))
```

## 🔧 Advanced Usage

### Custom Filtering Logic

```python
import sys
sys.path.append('/Users/niyaro/Documents/Code/zotero-code-execution')
import setup_paths
from zotero_lib import ZoteroLibrary, SearchOrchestrator, format_results

library = ZoteroLibrary()
orchestrator = SearchOrchestrator(library)

# Fetch large dataset
items = library.search_items("neural networks", limit=100)

# Custom filtering
recent_with_doi = [
    item for item in items
    if item.doi and item.date and int(item.date[:4]) >= 2020
]

print(format_results(recent_with_doi[:15]))
```

### Multi-Angle Custom Search

```python
import sys
sys.path.append('/Users/niyaro/Documents/Code/zotero-code-execution')
import setup_paths
from zotero_lib import ZoteroLibrary, SearchOrchestrator, format_results

library = ZoteroLibrary()
orchestrator = SearchOrchestrator(library)

all_results = set()

# Multiple search angles
queries = [
    "skill transfer",
    "transfer of learning",
    "generalization of skills"
]

for query in queries:
    results = library.search_items(query, limit=30)
    all_results.update(results)

# Rank combined results
ranked = orchestrator._rank_items(list(all_results), "skill transfer")
print(format_results(ranked[:20]))
```

### Iterative Refinement

```python
import sys
sys.path.append('/Users/niyaro/Documents/Code/zotero-code-execution')
import setup_paths
from zotero_lib import ZoteroLibrary, SearchOrchestrator, format_results

library = ZoteroLibrary()
orchestrator = SearchOrchestrator(library)

# Initial search
initial = library.search_items("memory", limit=50)

# Analyze tags
tag_freq = {}
for item in initial:
    for tag in item.tags:
        tag_freq[tag] = tag_freq.get(tag, 0) + 1

# Find most common tag
if tag_freq:
    most_common_tag = max(tag_freq, key=tag_freq.get)

    # Refine search
    refined = orchestrator.filter_by_criteria(
        initial,
        required_tags=[most_common_tag]
    )

    print(f"Papers with most common tag '{most_common_tag}':")
    print(format_results(refined))
```

## 📚 API Reference

### `SearchOrchestrator`

**Main class for automated searching.**

#### `comprehensive_search(query, max_results=20, use_semantic=True, use_keyword=True, use_tags=True, search_limit_per_strategy=50)`

Performs multi-strategy search with automatic deduplication and ranking.

**Parameters:**
- `query` (str): Search query
- `max_results` (int): Maximum results to return (default: 20)
- `use_semantic` (bool): Use semantic search (default: True)
- `use_keyword` (bool): Use keyword search (default: True)
- `use_tags` (bool): Use tag search (default: True)
- `search_limit_per_strategy` (int): Items to fetch per strategy (default: 50)

**Returns:** List of ZoteroItem objects

#### `filter_by_criteria(items, item_types=None, date_range=None, required_tags=None, excluded_tags=None)`

Filter items by various criteria.

**Parameters:**
- `items` (list): Items to filter
- `item_types` (list): Allowed item types (e.g., ["journalArticle"])
- `date_range` (tuple): (min_year, max_year)
- `required_tags` (list): Tags that must be present
- `excluded_tags` (list): Tags that must not be present

**Returns:** Filtered list of ZoteroItem objects

### `ZoteroLibrary`

**Low-level interface to Zotero.**

#### `search_items(query, qmode="titleCreatorYear", item_type="-attachment", limit=100, tag=None)`

Basic keyword search.

#### `semantic_search(query, limit=100, search_type="hybrid")`

Semantic/vector search.

#### `search_by_tag(tags, item_type="-attachment", limit=100)`

Search by tags.

#### `get_recent(limit=50)`

Get recently added items.

#### `get_tags()`

Get all tags in library.

### `format_results(items, include_abstracts=True, max_abstract_length=300)`

Format items as markdown.

## ⚙️ Configuration

### Default Parameters

Good defaults for most searches:

```python
orchestrator.comprehensive_search(
    query,
    max_results=20,              # Top 20 results
    search_limit_per_strategy=50 # Fetch 50 per strategy
)
```

### Adjusting Search Depth

For **quick searches** (fewer results, faster):
```python
results = orchestrator.comprehensive_search(
    query,
    max_results=10,
    search_limit_per_strategy=20
)
```

For **thorough searches** (more comprehensive):
```python
results = orchestrator.comprehensive_search(
    query,
    max_results=30,
    search_limit_per_strategy=100
)
```

## 🔍 How It Works

### Behind the Scenes

When you call `comprehensive_search("embodied cognition", max_results=20)`:

1. **Semantic Search** (if enabled):
   - Searches "embodied cognition" (hybrid mode) → 50 items
   - Searches "embodied cognition" (vector mode) → 50 items

2. **Keyword Search** (if enabled):
   - Searches with qmode="everything" → 50 items
   - Searches with qmode="titleCreatorYear" → 50 items

3. **Tag Search** (if enabled):
   - Extracts words from query
   - Finds matching tags in library
   - Searches by matching tags → 50 items

4. **Processing**:
   - Combines all results (~250 items)
   - Deduplicates using item keys (~120 unique)
   - Ranks by relevance score
   - Returns top 20

5. **Context**:
   - Only the final 20 items go to LLM context
   - All processing happens in code execution environment

### Why This Is Better

**Old Approach (Direct MCP):**
```python
# 5+ function calls, all results to context
results1 = zotero_semantic_search("query", limit=10)  # Crash risk if > 15
results2 = zotero_search_items("query", limit=10)
# ... manual deduplication, no ranking
# All items (50+) load into context
```

**New Approach (Code Execution):**
```python
# 1 function call, only top results to context
results = orchestrator.comprehensive_search("query", max_results=20)
# Fetches 250+ items, processes in code, returns top 20
```

## 🛠️ Error Handling

Always handle potential errors:

```python
import sys
sys.path.append('/Users/niyaro/Documents/Code/zotero-code-execution')
import setup_paths
from zotero_lib import SearchOrchestrator, format_results

orchestrator = SearchOrchestrator()

try:
    results = orchestrator.comprehensive_search("query", max_results=20)

    if results:
        print(format_results(results))
    else:
        print("No results found. Try a broader search term.")

except Exception as e:
    print(f"Search failed: {e}")
    print("Please check your Zotero MCP configuration.")
```

## 📖 Examples

See `/Users/niyaro/Documents/Code/zotero-code-execution/examples.py` for 8 complete working examples.

## 🎓 Quick Reference

| Task | Code |
|------|------|
| Basic search | `orchestrator.comprehensive_search(query, max_results=20)` |
| Filter by type | `orchestrator.filter_by_criteria(items, item_types=["journalArticle"])` |
| Filter by date | `orchestrator.filter_by_criteria(items, date_range=(2020, 2025))` |
| Search author | `library.search_items(author, qmode="titleCreatorYear", limit=50)` |
| Search by tag | `library.search_by_tag([tags], limit=50)` |
| Recent items | `library.get_recent(limit=20)` |
| Format output | `format_results(items, include_abstracts=True)` |

## 💡 Tips

1. **Start simple**: Use `comprehensive_search()` for most queries
2. **Adjust depth**: Use `search_limit_per_strategy` to control thoroughness
3. **Filter after**: Fetch broadly, filter in code
4. **Custom logic**: Use Python for complex filtering
5. **Check errors**: Always wrap in try/except

## 📁 Documentation

- **Quick Start**: `/Users/niyaro/Documents/Code/zotero-code-execution/QUICK_START.md`
- **Full Docs**: `/Users/niyaro/Documents/Code/zotero-code-execution/README.md`
- **Examples**: `/Users/niyaro/Documents/Code/zotero-code-execution/examples.py`
- **Status**: `/Users/niyaro/Documents/Code/zotero-code-execution/HONEST_STATUS.md`

## ⚠️ Important Notes

- This uses code execution, not direct MCP calls
- Large datasets are processed in code, keeping context small
- Semantic search may not be available (falls back to keyword)
- Results are automatically deduplicated and ranked
- Safe to use large limits (100+) because filtering happens in code

## 🔄 Migration from zotero-mcp

**Old pattern:**
```python
# Multiple manual MCP calls
results1 = zotero_semantic_search("query", limit=10)
results2 = zotero_search_items("query", limit=10)
# Manual deduplication...
```

**New pattern:**
```python
# One function call with code execution
import sys
sys.path.append('/Users/niyaro/Documents/Code/zotero-code-execution')
import setup_paths
from zotero_lib import SearchOrchestrator, format_results

orchestrator = SearchOrchestrator()
results = orchestrator.comprehensive_search("query", max_results=20)
print(format_results(results))
```

---

**Remember:** This skill uses code execution to safely handle large searches. The implementation is in `/Users/niyaro/Documents/Code/zotero-code-execution/`.
