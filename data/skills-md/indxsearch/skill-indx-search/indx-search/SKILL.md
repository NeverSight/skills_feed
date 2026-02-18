---
name: indx-search
description: Indx Search integration skill for AI coding agents. Use when building search functionality with Indx — a high-performance search engine using pattern recognition instead of tokenizers or stemmers. Covers C# NuGet (IndxSearchLib) and HTTP API (IndxCloudApi) integration, field configuration, querying, filters, boosts, coverage tuning, and search UX patterns.
---

# Indx Search — Agent Skill

Indx is a high-performance search engine for structured and unstructured text. It uses pattern recognition instead of tokenizers, stemmers, or analyzers — handling typos, formatting variations, and messy input without configuration.

## When to Use Indx

- Up to millions of documents where you need fast, typo-tolerant search
- When you don't want to configure tokenizers, stemmers, analyzers, or language settings
- When you want embedded search with no external dependencies (NuGet) or a lightweight self-hosted API
- Unmatched on speed — in-memory indexes and a fast vector model mean Indx outperforms Elastic/Solr/Algolia in most scenarios

**When Indx is not the right fit:**
- Tens of millions+ of documents (log aggregation, large-scale analytics)
- Pure exact-match queries (database-style lookups)
- Schemas that change frequently — Indx requires a full reload and reindex when the schema changes

## Choosing Your Integration Path

**C# / .NET project** → Use the [IndxSearchLib NuGet package](https://www.nuget.org/packages/IndxSearchLib/) directly. Embed search into your application with no external dependencies. See [references/csharp.md](references/csharp.md) for full API reference.

**Any other tech stack** (Node.js, Python, Java, etc.) → Deploy the [IndxCloudApi](https://github.com/indxSearch/IndxCloudApi) HTTP API server and interact via REST. Recommended deployment target: Azure App Service (works with zero config). See [references/cloudapi-setup.md](references/cloudapi-setup.md) for setup and deployment, and [references/http-api.md](references/http-api.md) for endpoints, schemas, and data loading.

## Core Concepts

### Two-Step Search Model

Every search executes in two phases:

1. **Pattern Matching** — Scans all documents for textual and structural patterns. Produces candidate results with strong recall and built-in typo tolerance. No query preprocessing needed.

2. **Coverage** (enabled by default) — A collection of algorithms that detect exact and near-exact token matches (whole words, fuzzy words, joined/split words, prefixes/suffixes) in the top-K candidates (default: 500). Confirmed matches are scored 0–255 and promoted above pure pattern matches. A truncation index marks where coverage-confirmed results end.

### Field Configuration

Fields must be explicitly marked with their roles before indexing:

| Role | Purpose | Notes |
|------|---------|-------|
| **Searchable** | Included in matching and scoring | At least one required. Supports weight for relative importance |
| **Filterable** | Available for filter operations | Used with value filters and range filters |
| **Facetable** | Used for aggregations | Returns value counts (histograms) |
| **Sortable** | Enables result ordering | Works on numbers and strings. See sorting behavior below |
| **WordIndexing** | Indexes entire words | Useful on fields with many repeating words. See below |

**WordIndexing** — indexes entire words in a field. Useful for large datasets where many documents share the same words (e.g. a `category` field across thousands of products). Complements Searchable and must be combined with it on the same field. Only affects single-word queries.

**Weight priority** — Searchable fields support a weight to control importance:
- C# API: `Weight.High`, `Weight.Med`, `Weight.Low` (enum)
- HTTP API: `0` (High), `1` (Medium), `2` (Low) (integer)

Note: Weights affect pattern recognition directly. A short text pattern in a longer string will not necessarily rank higher than the same pattern in a shorter string, even if the longer field has higher weight.

### Filters Must Be Server-Side

Never filter results client-side after a search. The search only returns a limited number of results (`maxNumberOfRecordsToReturn`), so client-side filtering on that subset will miss documents. Always use `CreateValueFilter` / `CreateRangeFilter` / `CombineFilters` and pass the filter in the query (`query.Filter` in C#, `CloudQuery.filter` in HTTP) so the server applies the filter during search.

### Search Behavior Guidance

- **Keep coverage enabled** (the default). This is the recommended setting for nearly all use cases — both human-facing and programmatic. Only disable coverage in edge cases where you search a single field and only care about top-K fuzzy matches (e.g. name lookup). With coverage disabled, truncation is unreliable and results degrade when searching across multiple fields (title + description + category, etc.).
- **Agent/tool usage**: Enable coverage and set `IncludePatternMatches = false` (`coverageSetup.includePatternMatches` in HTTP). This returns only exact and near-exact matches (within ~1 typo), filtering out loose pattern hits.
- **Empty search**: Supported with empty/null query text. Requires facets enabled and at least one facetable field. Returns all documents, ignores `CoverageDepth`.
- **No debounce needed on search**: Indx is fast enough that debouncing search requests is unnecessary. Fire on every keystroke.

### Sorting Behavior

- **With search text**: Sorting is **2nd-order** — search relevancy (score) is always the primary sort. Sorting only applies to results included in the coverage step.
- **Empty search** (no text): Sorting becomes the **primary** ordering function.
- Works on both numbers and strings (A–Z, 1–9). Default: descending. Set `SortAscending = true` to invert.
- To reset: set `query.SortBy = null`.

### Facets Tip

When implementing search-as-you-type with a large dataset, consider only fetching facets (`EnableFacets = true`) after a small delay, not on every keystroke.

### Coverage Tuning

- `EnableCoverage` (default: `true`) — Toggle the coverage refinement step.
- `CoverageDepth` (default: `500`) — Number of top-K pattern-match candidates to evaluate. Higher = better recall, more latency. Auto-increases if `MaxNumberOfRecordsToReturn > CoverageDepth`. Set to `engine.Status.DocumentCount` for full-dataset coverage.
- `CoverageSetup` — Fine-grained control (see advanced sections below).

---

## Data Format

Indx accepts JSON arrays of objects. Nested fields are supported (schemaless):

```json
[
  { "id": 1, "title": "Product A", "specs": { "weight": 1.2, "color": "red" } },
  { "id": 2, "title": "Product B", "specs": { "weight": 0.8, "color": "blue" } }
]
```

Nested fields use dot notation: `specs.weight`, `specs.color`.

---

## Search UX Patterns

These patterns come from [indx-intrface](https://github.com/indxSearch/indx-intrface), a React component library for Indx Search. Even if you're not using the library, these are good principles to follow when building search UI on top of Indx.

### Preserving empty facets

When a user applies filters, some facet values may drop to 0 hits and disappear from the facets response. Don't remove them from the UI — keep showing them (greyed out, with count 0) so the user can still see and deselect them. Removing filter options mid-interaction is disorienting.

### Empty search as browse mode

Support an empty search state (`allowEmptySearch`) that returns all documents with facets and sorting. This lets users browse and filter before typing anything — useful for catalogue-style interfaces. Requires `enableFacets: true` and at least one facetable field.

### Facet debouncing

When doing search-as-you-type, search results need no debounce (Indx is fast enough to fire on every keystroke). But facet counts jumping on every character is noisy — debounce facet requests (e.g. 500ms) while keeping result updates immediate.

### Range filters from facet data

Use facet histograms to derive min/max bounds for range filter UI (sliders, inputs). This way the range controls automatically reflect the actual data spread rather than hardcoded limits.

### Active filter summary

Show all active filters (value filters and range filters) as removable chips above the results. Include a "reset all" action. This gives the user a clear picture of what's narrowing their results.

### Two-step result display (C# only)

The C# NuGet API returns document keys and scores (not full documents). Fetch full JSON separately via `GetJsonDataOfKey`. Only fetch the fields you need for display — keep the result list lightweight and load full details on demand. The HTTP API returns full document JSON directly in the search response, so this step is not needed there.

### React component library

For React 19+ projects, [@indxsearch/intrface](https://github.com/indxSearch/indx-intrface) implements all of the above patterns as drop-in components: `SearchProvider`, `SearchInput`, `SearchResults`, `ValueFilterPanel`, `RangeFilterPanel`, `ActiveFiltersPanel`, `SortByPanel`, and more. See the [indx-intrface README](https://github.com/indxSearch/indx-intrface) for full component API.

---

## Key Design Properties

- **No language configuration** — works across languages without tokenizers, stemmers, or stop words
- **Built-in typo tolerance** — pattern matching handles misspellings automatically
- **In-memory indexing** — all search indexes live in memory for speed; persistence is metadata-only
- **Linear coverage scaling** — coverage cost scales linearly with `coverageDepth`
- **Schemaless JSON** — nested objects supported, fields discovered automatically via `Init`/`Analyze`
- **Two-step retrieval (C# only)** — the C# NuGet API returns keys + scores; fetch full documents separately with `GetJsonDataOfKey`. The HTTP API returns full document JSON directly in the search response

## Resources

- [Indx Home](https://indx.co) — registration and licensing
- [API Documentation](https://docs.indx.co/api-41) — full C# API reference with How-To guides
- **C# / .NET**
  - [IndxSearchLib NuGet](https://www.nuget.org/packages/IndxSearchLib/) — core search engine (.NET 9)
  - [IndxCloudLoader](https://github.com/indxSearch/IndxCloudLoader) — C# data loading reference
- **HTTP API**
  - [IndxCloudApi](https://github.com/indxSearch/IndxCloudApi) — self-host server template (ASP.NET Core)
  - [OpenAPI spec](https://cloud.indx.co/swagger/v1/swagger.json) — machine-readable API definition
- **Node.js / TypeScript**
  - [@indxsearch/indx-types](https://www.npmjs.com/package/@indxsearch/indx-types) — TypeScript type definitions
  - [IndxNodeLoader](https://github.com/indxSearch/IndxNodeLoader) — Node.js data loading reference
- **Frontend**
  - [indx-intrface](https://github.com/indxSearch/indx-intrface) — React search UI components (@indxsearch/intrface)
