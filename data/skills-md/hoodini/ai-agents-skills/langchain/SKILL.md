---
name: langchain
description: Build LLM applications with LangChain and LangGraph. Use when creating RAG pipelines, agent workflows, chains, or complex LLM orchestration. Triggers on LangChain, LangGraph, LCEL, RAG, retrieval, agent chain.
---

# LangChain & LangGraph

Build sophisticated LLM applications with composable chains and agent graphs.

## Quick Start

```bash
pip install langchain langchain-openai langchain-anthropic langgraph
```

```python
from langchain_anthropic import ChatAnthropic
from langchain_core.prompts import ChatPromptTemplate

# Simple chain
llm = ChatAnthropic(model="claude-3-sonnet-20240229")
prompt = ChatPromptTemplate.from_template("Explain {topic} in simple terms.")
chain = prompt | llm

response = chain.invoke({"topic": "quantum computing"})
```

## LCEL (LangChain Expression Language)

Compose chains with the pipe operator:

```python
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough

# Chain with parsing
chain = (
    {"topic": RunnablePassthrough()}
    | prompt
    | llm
    | StrOutputParser()
)

result = chain.invoke("machine learning")
```

## RAG Pipeline

```python
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import Chroma
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough

# Create vector store
embeddings = OpenAIEmbeddings()
vectorstore = Chroma.from_documents(documents, embeddings)
retriever = vectorstore.as_retriever(search_kwargs={"k": 4})

# RAG prompt
prompt = ChatPromptTemplate.from_template("""
Answer based on the following context:
{context}

Question: {question}
""")

# RAG chain
rag_chain = (
    {"context": retriever, "question": RunnablePassthrough()}
    | prompt
    | llm
    | StrOutputParser()
)

answer = rag_chain.invoke("What is the refund policy?")
```

## LangGraph Agent

```python
from langgraph.graph import StateGraph, END
from langgraph.prebuilt import ToolNode
from langchain_core.tools import tool
from typing import TypedDict, Annotated
import operator

# Define state
class AgentState(TypedDict):
    messages: Annotated[list, operator.add]

# Define tools
@tool
def search(query: str) -> str:
    """Search the web."""
    return f"Results for: {query}"

@tool
def calculator(expression: str) -> str:
    """Calculate mathematical expression."""
    return str(eval(expression))

tools = [search, calculator]

# Create graph
graph = StateGraph(AgentState)

# Add nodes
graph.add_node("agent", call_model)
graph.add_node("tools", ToolNode(tools))

# Add edges
graph.set_entry_point("agent")
graph.add_conditional_edges(
    "agent",
    should_continue,
    {"continue": "tools", "end": END}
)
graph.add_edge("tools", "agent")

# Compile
app = graph.compile()

# Run
result = app.invoke({"messages": [HumanMessage(content="What is 25 * 4?")]})
```

## Structured Output

```python
from langchain_core.pydantic_v1 import BaseModel, Field

class Person(BaseModel):
    name: str = Field(description="Person's name")
    age: int = Field(description="Person's age")
    occupation: str = Field(description="Person's job")

# Structured LLM
structured_llm = llm.with_structured_output(Person)

result = structured_llm.invoke("John is a 30 year old engineer")
# Person(name='John', age=30, occupation='engineer')
```

## Memory

```python
from langchain_community.chat_message_histories import ChatMessageHistory
from langchain_core.runnables.history import RunnableWithMessageHistory

# Message history
store = {}

def get_session_history(session_id: str):
    if session_id not in store:
        store[session_id] = ChatMessageHistory()
    return store[session_id]

# Chain with memory
with_memory = RunnableWithMessageHistory(
    chain,
    get_session_history,
    input_messages_key="input",
    history_messages_key="history"
)

# Use with session
response = with_memory.invoke(
    {"input": "My name is Alice"},
    config={"configurable": {"session_id": "user123"}}
)
```

## Streaming

```python
# Stream tokens
async for chunk in chain.astream({"topic": "AI"}):
    print(chunk.content, end="", flush=True)

# Stream events (for debugging)
async for event in chain.astream_events({"topic": "AI"}, version="v1"):
    print(event)
```

## LangSmith Tracing

```python
import os
os.environ["LANGCHAIN_TRACING_V2"] = "true"
os.environ["LANGCHAIN_API_KEY"] = "your-api-key"
os.environ["LANGCHAIN_PROJECT"] = "my-project"

# All chains are now traced automatically
chain.invoke({"topic": "AI"})
```

## Resources

- **LangChain Docs**: https://python.langchain.com/docs/introduction/
- **LangGraph Docs**: https://langchain-ai.github.io/langgraph/
- **LangSmith**: https://smith.langchain.com/
- **LangChain Hub**: https://smith.langchain.com/hub
- **LangChain Templates**: https://github.com/langchain-ai/langchain/tree/master/templates
