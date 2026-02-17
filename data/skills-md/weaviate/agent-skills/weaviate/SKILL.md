---
name: weaviate
description: Search, query, and manage Weaviate vector database collections. Use for semantic search, hybrid search, keyword search, natural language queries with AI-generated answers, collection management, data exploration, filtered fetching, data imports from CSV/JSON/JSONL files, create example data and collection creation.
---

# Weaviate Database Operations

This skill provides comprehensive access to Weaviate vector databases including search operations, natural language queries, schema inspection, data exploration, filtered fetching, collection creation, and data imports.

### Weaviate Cloud Instance

If the user does not have an instance yet, direct them to the cloud console to register and create a free sandbox. Create a Weaviate instance via [Weaviate Cloud](https://console.weaviate.cloud/).

## Environment Variables

**Required:**

- `WEAVIATE_URL` - Your Weaviate Cloud cluster URL
- `WEAVIATE_API_KEY` - Your Weaviate API key

**External Provider Keys (auto-detected):**
Set only the keys your collections use, refer to [Environment Requirements](references/environment_requirements.md) for more information.

## Script Index

### Search & Query

- [Query Agent - Ask Mode](references/ask.md): Use when the user wants a **direct answer** to a question based on collection data. The Query Agent synthesizes information from one or more collections and returns a structured response with source citations (collection name and object ID).
- [Query Agent - Search Mode](references/query_search.md): Use when the user wants to **explore or browse raw objects** across one or more collections. Unlike ask mode, this returns the actual data objects rather than a synthesized answer.
- [Hybrid Search](references/hybrid_search.md): **Default choice for most searches.** Provides a good balance of semantic understanding and exact keyword matching. Use this when you are unsure which search type to pick.
- [Semantic Search](references/semantic_search.md): Use for finding **conceptually similar content** regardless of exact wording. Best when the intent matters more than specific keywords.
- [Keyword Search](references/keyword_search.md): Use for finding **exact terms, IDs, SKUs, or specific text patterns**. Best when precise keyword matching is needed rather than semantic similarity.

### Collection Management

- [List Collections](references/list_collections.md): Use to **discover what collections exist** in the Weaviate instance. This should typically be the first step before performing any search or data operation.
- [Get Collection Details](references/get_collection.md): Use to **understand a collection's schema** — its properties, data types, vectorizer configuration, replication factor, and multi-tenancy status. Helpful before running searches or imports.
- [Explore Collection](references/explore_collection.md): Use to **analyze data distribution, top values, and inspect actual content** in a collection. Helpful for understanding what data looks like before querying.
- [Create Collection](references/create_collection.md): Use to **create new collections with custom schemas** before importing data. Do not specify a vectorizer unless the user explicitly requests one (the default `text2vec_weaviate` is used).

### Data Operations

- [Fetch and Filter](references/fetch_filter.md): Use to **retrieve specific objects by ID** or **strictly filtered subsets** of data. Best for precise data retrieval rather than search.
- [Import Data](references/import_data.md): Use to **bulk import data** into an existing collection from CSV, JSON, or JSONL files.
- [Create Example Data](references/example_data.md): Use to create example data for immediate use of other skills, if no data is available or user requests some toy data.

## Recommendations

1. **Start by listing collections** if you don't know what's available:

   ```bash
   uv run scripts/list_collections.py
   ```

2. **Ask the user** if they want to **create example data** if nothing is available and the user requests it. Otherwise continue.

  ```bash
  uv run scripts/example_data.py
  ```

3. **Get collection details** to understand the schema:

   ```bash
   uv run scripts/get_collection.py --name "COLLECTION_NAME"
   ```

4. **Explore collection data** to see values and statistics:

   ```bash
   uv run scripts/explore_collection.py "COLLECTION_NAME"
   ```

5. **Import data** to populate a new collection (if needed):

   ```bash
   uv run scripts/import.py "data.csv" --collection "CollectionName"
   ```

6. **Do not specify a vectorizer when creating collections** unless requested:

   ```bash
   uv run scripts/create_collection.py Article \
     --properties '[{"name": "title", "data_type": "text"}, {"name": "body", "data_type": "text"}]'
   ```

7. **Choose the right search type:**
   - Get AI-powered answers with source citations across multiple collections → `ask.py`
   - Get raw objects from multiple collections → `query_search.py`
   - General search → `hybrid_search.py` (default)
   - Conceptual similarity → `semantic_search.py`
   - Exact terms/IDs → `keyword_search.py`

## Output Formats

All scripts support:

- **Markdown tables** (default and recommended)
- **JSON** (`--json` flag)

## Error Handling

Common errors:

- `WEAVIATE_URL not set` → Set the environment variable
- `Collection not found` → Use `list_collections.py` to see available collections
- `Authentication error` → Check API keys for both Weaviate and vectorizer providers
