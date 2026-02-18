---
name: converter
description: 'Cross-platform skill converter. Parse AgentOps skills into a universal bundle format, then convert to target platforms (Codex, Cursor). Triggers: convert, converter, convert skill, export skill, cross-platform.'
metadata:
  tier: solo
  dependencies: []
---

# /converter -- Cross-Platform Skill Converter

Parse AgentOps skills into a universal SkillBundle format, then convert to target agent platforms.

## Quick Start

```bash
/converter skills/council codex     # Convert council skill to Codex format
/converter skills/vibe cursor       # Convert vibe skill to Cursor format
/converter --all codex              # Convert all skills to Codex
```

## Pipeline

The converter runs a three-stage pipeline:

```
parse --> convert --> write
```

### Stage 1: Parse

Read the source skill directory and produce a SkillBundle:

- Extract YAML frontmatter from SKILL.md (between `---` markers)
- Collect the markdown body (everything after the closing `---`)
- Enumerate all files in `references/` and `scripts/`
- Assemble into a SkillBundle (see `references/skill-bundle-schema.md`)

### Stage 2: Convert

Transform the SkillBundle into the target platform's format:

| Target | Output Format | Status |
|--------|---------------|--------|
| `codex` | Codex SKILL.md + prompt.md | Implemented |
| `cursor` | Cursor .mdc rule + optional mcp.json | Implemented |

The Codex adapter produces a `SKILL.md` (body + inlined references + scripts as code blocks) and a `prompt.md` (Codex prompt referencing the skill). Descriptions are truncated to 1024 chars at a word boundary if needed.

The Cursor adapter produces a `<name>.mdc` rule file with YAML frontmatter (`description`, `globs`, `alwaysApply: false`) and body content. References are inlined into the body, scripts are included as code blocks. Output is budget-fitted to 100KB max -- references are omitted largest-first if the total exceeds the limit. If the skill references MCP servers, a `mcp.json` stub is also generated.

### Stage 3: Write

Write the converted output to disk.

- **Default output directory:** `.agents/converter/<target>/<skill-name>/`
- **Write semantics:** Clean-write. The target directory is deleted before writing. No merge with existing content.

## CLI Usage

```bash
# Convert a single skill
bash skills/converter/scripts/convert.sh <skill-dir> <target> [output-dir]

# Convert all skills
bash skills/converter/scripts/convert.sh --all <target> [output-dir]
```

### Arguments

| Argument | Required | Description |
|----------|----------|-------------|
| `skill-dir` | Yes (or `--all`) | Path to skill directory (e.g. `skills/council`) |
| `target` | Yes | Target platform: `codex`, `cursor`, or `test` |
| `output-dir` | No | Override output location. Default: `.agents/converter/<target>/<skill-name>/` |
| `--all` | No | Convert all skills in `skills/` directory |

## Supported Targets

- **codex** -- Convert to OpenAI Codex format (SKILL.md + prompt.md). Output: `<dir>/SKILL.md` and `<dir>/prompt.md`.
- **cursor** -- Convert to Cursor rules format (`.mdc` rule file + optional `mcp.json`). Output: `<dir>/<name>.mdc` and optionally `<dir>/mcp.json`.
- **test** -- Emit the raw SkillBundle as structured markdown. Useful for debugging the parse stage.

## Extending

To add a new target platform:

1. Add a conversion function to `scripts/convert.sh` (pattern: `convert_<target>`)
2. Update the target table above
3. Add reference docs to `references/` if the target format needs documentation

## References

- `references/skill-bundle-schema.md` -- SkillBundle interchange format specification
