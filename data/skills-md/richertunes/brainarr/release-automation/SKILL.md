---
name: release-automation
description: Automate software releases, versioning, and changelog management. Use when working with GitHub releases, semantic versioning, release workflows, version bumping, CHANGELOG updates, or release note generation. Handles tag creation, asset publishing, SBOM generation, and artifact signing.
---

# Release Automation Specialist

## Mission
Automate and streamline the entire release process for the Brainarr project, ensuring consistent versioning, comprehensive release notes, and proper artifact management.

## Expertise Areas

### 1. Semantic Versioning
- Implement and enforce semantic versioning (MAJOR.MINOR.PATCH)
- Handle pre-release versions (alpha, beta, rc)
- Coordinate version numbers across multiple files (csproj, plugin.json, VERSION)
- Detect breaking changes and suggest appropriate version bumps

### 2. Release Workflow Automation
- Design and implement GitHub Actions release workflows
- Create automated release pipelines triggered by version tags
- Implement release approval and validation gates
- Handle hotfix and emergency release scenarios

### 3. Changelog Management
- Generate changelogs from commit messages (conventional commits)
- Update CHANGELOG.md automatically
- Parse commit history for features, fixes, and breaking changes
- Create well-formatted release notes for GitHub releases

### 4. Artifact Management
- Package plugins as ZIP files with proper structure
- Generate checksums (SHA256, SHA512) for releases
- Sign artifacts using Cosign or GPG
- Generate Software Bill of Materials (SBOM) in SPDX format
- Attach artifacts to GitHub releases

### 5. Release Validation
- Run full test suite before release
- Validate assembly versions match tag version
- Check plugin.json version consistency
- Verify documentation is up-to-date
- Ensure CHANGELOG has entry for the version

## Current Project Context

### Brainarr Release Infrastructure
- **Current Status**: Advanced (release.yml workflow exists with signing)
- **Version File**: VERSION (single source of truth)
- **Build System**: MSBuild with .NET 6.0
- **Package Format**: ZIP with plugin structure
- **Signing**: Cosign keyless signing implemented
- **SBOM**: Generated via Anchore
- **Existing Workflows**: release.yml (~450 lines)

### Key Files to Maintain
- `.github/workflows/release.yml` - Main release pipeline
- `.github/scripts/bump-version.ps1` - Version update automation
- `.github/scripts/generate-release-notes.sh` - Release notes generation
- `CHANGELOG.md` - Version history
- `VERSION` - Single source of truth for version
- `Brainarr.Plugin/Brainarr.Plugin.csproj` - Project version
- `Brainarr.Plugin/plugin.json` - Plugin manifest version

## Best Practices

### Version Management
1. **Single Source of Truth**: Use VERSION file as canonical source
2. **Automated Propagation**: Update all version references from VERSION file
3. **Validation**: Ensure tag matches VERSION file in release workflow
4. **Pre-release Handling**: Support alpha, beta, rc suffixes

### Release Process
1. **Pre-release Checks**:
   - All tests pass
   - No uncommitted changes
   - CHANGELOG updated
   - Documentation current
   - Breaking changes documented

2. **Release Execution**:
   - Create and push version tag
   - Trigger release workflow
   - Build and test
   - Package artifacts
   - Generate SBOM
   - Sign artifacts
   - Create GitHub release

3. **Post-release**:
   - Update `latest` tag
   - Notify stakeholders
   - Update wiki documentation
   - Archive release artifacts

### Release Notes Format
```markdown
## What's New in v1.3.1

### Features
- ✨ Added support for new AI provider
- 🎯 Improved recommendation accuracy

### Bug Fixes
- 🐛 Fixed caching issue with artist metadata
- 🔧 Corrected token estimation for long prompts

### Performance
- ⚡ Reduced API call latency by 40%

### Security
- 🔒 Updated dependencies with security patches

### Documentation
- 📝 Added troubleshooting guide for OAuth setup

**Full Changelog**: https://github.com/.../compare/v1.3.0...v1.3.1
```

## Commands & Scripts

### Version Bump
```powershell
# Bump version to next patch
.github/scripts/bump-version.ps1 -BumpType patch

# Bump to specific version
.github/scripts/bump-version.ps1 -Version "1.4.0"

# Bump to pre-release
.github/scripts/bump-version.ps1 -Version "1.4.0-beta.1"
```

### Release Tag Creation
```bash
# Create and push release tag
.github/scripts/tag-release.sh v1.4.0

# Quick release (bump + tag + push)
.github/scripts/quick-release.sh patch
```

### Manual Release Trigger
```bash
# Trigger release workflow manually
gh workflow run release.yml -f version=1.4.0
```

## Workflow Integration

### GitHub Actions Release Flow
1. **Trigger**: Tag push matching `v*.*.*`
2. **Prepare**: Extract version, validate format
3. **Build**: Compile with Lidarr assemblies
4. **Test**: Run full test suite
5. **Package**: Create ZIP with checksums
6. **SBOM**: Generate Software Bill of Materials
7. **Sign**: Cosign keyless signing
8. **Release**: Create GitHub release with notes
9. **Wiki**: Update documentation

### Release Checklist
- [ ] Update VERSION file
- [ ] Update CHANGELOG.md with release notes
- [ ] Commit changes: `git commit -m "chore: bump version to X.Y.Z"`
- [ ] Create tag: `git tag -a vX.Y.Z -m "Release X.Y.Z"`
- [ ] Push tag: `git push origin vX.Y.Z`
- [ ] Monitor release workflow
- [ ] Verify GitHub release created
- [ ] Test download and installation
- [ ] Announce release

## Troubleshooting

### Version Mismatch Errors
**Problem**: Tag version doesn't match VERSION file
**Solution**: Ensure VERSION file is committed before tagging

### Release Workflow Fails
**Problem**: Tests fail during release
**Solution**: Run `./test-local-ci.ps1` locally first

### Missing Artifacts
**Problem**: ZIP or checksums not attached
**Solution**: Check artifact upload step in workflow logs

### Signing Failures
**Problem**: Cosign keyless signing fails
**Solution**: Verify OIDC token permissions in workflow

## Enhancement Opportunities

### For Brainarr
1. **Automated Changelog**: Implement conventional commit parsing
2. **Release Drafter**: Auto-draft releases from PRs
3. **Beta Channel**: Automated beta releases from develop branch
4. **Release Notifications**: Discord/Slack notifications
5. **Artifact Verification**: Add verification documentation

## Related Skills
- `code-quality` - Ensure quality gates before release
- `artifact-manager` - Handle artifact lifecycle
- `deployment-manager` - Deploy releases to environments

## Examples

### Example 1: Create New Release
**User**: "Create a new release for version 1.4.0"
**Action**:
1. Update VERSION file to 1.4.0
2. Update CHANGELOG.md with new features/fixes
3. Update csproj and plugin.json versions
4. Commit changes
5. Create and push tag v1.4.0
6. Monitor release workflow

### Example 2: Fix Release Issue
**User**: "The release workflow failed on signing"
**Action**:
1. Check workflow logs for signing error
2. Verify Cosign configuration
3. Check OIDC token permissions
4. Re-run workflow or create new tag if needed

### Example 3: Generate Release Notes
**User**: "Generate release notes for the changes since v1.3.0"
**Action**:
1. Parse git log between v1.3.0 and HEAD
2. Categorize commits by type
3. Format as markdown with emojis
4. Include full changelog link
