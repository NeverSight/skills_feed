---
name: replicate-cli
description: This skill provides comprehensive guidance for using the Replicate CLI to run AI models, create predictions, manage deployments, and fine-tune models. Use this skill when the user wants to interact with Replicate's AI model platform via command line, including running image generation models, language models, or any ML model hosted on Replicate. This skill should be used when users ask about running models on Replicate, creating predictions, managing deployments, fine-tuning models, or working with the Replicate API through the CLI.
---

# Replicate CLI

The Replicate CLI is a command-line tool for interacting with Replicate's AI model platform. It enables running predictions, managing models, creating deployments, and fine-tuning models directly from the terminal.

## Authentication

Before using the Replicate CLI, set the API token:

```bash
export REPLICATE_API_TOKEN=<token-from-replicate.com/account>
```

Alternatively, authenticate interactively:

```bash
replicate auth login
```

Verify authentication:

```bash
replicate account current
```

## Core Commands

### Running Predictions

The primary use case is running predictions against hosted models.

**Basic prediction:**
```bash
replicate run <owner/model> input_key=value
```

**Examples:**

Image generation:
```bash
replicate run stability-ai/sdxl prompt="a studio photo of a rainbow colored corgi"
```

Text generation with streaming:
```bash
replicate run meta/llama-2-70b-chat --stream prompt="Tell me a joke"
```

**Prediction flags:**
- `--stream` - Stream output tokens in real-time (for text models)
- `--no-wait` - Submit prediction without waiting for completion
- `--web` - Open prediction in browser
- `--json` - Output result as JSON
- `--save` - Save outputs to local directory
- `--output-directory <dir>` - Specify output directory (default: `./{prediction-id}`)

### Input Handling

**File uploads:** Prefix local file paths with `@`:
```bash
replicate run nightmareai/real-esrgan image=@photo.jpg
```

**Output chaining:** Use `{{.output}}` template syntax to chain predictions:
```bash
replicate run stability-ai/sdxl prompt="a corgi" | \
replicate run nightmareai/real-esrgan image={{.output[0]}}
```

### Model Operations

**View model schema** (see required inputs and outputs):
```bash
replicate model schema <owner/model>
replicate model schema stability-ai/sdxl --json
```

**List models:**
```bash
replicate model list
replicate model list --json
```

**Show model details:**
```bash
replicate model show <owner/model>
```

**Create a new model:**
```bash
replicate model create <owner/name> \
  --hardware gpu-a100-large \
  --private \
  --description "Model description"
```

Model creation flags:
- `--hardware <sku>` - Hardware SKU (see `references/hardware.md`)
- `--private` / `--public` - Visibility setting
- `--description <text>` - Model description
- `--github-url <url>` - Link to source repository
- `--license-url <url>` - License information
- `--cover-image-url <url>` - Cover image for model page

### Training (Fine-tuning)

Fine-tune models using the training command:

```bash
replicate train <base-model> \
  --destination <owner/new-model> \
  input_key=value
```

**Example - Fine-tune SDXL with DreamBooth:**
```bash
replicate train stability-ai/sdxl \
  --destination myuser/custom-sdxl \
  --web \
  input_images=@training-images.zip \
  use_face_detection_instead=true
```

**List trainings:**
```bash
replicate training list
```

**Show training details:**
```bash
replicate training show <training-id>
```

### Deployments

Deployments provide dedicated, always-on inference endpoints with predictable performance.

**Create deployment:**
```bash
replicate deployments create <name> \
  --model <owner/model> \
  --hardware <sku> \
  --min-instances 1 \
  --max-instances 3
```

**Example:**
```bash
replicate deployments create text-to-image \
  --model stability-ai/sdxl \
  --hardware gpu-a100-large \
  --min-instances 1 \
  --max-instances 5
```

**Update deployment:**
```bash
replicate deployments update <name> \
  --max-instances 10 \
  --version <version-id>
```

**List deployments:**
```bash
replicate deployments list
```

**Show deployment details and schema:**
```bash
replicate deployments show <name>
replicate deployments schema <name>
```

### Hardware

List available hardware options:
```bash
replicate hardware list
```

See `references/hardware.md` for detailed hardware information and selection guidelines.

### Scaffolding

Create a local development environment from an existing prediction:

```bash
replicate scaffold <prediction-id-or-url> --template=<node|python>
```

This generates a project with the prediction's model and inputs pre-configured.

## Command Aliases

For convenience, these aliases are available:

| Alias | Equivalent Command |
|-------|-------------------|
| `replicate run` | `replicate prediction create` |
| `replicate stream` | `replicate prediction create --stream` |
| `replicate train` | `replicate training create` |

Short aliases for subcommands:
- `replicate m` = `replicate model`
- `replicate p` = `replicate prediction`
- `replicate t` = `replicate training`
- `replicate d` = `replicate deployments`
- `replicate hw` = `replicate hardware`
- `replicate a` = `replicate account`

## Common Workflows

### Image Generation Pipeline

Generate an image and upscale it:
```bash
replicate run stability-ai/sdxl \
  prompt="professional photo of a sunset" \
  negative_prompt="blurry, low quality" | \
replicate run nightmareai/real-esrgan \
  image={{.output[0]}} \
  --save
```

### Check Model Inputs Before Running

Always check the model schema to understand required inputs:
```bash
replicate model schema owner/model-name
```

### Batch Processing

Run predictions and save outputs:
```bash
for prompt in "cat" "dog" "bird"; do
  replicate run stability-ai/sdxl prompt="$prompt" --save --output-directory "./outputs/$prompt"
done
```

### Monitor Long-Running Tasks

Submit without waiting, then check status:
```bash
# Submit
replicate run owner/model input=value --no-wait --json > prediction.json

# Check status later
replicate prediction show $(jq -r '.id' prediction.json)
```

## Best Practices

1. **Always check schema first** - Run `replicate model schema <model>` to understand required and optional inputs before running predictions.

2. **Use streaming for text models** - Add `--stream` flag when running language models to see output in real-time.

3. **Save outputs explicitly** - Use `--save` and `--output-directory` to organize prediction outputs.

4. **Use JSON output for automation** - Add `--json` flag when parsing outputs programmatically.

5. **Open in web for debugging** - Add `--web` flag to view predictions in the Replicate dashboard for detailed logs.

6. **Chain predictions efficiently** - Use the `{{.output}}` syntax to pass outputs between models without intermediate saves.

## Troubleshooting

**Authentication errors:**
- Verify `REPLICATE_API_TOKEN` is set correctly
- Run `replicate account current` to test authentication

**Model not found:**
- Check model name format: `owner/model-name`
- Verify model exists at replicate.com

**Input validation errors:**
- Run `replicate model schema <model>` to see required inputs
- Check input types (string, number, file)

**File upload issues:**
- Ensure `@` prefix is used for local files
- Verify file path is correct and file exists

## Additional Resources

- Replicate documentation: https://replicate.com/docs
- Model explorer: https://replicate.com/explore
- API reference: https://replicate.com/docs/reference/http
- GitHub repository: https://github.com/replicate/cli
