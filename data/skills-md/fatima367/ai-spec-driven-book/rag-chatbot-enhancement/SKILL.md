---
name: RAG Chatbot Enhancement
description: Improves the RAG (Retrieval-Augmented Generation) chatbot for the Physical AI & Humanoid Robotics textbook with strict grounding, citation requirements, and performance optimization.
when to use: Use this skill when you need to enhance the chatbot's ability to answer questions based strictly on textbook content, provide citations, or improve response quality and performance.
---

**Instructions:**
You are an expert in RAG systems and educational chatbots. Your task is to enhance the chatbot's ability to answer questions based strictly on the Physical AI & Humanoid Robotics textbook content, with proper citations and without hallucination.

**Workflow:**
1. Ensure strict grounding to indexed textbook content only
2. Implement citation system that links to specific chapters/sections
3. Configure failure mode for out-of-scope queries
4. Optimize response time to meet <500ms target
5. Implement quality checks to prevent hallucination

**Technical Requirements:**
- Use only indexed textbook content (no web search)
- Include direct citations to source material
- Return polite refusal for out-of-scope queries
- Target <500ms response time for 95% of requests
- Use Qdrant Cloud Free Tier for vector storage
- Implement proper error handling and fallbacks

**Output Format:**
Chatbot responses should include the answer, source citations, and appropriate error handling.

**Example Use Case:**
User: "How does the chatbot handle queries outside the textbook content?"

**Expected Output:**
```python
def handle_query(query: str) -> dict:
    # Search vector database for relevant textbook content
    results = qdrant_service.search(query)

    if not results:
        return {
            "answer": "I can only answer questions based on the content of the textbook. The requested information is not available in the indexed textbook materials.",
            "citations": [],
            "confidence": 0.0
        }

    # Verify content relevance and extract answer
    answer = generate_answer_from_context(results, query)

    # Format citations
    citations = [
        {
            "chapter": result.chapter,
            "section": result.section,
            "url": f"/docs/{result.chapter_slug}#{result.section_slug}"
        }
        for result in results
    ]

    return {
        "answer": answer,
        "citations": citations,
        "confidence": calculate_confidence(results)
    }
```