---
name: pageindex-rag
description: Build reasoning-based RAG systems using PageIndex architecture. Replaces vector databases with hierarchical table-of-contents indices and LLM-driven navigation. Use when (1) implementing RAG for long structured documents (financial reports, legal contracts, technical manuals), (2) improving existing vector-based RAG systems with poor accuracy on structured content, (3) designing document indexing strategies with semantic coherence, (4) explaining PageIndex concepts including reasoning-based retrieval, hierarchical navigation, and cross-reference following, or (5) handling documents with internal references and multi-turn conversations. Focuses on technical architecture, core research insights, and practical implementation patterns rather than using the PageIndex package directly.
---

# PageIndex RAG Architecture

PageIndex replaces vector-based similarity search with LLM-driven hierarchical navigation, achieving 98.7% accuracy on financial document benchmarks by reasoning through document structure instead of matching embeddings.

## Core Innovation: Why Vector RAG Fails

**Query-Knowledge Mismatch**: Vector similarity measures surface semantics, not task relevance. "What are debt trends?" matches "trends" mentions, not actual trend analysis.

**Hard Chunking**: Fixed 512-1000 token chunks fragment mid-sentence, breaking contextual continuity. Financial statements split across chunks lose asset-liability relationships.

**Context Window Deterioration**: Retrieving 10-20 chunks creates needle-in-haystack problems where relevant info gets buried.

**Cross-Reference Blindness**: Cannot follow "see Appendix G" or "Section 3.2" references without manual preprocessing.

## PageIndex Solution

Replace vector databases with **hierarchical tree indices** stored as JSON:

```json
{
  "node_id": "section_2_1",
  "name": "Financial Assets",
  "description": "Current and long-term financial assets including marketable securities",
  "start_index": 12,
  "end_index": 15,
  "nodes": [...]
}
```

**Iterative reasoning loop**:
1. Read ToC → Reason about which sections likely contain relevant info
2. Select section → Navigate tree based on descriptions
3. Extract content → Retrieve full semantic units (pages 12-15)
4. Evaluate sufficiency → "Did I find what I need?"
5. Branch → Answer, follow cross-reference, or refine search

## When to Use PageIndex vs Vector RAG

**Use PageIndex for**:
- Long structured documents (10-K reports, legal contracts, technical manuals)
- Domain-specific precision requiring reasoning
- Documents with cross-references ("see Appendix G")
- Multi-turn conversations building context

**Use Vector RAG for**:
- Unstructured heterogeneous content (social media, reviews)
- Similarity-based tasks ("find documents like this")
- Real-time streaming data with continuous ingestion
- High query volume with cost constraints (vectors = O(1), PageIndex = multiple LLM calls)

See [comparison-patterns.md](references/comparison-patterns.md) for detailed trade-offs and hybrid approaches.

## Implementation Workflow

### 1. Build Hierarchical Index

**Extract document structure**:

```python
def extract_toc_from_pdf(pdf_path: str, toc_pages: int = 20) -> List[dict]:
    """
    Parse table of contents from first N pages
    Returns: [{title, page, level}, ...]
    """
    # Detect ToC patterns:
    # - Lines with page numbers: "Section 2.1 ..... 42"
    # - Indentation indicating hierarchy
    # - Keywords: Chapter, Section, Appendix
```

**Construct tree**:

```python
def build_tree(toc_entries: List[dict]) -> TreeNode:
    """
    Convert flat ToC to nested tree structure
    Assigns node_ids, page ranges, hierarchical relationships
    """
```

**Generate descriptions** (enables reasoning):

```python
def generate_descriptions(node: TreeNode, doc_path: str):
    """
    LLM creates semantic descriptions per section:
    - Key topics covered
    - Type of information (data, analysis, methodology)
    - Relevant domain concepts
    """
```

**For documents without explicit ToC**: Use LLM to infer structure from content patterns.

See [implementation-guide.md](references/implementation-guide.md) for complete indexing pipeline code.

### 2. Implement Reasoning-Based Retrieval

**Node selection**:

```python
def select_relevant_nodes(
    query: str,
    tree: TreeNode,
    conversation_history: List[str] = None
) -> List[TreeNode]:
    """
    LLM reasons over tree structure:
    1. What type of information does query require?
    2. Which sections' descriptions indicate relevance?
    3. Consider conversation history (prior focus areas)

    Returns 1-3 most promising nodes
    """
```

**Content extraction**:

```python
def extract_content_range(doc_path: str, start_page: int, end_page: int) -> str:
    """
    Retrieve exact page ranges (preserves semantic boundaries)
    Each node = 5-15 pages typically
    """
```

**Sufficiency evaluation**:

```python
def evaluate_sufficiency(query: str, collected_context: str) -> dict:
    """
    LLM meta-reasoning:
    - Does context contain data needed to answer?
    - Are there gaps requiring more information?
    - Does text reference another section?

    Returns: {status: "sufficient" | "insufficient" | "follow_reference"}
    """
```

**Cross-reference following**:

```python
def follow_cross_reference(context: str, tree: TreeNode) -> TreeNode:
    """
    Detect patterns: "see Appendix G", "discussed in Section 2.1"
    Navigate tree to referenced node
    """
```

**Complete loop**:

```python
def retrieve(query: str, tree: TreeNode, doc_path: str, max_iterations: int = 5):
    context = ""
    for _ in range(max_iterations):
        nodes = select_relevant_nodes(query, tree)
        context += extract_content(nodes)

        eval = evaluate_sufficiency(query, context)
        if eval['status'] == 'sufficient':
            return context
        elif eval['status'] == 'follow_reference':
            ref_node = follow_cross_reference(context, tree)
            context += extract_content([ref_node])

    return context
```

See [implementation-guide.md](references/implementation-guide.md) for complete retrieval code with error handling, caching, and optimization strategies.

## Key Configuration Parameters

```python
CONFIG = {
    # Indexing
    'max_pages_per_node': 10,      # 5-15 optimal (too small = overhead, too large = reverts to chunking)
    'max_tokens_per_node': 20000,  # Hard limit on node size
    'toc_check_pages': 20,         # Pages to scan for ToC

    # Retrieval
    'max_iterations': 5,            # Prevent infinite loops
    'max_nodes_per_iteration': 3,   # Sections to check simultaneously

    # LLM
    'model': 'gpt-4o-2024-11-20',  # Or claude-sonnet-4-5
    'temperature': 0.1,             # Low for consistent reasoning
}
```

**Tree design patterns**:
- **Depth**: Financial docs = 3-4 levels, research papers = 2-3, technical manuals = 4-5
- **Granularity**: 5-15 pages per node (balanced coherence/efficiency)
- **Description quality**: Must enable reasoning ("Balance sheet with current/long-term asset breakdown" not "Section 2.1")

## Architecture Deep Dive

For comprehensive technical details:

- **[architecture.md](references/architecture.md)**: Problem analysis, PageIndex solution, implementation stages, performance characteristics, tree structure design patterns
- **[implementation-guide.md](references/implementation-guide.md)**: Complete code for indexing pipeline (ToC extraction, tree building, description generation), retrieval pipeline (node selection, content extraction, sufficiency evaluation, reference following), configuration tuning, integration patterns (LangChain, FastAPI)
- **[comparison-patterns.md](references/comparison-patterns.md)**: Vector RAG vs PageIndex decision matrix, architectural trade-offs table, hybrid approaches (combining both, two-stage retrieval), migration strategies, common pitfalls and solutions, performance optimization (caching, parallel evaluation, early stopping)

## Common Pitfalls

**Over-fragmenting**: Setting `max_pages_per_node=1` creates excessive navigation. Use 5-15 pages.

**Poor descriptions**: Vague descriptions ("Section 2.1") don't enable reasoning. Use LLM to generate semantic summaries with domain keywords.

**Ignoring ToC absence**: Many PDFs lack explicit ToC. Detect this and use LLM structure inference.

**Independent query processing**: Pass conversation history to node selection for context refinement.

See [comparison-patterns.md](references/comparison-patterns.md) for detailed pitfall analysis with solutions.

## Integration Examples

**LangChain**:

```python
from langchain.schema import BaseRetriever, Document

class PageIndexRetriever(BaseRetriever):
    tree: TreeNode
    document_path: str

    def get_relevant_documents(self, query: str) -> List[Document]:
        context = retrieve(query, self.tree, self.document_path)
        return [Document(page_content=context)]
```

**Hybrid with vector search**:

```python
def hybrid_retrieve(query: str, doc_type: str):
    if doc_type == "structured":
        # Financial reports, contracts → PageIndex
        return pageindex_retrieve(query)
    else:
        # Unstructured content → vector search
        return vector_retrieve(query)
```

See [implementation-guide.md](references/implementation-guide.md) for FastAPI integration and [comparison-patterns.md](references/comparison-patterns.md) for hybrid architecture patterns.

## Performance Characteristics

- **Accuracy**: 98.7% on FinanceBench (vs 60-80% for vector RAG on structured docs)
- **Latency**: Higher per-query (3-5 LLM calls vs 1-2), but no embedding computation
- **Cost**: Higher LLM API cost, zero vector DB hosting costs
- **Scalability**: Works for documents up to ~1000 pages (tree = 10-50KB JSON)

See [architecture.md](references/architecture.md) for detailed performance analysis.
