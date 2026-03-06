---
name: ai-engineer
description: Build LLM applications, RAG systems, and prompt pipelines. Use for LLM features, chatbots, or AI-powered applications.
---

# AI Engineering

Build production LLM applications and AI systems.

## When to Use

- Integrating LLM APIs
- Building RAG systems
- Creating AI agents
- Vector database setup
- Token optimization

## LLM Integration

### API Setup

```python
from anthropic import Anthropic

client = Anthropic()

def chat(messages: list[dict], system: str = None) -> str:
    response = client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=1024,
        system=system or "You are a helpful assistant.",
        messages=messages
    )
    return response.content[0].text

# With retry and error handling
from tenacity import retry, stop_after_attempt, wait_exponential

@retry(stop=stop_after_attempt(3), wait=wait_exponential(min=1, max=10))
def safe_chat(messages, system=None):
    try:
        return chat(messages, system)
    except Exception as e:
        logger.error(f"LLM call failed: {e}")
        raise
```

### Structured Output

```python
import json

def extract_structured(text: str, schema: dict) -> dict:
    prompt = f"""Extract information from the text according to this schema:
{json.dumps(schema, indent=2)}

Text: {text}

Return valid JSON only."""

    response = chat([{"role": "user", "content": prompt}])
    return json.loads(response)
```

## RAG System

### Document Processing

```python
from langchain.text_splitter import RecursiveCharacterTextSplitter

def chunk_documents(docs: list[str], chunk_size=1000, overlap=200):
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=overlap,
        separators=["\n\n", "\n", ". ", " "]
    )
    return splitter.split_documents(docs)
```

### Vector Store

```python
from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams

client = QdrantClient(":memory:")  # or url="http://localhost:6333"

# Create collection
client.create_collection(
    collection_name="docs",
    vectors_config=VectorParams(size=1536, distance=Distance.COSINE)
)

# Upsert vectors
client.upsert(
    collection_name="docs",
    points=[
        {"id": i, "vector": embed(chunk), "payload": {"text": chunk}}
        for i, chunk in enumerate(chunks)
    ]
)

# Search
results = client.search(
    collection_name="docs",
    query_vector=embed(query),
    limit=5
)
```

### RAG Query

```python
def rag_query(question: str, top_k=5) -> str:
    # Retrieve relevant chunks
    results = client.search(
        collection_name="docs",
        query_vector=embed(question),
        limit=top_k
    )

    context = "\n\n".join([r.payload["text"] for r in results])

    prompt = f"""Answer based on the context below.

Context:
{context}

Question: {question}

Answer:"""

    return chat([{"role": "user", "content": prompt}])
```

## Cost Optimization

- Cache frequent queries
- Use smaller models for simple tasks
- Batch requests when possible
- Track token usage per feature
- Set max_tokens appropriately

## Examples

**Input:** "Add AI chat to this app"
**Action:** Set up LLM client, create chat endpoint, add error handling

**Input:** "Build RAG for documentation"
**Action:** Chunk docs, create embeddings, set up vector store, implement search
