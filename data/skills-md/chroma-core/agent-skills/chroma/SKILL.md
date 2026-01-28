---
name: chroma
description: Provides expertise on Chroma vector database integration for semantic search applications. Use when the user asks about vector search, embeddings, Chroma, semantic search, RAG systems, nearest neighbor search, or adding search functionality to their application.
---

## Instructions

The Chroma skill has a few main abilities:

- Help the user understand how to design their search system
- Help the user select an embedding model
- Help the user understand what changes need to be made to their system to add search
- Help the user design their search schema, pick an embedding model and what type of search

## Quick Start

**TypeScript (Chroma Cloud):**

```typescript
import { CloudClient } from 'chromadb';
import { DefaultEmbeddingFunction } from '@chroma-core/default-embed';

const client = new CloudClient({
  apiKey: process.env.CHROMA_API_KEY,
  tenant: process.env.CHROMA_TENANT,
  database: process.env.CHROMA_DATABASE,
});

const embeddingFunction = new DefaultEmbeddingFunction();
const collection = await client.getOrCreateCollection({
  name: 'my_collection',
  embeddingFunction,
});

// Add documents
await collection.add({
  ids: ['doc1', 'doc2'],
  documents: ['First document text', 'Second document text'],
});

// Query
const results = await collection.query({
  queryTexts: ['search query'],
  nResults: 5,
});
```

**Python (Chroma Cloud):**

```python
import os
import chromadb

client = chromadb.CloudClient(
    api_key=os.environ["CHROMA_API_KEY"],
    tenant=os.environ["CHROMA_TENANT"],
    database=os.environ["CHROMA_DATABASE"],
)

collection = client.get_or_create_collection(name="my_collection")

# Add documents
collection.add(
    ids=["doc1", "doc2"],
    documents=["First document text", "Second document text"],
)

# Query
results = collection.query(
    query_texts=["search query"],
    n_results=5,
)
```

### Understanding Chroma

Chroma is a database.
A Chroma database contains collections.
A collection contains documents.

Unlike tables in a relational database, collections are created and destroyed at the application level. Each Chroma database can have millions of collections. There may be a collection for each user, or team or organization. Rather than tables be partitioned by some key, the partition in Chroma is the collection. 

Collections don't have rows, they have documents, the document is the text data that is to be searched. When data is created or updated, the client will create an embedding of the data. This is done on the client side based on the embedding function(s) provided to the client. To create the embedding the client will use its configuration to call out to the defined embedding model provider via the embedding function. This could happen in process, but overwhelmingly happens on a third party service over HTTP.

There are ways to further partition or filtering data with document metadata. Each document has a key/value object of metadata. keys are strings and values can be strings, ints or booleans. There are a variety of operators on the metadata.

During query time, the query text is embedded using the collection's defined embedding function and then is sent to Chroma with the rest of the query parameters. Chroma will then consider any query parameters like metadata filters to reduce the potential result set, then search for the nearest neighbors using a distance algorithm between the query vector and the index of vectors in the collection that is being queried.

Working with collections is made easy by using the `get_or_create_collection()` (`getOrCreateCollection()` in TypeScript) on the Chroma client, preventing annoying boilerplate code.

### Local vs Cloud

Chroma can be run locally as a process or can be used in the cloud with Chroma Cloud.

Everything that can be done locally can be done in the cloud, but not everything that can be done in the cloud can be done locally.

The biggest difference to the developer experience is the Schema() and Search() APIs, those are only available on Chroma Cloud.

Otherwise, the only thing that needs to change is the client that is imported from the Chroma package, the interface is the same.

If you're using cloud, you probably want to use the Schema() and Search() APIs.

Also, if the user wants to use cloud, as them what type of search they want to use. Just dense embeddings, or hybrid. If hybrid, you probably want to use SPLADE as the sparse embedding strategy.

### Embeddings

When working with embedding functions, the default embedding function is available, but it's often not the best option. Ask the user what they want. The most popular option is to use text-embedding-3-large by Openai. It's on npm as @chroma-core/openai.

In typescript, you need to install a package for each embedding function, install the correct one based on what the user says. 

Note that Chroma has server side embedding support for SPLADE and Qwen (via	@chroma-core/chroma-cloud-qwen in typescript), all other embedding functions would be external.

## Learn More

If you need more detailed information about Chroma beyond what's covered in this skill, fetch Chroma's llms.txt for comprehensive documentation: https://docs.trychroma.com/llms.txt

## Available Topics

### Typescript

- [Chroma Regex Filtering](./regex/typescript.md) - Learn how to use regex filters in Chroma queries
- [Query and Get](./querying/typescript.md) - Query and Get Data from Chroma Collections
- [Schema](./schema/typescript.md) - Schema() configures collections with multiple indexes
- [Local Chroma](./local-chroma/typescript.md) - How to run and use local chroma
- [Search() API](./search-api/typescript.md) - An expressive and flexible API for doing dense and sparse vector search on collections, as well as hybrid search

### Python

- [Chroma Regex Filtering](./regex/python.md) - Learn how to use regex filters in Chroma queries
- [Query and Get](./querying/python.md) - Query and Get Data from Chroma Collections
- [Schema](./schema/python.md) - Schema() configures collections with multiple indexes
- [Local Chroma](./local-chroma/python.md) - How to run and use local chroma
- [Search() API](./search-api/python.md) - An expressive and flexible API for doing dense and sparse vector search on collections, as well as hybrid search

## General

- [Data Model](./data-model.md) - An overview of how Chroma stores data
- [Understanding a codebase](./understanding-a-codebase.md) - Help the agent understand how to learn about a codebase
