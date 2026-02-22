---
name: ai-building-chatbots
description: Build a conversational AI assistant with memory and state. Use when you need a customer support chatbot, helpdesk bot, onboarding assistant, sales qualification bot, FAQ assistant, or any multi-turn conversational AI. Powered by DSPy for response quality and LangGraph for conversation state management.
---

# Build a Conversational AI Chatbot

Guide the user through building a multi-turn chatbot that remembers context, follows conversation flows, and produces high-quality responses. Uses DSPy for optimizable response generation and LangGraph for conversation state, memory, and flow control.

## Step 1: Define the conversation

Ask the user:
1. **What does the bot do?** (answer questions, resolve issues, qualify leads, guide onboarding?)
2. **What states can the conversation be in?** (greeting, gathering info, resolving, escalating, closing?)
3. **When should the bot escalate to a human?** (complex issues, angry users, sensitive topics?)
4. **What docs or data should it draw from?** (help articles, product docs, FAQs, database?)

## Step 2: Build the response module (DSPy)

The core of your chatbot is a DSPy module that generates responses given conversation history and context.

### Basic response module

```python
import dspy

class ChatResponse(dspy.Signature):
    """Generate a helpful, on-brand response to the user's message."""
    conversation_history: str = dspy.InputField(desc="Previous messages in the conversation")
    context: str = dspy.InputField(desc="Relevant information from docs or database")
    user_message: str = dspy.InputField(desc="The user's latest message")
    response: str = dspy.OutputField(desc="Helpful response to the user")

class ChatBot(dspy.Module):
    def __init__(self):
        self.respond = dspy.ChainOfThought(ChatResponse)

    def forward(self, conversation_history, context, user_message):
        return self.respond(
            conversation_history=conversation_history,
            context=context,
            user_message=user_message,
        )
```

### With intent classification

Route different intents to specialized handlers:

```python
from typing import Literal

class ClassifyIntent(dspy.Signature):
    """Classify the user's intent from their message."""
    conversation_history: str = dspy.InputField()
    user_message: str = dspy.InputField()
    intent: Literal["question", "complaint", "request", "greeting", "goodbye"] = dspy.OutputField()

class ChatBotWithRouting(dspy.Module):
    def __init__(self):
        self.classify = dspy.Predict(ClassifyIntent)
        self.respond_question = dspy.ChainOfThought(AnswerQuestion)
        self.respond_complaint = dspy.ChainOfThought(HandleComplaint)
        self.respond_request = dspy.ChainOfThought(HandleRequest)
        self.respond_greeting = dspy.Predict(Greeting)

    def forward(self, conversation_history, context, user_message):
        intent = self.classify(
            conversation_history=conversation_history,
            user_message=user_message,
        ).intent

        handler = {
            "question": self.respond_question,
            "complaint": self.respond_complaint,
            "request": self.respond_request,
            "greeting": self.respond_greeting,
        }.get(intent, self.respond_question)

        return handler(
            conversation_history=conversation_history,
            context=context,
            user_message=user_message,
        )
```

## Step 3: Add conversation state (LangGraph)

LangGraph manages the conversation flow — what state the bot is in, when to transition, and when to escalate.

### Define conversation state

```python
from langgraph.graph import StateGraph, START, END
from typing import TypedDict, Annotated
import operator

class ConversationState(TypedDict):
    messages: Annotated[list[dict], operator.add]  # full message history
    current_intent: str
    context: str           # retrieved docs/data for current turn
    escalate: bool         # whether to hand off to a human
    resolved: bool         # whether the issue is resolved
    turn_count: int
```

### Build the conversation graph

```python
import dspy

# Initialize DSPy modules
classifier = dspy.Predict(ClassifyIntent)
responder = dspy.ChainOfThought(ChatResponse)

def classify_node(state: ConversationState) -> dict:
    """Classify the user's intent."""
    history = format_history(state["messages"][:-1])
    user_msg = state["messages"][-1]["content"]
    result = classifier(conversation_history=history, user_message=user_msg)
    return {"current_intent": result.intent}

def retrieve_node(state: ConversationState) -> dict:
    """Retrieve relevant docs for the current message."""
    user_msg = state["messages"][-1]["content"]
    # Your retrieval logic here (see /ai-searching-docs)
    docs = retrieve_relevant_docs(user_msg)
    return {"context": "\n".join(docs)}

def respond_node(state: ConversationState) -> dict:
    """Generate a response using DSPy."""
    history = format_history(state["messages"][:-1])
    user_msg = state["messages"][-1]["content"]
    result = responder(
        conversation_history=history,
        context=state["context"],
        user_message=user_msg,
    )
    return {
        "messages": [{"role": "assistant", "content": result.response}],
        "turn_count": state["turn_count"] + 1,
    }

def check_escalation(state: ConversationState) -> dict:
    """Decide if this needs human handoff."""
    should_escalate = (
        state["current_intent"] == "complaint"
        and state["turn_count"] > 3
    )
    return {"escalate": should_escalate}

def format_history(messages: list[dict]) -> str:
    return "\n".join(f"{m['role']}: {m['content']}" for m in messages[-10:])

# Build the graph
graph = StateGraph(ConversationState)
graph.add_node("classify", classify_node)
graph.add_node("retrieve", retrieve_node)
graph.add_node("respond", respond_node)
graph.add_node("check_escalation", check_escalation)

graph.add_edge(START, "classify")
graph.add_edge("classify", "retrieve")
graph.add_edge("retrieve", "respond")
graph.add_edge("respond", "check_escalation")

def route_after_escalation_check(state: ConversationState) -> str:
    if state["escalate"]:
        return "escalate"
    return "done"

graph.add_conditional_edges(
    "check_escalation",
    route_after_escalation_check,
    {"escalate": END, "done": END},
)

app = graph.compile()
```

### Run a conversation turn

```python
result = app.invoke({
    "messages": [{"role": "user", "content": "How do I reset my password?"}],
    "current_intent": "",
    "context": "",
    "escalate": False,
    "resolved": False,
    "turn_count": 0,
})
print(result["messages"][-1]["content"])
```

## Step 4: Add memory

### Session memory with checkpointing

LangGraph's checkpointer persists conversation state across requests:

```python
from langgraph.checkpoint.memory import MemorySaver

checkpointer = MemorySaver()
app = graph.compile(checkpointer=checkpointer)

# Each user session gets a unique thread_id
config = {"configurable": {"thread_id": "user-abc-123"}}

# Turn 1
result = app.invoke(
    {"messages": [{"role": "user", "content": "Hi, I need help with billing"}],
     "current_intent": "", "context": "", "escalate": False, "resolved": False, "turn_count": 0},
    config=config,
)

# Turn 2 — state is preserved, the bot remembers the conversation
result = app.invoke(
    {"messages": [{"role": "user", "content": "I was charged twice last month"}]},
    config=config,
)
```

For production, use a persistent backend:

```python
from langgraph.checkpoint.postgres import PostgresSaver

checkpointer = PostgresSaver(conn_string="postgresql://user:pass@localhost/chatbot")
app = graph.compile(checkpointer=checkpointer)
```

### Conversation summary for long chats

When conversations get long, summarize older messages to stay within token limits:

```python
class SummarizeConversation(dspy.Signature):
    """Summarize the conversation so far, preserving key details."""
    conversation: str = dspy.InputField()
    summary: str = dspy.OutputField(desc="Concise summary of the conversation so far")

summarizer = dspy.Predict(SummarizeConversation)

def maybe_summarize(state: ConversationState) -> dict:
    """Summarize if conversation is getting long."""
    if len(state["messages"]) > 20:
        history = format_history(state["messages"][:-5])
        summary = summarizer(conversation=history).summary
        # Keep summary + last 5 messages
        return {
            "messages": [
                {"role": "system", "content": f"Summary of earlier conversation: {summary}"},
                *state["messages"][-5:],
            ]
        }
    return {}
```

## Step 5: Ground responses in docs

Retrieve relevant documents each turn to keep responses factual.

```python
class DocGroundedResponse(dspy.Signature):
    """Answer the user's question based on the provided documentation.
    Only use information from the docs. If the docs don't cover it, say so."""
    conversation_history: str = dspy.InputField()
    docs: list[str] = dspy.InputField(desc="Relevant documentation passages")
    user_message: str = dspy.InputField()
    response: str = dspy.OutputField()

class GroundedChatBot(dspy.Module):
    def __init__(self, retriever):
        self.retriever = retriever
        self.respond = dspy.ChainOfThought(DocGroundedResponse)

    def forward(self, conversation_history, user_message):
        # Retrieve docs relevant to the current message
        docs = self.retriever(user_message).passages
        return self.respond(
            conversation_history=conversation_history,
            docs=docs,
            user_message=user_message,
        )
```

See `/ai-searching-docs` for setting up retrievers and vector stores, including loading data from PDFs, Notion, and other sources with LangChain document loaders.

## Step 6: Add guardrails

### Response quality with DSPy assertions

```python
class GuardedChatBot(dspy.Module):
    def __init__(self, retriever):
        self.retriever = retriever
        self.respond = dspy.ChainOfThought(DocGroundedResponse)

    def forward(self, conversation_history, user_message):
        docs = self.retriever(user_message).passages
        result = self.respond(
            conversation_history=conversation_history,
            docs=docs,
            user_message=user_message,
        )

        # Guardrails
        dspy.Suggest(
            len(result.response.split()) < 200,
            "Keep responses concise — under 200 words",
        )
        dspy.Suggest(
            not any(word in result.response.lower() for word in ["obviously", "clearly", "simply"]),
            "Avoid condescending language",
        )
        dspy.Assert(
            "I am an AI" not in result.response,
            "Don't break character with meta-statements",
        )

        return result
```

### Human-in-the-loop for sensitive actions

Use LangGraph's interrupt to pause before the bot takes real actions:

```python
app = graph.compile(
    checkpointer=checkpointer,
    interrupt_before=["execute_refund", "cancel_account"],  # pause here
)

# Bot runs until it reaches a sensitive action
result = app.invoke(input_state, config)

# Human agent reviews the proposed action
# If approved, resume:
result = app.invoke(None, config)  # continues from checkpoint
```

## Step 7: Optimize and evaluate

### Conversation-level metrics

```python
def chatbot_metric(example, prediction, trace=None):
    """Score a single conversation turn."""
    judge = dspy.Predict(JudgeTurn)
    result = judge(
        user_message=example.user_message,
        expected_response=example.response,
        actual_response=prediction.response,
        conversation_history=example.conversation_history,
    )
    return result.is_good

class JudgeTurn(dspy.Signature):
    """Judge if the chatbot response is helpful, accurate, and on-topic."""
    user_message: str = dspy.InputField()
    expected_response: str = dspy.InputField()
    actual_response: str = dspy.InputField()
    conversation_history: str = dspy.InputField()
    is_good: bool = dspy.OutputField()
```

### Build a training set from real conversations

```python
trainset = []
for convo in real_conversations:
    for turn in convo["turns"]:
        trainset.append(
            dspy.Example(
                conversation_history=turn["history"],
                user_message=turn["user_message"],
                context=turn["context"],
                response=turn["response"],
            ).with_inputs("conversation_history", "user_message", "context")
        )
```

### Optimize

```python
optimizer = dspy.MIPROv2(metric=chatbot_metric, auto="medium")
optimized_bot = optimizer.compile(chatbot, trainset=trainset)

# Save optimized prompts
optimized_bot.save("chatbot_optimized.json")
```

## Key patterns

- **DSPy for response generation, LangGraph for flow control** — DSPy modules handle what the bot says; LangGraph handles conversation state and routing
- **Checkpointing is your memory** — use LangGraph's checkpointer so conversations persist across HTTP requests
- **Retrieve every turn** — don't assume context from earlier turns is still relevant; re-retrieve each time
- **Summarize long conversations** — once past ~20 messages, summarize older context to stay within token limits
- **Classify intent early** — knowing the user's intent lets you route to specialized handlers
- **Interrupt before real actions** — use LangGraph's `interrupt_before` so humans approve refunds, cancellations, etc.
- **Optimize on real conversations** — collect actual chat logs to build training data for DSPy optimization

## Additional resources

- For worked examples (support bot, FAQ assistant), see [examples.md](examples.md)
- For the LangChain/LangGraph API reference, see [`docs/langchain-langgraph-reference.md`](../../docs/langchain-langgraph-reference.md)
- Need to search docs for grounding? Use `/ai-searching-docs`
- Need the bot to take actions (call APIs, tools)? Use `/ai-taking-actions`
- Building multiple bots that work together? Use `/ai-coordinating-agents`
- Next: `/ai-improving-accuracy` to measure and improve your chatbot
