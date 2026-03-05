---
name: backup-strategy
description: Implement automated backup strategy for VPS servers with regular snapshots, off-server storage, and retention policies to enable quick disaster recovery.
license: MIT
compatibility: Ubuntu, Debian, CentOS, RHEL, and most Linux distributions
metadata:
  author: secure-server-skill
  version: "1.0"
  category: disaster-recovery
allowed-tools: Bash(tar:*, gzip:*, rsync:*, cron:*, aws:*, scp:*)
---

# Backup Strategy Skill

Implement automated backup solutions for VPS servers to ensure quick recovery from security incidents or system failures.

## What This Skill Does

This skill helps AI agents configure automated backup systems on VPS servers. Security isn't just prevention - it's recovery. If your server gets compromised, you need to rebuild quickly. Regular, off-server backups are essential for business continuity and disaster recovery.

**Key capabilities:**

- Create automated backup scripts
- Schedule regular backups with cron
- Implement retention policies (keep N days of backups)
- Compress and encrypt backup archives
- Store backups off-server (S3, remote server, etc.)
- Verify backup integrity
- Document restoration procedures

## When to Use

Use this skill when you need to:

- Set up new server with backup strategy
- Implement disaster recovery plan
- Comply with data retention requirements
- Protect against ransomware and data loss
- Enable quick server rebuilds
- Meet business continuity requirements

**Critical understanding:** The backup must NOT be on the same server. If the server is compromised, local backups can be deleted or encrypted by attackers.

## Prerequisites

- Root or sudo access to the server
- Sufficient disk space for temporary backups
- Off-server storage solution (S3, remote server, NAS, etc.)
- Understanding of what needs to be backed up
- Credentials for remote storage (if applicable)

## What to Back Up

### Critical Directories

```bash
/home                    # User home directories
/etc                     # System and application configuration
/var/www                 # Web server content
/var/lib/mysql           # MySQL databases (if using file-based)
/root                    # Root user home (if used)
/opt                     # Optional software installations
/usr/local               # Locally installed software
```

### What NOT to Back Up

```bash
/tmp                     # Temporary files
/var/tmp                 # Temporary files
/proc                    # Virtual filesystem
/sys                     # Virtual filesystem
/dev                     # Device files
/run                     # Runtime data
/var/cache               # Cache files
```

## Basic Backup Script

### Simple Tar-Based Backup

Create `/usr/local/bin/backup.sh`:

```bash
#!/bin/bash
#
# Simple backup script using tar and gzip
#

# Configuration
BACKUP_DIR="/backup"
DATE=$(date +%Y-%m-%d)
BACKUP_NAME="backup-$DATE.tar.gz"
RETENTION_DAYS=7

# Create backup directory
mkdir -p "$BACKUP_DIR"

# Create compressed archive
echo "Creating backup: $BACKUP_NAME"
tar -czf "$BACKUP_DIR/$BACKUP_NAME" \
    --exclude='/backup' \
    --exclude='/proc' \
    --exclude='/sys' \
    --exclude='/dev' \
    --exclude='/run' \
    --exclude='/tmp' \
    --exclude='/var/tmp' \
    --exclude='/var/cache' \
    /home \
    /etc \
    /var/www \
    /root \
    2>/var/log/backup-error.log

# Check if backup was successful
if [ $? -eq 0 ]; then
    echo "Backup completed successfully"
    echo "Backup saved to: $BACKUP_DIR/$BACKUP_NAME"
else
    echo "Backup failed! Check /var/log/backup-error.log"
    exit 1
fi

# Delete old backups (keep last N days)
echo "Cleaning up old backups (keeping last $RETENTION_DAYS days)..."
find "$BACKUP_DIR" -name "backup-*.tar.gz" -mtime +$RETENTION_DAYS -delete

echo "Backup process complete"
```

Make it executable:

```bash
sudo chmod +x /usr/local/bin/backup.sh
```

## Advanced Backup Strategies

### Database Backups

**MySQL/MariaDB:**

```bash
#!/bin/bash
# MySQL backup script

DB_USER="root"
DB_PASS="your_password"
BACKUP_DIR="/backup/mysql"
DATE=$(date +%Y-%m-%d)

mkdir -p "$BACKUP_DIR"

# Backup all databases
mysqldump -u"$DB_USER" -p"$DB_PASS" --all-databases \
    --single-transaction \
    --quick \
    --lock-tables=false \
    > "$BACKUP_DIR/all-databases-$DATE.sql"

# Compress
gzip "$BACKUP_DIR/all-databases-$DATE.sql"

# Delete old backups
find "$BACKUP_DIR" -name "all-databases-*.sql.gz" -mtime +7 -delete
```

**PostgreSQL:**

```bash
#!/bin/bash
# PostgreSQL backup script

BACKUP_DIR="/backup/postgresql"
DATE=$(date +%Y-%m-%d)

mkdir -p "$BACKUP_DIR"

# Backup all databases
sudo -u postgres pg_dumpall > "$BACKUP_DIR/pg-backup-$DATE.sql"

# Compress
gzip "$BACKUP_DIR/pg-backup-$DATE.sql"

# Delete old backups
find "$BACKUP_DIR" -name "pg-backup-*.sql.gz" -mtime +7 -delete
```

### Incremental Backups with rsync

```bash
#!/bin/bash
# Incremental backup using rsync

BACKUP_DIR="/backup/incremental"
CURRENT="$BACKUP_DIR/current"
DATE=$(date +%Y-%m-%d-%H%M%S)
SNAPSHOT="$BACKUP_DIR/$DATE"

# Create backup directory
mkdir -p "$BACKUP_DIR"

# Perform incremental backup
rsync -av --delete \
    --link-dest="$CURRENT" \
    --exclude='/backup' \
    --exclude='/proc' \
    --exclude='/sys' \
    /home \
    /etc \
    /var/www \
    "$SNAPSHOT"

# Update current symlink
rm -f "$CURRENT"
ln -s "$SNAPSHOT" "$CURRENT"

# Keep only last 10 snapshots
ls -1dt "$BACKUP_DIR"/2* | tail -n +11 | xargs rm -rf
```

## Off-Server Storage

### AWS S3 Backup

```bash
#!/bin/bash
# Backup to AWS S3

BACKUP_DIR="/backup"
S3_BUCKET="s3://my-backups/server-name"
DATE=$(date +%Y-%m-%d)
BACKUP_FILE="backup-$DATE.tar.gz"

# Create backup
tar -czf "$BACKUP_DIR/$BACKUP_FILE" /home /etc /var/www

# Upload to S3
aws s3 cp "$BACKUP_DIR/$BACKUP_FILE" "$S3_BUCKET/"

# Verify upload
if [ $? -eq 0 ]; then
    echo "Backup uploaded to S3 successfully"
    # Remove local copy after successful upload
    rm "$BACKUP_DIR/$BACKUP_FILE"
else
    echo "S3 upload failed!"
    exit 1
fi

# S3 lifecycle policy handles retention
```

### SCP to Remote Server

```bash
#!/bin/bash
# Backup to remote server via SCP

BACKUP_DIR="/backup"
REMOTE_USER="backup"
REMOTE_HOST="backup-server.example.com"
REMOTE_DIR="/backups/webserver"
DATE=$(date +%Y-%m-%d)
BACKUP_FILE="backup-$DATE.tar.gz"

# Create backup
tar -czf "$BACKUP_DIR/$BACKUP_FILE" /home /etc /var/www

# Upload via SCP (requires SSH key authentication)
scp "$BACKUP_DIR/$BACKUP_FILE" "$REMOTE_USER@$REMOTE_HOST:$REMOTE_DIR/"

# Verify upload
if [ $? -eq 0 ]; then
    echo "Backup transferred successfully"
    rm "$BACKUP_DIR/$BACKUP_FILE"
else
    echo "Transfer failed!"
    exit 1
fi
```

### Encrypted Backups

```bash
#!/bin/bash
# Create encrypted backup

BACKUP_DIR="/backup"
DATE=$(date +%Y-%m-%d)
BACKUP_FILE="backup-$DATE.tar.gz"
ENCRYPTED_FILE="backup-$DATE.tar.gz.gpg"
GPG_RECIPIENT="admin@example.com"

# Create compressed backup
tar -czf "$BACKUP_DIR/$BACKUP_FILE" /home /etc /var/www

# Encrypt with GPG
gpg --encrypt --recipient "$GPG_RECIPIENT" \
    --output "$BACKUP_DIR/$ENCRYPTED_FILE" \
    "$BACKUP_DIR/$BACKUP_FILE"

# Remove unencrypted version
rm "$BACKUP_DIR/$BACKUP_FILE"

# Upload encrypted backup (S3, SCP, etc.)
# ...

echo "Encrypted backup created: $ENCRYPTED_FILE"
```

## Scheduling Backups with Cron

### Edit Crontab

```bash
sudo crontab -e
```

### Common Schedules

```bash
# Daily at 2 AM
0 2 * * * /usr/local/bin/backup.sh >> /var/log/backup.log 2>&1

# Weekly on Sunday at 3 AM
0 3 * * 0 /usr/local/bin/backup.sh

# Daily at 2 AM, keep 30 days
0 2 * * * /usr/local/bin/backup.sh && find /backup -name "backup-*.tar.gz" -mtime +30 -delete

# Every 6 hours
0 */6 * * * /usr/local/bin/backup.sh

# Monthly on the 1st at midnight
0 0 1 * * /usr/local/bin/backup.sh
```

### Cron with Logging

```bash
# Daily backup with logging and email on failure
0 2 * * * /usr/local/bin/backup.sh > /var/log/backup-$(date +\%Y\%m\%d).log 2>&1 || mail -s "Backup Failed" admin@example.com < /var/log/backup-$(date +\%Y\%m\%d).log
```

## Backup Verification

### Check Backup Integrity

```bash
#!/bin/bash
# Verify backup archive integrity

BACKUP_FILE="/backup/backup-2024-01-31.tar.gz"

# Test gzip integrity
gzip -t "$BACKUP_FILE"

if [ $? -eq 0 ]; then
    echo "Backup archive is valid"
else
    echo "Backup archive is corrupted!"
    exit 1
fi

# Test tar contents
tar -tzf "$BACKUP_FILE" > /dev/null

if [ $? -eq 0 ]; then
    echo "Tar archive structure is valid"
else
    echo "Tar archive has errors!"
    exit 1
fi
```

### List Backup Contents

```bash
# List files in backup
tar -tzf /backup/backup-2024-01-31.tar.gz | less

# Search for specific file
tar -tzf /backup/backup-2024-01-31.tar.gz | grep "config.php"
```

## Restoration Procedures

### Full System Restore

```bash
#!/bin/bash
# Restore from backup

BACKUP_FILE="/backup/backup-2024-01-31.tar.gz"

# WARNING: This will overwrite existing files!
echo "WARNING: This will restore files and may overwrite existing data!"
read -p "Continue? (yes/no): " CONFIRM

if [ "$CONFIRM" != "yes" ]; then
    echo "Aborted"
    exit 1
fi

# Extract to root
cd /
tar -xzf "$BACKUP_FILE"

echo "Restore complete. Review extracted files and restart services."
```

### Restore Specific Directory

```bash
# Restore only /etc
tar -xzf /backup/backup-2024-01-31.tar.gz -C / etc/

# Restore specific file
tar -xzf /backup/backup-2024-01-31.tar.gz -C / etc/nginx/nginx.conf
```

### Restore Database

```bash
# MySQL restore
gunzip < /backup/mysql/all-databases-2024-01-31.sql.gz | mysql -uroot -p

# PostgreSQL restore
gunzip < /backup/postgresql/pg-backup-2024-01-31.sql.gz | sudo -u postgres psql
```

## Monitoring and Alerting

### Email Notifications

```bash
#!/bin/bash
# Backup with email notification

BACKUP_SCRIPT="/usr/local/bin/backup.sh"
ADMIN_EMAIL="admin@example.com"

# Run backup
if $BACKUP_SCRIPT; then
    echo "Backup completed successfully on $(date)" | \
        mail -s "Backup Success - $(hostname)" "$ADMIN_EMAIL"
else
    echo "Backup failed on $(date)" | \
        mail -s "BACKUP FAILED - $(hostname)" "$ADMIN_EMAIL"
fi
```

### Check Last Backup Age

```bash
#!/bin/bash
# Alert if backup is too old

BACKUP_DIR="/backup"
MAX_AGE_HOURS=26  # Alert if no backup in last 26 hours

LATEST_BACKUP=$(find "$BACKUP_DIR" -name "backup-*.tar.gz" -type f -printf '%T@ %p\n' | sort -n | tail -1 | cut -d' ' -f2-)

if [ -z "$LATEST_BACKUP" ]; then
    echo "No backups found!" | mail -s "BACKUP ALERT" admin@example.com
    exit 1
fi

AGE_SECONDS=$(($(date +%s) - $(stat -c %Y "$LATEST_BACKUP")))
AGE_HOURS=$((AGE_SECONDS / 3600))

if [ $AGE_HOURS -gt $MAX_AGE_HOURS ]; then
    echo "Last backup is $AGE_HOURS hours old!" | \
        mail -s "BACKUP TOO OLD" admin@example.com
fi
```

## Security Best Practices

1. **Off-server storage** - Never rely solely on local backups
2. **Encryption** - Encrypt sensitive backups, especially if storing remotely
3. **Access control** - Restrict backup file permissions (600 or 640)
4. **Test restores** - Regularly test that backups can be restored
5. **Monitor backup jobs** - Alert on failures
6. **Retention policy** - Balance storage costs with recovery needs
7. **Version backups** - Keep multiple generations
8. **Document procedures** - Maintain restoration runbooks
9. **Separate credentials** - Don't store backup credentials on the server being backed up

## Common Mistakes to Avoid

- ❌ Only backing up to the same server (single point of failure)
- ❌ Not testing restore procedures
- ❌ Backing up cached/temporary files (waste of space)
- ❌ Not encrypting backups containing sensitive data
- ❌ Setting retention too short (can't recover from old issues)
- ❌ Not monitoring backup success/failure
- ❌ Including backup directory in backup (infinite loop!)
- ❌ Not documenting what's backed up and how to restore

## Additional Resources

See [references/backup-locations.md](references/backup-locations.md) for storage provider comparison.

See [scripts/backup-full.sh](scripts/backup-full.sh) for comprehensive backup script.

See [scripts/backup-mysql.sh](scripts/backup-mysql.sh) for database-specific backup.

## Related Skills

- `auto-updates` - Keep backup tools updated
- `ssh-hardening` - Secure SSH for remote backups
- `firewall-configuration` - Protect backup storage access
