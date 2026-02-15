---
name: api-billing-service-onboarding
description: This skill should be used when the user requests to add a new third-party API service to the AWS billing/quota monitoring system. It handles the complete onboarding process including adapter creation, Lambda deployment, CloudWatch alarms, Dashboard updates, and verification. Triggers on requests mentioning "add service monitoring", "monitor API balance", "setup quota alerts", "add to billing dashboard", or similar service integration requests.
---

# API Billing Service Onboarding

Automates the complete process of adding a new third-party API service to the AWS Lambda-based billing and quota monitoring system.

## Purpose

This skill provides a step-by-step workflow for integrating new API services into an existing AWS monitoring infrastructure that tracks account balances, quotas, and usage across multiple third-party services. The system monitors services every 30 minutes, pushes metrics to CloudWatch, triggers alerts via SNS to Feishu, and visualizes data on a centralized dashboard.

## When to Use

Use this skill when the user requests to:
- Add monitoring for a new API service's balance, quota, or credits
- Set up alerts for low balance/quota on a third-party service
- Integrate a new service into the billing dashboard
- Monitor remaining usage or spending on an external API

Common trigger phrases:
- "Add [Service] to monitoring"
- "Monitor [Service] API balance"
- "Set up quota alerts for [Service]"
- "Track [Service] credits in dashboard"

## Project Context

The monitoring system is located in `/Users/cdd/Code/all-code-in-mba/source-code/lambda-function/` and consists of:

- **Runtime**: Node.js 18.x (TypeScript)
- **Cloud Platform**: AWS Lambda + CloudWatch + Secrets Manager + EventBridge + SNS
- **Commands**: Managed via `just` (see `justfile`)
- **Architecture**: EventBridge (30min) → Lambda → CloudWatch Metrics → Alarms → SNS → Feishu

**Key Files**:
- `adapters/*.ts` - API service adapters
- `adapters/index.ts` - Adapter registry
- `src/handler.ts` - Lambda entry point
- `src/types.ts` - BillingMetric interface
- `src/metrics.ts` - CloudWatch metric publishing
- `CLAUDE.md` - Project documentation

## Workflow

### Step 1: Gather Service Information

Before starting implementation, collect the following information from the user:

1. **Service name** (e.g., "resend", "sendgrid")
2. **API documentation URL** (especially balance/quota endpoints)
3. **API Key/Token** (will be stored in Secrets Manager)
4. **Alert threshold** (absolute value or percentage)
5. **Service display name** (for Dashboard labels)

**Questions to ask**:
- "What is the API endpoint for checking balance/quota?"
- "How does the API authenticate? (Bearer token, API key header, query param?)"
- "What response format does the API return? (JSON structure)"
- "What threshold should trigger an alert? (e.g., remaining < 100, or < 5%)"
- "What unit does the service use? (USD, credits, emails, requests?)"

### Step 2: Create API Adapter

Create a new TypeScript adapter file at `adapters/<service_name>.ts`.

**Refer to**: `references/adapter-templates.md` for three common adapter patterns:
- Standard JSON response with balance fields
- Response headers containing quota information
- Prepaid credits with no total amount

The adapter must:
1. Call the service's API to retrieve balance/quota
2. Mask the API key (show first 6 and last 6 characters)
3. Return a `BillingMetric` object with:
   - `service`: lowercase service identifier
   - `apiKeyMask`: masked API key
   - `total`: total quota/balance
   - `remaining`: remaining quota/balance
   - `remainingRatio`: remaining/total (0-1)
   - `currency` (optional): "USD", "CNY", etc.
   - `unit` (optional): "credits", "emails", "requests"

**Use the Read tool** to examine existing adapters for reference:
- `adapters/resend.ts` - Response header quota pattern
- `adapters/serper.ts` - Prepaid credits pattern
- `adapters/scrapedo.ts` - Standard JSON response pattern

### Step 3: Register Adapter

Edit `adapters/index.ts`:
1. Import the new adapter function
2. Add entry to the `adapters` object

Example:
```typescript
import { fetchServiceName } from "./service_name";

export const adapters = {
  // ... existing adapters
  service_name: fetchServiceName,
};
```

### Step 4: Update Lambda Handler

Edit `src/handler.ts` to add the service call logic.

**Location**: Insert before `console.log("✅ Billing check completed")`

**Pattern**:
```typescript
// <Service Display Name>
if (apiKeys.<service_name>) {
  try {
    console.log("🔍 Fetching <Service> quota...");
    const metric = await adapters.<service_name>(apiKeys.<service_name>);
    await pushMetrics(metric);
    results.push({
      service: "<service_name>",
      status: "success",
      remaining: metric.remaining,
      total: metric.total,
      ratio: metric.remainingRatio
    });
  } catch (error: any) {
    console.error("❌ <Service> error:", error.message);
    results.push({ service: "<service_name>", status: "error", error: error.message });
  }
}
```

### Step 5: Add API Key to Secrets Manager

Use the helper script to safely add the API key:

```bash
scripts/add-secret-key.sh <service_name> <api_key>
```

**Manual alternative**:
```bash
# Get current secrets
aws secretsmanager get-secret-value \
  --secret-id api-billing-monitor/keys \
  --query SecretString --output text > /tmp/secrets.json

# Edit /tmp/secrets.json to add: "<service_name>": "<api_key>"

# Update secrets
aws secretsmanager update-secret \
  --secret-id api-billing-monitor/keys \
  --secret-string file:///tmp/secrets.json
```

### Step 6: Build and Deploy

```bash
# Quick deployment (recommended)
just deploy-quick

# Or full deployment with verbose output
just deploy
```

Verify deployment:
```bash
# Trigger Lambda manually
just invoke

# Check logs for the new service
just logs | grep <service_name>
```

### Step 7: Create CloudWatch Alarm

Choose the appropriate alarm strategy:

**Strategy A: Absolute Value Threshold** (for fixed quotas):
```bash
aws cloudwatch put-metric-alarm \
  --alarm-name "<Service>-Low-Balance" \
  --namespace "ThirdPartyAPIBilling" \
  --metric-name "Remaining" \
  --dimensions Name=Service,Value=<service_name> \
  --statistic Average \
  --period 1800 \
  --evaluation-periods 1 \
  --threshold <absolute_value> \
  --comparison-operator LessThanThreshold \
  --alarm-actions "arn:aws:sns:us-east-1:830101142436:CloudWatchAlarmsToFeishu" \
  --alarm-description "<Service> remaining balance below <threshold>"
```

**Strategy B: Percentage Threshold** (for variable quotas):
```bash
aws cloudwatch put-metric-alarm \
  --alarm-name "<Service>-Low-Ratio" \
  --namespace "ThirdPartyAPIBilling" \
  --metric-name "RemainingRatio" \
  --dimensions Name=Service,Value=<service_name> \
  --statistic Average \
  --period 1800 \
  --evaluation-periods 1 \
  --threshold 0.05 \
  --comparison-operator LessThanThreshold \
  --alarm-actions "arn:aws:sns:us-east-1:830101142436:CloudWatchAlarmsToFeishu" \
  --alarm-description "<Service> remaining ratio below 5%"
```

Verify alarm creation:
```bash
just alarms | grep <Service>
```

### Step 8: Update CloudWatch Dashboard

Use the helper script to automatically add the service to the dashboard:

```bash
scripts/add-to-dashboard.sh <service_name> "<Service Display Name>" "<masked_api_key>"
```

**Manual alternative**:
1. Get current dashboard configuration:
   ```bash
   aws cloudwatch get-dashboard \
     --dashboard-name "API-Billing-Monitor" \
     --query "DashboardBody" \
     --output text > /tmp/dashboard.json
   ```

2. Edit `/tmp/dashboard.json` to add the service in **4 locations**:
   - "所有服务剩余比例趋势" metrics array
   - "当前剩余比例" metrics array
   - Create a new widget (optional, for detailed service chart)
   - "当前剩余额度/Credits" metrics array

3. Update dashboard:
   ```bash
   aws cloudwatch put-dashboard \
     --dashboard-name "API-Billing-Monitor" \
     --dashboard-body file:///tmp/dashboard.json
   ```

**Refer to**: `references/dashboard-widget-template.json` for widget JSON structure examples.

### Step 9: Update Project Documentation

Edit `CLAUDE.md` to add the new service to the "已接入服务" table:

```markdown
| <service_name> | <unit> | <threshold> | <description> |
```

### Step 10: Verification

Run the complete verification checklist:

```bash
# 1. Trigger monitoring
just invoke

# 2. Check logs for successful execution
just logs | grep "<service_name>"
# Expected: "✅ Metrics pushed for <service_name>"

# 3. Verify metrics in CloudWatch
aws cloudwatch list-metrics \
  --namespace ThirdPartyAPIBilling \
  --dimensions Name=Service,Value=<service_name>

# 4. Check alarm status
just alarms | grep "<Service>"

# 5. View current status
just status

# 6. Visit dashboard
echo "https://us-east-1.console.aws.amazon.com/cloudwatch/home?region=us-east-1#dashboards/dashboard/API-Billing-Monitor"
```

**Success criteria**:
- ✅ Lambda logs show successful metric push
- ✅ CloudWatch metrics exist for the service
- ✅ Alarm is in OK or ALARM state (not INSUFFICIENT_DATA)
- ✅ Dashboard displays the service in all charts
- ✅ Service appears in `just status` output

## Troubleshooting

**Lambda execution fails**:
- Check logs: `just logs`
- Verify API key in Secrets Manager: `just secrets-full`
- Test API endpoint manually with curl/Postman

**Metrics not appearing in CloudWatch**:
- Confirm Lambda executed successfully: `just invoke`
- Check for errors in adapter code
- Verify metric push logic in logs

**Dashboard shows no data**:
- Wait 30 minutes for first execution cycle
- Confirm metrics exist: `aws cloudwatch list-metrics --namespace ThirdPartyAPIBilling`
- Verify Dashboard JSON syntax

**Alarm not triggering**:
- Check alarm configuration: `aws cloudwatch describe-alarms --alarm-names "<Service>-Low-Balance"`
- Verify metric data points exist
- Test alarm: `just test-alarm <Service>-Low-Balance`

## Notes

- The system runs on a 30-minute schedule via EventBridge
- All API keys are stored securely in AWS Secrets Manager
- Alarms notify via SNS to Feishu webhook
- The CloudWatch namespace is `ThirdPartyAPIBilling`
- Common dimension: `Service=<service_name>`, `APIKey=<masked_key>`

For detailed examples and edge cases, refer to `references/service-integration-examples.md`.
