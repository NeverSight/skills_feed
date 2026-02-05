---
name: drupal-contrib-mgmt
description: Comprehensive guide for managing Drupal contributed modules via Composer, including updates, patches, version compatibility, and Drupal 11 upgrades. Use when updating modules or resolving dependency issues.
---

# Drupal Contrib Module Management

## Core Update Workflow

### Standard Module Update

```bash
# Update a single module
composer require drupal/module_name --with-all-dependencies

# Update to specific version
composer require drupal/module_name:^3.0 --with-all-dependencies

# Update multiple modules
composer require drupal/module_a drupal/module_b --with-all-dependencies

# After any update, ALWAYS run database updates
drush updb -y

# Clear cache if needed
drush cr

# CRITICAL: Test by visiting pages to check for fatal errors
# Visit at least one page that uses the updated module
```

### Major Version Upgrades

When upgrading to a new major version (e.g., 2.x → 3.x):

1. **Check compatibility**: Ensure module supports your Drupal core version
2. **Search issue queue** for patches: `https://www.drupal.org/project/issues/MODULE_NAME?categories=All`
3. **Use Drupal Lenient** for version requirement issues (see below)
4. **Apply patches** via composer.json (see Patch Management section)
5. **Run upgrade_status** to check for deprecations

## Checking Drupal 11 Compatibility

**Three methods to check if a module is D11 compatible** (in order of preference):

### Method 1: Check .info.yml File (Fastest, Most Reliable)

```bash
# Check the module's .info.yml file for core_version_requirement
cat docroot/modules/contrib/MODULE_NAME/MODULE_NAME.info.yml | grep core_version_requirement
```

**What to look for**:
```yaml
core_version_requirement: ^9.5 || ^10 || ^11     # ✅ D11 compatible
core_version_requirement: ^8 || ^9 || ^10 || ^11  # ✅ D11 compatible
core_version_requirement: ^9 || ^10                # ❌ Not D11 compatible yet
```

**Example**:
```bash
$ cat docroot/modules/contrib/admin_toolbar/admin_toolbar.info.yml | grep core_version
core_version_requirement: ^9.5 || ^10 || ^11
# ✅ This module declares D11 support!
```

### Method 2: Use Composer Commands (Works Before Installing)

```bash
# Check what versions are available and their constraints
composer show drupal/MODULE_NAME --all | grep -A5 "^versions"

# Check currently installed version
composer show drupal/MODULE_NAME | grep versions
```

**What to look for**:
- Version number (e.g., 3.6.2)
- Check Drupal.org for release notes mentioning D11

### Method 3: Check Drupal.org Project Page

Only use as fallback when above methods aren't conclusive.

```
https://www.drupal.org/project/MODULE_NAME
```

Look for:
- Latest release notes mentioning "Drupal 11"
- Module page header showing D11 compatibility badge
- Issue queue for D11 compatibility issues

**Important Notes**:
- ⚠️ Module may declare D11 support but still have deprecation warnings
- ⚠️ upgrade_status warnings don't mean module is incompatible
- ⚠️ "Check manually" status often means runtime version checks (false positive)
- ✅ If .info.yml declares `^11` support, module maintainer says it works

**Real-World Examples**:

```bash
# admin_toolbar - Already D11 compatible
$ cat docroot/modules/contrib/admin_toolbar/admin_toolbar.info.yml | grep core_version
core_version_requirement: ^9.5 || ^10 || ^11

# But upgrade_status shows warnings about _drupal_flush_css_js()
# This is a FALSE POSITIVE - module handles it with version checks

# audiofield - Already D11 compatible
$ cat docroot/modules/contrib/audiofield/audiofield.info.yml | grep core_version
core_version_requirement: ^8 || ^9 || ^10 || ^11

# Has deprecation warnings but maintainer declares D11 support
```

## Drupal Lenient Plugin

The `mglaman/composer-drupal-lenient` plugin allows installing modules that haven't updated their version requirements yet.

### Setup

```json
{
  "require": {
    "mglaman/composer-drupal-lenient": "^1.0"
  },
  "config": {
    "allow-plugins": {
      "mglaman/composer-drupal-lenient": true
    }
  },
  "extra": {
    "drupal-lenient": {
      "allowed-list": [
        "drupal/module_name",
        "drupal/another_module"
      ]
    }
  }
}
```

### Usage

```bash
# Add module to allowed-list, then install
composer require drupal/module_name --with-all-dependencies
```

## Patch Management (cweagans/composer-patches)

### Patch Configuration

```json
{
  "require": {
    "cweagans/composer-patches": "^1.7"
  },
  "config": {
    "allow-plugins": {
      "cweagans/composer-patches": true
    }
  },
  "extra": {
    "patches": {
      "drupal/module_name": {
        "Description of patch": "https://www.drupal.org/files/issues/2024-01-15/module-issue-1234567-8.patch",
        "Local patch": "patches/custom-fix.patch"
      }
    },
    "enable-patching": true,
    "patchLevel": {
      "drupal/core": "-p2"
    }
  }
}
```

### Finding Patches

**Issue Queue Search**: `https://www.drupal.org/project/issues/MODULE_NAME?categories=All`

**Patch Naming Convention**:
- Format: `module-issue-NODEID-COMMENT.patch`
- Example: `audiofield-d11-3432063-12.patch`
- Node ID is the issue number (visit `drupal.org/node/NODEID`)

**When Existing Patches Fail After Update**:
1. Extract node ID from patch filename (e.g., `3432063` from above)
2. Visit `https://www.drupal.org/node/3432063`
3. Look for updated patch in latest comments
4. Update composer.json with new patch URL

### Creating Local Patches

```bash
# Method 1: Git diff
cd docroot/modules/contrib/module_name
# Make your changes
git diff > /path/to/project/patches/module-custom-fix.patch

# Method 2: diff command
diff -Naur original/file.php modified/file.php > patches/module-fix.patch

# Apply in composer.json
{
  "extra": {
    "patches": {
      "drupal/module_name": {
        "Custom fix description": "patches/module-custom-fix.patch"
      }
    }
  }
}
```

### Patch Application

```bash
# Install with patches
composer install

# If patches fail, composer will error
# Update or remove failing patches, then retry
composer install

# Force re-patch
composer update drupal/module_name --with-all-dependencies
```

## Drupal 11 Compatibility Workflow

### Step 1: Analyze Readiness

```bash
# Scan all modules
drush upgrade_status:analyze --all

# Scan specific modules
drush upgrade_status:analyze module1 module2 module3

# Machine-readable output
drush upgrade_status:analyze --all --format=json > d11-report.json
drush upgrade_status:analyze --all --format=codeclimate > d11-report-ci.json

# Scan only custom code
drush upgrade_status:analyze --all --ignore-contrib

# Scan only contrib
drush upgrade_status:analyze --all --ignore-custom
```

### Step 2: Identify Issues

**Major Issues** (blocking):
- `REQUEST_TIME` constant → Use `\Drupal::time()->getRequestTime()`
- `user_roles()` → Use `\Drupal\user\Entity\Role::loadMultiple()`
- `file_validate_extensions()` → Use `file.validator` service
- `system_retrieve_file()` → No replacement (refactor required)
- `_drupal_flush_css_js()` → Use `AssetQueryStringInterface::reset()`

**Info.yml Issues**:
- Update `core_version_requirement` to include `^11`
- Example: `core_version_requirement: ^9 || ^10 || ^11`

### Step 3: Fix Custom Code

**Example: Inject Time Service**

```php
use Drupal\Core\Datetime\TimeInterface;

class MyController extends ControllerBase {
  protected $time;

  public function __construct(TimeInterface $time) {
    $this->time = $time;
  }

  public static function create(ContainerInterface $container) {
    return new static(
      $container->get('datetime.time')
    );
  }

  public function myMethod() {
    // OLD: $timestamp = REQUEST_TIME;
    $timestamp = $this->time->getRequestTime();
  }
}
```

**Example: Replace user_roles()**

```php
// OLD:
$roles = user_roles(TRUE);

// NEW:
use Drupal\user\Entity\Role;

$roles = Role::loadMultiple();
$role_options = [];
foreach ($roles as $role_id => $role) {
  if ($role_id !== 'anonymous') {
    $role_options[$role_id] = $role->label();
  }
}
```

### Step 4: Create .info.yml Patches

```bash
# Create patch for contrib module
cd docroot/modules/contrib/module_name
git diff module.info.yml > /path/to/patches/module-d11-info.patch

# Patch content:
--- a/module.info.yml
+++ b/module.info.yml
@@ -2,7 +2,7 @@
 name: Module Name
 type: module
 description: Module description
-core_version_requirement: ^9 || ^10
+core_version_requirement: ^9 || ^10 || ^11
```

### Step 5: Apply Patches & Update Lenient List

```json
{
  "extra": {
    "patches": {
      "drupal/module_name": {
        "Drupal 11 .info.yml support": "patches/module-d11-info.patch"
      }
    },
    "drupal-lenient": {
      "allowed-list": [
        "drupal/module_name"
      ]
    }
  }
}
```

```bash
composer install
drush updb -y
drush cr
```

### Step 6: Verify Fixes

```bash
# Re-scan to confirm issues resolved
drush upgrade_status:analyze module_name

# Should show "No known issues found"
```

## Complete Update Checklist

- [ ] Check current module version: `composer show drupal/module_name`
- [ ] Search issue queue for known issues
- [ ] Check if module is D11 compatible
- [ ] Update composer.json with new version
- [ ] Add to drupal-lenient if needed
- [ ] Search for and apply necessary patches
- [ ] Run `composer require drupal/module_name:^X.0 --with-all-dependencies`
- [ ] Run `drush updb -y`
- [ ] Run `drush cr`
- [ ] Run `drush upgrade_status:analyze module_name`
- [ ] Test module functionality by visiting relevant pages
- [ ] Check for PHP errors/warnings in logs
- [ ] Commit changes with descriptive message

## Troubleshooting

### Patch Won't Apply

```bash
# Error: "Cannot apply patch..."
# 1. Check if module version changed
composer show drupal/module_name

# 2. Search issue queue for updated patch
# Visit drupal.org/node/NODEID (from patch filename)

# 3. Update composer.json with new patch URL
# 4. Or remove patch if merged upstream
```

### Version Conflict

```bash
# Error: "drupal/module_name requires drupal/core ^9"
# Add to drupal-lenient allowed-list
```

### Patch Already Applied

```bash
# Error: "patch ... has already been applied"
# Module maintainer merged the patch - remove from composer.json
```

### Database Update Fails

```bash
# Error during drush updb
# 1. Check error message carefully
# 2. May need to disable module, update, re-enable
drush pm:uninstall module_name
composer require drupal/module_name --with-all-dependencies
drush pm:enable module_name
drush updb -y
```

## Best Practices

1. **Always use `--with-all-dependencies`** for module updates
2. **Always run `drush updb`** after composer updates
3. **Test immediately** after updates (visit pages, check logs)
4. **Keep patches organized** in a `patches/` directory
5. **Document patches** with descriptive names and comments
6. **Check issue queues first** before creating custom patches
7. **Use upgrade_status** to validate D11 compatibility
8. **Commit atomically**: one module update per commit
9. **Use descriptive commit messages** with patch references
10. **Keep drupal-lenient list minimal** (only when necessary)

## Developing Contrib Modules Locally

When actively developing a contrib module for drupal.org, use this workflow to avoid constantly updating via composer:

### Symlink Development Workflow

```bash
# 1. Set up module repository in temp location
cd /tmp
git clone git@git.drupal.org:project/module_name.git
cd module_name
# Make your changes...

# 2. Remove composer-installed version and symlink your dev copy
cd /path/to/project
rm -rf docroot/modules/contrib/module_name
ln -s /tmp/module_name docroot/modules/contrib/module_name

# 3. Develop and test
# Make changes in /tmp/module_name
# Test immediately in your Drupal site
drush cr  # Clear cache as needed

# 4. When ready to publish
cd /tmp/module_name
git add -A
git commit -m "Your changes"
git push origin 1.0.x

# 5. Clean up: remove symlink and reinstall from composer
cd /path/to/project
rm docroot/modules/contrib/module_name
composer install  # Reinstalls from drupal.org
```

**Benefits**:
- Test changes immediately without composer update cycles
- Keep git history in the module's own repo
- Easy to commit and push changes
- No risk of accidentally committing module code to main project

**Important Notes**:
- Don't forget to remove the symlink before committing project changes
- Clear Drupal cache after changes: `drush cr`
- When done developing, always reinstall via composer to ensure clean state
- Useful for fixing autoloader issues, adding features, or troubleshooting

**Example**: Fixing recurly_commerce_api autoloader issue
```bash
# Module needed composer.json autoload section
cd /tmp/recurly_commerce_api
# Edit composer.json to add autoload section
git commit -m "Add PSR-4 autoload configuration"
git push origin 1.0.x

# Back in main project
rm docroot/modules/contrib/recurly_commerce_api
composer install  # Gets latest with fix
drush cr
```

## Common Patterns

### Pattern: Update Module with Known Patch

```bash
# 1. Find patch in issue queue
# 2. Add to composer.json patches section
# 3. Update module
composer require drupal/module_name:^3.0 --with-all-dependencies
drush updb -y
drush cr
# 4. Test
# 5. Commit
git add composer.json composer.lock patches/
git commit -m "Update module_name to 3.0 with D11 compatibility patch"
```

### Pattern: Fix Contrib D11 Issue

```bash
# 1. Scan for issues
drush upgrade_status:analyze module_name

# 2. Create info.yml patch if needed
cd docroot/modules/contrib/module_name
# Edit module.info.yml to add ^11
git diff module.info.yml > ../../../patches/module-d11-info.patch

# 3. Add patch to composer.json
# 4. Apply
composer install
drush cr

# 5. Verify
drush upgrade_status:analyze module_name
```

### Pattern: Major Version Upgrade with Breaking Changes

```bash
# 1. Read CHANGELOG/UPDATE.md for breaking changes
# 2. Check issue queue for upgrade path documentation
# 3. Backup database before upgrade
drush sql:dump > backup-before-update.sql

# 4. Update module
composer require drupal/module_name:^3.0 --with-all-dependencies

# 5. Run updates
drush updb -y

# 6. Check for errors
drush watchdog:show --severity=Error --count=20

# 7. Test thoroughly
# 8. If issues, can rollback:
# git checkout composer.json composer.lock
# composer install
# drush sql:cli < backup-before-update.sql
```

## Reference Links

- **Composer Patches**: https://github.com/cweagans/composer-patches
- **Drupal Lenient**: https://github.com/mglaman/composer-drupal-lenient
- **Upgrade Status Module**: https://www.drupal.org/project/upgrade_status
- **Drupal 11 Deprecations**: https://www.drupal.org/about/core/policies/core-change-policies/drupal-deprecation-policy
- **Patch Naming Standards**: https://www.drupal.org/node/1054616
