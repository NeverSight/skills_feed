---
name: sensei
description: "**WORKFLOW SKILL** - Iteratively improve skill frontmatter compliance using the Ralph loop pattern. USE FOR: run sensei, sensei help, improve skill, fix frontmatter, skill compliance, frontmatter audit, improve triggers, add anti-triggers, batch skill improvement, check skill tokens, score skill. DO NOT USE FOR: creating new skills from scratch (use skill-creator), writing skill content/body, general markdown editing, or non-SKILL.md files. INVOKES: token counting tools, test runners, git commands. FOR SINGLE OPERATIONS: use token CLI directly for counts/checks."
---

# Sensei

> "A true master teaches not by telling, but by refining."

Automates skill frontmatter improvement using the [Ralph loop pattern](https://github.com/soderlund/ralph) - iteratively improving skills until they reach Medium-High compliance with passing tests.

## Help

When user says "sensei help" or asks how to use sensei:

```
╔══════════════════════════════════════════════════════════════════╗
║  SENSEI - Skill Frontmatter Compliance Improver                  ║
╠══════════════════════════════════════════════════════════════════╣
║                                                                  ║
║  USAGE:                                                          ║
║    Run sensei on <skill-name>              # Single skill        ║
║    Run sensei on <skill-name> --fast       # Skip tests          ║
║    Run sensei on <skill1>, <skill2>        # Multiple skills     ║
║    Run sensei on all Low-adherence skills  # Batch by score      ║
║    Run sensei on all skills                # All skills          ║
║                                                                  ║
║  WHAT IT DOES:                                                   ║
║    1. READ    - Load skill's SKILL.md and count tokens           ║
║    2. SCORE   - Check compliance (Low/Medium/Medium-High/High)   ║
║    3. SCAFFOLD- Create tests from template if missing            ║
║    4. IMPROVE - Add USE FOR triggers + DO NOT USE FOR            ║
║    5. TEST    - Run tests, fix if needed                         ║
║    6. TOKENS  - Check token budget                               ║
║    7. SUMMARY - Show before/after comparison                     ║
║    8. PROMPT  - Ask: Commit, Create Issue, or Skip?              ║
║    9. REPEAT  - Until Medium-High score achieved                 ║
║                                                                  ║
║  TARGET SCORE: Medium-High                                       ║
║    ✓ Description > 150 chars                                     ║
║    ✓ Has "USE FOR:" trigger phrases                              ║
║    ✓ Has "DO NOT USE FOR:" anti-triggers                         ║
║    ✓ Has "INVOKES:" for tool relationships (optional)            ║
║    ✓ SKILL.md < 500 tokens (soft limit)                          ║
║                                                                  ║
║  MCP INTEGRATION (when INVOKES present):                         ║
║    ✓ Has "MCP Tools Used" table                                  ║
║    ✓ Has Prerequisites section                                   ║
║    ✓ Has CLI fallback pattern                                    ║
║    ✓ No skill-tool name collision                                ║
║                                                                  ║
╚══════════════════════════════════════════════════════════════════╝
```

## Configuration

Sensei uses these defaults (override by specifying in your prompt):

| Setting | Default | Description |
|---------|---------|-------------|
| Skills directory | `skills/` or `.github/skills/` | Where SKILL.md files live |
| Tests directory | `tests/` | Where test files live |
| Token soft limit | 500 | Target for SKILL.md |
| Token hard limit | 5000 | Maximum for SKILL.md |
| Target score | Medium-High | Minimum compliance level |
| Max iterations | 5 | Per-skill loop limit |

Auto-detect skills directory by checking (in order):
1. `skills/` in project root
2. `.github/skills/` 
3. User-specified path

## Invocation Modes

### Single Skill
```
Run sensei on my-skill-name
```

### Multiple Skills
```
Run sensei on skill-a, skill-b, skill-c
```

### By Adherence Level
```
Run sensei on all Low-adherence skills
Run sensei on all Medium-adherence skills
```

### All Skills
```
Run sensei on all skills
```

### Fast Mode (Skip Tests)
```
Run sensei on my-skill --fast
```

## The Ralph Loop

For each skill, execute this loop until score >= Medium-High:

### Step 1: READ
Load the skill's current state:
```
{skills-dir}/{skill-name}/SKILL.md
{tests-dir}/{skill-name}/ (if exists)
```

Run token count:
```bash
npm run tokens -- count {skills-dir}/{skill-name}/SKILL.md
```

### Step 2: SCORE
Assess compliance by checking the frontmatter for:
- Description length (>= 150 chars)
- "USE FOR:" trigger phrases
- "DO NOT USE FOR:" anti-triggers
- "INVOKES:" routing clarity (optional)

See [references/scoring.md](references/scoring.md) for detailed criteria.

### Step 3: CHECK
If score >= Medium-High AND tests pass → go to SUMMARY step.

### Step 4: SCAFFOLD (if needed)
If `{tests-dir}/{skill-name}/` doesn't exist, create test scaffolding using templates from [references/test-templates/](references/test-templates/).

### Step 5: IMPROVE FRONTMATTER
Enhance the SKILL.md description to include:

1. **Trigger phrases** - "USE FOR:" followed by specific keywords
2. **Anti-triggers** - "DO NOT USE FOR:" with scenarios that should use other skills
3. Keep description under 1024 characters

Template:
```yaml
---
name: skill-name
description: |
  [1-2 sentence description of what the skill does]
  USE FOR: [phrase1], [phrase2], [phrase3], [phrase4], [phrase5].
  DO NOT USE FOR: [scenario1] (use other-skill), [scenario2].
---
```

### Step 6: IMPROVE TESTS
Update test prompts to match new frontmatter:
- `shouldTriggerPrompts` - 5+ prompts matching "USE FOR:" phrases
- `shouldNotTriggerPrompts` - 5+ prompts matching "DO NOT USE FOR:"

### Step 7: VERIFY
Run tests (skip if `--fast` flag):
```bash
# Framework-specific command based on project
npm test -- --testPathPattern={skill-name}  # Jest
pytest tests/{skill-name}/                   # pytest
waza run tests/{skill-name}/trigger_tests.yaml  # Waza
```

### Step 8: TOKENS
Check token budget:
```bash
npm run tokens -- check {skills-dir}/{skill-name}/SKILL.md
```

Budget guidelines:
- SKILL.md: < 500 tokens (soft), < 5000 (hard)
- references/*.md: < 1000 tokens each

### Step 8b: MCP INTEGRATION (if INVOKES present)
When description contains `INVOKES:`, check:

1. **MCP Tools Used table** - Does skill body have the table?
2. **Prerequisites section** - Are requirements documented?
3. **CLI fallback** - Is there a fallback when MCP unavailable?
4. **Name collision** - Does skill name match an MCP tool?

If checks fail, add missing sections using patterns from [mcp-integration.md](references/mcp-integration.md).

### Step 9: SUMMARY
Display before/after comparison:

```
╔══════════════════════════════════════════════════════════════════╗
║  SENSEI SUMMARY: {skill-name}                                    ║
╠══════════════════════════════════════════════════════════════════╣
║  BEFORE                          AFTER                           ║
║  ──────                          ─────                           ║
║  Score: Low                      Score: Medium-High              ║
║  Tokens: 142                     Tokens: 385                     ║
║  Triggers: 0                     Triggers: 5                     ║
║  Anti-triggers: 0                Anti-triggers: 3                ║
╚══════════════════════════════════════════════════════════════════╝
```

### Step 10: PROMPT USER
Ask how to proceed:
- **[C] Commit** - Save with message `sensei: improve {skill-name} frontmatter`
- **[I] Create Issue** - Open issue with summary and suggestions
- **[S] Skip** - Discard changes, move to next skill

### Step 11: REPEAT or EXIT
- If score < Medium-High AND iterations < 5 → go to Step 2
- If iterations >= 5 → timeout, show summary, move to next skill

## Scoring Quick Reference

| Score | Requirements |
|-------|--------------|
| **Low** | Description < 150 chars OR no triggers |
| **Medium** | Description >= 150 chars AND has trigger keywords |
| **Medium-High** | Has "USE FOR:" AND "DO NOT USE FOR:" |
| **High** | Medium-High + routing clarity (INVOKES/FOR SINGLE OPERATIONS) |

### MCP Integration Score (when INVOKES present)

| Check | Status |
|-------|--------|
| MCP Tools Used table | ✓/✗ |
| Prerequisites section | ✓/✗ |
| CLI fallback pattern | ✓/✗ |
| No name collision | ✓/✗ |

See [references/scoring.md](references/scoring.md) for full criteria.
See [references/mcp-integration.md](references/mcp-integration.md) for MCP patterns.

## Frontmatter Patterns

### Skill Classification Prefix

Add a prefix to clarify the skill type:
- `**WORKFLOW SKILL**` - Multi-step orchestration
- `**UTILITY SKILL**` - Single-purpose helper
- `**ANALYSIS SKILL**` - Read-only analysis/reporting

### Routing Clarity (for High score)

When skills interact with MCP tools or other skills, add:
- `INVOKES:` - What tools/skills this skill calls
- `FOR SINGLE OPERATIONS:` - When to bypass this skill

### Quick Example

**Before (Low):**
```yaml
description: 'Process PDF files'
```

**After (High with routing):**
```yaml
description: |
  **WORKFLOW SKILL** - Process PDF files including text extraction, rotation, and merging.
  USE FOR: "extract PDF text", "rotate PDF", "merge PDFs", "PDF to text".
  DO NOT USE FOR: creating PDFs from scratch (use document-creator),
  image extraction (use image-extractor).
  INVOKES: pdf-tools MCP for extraction, file-system for I/O.
  FOR SINGLE OPERATIONS: Use pdf-tools MCP directly for simple extractions.
```

See [references/examples.md](references/examples.md) for more before/after transformations.

## Commit Messages

```
sensei: improve {skill-name} frontmatter
```

## Reference Documentation

- [scoring.md](references/scoring.md) - Detailed scoring criteria and algorithm
- [mcp-integration.md](references/mcp-integration.md) - MCP tool integration patterns
- [loop.md](references/loop.md) - Ralph loop workflow details
- [examples.md](references/examples.md) - Before/after transformation examples
- [configuration.md](references/configuration.md) - Project setup patterns
- [test-templates/](references/test-templates/) - Test scaffolding templates
- [test-templates/waza.md](references/test-templates/waza.md) - Waza trigger test format


## Built-in Scripts

Run `npm run tokens help` for full usage.

### Token Commands

```bash
npm run tokens count              # Count all markdown files
npm run tokens check              # Check against token limits
npm run tokens suggest            # Get optimization suggestions
npm run tokens compare            # Compare with git history
```

### Configuration

Create `.token-limits.json` to customize limits:
```json
{
  "defaults": { "SKILL.md": 500, "references/**/*.md": 1000 },
  "overrides": { "README.md": 3000 }
}
```
