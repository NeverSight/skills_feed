---
name: rag-builder
description: Build Retrieval-Augmented Generation systems with vector databases
---


# RAG Builder Skill

> Build the RAG (Retrieval-Augmented Generation) server using Qdrant.

## Overview

The RAG server provides vector search capabilities for the workspace:
- Document ingestion with chunking
- Semantic search across collections
- Multi-project isolation via collections

## Prerequisites

```bash
pip install qdrant-client sentence-transformers mcp fastembed
```

## Using the MCP Server

The Reflex plugin includes a pre-configured Qdrant MCP server. Use these tools:

### Store Documents

```
Tool: qdrant-store
Information: "Your document text here..."
Metadata:
  source: "user_upload"
  type: "notes"
```

### Search Documents

```
Tool: qdrant-find
Query: "quantum computing applications"
```

## Build Steps (Custom Server)

### Step 1: Create the RAG Server

**File: `mcp/servers/rag-server/server.py`**

```python
#!/usr/bin/env python3
"""
RAG MCP Server - Vector search using Qdrant.
"""

import asyncio
import json
import os
from datetime import datetime
from typing import Optional

from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams, PointStruct
from mcp.server import Server
from mcp.server.stdio import stdio_server
from sentence_transformers import SentenceTransformer

# Configuration
QDRANT_URL = os.getenv("QDRANT_URL", "http://localhost:6333")
EMBEDDING_MODEL = os.getenv("EMBEDDING_MODEL", "all-MiniLM-L6-v2")
DEFAULT_COLLECTION = os.getenv("COLLECTION_NAME", "default_memories")
CHUNK_SIZE = int(os.getenv("CHUNK_SIZE", "512"))
CHUNK_OVERLAP = int(os.getenv("CHUNK_OVERLAP", "50"))


class RAGServer:
    def __init__(self):
        self.server = Server("rag-server")

        # Initialize Qdrant
        self.client = QdrantClient(url=QDRANT_URL)

        # Initialize embedding model
        self.embedder = SentenceTransformer(EMBEDDING_MODEL)
        self.vector_size = self.embedder.get_sentence_embedding_dimension()

        self._setup_tools()

    def _ensure_collection(self, name: str):
        """Ensure collection exists."""
        collections = self.client.get_collections().collections
        if not any(c.name == name for c in collections):
            self.client.create_collection(
                collection_name=name,
                vectors_config=VectorParams(
                    size=self.vector_size,
                    distance=Distance.COSINE
                )
            )

    def _chunk_text(self, text: str) -> list[str]:
        """Split text into overlapping chunks."""
        words = text.split()
        chunks = []
        for i in range(0, len(words), CHUNK_SIZE - CHUNK_OVERLAP):
            chunk = " ".join(words[i:i + CHUNK_SIZE])
            if chunk:
                chunks.append(chunk)
        return chunks

    def _setup_tools(self):

        @self.server.tool()
        async def ingest(
            content: str,
            collection: str = DEFAULT_COLLECTION,
            metadata: Optional[dict] = None,
            doc_id: Optional[str] = None
        ) -> str:
            """
            Ingest a document into the vector database.

            Args:
                content: Document text to ingest
                collection: Collection name (use project name for isolation)
                metadata: Optional metadata (source, type, date, etc.)
                doc_id: Optional custom document ID
            """
            self._ensure_collection(collection)
            chunks = self._chunk_text(content)

            base_id = doc_id or f"doc_{datetime.now().timestamp()}"

            # Generate embeddings
            embeddings = self.embedder.encode(chunks).tolist()

            # Prepare metadata
            base_meta = metadata or {}
            base_meta["ingested_at"] = datetime.now().isoformat()
            base_meta["source_doc"] = base_id

            # Create points
            points = [
                PointStruct(
                    id=hash(f"{base_id}_chunk_{i}") % (2**63),
                    vector=embeddings[i],
                    payload={**base_meta, "chunk_index": i, "content": chunk}
                )
                for i, chunk in enumerate(chunks)
            ]

            self.client.upsert(collection_name=collection, points=points)

            return json.dumps({
                "status": "success",
                "collection": collection,
                "chunks": len(chunks),
                "doc_id": base_id
            })

        @self.server.tool()
        async def search(
            query: str,
            collection: str = DEFAULT_COLLECTION,
            n_results: int = 5
        ) -> str:
            """
            Search for relevant documents.

            Args:
                query: Search query
                collection: Collection to search
                n_results: Number of results (default 5)
            """
            self._ensure_collection(collection)

            query_embedding = self.embedder.encode([query])[0].tolist()

            results = self.client.search(
                collection_name=collection,
                query_vector=query_embedding,
                limit=n_results
            )

            formatted = [
                {
                    "id": str(r.id),
                    "content": r.payload.get("content", ""),
                    "metadata": {k: v for k, v in r.payload.items() if k != "content"},
                    "score": r.score
                }
                for r in results
            ]

            return json.dumps({
                "query": query,
                "collection": collection,
                "results": formatted
            })

        @self.server.tool()
        async def list_collections() -> str:
            """List all collections."""
            collections = self.client.get_collections()
            return json.dumps({
                "collections": [
                    {"name": c.name}
                    for c in collections.collections
                ]
            })

    async def run(self):
        async with stdio_server() as (read_stream, write_stream):
            await self.server.run(read_stream, write_stream)


def main():
    server = RAGServer()
    asyncio.run(server.run())


if __name__ == "__main__":
    main()
```

### Step 2: Create Requirements

**File: `mcp/servers/rag-server/requirements.txt`**

```
mcp>=1.0.0
qdrant-client>=1.7.0
sentence-transformers>=2.2.0
```

### Step 3: Create Test Script

**File: `mcp/servers/rag-server/test_rag.py`**

```python
#!/usr/bin/env python3
"""Quick test for RAG server components."""

import os
import sys

# Set up path
sys.path.insert(0, os.path.dirname(__file__))

def test_qdrant():
    """Test Qdrant is working."""
    from qdrant_client import QdrantClient
    client = QdrantClient(url="http://localhost:6333")
    collections = client.get_collections()
    print(f"✅ Qdrant working, {len(collections.collections)} collections")

def test_embeddings():
    """Test embedding model."""
    from sentence_transformers import SentenceTransformer
    model = SentenceTransformer('all-MiniLM-L6-v2')
    embedding = model.encode(["test sentence"])
    assert embedding.shape == (1, 384)
    print("✅ Embeddings working")

def test_server_init():
    """Test server initialization."""
    from server import RAGServer
    server = RAGServer()
    assert server.client is not None
    assert server.embedder is not None
    print("✅ Server initialization working")

if __name__ == "__main__":
    test_qdrant()
    test_embeddings()
    test_server_init()
    print("\n✅ All RAG tests passed!")
```

## Verification

```bash
# Start Qdrant (if using Docker)
docker run -d -p 6333:6333 qdrant/qdrant

# Navigate to server directory
cd mcp/servers/rag-server

# Install dependencies
pip install -r requirements.txt

# Run tests
python test_rag.py

# Expected output:
# ✅ Qdrant working, 0 collections
# ✅ Embeddings working
# ✅ Server initialization working
# ✅ All RAG tests passed!
```

## Usage Examples

Once running as MCP server:

```python
# Ingest a document
await ingest(
    content="Your document text here...",
    collection="project_alpha_docs",
    metadata={"source": "user_upload", "type": "notes"}
)

# Search
results = await search(
    query="quantum computing applications",
    collection="project_alpha_docs",
    n_results=5
)

# List collections
collections = await list_collections()
```

## Multi-Project Isolation

```python
# Each project gets its own collections
"project_alpha_docs"     # Project Alpha documentation
"project_alpha_code"     # Project Alpha code snippets
"project_beta_docs"      # Project Beta documentation
"shared_knowledge"       # Cross-project shared info
```

## Configuration

Environment variables:
```bash
QDRANT_URL=http://localhost:6333
EMBEDDING_MODEL=all-MiniLM-L6-v2
COLLECTION_NAME=default_memories
CHUNK_SIZE=512
CHUNK_OVERLAP=50
```

## After Building

1. ✅ Run tests to verify
2. Update `CLAUDE.md` status
3. Proceed to `skills/router-builder/SKILL.md`

## Refinement Notes

> Add notes here as we build and discover what works/doesn't work.

- [ ] Initial implementation
- [ ] Tested with real documents
- [ ] Integrated with MCP config
- [ ] Performance tuned
