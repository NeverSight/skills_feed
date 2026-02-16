---
name: ai-ml-integration
description: AI/ML APIs, LLM integration, and intelligent application patterns
domain: development-stacks
version: 1.0.0
tags: [openai, anthropic, langchain, embeddings, rag, vector-db]
triggers:
  keywords:
    primary: [ai, ml, llm, openai, anthropic, langchain, embedding, rag]
    secondary: [vector database, pinecone, chromadb, prompt engineering, agent, gpt]
  context_boost: [intelligent, chatbot, nlp, machine learning]
  context_penalty: [frontend, css, ui, database]
  priority: high
---

# AI/ML Integration

## Overview

Integrating AI and machine learning capabilities into applications, including LLM APIs, embeddings, and RAG patterns.

---

## LLM Integration

### OpenAI API

```typescript
import OpenAI from 'openai';

const openai = new OpenAI({
  apiKey: process.env.OPENAI_API_KEY,
});

// Chat completion
async function chat(messages: Array<{ role: string; content: string }>) {
  const response = await openai.chat.completions.create({
    model: 'gpt-4o',
    messages,
    temperature: 0.7,
    max_tokens: 1000,
  });

  return response.choices[0].message.content;
}

// Streaming response
async function* streamChat(prompt: string) {
  const stream = await openai.chat.completions.create({
    model: 'gpt-4o',
    messages: [{ role: 'user', content: prompt }],
    stream: true,
  });

  for await (const chunk of stream) {
    const content = chunk.choices[0]?.delta?.content;
    if (content) {
      yield content;
    }
  }
}

// Function calling
async function chatWithTools(message: string) {
  const tools = [
    {
      type: 'function' as const,
      function: {
        name: 'get_weather',
        description: 'Get current weather for a location',
        parameters: {
          type: 'object',
          properties: {
            location: { type: 'string', description: 'City name' },
            unit: { type: 'string', enum: ['celsius', 'fahrenheit'] },
          },
          required: ['location'],
        },
      },
    },
  ];

  const response = await openai.chat.completions.create({
    model: 'gpt-4o',
    messages: [{ role: 'user', content: message }],
    tools,
    tool_choice: 'auto',
  });

  const toolCall = response.choices[0].message.tool_calls?.[0];
  if (toolCall) {
    const args = JSON.parse(toolCall.function.arguments);
    // Execute the function
    const result = await executeFunction(toolCall.function.name, args);

    // Continue conversation with function result
    return openai.chat.completions.create({
      model: 'gpt-4o',
      messages: [
        { role: 'user', content: message },
        response.choices[0].message,
        {
          role: 'tool',
          tool_call_id: toolCall.id,
          content: JSON.stringify(result),
        },
      ],
    });
  }

  return response;
}
```

### Anthropic Claude

```typescript
import Anthropic from '@anthropic-ai/sdk';

const anthropic = new Anthropic({
  apiKey: process.env.ANTHROPIC_API_KEY,
});

// Basic message
async function chat(prompt: string) {
  const message = await anthropic.messages.create({
    model: 'claude-sonnet-4-20250514',
    max_tokens: 1024,
    messages: [{ role: 'user', content: prompt }],
  });

  return message.content[0].type === 'text' ? message.content[0].text : '';
}

// With system prompt
async function chatWithSystem(system: string, prompt: string) {
  const message = await anthropic.messages.create({
    model: 'claude-sonnet-4-20250514',
    max_tokens: 1024,
    system,
    messages: [{ role: 'user', content: prompt }],
  });

  return message.content[0];
}

// Streaming
async function* streamChat(prompt: string) {
  const stream = anthropic.messages.stream({
    model: 'claude-sonnet-4-20250514',
    max_tokens: 1024,
    messages: [{ role: 'user', content: prompt }],
  });

  for await (const event of stream) {
    if (event.type === 'content_block_delta' && event.delta.type === 'text_delta') {
      yield event.delta.text;
    }
  }
}

// Tool use
async function chatWithTools(prompt: string) {
  const response = await anthropic.messages.create({
    model: 'claude-sonnet-4-20250514',
    max_tokens: 1024,
    tools: [
      {
        name: 'search_database',
        description: 'Search the database for relevant information',
        input_schema: {
          type: 'object',
          properties: {
            query: { type: 'string', description: 'Search query' },
            limit: { type: 'number', description: 'Max results' },
          },
          required: ['query'],
        },
      },
    ],
    messages: [{ role: 'user', content: prompt }],
  });

  // Handle tool use blocks
  for (const block of response.content) {
    if (block.type === 'tool_use') {
      const result = await executeSearch(block.input);
      // Continue with tool result...
    }
  }
}
```

---

## Embeddings

### Text Embeddings

```typescript
import OpenAI from 'openai';

const openai = new OpenAI();

// Generate embeddings
async function getEmbedding(text: string): Promise<number[]> {
  const response = await openai.embeddings.create({
    model: 'text-embedding-3-small',
    input: text,
  });

  return response.data[0].embedding;
}

// Batch embeddings
async function getEmbeddings(texts: string[]): Promise<number[][]> {
  const response = await openai.embeddings.create({
    model: 'text-embedding-3-small',
    input: texts,
  });

  return response.data.map(d => d.embedding);
}

// Cosine similarity
function cosineSimilarity(a: number[], b: number[]): number {
  let dotProduct = 0;
  let normA = 0;
  let normB = 0;

  for (let i = 0; i < a.length; i++) {
    dotProduct += a[i] * b[i];
    normA += a[i] * a[i];
    normB += b[i] * b[i];
  }

  return dotProduct / (Math.sqrt(normA) * Math.sqrt(normB));
}

// Find similar items
async function findSimilar(query: string, items: Array<{ text: string; embedding: number[] }>, topK = 5) {
  const queryEmbedding = await getEmbedding(query);

  const scored = items.map(item => ({
    ...item,
    score: cosineSimilarity(queryEmbedding, item.embedding),
  }));

  return scored
    .sort((a, b) => b.score - a.score)
    .slice(0, topK);
}
```

### Vector Database (Pinecone)

```typescript
import { Pinecone } from '@pinecone-database/pinecone';

const pinecone = new Pinecone({
  apiKey: process.env.PINECONE_API_KEY,
});

const index = pinecone.index('my-index');

// Upsert vectors
async function upsertDocuments(documents: Document[]) {
  const vectors = await Promise.all(
    documents.map(async (doc) => ({
      id: doc.id,
      values: await getEmbedding(doc.content),
      metadata: {
        title: doc.title,
        source: doc.source,
        content: doc.content.slice(0, 1000), // Store truncated for retrieval
      },
    }))
  );

  await index.upsert(vectors);
}

// Query similar vectors
async function querySimilar(query: string, topK = 5, filter?: object) {
  const queryEmbedding = await getEmbedding(query);

  const results = await index.query({
    vector: queryEmbedding,
    topK,
    includeMetadata: true,
    filter,
  });

  return results.matches.map(match => ({
    id: match.id,
    score: match.score,
    ...match.metadata,
  }));
}
```

---

## RAG (Retrieval-Augmented Generation)

### Basic RAG Pipeline

```typescript
class RAGPipeline {
  constructor(
    private vectorStore: VectorStore,
    private llm: LLM,
    private embeddings: EmbeddingModel
  ) {}

  async query(question: string): Promise<string> {
    // 1. Retrieve relevant documents
    const relevantDocs = await this.retrieve(question);

    // 2. Build context
    const context = this.buildContext(relevantDocs);

    // 3. Generate response with context
    return this.generate(question, context);
  }

  private async retrieve(query: string, topK = 5) {
    const queryEmbedding = await this.embeddings.embed(query);

    return this.vectorStore.similaritySearch(queryEmbedding, topK);
  }

  private buildContext(docs: Document[]): string {
    return docs
      .map((doc, i) => `[Document ${i + 1}]\n${doc.content}`)
      .join('\n\n');
  }

  private async generate(question: string, context: string): Promise<string> {
    const prompt = `Answer the question based on the following context.
If the answer is not in the context, say "I don't have enough information."

Context:
${context}

Question: ${question}

Answer:`;

    return this.llm.generate(prompt);
  }
}
```

### Advanced RAG with Reranking

```typescript
import { CohereClient } from 'cohere-ai';

const cohere = new CohereClient({ token: process.env.COHERE_API_KEY });

class AdvancedRAG {
  async query(question: string): Promise<string> {
    // 1. Initial retrieval (over-fetch)
    const candidates = await this.vectorStore.similaritySearch(question, 20);

    // 2. Rerank with cross-encoder
    const reranked = await this.rerank(question, candidates, 5);

    // 3. Generate with reranked context
    return this.generate(question, reranked);
  }

  private async rerank(query: string, documents: Document[], topK: number) {
    const response = await cohere.rerank({
      model: 'rerank-english-v2.0',
      query,
      documents: documents.map(d => d.content),
      topN: topK,
    });

    return response.results.map(r => documents[r.index]);
  }

  private async generate(question: string, context: Document[]) {
    const systemPrompt = `You are a helpful assistant. Answer questions based on the provided context.
Cite your sources using [1], [2], etc.`;

    const contextText = context
      .map((doc, i) => `[${i + 1}] ${doc.content}`)
      .join('\n\n');

    const response = await openai.chat.completions.create({
      model: 'gpt-4o',
      messages: [
        { role: 'system', content: systemPrompt },
        { role: 'user', content: `Context:\n${contextText}\n\nQuestion: ${question}` },
      ],
    });

    return response.choices[0].message.content;
  }
}
```

---

## LangChain

### Chain Composition

```typescript
import { ChatOpenAI } from '@langchain/openai';
import { StringOutputParser } from '@langchain/core/output_parsers';
import { ChatPromptTemplate } from '@langchain/core/prompts';
import { RunnableSequence } from '@langchain/core/runnables';

const model = new ChatOpenAI({ model: 'gpt-4o' });

// Simple chain
const prompt = ChatPromptTemplate.fromTemplate(
  'Summarize the following text in {style} style:\n\n{text}'
);

const chain = prompt.pipe(model).pipe(new StringOutputParser());

const result = await chain.invoke({
  style: 'professional',
  text: 'Long text to summarize...',
});

// Chain with multiple steps
const analysisChain = RunnableSequence.from([
  ChatPromptTemplate.fromTemplate('Extract key points from:\n{text}'),
  model,
  new StringOutputParser(),
  (keyPoints: string) => ({ keyPoints }),
  ChatPromptTemplate.fromTemplate('Create a summary from these key points:\n{keyPoints}'),
  model,
  new StringOutputParser(),
]);

// Branching chain
const routerChain = RunnableSequence.from([
  ChatPromptTemplate.fromTemplate(
    'Classify this query as either "technical" or "general":\n{query}'
  ),
  model,
  new StringOutputParser(),
  async (classification: string) => {
    if (classification.includes('technical')) {
      return technicalChain.invoke({ query });
    }
    return generalChain.invoke({ query });
  },
]);
```

### Document Loading and Splitting

```typescript
import { PDFLoader } from 'langchain/document_loaders/fs/pdf';
import { RecursiveCharacterTextSplitter } from 'langchain/text_splitter';
import { OpenAIEmbeddings } from '@langchain/openai';
import { PineconeStore } from '@langchain/pinecone';

// Load documents
const loader = new PDFLoader('document.pdf');
const docs = await loader.load();

// Split into chunks
const splitter = new RecursiveCharacterTextSplitter({
  chunkSize: 1000,
  chunkOverlap: 200,
  separators: ['\n\n', '\n', ' ', ''],
});

const chunks = await splitter.splitDocuments(docs);

// Create vector store
const vectorStore = await PineconeStore.fromDocuments(
  chunks,
  new OpenAIEmbeddings(),
  {
    pineconeIndex: index,
    namespace: 'documents',
  }
);

// Create retriever
const retriever = vectorStore.asRetriever({
  k: 5,
  filter: { type: 'technical' },
});
```

---

## Structured Output

```typescript
import { z } from 'zod';
import OpenAI from 'openai';
import { zodResponseFormat } from 'openai/helpers/zod';

const PersonSchema = z.object({
  name: z.string(),
  age: z.number(),
  occupation: z.string(),
  skills: z.array(z.string()),
});

async function extractPerson(text: string) {
  const response = await openai.beta.chat.completions.parse({
    model: 'gpt-4o',
    messages: [
      {
        role: 'system',
        content: 'Extract person information from the text.',
      },
      { role: 'user', content: text },
    ],
    response_format: zodResponseFormat(PersonSchema, 'person'),
  });

  return response.choices[0].message.parsed;
}

// With function calling for complex extraction
const extractionTools = [
  {
    type: 'function' as const,
    function: {
      name: 'extract_entities',
      description: 'Extract named entities from text',
      parameters: {
        type: 'object',
        properties: {
          people: {
            type: 'array',
            items: {
              type: 'object',
              properties: {
                name: { type: 'string' },
                role: { type: 'string' },
              },
            },
          },
          organizations: {
            type: 'array',
            items: { type: 'string' },
          },
          dates: {
            type: 'array',
            items: { type: 'string' },
          },
        },
      },
    },
  },
];
```

---

## Related Skills

- [[system-design]] - AI system architecture
- [[performance-optimization]] - ML inference optimization
- [[backend]] - API integration patterns

