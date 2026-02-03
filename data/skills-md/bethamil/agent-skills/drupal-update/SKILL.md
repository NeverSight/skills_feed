---
name: drupal-update
description: Automate Drupal module updates in DDEV environments with safety snapshots, composer update, drush updb, config export, and changelog generation. Handles security updates, patch versions, minor versions, and major version upgrades with compatibility checking. Use when updating Drupal modules, checking for module updates, running composer update, upgrading dependencies, checking outdated packages, or when user mentions DDEV, drush, composer outdated, or module security updates.
---

# Drupal Module Updates

Safely update Drupal modules in DDEV environments with automatic snapshots, intelligent update handling, and comprehensive changelog generation.

## Quick Start

When the user requests a module update:

1. Create safety snapshot
2. Check and apply security updates automatically
3. Run automatic updates for all semver-safe versions
4. Check for major version updates
5. Check compatibility for major updates with current Drupal core
6. Ask user about compatible major updates
7. Apply confirmed major updates
8. Run database updates and export configuration
9. Generate changelog with all changes

## Script Path Convention

Throughout this skill, `[skill-directory]` refers to the location where this skill is installed. Common locations include:
- Project skills directory
- Personal skills directory
- Custom skills directory

Replace `[skill-directory]` with the actual path to this skill on your system when running the changelog fetch script.

## Pre-Flight Checklist

Before starting updates, copy this checklist:

```
Update Progress:
- [ ] Verify DDEV environment is running
- [ ] Create snapshot for rollback
- [ ] Check for security updates
- [ ] Run automatic composer updates
- [ ] Review major version updates available
- [ ] Check compatibility for major updates
- [ ] Apply confirmed major updates
- [ ] Run database updates (drush updb)
- [ ] Export configuration (drush cex)
- [ ] Clear caches
- [ ] Generate changelog
- [ ] Verify site functionality
```

## Step-by-Step Workflow

### Step 1: Verify Environment

Check DDEV is running:

```bash
ddev describe
```

If not running, start it:

```bash
ddev start
```

### Step 2: Create Safety Snapshot

Always create a snapshot before updates:

```bash
ddev snapshot --name=pre-update-$(date +%Y%m%d-%H%M%S)
```

Store the snapshot name for rollback instructions later.

### Step 3: Security Updates (Auto-Apply)

Check for security vulnerabilities:

```bash
ddev composer audit
```

**If vulnerabilities found**: Security updates are automatically applied without asking. Inform the user which security issues were found and will be fixed.

**If no vulnerabilities**: Proceed to next step.

### Step 4: Automatic Updates

Run composer update to handle all semver-safe updates:

```bash
ddev composer update
```

This automatically updates:
- Patch versions (e.g., 3.6.2 → 3.6.3)
- Minor versions within constraints (e.g., 3.6.0 → 3.7.0 if constraint is ^3.6)

**Monitor the output** for:
- Number of packages updated
- Any warnings or errors
- Dependency conflicts (rare but possible)

**Capture updated packages for changelog:**

After `composer update` completes, extract the list of updated Drupal modules and their version changes. For each updated Drupal module, you'll fetch the changelog in Step 11.

**To get the list of updated packages:**

```bash
# Compare composer.lock before and after, or parse composer update output
# The output shows: "Updating drupal/module (1.0.7 => 1.0.9)"
```

Store the list of updates in format: `drupal/[module]: [old_version] → [new_version]` for changelog generation.

### Step 5: Check for Major Version Updates

Get all outdated Drupal modules:

```bash
ddev composer outdated 'drupal/*' --direct --format=json
```

Parse the JSON output and filter for modules with `"latest-status": "update-possible"`. These are major version updates that require explicit version constraint changes.

**Example major updates:**
- `drupal/anchor_link`: 2.7.0 → 3.0.3
- `drupal/webform`: 6.2.0 → 7.0.0

### Step 5.5: Verify Compatibility with Current Drupal Core

For each major update found in Step 5, verify compatibility with current Drupal core:

**Get current Drupal core version:**

```bash
CORE_VERSION=$(ddev composer show drupal/core --format=json | jq -r '.versions[0]')
```

**For each major update, get all available versions:**

```bash
ddev composer show drupal/[module] --all --format=json
```

**Parse the JSON to find compatible versions:**

The output is an array of version objects, each containing:
- `version`: The version number (e.g., "3.0.0", "2.5.1")
- `require.drupal/core`: Core version constraint (e.g., "^10.2", "^11")
- `require.php`: PHP version requirement (e.g., ">=8.1")

**Logic for finding compatible version:**

1. Parse all versions from the JSON output
2. For each version, check if its `require.drupal/core` constraint is satisfied by current core version
3. Find the highest compatible version
4. If the highest compatible version is greater than the currently installed version, present it to the user
5. If the latest version requires Drupal 11 but we have Drupal 10, find the highest Drupal 10-compatible version

**Example constraint checking:**

- Current core: `10.3.5`
- Module version 3.0.0 requires: `^11` → NOT compatible
- Module version 2.5.0 requires: `^10.2` → Compatible
- Module version 2.0.0 requires: `^9.5 || ^10` → Compatible
- Result: Offer version 2.5.0 (highest compatible)

**Constraint syntax reference:**

- `^10.2` = `>=10.2.0 <11.0.0`
- `^11` = `>=11.0.0 <12.0.0`
- `^9.5 || ^10 || ^11` = Multiple versions supported
- `>=10.2` = Any version from 10.2.0 onwards

**Note:** When checking compatibility, compare the module's `require.drupal/core` constraint against the current Drupal core version. If the latest version is incompatible, iterate through available versions (sorted descending) to find the highest version that is compatible with the current core.

### Step 6: Interactive Major Update Selection

For each major update available, present to the user with compatibility information:

**If the latest version is compatible:**

```
Major update available:
- Module: drupal/anchor_link
- Current: 2.7.0
- Latest: 3.0.3 (compatible with current Drupal core)
- Risk: Major version update may contain breaking changes

Update this module? (y/n)
```

**If the latest version is NOT compatible, show recommended version:**

```
Major update available:
- Module: drupal/anchor_link
- Current: 2.7.0
- Latest: 3.0.3 (requires Drupal ^11, not compatible)
- Recommended: 2.9.0 (highest version compatible with Drupal 10.3.5)
- Risk: Major version update may contain breaking changes

Update to version 2.9.0? (y/n)
```

**If no compatible major version exists:**

```
Major update available:
- Module: drupal/anchor_link
- Current: 2.7.0
- Latest: 3.0.3 (requires Drupal ^11, not compatible)
- Warning: No compatible major version found for current Drupal core
- Note: Consider upgrading Drupal core first, or skip this update

Skip this update? (y/n)
```

Build a list of modules the user confirms, along with the compatible version to install for each.

### Step 7: Apply Major Updates

For each confirmed major update, use the compatible version determined in Step 5.5:

```bash
ddev composer require drupal/[module]:^[compatible-version] --update-with-all-dependencies
```

**Examples:**

If compatible version is 2.9.0:
```bash
ddev composer require drupal/anchor_link:^2.9 --update-with-all-dependencies
```

If latest version (3.0.3) is compatible:
```bash
ddev composer require drupal/anchor_link:^3.0 --update-with-all-dependencies
```

**Note:** Always use the compatible version determined in Step 5.5, not necessarily the latest version. This ensures the update will work with the current Drupal core version.

**Handle errors**: If a major update fails due to dependency conflicts:
1. Show the error to the user
2. Ask if they want to continue with other updates
3. Document the failed update in the changelog
4. If the error indicates incompatibility, re-check compatibility in Step 5.5

### Step 8: Database Updates

Run database updates to apply schema changes:

```bash
ddev drush updb -y
```

**Monitor for errors**: If database updates fail, stop immediately and inform the user.

### Step 9: Export Configuration

Export active configuration to sync directory:

```bash
ddev drush config:export -y
```

Verify the export location:

```bash
ddev drush status --field=config-sync
```

### Step 10: Clear Caches

Clear all caches to ensure changes take effect:

```bash
ddev drush cache:rebuild
```

### Step 11: Generate Changelog

Create a changelog file by fetching release notes for **all updates** (security, minor, patch, and major versions).

**For each updated Drupal module, fetch the changelog:**

```bash
ddev exec php [skill-directory]/scripts/fetch_changelog.php drupal/[module] [old_version] [new_version]
```

**Process all updates:**

1. **Security updates** (from Step 3): Fetch changelog for each security update applied
2. **Automatic updates** (from Step 4): Fetch changelog for each minor/patch update
3. **Major updates** (from Step 7): Fetch changelog for each major version update

**Example for multiple updates:**

```bash
# Security update
ddev exec php [skill-directory]/scripts/fetch_changelog.php drupal/admin_toolbar 3.6.2 3.6.3

# Minor update
ddev exec php [skill-directory]/scripts/fetch_changelog.php drupal/admin_audit_trail 1.0.7 1.0.9

# Major update
ddev exec php [skill-directory]/scripts/fetch_changelog.php drupal/anchor_link 2.7.0 3.0.3
```

**If the PHP script is unavailable**, manually create `UPDATES-[DATE].md` with this structure:

```markdown
# Drupal Module Updates - [YYYY-MM-DD]

## Security Updates (Auto-Applied)
[List security updates that were applied]

## Automatic Updates (composer update)
[List all packages updated by composer update - includes patch and minor versions]

For each update, include:
- drupal/admin_audit_trail: 1.0.7 → 1.0.9
  - Release: https://www.drupal.org/project/admin_audit_trail/releases/1.0.9
  - Changes: [Key changes from release notes fetched via fetch_changelog.php script]

## Major Version Updates
[List major updates applied via composer require]
- drupal/anchor_link: 2.7.0 → 3.0.3
  - Command: `composer require drupal/anchor_link:^3.0`
  - Release: https://www.drupal.org/project/anchor_link/releases/3.0.3
  - Changes: [Key changes and breaking changes]

## Post-Update Tasks Completed
- [x] Database updates applied (drush updb)
- [x] Configuration exported (drush cex)
- [x] Caches cleared (drush cr)

## Rollback Instructions
To rollback these updates:
\`\`\`bash
ddev snapshot restore --name=pre-update-[timestamp]
\`\`\`
```

## Validation and Testing

After updates are complete:

### Check for errors:

```bash
ddev drush watchdog:show --count=20 --severity=Error
```

### Verify configuration status:

```bash
ddev drush config:status
```

If there are configuration changes not exported, review them:

```bash
ddev drush config:export --diff
```

### Test critical functionality:

Inform the user to test:
- User authentication
- Content creation/editing
- Forms and submissions
- Any custom functionality

## Error Handling

### Composer Update Fails

If `composer update` fails:

1. Check the error message for dependency conflicts
2. Try updating specific packages that failed:
   ```bash
   ddev composer update drupal/[module] --with-all-dependencies
   ```
3. If still failing, check for known issues on drupal.org

### Database Updates Fail

If `drush updb` fails:

1. Review the error message carefully
2. Check watchdog logs: `ddev drush watchdog:show`
3. Consider rolling back: `ddev snapshot restore --name=[snapshot-name]`
4. Report the issue to the user with full error details

### Configuration Export Issues

If configuration export shows unexpected changes:

1. Review the diff: `ddev drush config:export --diff`
2. Check if changes are expected from the updates
3. If uncertain, ask the user to review before exporting

## Rollback Procedure

If something goes wrong:

```bash
# List available snapshots
ddev snapshot list

# Restore to pre-update state
ddev snapshot restore --name=pre-update-[timestamp]

# Verify restoration
ddev drush status
```

After rollback:
1. Clear caches: `ddev drush cr`
2. Verify site functionality
3. Investigate the issue before attempting updates again

## Common Scenarios

For real-world examples of update workflows including security updates, major version upgrades, compatibility issues, and error recovery, see [examples.md](examples.md).

## Additional Resources

For detailed composer command options, troubleshooting guides, and a quick commands reference, see [reference.md](reference.md).
