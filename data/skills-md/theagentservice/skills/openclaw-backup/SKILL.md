---
name: openclaw-backup
description: |
  Encrypted backup and restore for OpenClaw Agent workspace files
  (SOUL.md, MEMORY.md, IDENTITY.md, AGENTS.md, TOOLS.md). Uses
  tar + openssl (AES-256-CBC) encryption and soul-upload.com API.
  Auto-generates a new random password for each backup (DO NOT reuse
  passwords). Use when the user needs to: (1) Back up or upload agent
  workspace files, (2) Restore or download a previous backup, (3) Delete
  a backup from remote storage, or (4) Manage encrypted agent persistence.
allowed-tools: ["Bash", "Read", "Write"]
---

# OpenClaw Backup Skill

Automated encrypted backup and restore for OpenClaw Agent workspace files using Claude Code.

## Overview

This skill provides three core functions:

1. **Upload Backup** - Encrypt and upload workspace files to soul-upload.com with auto-generated password
2. **Download Backup** - Download and decrypt backups from soul-upload.com using stored password
3. **Delete Backup** - Delete backups from remote storage

All backups use **AES-256-CBC encryption** (via openssl) with **auto-generated random passwords**. Each backup gets a unique password that is stored in the recovery file.

## System Requirements

Before executing backup operations, ensure the following tools are installed:

- **Python 3.7+** (script runtime environment)
- **requests library** (`pip install requests`)
- **tar** (file archiving)
- **openssl** (encryption/decryption)
- **curl** (HTTP requests, system built-in)

## Default Backup Files

If the user doesn't specify files, the following OpenClaw workspace files are backed up by default:

- `SOUL.md` - Agent core identity and goals
- `MEMORY.md` - Agent memory and context
- `IDENTITY.md` - Agent identity definition
- `AGENTS.md` - Agent configuration
- `TOOLS.md` - Tool configuration

## Workflow 1: Upload Backup

### Trigger Scenarios

Execute when the user requests to backup workspace files:

- "Back up my workspace files"
- "Upload SOUL.md to soul-upload"
- "Create an encrypted backup of my agent files"
- "Backup SOUL.md and MEMORY.md"

### Execution Steps

1. **Collect File List**
   - If user specified files, use the user-specified files
   - Otherwise, use default list: `SOUL.md MEMORY.md IDENTITY.md AGENTS.md TOOLS.md`
   - Use Read tool to verify files exist

2. **Execute Backup Script** (Password Auto-Generated)
   - Locate script path (usually `scripts/backup.py` in Skill directory)
   - Execute command WITHOUT --password argument (script will auto-generate):
     ```bash
     python3 scripts/backup.py upload \
       --files "SOUL.md MEMORY.md IDENTITY.md"
     ```
   - Script automatically generates a 32-character random password
   - Capture stdout (JSON response) and stderr (progress info including generated password)

3. **Process Response**
   - On success, script outputs JSON:
     ```json
     {
       "backupId": "xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx",
       "downloadUrl": "https://soul-upload.com/backup/...",
       "sizeBytes": 12345,
       "sha256": "abc123...",
       "password": "auto-generated-32-char-random-password"
     }
     ```
   - Parse JSON and extract key information including the auto-generated password

4. **Save Recovery Information**
   - Use Write tool to create/update `.openclaw-backup-recovery.txt`
   - **CRITICAL**: Include the auto-generated password in the recovery file
   - Format:
     ```
     Backup ID: xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx
     Password: auto-generated-32-char-random-password
     Download URL: https://soul-upload.com/backup/...
     Created: 2024-01-15 10:30:00 UTC
     Size: 12.05 KB
     SHA256: abc123...
     Files: SOUL.md, MEMORY.md, IDENTITY.md
     ---
     ```
   - Append to end of file (preserve history)

5. **Display Success Message**
   - Inform user backup is complete
   - Show Backup ID and file size
   - **IMPORTANT**: Inform user that password was auto-generated and saved to `.openclaw-backup-recovery.txt`
   - Warn user: Recovery file is CRITICAL - without it, backup cannot be restored

### Error Handling

| Error Scenario | Detection | User Guidance |
|----------------|-----------|---------------|
| Files not found | Script returns error: "Files not found: ..." | List missing files, ask if user wants to continue backing up other files |
| Files too large | Script returns error: "Backup size ... exceeds limit ..." | Show actual size, suggest removing large files or splitting backup |
| Network error | Script returns error: "Network error: ..." | Suggest checking network connection, ask if retry is wanted |
| 413 Too Large | Script returns error: "File too large (413 Payload Too Large)" | Indicate 20MB limit exceeded, suggest reducing backup size |
| Encryption failed | Script returns error: "openssl encryption failed: ..." | Check if openssl is properly installed |

### Example Conversation

```
User: Back up my SOUL.md and MEMORY.md
Claude: I'll backup these files with auto-generated encryption.
       [Executes backup script]
       Backup complete!
       - Backup ID: 3f8a2b1c-...
       - Size: 45.2 KB
       - Password: Auto-generated (32 chars)
       - Recovery info saved to .openclaw-backup-recovery.txt

       IMPORTANT: Keep .openclaw-backup-recovery.txt safe!
       It contains the password needed to restore this backup.
```

## Workflow 2: Download Backup

### Trigger Scenarios

Execute when user requests to restore backup:

- "Restore my backup"
- "Download my last backup"
- "Recover backup [backup-id]"
- "Restore from [download-url]"

### Execution Steps

1. **Get Backup ID and Password**
   - Check if user provided Backup ID or Download URL
   - If not provided, use Read tool to read `.openclaw-backup-recovery.txt`
   - Extract latest Backup ID AND password from file
   - If file doesn't exist or is empty, cannot proceed (password unknown)

2. **Determine Output Directory**
   - Default: Current working directory (`.`)
   - If user specified a directory, use user-specified directory
   - Warn user: Existing files may be overwritten

3. **Execute Restore Script**
   - Execute command with password from recovery file:
     ```bash
     python3 scripts/backup.py download \
       --backup-id "xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx" \
       --password "password-from-recovery-file" \
       --output-dir "."
     ```
   - Capture stdout (JSON response) and stderr (progress info)

4. **Process Response**
   - On success, script outputs JSON:
     ```json
     {
       "success": true,
       "extractedFiles": ["SOUL.md", "MEMORY.md", "IDENTITY.md"],
       "outputDir": "/path/to/output"
     }
     ```
   - Parse extracted file list

5. **Verify Restoration Result**
   - Use Read tool to read first few lines of restored files
   - Show file preview for user to confirm content is correct
   - Remind user to check complete content

6. **Display Success Message**
   - List restored files
   - Show output directory
   - Suggest user verify file content

### Error Handling

| Error Scenario | Detection | User Guidance |
|----------------|-----------|---------------|
| Backup ID doesn't exist | Script returns error: "Backup not found: ..." | Check if Backup ID is correct, may have been deleted |
| Recovery file missing | `.openclaw-backup-recovery.txt` not found | Cannot restore - password is unknown without recovery file |
| Wrong password | Script returns error: "Decryption failed - wrong password ..." | Recovery file may be corrupted or from different backup |
| Network error | Script returns error: "Network error: ..." | Suggest checking network connection, ask if retry is wanted |
| Extraction failed | Script returns error: "tar extraction failed: ..." | File may be corrupted, try downloading again |

### Example Conversation

```
User: Restore my last backup
Claude: I found the most recent backup in .openclaw-backup-recovery.txt
       - Backup ID: 3f8a2b1c-...
       - Created: 2024-01-15 10:30:00 UTC
       Downloading and decrypting backup...
       Restoration complete! Extracted the following files:
       - SOUL.md
       - MEMORY.md
       - IDENTITY.md
       Files saved to current directory, please verify content is correct.
```

## Workflow 3: Delete Backup

### Trigger Scenarios

Execute when user requests to delete remote backup:

- "Delete my backup"
- "Remove backup [backup-id]"
- "Delete the backup from soul-upload"

### Execution Steps

1. **Get Backup ID**
   - Check if user provided Backup ID
   - If not provided, use Read tool to read `.openclaw-backup-recovery.txt`
   - Show available backup list for user to select
   - If file doesn't exist or is empty, ask user to provide Backup ID

2. **Request Confirmation**
   - Warning: This operation is irreversible, backup will be permanently deleted
   - Show Backup ID to delete and creation time
   - Ask user to confirm deletion

3. **Execute Delete Script**
   - After user confirms, execute command:
     ```bash
     python3 scripts/backup.py delete \
       --backup-id "xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx"
     ```
   - Capture stdout (JSON response) and stderr (progress info)

4. **Process Response**
   - On success, script outputs JSON:
     ```json
     {
       "success": true,
       "backupId": "xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx"
     }
     ```

5. **Update Recovery Info File**
   - Use Read tool to read `.openclaw-backup-recovery.txt`
   - Remove deleted backup record (including its password)
   - Use Write tool to save updated file
   - If file becomes empty, can delete the file

6. **Display Success Message**
   - Confirm backup was deleted
   - Show deleted Backup ID
   - Remind user: If backup is needed again, must create new one with new password

### Error Handling

| Error Scenario | Detection | User Guidance |
|----------------|-----------|---------------|
| Backup ID doesn't exist | Script returns error: "Backup not found: ..." | Backup may have been deleted or ID is incorrect |
| Network error | Script returns error: "Network error: ..." | Suggest checking network connection, ask if retry is wanted |
| User cancels | User declines confirmation | Operation cancelled, backup not deleted |

### Example Conversation

```
User: Delete my backup
Claude: I found the following backups in .openclaw-backup-recovery.txt:
       1. Backup ID: 3f8a2b1c-... (2024-01-15 10:30:00)
       2. Backup ID: 7b2c9d4e-... (2024-01-14 08:20:00)
       Which backup would you like to delete? (1 or 2)
User: 1
Claude: Warning: This will permanently delete backup 3f8a2b1c-...
       This action cannot be undone. Confirm deletion? (yes/no)
User: yes
Claude: Backup deleted.
       - Backup ID: 3f8a2b1c-...
       To backup again, create a new backup with a new auto-generated password.
```

## Security Notes

### Password Policy (NEW)

- **Auto-Generated Passwords**: Each backup gets a unique 32-character random password
- **Never Reuse Passwords**: Per soul-upload.com policy, do NOT reuse passwords across backups
- **Password Storage**: Password is stored in `.openclaw-backup-recovery.txt` (necessary for decryption)
- **User Responsibility**: Users must keep recovery file safe - without it, backup cannot be restored

### Recovery File Security

- **File Location**: `.openclaw-backup-recovery.txt` (workspace root directory)
- **Content**: Backup ID, Password (CRITICAL), Download URL, timestamp, SHA256
- **CRITICAL**: Recovery file is the ONLY place password is stored
- **Recommendation**:
  - Add to `.gitignore` if sensitive
  - OR commit to version control for team access
  - Consider backing up recovery file itself to separate secure location

### Encryption Algorithm

- **Algorithm**: AES-256-CBC (symmetric encryption)
- **Salting**: openssl automatically adds salt for enhanced security
- **Compatibility**: Consistent with soul-upload.com official documentation

### Temporary File Cleanup

- Script uses try-finally to ensure temporary files are cleaned up
- Avoids leaving unencrypted sensitive data on disk

## File Size Limits

- **Maximum Backup Size**: 20 MB (compressed and encrypted)
- **Check Timing**: Automatically checked before upload
- **Limit Exceeded Handling**: Show actual size, suggest user:
  - Remove large files (like logs, caches)
  - Split backup (backup different files in batches)

## API Reference

soul-upload.com Backup API:

| Endpoint | Method | Function | Response |
|----------|--------|----------|----------|
| `/backup` | POST | Upload backup | `{backupId, downloadUrl, sizeBytes, sha256}` |
| `/backup/:backupId` | GET | Download backup | 302 redirect to R2 storage URL |
| `/backup/:backupId` | DELETE | Delete backup | `{success: true, backupId}` |

Common Status Codes:

- **200** - Success
- **404** - Backup not found
- **413** - File too large (exceeds 20MB)
- **415** - Unsupported file type
- **500** - Server error

## Troubleshooting

### Missing Dependencies

**Problem**: Script error "Missing required tools: tar, openssl"

**Solution**:
- macOS: `brew install openssl` (tar built-in)
- Ubuntu/Debian: `sudo apt-get install tar openssl`
- Verify installation: `tar --version` and `openssl version`

### Python requests Library Missing

**Problem**: Script error "Error: 'requests' library not found"

**Solution**:
```bash
pip install requests
# or
pip3 install requests
```

### Recovery File Lost

**Problem**: Cannot restore backup - recovery file missing

**Solution**:
- Recovery file is CRITICAL - contains the only copy of the password
- Without recovery file, backup CANNOT be restored
- Recommend backing up recovery file to separate secure location
- If lost, backup is permanently inaccessible

### Network Timeout

**Problem**: Timeout during upload/download

**Solution**:
- Check network connection
- Reduce backup file size (remove unnecessary files)
- Script default timeout is 5 minutes, usually sufficient

### File Already Exists

**Problem**: Overwriting existing files during restore

**Solution**:
- Backup existing files before restore
- Specify different output directory
- Manually move existing files to other location

## Usage Examples

### Example 1: Backup All Default Files

```
User: Back up my workspace files
Claude: [Execute upload workflow using default file list]
       [Auto-generate password and save to recovery file]
```

### Example 2: Backup Specific Files

```
User: Back up only SOUL.md and MEMORY.md
Claude: [Execute upload workflow, backup only specified files]
       [Auto-generate password and save to recovery file]
```

### Example 3: Restore Latest Backup

```
User: Restore my last backup
Claude: [Read latest Backup ID and password from .openclaw-backup-recovery.txt]
       [Execute download workflow]
```

### Example 4: Restore Specific Backup

```
User: Restore backup 3f8a2b1c-1234-5678-90ab-cdef12345678
Claude: [Read password for this Backup ID from recovery file]
       [Execute download workflow]
```

### Example 5: Delete Old Backups

```
User: Delete my old backups
Claude: [Show available backup list from recovery file]
       [User selects backup to delete]
       [Execute delete workflow]
       [Remove entry from recovery file]
```

## Best Practices

1. **Regular Backups**: Recommend weekly backups or after important changes
2. **Recovery File Management**: Keep `.openclaw-backup-recovery.txt` safe and backed up separately
3. **Verify Restoration**: Regularly test backup restoration process to ensure backups are usable
4. **Clean Old Backups**: Regularly delete unneeded old backups to save storage space
5. **Multiple Copies**: Consider keeping recovery file in multiple secure locations

## Script Path

Script file is located in Skill directory at `scripts/backup.py`.

When executing Bash commands, ensure correct relative or absolute path is used. Usually:
- If currently in Skill directory: `python3 scripts/backup.py ...`
- If in other directory: Use absolute path or `cd` to Skill directory first

## Reference Documentation

- [soul-upload.com Backup Guide](https://soul-upload.com/guides/how-to-backup-soul-md)
- [soul-upload.com Restore Guide](https://soul-upload.com/guides/how-to-restore-soul-md)
- [OpenClaw Agent Documentation](https://openclaw.com)

---

**Version**: 2.0.0
**Author**: Claude Code
**License**: MIT
**Password Policy**: Auto-generated unique password per backup (NEW in v2.0.0)
