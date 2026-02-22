---
name: policy-save-load-audit
description: "Audit policy save/load and checkpoint handling across metta/cogames to find compatibility risks or legacy shims. Use when save/load behavior is in question."
---

# Policy Save/Load Audit

## Workflow
- Trace the save/load call graph (policy spec, checkpoint writer/reader).
- Check file formats and compatibility points (.mpt, safetensors, metadata).
- Flag risks or legacy shims and propose cleanup steps.
- Summarize findings with file paths.
