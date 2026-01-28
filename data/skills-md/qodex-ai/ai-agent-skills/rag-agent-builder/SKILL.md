---
name: rag-agent-builder
description: Build Retrieval-Augmented Generation (RAG) applications that combine LLM capabilities with external knowledge sources. Covers vector databases, embeddings, retrieval strategies, and response generation. Use when building document Q&A systems, knowledge base applications, enterprise search, or combining LLMs with custom data.
---

# RAG Agent Builder

Build powerful Retrieval-Augmented Generation (RAG) applications that enhance LLM capabilities with external knowledge sources, enabling accurate, contextualized AI responses.

## Quick Start

Get started with RAG implementations in the examples and utilities:

- **Examples**: See [`examples/`](examples/) directory for complete implementations:
  - [`basic_rag.py`](examples/basic_rag.py) - Simple chunk-embed-retrieve-generate pipeline
  - [`retrieval_strategies.py`](examples/retrieval_strategies.py) - Hybrid search, reranking, and filtering
  - [`agentic_rag.py`](examples/agentic_rag.py) - Agent-controlled retrieval with iterative refinement

- **Utilities**: See [`scripts/`](scripts/) directory for helper modules:
  - [`embedding_management.py`](scripts/embedding_management.py) - Embedding generation, normalization, and caching
  - [`vector_db_manager.py`](scripts/vector_db_manager.py) - Vector database abstraction and factory
  - [`rag_evaluation.py`](scripts/rag_evaluation.py) - Retrieval and answer quality metrics

## Overview

RAG systems combine three key components:
1. **Document Retrieval** - Find relevant information from knowledge bases
2. **Context Integration** - Pass retrieved context to the LLM
3. **Response Generation** - Generate answers grounded in the retrieved information

This skill covers building production-ready RAG applications with various frameworks and approaches.

## Core Concepts

### What is RAG?

RAG augments LLM knowledge with external data:
- **Without RAG**: LLM relies on training data (may be outdated or limited)
- **With RAG**: LLM uses real-time, custom knowledge + training knowledge

### When to Use RAG

- **Document Q&A**: Answer questions about PDFs, books, reports
- **Knowledge Base Search**: Query internal documentation, wikis
- **Enterprise Search**: Search proprietary company data
- **Context-Specific Assistants**: Customer support, HR assistants
- **Fact-Heavy Applications**: Legal docs, medical records, financial data

### When RAG Might Not Be Needed

- General knowledge questions (ChatGPT-like)
- Real-time data that changes constantly (use tools instead)
- Very simple lookup tasks (use database queries)

## Architecture Patterns

### Basic RAG Pipeline

```
Documents → Chunks → Embeddings → Vector DB
                                        ↓
User Question → Embedding → Retrieval → LLM → Answer
                              ↑         ↓
                         Vector DB    Context
```

### Advanced RAG Patterns

#### 1. Agentic RAG
- Agent decides what to retrieve and when
- Can refine queries iteratively
- Better for complex reasoning

#### 2. Hierarchical RAG
- Multi-level document structure
- Search at different levels of detail
- More flexible organization

#### 3. Hybrid Search RAG
- Combines keyword search (BM25) + semantic search (embeddings)
- Captures both exact matches and meaning
- Better for mixed query types

#### 4. Corrective RAG (CRAG)
- Evaluates retrieved documents for relevance
- Retrieves additional sources if needed
- Ensures high-quality context

## Implementation Components

### 1. Document Processing

**Chunking Strategies**:
```python
# Simple fixed-size chunks
chunks = split_text(doc, chunk_size=1000, overlap=100)

# Semantic chunks (group by meaning)
chunks = semantic_chunking(doc, max_tokens=512)

# Hierarchical chunks (different levels)
chapters = split_by_heading(doc)
chunks = split_each_chapter(chapters, size=1000)
```

**Key Considerations**:
- Chunk size affects retrieval quality and cost
- Overlap helps maintain context between chunks
- Semantic chunking preserves meaning better

### 2. Embedding Generation

**Popular Embedding Models**:
- OpenAI: `text-embedding-3-small`, `text-embedding-3-large`
- Open Source: `all-MiniLM-L6-v2`, `all-mpnet-base-v2`
- Domain-Specific: Domain-trained embeddings for specialized knowledge

**Best Practices**:
- Use consistent embedding model for retrieval and queries
- Store embeddings with normalized vectors
- Update embeddings when documents change

### 3. Vector Databases

**Popular Options**:
- **Pinecone**: Managed, serverless, easy to scale
- **Weaviate**: Open-source, self-hosted, flexible
- **Milvus**: Open-source, high performance
- **Chroma**: Lightweight, good for prototypes
- **Qdrant**: Production-grade, high-performance

**Selection Criteria**:
- Scale requirements (data volume, queries per second)
- Latency needs (real-time vs batch)
- Cost considerations
- Deployment preferences (managed vs self-hosted)

### 4. Retrieval Strategies

**Retrieval Methods**:
```python
# Similarity search (most common)
results = vector_db.query(question_embedding, k=5)

# Hybrid search (keyword + semantic)
keyword_results = bm25.search(question, k=3)
semantic_results = vector_db.query(embedding, k=3)
results = combine_and_rank(keyword_results, semantic_results)

# Reranking (improve relevance)
retrieved = initial_retrieval(query)
reranked = rerank_by_relevance(retrieved, query)
```

**Retrieval Parameters**:
- **k** (number of results): Balance between context and relevance
- **Similarity threshold**: Filter out low-relevance results
- **Diversity**: Return varied results vs best matches

### 5. Context Integration

**Context Window Management**:
```python
# Fit retrieved documents into context window
def prepare_context(retrieved_docs, max_tokens=3000):
    context = ""
    for doc in retrieved_docs:
        if len(tokenize(context + doc)) <= max_tokens:
            context += doc
        else:
            break
    return context
```

**Prompt Design**:
```
You are a helpful assistant. Answer the question based on the provided context.

Context:
{retrieved_documents}

Question: {user_question}

Answer:
```

### 6. Response Generation

**Generation Strategies**:
- **Direct Generation**: LLM answers from context
- **Summarization**: Summarize multiple retrieved docs first
- **Fact-Grounding**: Ensure answer cites sources
- **Iterative Refinement**: Refine based on user feedback

## Implementation Patterns

### Pattern 1: Basic RAG

Simplest RAG implementation:
1. Split documents into chunks
2. Generate embeddings for each chunk
3. Store in vector database
4. Retrieve top-k similar chunks for query
5. Pass to LLM with context

**Pros**: Simple, fast, works well for straightforward QA
**Cons**: May miss relevant context, no refinement

### Pattern 2: Agentic RAG

Agent controls retrieval:
1. Agent receives user question
2. Decides whether to retrieve documents
3. Formulates retrieval query (may differ from original)
4. Retrieves relevant documents
5. Can iterate or use tools
6. Generates final answer

**Pros**: Better for complex questions, iterative improvement
**Cons**: More complex, higher costs

### Pattern 3: Corrective RAG (CRAG)

Validates retrieved documents:
1. Retrieve documents for question
2. Grade each document for relevance
3. If poor relevance:
   - Try different retrieval strategy
   - Expand search scope
   - Retrieve from different sources
4. Generate answer from validated context

**Pros**: Higher quality answers, adapts to failures
**Cons**: More API calls, slower

## Popular Frameworks

### LangChain
```python
from langchain.document_loaders import PDFLoader
from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores import Pinecone
from langchain.chains import RetrievalQA

# Load documents
loader = PDFLoader("document.pdf")
docs = loader.load()

# Create RAG chain
embeddings = OpenAIEmbeddings()
vectorstore = Pinecone.from_documents(docs, embeddings)
qa = RetrievalQA.from_chain_type(
    llm=ChatOpenAI(),
    chain_type="stuff",
    retriever=vectorstore.as_retriever()
)

answer = qa.run("What is the document about?")
```

### LlamaIndex
```python
from llama_index import GPTVectorStoreIndex, SimpleDirectoryReader

# Load documents
documents = SimpleDirectoryReader("./data").load_data()

# Create index
index = GPTVectorStoreIndex.from_documents(documents)

# Query
response = index.as_query_engine().query("What is the main topic?")
```

### CrewAI with RAG
```python
from crewai import Agent, Task, Crew
from tools import retrieval_tool

researcher = Agent(
    role="Research Assistant",
    goal="Research topics using knowledge base",
    tools=[retrieval_tool]
)

research_task = Task(
    description="Research the topic: {topic}",
    agent=researcher
)
```

## Best Practices

### Document Preparation
- ✓ Clean and normalize text (remove headers, footers)
- ✓ Preserve document structure when possible
- ✓ Add metadata (source, date, category)
- ✓ Handle PDFs with OCR if scanned
- ✓ Test chunk sizes for your domain

### Embedding Strategy
- ✓ Use same embedding model for indexing and queries
- ✓ Fine-tune embeddings for domain-specific needs
- ✓ Normalize embeddings for consistency
- ✓ Monitor embedding quality metrics

### Retrieval Optimization
- ✓ Tune k (number of results) for your use case
- ✓ Use reranking for quality improvement
- ✓ Implement relevance filtering
- ✓ Monitor retrieval precision and recall
- ✓ Cache frequently retrieved documents

### Generation Quality
- ✓ Include source citations in answers
- ✓ Prompt LLM to indicate confidence
- ✓ Ask to cite specific documents
- ✓ Generate summaries for long contexts
- ✓ Validate answers against context

### Monitoring & Evaluation
- ✓ Track retrieval metrics (precision, recall, MRR)
- ✓ Monitor answer quality and relevance
- ✓ Log failed retrievals for improvement
- ✓ Collect user feedback
- ✓ Iterate based on failures

## Common Challenges & Solutions

### Challenge: Irrelevant Retrieval
**Solutions**:
- Improve chunking strategy
- Better embedding model
- Add document metadata to queries
- Implement reranking
- Use hybrid search

### Challenge: Context Too Large
**Solutions**:
- Reduce chunk size
- Retrieve fewer results (smaller k)
- Summarize retrieved context
- Use hierarchical retrieval
- Filter by relevance score

### Challenge: Missing Information
**Solutions**:
- Increase k (retrieve more)
- Improve embedding model
- Better preprocessing
- Use multiple search strategies
- Add document hierarchy

### Challenge: Slow Performance
**Solutions**:
- Use managed vector database
- Cache embeddings
- Batch process documents
- Optimize chunk size
- Use smaller embedding model for speed

## Evaluation Metrics

**Retrieval Metrics**:
- **Precision**: % of retrieved docs that are relevant
- **Recall**: % of relevant docs that are retrieved
- **MRR (Mean Reciprocal Rank)**: Rank of first relevant result
- **NDCG (Normalized DCG)**: Quality of ranking

**Answer Quality Metrics**:
- **Relevance**: Does answer address the question?
- **Correctness**: Is the answer factually accurate?
- **Grounding**: Is answer supported by context?
- **User Satisfaction**: Would user find answer helpful?

## Advanced Techniques

### 1. Query Expansion
```python
# Expand query with related terms
expanded_query = query + " " + synonym_expansion(query)
results = retrieve(expanded_query)
```

### 2. Document Compression
```python
# Compress retrieved docs before passing to LLM
compressed = compress_documents(retrieved_docs, query)
context = format_context(compressed)
```

### 3. Active Retrieval
```python
# Iteratively refine retrieval based on LLM output
query = user_question
while iterations < max:
    results = retrieve(query)
    answer = generate_with_context(results)
    if answer_complete(answer):
        break
    query = refine_query(answer)
```

### 4. Multi-Modal RAG
```python
# Retrieve both text and images
text_results = text_retriever.query(question)
image_results = image_retriever.query(question)
context = combine_multimodal(text_results, image_results)
```

## Resources & References

### Key Papers
- "Retrieval-Augmented Generation for Knowledge-Intensive NLP Tasks" (Lewis et al.)
- "REALM: Retrieval-Augmented Language Model Pre-Training" (Guu et al.)

### Frameworks
- LangChain: https://python.langchain.com/
- LlamaIndex: https://www.llamaindex.ai/
- HayStack: https://haystack.deepset.ai/

### Vector Databases
- Pinecone: https://www.pinecone.io/
- Weaviate: https://weaviate.io/
- Qdrant: https://qdrant.tech/

### Embedding Models
- OpenAI: https://platform.openai.com/docs/guides/embeddings
- Hugging Face: https://huggingface.co/models?pipeline_tag=sentence-similarity

## Next Steps

1. **Choose your stack**: Decide on framework (LangChain, LlamaIndex, etc.)
2. **Prepare documents**: Process and chunk your knowledge base
3. **Select embeddings**: Choose embedding model for your domain
4. **Pick vector DB**: Select storage solution for scale
5. **Build pipeline**: Implement retrieval and generation
6. **Evaluate**: Test on sample questions and iterate
7. **Monitor**: Track quality metrics in production

