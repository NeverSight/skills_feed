---
name: xlb-topic-index
description: Use when user input contains xlb topic queries (for example "xlb >vibe coding/vib", "xlb ??vibe coding", or "查询xlb vibe coding主题") and the task is to fetch Markdown index from local getPluginInfo API, then perform code-based retrieval with routing to available network skills/MCP tools when possible.
---

# Topic Index Command

## Overview
Resolve `xlb` query phrases into a `title` command for the local API, then return Markdown index content.

## When to Use
- User input contains `xlb` as a query trigger.
- User gives `>.../` command directly and expects passthrough.
- User asks for topic index/navigation instead of narrative explanation.
- User wants direct Markdown output from the knowledge source.

## Interaction Rule
- If input matches any trigger pattern below, execute directly without extra questions.
- If input mentions `xlb` but no topic can be extracted, ask:
  - `请发送你要查询的指令，例如：xlb >Vibe Coding/AI超元域 或 xlb ??Vibe Coding`

## Trigger Mapping
- `xlb >vibe coding/vib` -> `title=>vibe coding/vib` (strip `xlb `, payload passthrough)
- `xlb ??vibe coding` -> `title=??vibe coding` (strip `xlb `, payload passthrough)
- `xlb ->vibe coding/:` -> `title=->vibe coding/:` (strip `xlb `, payload passthrough to API)
- `xlb >vibe coding/searchin:` -> `title=>vibe coding/searchin:` (related-topic edges only)
- `xlb >vibe coding/command:` -> `title=>vibe coding/command:` (executable command edges only)
- `查询xlb vibe coding主题` -> `title=>vibe coding/`
- `>AI Model/` -> `title=>AI Model/` (direct passthrough)

## Execute
Run:

```bash
skills/xlb-topic-index/scripts/fetch-topic-index.sh "xlb ??Vibe Coding"
```

The script performs:
- `POST http://localhost:5000/getPluginInfo`
- form fields:
  - `title=<resolved command>`
  - `url=`
  - `markdown=`

## Output Rule
- Return API response Markdown directly.
- Do not paraphrase unless the user asks for analysis.

## Local URL Opening (built-in, no external dependency)
- This project has native URL-open capability for local apps, no dependency on `/Users/wowdd1/App/*.sh`.
- Single URL:
  - `skills/xlb-topic-index/scripts/xlb-open-url.sh "https://example.com" chrome`
  - `python3 skills/xlb-topic-index/scripts/xlb_rag_pipeline.py open-url --url "https://example.com" --app chrome`
  - `python3 skills/xlb-topic-index/scripts/xlb_rag_pipeline.py open-url --url "https://example.com" --app dia`
  - `python3 skills/xlb-topic-index/scripts/xlb_rag_pipeline.py open-url --url "https://example.com" --app atlas`
- Open links from search result JSON:
  - `python3 skills/xlb-topic-index/scripts/xlb_rag_pipeline.py open-hits --hits-json-file /tmp/xlb-search.json --app chrome --limit 3`
- Optional integration with retrieve script:
  - `XLB_OPEN_HITS=1 XLB_OPEN_APP=chrome XLB_OPEN_LIMIT=2 skills/xlb-topic-index/scripts/retrieve-topic-index.sh "xlb >vibe coding/:" "codex cli"`

## Capability Routing Rule (for network content)
- Before fetching external URL content, discover capabilities each run:
  - `python3 skills/xlb-topic-index/scripts/xlb_rag_pipeline.py discover`
- If discover result contains suitable network skills or MCP tools, use them first.
- If no suitable skill/MCP capability exists, fallback to this skill's local scripts.
- Fallback policy: this skill must always remain runnable standalone (no hard dependency on external skills).
- Optional external route hook:
  - Set `XLB_EXTERNAL_ROUTE_CMD=/path/to/command`
  - Command contract: `cmd "<input>" "<retrieval_query>"` and prints final output when it handles the request.
  - If external command exits non-zero or prints empty, fallback to local pipeline.

## Code Retrieval Mode (efficient)
- Use code-based retrieval instead of full markdown dump when user asks to search/analyze:
  - `skills/xlb-topic-index/scripts/retrieve-topic-index.sh "xlb >vibe coding/coding" "codex cli"`
- This mode does:
  1. Cache raw markdown
  2. Incremental update: if raw hash unchanged, skip re-ingest
  3. Parse markdown to virtual file tree
  4. Build sqlite index
  5. Optional concurrent prefetch of top-k URLs (`XLB_PREFETCH_ARTIFACTS=1`)
     - HTML links are converted to `markdown`/`text` artifacts (not stored as raw HTML)
     - External HTML converter is optional and preferred when configured
  6. Return top-k hits by query, or iterative rounds with stop strategy (`XLB_ITERATIVE_SEARCH=1`)

### Performance Flags
- `XLB_FORCE_REFRESH=1` force refresh markdown from API
- `XLB_RAW_CACHE_TTL_SEC=300` raw cache TTL value used only when `XLB_AUTO_REFRESH_ON_QUERY=1`
- `XLB_AUTO_REFRESH_ON_QUERY=0` (default) do not auto refresh by TTL; only user explicit refresh (`XLB_FORCE_REFRESH=1`) or cache miss will fetch
- `XLB_STORAGE_PROFILE=minimal` (default) keep compact cache (`raw + db + jsonl/topics`), no large VFS tree
- `XLB_STORAGE_PROFILE=full` enable VFS folder/file materialization for folder-style browsing
- `XLB_OUTPUT=json` force JSON output for no-query mode (returns raw file reference instead of full markdown text)
- `XLB_FORCE_REINDEX=1` force re-ingest even when cache hash unchanged
- `XLB_PREFETCH_ARTIFACTS=1` enable concurrent URL artifact prefetch
- `XLB_MAX_WORKERS=6` control prefetch concurrency
- `XLB_TOPK=8` control returned hit count
- `XLB_HTML_MODE=markdown|text` choose HTML conversion output format
- `XLB_HTML_CONVERTER_BIN=/path/to/script` optional external converter command
- `XLB_HTML_CONVERTER_TOOL_ID=url-to-markdown` tool id passed to external converter
- `XLB_HTML_CONVERT_TIMEOUT_SEC=20` timeout for external converter execution
- `XLB_ITERATIVE_SEARCH=1` enable iterative retrieval summary output
- `XLB_MAX_ITER=5` max iterative rounds
- `XLB_GAIN_THRESHOLD=0.05` low-gain threshold
- `XLB_LOW_GAIN_ROUNDS=3` consecutive low-gain rounds before stop
- `XLB_DISCOVER_CACHE_TTL_SEC=30` capability discovery cache TTL (seconds)
- `XLB_OPEN_HITS=1` open top hit URLs after retrieval (local app automation)
- `XLB_OPEN_APP=chrome|dia|atlas|default` target app for opened URLs
- `XLB_OPEN_LIMIT=1` number of URLs to open
- `XLB_OPEN_DRY_RUN=1` print open plan only, do not trigger app actions

### `??` Multi-Topic Behavior
- For inputs like `xlb ??vibe coding` (without retrieval query), the script returns a topic suggestion JSON.
- Each topic item includes:
  - `topic`, `count`, `samples`
  - `entry_query` (for example `>Vibe Coding/`)
  - `entry_input` (for example `xlb >Vibe Coding/`)
- If multiple topics are returned, pick one `entry_input` and run it for focused retrieval.

### Network Confirmation Policy
- Default is confirmation-required for expensive network expansion steps.
- `XLB_REQUIRE_NETWORK_CONFIRMATION=1` (default): external route + prefetch disabled unless confirmed.
- `XLB_NETWORK_CONFIRMED=1`: allow network-expensive actions for current command.
- `XLB_SHOW_CONFIRM_TEMPLATE=1` (default): print standardized confirmation template to stderr when network expansion is blocked.
- Default behavior without confirmation: only local index search + URL metadata output.

Example:

```bash
XLB_PREFETCH_ARTIFACTS=1 \
XLB_HTML_MODE=markdown \
XLB_HTML_CONVERTER_BIN=/path/to/url-convert.sh \
XLB_HTML_CONVERTER_TOOL_ID=url-to-markdown \
skills/xlb-topic-index/scripts/retrieve-topic-index.sh "xlb >vibe coding/coding" "agent skills"
```

### Benchmark (before/after)

```bash
python3 skills/xlb-topic-index/bench/run_benchmark.py \
  --queries-file skills/xlb-topic-index/bench/queries.txt \
  --runs 3 \
  --topk 8
```

## Interop for Other Skills
- Cache contract reference: `skills/xlb-topic-index/references/cache-interop.md`
- Resolve user input to stable cache key:
  - `python3 skills/xlb-topic-index/scripts/xlb_rag_pipeline.py resolve-input --input "xlb >vibe coding/coding"`
- Export cache usage guide from meta:
  - `python3 skills/xlb-topic-index/scripts/xlb_rag_pipeline.py describe-cache --meta-path "skills/xlb-topic-index/cache/index/<HASH>.meta.json" --format markdown`
- Program-first data files:
  - `skills/xlb-topic-index/cache/dataset/snap-<HASH>.nodes.jsonl`
  - `skills/xlb-topic-index/cache/dataset/snap-<HASH>.topics.json`
  - `skills/xlb-topic-index/cache/dataset/snap-<HASH>.navigation.json`

### Query Edge Semantics (for auto exploration)
- `searchin` section -> `topic_navigation` edges:
  - usually “related topics”, for example `>AI Model` -> normalized executable `>AI Model/`
- `command` section -> `knowledge_search` edges:
  - executable knowledge-search commands, including bracket style like `search(>vibe coding/vibe)` -> executable `>vibe coding/vibe`
- External skill can choose either:
  - follow `topic_navigation` to jump to another topic
  - run `knowledge_search` to deepen inside current domain
- Prefer section-specific commands for efficient edge collection:
  - `>topic/searchin:` for topic-to-topic traversal
  - `>topic/command:` for command/deep-search traversal

### Auto Explore Command
- Use:
  - `python3 skills/xlb-topic-index/scripts/xlb_rag_pipeline.py explore-next --meta-path "skills/xlb-topic-index/cache/index/<HASH>.meta.json" --strategy topic_first --dry-run`
- Remove `--dry-run` to execute next hop directly.
- Useful flags:
  - `--strategy topic_first|search_first|mixed`
  - `--visited-file <path> --update-visited` to avoid repeated edges
  - `--include-other-queries` to allow `??...` style fallback edges

### Explore Loop (dedupe + budget + priority)
- Use:
  - `python3 skills/xlb-topic-index/scripts/xlb_rag_pipeline.py explore-loop --seed-input "xlb >vibe coding/:" --edge-strategy searchin_command_backlink --max-steps 12 --max-depth 4 --max-seconds 90 --visited-file /tmp/xlb-visited.json --visited-topics-file /tmp/xlb-visited-topics.json --update-visited`
- Behavior:
  - Auto uses `>topic/searchin:` and `>topic/command:` to collect next edges.
  - Applies visited dedupe (`visited-file` + `visited-topics-file`) to avoid loops.
  - Stops by budget (`max-steps` / `max-depth` / `max-seconds`).
  - Edge priority default is `searchin -> command -> backlink`.

### One-Click Wrapper
- Use:
  - `skills/xlb-topic-index/scripts/xlb-auto-explore.sh "vibe coding"`
  - `skills/xlb-topic-index/scripts/xlb-auto-explore.sh "xlb >vibe coding/:"`
  - `skills/xlb-topic-index/scripts/xlb-auto-explore.sh "xlb auto vibe coding"`
- Wrapper defaults:
  - persistent visited files under `skills/xlb-topic-index/cache/`
  - strategy `searchin_command_backlink`
  - budget `12 steps / depth 4 / 90s`
- Override with env vars:
  - `XLB_AUTO_MAX_STEPS`, `XLB_AUTO_MAX_DEPTH`, `XLB_AUTO_MAX_SECONDS`
  - `XLB_AUTO_EDGE_STRATEGY`, `XLB_AUTO_INCLUDE_BACKLINKS`, `XLB_AUTO_UPDATE_VISITED`

### Graph Backlink Query (`->`)
- Input:
  - `xlb ->vibe coding/:`
- Meaning:
  - This is a server-side command and is passed through as `title=->vibe coding/:`.
  - `retrieve-topic-index.sh` should not local-intercept this command.
- Local graph helper (explicit, optional):
  - `python3 skills/xlb-topic-index/scripts/xlb_rag_pipeline.py graph-neighbors --index-dir skills/xlb-topic-index/cache/index --target-title "->vibe coding/:"`
  - Used only when you explicitly want cache-based local graph exploration.

## Error Handling
- API unreachable: report connection failure and suggest checking local service on port `5000`.
- Empty response: return a short warning and ask whether to retry with a broader command (for example `>Vibe Coding/`).
- Empty input only: ask user to provide any non-empty title command.
