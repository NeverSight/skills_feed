---
name: dspy-code
description: Specialized AI assistant for DSPy development with deep knowledge of predictors, optimizers, adapters, and GEPA integration. Provides session management, codebase indexing, and command-based workflows.
triggers:
  - dspy
  - prompt optimization
  - llm application
  - language model programming
  - few-shot learning
  - chain of thought
  - retrieval augmented generation
  - rag pipeline
  - optimizer
  - signature
  - predictor
version: 1.0.0
codebase: /Users/mikhail/Downloads/architect/dspy-code-codebase
---

# DSPy-Code Skill

**Specialized AI assistant for building LLM applications with DSPy**

---

## When to Use This Skill

**Activate dspy-code for:**

### Development Tasks
- Creating DSPy modules, signatures, and pipelines
- Building RAG (Retrieval-Augmented Generation) systems
- Implementing multi-hop reasoning and complex workflows
- Designing typed outputs with Pydantic schemas
- Creating agents with tool use (ReAct patterns)
- Writing custom metrics and evaluation functions

### Optimization Tasks
- Running prompt optimization with GEPA
- Compiling modules with BootstrapFewShot, MIPRO, COPRO
- Hyperparameter tuning and grid search
- A/B testing optimized vs unoptimized modules
- Statistical significance testing
- Performance benchmarking

### Project Management
- Initializing new DSPy projects
- Connecting to existing workspaces
- Generating demos from templates
- Validating DSPy code for correctness
- Exporting to Python, JSON, YAML formats
- Session tracking and history

### Learning & Exploration
- Understanding DSPy patterns and anti-patterns
- Choosing the right predictor for your task
- Selecting optimal optimizers based on data size
- Learning about 10 predictors, 11 optimizers, 4 adapters
- Exploring 12 production-ready module templates

---

## Key Principle

**Use dspy-code for ALL DSPy-related development**

DSPy is fundamentally different from traditional prompt engineering:
- **Programming, not prompting** - Write declarative modules, not brittle prompts
- **Signatures define contracts** - Clear input/output specifications
- **Optimizers tune automatically** - No manual prompt engineering
- **Composition over monoliths** - Build complex programs from simple modules

---

## Core Capabilities

### 1. Deep DSPy Knowledge

**10 Predictor Types**:
- `Predict` - Basic predictor
- `ChainOfThought` - CoT reasoning
- `ChainOfThoughtWithHint` - CoT with hints
- `ProgramOfThought` - Code execution for math
- `ReAct` - Reasoning + Acting for agents
- `MultiChainComparison` - Compare multiple chains
- `Retrieve` - Document retrieval
- `TypedPredictor` - Type-constrained outputs
- `Ensemble` - Multiple predictor voting
- `majority` - Majority voting aggregation

**11 Optimizer Types**:
- `BootstrapFewShot` - Example-based (10-50 examples, ⚡⚡⚡ fast)
- `BootstrapFewShotWithRandomSearch` - Hyperparameter tuning (50+, ⚡⚡)
- `BootstrapFewShotWithOptuna` - Optuna integration (50+, ⚡⚡)
- `COPRO` - Prompt optimization (50+, ⚡⚡, ⭐⭐⭐⭐)
- `MIPRO` - Multi-stage instruction (100+, ⚡, ⭐⭐⭐⭐⭐)
- `MIPROv2` - Enhanced MIPRO (200+, ⚡, ⭐⭐⭐⭐⭐)
- `BetterTogether` - Collaborative optimization (100+, ⚡⚡)
- `Ensemble` - Ensemble methods (100+, ⚡, ⭐⭐⭐⭐)
- `KNNFewShot` - KNN-based selection (100+, ⚡⚡, ⭐⭐⭐⭐)
- `LabeledFewShot` - Labeled examples (50+, ⚡⚡⚡)
- `SignatureOptimizer` - Signature tuning (100+, ⚡⚡)

**4 Adapter Types**:
- `ChatAdapter` - Chat model integration
- `JSONAdapter` - JSON output formatting
- `FunctionAdapter` - Function calling
- `ImageAdapter` - Image input handling

**Built-in Metrics**:
- Accuracy (classification tasks)
- F1 Score (multi-label classification)
- ROUGE-L (text generation quality)
- BLEU (translation quality)
- Exact Match (strict comparison)
- Semantic Similarity (embedding-based)
- Custom metrics (user-defined)

### 2. GEPA Integration

**Genetic-Evolutionary Prompt Architecture** for automatic prompt optimization:

```python
from dspy.gepa import GEPA

gepa = GEPA(
    metric=accuracy,
    population_size=10,
    generations=20,
    mutation_rate=0.3,
    crossover_rate=0.7
)

result = gepa.optimize(
    seed_prompt="question -> answer",
    training_examples=trainset,
    budget=100  # Max LLM calls
)
```

**GEPA Workflow**:
1. **Initialize** population with prompt variants
2. **Evaluate** each variant on training data
3. **Select** best-performing prompts
4. **Crossover** and **mutate** to create new variants
5. **Repeat** for N generations
6. **Return** optimized prompt

**When to use GEPA**:
- Prompt engineering bottleneck
- Need automatic optimization
- Have 50+ training examples
- Want to explore prompt space systematically

### 3. Session Management

Track development across multiple sessions:

```python
session = {
    'id': 'session_123',
    'workspace': '/path/to/project',
    'created_at': '2024-01-15T10:30:00Z',
    'modules': [...],
    'optimizers': [...],
    'datasets': [...],
    'metrics': [...]
}
```

**Session features**:
- Workspace tracking
- Module registry
- Optimizer history
- Dataset versioning
- Metric tracking
- Export/import state

### 4. Codebase RAG Indexing

Index existing DSPy codebases for contextual assistance:

```typescript
interface CodebaseIndex {
    workspace: string;
    indexed_at: string;
    modules: Array<{
        path: string;
        name: string;
        signature?: string;
        type: string;
    }>;
    signatures: Array<{
        path: string;
        definition: string;
    }>;
    metrics: Array<{
        path: string;
        name: string;
        type: MetricType;
    }>;
}
```

**Indexing enables**:
- Fast module discovery
- Signature lookups
- Metric finding
- Pattern detection
- Dependency analysis

---

## Two-Phase Workflow

### Phase 1: Development

**Goal**: Build working DSPy modules

```
┌──────────────┐
│  /init       │  Initialize project structure
└──────┬───────┘
       │
       ▼
┌──────────────┐
│  Design      │  Define signatures and modules
└──────┬───────┘
       │
       ▼
┌──────────────┐
│  Implement   │  Write forward() methods
└──────┬───────┘
       │
       ▼
┌──────────────┐
│  /validate   │  Check correctness
└──────────────┘
```

**Commands**:
- `/init <project_name>` - Create new DSPy project
- `/connect` - Connect to existing workspace
- `/demo <template>` - Generate demo from 12 templates
- `/validate <file>` - Validate module structure and signatures

**Development checklist**:
- [ ] Signatures defined with clear inputs/outputs
- [ ] Modules composed from predictors
- [ ] Forward methods implemented
- [ ] Type hints added where appropriate
- [ ] Unit tests written
- [ ] Validation passed

### Phase 2: Optimization

**Goal**: Optimize modules for production

```
┌──────────────┐
│  Data        │  Prepare training/dev/test sets
└──────┬───────┘
       │
       ▼
┌──────────────┐
│  Metric      │  Define evaluation function
└──────┬───────┘
       │
       ▼
┌──────────────┐
│  /optimize   │  Compile with optimizer
└──────┬───────┘
       │
       ▼
┌──────────────┐
│  Evaluate    │  Test on dev/test sets
└──────┬───────┘
       │
       ▼
┌──────────────┐
│  /export     │  Save optimized program
└──────────────┘
```

**Commands**:
- `/optimize <module>` - Run full optimization workflow
- `/evaluate <module>` - Evaluate on dev/test sets
- `/export <format>` - Export to Python/JSON/YAML

**Optimization checklist**:
- [ ] Training data prepared (10+ examples)
- [ ] Metric function defined
- [ ] Optimizer selected based on data size
- [ ] Compilation completed successfully
- [ ] Dev set evaluation performed
- [ ] A/B test against baseline
- [ ] Optimized program saved
- [ ] Production deployment planned

---

## Command Reference

### `/init <project_name>`
Initialize new DSPy project with structure:
```
project_name/
├── modules/          # DSPy modules
├── data/            # Training/dev/test datasets
├── metrics/         # Custom metrics
├── optimized/       # Saved optimized programs
├── tests/           # Unit tests
└── config.py        # Configuration
```

**Options**:
- `--template <name>` - Use template (qa, rag, multi-hop, agent)
- `--lm <model>` - Set language model (gpt-3.5-turbo, gpt-4, claude-3, etc.)
- `--retrieval` - Include retrieval setup

### `/connect`
Connect to existing DSPy workspace:
- Indexes codebase for RAG
- Discovers modules, signatures, metrics
- Loads configuration
- Resumes session

### `/demo <template>`
Generate demo from 12 templates:
- `simple-qa` - Basic question answering
- `rag` - Retrieval-augmented generation
- `multi-hop` - Multi-step reasoning
- `typed-output` - Structured data extraction
- `classification` - Multi-class classification
- `agent` - ReAct agent with tools
- `ensemble` - Multiple predictor voting
- `self-refining` - Iterative refinement
- `hinted-qa` - Guided reasoning
- `program-of-thought` - Code generation
- `chatbot` - Multi-turn conversation
- `data-pipeline` - ETL workflow

**Options**:
- `--with-optimization` - Include optimization example
- `--with-tests` - Include unit tests
- `--output <path>` - Custom output path

### `/optimize <module>`
Run complete optimization workflow:

**Steps**:
1. Load module from file
2. Prompt for training data
3. Prompt for metric function
4. Suggest optimizer based on data size
5. Run compilation
6. Evaluate on dev set
7. Display results and improvements
8. Save optimized program

**Options**:
- `--optimizer <type>` - Force optimizer (bootstrap, mipro, copro, etc.)
- `--budget <N>` - Max optimization budget
- `--metric <name>` - Use specific metric
- `--no-save` - Don't save optimized program
- `--use-gepa` - Enable GEPA optimization

### `/validate <file>`
Validate DSPy code for correctness:

**Checks**:
- Signature format validity
- Forward method presence
- Type annotations
- Module composition
- Metric function signature
- Dataset format
- Optimizer configuration

**Returns**:
```typescript
{
    valid: boolean;
    errors: string[];        // Critical issues
    warnings: string[];      // Non-critical issues
    suggestions: string[];   // Improvement suggestions
}
```

### `/export <format>`
Export module to target format:

**Formats**:
- `python` - Python code with comments
- `json` - JSON configuration
- `yaml` - YAML configuration
- `markdown` - Documentation

**Options**:
- `--include-examples` - Include usage examples
- `--include-tests` - Include test code
- `--minify` - Remove comments and whitespace

---

## Version-Aware Guidance

### DSPy 2.5+ (Recommended)
Full feature support:
- All 10 predictors
- All 11 optimizers
- All 4 adapters
- GEPA integration
- Typed outputs with Pydantic
- Advanced RAG features

### DSPy 2.4
Legacy support:
- Most predictors available
- Optimizer syntax differences
- Limited GEPA support
- Basic RAG features

**Migration guide**:
```python
# DSPy 2.4 (old)
optimizer = dspy.BootstrapFewShot(
    metric=metric,
    max_bootstrapped_demos=4
)

# DSPy 2.5+ (new)
optimizer = dspy.BootstrapFewShot(
    metric=metric,
    max_bootstrapped_demos=4,
    max_labeled_demos=8  # New parameter
)
```

### DSPy 2.0-2.3
Basic support:
- Core predictors only
- Limited optimizer options
- No GEPA
- Manual RAG setup

---

## Usage Examples

### Example 1: Build Simple QA Module

**User**: Create a question-answering module with chain-of-thought reasoning

**Assistant** (using dspy-code):
```python
import dspy

class QAModule(dspy.Module):
    """Question answering with chain of thought."""

    def __init__(self):
        super().__init__()
        self.qa = dspy.ChainOfThought("question -> answer")

    def forward(self, question):
        return self.qa(question=question)

# Usage
lm = dspy.OpenAI(model="gpt-3.5-turbo")
dspy.settings.configure(lm=lm)

qa = QAModule()
result = qa(question="What is DSPy?")
print(result.answer)
```

**Next steps**: Use `/validate` to check, then `/optimize` with training data.

### Example 2: Optimize RAG Pipeline

**User**: I have a RAG module and 100 training examples. How do I optimize it?

**Assistant** (using dspy-code):
```python
# 1. Define metric
def accuracy(example, prediction, trace=None):
    return example.answer.lower() in prediction.answer.lower()

# 2. Prepare data
trainset = [
    dspy.Example(question="...", answer="...").with_inputs("question")
    for ... in data
]

# 3. Choose optimizer (MIPRO for 100+ examples)
optimizer = dspy.MIPRO(
    metric=accuracy,
    prompt_model=dspy.OpenAI("gpt-4"),
    task_model=dspy.OpenAI("gpt-3.5-turbo"),
    num_trials=20,
    minibatch_size=50
)

# 4. Compile
optimized_rag = optimizer.compile(rag_module, trainset=trainset)

# 5. Evaluate
from dspy.evaluate import Evaluate
evaluator = Evaluate(devset=devset, metric=accuracy)
score = evaluator(optimized_rag)
print(f"Accuracy: {score:.2%}")

# 6. Save
optimized_rag.save('rag_optimized.json')
```

**Expected improvement**: +30-50% accuracy with 100 examples and MIPRO.

### Example 3: Use GEPA for Prompt Optimization

**User**: I want to automatically find the best prompt for my task

**Assistant** (using dspy-code):
```python
from dspy.gepa import GEPA

# 1. Define task
seed_prompt = "question -> answer"
training_examples = trainset[:50]

# 2. Configure GEPA
gepa = GEPA(
    metric=accuracy,
    population_size=10,
    generations=20,
    mutation_rate=0.3,
    crossover_rate=0.7
)

# 3. Optimize
result = gepa.optimize(
    seed_prompt=seed_prompt,
    training_examples=training_examples,
    budget=100  # Max 100 LLM calls
)

# 4. Use optimized prompt
print(f"Best prompt: {result.best_prompt}")
print(f"Score: {result.best_score:.2%}")

# 5. Create module with optimized prompt
class OptimizedQA(dspy.Module):
    def __init__(self):
        super().__init__()
        self.qa = dspy.ChainOfThought(result.best_prompt)

    def forward(self, question):
        return self.qa(question=question)
```

**GEPA benefits**: Explores prompt space automatically, no manual engineering needed.

---

## Best Practices

### 1. Start Simple
Begin with basic signatures and predictors:
```python
# Good: Start simple
self.qa = dspy.ChainOfThought("question -> answer")

# Bad: Overengineering
self.qa = dspy.Ensemble([
    dspy.ChainOfThought(...),
    dspy.ProgramOfThought(...),
    dspy.ReAct(...)
])  # Too complex for iteration
```

### 2. Optimize Early
Run optimization on small datasets before scaling:
```python
# Iterate quickly with 10 examples
quick_optimizer = dspy.BootstrapFewShot(metric=accuracy)
quick_test = quick_optimizer.compile(module, trainset=trainset[:10])

# Then scale to full dataset
full_optimizer = dspy.MIPRO(metric=accuracy)
production = full_optimizer.compile(module, trainset=full_trainset)
```

### 3. Measure Everything
Track metrics throughout development:
```python
# Log all predictions
def predict_with_logging(module, input):
    prediction = module(input=input)
    log_prediction(input, prediction, timestamp=datetime.now())
    return prediction
```

### 4. Version Control
Save and track optimized programs:
```python
# Save with version
version = "v1.2.3"
optimized.save(f'models/qa_{version}.json')

# Track performance
performance_log = {
    'version': version,
    'dev_score': dev_score,
    'test_score': test_score,
    'optimizer': 'MIPRO',
    'timestamp': datetime.now().isoformat()
}
save_performance_log(performance_log)
```

### 5. Modular Design
Keep modules focused and composable:
```python
# Good: Single responsibility
class Retriever(dspy.Module):
    def forward(self, query):
        return self.retrieve(query)

class Generator(dspy.Module):
    def forward(self, context, question):
        return self.generate(context=context, question=question)

class RAG(dspy.Module):
    def __init__(self):
        self.retriever = Retriever()
        self.generator = Generator()

    def forward(self, question):
        context = self.retriever(query=question)
        return self.generator(context=context, question=question)
```

### 6. Test Thoroughly
Unit test modules before optimization:
```python
import unittest

class TestQAModule(unittest.TestCase):
    def setUp(self):
        self.qa = QAModule()

    def test_basic_question(self):
        result = self.qa(question="What is 2+2?")
        self.assertIsNotNone(result.answer)

    def test_complex_question(self):
        result = self.qa(question="Explain quantum computing")
        self.assertTrue(len(result.answer) > 50)
```

---

## Troubleshooting

### Issue: Low improvement after optimization
**Solutions**:
1. Increase training data size (aim for 50-200 examples)
2. Try different optimizer (MIPRO, COPRO for better quality)
3. Improve metric function (ensure it captures task requirements)
4. Add more demonstrations (`max_bootstrapped_demos`)
5. Use stronger teacher model (GPT-4 for optimization)

### Issue: Optimization too slow
**Solutions**:
1. Reduce `num_trials` or `budget`
2. Use smaller training set for iteration
3. Enable parallel evaluation (`num_threads=4`)
4. Use faster base model (gpt-3.5-turbo)
5. Cache predictions to avoid redundant calls

### Issue: Module validation fails
**Solutions**:
1. Check signature format: `"input1, input2 -> output1, output2"`
2. Ensure forward() method exists and returns Prediction
3. Add type hints: `def forward(self, input: str) -> dspy.Prediction`
4. Verify module inheritance: `class MyModule(dspy.Module)`
5. Check that all predictors are initialized in `__init__()`

### Issue: GEPA not improving prompts
**Solutions**:
1. Increase `population_size` (try 15-20)
2. Run more `generations` (try 30-50)
3. Adjust mutation rate (0.4-0.5 for exploration)
4. Provide more training examples (50+ recommended)
5. Ensure metric function is accurate and informative

---

## Integration with Claude Code

This skill provides:

- **Contextual assistance** - Deep DSPy knowledge available in chat
- **Code generation** - Generate modules from templates
- **Validation** - Check DSPy code for correctness
- **Optimization guidance** - Recommend optimizers and configurations
- **Workflow management** - Track sessions and progress
- **Export utilities** - Convert to multiple formats

**When to use in conversation**:
- "Create a RAG module with MIPRO optimization"
- "Validate my DSPy code"
- "What optimizer should I use for 50 examples?"
- "Generate a demo of multi-hop reasoning"
- "Export this module to JSON"
- "How do I use GEPA for prompt optimization?"

---

## Resources

- **DSPy Documentation**: https://dspy-docs.vercel.app
- **GitHub**: https://github.com/stanfordnlp/dspy
- **Paper**: "DSPy: Compiling Declarative Language Model Calls into Self-Improving Pipelines"
- **Examples**: https://github.com/stanfordnlp/dspy/tree/main/examples
- **Codebase**: `/Users/mikhail/Downloads/architect/dspy-code-codebase`

---

**Skill Version**: 1.0.0
**Last Updated**: 2025-12-02
**Compatible with**: DSPy 2.4+
