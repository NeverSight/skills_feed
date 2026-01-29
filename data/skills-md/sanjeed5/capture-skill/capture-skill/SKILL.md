---
name: capture-skill
description: Capture learnings, patterns, or workflows from the current conversation into a new or existing skill. Use when the user wants to save what was learned, discovered, or built during a conversation as a reusable skill for future sessions. Triggers include "capture this as a skill", "save this for next time", "turn this into a skill", or when a useful workflow, pattern, or piece of domain knowledge emerged during the conversation.
---

# Capture Skill from Conversation

Extract knowledge, patterns, and workflows from the current conversation and persist them as a reusable skill.

## When to Use

- The user says "capture this as a skill" or "save this for next time"
- A useful workflow, pattern, or piece of domain knowledge emerged during the conversation
- The user wants to update an existing skill with new learnings
- The conversation uncovered non-obvious steps, gotchas, or best practices worth preserving

## Capture Process

### Phase 1: Identify What to Capture

Review the conversation for:

1. **Workflows**: Multi-step processes that were figured out through trial and error
2. **Domain knowledge**: Non-obvious facts, configurations, or constraints discovered
3. **Gotchas and fixes**: Problems encountered and their solutions
4. **Patterns**: Code patterns, command sequences, or templates that worked well
5. **Decision rationale**: Why certain approaches were chosen over alternatives

Summarize what you plan to capture and confirm with the user before proceeding.

### Phase 2: Decide Destination

If the user already specified a skill or the destination is obvious from context, proceed. Otherwise, clarify:

1. **New or existing skill?**
   - If existing: Which skill to update? (list relevant skills from `~/.cursor/skills/` and `.cursor/skills/`)
   - If new: What should it be named?
2. **Storage location** (for new skills):
   - Personal (`~/.cursor/skills/`) — available across all projects
   - Project (`.cursor/skills/`) — shared with the repository

### Phase 3: Draft the Skill Content

**When capturing into a new skill:**

1. Choose a descriptive name (lowercase, hyphens, max 64 chars)
2. Write a specific description including WHAT and WHEN (third person)
3. Distill the conversation into concise, actionable instructions
4. Include concrete examples drawn from the conversation
5. Add any utility scripts or commands that were used

**When updating an existing skill:**

1. Read the existing SKILL.md
2. Identify where new learnings fit (new section, updated steps, additional examples)
3. Integrate without duplicating existing content
4. Preserve the existing structure and voice

### Phase 4: Distillation Guidelines

Transform a messy conversation into clean, reusable instructions.

**Do:**

- Extract the final working approach, not the failed attempts (unless gotchas are instructive)
- Generalize from the specific case discussed (replace hardcoded values with placeholders)
- Include the "why" behind non-obvious steps
- Add context the agent wouldn't know without this conversation
- Keep it under 500 lines

**Don't:**

- Include conversation artifacts ("as we discussed", "you mentioned")
- Repeat information the agent already knows
- Include overly specific details that won't transfer to other situations
- Add verbose explanations where a code example suffices

### Phase 5: Write and Verify

1. Create/update the skill file(s)
2. Verify the SKILL.md is under 500 lines
3. Check that the description is specific and includes trigger terms
4. Confirm with the user that the captured content is accurate

## Example: Capturing a Debugging Workflow

If a conversation involved debugging a tricky deployment issue, the captured skill might look like:

```markdown
---
name: debug-k8s-deployments
description: Debug Kubernetes deployment failures including CrashLoopBackOff, image pull errors, and resource limits. Use when pods are failing to start or deployments are stuck.
---

# Debug K8s Deployments

## Diagnostic Steps

1. Check pod status: `kubectl get pods -n <namespace> | grep -v Running`
2. Get events: `kubectl describe pod <pod> -n <namespace>`
3. Check logs: `kubectl logs <pod> -n <namespace> --previous`

## Common Issues

### CrashLoopBackOff

- Check if the entrypoint command exists in the container
- Verify environment variables are set (especially secrets)
- Look for OOMKilled in `describe` output → increase memory limits

### ImagePullBackOff

- Verify image tag exists: `docker manifest inspect <image>`
- Check imagePullSecrets are configured for private registries
```

Note how this captures the diagnostic sequence and common solutions without any conversation artifacts.

## Handling Edge Cases

**Conversation had multiple topics**: Ask which specific learning to capture, or suggest creating separate skills for distinct topics.

**Learning is too small for a skill**: Use a rule instead (`.cursor/rules/`, `.claude/rules/`, etc.). Heuristic: single behavioral guideline or coding convention → rule. Multi-step workflow or needs bundled resources → skill.

**Existing skill needs major rewrite**: Confirm with the user whether to restructure the existing skill or create a new one that supersedes it.
