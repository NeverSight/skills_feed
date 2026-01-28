---
name: logs
description: View recent CloudWatch logs for Lambda functions and API Gateway.
allowed-tools: Bash
---

# View CloudWatch Logs

Fetch and display recent logs from AWS CloudWatch.

## Arguments
- `$ARGUMENTS` - Optional: function name (contact, booking, proofing, orders)

## Default: All Functions
Show recent logs from all Lambda functions:
```bash
for func in contact booking proofing orders; do
  echo "=== pitfal-${func} ==="
  aws logs tail /aws/lambda/pitfal-${func} \
    --since 1h \
    --profile pitfal \
    --format short 2>/dev/null || echo "No logs found"
  echo ""
done
```

## Specific Function
If `$ARGUMENTS` is provided (e.g., `/logs contact`):
```bash
aws logs tail /aws/lambda/pitfal-$ARGUMENTS \
  --follow \
  --profile pitfal \
  --format short
```

## Error Filtering
Show only errors from the last hour:
```bash
aws logs filter-log-events \
  --log-group-name /aws/lambda/pitfal-${ARGUMENTS:-contact} \
  --filter-pattern "ERROR" \
  --start-time $(( $(date +%s) - 3600 ))000 \
  --profile pitfal
```

## API Gateway Logs
```bash
aws logs tail /aws/api-gateway/pitfal-api \
  --since 1h \
  --profile pitfal \
  --format short
```

## Output Format
Display logs with:
- Timestamp
- Log level (INFO/WARN/ERROR)
- Message content
- Request ID (if available)
