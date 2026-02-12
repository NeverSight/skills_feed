---
name: marimo-batch
description: An opintionated skill to prepare a marimo notebook to make it ready for a scheduled run.
---

Pydantic is a great way to declare a source of truth for a batch job, especially for ML. You can declare something like: 

```python
from pydantic import BaseModel, Field

class ModelParams(BaseModel):
    sample_size: int = Field(
        default=1024 * 4, description="Number of training samples per epoch."
    )
    learning_rate: float = Field(default=0.01, description="Learning rate for the optimizer.")
```

You can fill these model params with two methods too, you can imagine a form in the UI. 

```python
el = mo.md("""
{sample_size} 
{learning_rate}
""").batch(
    sample_size=mo.ui.slider(1024, 1024 * 10, value=1024 * 4, step=1024, label="Sample size"),
    learning_rate=mo.ui.slider(0.001, 0.1, value=0.01, step=0.001, label="Learning rate"),
).form()
el
```

But you can also use the CLI from marimo. 

```python
if mo.app_meta().mode == "script":
    model_params = ModelParams(
        **{k.replace("-", "_"): v for k, v in mo.cli_args().items()
    })
else: 
    model_params = ModelParams(**el.value)
```

The user can now run this from the command line via: 

```bash
uv run notebook.py --sample-size 4096 --learning-rate 0.005
```

This is the best of both worlds, you can use the UI to test and iterate, and then use the CLI to run the batch job.

The user wants to be able to run a notebook using this pattern, so make sure you ask the user which parameters they want to make configurable via the CLI and the proceed to make the changes to the notebook. Make sure you verify the changes with the user before making them. 

## Weights and Biases

It is possible that the user is interested in adding support for weights and biases. If that is the case, make sure these ModelParams are logged. 