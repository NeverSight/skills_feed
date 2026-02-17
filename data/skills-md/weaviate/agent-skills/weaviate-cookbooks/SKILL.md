---
name: weaviate-cookbooks
description: Use this skill when the user wants to build AI applications with Weaviate. It contains a high-level index of architectural patterns, 'one-shot' blueprints, and best practices for common use cases. Currently, it includes references for building a Query Agent Chatbot, Data Explorer, Multimodal PDF RAG (Document Search), Basic RAG, Advanced RAG, Basic Agent, Agentic RAG, and optional guidance on how to build a frontend for each of them.
---

# Weaviate Cookbooks

## Overview

This skill provides an index of implementation guides and foundational requirements for building Weaviate-powered AI applications. Use the references to quickly scaffold full-stack applications with best practices for connection management, environment setup, and application architecture.

### Weaviate Cloud Instance

If the user does not have an instance yet, direct them to the cloud console to register and create a free sandbox. Create a Weaviate instance via [Weaviate Cloud](https://console.weaviate.cloud/).

## Environment Requirements

Before generating backend code that initializes a Weaviate client:

1. Read [Environment Requirements](references/environment-requirements.md) for the canonical env var and header mapping.
2. Use provider-specific env var names only (for example, `OPENAI_API_KEY`).
3. Do not introduce generic placeholders like `INFERENCE_API_KEY` or `EXTERNAL_PROVIDER_API_KEY`.

## Cookbook Index

- [Query Agent Chatbot](references/query_agent_chatbot.md): Build a full-stack chatbot using Weaviate Query Agent with streaming and chat history support.
- [Data Explorer](references/data_explorer.md): Build a full-stack data explorer app including sorting, keyword search and tabular view of weaviate data.
- [Multimodal RAG: Building Document Search](references/pdf_multimodal_rag.md): Build a multimodal Retrieval-Augmented Generation (RAG) system using Weaviate Embeddings (ModernVBERT/colmodernvbert) and Ollama with Qwen3-VL for generation.
- [Basic RAG](references/basic_rag.md): Implement basic retrieval and generation with Weaviate. Useful for most forms of data retrieval from a Weaviate collection.
- [Advanced RAG](references/advanced_rag.md): Improve on basic RAG by adding extra features such as re-ranking, query decomposition, query re-writing, LLM filter selection.
- [Basic Agent](references/basic_agent.md): Build a tool-calling AI agent with structured outputs using DSPy. Covers AgentResponse signatures, RouterAgent, tool design, and sequential multi-step loops.
- [Agentic RAG](references/agentic_rag.md): Build RAG-powered AI agents with Weaviate. Covers naive RAG tools, hierarchical RAG with LLM-created filters, vector DB memory, Weaviate Query Agent, and Elysia integration.

## Interface (Optional)

Use this when the user explicitly asks for a frontend for their Weaviate backend.

- [Frontend Interface](references/frontend_interface.md): Build a Next.js frontend to interact with the Weaviate backend.
