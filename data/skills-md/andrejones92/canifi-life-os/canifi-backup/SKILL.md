---
name: canifi-backup
description: Automated backup system for your entire Canifi LifeOS configuration, skills, and Claude settings
category: productivity
version: 1.0.0
author: Canifi LifeOS
required: true
---

# Canifi Backup

## Overview

The Canifi Backup skill creates comprehensive backups of your entire LifeOS system with a single command. It packages your configuration, skills, and Claude settings into a timestamped ZIP file stored at your preferred destination.

**Why This Skill is Required:**
- Protects your custom skills and configurations from loss
- Enables easy migration to new machines
- Provides restore points before major changes
- Ensures your LifeOS investment is never lost

---

## Privacy & Authentication

**Your credentials, your choice.** Canifi LifeOS respects your privacy.

### Option 1: Manual Browser Login (Recommended)
If you prefer not to share credentials with Claude Code:
1. Complete the [Browser Automation Setup](/setup/automation) using CDP mode
2. Login to the service manually in the Playwright-controlled Chrome window
3. Claude will use your authenticated session without ever seeing your password

### Option 2: Environment Variables
If you're comfortable sharing credentials, you can store them locally:
```bash
canifi-env set SERVICE_EMAIL "your-email"
canifi-env set SERVICE_PASSWORD "your-password"
```

**Note**: Credentials stored in canifi-env are only accessible locally on your machine and are never transmitted.

## What Gets Backed Up

The backup includes three critical directories:

### 1. Claude Configuration (`~/.claude/`)
- `CLAUDE.md` - Your global Claude instructions
- `settings.json` - Claude Code settings
- `projects/` - Project-specific configurations
- All custom configurations

### 2. Global Skills (`~/.claude/skills/`)
- All installed skills (including auto-generated ones)
- Custom skill modifications
- Skill configurations

### 3. Canifi Scripts (`~/canifi/`)
- iMessage integration scripts
- Helper scripts
- Custom automation scripts

---

## First-Time Setup

On your first backup request, Canifi will ask for your backup destination:

```
User: "canifi backup"

Canifi: "This is your first backup. Where would you like to store backups?

Please provide a full path, for example:
- ~/Backups/canifi
- ~/Documents/CanifiBackups
- /Volumes/ExternalDrive/Backups

I'll remember this location for future backups."

User: "~/Backups/canifi"

Canifi: "Got it! I'll store backups at ~/Backups/canifi

Saving this to your global CLAUDE.md...
Creating your first backup now..."
```

The destination is stored in your global `~/.claude/CLAUDE.md` file:

```markdown
## Canifi Backup Configuration

CANIFI_BACKUP_DESTINATION="~/Backups/canifi"
```

---

## Usage

### Create a Backup
```
canifi backup
```

Creates a timestamped backup at your configured destination:
```
~/Backups/canifi/canifi-backup-2026-01-09-143022.zip
```

### Backup with Custom Name
```
canifi backup before-major-update
```

Creates:
```
~/Backups/canifi/canifi-backup-before-major-update-2026-01-09.zip
```

### Change Backup Destination
```
canifi backup set destination ~/NewLocation/backups
```

Updates the destination in your global CLAUDE.md.

### List Recent Backups
```
canifi backup list
```

Shows recent backups with sizes and dates.

### Restore from Backup
```
canifi backup restore ~/Backups/canifi/canifi-backup-2026-01-09-143022.zip
```

Restores files from a backup (with confirmation prompts).

---

## Backup Workflow

### Step 1: Check for Destination

First, check if `CANIFI_BACKUP_DESTINATION` exists in `~/.claude/CLAUDE.md`:

```bash
grep "CANIFI_BACKUP_DESTINATION" ~/.claude/CLAUDE.md
```

If not found, prompt user for destination.

### Step 2: Store Destination (First Time Only)

Append to `~/.claude/CLAUDE.md`:

```bash
cat >> ~/.claude/CLAUDE.md << 'EOF'

## Canifi Backup Configuration

CANIFI_BACKUP_DESTINATION="[USER_PROVIDED_PATH]"
EOF
```

### Step 3: Create Backup Directory

```bash
mkdir -p "$CANIFI_BACKUP_DESTINATION"
```

### Step 4: Generate Timestamp

```bash
TIMESTAMP=$(date +"%Y-%m-%d-%H%M%S")
BACKUP_NAME="canifi-backup-${TIMESTAMP}.zip"
```

### Step 5: Create ZIP Archive

```bash
cd ~
zip -r "$CANIFI_BACKUP_DESTINATION/$BACKUP_NAME" \
  .claude/ \
  canifi/ \
  -x "*.DS_Store" \
  -x "*node_modules/*" \
  -x "*.git/*"
```

### Step 6: Verify and Report

```bash
# Check file was created
ls -lh "$CANIFI_BACKUP_DESTINATION/$BACKUP_NAME"

# Report to user
echo "Backup complete: $BACKUP_NAME"
echo "Location: $CANIFI_BACKUP_DESTINATION"
echo "Size: $(du -h "$CANIFI_BACKUP_DESTINATION/$BACKUP_NAME" | cut -f1)"
```

---

## Restore Workflow

### Step 1: Confirm with User

```
WARNING: Restoring will overwrite existing files:
- ~/.claude/
- ~/canifi/

Current files will be backed up to ~/.canifi-restore-backup/ first.

Proceed? (yes/no)
```

### Step 2: Backup Current State

```bash
mkdir -p ~/.canifi-restore-backup
cp -r ~/.claude ~/.canifi-restore-backup/
cp -r ~/canifi ~/.canifi-restore-backup/
```

### Step 3: Extract Archive

```bash
cd ~
unzip -o "$BACKUP_FILE"
```

### Step 4: Verify Restore

```bash
echo "Restore complete!"
echo "Your previous configuration was backed up to ~/.canifi-restore-backup/"
```

---

## Backup Contents Structure

```
canifi-backup-2026-01-09-143022.zip
├── .claude/
│   ├── CLAUDE.md
│   ├── settings.json
│   ├── projects/
│   │   └── [project-specific configs]
│   └── skills/
│       ├── canifi/
│       ├── canifi-skill-generator/
│       ├── canifi-backup/
│       └── [all other skills]
└── canifi/
    ├── canifi-send.sh
    ├── canifi-help.sh
    ├── canifi-status.sh
    ├── canifi-stream.sh
    ├── canifi-pause.sh
    ├── canifi-resume.sh
    ├── canifi-abort.sh
    └── canifi-imessage-monitor.sh
```

---

## Configuration in CLAUDE.md

After first backup, your `~/.claude/CLAUDE.md` will include:

```markdown
## Canifi Backup Configuration

CANIFI_BACKUP_DESTINATION="~/Backups/canifi"

### Backup History
- Last backup: 2026-01-09 14:30:22
- Total backups: 5
- Oldest backup: 2026-01-01
```

---

## Automatic Backup Triggers

Consider setting up automatic backups:

### Before Major Operations
The skill generator can trigger a backup before creating new skills:
```
"Creating new skill 'todoist'...
 Running pre-change backup first..."
```

### Scheduled Backups
Add to your workflow:
```
canifi backup weekly
```

### Pre-Update Backups
Before updating Canifi LifeOS:
```
canifi backup pre-update
```

---

## Cloud Backup Destinations

You can set your backup destination to cloud-synced folders:

### iCloud Drive (macOS)
```
~/Library/Mobile Documents/com~apple~CloudDocs/Backups/canifi
```

### Dropbox
```
~/Dropbox/Backups/canifi
```

### Google Drive
```
~/Google Drive/Backups/canifi
```

### OneDrive
```
~/OneDrive/Backups/canifi
```

This way your backups are automatically synced to the cloud!

---

## Troubleshooting

### "Destination not found"
```bash
# Create the directory
mkdir -p ~/Backups/canifi

# Or change destination
canifi backup set destination ~/NewPath
```

### "Permission denied"
```bash
# Check permissions
ls -la ~/Backups/

# Fix if needed
chmod 755 ~/Backups/canifi
```

### "Backup too large"
The backup excludes node_modules and .git by default. If still large:
```bash
# Check what's taking space
du -sh ~/.claude/* ~/canifi/*
```

### "Cannot find CLAUDE.md"
```bash
# Create if missing
touch ~/.claude/CLAUDE.md
```

---

## Example Session

```
User: "canifi backup"

Canifi: "I notice this is your first backup request.
        Where would you like me to store your backups?

        Suggested locations:
        1. ~/Backups/canifi (local)
        2. ~/Dropbox/Backups/canifi (cloud-synced)
        3. Custom path

        Please provide your preferred backup destination."

User: "Use Dropbox"

Canifi: "Setting backup destination to: ~/Dropbox/Backups/canifi

        Updating ~/.claude/CLAUDE.md with backup configuration...
        Creating directory ~/Dropbox/Backups/canifi...

        Now creating your first backup...

        Backing up:
        ✓ ~/.claude/ (1.2 MB)
        ✓ ~/.claude/skills/ (4.8 MB)
        ✓ ~/canifi/ (52 KB)

        Backup complete!

        📦 canifi-backup-2026-01-09-143022.zip
        📍 ~/Dropbox/Backups/canifi/
        📊 Size: 6.1 MB

        Your LifeOS is now backed up and syncing to Dropbox."
```

---

## Security Notes

1. **Backups may contain sensitive data** - Your CLAUDE.md might have API keys or credentials
2. **Encrypt sensitive backups** - Consider using encrypted disk images for highly sensitive setups
3. **Cloud sync considerations** - Cloud-synced folders upload your backup; ensure you trust the provider
4. **Exclude from git** - Never commit backup ZIPs to version control
