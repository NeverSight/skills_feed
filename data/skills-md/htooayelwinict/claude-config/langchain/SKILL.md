---
name: langchain
description: Expert guidance for building LLM applications with LangChain framework - chains, prompts, memory, retrievers, and integrations.
allowed-tools: Read, Edit, Bash, Grep, mcp_context7
---

# LangChain Skill

Use this skill when working with LangChain for building LLM-powered applications.

## 📚 Documentation Lookup (Context7)

Always verify patterns with latest docs:
```
mcp_context7_resolve-library-id(libraryName="langchain", query="LCEL chains")
mcp_context7_query-docs(libraryId="/langchain-ai/langchain", query="RunnablePassthrough examples")
```

## Core Concepts

### 1. LLMs and Chat Models
```python
from langchain_openai import ChatOpenAI
from langchain_anthropic import ChatAnthropic

# Chat model initialization
llm = ChatOpenAI(model="gpt-4o", temperature=0)
claude = ChatAnthropic(model="claude-sonnet-4-20250514")

# Invoke with messages
from langchain_core.messages import HumanMessage, SystemMessage
response = llm.invoke([
    SystemMessage(content="You are a helpful assistant."),
    HumanMessage(content="Hello!")
])
```

### 2. Prompt Templates
```python
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder

# Simple template
prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a {role} assistant."),
    ("human", "{input}")
])

# With message history placeholder
prompt_with_history = ChatPromptTemplate.from_messages([
    ("system", "You are a helpful assistant."),
    MessagesPlaceholder(variable_name="history"),
    ("human", "{input}")
])

# Format and invoke
chain = prompt | llm
result = chain.invoke({"role": "coding", "input": "Write a function"})
```

### 3. Output Parsers
```python
from langchain_core.output_parsers import StrOutputParser, JsonOutputParser
from pydantic import BaseModel, Field

class Answer(BaseModel):
    answer: str = Field(description="The answer")
    confidence: float = Field(description="Confidence 0-1")

parser = JsonOutputParser(pydantic_object=Answer)
chain = prompt | llm | parser
```

### 4. Chains with LCEL (LangChain Expression Language)
```python
from langchain_core.runnables import RunnablePassthrough, RunnableLambda

# Pipe syntax for chaining
chain = prompt | llm | StrOutputParser()

# Parallel execution
from langchain_core.runnables import RunnableParallel

parallel_chain = RunnableParallel(
    summary=summary_chain,
    translation=translate_chain
)

# Branching with RunnableBranch
from langchain_core.runnables import RunnableBranch

branch = RunnableBranch(
    (lambda x: "code" in x["topic"], code_chain),
    (lambda x: "math" in x["topic"], math_chain),
    default_chain
)
```

### 5. Memory and Chat History
```python
from langchain_community.chat_message_histories import ChatMessageHistory
from langchain_core.runnables.history import RunnableWithMessageHistory

history = ChatMessageHistory()

chain_with_history = RunnableWithMessageHistory(
    chain,
    lambda session_id: history,
    input_messages_key="input",
    history_messages_key="history"
)

# Invoke with session
result = chain_with_history.invoke(
    {"input": "Hi!"},
    config={"configurable": {"session_id": "user123"}}
)
```

### 6. Retrievers and RAG
```python
from langchain_community.vectorstores import FAISS
from langchain_openai import OpenAIEmbeddings
from langchain_core.runnables import RunnablePassthrough

# Create retriever
embeddings = OpenAIEmbeddings()
vectorstore = FAISS.from_texts(texts, embeddings)
retriever = vectorstore.as_retriever(search_kwargs={"k": 4})

# RAG chain
rag_prompt = ChatPromptTemplate.from_template("""
Answer based on context:
{context}

Question: {question}
""")

rag_chain = (
    {"context": retriever, "question": RunnablePassthrough()}
    | rag_prompt
    | llm
    | StrOutputParser()
)
```

### 7. Tools and Tool Calling
```python
from langchain_core.tools import tool

@tool
def search(query: str) -> str:
    """Search for information."""
    return f"Results for: {query}"

@tool
def calculator(expression: str) -> float:
    """Evaluate math expression."""
    return eval(expression)

# Bind tools to model
llm_with_tools = llm.bind_tools([search, calculator])

# Or use ToolNode in LangGraph
from langgraph.prebuilt import ToolNode
tool_node = ToolNode([search, calculator])
```

## Best Practices

1. **Use LCEL** - Prefer `|` pipe syntax over legacy Chain classes
2. **Streaming** - Use `.stream()` for real-time output
3. **Async** - Use `.ainvoke()`, `.astream()` for concurrent operations
4. **Callbacks** - Add logging/tracing with callback handlers
5. **Caching** - Enable LLM caching for repeated queries
6. **Error Handling** - Wrap chains with fallbacks using `.with_fallbacks()`

## Common Patterns

### Structured Output
```python
from langchain_core.output_parsers import PydanticOutputParser

class Output(BaseModel):
    result: str
    
llm_structured = llm.with_structured_output(Output)
```

### Streaming
```python
for chunk in chain.stream({"input": "Tell me a story"}):
    print(chunk, end="", flush=True)
```

### Retry with Fallback
```python
chain_with_fallback = main_chain.with_fallbacks([backup_chain])
```

## Installation
```bash
pip install langchain langchain-core langchain-openai langchain-anthropic
pip install langchain-community  # for integrations
```
