---
name: localstack-logs
description: Analyze LocalStack logs and debug issues. Use when users need to view LocalStack logs, debug AWS API errors, troubleshoot Lambda functions, identify error patterns, or enable debug mode.
---

# LocalStack Logs Analysis

Analyze LocalStack logs to debug issues, identify errors, and understand AWS API interactions.

## Capabilities

- View and filter LocalStack logs
- Identify error patterns and failures
- Analyze AWS API request/response cycles
- Track service-specific operations
- Debug Lambda function executions

## Viewing Logs

### Basic Log Commands

```bash
# Follow logs in real-time
localstack logs -f

# View last N lines
localstack logs --tail 100

# Via Docker
docker logs localstack-main -f
docker logs localstack-main --tail 200
```

### Filtering Logs

```bash
# Filter by service
localstack logs | grep -i s3
localstack logs | grep -i lambda
localstack logs | grep -i dynamodb

# Filter errors only
localstack logs | grep -i error
localstack logs | grep -i exception

# Filter by request ID
localstack logs | grep "request-id-here"
```

## Debug Mode

Enable detailed logging:

```bash
# Start with debug mode
DEBUG=1 localstack start -d

# Enable specific debug flags
LS_LOG=trace localstack start -d
```

## Analyzing API Requests

### Request/Response Tracking

LocalStack logs include AWS API requests. Look for patterns like:

```
AWS <service>.<operation> => <status>
```

Example log entries:
```
AWS s3.CreateBucket => 200
AWS dynamodb.PutItem => 200
AWS lambda.Invoke => 200
```

### Common Error Patterns

| Error | Possible Cause | Solution |
|-------|---------------|----------|
| `ResourceNotFoundException` | Resource doesn't exist | Create the resource first |
| `AccessDeniedException` | IAM policy issue | Check IAM enforcement mode |
| `ValidationException` | Invalid parameters | Verify request parameters |
| `ServiceException` | Internal error | Check LocalStack logs for details |

## Lambda Debugging

### View Lambda Logs

```bash
# Lambda function logs appear in LocalStack logs
localstack logs | grep -A 10 "Lambda"

# Or use CloudWatch Logs locally
awslocal logs describe-log-groups
awslocal logs get-log-events \
  --log-group-name /aws/lambda/my-function \
  --log-stream-name <stream-name>
```

### Enable Lambda Debug Mode

```bash
LAMBDA_DEBUG=1 localstack start -d
```

## Health Check

```bash
# Check overall health
curl http://localhost:4566/_localstack/health | jq

# Check specific service
curl http://localhost:4566/_localstack/health | jq '.services.s3'
```

## Troubleshooting Tips

- **No logs appearing**: Ensure LocalStack is running (`localstack status`)
- **Missing debug info**: Enable `DEBUG=1` for verbose logging
- **Lambda issues**: Check both LocalStack logs and CloudWatch Logs
- **Intermittent errors**: Look for resource limits or timing issues
