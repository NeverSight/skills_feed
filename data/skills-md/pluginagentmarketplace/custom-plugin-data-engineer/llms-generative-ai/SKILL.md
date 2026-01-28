---
name: llms-generative-ai
description: LLMs, prompt engineering, RAG systems, LangChain, and AI application development
sasmp_version: "1.3.0"
bonded_agent: 06-ml-ai-engineer
bond_type: PRIMARY_BOND
skill_version: "2.0.0"
last_updated: "2025-01"
complexity: advanced
estimated_mastery_hours: 180
prerequisites: [python-programming, machine-learning]
unlocks: [deep-learning, mlops]
---

# LLMs & Generative AI

Production-grade LLM applications with prompt engineering, RAG systems, and modern AI development patterns.

## Quick Start

```python
# Production RAG System with LangChain (2024-2025)
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_community.vectorstores import Chroma
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser

# Initialize components
llm = ChatOpenAI(model="gpt-4-turbo-preview", temperature=0)
embeddings = OpenAIEmbeddings(model="text-embedding-3-small")

# Document processing
text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=1000,
    chunk_overlap=200,
    separators=["\n\n", "\n", ". ", " ", ""]
)

documents = text_splitter.split_documents(raw_documents)

# Vector store
vectorstore = Chroma.from_documents(
    documents=documents,
    embedding=embeddings,
    persist_directory="./chroma_db"
)
retriever = vectorstore.as_retriever(
    search_type="mmr",  # Maximum Marginal Relevance
    search_kwargs={"k": 5, "fetch_k": 10}
)

# RAG chain
template = """Answer the question based only on the following context:

Context: {context}

Question: {question}

Answer thoughtfully and cite specific parts of the context."""

prompt = ChatPromptTemplate.from_template(template)

rag_chain = (
    {"context": retriever, "question": RunnablePassthrough()}
    | prompt
    | llm
    | StrOutputParser()
)

# Query
response = rag_chain.invoke("What are the key features?")
print(response)
```

## Core Concepts

### 1. Prompt Engineering Patterns

```python
from langchain_core.prompts import ChatPromptTemplate, FewShotChatMessagePromptTemplate

# System prompt design
system_prompt = """You are an expert data analyst assistant.

CAPABILITIES:
- Analyze data patterns and trends
- Generate SQL queries
- Explain statistical concepts

CONSTRAINTS:
- Only use information provided in the context
- Acknowledge uncertainty when relevant
- Format outputs in clear, structured way

OUTPUT FORMAT:
- Start with a brief summary
- Use bullet points for key findings
- Include confidence level (high/medium/low)
"""

# Few-shot prompting
examples = [
    {"input": "What's the average order value?",
     "output": "```sql\nSELECT AVG(total_amount) as avg_order_value\nFROM orders\nWHERE status = 'completed';\n```"},
    {"input": "Show top customers by revenue",
     "output": "```sql\nSELECT customer_id, SUM(total_amount) as revenue\nFROM orders\nGROUP BY customer_id\nORDER BY revenue DESC\nLIMIT 10;\n```"}
]

example_prompt = ChatPromptTemplate.from_messages([
    ("human", "{input}"),
    ("ai", "{output}")
])

few_shot_prompt = FewShotChatMessagePromptTemplate(
    example_prompt=example_prompt,
    examples=examples
)

# Chain of Thought prompting
cot_prompt = """Let's solve this step by step:

Question: {question}

Step 1: Identify the key components
Step 2: Break down the problem
Step 3: Apply relevant knowledge
Step 4: Synthesize the answer

Reasoning:"""

# Self-consistency (multiple reasoning paths)
async def self_consistent_answer(question: str, n_samples: int = 5) -> str:
    responses = await asyncio.gather(*[
        llm.ainvoke(question) for _ in range(n_samples)
    ])
    # Majority voting or aggregation
    return aggregate_responses(responses)
```

### 2. Advanced RAG Patterns

```python
from langchain.retrievers import ContextualCompressionRetriever
from langchain.retrievers.document_compressors import LLMChainExtractor
from langchain_community.retrievers import BM25Retriever
from langchain.retrievers import EnsembleRetriever

# Hybrid search (dense + sparse)
bm25_retriever = BM25Retriever.from_documents(documents)
bm25_retriever.k = 5

chroma_retriever = vectorstore.as_retriever(search_kwargs={"k": 5})

ensemble_retriever = EnsembleRetriever(
    retrievers=[bm25_retriever, chroma_retriever],
    weights=[0.4, 0.6]
)

# Contextual compression
compressor = LLMChainExtractor.from_llm(llm)
compression_retriever = ContextualCompressionRetriever(
    base_compressor=compressor,
    base_retriever=ensemble_retriever
)

# Parent document retriever (for better context)
from langchain.retrievers import ParentDocumentRetriever
from langchain.storage import InMemoryStore

parent_splitter = RecursiveCharacterTextSplitter(chunk_size=2000)
child_splitter = RecursiveCharacterTextSplitter(chunk_size=400)

store = InMemoryStore()
parent_retriever = ParentDocumentRetriever(
    vectorstore=vectorstore,
    docstore=store,
    child_splitter=child_splitter,
    parent_splitter=parent_splitter
)

# Self-querying retriever
from langchain.retrievers.self_query.base import SelfQueryRetriever
from langchain.chains.query_constructor.base import AttributeInfo

metadata_field_info = [
    AttributeInfo(name="source", description="Document source", type="string"),
    AttributeInfo(name="date", description="Creation date", type="date"),
    AttributeInfo(name="category", description="Document category", type="string"),
]

self_query_retriever = SelfQueryRetriever.from_llm(
    llm=llm,
    vectorstore=vectorstore,
    document_contents="Technical documentation",
    metadata_field_info=metadata_field_info
)
```

### 3. Agents and Tool Use

```python
from langchain.agents import create_openai_functions_agent, AgentExecutor
from langchain.tools import Tool, StructuredTool
from langchain_core.pydantic_v1 import BaseModel, Field
from typing import Optional

# Define tools with Pydantic schemas
class SQLQueryInput(BaseModel):
    query: str = Field(description="SQL query to execute")
    limit: Optional[int] = Field(default=100, description="Max rows to return")

def execute_sql(query: str, limit: int = 100) -> str:
    """Execute SQL query against the database."""
    # Validate query (prevent injection)
    if any(kw in query.upper() for kw in ["DROP", "DELETE", "UPDATE", "INSERT"]):
        return "Error: Only SELECT queries allowed"

    result = db.execute(f"{query} LIMIT {limit}")
    return result.to_markdown()

sql_tool = StructuredTool.from_function(
    func=execute_sql,
    name="sql_executor",
    description="Execute SQL queries against the data warehouse",
    args_schema=SQLQueryInput
)

# Calculator tool
def calculate(expression: str) -> str:
    """Evaluate mathematical expression."""
    try:
        # Safe eval with limited scope
        allowed_names = {"abs": abs, "round": round, "sum": sum}
        return str(eval(expression, {"__builtins__": {}}, allowed_names))
    except Exception as e:
        return f"Error: {e}"

calc_tool = Tool.from_function(
    func=calculate,
    name="calculator",
    description="Evaluate mathematical expressions"
)

# Create agent
tools = [sql_tool, calc_tool]
agent = create_openai_functions_agent(llm, tools, prompt)
agent_executor = AgentExecutor(
    agent=agent,
    tools=tools,
    verbose=True,
    max_iterations=5,
    early_stopping_method="generate"
)

result = agent_executor.invoke({"input": "What's the total revenue for Q4 2024?"})
```

### 4. Structured Output

```python
from langchain_core.pydantic_v1 import BaseModel, Field
from typing import List, Optional
from langchain.output_parsers import PydanticOutputParser

# Define output schema
class DataInsight(BaseModel):
    title: str = Field(description="Brief title of the insight")
    description: str = Field(description="Detailed explanation")
    confidence: float = Field(description="Confidence score 0-1")
    data_points: List[str] = Field(description="Supporting data points")
    recommendations: Optional[List[str]] = Field(description="Action items")

class AnalysisReport(BaseModel):
    summary: str = Field(description="Executive summary")
    insights: List[DataInsight] = Field(description="Key insights found")
    methodology: str = Field(description="Analysis approach used")

# Parser
parser = PydanticOutputParser(pydantic_object=AnalysisReport)

prompt = ChatPromptTemplate.from_messages([
    ("system", "Analyze the data and provide structured insights."),
    ("human", "{input}\n\n{format_instructions}")
]).partial(format_instructions=parser.get_format_instructions())

chain = prompt | llm | parser

report: AnalysisReport = chain.invoke({"input": "Analyze Q4 sales trends"})
print(report.summary)
for insight in report.insights:
    print(f"- {insight.title}: {insight.confidence:.0%} confidence")
```

### 5. Evaluation and Monitoring

```python
from langchain.evaluation import load_evaluator
from langsmith import Client
import openai

# LangSmith for tracing
client = Client()

# Create evaluation dataset
examples = [
    {"input": "What is RAG?", "output": "Retrieval Augmented Generation..."},
    {"input": "How does chunking work?", "output": "Chunking splits documents..."},
]
dataset = client.create_dataset("rag-evaluation")
for ex in examples:
    client.create_example(inputs={"question": ex["input"]},
                          outputs={"answer": ex["output"]},
                          dataset_id=dataset.id)

# Evaluators
faithfulness_evaluator = load_evaluator("labeled_criteria", criteria="correctness")
relevance_evaluator = load_evaluator("embedding_distance")

# Custom evaluator for RAG
def evaluate_rag_response(question: str, context: str, response: str) -> dict:
    """Evaluate RAG response quality."""

    # Faithfulness: Is response grounded in context?
    faithfulness_prompt = f"""
    Context: {context}
    Response: {response}

    Is the response fully supported by the context?
    Score 1-5 and explain.
    """

    # Relevance: Does response answer the question?
    relevance_prompt = f"""
    Question: {question}
    Response: {response}

    Does the response adequately answer the question?
    Score 1-5 and explain.
    """

    # Get scores
    faithfulness_score = llm.invoke(faithfulness_prompt)
    relevance_score = llm.invoke(relevance_prompt)

    return {
        "faithfulness": parse_score(faithfulness_score),
        "relevance": parse_score(relevance_score)
    }

# Production monitoring
from prometheus_client import Counter, Histogram

llm_requests = Counter("llm_requests_total", "Total LLM requests", ["model", "status"])
llm_latency = Histogram("llm_latency_seconds", "LLM request latency")
token_usage = Counter("llm_tokens_total", "Total tokens used", ["type"])

@llm_latency.time()
def monitored_llm_call(prompt: str) -> str:
    try:
        response = llm.invoke(prompt)
        llm_requests.labels(model="gpt-4", status="success").inc()
        token_usage.labels(type="input").inc(count_tokens(prompt))
        token_usage.labels(type="output").inc(count_tokens(response))
        return response
    except Exception as e:
        llm_requests.labels(model="gpt-4", status="error").inc()
        raise
```

## Tools & Technologies

| Tool | Purpose | Version (2025) |
|------|---------|----------------|
| **LangChain** | LLM application framework | 0.2+ |
| **LlamaIndex** | Data framework for LLMs | 0.10+ |
| **OpenAI API** | GPT-4, embeddings | Latest |
| **Anthropic API** | Claude models | Latest |
| **Chroma** | Vector database | 0.4+ |
| **Pinecone** | Managed vector DB | Latest |
| **LangSmith** | LLM observability | Latest |
| **Ollama** | Local LLM running | 0.1+ |
| **vLLM** | High-perf LLM serving | 0.3+ |

## Learning Path

### Phase 1: Foundations (Weeks 1-3)
```
Week 1: LLM concepts, tokenization, prompting basics
Week 2: OpenAI/Anthropic APIs, prompt engineering
Week 3: LangChain basics, chains, output parsers
```

### Phase 2: RAG Systems (Weeks 4-7)
```
Week 4: Embeddings, vector databases
Week 5: Document processing, chunking strategies
Week 6: Retrieval strategies (hybrid, reranking)
Week 7: Advanced RAG patterns
```

### Phase 3: Agents (Weeks 8-10)
```
Week 8: Tool calling, function calling
Week 9: Agent architectures, planning
Week 10: Multi-agent systems
```

### Phase 4: Production (Weeks 11-14)
```
Week 11: Evaluation frameworks
Week 12: Guardrails, safety
Week 13: Deployment, scaling
Week 14: Monitoring, optimization
```

## Troubleshooting Guide

### Common Failure Modes

| Issue | Symptoms | Root Cause | Fix |
|-------|----------|------------|-----|
| **Hallucination** | Incorrect facts | No grounding | Better RAG, fact-checking |
| **Context Overflow** | Truncated response | Too much context | Summarize, filter |
| **Poor Retrieval** | Irrelevant chunks | Bad embeddings/chunking | Tune chunk size, reranking |
| **Slow Response** | High latency | Large context, no cache | Streaming, caching |
| **Rate Limits** | 429 errors | Too many requests | Backoff, batch requests |

### Debug Checklist

```python
# 1. Check retrieval quality
retrieved_docs = retriever.get_relevant_documents("test query")
for doc in retrieved_docs:
    print(f"Score: {doc.metadata.get('score')}")
    print(f"Content: {doc.page_content[:200]}...")

# 2. Validate prompt
print(prompt.format(context="test", question="test"))

# 3. Token counting
import tiktoken
enc = tiktoken.encoding_for_model("gpt-4")
tokens = len(enc.encode(full_prompt))
print(f"Token count: {tokens}")

# 4. Test LLM directly
response = llm.invoke("Simple test prompt")
print(response)

# 5. Check embeddings
embedding = embeddings.embed_query("test")
print(f"Embedding dim: {len(embedding)}")
```

## Unit Test Template

```python
import pytest
from unittest.mock import Mock, patch
from your_rag_system import RAGPipeline, DocumentProcessor

class TestRAGPipeline:

    @pytest.fixture
    def mock_llm(self):
        llm = Mock()
        llm.invoke.return_value = "Mocked response"
        return llm

    @pytest.fixture
    def rag_pipeline(self, mock_llm):
        return RAGPipeline(llm=mock_llm)

    def test_retrieves_relevant_documents(self, rag_pipeline):
        query = "What is machine learning?"
        docs = rag_pipeline.retrieve(query)

        assert len(docs) > 0
        assert all("machine learning" in doc.page_content.lower()
                   for doc in docs[:3])

    def test_generates_grounded_response(self, rag_pipeline, mock_llm):
        response = rag_pipeline.query("Test question")

        mock_llm.invoke.assert_called_once()
        assert response is not None

    def test_handles_empty_retrieval(self, rag_pipeline):
        with patch.object(rag_pipeline.retriever, 'get_relevant_documents',
                         return_value=[]):
            response = rag_pipeline.query("Obscure question")
            assert "no information" in response.lower()


class TestDocumentProcessor:

    def test_chunks_documents_correctly(self):
        processor = DocumentProcessor(chunk_size=100, chunk_overlap=20)
        text = "A" * 250  # 250 character document

        chunks = processor.split(text)

        assert len(chunks) >= 2
        assert all(len(c) <= 100 for c in chunks)

    def test_preserves_metadata(self):
        processor = DocumentProcessor()
        doc = Document(page_content="Test", metadata={"source": "test.pdf"})

        chunks = processor.split_documents([doc])

        assert all(c.metadata["source"] == "test.pdf" for c in chunks)
```

## Best Practices

### Prompt Engineering
```python
# ✅ DO: Be specific and structured
prompt = """Task: Summarize the document.
Format: 3 bullet points
Constraints: Max 50 words per point
Tone: Professional"""

# ✅ DO: Include examples
# ✅ DO: Set clear output format
# ✅ DO: Handle edge cases in prompt

# ❌ DON'T: Vague prompts
# ❌ DON'T: Assume LLM knows context
# ❌ DON'T: Trust LLM output without validation
```

### RAG Systems
```python
# ✅ DO: Tune chunk size for your domain
# ✅ DO: Use hybrid retrieval
# ✅ DO: Implement reranking
# ✅ DO: Add metadata filtering

# ❌ DON'T: One-size-fits-all chunking
# ❌ DON'T: Skip evaluation
# ❌ DON'T: Ignore retrieval quality
```

## Resources

### Official Documentation
- [LangChain Docs](https://python.langchain.com/)
- [OpenAI Cookbook](https://cookbook.openai.com/)
- [Anthropic Docs](https://docs.anthropic.com/)

### Courses
- [DeepLearning.AI LangChain](https://www.deeplearning.ai/)
- [LlamaIndex Course](https://docs.llamaindex.ai/en/stable/)

### Research
- [RAG Survey Paper](https://arxiv.org/abs/2312.10997)
- [Prompt Engineering Guide](https://www.promptingguide.ai/)

## Next Skills

After mastering LLMs & Generative AI:
- → `deep-learning` - Understand transformer internals
- → `mlops` - Deploy LLM applications at scale
- → `big-data` - Process training data

---

**Skill Certification Checklist:**
- [ ] Can build production RAG systems
- [ ] Can implement effective prompt engineering
- [ ] Can create tool-using agents
- [ ] Can evaluate and monitor LLM applications
- [ ] Can optimize for latency and cost
