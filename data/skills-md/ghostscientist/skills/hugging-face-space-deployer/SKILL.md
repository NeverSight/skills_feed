---
name: hugging-face-space-deployer
description: Create, configure, and deploy Hugging Face Spaces for showcasing ML models. Supports Gradio, Streamlit, and Docker SDKs with templates for common use cases like chat interfaces, image generation, and model comparisons.
---

# Hugging Face Space Deployer

A skill for AI engineers to create, configure, and deploy interactive ML demos on Hugging Face Spaces.

## CRITICAL: Pre-Deployment Checklist

**Before writing ANY code, gather this information about the model:**

### 1. Check Model Type (LoRA Adapter vs Full Model)

**Use the HF MCP tool to inspect the model files:**
```
hf-skills - Hub Repo Details (repo_ids: ["username/model"], repo_type: "model")
```

**Look for these indicators:**

| Files Present | Model Type | Action Required |
|---------------|------------|-----------------|
| `model.safetensors` or `pytorch_model.bin` | Full model | Load directly with `AutoModelForCausalLM` |
| `adapter_model.safetensors` + `adapter_config.json` | LoRA/PEFT adapter | Must load base model first, then apply adapter with `peft` |
| Only config files, no weights | Broken/incomplete | Ask user to verify |

**If adapter_config.json exists, check for `base_model_name_or_path` to identify the base model.**

### 2. Check Inference API Availability

Visit the model page on HF Hub and look for "Inference Providers" widget on the right side.

**Indicators that model HAS Inference API:**
- Inference widget visible on model page
- Model from known provider: `meta-llama`, `mistralai`, `HuggingFaceH4`, `google`, `stabilityai`, `Qwen`
- High download count (>10,000) with standard architecture

**Indicators that model DOES NOT have Inference API:**
- Personal namespace (e.g., `GhostScientist/my-model`)
- LoRA/PEFT adapter (adapters never have direct Inference API)
- Missing `pipeline_tag` in model metadata
- No inference widget on model page

### 3. Check Model Metadata

- Ensure `pipeline_tag` is set (e.g., `text-generation`)
- Add `conversational` tag for chat models

### 4. Determine Hardware Needs

| Model Size | Recommended Hardware |
|------------|---------------------|
| < 3B parameters | ZeroGPU (free) or CPU |
| 3B - 7B parameters | ZeroGPU or T4 |
| > 7B parameters | A10G or A100 |

### 5. Ask User If Unclear

**If you cannot determine the model type, ASK THE USER:**

> "I'm analyzing your model to determine the best deployment strategy. I found:
> - [what you found about files]
> - [what you found about inference API]
>
> Is this model:
> 1. A full model you trained/uploaded?
> 2. A LoRA/PEFT adapter on top of another model?
> 3. Something else?
>
> Also, would you prefer:
> A. Free deployment with ZeroGPU (may have queue times)
> B. Paid GPU for faster response (~$0.60/hr)"

## Hardware Options

| Hardware | Use Case | Cost |
|----------|----------|------|
| `cpu-basic` | Simple demos, Inference API apps | Free |
| `cpu-upgrade` | Faster CPU inference | ~$0.03/hr |
| **`zero-a10g`** | **Models needing GPU on-demand (recommended for most)** | **Free (with quota)** |
| `t4-small` | Small GPU models (<7B) | ~$0.60/hr |
| `t4-medium` | Medium GPU models | ~$0.90/hr |
| `a10g-small` | Large models (7B-13B) | ~$1.50/hr |
| `a10g-large` | Very large models (30B+) | ~$3.15/hr |
| `a100-large` | Largest models | ~$4.50/hr |

**ZeroGPU Note:** ZeroGPU (`zero-a10g`) provides free GPU access on-demand. The Space runs on CPU, and when a user triggers inference, a GPU is allocated temporarily (~60-120 seconds). **After deployment, you must manually set the runtime to "ZeroGPU" in Space Settings > Hardware.**

## Deployment Decision Tree

```
Analyze Model
│
├── Does it have adapter_config.json?
│   └── YES → It's a LoRA adapter
│       ├── Find base_model_name_or_path in adapter_config.json
│       └── Use Template 3 (LoRA + ZeroGPU)
│
├── Does it have model.safetensors or pytorch_model.bin?
│   └── YES → It's a full model
│       ├── Is it from a major provider with inference widget?
│       │   ├── YES → Use Inference API (Template 1)
│       │   └── NO → Use ZeroGPU (Template 2)
│
└── Neither found?
    └── ASK USER - model may be incomplete
```

## Dependencies

**For Inference API (cpu-basic, free):**
```
gradio>=5.0.0
huggingface_hub>=0.26.0
```

**For ZeroGPU full models (zero-a10g, free with quota):**
```
gradio>=5.0.0
torch
transformers
accelerate
spaces
```

**For ZeroGPU LoRA adapters (zero-a10g, free with quota):**
```
gradio>=5.0.0
torch
transformers
accelerate
spaces
peft
```

## CLI Commands (CORRECT Syntax)

```bash
# Create Space
hf repo create my-space-name --repo-type space --space-sdk gradio

# Upload files
hf upload username/space-name ./local-folder --repo-type space

# Download model files to inspect
hf download username/model-name --local-dir ./model-check --dry-run

# Check what files exist in a model
hf download username/model-name --local-dir /tmp/check --dry-run 2>&1 | grep -E '\.(safetensors|bin|json)'
```

## Template 1: Inference API (For Supported Models)

**Use when:** Model has inference widget, is from major provider, or explicitly supports serverless API.

```python
import gradio as gr
from huggingface_hub import InferenceClient

MODEL_ID = "HuggingFaceH4/zephyr-7b-beta"  # Must support Inference API!
client = InferenceClient(MODEL_ID)

def respond(message, history, system_message, max_tokens, temperature, top_p):
    messages = [{"role": "system", "content": system_message}]

    for user_msg, assistant_msg in history:
        if user_msg:
            messages.append({"role": "user", "content": user_msg})
        if assistant_msg:
            messages.append({"role": "assistant", "content": assistant_msg})

    messages.append({"role": "user", "content": message})

    response = ""
    for token in client.chat_completion(
        messages,
        max_tokens=max_tokens,
        stream=True,
        temperature=temperature,
        top_p=top_p,
    ):
        delta = token.choices[0].delta.content or ""
        response += delta
        yield response

demo = gr.ChatInterface(
    respond,
    title="Chat Assistant",
    description="Powered by Hugging Face Inference API",
    additional_inputs=[
        gr.Textbox(value="You are a helpful assistant.", label="System message"),
        gr.Slider(minimum=1, maximum=2048, value=512, step=1, label="Max tokens"),
        gr.Slider(minimum=0.1, maximum=2.0, value=0.7, step=0.1, label="Temperature"),
        gr.Slider(minimum=0.1, maximum=1.0, value=0.95, step=0.05, label="Top-p"),
    ],
    examples=[
        ["Hello! How are you?"],
        ["Write a Python function to sort a list"],
    ],
)

if __name__ == "__main__":
    demo.launch()
```

**requirements.txt:**
```
gradio>=5.0.0
huggingface_hub>=0.26.0
```

**README.md:**
```yaml
---
title: My Chat App
emoji: 💬
colorFrom: blue
colorTo: purple
sdk: gradio
sdk_version: 5.9.1
app_file: app.py
pinned: false
license: apache-2.0
---
```

## Template 2: ZeroGPU Full Model (For Models Without Inference API)

**Use when:** Full model (has model.safetensors) but no Inference API support.

```python
import gradio as gr
import spaces
import torch
from transformers import AutoModelForCausalLM, AutoTokenizer

MODEL_ID = "username/my-full-model"

# Load tokenizer at startup
tokenizer = AutoTokenizer.from_pretrained(MODEL_ID)

# Global model - loaded lazily on first GPU call for faster Space startup
model = None

def load_model():
    global model
    if model is None:
        model = AutoModelForCausalLM.from_pretrained(
            MODEL_ID,
            torch_dtype=torch.float16,
            device_map="auto",
        )
    return model

@spaces.GPU(duration=120)
def generate_response(message, history, system_message, max_tokens, temperature, top_p):
    model = load_model()

    messages = [{"role": "system", "content": system_message}]

    for user_msg, assistant_msg in history:
        if user_msg:
            messages.append({"role": "user", "content": user_msg})
        if assistant_msg:
            messages.append({"role": "assistant", "content": assistant_msg})

    messages.append({"role": "user", "content": message})

    text = tokenizer.apply_chat_template(
        messages,
        tokenize=False,
        add_generation_prompt=True
    )
    inputs = tokenizer([text], return_tensors="pt").to(model.device)

    with torch.no_grad():
        outputs = model.generate(
            **inputs,
            max_new_tokens=int(max_tokens),
            temperature=float(temperature),
            top_p=float(top_p),
            do_sample=True,
            pad_token_id=tokenizer.eos_token_id,
        )

    response = tokenizer.decode(
        outputs[0][inputs['input_ids'].shape[1]:],
        skip_special_tokens=True
    )
    return response

demo = gr.ChatInterface(
    generate_response,
    title="My Model",
    description="Powered by ZeroGPU (free!)",
    additional_inputs=[
        gr.Textbox(value="You are a helpful assistant.", label="System message", lines=2),
        gr.Slider(minimum=64, maximum=2048, value=512, step=64, label="Max tokens"),
        gr.Slider(minimum=0.1, maximum=1.5, value=0.7, step=0.1, label="Temperature"),
        gr.Slider(minimum=0.1, maximum=1.0, value=0.95, step=0.05, label="Top-p"),
    ],
    examples=[
        ["Hello! How are you?"],
        ["Help me write some code"],
    ],
)

if __name__ == "__main__":
    demo.launch()
```

**requirements.txt:**
```
gradio>=5.0.0
torch
transformers
accelerate
spaces
```

**README.md:**
```yaml
---
title: My Model
emoji: 🤖
colorFrom: blue
colorTo: purple
sdk: gradio
sdk_version: 5.9.1
app_file: app.py
pinned: false
license: apache-2.0
suggested_hardware: zero-a10g
---
```

## Template 3: ZeroGPU LoRA Adapter (CRITICAL FOR FINE-TUNED MODELS)

**Use when:** Model has `adapter_config.json` and `adapter_model.safetensors` (NOT `model.safetensors`)

**You MUST identify the base model from `adapter_config.json` field `base_model_name_or_path`**

```python
import gradio as gr
import spaces
import torch
from transformers import AutoModelForCausalLM, AutoTokenizer
from peft import PeftModel

# Your LoRA adapter
ADAPTER_ID = "username/my-lora-adapter"
# Base model (from adapter_config.json -> base_model_name_or_path)
BASE_MODEL_ID = "Qwen/Qwen2.5-Coder-1.5B-Instruct"

# Load tokenizer at startup
tokenizer = AutoTokenizer.from_pretrained(BASE_MODEL_ID)

# Global model - loaded lazily on first GPU call
model = None

def load_model():
    global model
    if model is None:
        base_model = AutoModelForCausalLM.from_pretrained(
            BASE_MODEL_ID,
            torch_dtype=torch.float16,
            device_map="auto",
        )
        model = PeftModel.from_pretrained(base_model, ADAPTER_ID)
        model = model.merge_and_unload()  # Merge for faster inference
    return model

@spaces.GPU(duration=120)
def generate_response(message, history, system_message, max_tokens, temperature, top_p):
    model = load_model()

    messages = [{"role": "system", "content": system_message}]

    for item in history:
        if isinstance(item, (list, tuple)) and len(item) == 2:
            user_msg, assistant_msg = item
            if user_msg:
                messages.append({"role": "user", "content": user_msg})
            if assistant_msg:
                messages.append({"role": "assistant", "content": assistant_msg})

    messages.append({"role": "user", "content": message})

    text = tokenizer.apply_chat_template(
        messages,
        tokenize=False,
        add_generation_prompt=True
    )
    inputs = tokenizer([text], return_tensors="pt").to(model.device)

    with torch.no_grad():
        outputs = model.generate(
            **inputs,
            max_new_tokens=int(max_tokens),
            temperature=float(temperature),
            top_p=float(top_p),
            do_sample=True,
            pad_token_id=tokenizer.eos_token_id,
        )

    response = tokenizer.decode(
        outputs[0][inputs['input_ids'].shape[1]:],
        skip_special_tokens=True
    )
    return response

demo = gr.ChatInterface(
    generate_response,
    title="My Fine-Tuned Model",
    description="LoRA fine-tuned model powered by ZeroGPU (free!)",
    additional_inputs=[
        gr.Textbox(value="You are a helpful assistant.", label="System message", lines=2),
        gr.Slider(minimum=64, maximum=2048, value=512, step=64, label="Max tokens"),
        gr.Slider(minimum=0.1, maximum=1.5, value=0.7, step=0.1, label="Temperature"),
        gr.Slider(minimum=0.1, maximum=1.0, value=0.95, step=0.05, label="Top-p"),
    ],
    examples=[
        ["Hello! How are you?"],
        ["Help me with a coding task"],
    ],
)

if __name__ == "__main__":
    demo.launch()
```

**requirements.txt (MUST include peft):**
```
gradio>=5.0.0
torch
transformers
accelerate
spaces
peft
```

**README.md:**
```yaml
---
title: My Fine-Tuned Model
emoji: 🔧
colorFrom: green
colorTo: blue
sdk: gradio
sdk_version: 5.9.1
app_file: app.py
pinned: false
license: apache-2.0
suggested_hardware: zero-a10g
---
```

## Post-Deployment Steps

**After uploading your Space files:**

### 1. Set the Runtime Hardware (REQUIRED for GPU models)

- Go to: `https://huggingface.co/spaces/USERNAME/SPACE_NAME/settings`
- Under "Space Hardware", select the appropriate option:
  - **ZeroGPU** for free on-demand GPU (recommended)
  - Or a dedicated GPU tier if needed

### 2. Verify the Space is Running

- Check the Space URL for any build errors
- Review container logs in Settings if issues occur

### 3. Common Post-Deploy Fixes

| Issue | Cause | Fix |
|-------|-------|-----|
| "No API found" error | Hardware mismatch | Set runtime to ZeroGPU in Settings |
| Model not loading | LoRA vs full model confusion | Check if it's an adapter, use correct template |
| Inference API errors | Model not on serverless | Load directly with transformers instead |

## Detecting Model Type - Quick Reference

### Full Model
Files include: `model.safetensors`, `pytorch_model.bin`, or sharded versions
```python
# Can load directly
model = AutoModelForCausalLM.from_pretrained("username/model")
```

### LoRA/PEFT Adapter
Files include: `adapter_config.json`, `adapter_model.safetensors`
```python
# Must load base model first, then apply adapter
base_model = AutoModelForCausalLM.from_pretrained("base-model-id")
model = PeftModel.from_pretrained(base_model, "username/adapter")
model = model.merge_and_unload()  # Optional: merge for faster inference
```

### Inference API Available
Model page shows "Inference Providers" widget on the right side
```python
# Can use InferenceClient (simplest approach)
from huggingface_hub import InferenceClient
client = InferenceClient("username/model")
```

## Fixing Missing pipeline_tag (To Enable Inference API)

If a model doesn't have an inference widget but should, it may be missing metadata:

```bash
# Download the README
hf download username/model-name README.md --local-dir /tmp/fix

# Edit to add pipeline_tag in YAML frontmatter:
# ---
# pipeline_tag: text-generation
# tags:
# - conversational
# ---

# Upload the fix
hf upload username/model-name /tmp/fix/README.md README.md
```

**Note:** Even with correct tags, custom models may not get Inference API - it depends on HF's infrastructure decisions.

## CRITICAL: Gradio 5.x Requirements

### Examples Format (MUST be nested lists)
```python
# CORRECT:
examples=[
    ["Example 1"],
    ["Example 2"],
]

# WRONG (causes ValueError):
examples=[
    "Example 1",
    "Example 2",
]
```

### Version Requirements
```
gradio>=5.0.0
huggingface_hub>=0.26.0
```

Do NOT use `gradio==4.44.0` - causes `ImportError: cannot import name 'HfFolder'`

## Troubleshooting

### "No API found" Error
**Cause:** Gradio app isn't exposing API correctly, often due to hardware mismatch
**Fix:** Go to Space Settings and set runtime to "ZeroGPU" or appropriate GPU tier

### "OSError: does not appear to have a file named pytorch_model.bin, model.safetensors"
**Cause:** Trying to load a LoRA adapter as a full model
**Fix:** Check for `adapter_config.json` - if present, use PEFT to load:
```python
from peft import PeftModel
base_model = AutoModelForCausalLM.from_pretrained("base-model")
model = PeftModel.from_pretrained(base_model, "adapter-id")
```

### Inference API Not Available
**Cause:** Model doesn't have pipeline_tag or isn't deployed to serverless
**Fix:** Either:
  a. Add `pipeline_tag: text-generation` to model's README.md
  b. Or load model directly with transformers instead of InferenceClient

### `ImportError: cannot import name 'HfFolder'`
**Cause:** gradio/huggingface_hub version mismatch
**Fix:** Use `gradio>=5.0.0` and `huggingface_hub>=0.26.0`

### `ValueError: examples must be nested list`
**Cause:** Gradio 5.x format change
**Fix:** Use `[["ex1"], ["ex2"]]` not `["ex1", "ex2"]`

### Space builds but model doesn't load
**Cause:** Missing `peft` for adapters, or wrong base model
**Fix:** Check adapter_config.json for correct base_model_name_or_path

## Workflow Summary

1. **Analyze model** (check for adapter_config.json, model files, inference widget)
2. **Determine strategy** (Inference API vs ZeroGPU, full model vs LoRA)
3. **Ask user if unclear** about model type or cost preferences
4. **Generate correct template** based on analysis
5. **Create Space** with correct requirements and README
6. **Upload files** using `hf upload`
7. **Set hardware** in Space Settings (ZeroGPU for free GPU access)
8. **Monitor build logs** for any issues
