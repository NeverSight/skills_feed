---
name: google-developer-knowledge
description: "Search and retrieve Google's developer documentation using the Developer Knowledge API. Query documentation chunks, get full document content, or batch retrieve multiple documents. Covers ai.google.dev, developer.android.com, docs.cloud.google.com, firebase.google.com, and more."
---

# Google Developer Knowledge

Use this skill to search and retrieve content from Google's public developer documentation corpus using the Developer Knowledge API.

This skill uses simple bash scripts with curl (no dependencies required).

## Prerequisites

1.  **Enable the API**: Enable the [Developer Knowledge API](https://console.cloud.google.com/apis/library/developerknowledge.googleapis.com) in your Google Cloud project.

2.  **Create an API Key**:
    -   Go to the [Credentials page](https://console.cloud.google.com/apis/credentials)
    -   Click **Create credentials** → **API key**
    -   Restrict the key to **Developer Knowledge API** only

3.  **Set Environment Variable**:
    -   `DEVELOPERKNOWLEDGE_API_KEY`: Your Developer Knowledge API key

## Searchable Corpus

The API searches these domains:
-   `ai.google.dev`
-   `developer.android.com`
-   `developer.chrome.com`
-   `developers.google.com`
-   `docs.cloud.google.com`
-   `firebase.google.com`
-   `web.dev`
-   `www.tensorflow.org`

## Usage

### 1. Search for Documents

Search for document chunks matching a query. Returns snippets and parent document references.

```bash
./skills/google-developer-knowledge/scripts/search_docs.sh "How to use Gemini API in Python"
```

**With pagination:**
```bash
./skills/google-developer-knowledge/scripts/search_docs.sh "BigQuery" --page-size 10
```

### 2. Get a Single Document

Retrieve the full content of a document using its name from search results.

```bash
./skills/google-developer-knowledge/scripts/get_document.sh "documents/ai.google.dev/gemini-api/docs/get-started/python"
```

**Save to file:**
```bash
./skills/google-developer-knowledge/scripts/get_document.sh "documents/ai.google.dev/..." --output doc.json
```

### 3. Batch Get Documents

Retrieve up to 20 documents in a single API call.

```bash
./skills/google-developer-knowledge/scripts/batch_get_documents.sh \
  "documents/ai.google.dev/gemini-api/docs/get-started/python" \
  "documents/ai.google.dev/gemini-api/docs/models"
```

## Options

**search_docs.sh**
-   `query`: The search query (required)
-   `--page-size`: Number of results (1-20, default 5)
-   `--page-token`: Token for next page of results
-   `--output`: Save results to JSON file

**get_document.sh**
-   `name`: Document name from search results (required)
-   `--output`: Save content to file

**batch_get_documents.sh**
-   `names`: Space-separated document names (up to 20)
-   `--output`: Save all documents to directory

