---
name: novita-docs
description: Complete reference documentation for Novita AI platform. Use when user asks about Novita AI products, APIs, pricing, integrations, GPU instances, model catalogs, sandbox environments, or design system.
---

# Novita AI Platform Reference

Complete documentation for the Novita AI platform - an AI & Agent Cloud for developers.

## When to Use This Skill

Load this skill when the user asks about:
- **Novita AI products**: Model APIs, GPU instances, serverless GPUs, agent sandbox
- **Model information**: "What models does Novita support?", model pricing, capabilities
- **API guidance**: How to use APIs, authentication, endpoints, parameters
- **Pricing and billing**: Cost estimates, billing queries, payment methods
- **Integrations**: LangChain, LlamaIndex, Cursor, and 30+ other tools
- **Design system**: Colors, typography, buttons, navigation, icons, logo
- **Getting started**: Quickstart guides, FAQs, setup instructions
- **Troubleshooting**: Error codes, common issues, support

## Quick Reference

| Resource | URL |
|----------|-----|
| **Website** | https://novita.ai |
| **Model Catalog** | https://novita.ai/models (200+ models) |
| **Documentation** | https://novita.ai/docs |
| **Pricing** | https://novita.ai/pricing |
| **Console** | https://novita.ai/console |
| **API Base URL** | `https://api.novita.ai/openai` |
| **Support** | support@novita.ai |
| **Discord** | https://discord.gg/YyPRAzwp7P |

---

## 🔍 Quick: Query Available Models

**Most common question**: "What models does Novita support?"

### Query Methods

**1. Web Catalog** (human-friendly):
   - Browse 200+ models at https://novita.ai/models
   - Filter by type: LLM, image, video, audio, embeddings

**2. API Endpoint** (automation):
   ```bash
   curl https://api.novita.ai/openai/v1/models \
     -H "Authorization: Bearer <YOUR_API_KEY>"
   ```
   Returns: Model ID, pricing per million tokens, context size, description

### Model Categories

- **LLMs**: 100+ models (Llama, Qwen, DeepSeek, Mistral, etc.)
- **Image Generation**: Flux, Stable Diffusion, SDXL
- **Video**: Wan 2.6, CogVideoX
- **Audio**: TTS, voice cloning
- **Embeddings**: Text embedding models

### Quick Links

| Task | Reference |
|------|-----------|
| List all models via API | [list-models.md](references/api-reference/llm/list-models.md) |
| Get specific model info | [retrieve-model.md](references/api-reference/llm/retrieve-model.md) |
| Recommended LLMs | [llm/recommended.md](references/llm/recommended.md) |
| Image model APIs | [api-reference/image-apis/](references/api-reference/image-apis/) |
| Model API guides | [model-apis/](references/model-apis/) |

**Pro Tip**: Always call `/v1/models` API first for the latest model list and current pricing.

---

## How to Use This Documentation

### 1. Start Here
- **New users**: See [getting-started/](references/getting-started/) - company overview, quickstart, FAQ
- **Model queries**: Check the "Quick: Query Available Models" section above
- **API help**: Jump to specific API reference sections below

### 2. Find Documentation by Category

**Product Guides** (usage and features):
- [getting-started/](references/getting-started/) - Overview, quickstart, product pages
- [llm/](references/llm/) - LLM API guides (16 files)
- [model-apis/](references/model-apis/) - Model API guides (11 files)
- [gpu-instance/](references/gpu-instance/) - GPU instances (14 files)
- [serverless-gpus/](references/serverless-gpus/) - Serverless GPUs (6 files)
- [sandbox/](references/sandbox/) - Agent Sandbox (43 files)
- [integrations/](references/integrations/) - 30+ integration guides

**API Reference** (endpoints and parameters):
- [api-reference/basic/](references/api-reference/basic/) - Auth, billing (6 files)
- [api-reference/llm/](references/api-reference/llm/) - LLM endpoints (16 files)
- [api-reference/image-apis/](references/api-reference/image-apis/) - Image/video APIs (48 files)
- [api-reference/gpu-instance/](references/api-reference/gpu-instance/) - GPU APIs (2 files)

**Support**:
- [billing/](references/billing/) - Billing and payments (4 files)
- [team/](references/team/) - Team management (1 file)

**Design System**:
- [design-system/](references/design-system/) - UI/UX specs (7 files)

### 3. File Naming Convention

Files are organized by category:
```
references/
├── getting-started/          # Product overviews and quickstart
├── llm/                      # LLM feature guides
├── model-apis/               # Model API guides
├── gpu-instance/             # GPU instance guides
├── serverless-gpus/          # Serverless GPU guides
├── sandbox/                  # Agent Sandbox docs (with subdirs)
├── integrations/             # Third-party tool integrations
├── api-reference/            # API endpoint documentation
│   ├── basic/               # Auth, billing APIs
│   ├── llm/                 # LLM API endpoints
│   ├── image-apis/          # Image/video API endpoints
│   └── gpu-instance/        # GPU instance APIs
├── billing/                  # Billing and payment
├── team/                     # Team management
└── design-system/            # UI/UX design specs
```

---

## 📚 Documentation Index

### Core Product Documentation

**Getting Started** (8 files)
- [company-overview.md](references/getting-started/company-overview.md) - Company overview, products, testimonials
- [gpus.md](references/getting-started/gpus.md) - GPU Cloud product overview
- [sandbox.md](references/getting-started/sandbox.md) - Agent Sandbox product overview
- [gpu-baremetal.md](references/getting-started/gpu-baremetal.md) - Bare metal GPU servers
- [introduction.md](references/getting-started/introduction.md) - Platform introduction
- [quickstart.md](references/getting-started/quickstart.md) - Quick start guide
- [faq.md](references/getting-started/faq.md) - Frequently asked questions
- [error-handling.md](references/getting-started/error-handling.md) - Error handling

**LLM Guides** (17 files)
Core: [api](references/llm/api.md) · [batch-api](references/llm/batch-api.md) · [function-calling](references/llm/function-calling.md) · [vision](references/llm/vision.md) · [reasoning](references/llm/reasoning.md) · [structured-outputs](references/llm/structured-outputs.md) · [prompt-cache](references/llm/prompt-cache.md) · [rate-limits](references/llm/rate-limits.md) · [monitoring](references/llm/monitoring.md) · [observability-metrics](references/llm/observability-metrics.md) · [dedicated-endpoint](references/llm/dedicated-endpoint.md) · [playgrounds](references/llm/playgrounds.md) · [recommended](references/llm/recommended.md)

**Model APIs** (11 files)
[overview](references/model-apis/overview.md) · [sdks](references/model-apis/sdks.md) · [dedicated-endpoints](references/model-apis/dedicated-endpoints.md) · [training-guidance](references/model-apis/training-guidance.md) · [custom-model](references/model-apis/custom-model.md) · [sampler](references/model-apis/sampler.md) · [vae](references/model-apis/vae.md) · [clip-skip](references/model-apis/clip-skip.md) · [rate-limits](references/model-apis/rate-limits.md) · [v2-to-v3-migration](references/model-apis/v2-to-v3-migration.md) · [configure-custom-s3-bucket](references/model-apis/configure-custom-s3-bucket.md)

**GPU Instance** (14 files)
[overview](references/gpu-instance/overview.md) · [overview-guide](references/gpu-instance/overview-guide.md) · [choose-a-gpu](references/gpu-instance/choose-a-gpu.md) · [pricing](references/gpu-instance/pricing.md) · [quickstart-*](references/gpu-instance/quickstart-preparations.md) (5 files) · [jupyterlab](references/gpu-instance/jupyterlab.md) · [save-image](references/gpu-instance/save-image.md) · [upgrade-instance](references/gpu-instance/upgrade-instance.md) · [edit-instance](references/gpu-instance/edit-instance.md) · [image-prewarm](references/gpu-instance/image-prewarm.md)

**Serverless GPUs** (6 files)
[overview](references/serverless-gpus/overview.md) · [pricing](references/serverless-gpus/pricing.md) · [quickstart-*](references/serverless-gpus/quickstart-preparations.md) (4 files)

**Agent Sandbox** (43 files organized in subdirectories)
Core: [overview](references/sandbox/overview.md) · [pricing](references/sandbox/pricing.md) · [sdk-and-cli](references/sandbox/sdk-and-cli.md)

Quickstart: [your-first-sandbox](references/sandbox/quickstart/your-first-sandbox.md) · [introduction](references/sandbox/quickstart/introduction.md) · [installation](references/sandbox/quickstart/installation.md) · [quick-start](references/sandbox/quickstart/quick-start.md) · [frameworks](references/sandbox/quickstart/frameworks.md) · [advanced](references/sandbox/quickstart/advanced.md)

CLI: [overview](references/sandbox/cli/overview.md) · [auth](references/sandbox/cli/auth.md) · [spawn](references/sandbox/cli/spawn.md) · [list](references/sandbox/cli/list.md) · [shutdown](references/sandbox/cli/shutdown.md)

Commands: [overview](references/sandbox/commands/overview.md) · [background](references/sandbox/commands/background.md) · [streaming](references/sandbox/commands/streaming.md)

Filesystem: [overview](references/sandbox/filesystem/overview.md) · [read-write](references/sandbox/filesystem/read-write.md) · [upload](references/sandbox/filesystem/upload.md) · [download](references/sandbox/filesystem/download.md) · [watch](references/sandbox/filesystem/watch.md)

Lifecycle: [overview](references/sandbox/lifecycle/overview.md) · [clone](references/sandbox/lifecycle/clone.md) · [list](references/sandbox/lifecycle/list.md) · [idle-timeout](references/sandbox/lifecycle/idle-timeout.md)

Template: [overview](references/sandbox/template/overview.md) · [customize-cpu-ram](references/sandbox/template/customize-cpu-ram.md) · [start-cmd](references/sandbox/template/start-cmd.md) · [ready-cmd](references/sandbox/template/ready-cmd.md) · [version-management](references/sandbox/template/version-management.md)

More: [console](references/sandbox/console.md) · [connect](references/sandbox/connect.md) · [internet-access](references/sandbox/internet-access.md) · [environment-variables](references/sandbox/environment-variables.md) · [metadata](references/sandbox/metadata.md) · [metrics](references/sandbox/metrics.md) · [mount-cloudstorage](references/sandbox/mount-cloudstorage.md)

**Integrations** (30 tools)
[langchain](references/integrations/langchain.md) · [llamaindex](references/integrations/llamaindex.md) · [huggingface](references/integrations/huggingface.md) · [cursor](references/integrations/cursor.md) · [dify](references/integrations/dify.md) · [browseruse](references/integrations/browseruse.md) · [skyvern](references/integrations/skyvern.md) · [gradio](references/integrations/gradio.md) · [anythingllm](references/integrations/anythingllm.md) · [axolotl](references/integrations/axolotl.md) · [chatbox](references/integrations/chatbox.md) · [claude-code](references/integrations/claude-code.md) · [codecompanion](references/integrations/codecompanion.md) · [continue](references/integrations/continue.md) · [deepsearcher](references/integrations/deepsearcher.md) · [docsgpt](references/integrations/docsgpt.md) · [helicone](references/integrations/helicone.md) · [kohya-ss-gui](references/integrations/kohya-ss-gui.md) · [langflow](references/integrations/langflow.md) · [langfuse](references/integrations/langfuse.md) · [litellm](references/integrations/litellm.md) · [lobechat](references/integrations/lobechat.md) · [lollms-webui](references/integrations/lollms-webui.md) · [openai-agents-sdk](references/integrations/openai-agents-sdk.md) · [owl](references/integrations/owl.md) · [pageassist](references/integrations/pageassist.md) · [portkey](references/integrations/portkey.md) · [verba](references/integrations/verba.md)

### API Reference

**Basic APIs** (6 files)
[authentication](references/api-reference/basic/authentication.md) · [error-code](references/api-reference/basic/error-code.md) · [get-user-balance](references/api-reference/basic/get-user-balance.md) · [query-*-billing](references/api-reference/basic/) (3 files)

**LLM APIs** (16 files)
[list-models](references/api-reference/llm/list-models.md) · [retrieve-model](references/api-reference/llm/retrieve-model.md) · [create-chat-completion](references/api-reference/llm/create-chat-completion.md) · [create-completion](references/api-reference/llm/create-completion.md) · [create-embeddings](references/api-reference/llm/create-embeddings.md) · [create-rerank](references/api-reference/llm/create-rerank.md) · [create-batch](references/api-reference/llm/create-batch.md) · [cancel-batch](references/api-reference/llm/cancel-batch.md) · [list-batches](references/api-reference/llm/list-batches.md) · [retrieve-batch](references/api-reference/llm/retrieve-batch.md) · [list-files](references/api-reference/llm/list-files.md) · [upload-batch-input-file](references/api-reference/llm/upload-batch-input-file.md) · [query-file](references/api-reference/llm/query-file.md) · [retrieve-file-content](references/api-reference/llm/retrieve-file-content.md) · [delete-file](references/api-reference/llm/delete-file.md)

**Image/Video APIs** (54 files)
[introduction](references/api-reference/image-apis/introduction.md)

Core APIs: [txt2img](references/api-reference/image-apis/txt2img.md) · [img2img](references/api-reference/image-apis/img2img.md) · [inpainting](references/api-reference/image-apis/inpainting.md) · [upscale](references/api-reference/image-apis/upscale.md) · [image-upscaler](references/api-reference/image-apis/image-upscaler.md) · [remove-background](references/api-reference/image-apis/remove-background.md) · [image-to-prompt](references/api-reference/image-apis/image-to-prompt.md) · [eraser](references/api-reference/image-apis/eraser.md) · [remove-text](references/api-reference/image-apis/remove-text.md) · [replace-background](references/api-reference/image-apis/replace-background.md) · [merge-face](references/api-reference/image-apis/merge-face.md) · [reimagine](references/api-reference/image-apis/reimagine.md) · [video-merge-face](references/api-reference/image-apis/video-merge-face.md) · [task-result](references/api-reference/image-apis/task-result.md)

Flux Models: [flux-1-schnell](references/api-reference/image-apis/flux-1-schnell.md) · [flux-1-kontext-dev](references/api-reference/image-apis/flux-1-kontext-dev.md) · [flux-1-kontext-max](references/api-reference/image-apis/flux-1-kontext-max.md) · [flux-1-kontext-pro](references/api-reference/image-apis/flux-1-kontext-pro.md) · [flux-2-dev](references/api-reference/image-apis/flux-2-dev.md) · [flux-2-flex](references/api-reference/image-apis/flux-2-flex.md) · [flux-2-pro](references/api-reference/image-apis/flux-2-pro.md)

Other Models: [seedream-*](references/api-reference/image-apis/seedream-3-0.md) (3) · [glm-image](references/api-reference/image-apis/glm-image.md) · [hunyuan-image-3](references/api-reference/image-apis/hunyuan-image-3.md) · [qwen-*](references/api-reference/image-apis/qwen-txt2img.md) (2) · [z-image-turbo](references/api-reference/image-apis/z-image-turbo.md) · [z-image-turbo-lora](references/api-reference/image-apis/z-image-turbo-lora.md)

Training: [create-style-training](references/api-reference/image-apis/create-style-training.md) · [create-subject-training](references/api-reference/image-apis/create-subject-training.md) · [list-training-task](references/api-reference/image-apis/list-training-task.md) · [get-training-images-url](references/api-reference/image-apis/get-training-images-url.md)

Other: [glm-tts-voice-clone](references/api-reference/image-apis/glm-tts-voice-clone.md) · [webhook](references/api-reference/image-apis/webhook.md)

**GPU Instance APIs** (2 files)
[create-instance](references/api-reference/gpu-instance/create-instance.md) · [list-clusters](references/api-reference/gpu-instance/list-clusters.md)

### Support & Design System

**Billing** (4 files)
[budgets](references/billing/budgets.md) · [auto-top-up](references/billing/auto-top-up.md) · [payment-methods](references/billing/payment-methods.md) · [low-balance-alert](references/billing/low-balance-alert.md)

**Team** (1 file)
[team-management](references/team/team-management.md)

**Design System** (7 files)
[overview](references/design-system/overview.md) · [typography](references/design-system/typography.md) · [colors](references/design-system/colors.md) · [buttons](references/design-system/buttons.md) · [navigation](references/design-system/navigation.md) · [icons](references/design-system/icons.md) · [logo](references/design-system/logo.md)

---

## Common Tasks

### Start with Model APIs
1. Get API key from https://novita.ai/console
2. Set base URL to `https://api.novita.ai/openai`
3. Call `/v1/models` to list available models
4. Use OpenAI-compatible APIs for chat completions
5. See [llm/api.md](references/llm/api.md) for details

### Launch GPU Instance
1. Go to https://novita.ai/gpus-console/explore
2. Choose GPU or template
3. Configure and launch
4. Connect via SSH or web terminal
5. See [gpu-instance/](references/gpu-instance/) for details

### Create Serverless Endpoint
1. Prepare container image
2. Go to https://novita.ai/gpus-console/serverless
3. Create endpoint with scale policy
4. Test and deploy
5. See [serverless-gpus/](references/serverless-gpus/) for details

### Start Agent Sandbox
1. Install SDK or CLI
2. Create sandbox with desired resources
3. Run commands or upload code
4. Pause/resume as needed
5. See [sandbox/](references/sandbox/) for details

### Integrate with Framework
1. Get Novita API key
2. Set base URL to `https://api.novita.ai/openai`
3. Update model names as needed
4. See [integrations/](references/integrations/) for specific guides

---

## Support & Resources

- **Documentation**: https://novita.ai/docs
- **Email**: support@novita.ai
- **Discord**: https://discord.gg/YyPRAzwp7P
- **FAQ**: https://novita.ai/docs/guides/faq
- **Status Page**: https://status.novita.ai/
