---
name: sync-content
description: Sync gallery images and content to S3. Use after adding new photos to the portfolio.
allowed-tools: Bash, Read
---

# Sync Content to S3

Sync local gallery content to AWS S3 bucket.

## Arguments
- `$ARGUMENTS` - Optional: specific gallery folder to sync

## Steps
1. Verify AWS credentials:
   ```bash
   aws sts get-caller-identity --profile pitfal
   ```

2. Sync all media files:
   ```bash
   aws s3 sync ./content/galleries/ s3://pitfal-media/galleries/ \
     --profile pitfal \
     --exclude "*.DS_Store" \
     --exclude "*.tmp" \
     --exclude ".git/*"
   ```

3. Report files uploaded and total size

## For Specific Gallery
If `$ARGUMENTS` is provided:
```bash
aws s3 sync ./content/galleries/$ARGUMENTS/ s3://pitfal-media/galleries/$ARGUMENTS/ \
  --profile pitfal \
  --exclude "*.DS_Store"
```

## Dry Run (Preview Only)
To see what would be synced without uploading:
```bash
aws s3 sync ./content/galleries/ s3://pitfal-media/galleries/ \
  --profile pitfal \
  --dryrun
```

## Output
Report:
- Number of files uploaded
- Number of files deleted (if --delete used)
- Total data transferred
- S3 bucket URL
