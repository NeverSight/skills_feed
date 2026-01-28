---
name: ai
description: >
  AI/ML development patterns and best practices.
  Trigger: When working with AI/ML development or model training.
license: Apache-2.0
metadata:
  author: poletron
  version: "1.0"
  scope: [root]
  auto_invoke: "Working with ai"

## When to Use

Use this skill when:
- Developing AI/ML models
- Working with machine learning pipelines
- Integrating AI services
- Processing ML data

---

## Critical Patterns

### Model Development (REQUIRED)

```python
# ✅ ALWAYS: Version your models and data
from datetime import datetime

model_config = {
    "version": "1.2.0",
    "trained_at": datetime.now().isoformat(),
    "dataset_hash": compute_hash(training_data),
    "hyperparameters": {...}
}
```

### Reproducibility (REQUIRED)

```python
# ✅ ALWAYS: Set seeds for reproducibility
import random
import numpy as np
import torch

def set_seed(seed: int = 42):
    random.seed(seed)
    np.random.seed(seed)
    torch.manual_seed(seed)
    if torch.cuda.is_available():
        torch.cuda.manual_seed_all(seed)
```

---

## Decision Tree

```
Need classification?       → Start with simple baseline
Need embeddings?           → Use pre-trained models
Need fine-tuning?          → Start with small learning rate
Need deployment?           → Consider ONNX export
Need monitoring?           → Track drift metrics
```

---

## Resources

- **ML Development**: [ml-development.md](ml-development.md)
- **Cognee Integration**: [cognee/](cognee/)
