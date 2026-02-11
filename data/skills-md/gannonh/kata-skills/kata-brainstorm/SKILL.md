---
name: kata-brainstorm
description: Run structured brainstorming sessions using paired explorer/challenger agent teams. Explorers generate ideas, challengers play devil's advocate, and 2-3 rounds of debate produce pressure-tested proposals. Use when brainstorming product ideas, exploring feature directions, evaluating strategic options, generating milestone candidates, or when the user says "brainstorm", "explore ideas", "what should we build next", "generate options", or "run an ideation session".
metadata:
  version: "0.1.0"
---

# Explorer/Challenger Brainstorming

Run structured brainstorming sessions using paired agent teams. Each pair has an explorer (generates ideas) and a challenger (plays devil's advocate). Multiple pairs run in parallel with different remits, producing debate-tested proposals.

## Default Team Structure

Three pairs, each with a different lens:

| Pair | Explorer           | Challenger           | Remit                                             |
| ---- | ------------------ | -------------------- | ------------------------------------------------- |
| 1    | explorer-quickwins | challenger-quickwins | Low-effort, high-impact improvements              |
| 2    | explorer-highvalue | challenger-highvalue | Substantial features worth significant investment |
| 3    | explorer-radical   | challenger-radical   | New directions and paradigm shifts                |

The user may customize remits, number of pairs, or focus areas. Adapt the team structure to match.

## Process

### Step 0: Check Agent Teams Prerequisite

Brainstorming requires Claude Code Agent Teams (experimental). Check before proceeding.

1. Run bash to check the env var:

```bash
echo "$CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS"
```

2. **If output is "1":** Proceed to Step 1.

3. **If output is NOT "1":** Run a secondary check against settings.json:

```bash
node -e "
  try {
    const fs = require('fs');
    const path = require('path');
    const s = JSON.parse(fs.readFileSync(path.join(process.env.HOME, '.claude', 'settings.json'), 'utf8'));
    console.log((s.env && s.env.CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS) || '');
  } catch(e) { console.log(''); }
"
```

4. **If settings.json shows "1" but env var doesn't:** Display the following message and STOP (do not continue to Step 1):

> Agent Teams is enabled in settings but requires a restart. Please exit Claude Code (`/exit`) and relaunch, then run `/kata-brainstorm` again.

5. **If neither env var nor settings.json shows "1":** Present AskUserQuestion:

**Header:** Agent Teams Required

**Question:** Brainstorming uses Claude Code Agent Teams (experimental feature). Enable it?

**Option A — Enable Agent Teams:**

Run the settings.json merge (read-merge-write pattern):

```bash
node -e "
  const fs = require('fs');
  const path = require('path');
  const settingsPath = path.join(process.env.HOME, '.claude', 'settings.json');
  let settings = {};
  try {
    settings = JSON.parse(fs.readFileSync(settingsPath, 'utf8'));
  } catch (e) {}
  if (!settings.env) settings.env = {};
  settings.env.CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS = '1';
  fs.mkdirSync(path.dirname(settingsPath), { recursive: true });
  fs.writeFileSync(settingsPath, JSON.stringify(settings, null, 2));
  console.log('Agent Teams enabled in ~/.claude/settings.json');
"
```

Then display and STOP:

> Agent Teams enabled in ~/.claude/settings.json. Please restart Claude Code (`/exit` then relaunch) and run `/kata-brainstorm` again.

**Option B — Skip brainstorm:**

Display and STOP:

> Brainstorming requires Agent Teams. You can enable it later by adding `CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS=1` to `~/.claude/settings.json` under the `env` key.

### Step 1: Gather Context

Before spawning agents, assemble a project brief. The approach depends on whether this is a Kata project.

**Check for Kata project:**

```bash
[ -d ".planning" ] && echo "kata" || echo "generic"
```

#### Path A: Kata Project (`.planning/` exists)

Read and condense the following sources into a single project brief (target ~1300 words total). Use the Read tool for each file. If any file is missing, skip it and continue with available data.

| Source | What to extract | Target size |
| ------ | -------------- | ----------- |
| `.planning/PROJECT.md` | Core value statement, current milestone name and goals, validated requirements (list only), active requirements, constraints | ~500 words |
| `.planning/ROADMAP.md` | Current milestone section (phases with goals), progress summary table | ~300 words |
| `.planning/issues/open/*.md` | Issue titles and areas (one line each) | ~200 words |
| `.planning/STATE.md` | Current position block, recent decisions (last 3-5) | ~200 words |

For open issues, list files with bash then read first few lines of each to extract titles:

```bash
ls .planning/issues/open/*.md 2>/dev/null | head -20
```

#### Path B: Non-Kata Project (no `.planning/` directory)

Fall back to generic context gathering:

- Read `README.md` or `README` if it exists
- Read `package.json` description field if it exists
- Read any `CHANGELOG.md` or `HISTORY.md` for recent changes
- Read any roadmap, backlog, or planning files found in the repo root

Condense available information into a project brief.

#### Brief Injection

The assembled brief (Kata or generic) replaces the `[CONDENSED PROJECT BRIEF]` placeholder in the explorer and challenger prompt templates when spawning agents in Step 4.

### Step 2: Create Output Directory

Create a timestamped output directory for this brainstorm session:

```
.planning/brainstorms/YYYY-MM-DDTHH-MM-brainstorm/
```

Use the current date and time (e.g., `2026-02-05T11-18-brainstorm`). All agent output files and the final SUMMARY.md go here. Use this directory as the scratchpad for agent file writes (do NOT use /tmp or the scratchpad directory).

### Step 3: Create Team and Tasks

1. Create team with `TeamCreate` tool
2. Create one task per agent (6 tasks for 3 pairs)
3. Set dependencies: each challenger task is blocked by its paired explorer task

### Step 4: Spawn Agents

Spawn all agents in parallel using the Task tool with `team_name` and `name` parameters. Use `general-purpose` subagent type for all agents.

Tell each agent to write output files to the brainstorm output directory created in Step 2.

**Explorer prompt template:**

```
You are an EXPLORER on a brainstorm team for [PROJECT]. Your job is to propose [REMIT DESCRIPTION] ideas.

## Your Role
Generate creative, practical ideas. You're the optimist — find opportunities.
[Don't self-censor. The challenger's job is to ground ideas — yours is to push boundaries.]

## Project Context
[CONDENSED PROJECT BRIEF]

## Your Task
1. Claim your task from the task list using TaskUpdate
2. Explore the codebase to understand current architecture and gaps
3. Read any backlog/issues for inspiration
4. Write [N] proposals to [OUTPUT_DIR]/[category]-ideas.md

For each idea, include:
- **Name**: Short descriptive name
- **What**: Description of the idea
- **Why**: Strategic justification
- **Scope**: Rough effort estimate
- **Risks**: What could go wrong

5. Message your challenger partner with a summary
6. Engage in 2-3 rounds of back-and-forth debate
7. Write final consolidated report to [OUTPUT_DIR]/[category]-report.md incorporating valid critiques
8. Mark your task as completed
```

**Challenger prompt template:**

```
You are a CHALLENGER (devil's advocate) on a brainstorm team for [PROJECT]. Your partner "[explorer-name]" is proposing [REMIT DESCRIPTION] ideas. Your job is to pressure-test them.

## Your Role
You're the skeptic. Find flaws, question assumptions, identify hidden complexity. But be constructive — if an idea survives your scrutiny, it's probably good. Your goal isn't to kill ideas but to make them better.
[Be specific. "This seems hard" is weak. "This requires X which has Y dependency" is strong.]

## Project Context
[CONDENSED PROJECT BRIEF]

## Your Task
1. Claim your task (blocked until explorer finishes initial proposals)
2. While waiting, explore the codebase to build your own understanding
3. When you receive ideas, evaluate each on:
   - Feasibility: Is the scope realistic?
   - Value: Does this solve a real problem?
   - Risks: What could go wrong?
   - Alternatives: Is there a simpler way?
4. Send critique back to your explorer partner
5. Engage in 2-3 rounds of discussion
6. After the explorer writes the final report, mark your task as completed

Your best output: "This idea is viable IF you scope it to X and start with Y."
```

### Step 5: Monitor and Manage

- Watch for task completions via TaskList
- Shut down completed pairs (explorer first, then challenger) via `shutdown_request` messages
- Don't intervene in debates unless an agent is stuck

### Step 6: Synthesize and Write Reports

Once all pairs complete:

1. Read all final reports from the output directory
2. Clean up the team with `TeamDelete` tool
3. Write a `SUMMARY.md` file to the output directory that consolidates all results:
   - Brief intro describing the session (topic, number of pairs, remits)
   - One section per category summarizing the surviving proposals in a table
   - Links to the full category reports (e.g., `[Full report](quickwins-report.md)`)
   - Deferred/dropped items with brief rationale
   - Cross-cutting themes that emerged across multiple pairs
   - Recommended sequencing if applicable
4. Present the SUMMARY.md content to the user

The final output directory structure should look like:

```
.planning/brainstorms/YYYY-MM-DDTHH-MM-brainstorm/
├── SUMMARY.md              # Consolidated synthesis (primary output)
├── [category]-ideas.md     # Raw proposals per pair
└── [category]-report.md    # Debate-refined reports per pair
```

## Customization

**Fewer/more pairs:** Adjust based on scope. A focused session might use 1 pair. A broad exploration might use 4-5.

**Custom remits:** Replace the default three lenses with whatever framing suits the question. Examples:

- Technical feasibility / Business value / User experience
- Build / Buy / Partner
- Short-term / Medium-term / Long-term
- Core product / Adjacent markets / New markets

**Solo explorer (no challenger):** For pure idea generation without debate, spawn explorers only. Skip the challenger role.

**Domain-specific context:** For technical brainstorming, have explorers read specific code paths. For product brainstorming, have them research competitors or user feedback.

## Output Structure

Each pair produces:

- `[category]-ideas.md` — Explorer's initial proposals (raw)
- `[category]-report.md` — Final consolidated report after debate (refined)

The `SUMMARY.md` is the primary deliverable. Category reports provide detail. Initial ideas files are retained for reference.
