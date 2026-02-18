---
name: typo3-workspaces
description: >-
  Expert guidance on TYPO3 Workspaces: versioning, staging, publishing workflows,
  file limitations, file collection workspace safety, query migration, debugging,
  and testing. Use when working with workspace, versioning, staging, publishing,
  review, draft content, workflow, file collection.
compatibility: TYPO3 13.0 - 14.x
metadata:
  version: "1.0.0"
---

# TYPO3 Workspaces

> **Compatibility:** TYPO3 v13.x and v14.x (v14 preferred)
> All code examples in this skill are designed to work on both TYPO3 v13 and v14.

> **TYPO3 API First:** Always use TYPO3's built-in APIs, core features, and established conventions before creating custom implementations. Do not reinvent what TYPO3 already provides. Always verify that the APIs and methods you use exist and are not deprecated in your target TYPO3 version (v13 or v14) by checking the official TYPO3 documentation.

## Sources

This skill is based on 18 authoritative sources:

1. [TYPO3 Workspaces Extension Docs](https://docs.typo3.org/c/typo3/cms-workspaces/main/en-us/Index.html)
2. [Versioning (Workspaces Extension)](https://docs.typo3.org/c/typo3/cms-workspaces/main/en-us/Administration/Versioning/Index.html)
3. [Creating a Custom Workspace](https://docs.typo3.org/c/typo3/cms-workspaces/main/en-us/Administration/CustomWorkspace/Index.html)
4. [Configuration Options (Workspaces)](https://docs.typo3.org/c/typo3/cms-workspaces/main/en-us/Administration/Configuration/Index.html)
5. [PSR-14 Events (Workspaces)](https://docs.typo3.org/c/typo3/cms-workspaces/main/en-us/Events/Index.html)
6. [Versioning & Workspaces (TYPO3 Explained / Core API)](https://docs.typo3.org/m/typo3/reference-coreapi/main/en-us/ApiOverview/Workspaces/Index.html)
7. [TCA versioningWS Reference](https://docs.typo3.org/m/typo3/reference-tca/main/en-us/Ctrl/Properties/VersioningWSAlwaysAllowLiveEdit.html)
8. [Restriction Builder (TYPO3 Explained)](https://docs.typo3.org/m/typo3/reference-coreapi/main/en-us/ApiOverview/Database/RestrictionBuilder/Index.html)
9. [b13 Blog: The Elegant Efficiency of TYPO3 Overlays (Benni Mack)](https://b13.com/blog/mastering-localization-and-content-staging)
10. [Scheduler Tasks (Workspaces)](https://docs.typo3.org/c/typo3/cms-workspaces/main/en-us/Administration/Scheduler/Index.html)
11. [Users Guide (Workspaces)](https://docs.typo3.org/c/typo3/cms-workspaces/main/en-us/UsersGuide/Index.html)
12. [TYPO3-CORE-SA-2025-022: Information Disclosure in Workspaces Module](https://typo3.org/security/advisory/typo3-core-sa-2025-022)
13. [Forge Bug #88021: FAL preview fails when file changed in workspace](https://forge.typo3.org/issues/88021)
14. [Localized Content Guide](https://docs.typo3.org/m/typo3/guide-frontendlocalization/main/en-us/LocalizedContent/Index.html)
15. [File Collections (TYPO3 Explained)](https://docs.typo3.org/m/typo3/reference-coreapi/main/en-us/ApiOverview/Fal/Collections/Index.html)
16. [FAL Database Architecture](https://docs.typo3.org/m/typo3/reference-coreapi/main/en-us/ApiOverview/Fal/Architecture/Database.html)
17. [Forge Bug #60343: sys_file_metadata does not recognize workspace](https://forge.typo3.org/issues/60343)
18. [Forge Feature #97923: Combined folder_identifier field for sys_file_collection](https://forge.typo3.org/issues/97923)

## 1. Core Concepts

### What Are Workspaces?

Workspaces allow editors to prepare content changes **without affecting the live website**. Changes go through a configurable review process before publication.

There are two types:

- **LIVE workspace** (ID=0): The default state. Every change is immediately visible. Access must be **explicitly granted** to backend users/groups.
- **Custom workspaces** (ID>0): Safe editing environments. Changes are versioned, previewable, and go through stages before going live.

### How Versioning Works (Database Level)

Offline (workspace) versions live in the **same database table** as live records. They are identified by:

| Field | Purpose |
|-------|---------|
| `t3ver_oid` | Points to the live record's `uid` (0 for live records) |
| `t3ver_wsid` | Workspace ID this version belongs to (0 for live) |
| `t3ver_state` | Special state flags (see below) |
| `t3ver_stage` | Workflow stage (0=editing, -10=ready to publish) |
| `pid` | Set to `-1` for all offline versions |

**t3ver_state values:**

| Value | Meaning |
|-------|---------|
| `-1` | New placeholder version (workspace pendant for new record) |
| `0` | Default: workspace modification of existing record |
| `1` | New placeholder (live pendant, insertion point for sorting) |
| `2` | Delete placeholder (record marked for deletion upon publish) |
| `3` | Move placeholder (live placeholder, hidden online, linked via `t3ver_move_id`) |
| `4` | Move pointer (workspace pendant of record to be moved) |

### The Overlay Mechanism

TYPO3 **always fetches live records first**, then overlays workspace versions on top. For translations with workspaces, the chain is:

1. Fetch default language, live record (language=0, workspace=0)
2. Overlay workspace version (search for `t3ver_oid=<uid>` AND `t3ver_wsid=<current_ws>`)
3. Overlay language translation (search for `l10n_parent=<uid>` in target language)
4. Overlay workspace version of translation

The `uid` of the live record is **always preserved** during overlay -- this keeps all references and links intact.

### Publishing Workflow

- **Publish**: Draft content replaces live content through the workspace publish process.
- TYPO3 v13/v14 use publish workflows; do not rely on legacy workspace-level swap mode.
- **IMPORTANT**: The `swap` action is no longer allowed in TYPO3 v14. Use `action => 'publish'` instead of `action => 'swap'`.

## 2. CRITICAL: File/FAL Limitation

> **Files (FAL) are NOT versioned.** This is the single most important limitation of TYPO3 Workspaces.
> See also Section 2a below for the additional **file collection** limitation (folder-based collections).

### What This Means

- Files in `fileadmin/` live exclusively in the **LIVE workspace**
- If you **overwrite** a file, the change affects **ALL workspaces immediately**
- `sys_file_reference` records are workspace-versioned; physical files and `sys_file` records are not versioned like content overlays
- Replacing an image in a workspace content element may fail in preview (Forge #88021)

### The Predictable Filename Security Problem

**Scenario:** An editor creates a workspace version of a page replacing `geschaeftsbericht2024.pdf` with `geschaeftsbericht2025.pdf`. The workspace is NOT published yet. However:

1. The new PDF is uploaded to `fileadmin/` immediately (files are live!)
2. An external person guesses the URL by incrementing the year
3. `geschaeftsbericht2025.pdf` is accessible before the content element referencing it is published

This is a **real security/confidentiality risk**.

### Workarounds

**1. Use non-guessable filenames:**

```
# Instead of:
fileadmin/reports/geschaeftsbericht2025.pdf

# Use hashed/random names:
fileadmin/reports/gb-a8f3e2b1c9d4.pdf
```

**2. Store confidential files outside the web root:**

```php
// config/system/settings.php
// Use a private storage that is NOT publicly accessible
// Deliver files programmatically via a controller
```

**3. Use EXT:secure_downloads (leuchtfeuer/secure-downloads):**

Files are delivered through a PHP script that checks access permissions. No direct file URL access.

**4. Server-level protection for sensitive directories:**

```apache
# Apache (.htaccess in a subdirectory)
<IfModule mod_authz_core.c>
    Require all denied
</IfModule>
```

```nginx
# NGINX
location /fileadmin/confidential/ {
    deny all;
    return 403;
}
```

**5. Use separate file references per workspace version:**

Upload the new file with a different name. Do NOT overwrite the existing file. The workspace version of the content element references the new file, the live version keeps the old one. Upon publishing, both files exist but only the new one is referenced.

### Rules for Workspace-Safe File Handling

- **NEVER** overwrite files that are used in content elements across workspaces
- **ALWAYS** upload new files with unique names when preparing workspace content
- **NEVER** rely on "the page is not published yet" to protect file confidentiality
- **CONSIDER** EXT:secure_downloads for any confidential documents
- **AUDIT** `fileadmin/` for files with predictable naming patterns

## 2a. File Collections and Workspaces

> **File collections (`sys_file_collection`) are workspace-versioned at the record level, but folder-based collections resolve files from the live filesystem at runtime -- there is no database relation to overlay.**

### How File Collections Work

`sys_file_collection` stores three collection types, distinguished by the `type` field:

| `type` value | Resolution mechanism | Database relations involved |
|---|---|---|
| `static` (0) | `sys_file_reference` rows (`tablenames='sys_file_collection'`, `fieldname='files'`) | One `sys_file_reference` row per file |
| `folder` (1) | `folder_identifier` string (e.g. `1:/user_upload/gallery/`) | **None** -- no join table, no reference rows |
| `category` (2) | `category` uid resolved via `sys_category_record_mm` | MM table (handled via parent record overlay) |

The TCA for `sys_file_collection` has `versioningWS => true`. This means the **collection record itself** gets workspace versions with `t3ver_*` fields. However, the record-level versioning only versions the fields stored in `sys_file_collection` -- it does **not** version the files that the collection resolves.

### Workspace Safety per Collection Type

| Collection Type | Record versioned? | File binding versioned? | Physical files versioned? | Workspace-safe? |
|---|---|---|---|---|
| **Static** | Yes | Yes (`sys_file_reference` has `versioningWS = true`) | No | Partially safe |
| **Folder-based** | Yes (record only) | **No** -- no DB binding exists | No | **Not safe** |
| **Category-based** | Yes | Partially (category MM handled via parent overlay) | No | Partially safe |

### Why Folder-Based Collections Break Workspace Isolation

For folder-based collections, the "relation" between the collection and its files is **not a database relation**. The collection record stores only a `folder_identifier` string. When `FolderBasedFileCollection::loadContents()` is called, TYPO3 calls `$storage->getFilesInFolder()` to list files directly from the live storage driver. There is no overlay-capable database row between the collection and its files.

**Consequences:**

- Adding a file to the folder makes it visible in **all workspaces** immediately
- Removing a file from the folder removes it from **all workspaces** immediately
- Changing the `folder_identifier` field in a workspace version points to a different folder, but the folder contents themselves are always live
- The "File links" content element (`CType=uploads`) using a folder-based collection will show different files than intended during workspace preview if the folder contents changed after the workspace version was created

### Static Collections Are Safer

Static collections (`type=static`) bind files via `sys_file_reference` rows. Both `sys_file_collection` and `sys_file_reference` have `versioningWS = true`. When you add or remove a file from a static collection inside a workspace, TYPO3 creates workspace versions of the `sys_file_reference` rows. The binding between collection and file is versioned.

The remaining limitation: physical files (`sys_file`) are still not versioned (see Section 2). If you overwrite a file, it changes everywhere.

### Workarounds for Folder-Based Collections

**1. Prefer static collections when workspace isolation matters:**

Use `type=static` instead of `type=folder`. The file-to-collection binding is a `sys_file_reference` row, which is workspace-versioned.

**2. Use separate folders per workspace version:**

For folder-based collections, create a new folder for the workspace change (e.g. `gallery-v2/`) and change the `folder_identifier` in the workspace version of the collection record. The live version still points to the original folder.

**3. Do NOT modify shared folder contents while workspace drafts reference them:**

If a folder-based collection is used in workspace content, avoid adding or removing files from that folder until the workspace is published.

**4. Clean up old folders after publishing:**

Use `AfterRecordPublishedEvent` to remove obsolete folders after the workspace version is published:

```php
<?php

declare(strict_types=1);

namespace MyVendor\MyExtension\EventListener;

use TYPO3\CMS\Core\Attribute\AsEventListener;
use TYPO3\CMS\Core\Resource\StorageRepository;
use TYPO3\CMS\Workspaces\Event\AfterRecordPublishedEvent;

#[AsEventListener]
final class CleanupOldCollectionFolderListener
{
    public function __construct(
        private readonly StorageRepository $storageRepository,
    ) {}

    public function __invoke(AfterRecordPublishedEvent $event): void
    {
        if ($event->getTable() !== 'sys_file_collection') {
            return;
        }

        // After publishing a folder-based collection, remove the old folder
        // if it is no longer referenced by any collection.
        // Implementation depends on your naming convention (e.g. gallery-v1/, gallery-v2/).
    }
}
```

### Rules for Workspace-Safe File Collections

- **PREFER** static collections (`type=static`) over folder-based when workspaces are used
- **NEVER** add or remove files from a folder that is referenced by a folder-based collection in an unpublished workspace
- **USE** separate folders per workspace version if folder-based collections are required
- **DOCUMENT** for editors that folder-based collections show live folder contents regardless of workspace state
- **TEST** file collection behavior in workspace preview before relying on it for editorial workflows

## 3. Installation & Setup Checklist

### Installation

```bash
# Composer (v13/v14)
composer require typo3/cms-workspaces

# Non-Composer: activate in Admin Tools > Extensions
```

### Complete Setup Checklist

Use this checklist to verify your workspace setup is complete:

#### Extension & System

- [ ] `typo3/cms-workspaces` is installed and activated
- [ ] Database schema is up to date (`bin/typo3 database:updateschema`)
- [ ] `typo3/cms-scheduler` is installed (required for auto-publish)
- [ ] Scheduler cron job is configured on server

#### Backend User Groups

- [ ] Workspace-specific backend user group created (e.g., "Workspace Editors")
- [ ] Group has **explicit LIVE workspace access** (Mounts and Workspaces tab > "Live" checkbox)
- [ ] Group has access to the custom workspace (assigned as owner or member in workspace record)
- [ ] DB mounts are set correctly (pages the group can edit)
- [ ] File mounts are set correctly (directories the group can access)
- [ ] Group has `tables_modify` permissions for all relevant tables
- [ ] Group has permissions on page types the workspace will contain

#### Backend Users

- [ ] Users are assigned to the workspace user group
- [ ] Users can see the workspace selector in the top bar
- [ ] Non-admin users have LIVE workspace access only if they need it

#### Workspace Record

- [ ] Workspace record created as System Record on root page (pid=0)
- [ ] Title and description set
- [ ] **Owners** assigned (use groups, not individual users)
- [ ] **Members** assigned (use groups, not individual users)
- [ ] Custom stages created if needed (between "Editing" and "Ready to publish")
- [ ] Notification settings configured per stage
- [ ] Mountpoints set if workspace should be restricted to specific page trees
- [ ] Publish date set if auto-publish is desired
- [ ] "Publish access" configured (restrict publishing to owners if needed)

#### Tables (TCA)

- [ ] All custom extension tables have `'versioningWS' => true` in `$GLOBALS['TCA'][<table>]['ctrl']`
- [ ] Tables that must NOT be versioned have `'versioningWS' => false`
- [ ] Tables requiring live-editing in workspace have `'versioningWS_alwaysAllowLiveEdit' => true`
- [ ] `t3ver_*` database columns exist (auto-created when `versioningWS = true`)

#### Scheduler Tasks

- [ ] "Workspaces auto-publication" task created and enabled
- [ ] "Workspaces cleanup preview links" task created and enabled
- [ ] Cron frequency is appropriate (e.g., every 15 minutes)

#### TSconfig

- [ ] `options.workspaces.previewLinkTTLHours` set (default: 48)
- [ ] `options.workspaces.allowed_languages.<wsId>` set if language restrictions needed
- [ ] `workspaces.splitPreviewModes` configured if preview modes should be limited
- [ ] `options.workspaces.previewPageId` set for custom record preview pages

## 4. DataHandler Setup Script

### CLI Command: Create Workspace with DataHandler

```php
<?php

declare(strict_types=1);

namespace MyVendor\MySitepackage\Command;

use Symfony\Component\Console\Command\Command;
use Symfony\Component\Console\Input\InputInterface;
use Symfony\Component\Console\Output\OutputInterface;
use Symfony\Component\Console\Style\SymfonyStyle;
use TYPO3\CMS\Core\DataHandling\DataHandler;
use TYPO3\CMS\Core\Utility\GeneralUtility;

/**
 * CLI command to create a workspace with base configuration.
 *
 * Register in Configuration/Services.yaml:
 *   console.command.tag: 'console.command'
 *   command: 'workspace:setup'
 */
final class SetupWorkspaceCommand extends Command
{
    protected function configure(): void
    {
        $this->setDescription('Create a workspace with backend group and base configuration');
    }

    protected function execute(InputInterface $input, OutputInterface $output): int
    {
        $io = new SymfonyStyle($input, $output);

        // Step 1: Create backend user group for workspace editors
        $data = [];
        $data['be_groups']['NEW_ws_group'] = [
            'pid' => 0,
            'title' => 'Workspace Editors',
            'description' => 'Backend group for workspace editing access',
            // Grant access to common tables
            'tables_modify' => 'pages,tt_content,sys_file_reference',
            'tables_select' => 'pages,tt_content,sys_file_reference,sys_file',
            // Grant LIVE workspace access
            'workspace_perms' => 1,
            // Page types allowed
            'pagetypes_select' => '1,3,4,6,7,199,254',
            // Explicitly allow content types
            'explicit_allowdeny' => '',
        ];

        $dataHandler = GeneralUtility::makeInstance(DataHandler::class);
        $dataHandler->start($data, []);
        $dataHandler->process_datamap();

        if (!empty($dataHandler->errorLog)) {
            $io->error('Failed to create backend group: ' . implode(', ', $dataHandler->errorLog));
            return Command::FAILURE;
        }

        $groupUid = $dataHandler->substNEWwithIDs['NEW_ws_group'] ?? 0;
        $io->success('Created backend group "Workspace Editors" (uid=' . $groupUid . ')');

        // Step 2: Create the custom workspace
        $data = [];
        $data['sys_workspace']['NEW_workspace'] = [
            'pid' => 0,
            'title' => 'Staging Workspace',
            'description' => 'Content staging workspace for preview and review before publishing',
            'adminusers' => 'be_groups_' . $groupUid,
            'members' => 'be_groups_' . $groupUid,
            // Stages: default stages (Editing, Ready to publish) are always available
            // Publish access: 0 = no restriction, 1 = only publish-stage content, 2 = only owners can publish
            'publish_access' => 0,
            // Allow editing of non-versionable records (live edit)
            'edit_allow_notificaton_settings' => 0,
        ];

        $dataHandler = GeneralUtility::makeInstance(DataHandler::class);
        $dataHandler->start($data, []);
        $dataHandler->process_datamap();

        if (!empty($dataHandler->errorLog)) {
            $io->error('Failed to create workspace: ' . implode(', ', $dataHandler->errorLog));
            return Command::FAILURE;
        }

        $wsUid = $dataHandler->substNEWwithIDs['NEW_workspace'] ?? 0;
        $io->success('Created workspace "Staging Workspace" (uid=' . $wsUid . ')');

        $io->section('Next Steps');
        $io->listing([
            'Assign backend users to the "Workspace Editors" group',
            'Configure DB mounts and file mounts on the group',
            'Set up Scheduler tasks: "Workspaces auto-publication" + "Workspaces cleanup preview links"',
            'Configure TSconfig: options.workspaces.previewLinkTTLHours = 48',
            'Test: switch to the workspace in the backend top bar and edit a page',
        ]);

        return Command::SUCCESS;
    }
}
```

**Register in `Configuration/Services.yaml`:**

```yaml
services:
  MyVendor\MySitepackage\Command\SetupWorkspaceCommand:
    tags:
      - name: 'console.command'
        command: 'workspace:setup'
        description: 'Create workspace with base configuration'
```

**Run:**

```bash
# DDEV
ddev exec bin/typo3 workspace:setup

# Non-DDEV
bin/typo3 workspace:setup
```

### SQL Setup (LOCAL DDEV ONLY)

> **WARNING: These SQL queries are for LOCAL DDEV development environments ONLY.**
> **NEVER run raw SQL on production.** Use the DataHandler CLI command above instead.
> Raw SQL bypasses DataHandler, reference index, history, and cache clearing.

```sql
-- ============================================================
-- LOCAL DDEV ONLY - Workspace base configuration
-- Save this block as setup-workspace.sql, then run: ddev mysql < setup-workspace.sql
-- ============================================================

-- 1. Create backend user group for workspace editors
INSERT INTO be_groups (pid, title, description, workspace_perms, tables_modify, tables_select, pagetypes_select, tstamp, crdate)
VALUES (
    0,
    'Workspace Editors',
    'Backend group for workspace editing access',
    1,  -- 1 = access to LIVE workspace
    'pages,tt_content,sys_file_reference',
    'pages,tt_content,sys_file_reference,sys_file',
    '1,3,4,6,7,199,254',
    UNIX_TIMESTAMP(),
    UNIX_TIMESTAMP()
);

SET @group_uid = LAST_INSERT_ID();

-- 2. Create custom workspace
INSERT INTO sys_workspace (pid, title, description, adminusers, members, publish_access, tstamp, crdate)
VALUES (
    0,
    'Staging Workspace',
    'Content staging workspace for preview and review before publishing',
    CONCAT('be_groups_', @group_uid),
    CONCAT('be_groups_', @group_uid),
    0,  -- 0 = no publish restriction
    UNIX_TIMESTAMP(),
    UNIX_TIMESTAMP()
);

SET @ws_uid = LAST_INSERT_ID();

-- 3. Verify
SELECT 'Backend Group' AS type, @group_uid AS uid, 'Workspace Editors' AS title
UNION ALL
SELECT 'Workspace' AS type, @ws_uid AS uid, 'Staging Workspace' AS title;

-- 4. Check existing workspace-enabled tables
SELECT TABLE_NAME
FROM information_schema.COLUMNS
WHERE COLUMN_NAME = 't3ver_oid'
  AND TABLE_SCHEMA = DATABASE()
ORDER BY TABLE_NAME;
```

```bash
# Run in DDEV:
ddev mysql < setup-workspace.sql
```

## 5. Making Extensions Workspace-Compatible

### Step 1: Enable versioningWS in TCA

```php
<?php
// EXT:my_extension/Configuration/TCA/tx_myextension_domain_model_item.php

return [
    'ctrl' => [
        'title' => 'LLL:EXT:my_extension/Resources/Private/Language/locallang_db.xlf:tx_myextension_domain_model_item',
        'label' => 'title',
        'tstamp' => 'tstamp',
        'crdate' => 'crdate',
        'delete' => 'deleted',
        'sortby' => 'sorting',
        // Enable workspace versioning
        'versioningWS' => true,
        // Language support
        'languageField' => 'sys_language_uid',
        'transOrigPointerField' => 'l10n_parent',
        'transOrigDiffSourceField' => 'l10n_diffsource',
        'translationSource' => 'l10n_source',
        'enablecolumns' => [
            'disabled' => 'hidden',
            'starttime' => 'starttime',
            'endtime' => 'endtime',
        ],
        'iconfile' => 'EXT:my_extension/Resources/Public/Icons/item.svg',
    ],
    // ... columns, types, palettes
];
```

The `t3ver_*` database columns are **auto-created** when `versioningWS = true` -- you do NOT need to add them to `ext_tables.sql`.

After enabling, run:

```bash
bin/typo3 database:updateschema
```

### Step 2: Disable Versioning for Specific Tables

If a table must NOT be versioned (e.g., logging, statistics):

```php
<?php
// EXT:my_extension/Configuration/TCA/Overrides/tx_myextension_log.php

$GLOBALS['TCA']['tx_myextension_log']['ctrl']['versioningWS'] = false;
```

### Step 3: Allow Live Editing in Workspaces

For tables that should always be edited live (e.g., user settings, configuration):

```php
<?php
// EXT:my_extension/Configuration/TCA/Overrides/tx_myextension_settings.php

// Records of this table are edited live even when a workspace is active
$GLOBALS['TCA']['tx_myextension_settings']['ctrl']['versioningWS_alwaysAllowLiveEdit'] = true;
```

### Step 4: Backend Overlay (REQUIRED for Backend Modules)

```php
<?php

declare(strict_types=1);

namespace MyVendor\MyExtension\Controller;

use TYPO3\CMS\Backend\Utility\BackendUtility;
use TYPO3\CMS\Core\Database\Connection;
use TYPO3\CMS\Core\Database\ConnectionPool;

final class BackendItemController
{
    public function __construct(
        private readonly ConnectionPool $connectionPool,
    ) {}

    /**
     * Fetch a single record with workspace overlay.
     */
    public function getItem(int $uid): ?array
    {
        // Option A: One-liner (recommended)
        $row = BackendUtility::getRecordWSOL('tx_myextension_domain_model_item', $uid);

        // Option B: Manual (equivalent to A)
        // $row = BackendUtility::getRecord('tx_myextension_domain_model_item', $uid);
        // BackendUtility::workspaceOL('tx_myextension_domain_model_item', $row);

        return is_array($row) ? $row : null;
    }

    /**
     * Fetch multiple records with workspace overlay.
     */
    public function getItemsByPage(int $pageId): array
    {
        $queryBuilder = $this->connectionPool
            ->getQueryBuilderForTable('tx_myextension_domain_model_item');

        $result = $queryBuilder
            ->select('*')
            ->from('tx_myextension_domain_model_item')
            ->where(
                $queryBuilder->expr()->eq(
                    'pid',
                    $queryBuilder->createNamedParameter($pageId, Connection::PARAM_INT)
                )
            )
            ->executeQuery();

        $items = [];
        while ($row = $result->fetchAssociative()) {
            // CRITICAL: Apply workspace overlay to each row
            BackendUtility::workspaceOL('tx_myextension_domain_model_item', $row);
            if (is_array($row)) {
                $items[] = $row;
            }
        }

        return $items;
    }
}
```

### Step 5: Frontend Overlay (REQUIRED for Frontend Plugins)

```php
<?php

declare(strict_types=1);

namespace MyVendor\MyExtension\Service;

use TYPO3\CMS\Core\Database\Connection;
use TYPO3\CMS\Core\Database\ConnectionPool;
use TYPO3\CMS\Core\Domain\Repository\PageRepository;

final class ItemService
{
    public function __construct(
        private readonly ConnectionPool $connectionPool,
        private readonly PageRepository $pageRepository,
    ) {}

    /**
     * Fetch items with workspace + language overlay for frontend rendering.
     */
    public function findByPage(int $pageId): array
    {
        $queryBuilder = $this->connectionPool
            ->getQueryBuilderForTable('tx_myextension_domain_model_item');

        $result = $queryBuilder
            ->select('*')
            ->from('tx_myextension_domain_model_item')
            ->where(
                $queryBuilder->expr()->eq(
                    'pid',
                    $queryBuilder->createNamedParameter($pageId, Connection::PARAM_INT)
                )
            )
            ->executeQuery();

        $items = [];
        while ($row = $result->fetchAssociative()) {
            // Apply workspace overlay (MUST be called before language overlay)
            $this->pageRepository->versionOL('tx_myextension_domain_model_item', $row);
            if (!is_array($row)) {
                continue;
            }
            // Apply language overlay
            $row = $this->pageRepository->getLanguageOverlay(
                'tx_myextension_domain_model_item',
                $row
            );
            if (is_array($row)) {
                $items[] = $row;
            }
        }

        return $items;
    }
}
```

### Step 6: Backend Module Workspace Restriction

```php
<?php
// EXT:my_extension/Configuration/Backend/Modules.php

return [
    'my_module' => [
        'parent' => 'web',
        'position' => ['after' => 'web_info'],
        'access' => 'user',
        // Control workspace availability:
        // '*'       = available in all workspaces (default)
        // 'live'    = only available in live workspace
        // 'offline' = only available in custom workspaces
        'workspaces' => '*',
        'iconIdentifier' => 'my-module-icon',
        'labels' => 'LLL:EXT:my_extension/Resources/Private/Language/locallang_mod.xlf',
        'routes' => [
            '_default' => [
                'target' => \MyVendor\MyExtension\Controller\MyModuleController::class . '::handleRequest',
            ],
        ],
    ],
];
```

## 6. Migrating Queries: WITHOUT Workspaces to WITH Workspaces

### Pattern A: Backend QueryBuilder (Before/After)

**BEFORE (no workspace awareness):**

```php
<?php
// WRONG: Does not respect workspaces
$queryBuilder = $this->connectionPool->getQueryBuilderForTable('tt_content');
$rows = $queryBuilder
    ->select('*')
    ->from('tt_content')
    ->where(
        $queryBuilder->expr()->eq('pid', $queryBuilder->createNamedParameter($pageId, Connection::PARAM_INT))
    )
    ->executeQuery()
    ->fetchAllAssociative();

// Rows may include workspace placeholders and miss workspace versions!
```

**AFTER (workspace-aware):**

```php
<?php

use TYPO3\CMS\Backend\Utility\BackendUtility;
use TYPO3\CMS\Core\Database\Connection;

$queryBuilder = $this->connectionPool->getQueryBuilderForTable('tt_content');
$result = $queryBuilder
    ->select('*')
    ->from('tt_content')
    ->where(
        $queryBuilder->expr()->eq('pid', $queryBuilder->createNamedParameter($pageId, Connection::PARAM_INT))
    )
    ->executeQuery();

$rows = [];
while ($row = $result->fetchAssociative()) {
    // Apply workspace overlay
    BackendUtility::workspaceOL('tt_content', $row);
    if (is_array($row)) {
        $rows[] = $row;
    }
}
```

### Pattern B: Frontend with WorkspaceRestriction

**BEFORE (no workspace restriction):**

```php
<?php
// WRONG for frontend: Missing WorkspaceRestriction
$queryBuilder = $this->connectionPool->getQueryBuilderForTable('tx_news_domain_model_news');
$queryBuilder->getRestrictions()->removeAll()->add(
    GeneralUtility::makeInstance(DeletedRestriction::class)
);
```

**AFTER (proper frontend restrictions):**

```php
<?php

use TYPO3\CMS\Core\Database\Query\Restriction\FrontendRestrictionContainer;

// FrontendRestrictionContainer includes:
// - DeletedRestriction
// - HiddenRestriction
// - StartTimeRestriction
// - EndTimeRestriction
// - WorkspaceRestriction  <-- automatically included!
// - FrontendGroupRestriction
$queryBuilder = $this->connectionPool->getQueryBuilderForTable('tx_news_domain_model_news');
$queryBuilder->setRestrictions(
    GeneralUtility::makeInstance(FrontendRestrictionContainer::class)
);
```

### Pattern C: Adding WorkspaceRestriction Manually

```php
<?php

use TYPO3\CMS\Core\Database\Query\Restriction\DeletedRestriction;
use TYPO3\CMS\Core\Database\Query\Restriction\WorkspaceRestriction;
use TYPO3\CMS\Core\Context\Context;
use TYPO3\CMS\Core\Utility\GeneralUtility;

$workspaceId = GeneralUtility::makeInstance(Context::class)
    ->getPropertyFromAspect('workspace', 'id', 0);

$queryBuilder = $this->connectionPool->getQueryBuilderForTable('tx_myext_item');
$queryBuilder->getRestrictions()
    ->removeAll()
    ->add(GeneralUtility::makeInstance(DeletedRestriction::class))
    ->add(GeneralUtility::makeInstance(WorkspaceRestriction::class, $workspaceId));
```

> **Important:** `WorkspaceRestriction` only filters the SQL result to exclude wrong workspace records. You **still must call** `versionOL()` or `workspaceOL()` on each row to get the actual workspace content overlaid.

### Pattern D: Extbase Repository (Mostly Transparent)

Extbase repositories handle workspace overlays **automatically** via the persistence layer. No changes needed for standard `findBy*` methods.

**However**, if you use custom QueryBuilder inside a repository:

```php
<?php

declare(strict_types=1);

namespace MyVendor\MyExtension\Domain\Repository;

use TYPO3\CMS\Core\Database\ConnectionPool;
use TYPO3\CMS\Core\Domain\Repository\PageRepository;
use TYPO3\CMS\Extbase\Persistence\Repository;

final class ItemRepository extends Repository
{
    public function __construct(
        private readonly ConnectionPool $connectionPool,
        private readonly PageRepository $pageRepository,
    ) {
        // parent constructor is called automatically via DI
    }

    /**
     * Custom query that needs manual workspace handling.
     */
    public function findItemsWithCustomQuery(int $categoryId): array
    {
        $queryBuilder = $this->connectionPool
            ->getQueryBuilderForTable('tx_myextension_domain_model_item');

        // Use FrontendRestrictionContainer for proper workspace filtering
        $queryBuilder->setRestrictions(
            \TYPO3\CMS\Core\Utility\GeneralUtility::makeInstance(
                \TYPO3\CMS\Core\Database\Query\Restriction\FrontendRestrictionContainer::class
            )
        );

        $result = $queryBuilder
            ->select('i.*')
            ->from('tx_myextension_domain_model_item', 'i')
            ->join(
                'i',
                'sys_category_record_mm',
                'mm',
                $queryBuilder->expr()->eq('mm.uid_foreign', $queryBuilder->quoteIdentifier('i.uid'))
            )
            ->where(
                $queryBuilder->expr()->eq(
                    'mm.uid_local',
                    $queryBuilder->createNamedParameter($categoryId, \TYPO3\CMS\Core\Database\Connection::PARAM_INT)
                )
            )
            ->executeQuery();

        $items = [];
        while ($row = $result->fetchAssociative()) {
            $this->pageRepository->versionOL('tx_myextension_domain_model_item', $row);
            if (is_array($row)) {
                $items[] = $row;
            }
        }

        return $items;
    }
}
```

### Pattern E: Migrating Legacy Queries (TYPO3 v10/v11 style to v13/v14)

**BEFORE (deprecated -- old exec_SELECTquery pattern, no longer available):**

```php
<?php
// DEPRECATED: Do NOT use. Not available in v13/v14.
// $res = $GLOBALS['TYPO3_DB']->exec_SELECTquery('*', 'tt_content', 'pid=' . (int)$pageId);
```

**AFTER (modern QueryBuilder with workspace support):**

```php
<?php

use TYPO3\CMS\Backend\Utility\BackendUtility;
use TYPO3\CMS\Core\Database\Connection;
use TYPO3\CMS\Core\Database\ConnectionPool;
use TYPO3\CMS\Core\Utility\GeneralUtility;

$queryBuilder = GeneralUtility::makeInstance(ConnectionPool::class)
    ->getQueryBuilderForTable('tt_content');

$result = $queryBuilder
    ->select('*')
    ->from('tt_content')
    ->where(
        $queryBuilder->expr()->eq(
            'pid',
            $queryBuilder->createNamedParameter($pageId, Connection::PARAM_INT)
        )
    )
    ->executeQuery();

while ($row = $result->fetchAssociative()) {
    BackendUtility::workspaceOL('tt_content', $row);
    if (is_array($row)) {
        // Process the workspace-overlaid record
    }
}
```

## 7. Translations with Workspaces

### How the Dual Overlay Works

When rendering a page in a workspace with a non-default language:

```
Live Record (lang=0, ws=0)
  └─► Workspace Overlay (lang=0, ws=1)     ← workspace version of default language
  └─► Language Overlay (lang=1, ws=0)       ← translation of live record
        └─► Workspace Overlay (lang=1, ws=1) ← workspace version of translation
```

TYPO3 handles this automatically when using `PageRepository->versionOL()` and `PageRepository->getLanguageOverlay()`.

### Creating Translations in Workspace Context

When working in a workspace:

1. The **default language record** is versioned first (if modified)
2. Translations created in a workspace get their own placeholder + version records
3. The `l10n_parent` field points to the **live** default language record UID
4. Each translation version has its own `t3ver_oid` pointing to the live translation

Database example for a tt_content record translated to French in workspace 1:

| uid | pid | t3ver_wsid | t3ver_oid | t3ver_state | l10n_parent | sys_language_uid | header |
|-----|-----|------------|-----------|-------------|-------------|------------------|--------|
| 11 | 20 | 0 | 0 | 0 | 0 | 0 | Article #1 |
| 31 | 20 | 1 | 0 | 1 | 11 | 1 | Placeholder (fr) |
| 32 | -1 | 1 | 31 | -1 | 11 | 1 | Article #1 (fr) |

### Language Restrictions per Workspace

Restrict which languages a user can edit in a specific workspace:

```
# User TSconfig
# Allow only French (uid=1) and German (uid=2) in workspace 3
options.workspaces.allowed_languages.3 = 1,2
```

### File Translations with Workspaces

The same file limitation applies to translations:

- **Translated file references** (`sys_file_reference` with `sys_language_uid > 0`) ARE versioned
- **Physical files** are NOT versioned
- If a translation needs a different PDF/image, upload it as a **new file** with a unique name
- Do NOT overwrite files shared between language versions

## 8. Debugging & Troubleshooting

### Quick Diagnostic Checklist

When workspaces "don't work", check these in order:

| # | Check | How |
|---|-------|-----|
| 1 | Extension installed? | `composer show typo3/cms-workspaces` |
| 2 | Workspace record exists? | List module on root page, filter System Records |
| 3 | User has workspace access? | Backend user/group > Mounts and Workspaces tab |
| 4 | User has LIVE access? | Same tab, "Live" checkbox must be checked |
| 5 | Table is versioningWS? | Check `$GLOBALS['TCA'][<table>]['ctrl']['versioningWS']` |
| 6 | DB columns exist? | `DESCRIBE <table>` -- look for `t3ver_oid`, `t3ver_wsid`, `t3ver_state` |
| 7 | DB mounts correct? | User/group must have DB mounts covering the pages being edited |
| 8 | File mounts correct? | User/group must have file mounts for media access |
| 9 | Schema up to date? | `bin/typo3 database:updateschema` |
| 10 | Cache cleared? | `bin/typo3 cache:flush` |

### SQL Queries for Debugging (DDEV Local Only)

```sql
-- Check if workspace records exist
SELECT uid, title, adminusers, members, publish_access
FROM sys_workspace
WHERE deleted = 0;

-- Check versioned records for a specific page
SELECT uid, pid, t3ver_oid, t3ver_wsid, t3ver_state, t3ver_stage, header
FROM tt_content
WHERE t3ver_wsid > 0
  AND deleted = 0
ORDER BY t3ver_wsid, t3ver_oid;

-- Find orphaned workspace records (pointing to deleted live records)
SELECT ws.uid AS ws_uid, ws.t3ver_oid, ws.t3ver_wsid, ws.header
FROM tt_content ws
LEFT JOIN tt_content live ON ws.t3ver_oid = live.uid
WHERE ws.t3ver_wsid > 0
  AND ws.deleted = 0
  AND (live.uid IS NULL OR live.deleted = 1);

-- Check workspace-enabled tables
SELECT TABLE_NAME
FROM information_schema.COLUMNS
WHERE COLUMN_NAME = 't3ver_oid'
  AND TABLE_SCHEMA = DATABASE()
ORDER BY TABLE_NAME;

-- Inspect backend user's workspace permissions
SELECT
    bu.uid,
    bu.username,
    bu.workspace_perms,
    GROUP_CONCAT(bg.title SEPARATOR ', ') AS groups,
    GROUP_CONCAT(bg.workspace_perms SEPARATOR ', ') AS group_ws_perms
FROM be_users bu
LEFT JOIN be_users_be_groups_mm mm ON bu.uid = mm.uid_local
LEFT JOIN be_groups bg ON mm.uid_foreign = bg.uid
WHERE bu.deleted = 0
  AND bu.disable = 0
GROUP BY bu.uid, bu.username, bu.workspace_perms;

-- Check sys_log for workspace operations
SELECT
    FROM_UNIXTIME(tstamp) AS time,
    userid,
    action,
    details,
    tablename,
    recuid,
    workspace
FROM sys_log
WHERE workspace > 0
ORDER BY tstamp DESC
LIMIT 50;
```

### Programmatic Permission Check

```php
<?php

declare(strict_types=1);

use TYPO3\CMS\Core\Context\Context;
use TYPO3\CMS\Core\Utility\GeneralUtility;

// Get current workspace ID
$workspaceId = GeneralUtility::makeInstance(Context::class)
    ->getPropertyFromAspect('workspace', 'id', 0);

// Check if user can edit in current workspace
$cannotEdit = $GLOBALS['BE_USER']->workspaceCannotEditRecord('tt_content', $row);
if ($cannotEdit) {
    // $cannotEdit contains error message explaining why
    throw new \RuntimeException('Cannot edit: ' . $cannotEdit);
}

// Check if new records can be created on a page
$canCreate = $GLOBALS['BE_USER']->workspaceCreateNewRecord($pageId, 'tt_content');

// Check user's workspace access level
$workspaceAccess = $GLOBALS['BE_USER']->checkWorkspace($workspaceId);
// Returns: array with 'uid', '_ACCESS' key ('admin', 'owner', 'member', or false)
```

### Common Issues & Solutions

| Issue | Cause | Solution |
|-------|-------|----------|
| Records not visible in workspace | `versioningWS = false` on table | Set `versioningWS = true`, run `database:updateschema` |
| Workspace changes visible on live site | Missing `WorkspaceRestriction` in custom query | Add `FrontendRestrictionContainer` or manual `WorkspaceRestriction` |
| "Editing not possible" error | User lacks edit permission or stage access | Check user/group `tables_modify`, DB mounts, workspace membership |
| Preview shows wrong content | Missing `versionOL()` call in extension | Add `BackendUtility::workspaceOL()` or `PageRepository->versionOL()` after query |
| Publish does nothing | Content not in "Ready to publish" stage | Advance content through stages, or disable stage restriction |
| File changed in all workspaces | Files are not versioned (by design) | Upload new files with unique names instead of overwriting |
| Translation missing in workspace | Language not allowed in workspace | Set `options.workspaces.allowed_languages.<wsId>` TSconfig |
| Auto-publish not working | Scheduler task not configured or not running | Create "Workspaces auto-publication" task, verify cron job |
| Workspace selector not visible | User has no workspace access | Assign user/group as workspace member or owner |

## 9. Testing Workspace Support

### Prerequisites: Install Testing Framework

**Step 1: Require dev dependencies**

```bash
# DDEV
ddev composer require --dev typo3/testing-framework:"^9.0" phpunit/phpunit:"^11.0"

# Non-DDEV
composer require --dev typo3/testing-framework:"^9.0" phpunit/phpunit:"^11.0"
```

> Adjust `typo3/testing-framework` version to match your TYPO3 version:
> - TYPO3 v13: `typo3/testing-framework:"^8.2 || ^9.0"`
> - TYPO3 v14: `typo3/testing-framework:"^9.0"`

**Step 2: Create PHPUnit configuration for functional tests**

Create `Build/phpunit-functional.xml` in your extension root:

```xml
<?xml version="1.0" encoding="UTF-8"?>
<phpunit xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
         xsi:noNamespaceSchemaLocation="vendor/phpunit/phpunit/phpunit.xsd"
         bootstrap="vendor/typo3/testing-framework/Resources/Core/Build/FunctionalTestsBootstrap.php"
         colors="true"
         cacheResult="false">
    <testsuites>
        <testsuite name="Functional">
            <directory>Tests/Functional</directory>
        </testsuite>
    </testsuites>
    <php>
        <!-- Functional tests need a database. DDEV provides one automatically. -->
        <!-- For non-DDEV: set typo3DatabaseHost, typo3DatabaseUsername, etc. -->
        <!-- Example for DDEV (auto-detected, usually no env vars needed): -->
        <!-- <env name="typo3DatabaseHost" value="db"/> -->
        <!-- <env name="typo3DatabaseUsername" value="db"/> -->
        <!-- <env name="typo3DatabasePassword" value="db"/> -->
        <!-- <env name="typo3DatabaseName" value="db"/> -->
    </php>
</phpunit>
```

**Step 3: Create directory structure**

```bash
mkdir -p Tests/Functional/Fixtures
```

```
your-extension/
├── Build/
│   └── phpunit-functional.xml       ← PHPUnit config
├── Classes/
│   └── ...
├── Configuration/
│   └── TCA/
├── Tests/
│   └── Functional/
│       ├── Fixtures/
│       │   └── WorkspaceTestData.csv ← Test data
│       └── WorkspaceAwareTest.php    ← Test class
├── composer.json
└── ext_emconf.php
```

**Step 4: Ensure composer.json has autoload-dev**

```json
{
    "autoload-dev": {
        "psr-4": {
            "MyVendor\\MyExtension\\Tests\\": "Tests/"
        }
    }
}
```

Then run:

```bash
# DDEV
ddev composer dump-autoload

# Non-DDEV
composer dump-autoload
```

### Functional Test Setup

```php
<?php

declare(strict_types=1);

namespace MyVendor\MyExtension\Tests\Functional;

use TYPO3\CMS\Core\Authentication\BackendUserAuthentication;
use TYPO3\CMS\Core\Context\Context;
use TYPO3\CMS\Core\Context\WorkspaceAspect;
use TYPO3\CMS\Core\Core\Bootstrap;
use TYPO3\CMS\Core\Database\ConnectionPool;
use TYPO3\CMS\Core\DataHandling\DataHandler;
use TYPO3\CMS\Core\Utility\GeneralUtility;
use TYPO3\TestingFramework\Core\Functional\FunctionalTestCase;

final class WorkspaceAwareTest extends FunctionalTestCase
{
    /**
     * Load the workspaces extension for all tests in this class.
     */
    protected array $coreExtensionsToLoad = [
        'workspaces',
    ];

    /**
     * Load your own extension.
     */
    protected array $testExtensionsToLoad = [
        'typo3conf/ext/my_extension',
    ];

    protected function setUp(): void
    {
        parent::setUp();

        // Import base data: pages, content, workspace record, backend user
        $this->importCSVDataSet(__DIR__ . '/Fixtures/WorkspaceTestData.csv');

        // Initialize backend user (uid=1 from fixture, must be admin for DataHandler)
        $this->setUpBackendUser(1);
        Bootstrap::initializeLanguageObject();
    }

    /**
     * Helper: set the current workspace context.
     */
    private function setWorkspaceId(int $workspaceId): void
    {
        $context = GeneralUtility::makeInstance(Context::class);
        $context->setAspect('workspace', new WorkspaceAspect($workspaceId));
        $GLOBALS['BE_USER']->setWorkspace($workspaceId);
    }

    /**
     * Test: Record created in workspace is NOT visible in live.
     */
    public function testRecordCreatedInWorkspaceNotVisibleInLive(): void
    {
        // Switch to workspace 1
        $this->setWorkspaceId(1);

        // Create a record in the workspace via DataHandler
        $data = [
            'tt_content' => [
                'NEW_1' => [
                    'pid' => 1,
                    'CType' => 'text',
                    'header' => 'Workspace Only Content',
                    'bodytext' => '<p>This should not be live</p>',
                ],
            ],
        ];

        $dataHandler = GeneralUtility::makeInstance(DataHandler::class);
        $dataHandler->start($data, []);
        $dataHandler->process_datamap();

        self::assertEmpty($dataHandler->errorLog, 'DataHandler errors: ' . implode(', ', $dataHandler->errorLog));

        // Switch back to LIVE
        $this->setWorkspaceId(0);

        // Query live records -- the workspace record should NOT appear
        $queryBuilder = GeneralUtility::makeInstance(ConnectionPool::class)
            ->getQueryBuilderForTable('tt_content');

        $liveRecords = $queryBuilder
            ->select('uid', 'header')
            ->from('tt_content')
            ->where(
                $queryBuilder->expr()->eq('pid', 1),
                $queryBuilder->expr()->eq('t3ver_wsid', 0),
                $queryBuilder->expr()->neq('t3ver_state', 1) // exclude new placeholders
            )
            ->executeQuery()
            ->fetchAllAssociative();

        $headers = array_column($liveRecords, 'header');
        self::assertNotContains('Workspace Only Content', $headers);
    }

    /**
     * Test: Workspace overlay returns modified content.
     */
    public function testWorkspaceOverlayReturnsModifiedContent(): void
    {
        // Record uid=10 exists in fixture with header "Original Header"
        // Workspace version exists with header "Modified In Workspace"
        $this->setWorkspaceId(1);

        $row = \TYPO3\CMS\Backend\Utility\BackendUtility::getRecordWSOL('tt_content', 10);

        self::assertIsArray($row);
        self::assertSame('Modified In Workspace', $row['header']);
    }

    /**
     * Test: Workspace publish command makes staged content live for a record pair.
     *
     * DEPRECATED: The 'swap' action is no longer allowed in TYPO3 v14.
     * Use 'action' => 'publish' instead. The 'swapWith' key is replaced by 'uid' (workspace version uid).
     */
    public function testPublishWorkspaceRecordPairMakesContentLive(): void
    {
        $this->setWorkspaceId(1);

        // Publish workspace record for tt_content uid=10
        $cmd = [
            'tt_content' => [
                10 => [
                    'version' => [
                        'action' => 'publish',
                        'uid' => $this->getWorkspaceVersionUid('tt_content', 10, 1),
                    ],
                ],
            ],
        ];

        $dataHandler = GeneralUtility::makeInstance(DataHandler::class);
        $dataHandler->start([], $cmd);
        $dataHandler->process_cmdmap();

        self::assertEmpty($dataHandler->errorLog);

        // Switch to LIVE and verify
        $this->setWorkspaceId(0);
        $row = \TYPO3\CMS\Backend\Utility\BackendUtility::getRecord('tt_content', 10);

        self::assertSame('Modified In Workspace', $row['header']);
    }

    /**
     * Helper: Get the uid of the workspace version of a record.
     */
    private function getWorkspaceVersionUid(string $table, int $liveUid, int $workspaceId): int
    {
        $queryBuilder = GeneralUtility::makeInstance(ConnectionPool::class)
            ->getQueryBuilderForTable($table);
        $queryBuilder->getRestrictions()->removeAll();

        $row = $queryBuilder
            ->select('uid')
            ->from($table)
            ->where(
                $queryBuilder->expr()->eq('t3ver_oid', $liveUid),
                $queryBuilder->expr()->eq('t3ver_wsid', $workspaceId),
                $queryBuilder->expr()->eq('deleted', 0)
            )
            ->executeQuery()
            ->fetchAssociative();

        return (int)($row['uid'] ?? 0);
    }
}
```

### CSV Fixture File

Create `Tests/Functional/Fixtures/WorkspaceTestData.csv`:

```csv
"be_users"
,"uid","pid","username","password","admin","workspace_perms"
,1,0,"admin","$2y$12$placeholder",1,1

"sys_workspace"
,"uid","pid","title","adminusers","members","deleted"
,1,0,"Test Workspace","1","1",0

"pages"
,"uid","pid","title","slug","deleted","t3ver_oid","t3ver_wsid","t3ver_state"
,1,0,"Test Page","/test-page",0,0,0,0

"tt_content"
,"uid","pid","header","CType","bodytext","deleted","t3ver_oid","t3ver_wsid","t3ver_state"
,10,1,"Original Header","text","<p>Original</p>",0,0,0,0
,11,-1,"Modified In Workspace","text","<p>Modified</p>",0,10,1,0
```

### Run Tests

**DDEV (recommended):**

```bash
# Run all workspace functional tests
ddev exec bin/phpunit -c Build/phpunit-functional.xml \
  Tests/Functional/WorkspaceAwareTest.php

# Run a single test method
ddev exec bin/phpunit -c Build/phpunit-functional.xml \
  --filter testWorkspaceOverlayReturnsModifiedContent \
  Tests/Functional/WorkspaceAwareTest.php

# Verbose output (shows each test name)
ddev exec bin/phpunit -c Build/phpunit-functional.xml \
  -v Tests/Functional/WorkspaceAwareTest.php
```

DDEV auto-provides the test database. No extra env vars needed.

**Non-DDEV (manual database config):**

```bash
# Set database credentials for the test runner
export typo3DatabaseHost="127.0.0.1"
export typo3DatabasePort="3306"
export typo3DatabaseUsername="root"
export typo3DatabasePassword="root"
export typo3DatabaseName="typo3_test"

bin/phpunit -c Build/phpunit-functional.xml \
  Tests/Functional/WorkspaceAwareTest.php
```

> The testing framework creates a **temporary database** per test case. Your env vars point to the DB server -- the framework handles the rest.

**Troubleshooting test failures:**

| Error | Cause | Fix |
|-------|-------|-----|
| `Table 'sys_workspace' doesn't exist` | `workspaces` not in `$coreExtensionsToLoad` | Add `'workspaces'` to array |
| `Table 'be_users' has no column 'workspace_perms'` | Schema not created for test DB | Ensure `workspaces` is loaded before `setUp()` |
| `Access denied for user` | Wrong DB credentials | Check env vars or DDEV status (`ddev describe`) |
| `Call to undefined method setUpBackendUser` | Wrong testing-framework version | Use `typo3/testing-framework ^8.2` (v13) or `^9.0` (v14) |
| `Record not found after DataHandler` | CSV fixture malformed | Verify CSV: first row is table name, second row is column headers, data rows start with comma |

## 10. Best Practices

### Pages with Content Elements (Standard Workflow)

1. Editor switches to the custom workspace via the top bar selector
2. Editor navigates to the page and edits content elements
3. TYPO3 automatically creates workspace versions of modified records
4. Editor previews via "View webpage" button (shows workspace version)
5. Editor sends changes to "Ready to publish" stage
6. Reviewer approves or sends back with comments
7. Publisher publishes to live (or auto-publish via Scheduler)

**Key points:**
- `pages` and `tt_content` have `versioningWS = true` by default
- FAL relations (images, media) are versioned via `sys_file_reference` overlays (physical files are not versioned); MM relations (categories) are handled through parent record overlays/DataHandler relation handling; simple fields (links, text) are versioned directly in the record overlay
- Page tree shows modified pages with a highlighting indicator
- The Workspaces module gives a full overview of all changes

### News with Content Elements (EXT:news)

`tx_news_domain_model_news` has `versioningWS = true` by default. Workspace workflows work for news records.

**Watch out for:**

- News categories (`sys_category`): versioned by default, works
- News tags (`tx_news_domain_model_tag`): check if `versioningWS` is enabled
- News detail page preview: configure preview page in TSconfig:

```
# Page TSconfig for news preview in workspace
options.workspaces.previewPageId.tx_news_domain_model_news = 42
```

- Related news: MM relations are handled by DataHandler
- News images: FAL references are versioned, but **physical files are not** (see Section 2)

### Campaign/Seasonal Content with Scheduled Publish

For temporary content (Christmas, Black Friday, product launches):

1. Prepare all campaign content in the workspace
2. Send changes to review and approval stage
3. Publish (or schedule auto-publish) at campaign start
4. Create a follow-up workspace change set to restore baseline content after campaign end
5. Publish the rollback change set when the campaign is over

### Preview Links for External Reviewers

```
# User TSconfig -- set preview link expiry
options.workspaces.previewLinkTTLHours = 72
```

Generate via Workspaces module: "Generate page preview links" button. The link works without any TYPO3 backend access.

### Scheduler Auto-Publish

1. Set a "Publish" date on the workspace record (Publishing tab)
2. Create Scheduler task: "Workspaces auto-publication"
3. Set task frequency (e.g., every 15 minutes)
4. Only content in "Ready to publish" stage gets published

```bash
# Cron job (runs every 15 minutes)
*/15 * * * * /path/to/bin/typo3 scheduler:run
```

### General Rules

- **Use groups, not individual users** for workspace ownership and membership
- **Test workspace workflows** before going live with workspace-based editing
- **Document the review process** for editors (which stages, who approves)
- **Monitor disk space** -- workspace versions accumulate in the database
- **Clean up** old workspace data periodically (discard unused versions)
- **Keep patch level current** -- workspace security issues exist (see TYPO3-CORE-SA-2025-022)

## 11. PSR-14 Events Reference

### AfterRecordPublishedEvent

Fired after a record has been published from a workspace to live.

```php
<?php

declare(strict_types=1);

namespace MyVendor\MyExtension\EventListener;

use TYPO3\CMS\Core\Attribute\AsEventListener;
use TYPO3\CMS\Workspaces\Event\AfterRecordPublishedEvent;

#[AsEventListener]
final class AfterPublishListener
{
    public function __invoke(AfterRecordPublishedEvent $event): void
    {
        $table = $event->getTable();
        $liveId = $event->getRecordId();

        // Example: Clear external CDN cache after publishing
        if ($table === 'pages') {
            // Trigger CDN purge for the published page
        }

        // Example: Notify external system
        if ($table === 'tx_news_domain_model_news') {
            // Send webhook to newsletter system
        }
    }
}
```

### SortVersionedDataEvent

Fired after sorting data in the Workspaces backend module. Use to apply custom sorting.

```php
<?php

declare(strict_types=1);

namespace MyVendor\MyExtension\EventListener;

use TYPO3\CMS\Core\Attribute\AsEventListener;
use TYPO3\CMS\Workspaces\Event\SortVersionedDataEvent;

#[AsEventListener]
final class CustomWorkspaceSortListener
{
    public function __invoke(SortVersionedDataEvent $event): void
    {
        // Custom sorting logic for workspace module
        $data = $event->getData();
        // ... modify $data ...
        $event->setData($data);
    }
}
```

### All Available Events

| Event | When Fired |
|-------|------------|
| `AfterCompiledCacheableDataForWorkspaceEvent` | After compiling cacheable workspace version data |
| `AfterDataGeneratedForWorkspaceEvent` | After generating all workspace version data |
| `AfterRecordPublishedEvent` | After a record is published to live |
| `GetVersionedDataEvent` | After preparing/cleaning workspace version data |
| `ModifyVersionDifferencesEvent` | When computing diffs between live and workspace version |
| `SortVersionedDataEvent` | After sorting workspace version data in the module |

All events are in the `\TYPO3\CMS\Workspaces\Event\` namespace.

---

## Related Skills

- [typo3-datahandler](../typo3-datahandler/SKILL.md) -- DataHandler operations (used for all record manipulation in workspaces)
- [typo3-testing](../typo3-testing/SKILL.md) -- Testing infrastructure (functional tests for workspace support)
- [typo3-security](../typo3-security/SKILL.md) -- Security hardening (file access, permissions)
- [typo3-seo](../typo3-seo/SKILL.md) -- SEO configuration (preview links, robots handling)

---

## Credits & Attribution

This skill is based on the official TYPO3 CMS documentation and community resources.
Special thanks to the TYPO3 Core Team and **[b13 GmbH](https://b13.com/)** (Benni Mack) for
their excellent explanation of the overlay mechanism.

Thanks to Netresearch DTT GmbH for their contributions to the TYPO3 community.
