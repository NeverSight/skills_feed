---
name: ai
description: Use this skill when building AI features, integrating LLMs, implementing RAG, working with embeddings, deploying ML models, or doing data science. Activates on mentions of OpenAI, Anthropic, Claude, GPT, LLM, RAG, embeddings, vector database, Pinecone, Qdrant, LangChain, LlamaIndex, DSPy, MLflow, fine-tuning, LoRA, QLoRA, model deployment, ML pipeline, feature engineering, or machine learning.
---

# AI/ML Engineering

Build production AI systems with modern patterns and tools.

## Quick Reference

### The 2026 AI Stack

| Layer               | Tool              | Purpose                          |
| ------------------- | ----------------- | -------------------------------- |
| Prompting           | DSPy              | Programmatic prompt optimization |
| Orchestration       | LangGraph         | Stateful multi-agent workflows   |
| RAG                 | LlamaIndex        | Document ingestion and retrieval |
| Vectors             | Qdrant / Pinecone | Embedding storage and search     |
| Evaluation          | RAGAS             | RAG quality metrics              |
| Experiment Tracking | MLflow / W&B      | Logging, versioning, comparison  |
| Serving             | BentoML / vLLM    | Model deployment                 |
| Protocol            | MCP               | Tool and context integration     |

### DSPy: Programmatic Prompting

**Manual prompts are dead.** DSPy treats prompts as optimizable code:

```python
import dspy

class QA(dspy.Signature):
    """Answer questions with short factoid answers."""
    question = dspy.InputField()
    answer = dspy.OutputField(desc="1-5 words")

# Create module
qa = dspy.Predict(QA)

# Use it
result = qa(question="What is the capital of France?")
print(result.answer)  # "Paris"
```

**Optimize with real data:**

```python
from dspy.teleprompt import BootstrapFewShot

optimizer = BootstrapFewShot(metric=exact_match)
optimized_qa = optimizer.compile(qa, trainset=train_data)
```

### RAG Architecture (Production)

```
Query → Rewrite → Hybrid Retrieval → Rerank → Generate → Cite
         │              │                │
         v              v                v
    Query expansion  Dense + BM25   Cross-encoder
```

**LlamaIndex + LangGraph Pattern:**

```python
from llama_index.core import VectorStoreIndex
from langgraph.graph import StateGraph

# Data layer (LlamaIndex)
index = VectorStoreIndex.from_documents(docs)
query_engine = index.as_query_engine()

# Control layer (LangGraph)
def retrieve(state):
    response = query_engine.query(state["question"])
    return {"context": response.response, "sources": response.source_nodes}

graph = StateGraph(State)
graph.add_node("retrieve", retrieve)
graph.add_node("generate", generate_answer)
graph.add_edge("retrieve", "generate")
```

### MCP Integration

Model Context Protocol is the standard for tool integration:

```python
from mcp import Server, Tool

server = Server("my-tools")

@server.tool()
async def search_docs(query: str) -> str:
    """Search the knowledge base."""
    results = await vector_store.search(query)
    return format_results(results)
```

### Embeddings (2026)

| Model                  | Dimensions | Best For         |
| ---------------------- | ---------- | ---------------- |
| text-embedding-3-large | 3072       | General purpose  |
| BGE-M3                 | 1024       | Multilingual RAG |
| Qwen3-Embedding        | Flexible   | Custom domains   |

### Fine-Tuning with LoRA/QLoRA

```python
from peft import LoraConfig, get_peft_model

config = LoraConfig(
    r=16,
    lora_alpha=32,
    target_modules=["q_proj", "v_proj"],
    lora_dropout=0.05,
)

model = get_peft_model(base_model, config)
# Train on ~24GB VRAM (QLoRA on RTX 4090)
```

### MLOps Pipeline

```yaml
# MLflow tracking
mlflow.set_experiment("rag-v2")

with mlflow.start_run():
    mlflow.log_params({"chunk_size": 512, "model": "gpt-4"})
    mlflow.log_metrics({"faithfulness": 0.92, "relevance": 0.88})
    mlflow.log_artifact("prompts/qa.txt")
```

### Evaluation with RAGAS

```python
from ragas import evaluate
from ragas.metrics import faithfulness, answer_relevancy, context_precision

results = evaluate(
    dataset,
    metrics=[faithfulness, answer_relevancy, context_precision],
)
print(results)  # {'faithfulness': 0.92, 'answer_relevancy': 0.88, ...}
```

### Vector Database Selection

| DB       | Best For               | Pricing             |
| -------- | ---------------------- | ------------------- |
| Qdrant   | Self-hosted, filtering | 1GB free forever    |
| Pinecone | Managed, zero-ops      | Free tier available |
| Weaviate | Knowledge graphs       | 14-day trial        |
| Milvus   | Billion-scale          | Self-hosted         |

## Agents

- **ai-engineer** - LLM integration, RAG, MCP, production AI
- **mlops-engineer** - Model deployment, monitoring, pipelines
- **data-scientist** - Analysis, modeling, experimentation
- **ml-researcher** - Cutting-edge architectures, paper implementation
- **cv-engineer** - Computer vision, VLMs, image processing

## Deep Dives

- [references/dspy-guide.md](references/dspy-guide.md)
- [references/rag-patterns.md](references/rag-patterns.md)
- [references/mcp-integration.md](references/mcp-integration.md)
- [references/fine-tuning.md](references/fine-tuning.md)
- [references/evaluation.md](references/evaluation.md)

## Examples

- [examples/rag-pipeline/](examples/rag-pipeline/)
- [examples/mcp-server/](examples/mcp-server/)
- [examples/dspy-optimization/](examples/dspy-optimization/)
