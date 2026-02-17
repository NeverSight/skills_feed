---
name: langchain-agents
description: Use when "LangChain", "LLM chains", "ReAct agents", "tool calling", or asking about "RAG pipelines", "conversation memory", "document QA", "agent tools", "LangSmith"
version: 1.0.0
---

# LangChain - LLM Applications with Agents & RAG

The most popular framework for building LLM-powered applications.

## When to Use

- Building agents with tool calling and reasoning (ReAct pattern)
- Implementing RAG (retrieval-augmented generation) pipelines
- Need to swap LLM providers easily (OpenAI, Anthropic, Google)
- Creating chatbots with conversation memory
- Rapid prototyping of LLM applications

---

## Core Components

| Component | Purpose | Key Concept |
|-----------|---------|-------------|
| **Chat Models** | LLM interface | Unified API across providers |
| **Agents** | Tool use + reasoning | ReAct pattern |
| **Chains** | Sequential operations | Composable pipelines |
| **Memory** | Conversation state | Buffer, summary, vector |
| **Retrievers** | Document lookup | Vector search, hybrid |
| **Tools** | External capabilities | Functions agents can call |

---

## Agent Patterns

| Pattern | Description | Use Case |
|---------|-------------|----------|
| **ReAct** | Reason-Act-Observe loop | General tool use |
| **Plan-and-Execute** | Plan first, then execute | Complex multi-step |
| **Self-Ask** | Generate sub-questions | Research tasks |
| **Structured Chat** | JSON tool calling | API integration |

### Tool Definition

| Element | Purpose |
|---------|---------|
| **Name** | How agent refers to tool |
| **Description** | When to use (critical for selection) |
| **Parameters** | Input schema |
| **Return type** | What agent receives back |

**Key concept**: Tool descriptions are critical—the LLM uses them to decide which tool to call. Be specific about when and why to use each tool.

---

## RAG Pipeline Stages

| Stage | Purpose | Options |
|-------|---------|---------|
| **Load** | Ingest documents | Web, PDF, GitHub, DBs |
| **Split** | Chunk into pieces | Recursive, semantic |
| **Embed** | Convert to vectors | OpenAI, Cohere, local |
| **Store** | Index vectors | Chroma, FAISS, Pinecone |
| **Retrieve** | Find relevant chunks | Similarity, MMR, hybrid |
| **Generate** | Create response | LLM with context |

### Chunking Strategies

| Strategy | Best For | Typical Size |
|----------|----------|--------------|
| **Recursive** | General text | 500-1000 chars |
| **Semantic** | Coherent passages | Variable |
| **Token-based** | LLM context limits | 256-512 tokens |

### Retrieval Strategies

| Strategy | How It Works |
|----------|--------------|
| **Similarity** | Nearest neighbors by embedding |
| **MMR** | Diversity + relevance balance |
| **Hybrid** | Keyword + semantic combined |
| **Self-query** | LLM generates metadata filters |

---

## Memory Types

| Type | Stores | Best For |
|------|--------|----------|
| **Buffer** | Full conversation | Short conversations |
| **Window** | Last N messages | Medium conversations |
| **Summary** | LLM-generated summary | Long conversations |
| **Vector** | Embedded messages | Semantic recall |
| **Entity** | Extracted entities | Track facts about people/things |

**Key concept**: Buffer memory grows unbounded. Use summary or vector for long conversations to stay within context limits.

---

## Document Loaders

| Source | Loader Type |
|--------|-------------|
| **Web pages** | WebBaseLoader, AsyncChromium |
| **PDFs** | PyPDFLoader, UnstructuredPDF |
| **Code** | GitHubLoader, DirectoryLoader |
| **Databases** | SQLDatabase, Postgres |
| **APIs** | Custom loaders |

---

## Vector Stores

| Store | Type | Best For |
|-------|------|----------|
| **Chroma** | Local | Development, small datasets |
| **FAISS** | Local | Large local datasets |
| **Pinecone** | Cloud | Production, scale |
| **Weaviate** | Self-hosted/Cloud | Hybrid search |
| **Qdrant** | Self-hosted/Cloud | Filtering, metadata |

---

## LangSmith Observability

| Feature | Benefit |
|---------|---------|
| **Tracing** | See every LLM call, tool use |
| **Evaluation** | Test prompts systematically |
| **Datasets** | Store test cases |
| **Monitoring** | Track production performance |

**Key concept**: Enable LangSmith tracing early—debugging agents without observability is extremely difficult.

---

## Best Practices

| Practice | Why |
|----------|-----|
| Start simple | `create_agent()` covers most cases |
| Enable streaming | Better UX for long responses |
| Use LangSmith | Essential for debugging |
| Optimize chunk size | 500-1000 chars typically works |
| Cache embeddings | They're expensive to compute |
| Test retrieval separately | RAG quality depends on retrieval |

---

## LangChain vs LangGraph

| Aspect | LangChain | LangGraph |
|--------|-----------|-----------|
| **Best for** | Quick agents, RAG | Complex workflows |
| **Code to start** | <10 lines | ~30 lines |
| **State management** | Limited | Native |
| **Branching logic** | Basic | Advanced |
| **Human-in-loop** | Manual | Built-in |

**Key concept**: Use LangChain for straightforward agents and RAG. Use LangGraph when you need complex state machines, branching, or human checkpoints.

## Resources

- Docs: <https://docs.langchain.com>
- LangSmith: <https://smith.langchain.com>
- Templates: <https://github.com/langchain-ai/langchain/tree/master/templates>
