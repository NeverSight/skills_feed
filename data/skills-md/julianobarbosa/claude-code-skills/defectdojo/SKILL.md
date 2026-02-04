---
name: defectdojo
description: Guide for implementing DefectDojo - an open-source DevSecOps, ASPM, and vulnerability management platform. Use when querying vulnerabilities, managing findings, configuring CI/CD pipeline imports, or working with security scan data. Includes MCP tools for direct API interaction.
tools:
  - defectdojo_list_products
  - defectdojo_get_product
  - defectdojo_list_engagements
  - defectdojo_list_tests
  - defectdojo_list_findings
  - defectdojo_get_finding
  - defectdojo_get_statistics
  - defectdojo_list_endpoints
  - defectdojo_list_test_types
  - defectdojo_create_engagement
  - defectdojo_update_finding
  - defectdojo_close_engagement
---

# DefectDojo Skill

## Overview

DefectDojo is an open-source DevSecOps, Application Security Posture Management (ASPM), and vulnerability management platform. It orchestrates end-to-end security testing, vulnerability tracking, deduplication, remediation, and reporting.

**Key Capabilities:**

- Unified vulnerability management across 200+ security tools
- Automated scan import and deduplication
- CI/CD pipeline integration
- Bidirectional JIRA integration
- Role-based access control
- SLA tracking and reporting
- REST API v2 for automation
- **MCP Tools for Claude Code integration**

**Official Resources:**

- Documentation: <https://docs.defectdojo.com/>
- GitHub: <https://github.com/DefectDojo/django-DefectDojo>
- Demo: <https://demo.defectdojo.org> (admin / 1Defectdojo@demo#appsec)

## MCP Tools (Primary Interface)

This skill provides 12 MCP tools for direct DefectDojo API interaction. Use these tools instead of manual API calls.

### Read Operations

| Tool | Description | Key Parameters |
|------|-------------|----------------|
| `defectdojo_list_products` | List and search products | `name_contains`, `prod_type`, `limit` |
| `defectdojo_get_product` | Get detailed product info | `product_id` (required) |
| `defectdojo_list_engagements` | List engagements with filters | `product_id`, `status`, `engagement_type` |
| `defectdojo_list_tests` | List tests in engagements | `engagement_id`, `test_type` |
| `defectdojo_list_findings` | **Primary tool** - Search findings | `severity`, `active`, `product_id`, `cwe` |
| `defectdojo_get_finding` | Get finding details | `finding_id` (required) |
| `defectdojo_get_statistics` | Vulnerability statistics | `product_id`, `engagement_id` |
| `defectdojo_list_endpoints` | List product endpoints | `product_id`, `host`, `protocol` |
| `defectdojo_list_test_types` | List scanner types | `name_contains` |

### Write Operations

| Tool | Description | Key Parameters |
|------|-------------|----------------|
| `defectdojo_create_engagement` | Create new engagement | `product_id`, `name`, `engagement_type` |
| `defectdojo_update_finding` | Update finding status | `finding_id`, `active`, `verified`, `false_p` |
| `defectdojo_close_engagement` | Close engagement | `engagement_id` |

### Usage Examples

**List all critical active findings:**

```
Use defectdojo_list_findings with:
- severity: "Critical"
- active: true
```

**Get vulnerability statistics for a product:**

```
Use defectdojo_get_statistics with:
- product_id: 1
```

**Search for SQL injection findings:**

```
Use defectdojo_list_findings with:
- cwe: 89
- active: true
```

**Mark a finding as false positive:**

```
Use defectdojo_update_finding with:
- finding_id: 123
- false_p: true
- active: false
```

**Create a CI/CD engagement:**

```
Use defectdojo_create_engagement with:
- product_id: 1
- name: "Pipeline Security Scan"
- engagement_type: "CI/CD"
```

### Response Formats

All tools support two output formats via the `response_format` parameter:

- `markdown` (default) - Human-readable formatted output
- `json` - Raw JSON for programmatic processing

### MCP Server Configuration

The MCP server is configured in `.mcp.json`:

```json
{
  "mcpServers": {
    "defectdojo": {
      "command": "python",
      "args": [".claude/mcp-servers/defectdojo-mcp/defectdojo_mcp.py"],
      "env": {
        "DEFECTDOJO_URL": "https://defectdojo.dev.cafehyna.com.br",
        "DEFECTDOJO_API_TOKEN": "${DEFECTDOJO_API_TOKEN}"
      }
    }
  }
}
```

**Environment Variables:**

- `DEFECTDOJO_URL` - Your DefectDojo instance URL
- `DEFECTDOJO_API_TOKEN` - API token from `/api/key-v2`

## Data Model (Product Hierarchy)

DefectDojo uses five interconnected data classes to organize security work:

```
Product Type
    └── Product
        └── Engagement (CI/CD or Interactive)
            └── Test
                └── Finding
                    └── Endpoint
```

### Product Types

The topmost organizational level that categorizes products by business domain, team, or security area. Enables role-based access control at the category level.

### Products

Individual applications or systems under security testing. Each product maintains:

- Its own testing history
- Deduplication scope (findings deduplicate within products)
- SLA configuration
- Team assignments

### Engagements

Scheduled testing periods containing one or more tests. Two types:

| Type | Purpose | Use Case |
|------|---------|----------|
| **CI/CD** | Automated pipeline integration | Automated scans per build/commit |
| **Interactive** | Manual testing by engineers | Penetration tests, manual reviews |

### Tests

Individual security scans grouped by tool type. Tests support:

- Reimporting (add findings to existing test)
- Environment tagging
- Version tracking

### Findings

Specific vulnerabilities discovered during testing:

| Severity | Description |
|----------|-------------|
| Critical | Immediate action required |
| High | High priority remediation |
| Medium | Standard priority |
| Low | Low priority |
| Info | Informational only |

**Finding States:**

- Active / Inactive
- Verified / Unverified
- Duplicate
- Mitigated
- False Positive
- Risk Accepted
- Out of Scope

### Endpoints

References to affected hosts, URLs, or systems. Enables vulnerability tracking by infrastructure component.

## API v2 Reference

> **Note:** For most operations, use the [MCP Tools](#mcp-tools-primary-interface) above instead of direct API calls. Use direct API calls only for scan imports or operations not covered by MCP tools.

### Authentication

Generate API token at: `<your-instance>/api/key-v2`

```bash
# Header format
Authorization: Token <api_key>
```

**Environment Variables:**

- `DD_API_TOKENS_ENABLED=False` - Disable API tokens entirely
- `DD_API_TOKEN_AUTH_ENDPOINT_ENABLED=False` - Disable only token auth endpoint

### Core Endpoints

| Endpoint | Method | Purpose |
|----------|--------|---------|
| `/api/v2/import-scan/` | POST | Initial scan import |
| `/api/v2/reimport-scan/` | POST | Subsequent imports (deduplication) |
| `/api/v2/products/` | GET/POST | Manage products |
| `/api/v2/engagements/` | GET/POST | Manage engagements |
| `/api/v2/tests/` | GET/POST | Manage tests |
| `/api/v2/findings/` | GET/POST/PATCH | Manage findings |
| `/api/v2/endpoints/` | GET/POST | Manage endpoints |
| `/api/v2/users/` | GET | List users |

### Import Scan Parameters

```bash
curl -X POST "https://defectdojo.example.com/api/v2/import-scan/" \
  -H "Authorization: Token <api-token>" \
  -F "scan_type=<scanner-type>" \
  -F "file=@results.json" \
  -F "engagement=<engagement-id>" \
  -F "minimum_severity=Info" \
  -F "active=true" \
  -F "verified=false" \
  -F "scan_date=2024-01-15"
```

**Key Parameters:**

| Parameter | Description |
|-----------|-------------|
| `scan_type` | Scanner identifier (e.g., "Trivy Scan", "Semgrep JSON Report") |
| `engagement` | Target engagement ID |
| `test_title` | Custom test name |
| `minimum_severity` | Filter threshold (Info, Low, Medium, High, Critical) |
| `active` | Mark findings as active (boolean) |
| `verified` | Mark findings as verified (boolean) |
| `scan_date` | Override scan completion date |
| `do_not_reactivate` | Prevent reopening closed findings |
| `auto_create_context` | Auto-create Product/Engagement if missing |

### Reimport Scan (Deduplication)

```bash
curl -X POST "https://defectdojo.example.com/api/v2/reimport-scan/" \
  -H "Authorization: Token <api-token>" \
  -F "scan_type=Trivy Scan" \
  -F "file=@trivy-results.json" \
  -F "test=<test-id>" \
  -F "do_not_reactivate=true"
```

The reimport endpoint:

- Detects new vs. existing findings
- Updates existing findings
- Closes findings not in the new scan
- Can auto-create context when `auto_create_context=true`

### Interactive API Documentation

Access Swagger UI at: `<your-instance>/api/v2/oa3/swagger-ui/`

## CI/CD Integration

### Pipeline Integration Pattern

```yaml
# GitLab CI Example
stages:
  - security-scan
  - upload-results

trivy-scan:
  stage: security-scan
  script:
    - trivy image --format json -o trivy-results.json $CI_REGISTRY_IMAGE:$CI_COMMIT_SHA
  artifacts:
    paths:
      - trivy-results.json

upload-to-defectdojo:
  stage: upload-results
  script: |
    curl -X POST "${DEFECTDOJO_URL}/api/v2/reimport-scan/" \
      -H "Authorization: Token ${DEFECTDOJO_API_TOKEN}" \
      -F "scan_type=Trivy Scan" \
      -F "file=@trivy-results.json" \
      -F "product_name=${CI_PROJECT_NAME}" \
      -F "engagement_name=CI/CD-${CI_PIPELINE_ID}" \
      -F "auto_create_context=true" \
      -F "minimum_severity=Low"
```

### Jenkins Integration

Install the DefectDojo Jenkins plugin from: <https://plugins.jenkins.io/defectdojo/>

**Pipeline Configuration:**

```groovy
pipeline {
    agent any
    environment {
        DEFECTDOJO_URL = 'https://defectdojo.example.com'
        DEFECTDOJO_API_KEY = credentials('defectdojo-api-key')
    }
    stages {
        stage('Security Scan') {
            steps {
                sh 'trivy image --format json -o trivy.json myapp:latest'
            }
        }
        stage('Upload to DefectDojo') {
            steps {
                defectDojoPublisher(
                    artifact: 'trivy.json',
                    productName: 'MyApp',
                    scanType: 'Trivy Scan',
                    engagementName: "Build-${BUILD_NUMBER}"
                )
            }
        }
    }
}
```

### GitHub Actions Integration

```yaml
name: Security Scan
on: [push]

jobs:
  security:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Run Trivy
        uses: aquasecurity/trivy-action@master
        with:
          scan-type: 'fs'
          format: 'json'
          output: 'trivy-results.json'

      - name: Upload to DefectDojo
        run: |
          curl -X POST "${{ secrets.DEFECTDOJO_URL }}/api/v2/reimport-scan/" \
            -H "Authorization: Token ${{ secrets.DEFECTDOJO_TOKEN }}" \
            -F "scan_type=Trivy Scan" \
            -F "file=@trivy-results.json" \
            -F "product_name=${{ github.repository }}" \
            -F "engagement_name=GitHub-${{ github.run_id }}" \
            -F "auto_create_context=true"
```

## Python API Examples

> **Tip:** For Claude Code interactions, use the MCP tools (`defectdojo_list_findings`, etc.) instead of writing Python code. The examples below are for CI/CD scripts and external integrations.

### Basic API Connection

```python
import requests

class DefectDojoAPI:
    def __init__(self, url, api_token):
        self.url = url.rstrip('/')
        self.headers = {
            'Authorization': f'Token {api_token}',
            'Accept': 'application/json'
        }

    def get_products(self):
        response = requests.get(
            f'{self.url}/api/v2/products/',
            headers=self.headers
        )
        response.raise_for_status()
        return response.json()

    def import_scan(self, engagement_id, scan_type, file_path, **kwargs):
        with open(file_path, 'rb') as f:
            data = {
                'engagement': engagement_id,
                'scan_type': scan_type,
                'minimum_severity': kwargs.get('minimum_severity', 'Info'),
                'active': kwargs.get('active', True),
                'verified': kwargs.get('verified', False),
            }
            files = {'file': f}
            response = requests.post(
                f'{self.url}/api/v2/import-scan/',
                headers={'Authorization': self.headers['Authorization']},
                data=data,
                files=files
            )
        response.raise_for_status()
        return response.json()

# Usage
api = DefectDojoAPI('https://defectdojo.example.com', 'your-api-token')
products = api.get_products()
```

### Create Product and Engagement

```python
def create_product(api, name, prod_type_id, description=''):
    response = requests.post(
        f'{api.url}/api/v2/products/',
        headers=api.headers,
        json={
            'name': name,
            'prod_type': prod_type_id,
            'description': description
        }
    )
    response.raise_for_status()
    return response.json()

def create_engagement(api, product_id, name, target_start, target_end,
                      engagement_type='CI/CD'):
    response = requests.post(
        f'{api.url}/api/v2/engagements/',
        headers=api.headers,
        json={
            'name': name,
            'product': product_id,
            'target_start': target_start,
            'target_end': target_end,
            'engagement_type': engagement_type,
            'status': 'In Progress'
        }
    )
    response.raise_for_status()
    return response.json()
```

### Query Findings

```python
def get_findings(api, product_id=None, severity=None, active=True):
    params = {'active': active}
    if product_id:
        params['test__engagement__product'] = product_id
    if severity:
        params['severity'] = severity

    response = requests.get(
        f'{api.url}/api/v2/findings/',
        headers=api.headers,
        params=params
    )
    response.raise_for_status()
    return response.json()

# Get all critical findings
critical = get_findings(api, severity='Critical')
```

## Supported Security Tools (200+)

### SAST / Code Analysis

- Bandit, Checkmarx, Fortify, SonarQube, Semgrep
- CodeQL, Horusec, Brakeman, SpotBugs

### Dependency / SCA

- Snyk, OWASP Dependency-Check, Dependency-Track
- npm Audit, pip-audit, Trivy, Safety

### DAST / Web Scanning

- Burp Suite, OWASP ZAP, Nikto, Nessus
- Qualys, OpenVAS, Acunetix, AppScan

### Container / Infrastructure

- Trivy, Aqua, Anchore, Wiz, NeuVector
- kube-bench, Kubescape, Prisma Cloud

### Secrets Detection

- Gitleaks, Trufflehog, Detect-secrets
- GitHub Secret Scanning

### Cloud Security

- AWS Inspector, AWS Prowler, ScoutSuite
- Azure Security Center, Checkov

### IaC Scanning

- Checkov, Terrascan, KICS, TFSec, Dockle

Full list: <https://docs.defectdojo.com/supported_tools/>

## JIRA Integration

### Configuration

1. **Enable in System Settings:**

   ```
   Configuration > System Settings > Enable JIRA Integration
   ```

2. **Add JIRA Instance:**

   ```
   Enterprise Settings > JIRA Instances > + New JIRA Instance
   ```

3. **Configure Webhook (bidirectional sync):**
   - Create webhook in JIRA pointing to:
     `https://<defectdojo>/jira/webhook/<webhook-secret>`
   - Enable in DefectDojo: "Enable JIRA web hook"

### Environment Variables

```yaml
extraEnv:
  - name: DD_JIRA_URL
    value: "https://your-jira.atlassian.net"
  - name: DD_JIRA_MAX_RETRIES
    value: "3"
```

### Features

- Push findings to JIRA as issues
- Bidirectional comment sync
- Auto-close findings when JIRA issues close
- SLA notifications as JIRA comments

## Project File Locations

| File Type | Path |
|-----------|------|
| ApplicationSet | `infra-team/applicationset/defectdojo.yaml` |
| Helm Values | `argo-cd-helm-values/kube-addons/defectdojo/<cluster>/values.yaml` |
| SecretProviderClass | `argo-cd-helm-values/kube-addons/defectdojo/<cluster>/secretproviderclass.yaml` |

### Environment Configuration

| Cluster | Key Vault | Azure AD Tenant ID |
|---------|-----------|-------------------|
| cafehyna-dev | `kv-cafehyna-dev-hlg` | `3f7a3df4-f85b-4ca8-98d0-08b1034e6567` |

### Azure AD App Registration

| Setting | Value |
|---------|-------|
| Application (Client) ID | `79ada8c7-4270-41e8-9ea0-1e1e62afff3d` |
| Tenant ID | `3f7a3df4-f85b-4ca8-98d0-08b1034e6567` |
| Redirect URI | `https://defectdojo.dev.cafehyna.com.br/complete/azuread-tenant-oauth2/` |

## Azure AD SSO Configuration

### Required Environment Variables

```yaml
extraEnv:
  # Enable Azure AD OAuth2
  - name: DD_SOCIAL_AUTH_AZUREAD_TENANT_OAUTH2_ENABLED
    value: "True"
  # Application (Client) ID
  - name: DD_SOCIAL_AUTH_AZUREAD_TENANT_OAUTH2_KEY
    value: "<client-id>"
  # Directory (Tenant) ID
  - name: DD_SOCIAL_AUTH_AZUREAD_TENANT_OAUTH2_TENANT_ID
    value: "<tenant-id>"
  # Client Secret (from Key Vault)
  - name: DD_SOCIAL_AUTH_AZUREAD_TENANT_OAUTH2_SECRET
    valueFrom:
      secretKeyRef:
        name: defectdojo
        key: DD_SOCIAL_AUTH_AZUREAD_TENANT_OAUTH2_SECRET
```

### Group Synchronization

```yaml
extraEnv:
  # Sync groups from Azure AD token
  - name: DD_SOCIAL_AUTH_AZUREAD_TENANT_OAUTH2_GET_GROUPS
    value: "True"
  # Remove users from groups when removed in Azure AD
  - name: DD_SOCIAL_AUTH_AZUREAD_TENANT_OAUTH2_CLEANUP_GROUPS
    value: "True"
  # Filter to only sync DefectDojo groups
  - name: DD_SOCIAL_AUTH_AZUREAD_TENANT_OAUTH2_GROUPS_FILTER
    value: "^G-Usuarios-DefectDojo-.*"
```

**Required Azure AD Permissions (Application type, Admin consent required):**

- `Group.Read.All`
- `GroupMember.Read.All`
- `User.Read.All`

For complete Azure AD SSO details, see [references/azure-ad-sso.md](references/azure-ad-sso.md).

## DefectDojo Roles

| Role | Permissions |
|------|-------------|
| **Superuser** | Full system access, manage users, system settings |
| **Owner** | Delete products, designate other owners |
| **Maintainer** | Edit products, add members, delete findings |
| **Writer** | Add/edit engagements, tests, findings |
| **Reader** | View-only, add comments |
| **API Importer** | Limited API access for CI/CD pipelines |

### Azure AD Groups for Role Mapping

| Azure AD Group | DefectDojo Role |
|----------------|-----------------|
| `G-Usuarios-DefectDojo-Superuser` | Superuser |
| `G-Usuarios-DefectDojo-Owner` | Owner |
| `G-Usuarios-DefectDojo-Maintainer` | Maintainer |
| `G-Usuarios-DefectDojo-Writer` | Writer |
| `G-Usuarios-DefectDojo-Reader` | Reader |

## Helm Chart Quick Reference

### Key Values

```yaml
# Host configuration
host: defectdojo.dev.cafehyna.com.br
siteUrl: https://defectdojo.dev.cafehyna.com.br

# Secrets (use CSI driver)
createSecret: false
disableHooks: true

# Django
django:
  replicas: 1
  ingress:
    enabled: true
    activateTLS: true
    className: nginx

# Celery (keep beat at 1 replica)
celery:
  beat:
    enabled: true
    replicas: 1
  worker:
    enabled: true
    replicas: 1

# Database
postgresql:
  enabled: true

# Cache
redis:
  enabled: true
```

For complete Helm values reference, see [references/helm-values.md](references/helm-values.md).

## Kubernetes Deployment

### Basic Helm Install

```bash
git clone https://github.com/DefectDojo/django-DefectDojo
cd django-DefectDojo

helm install defectdojo ./helm/defectdojo \
  -n defectdojo --create-namespace \
  --set django.ingress.enabled=true \
  --set django.ingress.activateTLS=false \
  --set createSecret=true \
  --set createRabbitMqSecret=true \
  --set createPostgresqlSecret=true
```

### Access DefectDojo

```bash
kubectl port-forward --namespace=defectdojo service/defectdojo-django 8080:80
```

## Secrets Management

Secrets are managed via Azure Key Vault CSI Driver:

| Key Vault Secret | K8s Secret Key | Purpose |
|------------------|----------------|---------|
| `defectdojo-admin-password` | `DD_ADMIN_PASSWORD` | Admin user password |
| `defectdojo-secret-key` | `DD_SECRET_KEY` | Django secret key |
| `defectdojo-credential-aes-key` | `DD_CREDENTIAL_AES_256_KEY` | Credential encryption |
| `defectdojo-azuread-client-secret` | `DD_SOCIAL_AUTH_AZUREAD_TENANT_OAUTH2_SECRET` | Azure AD client secret |

## Common Troubleshooting

### User Not in Groups After SSO Login

**Symptoms:** User logged in via Azure AD but shows "No group members found"

**Solutions:**

1. Verify `DD_SOCIAL_AUTH_AZUREAD_TENANT_OAUTH2_GET_GROUPS=True`
2. Check Azure AD API permissions (Group.Read.All with admin consent)
3. Verify Azure AD token includes group claim (not role claims)
4. User must log out and log back in to sync groups
5. Create matching groups in DefectDojo UI

### HTTPS Redirect URI Mismatch (ADSTS50011)

**Error:** "The redirect URI specified in the request does not match"

**Solution:** Ensure these are set:

```yaml
- name: DD_SESSION_COOKIE_SECURE
  value: "True"
- name: DD_CSRF_COOKIE_SECURE
  value: "True"
- name: DD_SECURE_PROXY_SSL_HEADER
  value: "True"
```

### ERR_TOO_MANY_REDIRECTS

**Cause:** `DD_SECURE_SSL_REDIRECT=True` with TLS-terminating proxy

**Solution:** Set `DD_SECURE_SSL_REDIRECT=False` when behind NGINX Ingress

### Emergency Login Access

If SSO breaks, access standard login form:

```
https://defectdojo.dev.cafehyna.com.br/login?force_login_form
```

For complete troubleshooting guide, see [references/troubleshooting.md](references/troubleshooting.md).

## Useful Commands

### Check Pod Status

```bash
KUBECONFIG=~/.kube/aks-rg-hypera-cafehyna-dev-config kubectl get pods -n defectdojo
```

### View Logs

```bash
KUBECONFIG=~/.kube/aks-rg-hypera-cafehyna-dev-config kubectl logs -n defectdojo -l app.kubernetes.io/name=defectdojo -c uwsgi
```

### Restart Deployment

```bash
KUBECONFIG=~/.kube/aks-rg-hypera-cafehyna-dev-config kubectl rollout restart deployment/defectdojo-django -n defectdojo
```

## Additional References

### MCP Server

- [MCP Server README](../../mcp-servers/defectdojo-mcp/README.md) - MCP server setup and usage
- [MCP Server Source](../../mcp-servers/defectdojo-mcp/defectdojo_mcp.py) - Server implementation

### Skill References

- [Azure AD SSO Configuration](references/azure-ad-sso.md) - Complete SSO setup guide
- [Helm Values Reference](references/helm-values.md) - Full Helm chart configuration
- [Troubleshooting Guide](references/troubleshooting.md) - Common issues and solutions
- [API v2 Reference](references/api-v2-reference.md) - Complete API documentation
- [CI/CD Integration Guide](references/cicd-integration.md) - Pipeline integration patterns

### External

- [Official Documentation](https://docs.defectdojo.com/)
- [Swagger UI](https://defectdojo.dev.cafehyna.com.br/api/v2/oa3/swagger-ui/) - Interactive API docs
