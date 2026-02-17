---
name: dspy-prompting
description: Use when "DSPy", "declarative prompting", "automatic prompt optimization", "Stanford NLP", or asking about "optimizing prompts", "prompt compilation", "modular LLM programming", "chain of thought", "few-shot learning"
version: 1.0.0
---

<!-- Adapted from: AI-research-SKILLs/16-prompt-engineering/dspy -->

# DSPy Declarative Language Model Programming

Build AI systems with automatic prompt optimization from Stanford NLP.

## When to Use

- Building complex AI systems with multiple components
- Programming LMs declaratively instead of manual prompting
- Optimizing prompts automatically using data-driven methods
- Creating modular AI pipelines that are maintainable
- Building RAG systems, agents, or classifiers with better reliability

## Quick Start

```bash
pip install dspy
```

### Basic Question Answering

```python
import dspy

lm = dspy.Claude(model="claude-sonnet-4-5-20250929")
dspy.settings.configure(lm=lm)

# Define a signature (input -> output)
class QA(dspy.Signature):
    """Answer questions with short factual answers."""
    question = dspy.InputField()
    answer = dspy.OutputField(desc="often between 1 and 5 words")

qa = dspy.Predict(QA)
response = qa(question="What is the capital of France?")
print(response.answer)  # "Paris"
```

### Chain of Thought Reasoning

```python
class MathProblem(dspy.Signature):
    """Solve math word problems."""
    problem = dspy.InputField()
    answer = dspy.OutputField(desc="numerical answer")

cot = dspy.ChainOfThought(MathProblem)
response = cot(problem="If John has 5 apples and gives 2 to Mary, how many does he have?")
print(response.rationale)  # Shows reasoning steps
print(response.answer)     # "3"
```

## Core Modules

| Module | Use Case |
|--------|----------|
| `dspy.Predict` | Basic prediction |
| `dspy.ChainOfThought` | Reasoning with steps |
| `dspy.ReAct` | Agent-like with tools |
| `dspy.ProgramOfThought` | Code generation for reasoning |

### ReAct Agent

```python
from dspy.predict import ReAct

class SearchQA(dspy.Signature):
    """Answer questions using search."""
    question = dspy.InputField()
    answer = dspy.OutputField()

def search_tool(query: str) -> str:
    """Search Wikipedia."""
    return results

react = ReAct(SearchQA, tools=[search_tool])
result = react(question="When was Python created?")
```

## Automatic Optimization

### BootstrapFewShot

```python
from dspy.teleprompt import BootstrapFewShot

trainset = [
    dspy.Example(question="What is 2+2?", answer="4").with_inputs("question"),
    dspy.Example(question="What is 3+5?", answer="8").with_inputs("question"),
]

def validate_answer(example, pred, trace=None):
    return example.answer == pred.answer

optimizer = BootstrapFewShot(metric=validate_answer, max_bootstrapped_demos=3)
optimized_qa = optimizer.compile(qa, trainset=trainset)
```

### MIPRO Optimizer

```python
from dspy.teleprompt import MIPRO

optimizer = MIPRO(
    metric=validate_answer,
    num_candidates=10,
    init_temperature=1.0
)

optimized_cot = optimizer.compile(cot, trainset=trainset, num_trials=100)
```

## Multi-Stage Pipeline

```python
class MultiHopQA(dspy.Module):
    def __init__(self):
        super().__init__()
        self.retrieve = dspy.Retrieve(k=3)
        self.generate_query = dspy.ChainOfThought("question -> search_query")
        self.generate_answer = dspy.ChainOfThought("context, question -> answer")

    def forward(self, question):
        search_query = self.generate_query(question=question).search_query
        passages = self.retrieve(search_query).passages
        context = "\n".join(passages)
        answer = self.generate_answer(context=context, question=question).answer
        return dspy.Prediction(answer=answer, context=context)
```

## Structured Output

```python
from pydantic import BaseModel, Field

class PersonInfo(BaseModel):
    name: str = Field(description="Full name")
    age: int = Field(description="Age in years")
    occupation: str = Field(description="Current job")

class ExtractPerson(dspy.Signature):
    """Extract person information from text."""
    text = dspy.InputField()
    person: PersonInfo = dspy.OutputField()

extractor = dspy.TypedPredictor(ExtractPerson)
result = extractor(text="John Doe is a 35-year-old software engineer.")
```

## LLM Providers

```python
# Anthropic
lm = dspy.Claude(model="claude-sonnet-4-5-20250929")

# OpenAI
lm = dspy.OpenAI(model="gpt-4")

# Local (Ollama)
lm = dspy.OllamaLocal(model="llama3.1", base_url="http://localhost:11434")

dspy.settings.configure(lm=lm)
```

## Save and Load

```python
# Save optimized module
optimized_qa.save("models/qa_v1.json")

# Load later
loaded_qa = dspy.ChainOfThought("question -> answer")
loaded_qa.load("models/qa_v1.json")
```

## vs Alternatives

| Feature | DSPy | LangChain | Manual |
|---------|------|-----------|--------|
| Prompt Engineering | Automatic | Manual | Manual |
| Optimization | Data-driven | None | Trial & error |
| Modularity | High | Medium | Low |
| Learning Curve | Medium-High | Medium | Low |

**Choose DSPy when:**

- You have training data or can generate it
- Need systematic prompt improvement
- Building complex multi-stage systems

## Resources

- Docs: <https://dspy.ai>
- GitHub: <https://github.com/stanfordnlp/dspy>
- Paper: "DSPy: Compiling Declarative Language Model Calls into Self-Improving Pipelines"
