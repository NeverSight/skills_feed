---
name: link-validator
description: Validate markdown link portability in skills. TRIGGERS - check links, validate portability, fix broken links, relative paths.
---

# Link Validator

Validates markdown links in Claude Code skills for portability across installation locations.

## The Problem

Skills with absolute repo paths break when installed elsewhere:

| Path Type       | Example                 | Works When Installed?   |
| --------------- | ----------------------- | ----------------------- |
| Absolute repo   | `/skills/foo/SKILL.md`  | No - path doesn't exist |
| Relative        | `./references/guide.md` | Yes - always resolves   |
| Relative parent | `../sibling/SKILL.md`   | Yes - always resolves   |

## When to Use This Skill

- Before distributing a skill/plugin
- After creating new markdown links in skills
- When CI reports link validation failures
- To audit existing skills for portability issues

---

## TodoWrite Task Templates

### Template A: Validate Single Skill

```
1. Identify skill path to validate
2. Run: uv run scripts/validate_links.py <skill-path>
3. Review violation report (if any)
4. For each violation, apply suggested fix
5. Re-run validator to confirm all fixed
```

### Template B: Validate Plugin (Multiple Skills)

```
1. Identify plugin root directory
2. Run: uv run scripts/validate_links.py <plugin-path>
3. Review grouped violations by skill
4. Fix violations skill-by-skill
5. Re-validate entire plugin
```

### Template C: Fix Violations

```
1. Read violation report output
2. Locate file and line number
3. Review suggested relative path
4. Apply fix using Edit tool
5. Re-run validator on file
```

---

## Post-Change Checklist

After modifying this skill:

1. [ ] Script remains in sync with latest patterns
2. [ ] References updated if new patterns added
3. [ ] Tested on real skill with violations

---

## Quick Start

```bash
# Validate a single skill
uv run scripts/validate_links.py ~/.claude/skills/my-skill/

# Validate a plugin with multiple skills
uv run scripts/validate_links.py ~/.claude/plugins/my-plugin/

# Dry-run in current directory
uv run scripts/validate_links.py .
```

## Exit Codes

| Code | Meaning                                 |
| ---- | --------------------------------------- |
| 0    | All links valid (relative paths)        |
| 1    | Violations found (absolute repo paths)  |
| 2    | Error (invalid path, no markdown files) |

## What Gets Checked

**Flagged as Violations:**

- `/skills/foo/SKILL.md` - Absolute repo path
- `/docs/guide.md` - Absolute repo path

**Allowed (Pass):**

- `./references/guide.md` - Relative same directory
- `../sibling/SKILL.md` - Relative parent
- `https://example.com` - External URL
- `#section` - Anchor link

## Reference Documentation

- [Link Patterns Reference](./references/link-patterns.md) - Detailed pattern explanations and fix strategies

---

## Troubleshooting

| Issue                     | Cause                         | Solution                                          |
| ------------------------- | ----------------------------- | ------------------------------------------------- |
| Script not found          | Path or plugin not installed  | Verify plugin installed with `claude plugin list` |
| Exit code 2               | Invalid path or no .md files  | Check target path exists and contains markdown    |
| False positive on URL     | Regex matched external link   | URLs starting with `http` should be ignored       |
| Anchor link flagged       | Script treating `#` as path   | Anchor links (`#section`) are allowed by design   |
| Relative path still fails | Wrong relative direction      | Use `./` for same dir, `../` for parent           |
| Validation passes locally | CI uses different working dir | Ensure CI runs from correct repo root             |
| Too many violations       | Legacy codebase               | Fix incrementally, prioritize high-impact files   |
| Can't determine fix       | Complex path structure        | Read link-patterns.md for detailed fix strategies |
