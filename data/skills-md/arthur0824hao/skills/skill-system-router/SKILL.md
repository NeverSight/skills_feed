---
name: skill-system-router
description: "Meta-skill that teaches the Agent how to discover, select, execute, chain, and observe skills in the skill system. Load this skill when you need to: (1) find which skill can handle a capability, (2) execute a skill operation via its entrypoint, (3) chain multiple skill operations together, (4) check policy before executing, or (5) log skill execution for observability. This skill makes YOU the router — you decide what to run, in what order, based on context."
license: MIT
compatibility: opencode
metadata:
  os: windows, linux, macos
---

# Skill System Router

You are the Router. This skill teaches you how to orchestrate other skills.

## How It Works

```
User goal → Read skills-index.json → Match capabilities → Read skill manifest
→ Check policy → Execute entrypoints → Parse JSON output → Decide next step → Log
```

## Step 0: Bootstrap (First Run Only)

Check if the project's AGENTS.md contains `## Skill System`.

- If found: skip to Step 1 (already bootstrapped).
- If not found: follow `scripts/bootstrap.md` to embed the skill system into this project.

This only runs once per project. After bootstrap, every future session reads AGENTS.md and knows about the skill system automatically.

## Step 1: Discover Skills

Read `skills-index.json` (in the skills root directory, sibling to skill folders) to see available capabilities.

The index maps capabilities → skills and lists each skill's operations with descriptions and input params. Match the user's goal to capabilities. If no match, check if the goal can be decomposed into sub-capabilities.

If `skills-index.json` is missing or stale, regenerate it:

```bash
bash "<this-skill-dir>/scripts/build-index.sh"
```

```powershell
powershell.exe -NoProfile -ExecutionPolicy Bypass -File "<this-skill-dir>\scripts\build-index.ps1"
```

## Step 2: Read Skill Manifest

Open the target skill's `SKILL.md` and find the `` `skill-manifest` `` fenced block. This gives you:

- **operations**: what the skill can do, with input/output schemas
- **effects**: side effects (used for policy check)
- **entrypoints**: OS-specific commands to run

Full manifest spec: `references/manifest-spec.md`

## Step 3: Check Policy

Before executing, verify the skill's declared `effects` against the active policy profile:

```sql
SELECT allowed_effects FROM skill_system.policy_profiles WHERE name = 'dev';
```

- ALL effects in `allowed_effects` → proceed
- ANY effect NOT in `allowed_effects` → **ask the user** before proceeding
- No policy profile exists → ask the user

Standard effects: `db.read`, `db.write`, `proc.exec`, `fs.read`, `fs.write`, `net.fetch`, `git.read`, `git.write`

## Step 4: Execute

1. Determine OS: `OS` env = `Windows_NT` → use `windows` entrypoint, otherwise `unix`
2. Read the operation's `entrypoints` for your OS
3. Substitute `{param}` placeholders with actual values
4. Set cwd to the skill's directory
5. Run the command
6. Parse the **last line of stdout** as JSON — this is the result

Exit code ≠ 0 or last line not JSON → operation failed.

## Step 5: Chain Operations

When a goal requires multiple skills/operations:

1. Execute first operation → parse JSON output
2. Use output values as input to the next operation (you decide the mapping)
3. Repeat until goal is met

You are intelligent — adapt based on intermediate results. This is better than a fixed pipeline because you can handle errors, skip unnecessary steps, and make contextual decisions.

## Step 6: Log (Observability)

After non-trivial workflows, log for observability:

```sql
INSERT INTO skill_system.runs(task_spec_id, status, started_at, effective_policy)
VALUES (NULL, 'running', NOW(), '{}'::jsonb) RETURNING id;

INSERT INTO skill_system.run_events(run_id, level, event_type, payload)
VALUES (<run_id>, 'info', 'step_completed',
  jsonb_build_object('skill', '<id>', 'operation', '<op>', 'status', '<ok|error>', 'duration_ms', <ms>));

UPDATE skill_system.runs SET status='succeeded', ended_at=NOW(),
  metrics=jsonb_build_object('steps', <n>, 'duration_ms', <ms>) WHERE id=<run_id>;
```

Skip logging for simple single-operation calls.

## Insight Suggestion

After completing a non-trivial session (multi-step work, significant discussion, or debugging), consider suggesting an insight pass:

> "Want me to run an insight pass on this session? It helps me learn your preferences for better collaboration next time."

This is a lightweight, optional prompt. Only suggest when:
- The session had meaningful interaction (not a single-line fix)
- The user hasn't already triggered insight extraction recently
- The session contained signals worth capturing (frustration, satisfaction, style preferences)

If the user agrees, load `skill-system-insight` and follow `scripts/extract-facets.md`.

## Common Patterns

**Single operation:**
Goal → index lookup → execute one entrypoint → return result

**Multi-step chain:**
Goal → op1.search → parse results → op2.store(using results) → done

**Cross-skill chain:**
Goal → skill-A.op1 → use output as context → skill-B.op2 → rebuild index → done

## Database

Uses tables from `skill-system-postgres`:
- `skill_system.policy_profiles` — effect allowlists
- `skill_system.runs` — execution records
- `skill_system.run_events` — step-level logs

```skill-manifest
{
  "schema_version": "2.0",
  "id": "skill-system-router",
  "version": "1.0.0",
  "capabilities": ["skill-discover", "skill-execute", "skill-chain", "index-rebuild"],
  "effects": ["fs.read", "fs.write", "proc.exec", "db.read", "db.write"],
  "operations": {
    "rebuild-index": {
      "description": "Regenerate skills-index.json by scanning all skill manifests.",
      "input": {},
      "output": {
        "description": "Index file path and skill count",
        "fields": { "file": "string", "skill_count": "integer" }
      },
      "entrypoints": {
        "unix": ["bash", "scripts/build-index.sh"],
        "windows": ["powershell.exe", "-NoProfile", "-ExecutionPolicy", "Bypass", "-File", "scripts\\build-index.ps1"]
      }
    },
    "bootstrap": {
      "description": "Embed skill-system into project AGENTS.md (first run only).",
      "input": {},
      "output": {
        "description": "Path to updated AGENTS.md",
        "fields": { "agents_md_path": "string" }
      },
      "entrypoints": {
        "agent": "Follow scripts/bootstrap.md procedure"
      }
    }
  },
  "stdout_contract": {
    "last_line_json": false,
    "note": "rebuild-index prints summary to stdout; bootstrap is agent-executed."
  }
}
```
