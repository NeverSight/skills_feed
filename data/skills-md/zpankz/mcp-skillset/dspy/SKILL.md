---
name: dspy
description: "Build complex AI systems with declarative programming, optimize prompts automatically, create modular RAG systems and agents with DSPy - Stanford NLP's framework for systematic LM programming. Use when you need to build complex AI systems, program LMs declaratively, optimize prompts automatically, create modular AI pipelines, or build RAG systems and agents."
---

# DSPy: Declarative Language Model Programming

**Stanford NLP's framework for programming—not prompting—language models.**

## Quick Start

```python
import dspy

# 1. Configure
dspy.settings.configure(lm=dspy.OpenAI(model='gpt-4o-mini'))

# 2. Define Module
qa = dspy.ChainOfThought("question -> answer")

# 3. Run
response = qa(question="What is the capital of France?")
print(response.answer)
```

## Learning Path (DAG)

The DSPy framework follows a natural progression from core concepts through optimization to advanced applications. Use this directed acyclic graph to understand dependencies and navigate the skill components.

### Foundation Layer (Start Here)
1. **[Configuring Language Models](./core/configuring-language-models.md)**
   - Prerequisites: None
   - Next: Signatures, Modules, Datasets

2. **[Designing Signatures](./core/designing-signatures.md)**
   - Prerequisites: LM Configuration
   - Next: Modules, Optimization

3. **[Building Modules](./core/building-modules.md)**
   - Prerequisites: Signatures
   - Next: Optimization, Applications

4. **[Creating Datasets](./core/creating-datasets.md)**
   - Prerequisites: None
   - Next: Optimization

### Optimization Layer
5. **[Few-Shot Learning](./optimization/few-shot-learning.md)**
   - Prerequisites: Modules, Datasets
   - Techniques: LabeledFewShot, BootstrapFewShot, KNNFewShot
   - Next: Applications

6. **[Instruction Optimization](./optimization/instruction-optimization.md)**
   - Prerequisites: Modules, Datasets
   - Techniques: COPRO, MIPROv2, GEPA
   - Next: Applications

7. **[Finetuning Models](./optimization/finetuning-models.md)**
   - Prerequisites: Modules, Datasets
   - Techniques: BootstrapFinetune
   - Next: Applications

8. **[Ensemble Strategies](./optimization/ensemble-strategies.md)**
   - Prerequisites: Multiple trained modules
   - Next: Applications

### Application Layer
9. **[Building RAG Pipelines](./applications/building-rag-pipelines.md)**
   - Prerequisites: Modules, Optimization (recommended)

10. **[Evaluating Programs](./applications/evaluating-programs.md)**
    - Prerequisites: Modules, Datasets

11. **[Integrating Haystack](./applications/integrating-haystack.md)**
    - Prerequisites: Modules, Haystack knowledge

### Advanced Features (Cross-Cutting)
12. **[Assertions & Validation](./advanced/assertions-validation.md)**
    - Prerequisites: Modules

13. **[Typed Outputs](./advanced/typed-outputs.md)**
    - Prerequisites: Signatures

14. **[Multi-Chain Comparison](./advanced/multi-chain-comparison.md)**
    - Prerequisites: ChainOfThought module

## Reference Documentation

- **[Modules Reference](./references/modules-reference.md)** - Complete module catalog
- **[Optimizers Reference](./references/optimizers-reference.md)** - All optimization techniques
- **[Examples Reference](./references/examples-reference.md)** - Real-world implementations

## Common Workflows

### Workflow 1: Basic QA System
1. Configure LM → Design Signature → Build Module
2. Path: `configuring-language-models.md` → `designing-signatures.md` → `building-modules.md`

### Workflow 2: Optimized RAG System
1. Configure LM → Build RAG Module → Optimize with Few-Shot → Evaluate
2. Path: `configuring-language-models.md` → `building-rag-pipelines.md` → `few-shot-learning.md` → `evaluating-programs.md`

### Workflow 3: Production Agent
1. Configure LM → Design Signature → Build ReAct Module → Add Assertions → Optimize Instructions → Evaluate
2. Path: `configuring-language-models.md` → `designing-signatures.md` → `building-modules.md` → `assertions-validation.md` → `instruction-optimization.md` → `evaluating-programs.md`

## Installation

```bash
pip install dspy
# Or with specific providers
pip install dspy[anthropic]  # Claude
pip install dspy[openai]     # GPT
pip install dspy[all]        # All providers
```

## Additional Resources

- **Official Docs**: dspy.ai
- **GitHub**: github.com/stanfordnlp/dspy
