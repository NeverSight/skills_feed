---
name: release-engine
type: atomic
license: MIT
description: >
  Use when preparing a versioned Rails engine release (SemVer, changelog).
  Trigger words: release engine, version bump, publish gem, changelog.
metadata:
  version: 1.0.0
  user-invocable: "true"
---

# Release Engine

Use this skill when the task is to ship a Rails engine as a gem or prepare a new version.

## Quick Reference

| Bump | When to use | Action |
|------|-------------|--------|
| **Patch** | Bug fixes and internal changes without public behavior breakage | Update version constant, document under Fixed |
| **Minor** | Backward-compatible features and new extension points | Update version constant, document under Added/Changed |
| **Major** | Breaking changes to API, setup, routes, migrations, config, or supported framework versions | Update version constant, document under Changed/Deprecated; write explicit upgrade notes |

## HARD-GATE

```text
DO NOT release without updating CHANGELOG and version file.
```

## Core Process

1. Confirm scope and compatibility impact — is this patch, minor, or major?
2. Run full test suite: `bundle exec rspec`. Fix all failures before proceeding.
3. Set the version bump — update the version constant once: `module MyEngine; VERSION = "1.2.0"; end` in `lib/my_engine/version.rb`.
4. Update changelog and upgrade notes.
5. Verify gemspec metadata and dependencies match tested Rails/Ruby versions.
6. Dry-run the gem build: `gem build *.gemspec && gem push --dry-run *.gem`. Verify contents.
7. Confirm installation docs and README match the release — update if needed.
8. Publish: `gem push *.gem`.

## Extended Resources

Load release assets conditionally and say which one informed the output:

- Read `assets/release_checklist.md` when producing the release verification checklist or quality gates.
- Read `assets/release_notes_template.md` when drafting GitHub release notes, a long-form announcement, or public release copy.
- Read `assets/examples.md` only when the user needs concrete release examples.

**Changelog Guidelines**
- Document user-visible changes, not commits; group by Added/Changed/Fixed/Deprecated.
- For deprecations, document removal plan and replacement; keep deprecated code for at least one minor cycle.
- If the engine requires host changes during upgrade, document them explicitly even if the version bump is minor.

**Examples**
```markdown
## [1.2.0] - 2024-03-15
### Added
- `widget_count` config option to limit dashboard widgets (default: 10).
### Changed
- Minimum Rails version is now 7.0.
```

- [assets/release_checklist.md](assets/release_checklist.md)
- [assets/release_notes_template.md](assets/release_notes_template.md)
- [assets/examples.md](assets/examples.md)

## Output Style

1. **Version bump** — patch/minor/major with explicit reasoning.
2. **Version constant** — updated `lib/[engine_name]/version.rb`.
3. **CHANGELOG entries** — under Added/Changed/Fixed/Deprecated headers.
4. **Upgrade notes** — host app steps (config, migrations, dependencies).
5. **Gemspec + test status** — metadata, files, dependency ranges confirmed; pass/fail result of `bundle exec rspec`.
6. **Dry-run output** — exact command `gem build *.gemspec && gem push --dry-run *.gem` plus contents verification (`tar tf pkg/*.gem` or `gem contents`).
7. **Asset usage** — state which of `assets/release_checklist.md`, `assets/release_notes_template.md`, `assets/examples.md` was loaded, or explicitly say none was needed.
8. **GitHub release notes** — concise draft with summary, highlights, upgrade notes, and verification status.
9. **Release blockers** — open issues, or explicitly "No blockers".

## Integration

| Skill | When to chain |
|-------|---------------|
| document-engine | Updating README, setup instructions, or API docs for the release |
| upgrade-engine | Verifying Rails/Ruby version support or deprecation impact |
| test-engine | Ensuring tests pass before release and match documented behavior |
