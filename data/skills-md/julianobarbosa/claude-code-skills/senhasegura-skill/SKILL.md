---
name: senhasegura-skill
description: Comprehensive senhasegura PAM platform skill for secrets management, credential vaulting, SSH key rotation, and DevOps secrets integration. Use when working with senhasegura A2A APIs, DSM CLI, MySafe, credential management, password rotation, External Secrets Operator integration, or any senhasegura PAM operations.
---

# Senhasegura PAM Platform Skill

Comprehensive guide for integrating with senhasegura (Segura) Privileged Access Management platform. Covers A2A APIs, DevOps Secrets Management (DSM), MySafe, credential management, SSH key rotation, and Kubernetes integration.

---

## Platform Overview

### Core Modules

| Module | Purpose | Use Case |
|--------|---------|----------|
| **PAM Core** | Credential vaulting, password rotation, session management | Enterprise credential management |
| **A2A** | Application-to-Application API authentication | Programmatic secrets access |
| **DSM** | DevOps Secret Manager for CI/CD pipelines | Pipeline secret injection |
| **MySafe** | Personal/team password manager | Corporate credential sharing |
| **Executions** | Automated password rotation, script execution | Scheduled credential changes |
| **SCIM** | Identity provisioning and management | User sync with IdP |

### Authentication Methods

| Method | Use Case | Security Level |
|--------|----------|----------------|
| **OAuth 2.0** | Recommended for all integrations | High (recommended) |
| **OAuth 1.0** | Legacy support | Medium |
| **AWS Signature** | AWS workloads | High |

---

## Authentication Setup

### OAuth 2.0 Configuration (Recommended)

#### Step 1: Create A2A Application

```
senhasegura Console:
1. Navigate to: A2A > Applications
2. Click: + New Application
3. Configure:
   - Name: my-app-integration
   - Authentication: OAuth 2.0
   - Enabled: Yes
4. Save and note the Client ID
```

#### Step 2: Retrieve Credentials

```
After saving:
1. Go to: A2A > Applications > [your-app]
2. Click: Authorization > View
3. Copy:
   - client_id: xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx
   - client_secret: xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
```

#### Step 3: Request Access Token

```bash
# OAuth 2.0 Token Request
curl -X POST "https://senhasegura.example.com/iso/oauth2/token" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "grant_type=client_credentials" \
  -d "client_id=YOUR_CLIENT_ID" \
  -d "client_secret=YOUR_CLIENT_SECRET"
```

Response:
```json
{
  "access_token": "eyJhbGciOiJSUzI1NiIsInR...",
  "token_type": "Bearer",
  "expires_in": 3600
}
```

#### Step 4: Use Token in API Calls

```bash
curl -X GET "https://senhasegura.example.com/api/pam/credential" \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN" \
  -H "Content-Type: application/json"
```

---

## PAM Core API Reference

### Credentials Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/api/pam/credential` | List all credentials |
| `GET` | `/api/pam/credential/{id}` | Get credential by ID |
| `POST` | `/api/pam/credential` | Create new credential |
| `PUT` | `/api/pam/credential/{id}` | Update credential |
| `DELETE` | `/api/pam/credential/{id}` | Disable credential |
| `DELETE` | `/iso/pam/credential/custody/{id}` | Release credential custody |

### List All Credentials

```bash
curl -X GET "https://senhasegura.example.com/api/pam/credential" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json"
```

Response:
```json
{
  "response": {
    "status": 200,
    "message": "Credentials found",
    "error": false,
    "error_code": 0,
    "credentials": [
      {
        "id": "123",
        "identifier": "db-admin-prod",
        "username": "admin",
        "hostname": "db.example.com",
        "ip": "10.0.1.50",
        "type": "Local User"
      }
    ]
  }
}
```

### Get Credential Password

```bash
# Legacy endpoint for password retrieval
curl -X GET "https://senhasegura.example.com/iso/coe/senha" \
  -H "Authorization: Bearer $TOKEN" \
  -d "credentialId=123"
```

Response:
```json
{
  "response": {
    "status": 200,
    "credential": {
      "id": "123",
      "password": "S3cur3P@ssw0rd!",
      "expiration": "2024-12-31T23:59:59Z"
    }
  }
}
```

### Create Credential

```bash
curl -X POST "https://senhasegura.example.com/api/pam/credential" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "identifier": "new-service-account",
    "username": "svc_app",
    "password": "InitialP@ss123",
    "hostname": "app-server.example.com",
    "ip": "10.0.2.100",
    "type": "Local User",
    "additional_info": "Service account for app",
    "tags": ["production", "critical"]
  }'
```

### Release Credential Custody

```bash
# After API password request, release custody
curl -X DELETE "https://senhasegura.example.com/iso/pam/credential/custody/123" \
  -H "Authorization: Bearer $TOKEN"
```

---

## SSH Keys API

### Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/api/pam/sshkey` | List all SSH keys |
| `GET` | `/api/pam/sshkey/{id}` | Get SSH key by ID |
| `POST` | `/api/pam/sshkey` | Register new SSH key |
| `PUT` | `/api/pam/sshkey/{id}` | Update SSH key |
| `POST` | `/api/pam/sshkey/{id}/rotate` | Trigger key rotation |

### Register SSH Key

```bash
curl -X POST "https://senhasegura.example.com/api/pam/sshkey" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "identifier": "deploy-key-prod",
    "username": "deploy",
    "hostname": "*.prod.example.com",
    "public_key": "ssh-ed25519 AAAAC3Nza...",
    "private_key": "-----BEGIN OPENSSH PRIVATE KEY-----...",
    "passphrase": "optional-passphrase",
    "auto_rotate": true,
    "rotation_days": 90
  }'
```

### Trigger Key Rotation

```bash
curl -X POST "https://senhasegura.example.com/api/pam/sshkey/456/rotate" \
  -H "Authorization: Bearer $TOKEN"
```

---

## DevOps Secret Manager (DSM)

### DSM CLI Installation

```bash
# Download latest binary
curl -LO https://github.com/senhasegura/dsmcli/releases/latest/download/dsm-linux-amd64
chmod +x dsm-linux-amd64
sudo mv dsm-linux-amd64 /usr/local/bin/dsm

# Verify installation
dsm --version
```

### DSM CLI Configuration

Create `~/.senhasegura/config.yaml`:

```yaml
# Required
SENHASEGURA_URL: "https://senhasegura.example.com"
SENHASEGURA_CLIENT_ID: "your-client-id"
SENHASEGURA_CLIENT_SECRET: "your-client-secret"

# Optional
SENHASEGURA_MAPPING_FILE: "/path/to/mapping.json"
SENHASEGURA_SECRETS_FILE: ".runb.vars"
SENHASEGURA_DISABLE_RUNB: 0
```

### Environment Variables (Alternative)

```bash
export SENHASEGURA_URL="https://senhasegura.example.com"
export SENHASEGURA_CLIENT_ID="your-client-id"
export SENHASEGURA_CLIENT_SECRET="your-client-secret"
export SENHASEGURA_CONFIG_FILE="/path/to/config.yaml"
```

### Running Belt (runb) - Secret Injection

```bash
# Fetch secrets and create environment file
dsm runb \
  --application "my-application" \
  --system "production" \
  --environment "prod" \
  --config ~/.senhasegura/config.yaml

# Source the secrets
source .runb.vars

# Use in your application
echo "Database password: $DB_PASSWORD"

# Clean up after use (IMPORTANT)
rm -f .runb.vars
```

### CI/CD Tool Integration

```bash
# GitHub Actions
dsm runb --tool-name github --application myapp --system prod --environment prod

# Azure DevOps
dsm runb --tool-name azure-devops --application myapp --system prod --environment prod

# GitLab CI
dsm runb --tool-name gitlab --application myapp --system prod --environment prod

# Jenkins
dsm runb --tool-name linux --application myapp --system prod --environment prod
```

### Mapping File for Secret Registration

Create `mapping.json` to register/update secrets from CI/CD:

```json
{
  "access_keys": [
    {
      "name": "AWS_PROD_KEYS",
      "type": "aws",
      "fields": {
        "access_key_id": "AWS_ACCESS_KEY_ID",
        "secret_access_key": "AWS_SECRET_ACCESS_KEY"
      }
    }
  ],
  "credentials": [
    {
      "name": "DATABASE_CREDS",
      "fields": {
        "user": "DB_USER",
        "password": "DB_PASSWORD",
        "host": "DB_HOST"
      }
    }
  ],
  "key_value": [
    {
      "name": "API_TOKENS",
      "fields": ["API_KEY", "API_SECRET", "WEBHOOK_SECRET"]
    }
  ]
}
```

### DSM API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/api/dsm/secret` | List secrets |
| `GET` | `/api/dsm/secret/{identifier}` | Get secret by identifier |
| `POST` | `/api/dsm/secret` | Create secret |
| `PUT` | `/api/dsm/secret/{identifier}` | Update secret |
| `DELETE` | `/api/dsm/secret/{identifier}` | Delete secret |

---

## Kubernetes Integration

### External Secrets Operator Setup

#### Install ESO

```bash
helm repo add external-secrets https://charts.external-secrets.io
helm install external-secrets external-secrets/external-secrets \
  -n external-secrets --create-namespace
```

#### Create Authentication Secret

```yaml
apiVersion: v1
kind: Secret
metadata:
  name: senhasegura-auth
  namespace: external-secrets
type: Opaque
stringData:
  clientId: "your-oauth2-client-id"
  clientSecret: "your-oauth2-client-secret"
```

#### Configure SecretStore

```yaml
apiVersion: external-secrets.io/v1beta1
kind: SecretStore
metadata:
  name: senhasegura-dsm
  namespace: default
spec:
  provider:
    senhasegura:
      url: "https://senhasegura.example.com"
      module: DSM
      auth:
        clientId:
          secretRef:
            name: senhasegura-auth
            key: clientId
            namespace: external-secrets
        clientSecretSecretRef:
          name: senhasegura-auth
          key: clientSecret
          namespace: external-secrets
      # Optional: skip TLS verification (not recommended for production)
      # ignoreSslCertificate: true
```

#### ClusterSecretStore (Multi-Namespace)

```yaml
apiVersion: external-secrets.io/v1beta1
kind: ClusterSecretStore
metadata:
  name: senhasegura-dsm-global
spec:
  provider:
    senhasegura:
      url: "https://senhasegura.example.com"
      module: DSM
      auth:
        clientId:
          secretRef:
            name: senhasegura-auth
            key: clientId
            namespace: external-secrets
        clientSecretSecretRef:
          name: senhasegura-auth
          key: clientSecret
          namespace: external-secrets
```

#### ExternalSecret - Explicit Keys

```yaml
apiVersion: external-secrets.io/v1beta1
kind: ExternalSecret
metadata:
  name: database-credentials
  namespace: default
spec:
  refreshInterval: 1h
  secretStoreRef:
    name: senhasegura-dsm
    kind: SecretStore
  target:
    name: db-secret
    creationPolicy: Owner
  data:
    - secretKey: username
      remoteRef:
        key: database-prod
        property: username
    - secretKey: password
      remoteRef:
        key: database-prod
        property: password
    - secretKey: host
      remoteRef:
        key: database-prod
        property: host
```

#### ExternalSecret - Extract All Fields

```yaml
apiVersion: external-secrets.io/v1beta1
kind: ExternalSecret
metadata:
  name: api-secrets
  namespace: default
spec:
  refreshInterval: 30m
  secretStoreRef:
    name: senhasegura-dsm
    kind: SecretStore
  target:
    name: api-config
    creationPolicy: Owner
  dataFrom:
    - extract:
        key: api-settings-prod
```

---

## MySafe Integration

### MySafe Features

- **Passwords**: Store and share login credentials
- **Notes**: Secure text notes
- **Files**: Encrypted file storage
- **API Secrets**: Store API keys, tokens, client credentials

### Web Access

```
URL: https://senhasegura.example.com/mysafe
Features:
- Central vault administration
- Credential creation and management
- Sharing with internal/external users
- Access history and auditing
```

### Browser Extension

```
Chrome: Segura MySafe Extension
Features:
- Auto-fill passwords
- Create new credentials
- Quick access to notes
```

### Sharing Items

```
Sharing Options:
1. Internal sharing (MySafe users)
   - Select users/groups
   - Set permissions (view/edit)

2. External sharing (temporary)
   - Generate unique link
   - Set expiration time
   - Limit number of views
   - Revoke access anytime
```

---

## Python SDK Integration

### Installation

```bash
pip install senhasegura
```

### Basic Usage

```python
from senhasegura import A2A

# Initialize with OAuth 2.0 (recommended)
client = A2A(
    base_url="https://senhasegura.example.com",
    client_id="your-client-id",
    client_secret="your-client-secret",
    auth_method="oauth2"  # or "oauth1"
)

# Get credential password
response = client.get(
    "/iso/coe/senha",
    params={"credentialId": 123}
)
password = response.json()["response"]["credential"]["password"]

# List all credentials
credentials = client.get("/api/pam/credential")
for cred in credentials.json()["response"]["credentials"]:
    print(f"{cred['identifier']}: {cred['username']}@{cred['hostname']}")

# Create new credential
new_cred = client.post(
    "/api/pam/credential",
    json={
        "identifier": "new-service",
        "username": "svc_user",
        "password": "SecurePass123!",
        "hostname": "server.example.com"
    }
)

# Release credential custody
client.delete(f"/iso/pam/credential/custody/{credential_id}")
```

### OAuth 1.0 (Legacy)

```python
from senhasegura import A2A

client = A2A(
    base_url="https://senhasegura.example.com",
    consumer_key="your-consumer-key",
    consumer_secret="your-consumer-secret",
    token_key="your-token-key",
    token_secret="your-token-secret",
    auth_method="oauth1"
)
```

### Error Handling

```python
from senhasegura import A2A
from senhasegura.exceptions import AuthenticationError, APIError

try:
    client = A2A(
        base_url="https://senhasegura.example.com",
        client_id="client-id",
        client_secret="client-secret"
    )

    response = client.get("/api/pam/credential/999")
    response.raise_for_status()

except AuthenticationError as e:
    print(f"Authentication failed: {e}")
except APIError as e:
    print(f"API error: {e.status_code} - {e.message}")
```

---

## CI/CD Pipeline Examples

### GitHub Actions

```yaml
name: Deploy with Secrets

on:
  push:
    branches: [main]

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Install DSM CLI
        run: |
          curl -LO https://github.com/senhasegura/dsmcli/releases/latest/download/dsm-linux-amd64
          chmod +x dsm-linux-amd64
          sudo mv dsm-linux-amd64 /usr/local/bin/dsm

      - name: Fetch Secrets
        env:
          SENHASEGURA_URL: ${{ secrets.SENHASEGURA_URL }}
          SENHASEGURA_CLIENT_ID: ${{ secrets.SENHASEGURA_CLIENT_ID }}
          SENHASEGURA_CLIENT_SECRET: ${{ secrets.SENHASEGURA_CLIENT_SECRET }}
        run: |
          dsm runb \
            --tool-name github \
            --application my-app \
            --system production \
            --environment prod
          source .runb.vars

      - name: Deploy
        run: |
          # Secrets are now available as environment variables
          ./deploy.sh

      - name: Cleanup
        if: always()
        run: rm -f .runb.vars
```

### Azure DevOps Pipeline

```yaml
trigger:
  - main

pool:
  vmImage: ubuntu-latest

steps:
  - script: |
      curl -LO https://github.com/senhasegura/dsmcli/releases/latest/download/dsm-linux-amd64
      chmod +x dsm-linux-amd64
      sudo mv dsm-linux-amd64 /usr/local/bin/dsm
    displayName: Install DSM CLI

  - script: |
      dsm runb \
        --tool-name azure-devops \
        --application $(APPLICATION_NAME) \
        --system $(SYSTEM_NAME) \
        --environment $(ENVIRONMENT)
    displayName: Fetch Secrets
    env:
      SENHASEGURA_URL: $(SENHASEGURA_URL)
      SENHASEGURA_CLIENT_ID: $(SENHASEGURA_CLIENT_ID)
      SENHASEGURA_CLIENT_SECRET: $(SENHASEGURA_CLIENT_SECRET)

  - script: |
      source .runb.vars
      ./deploy.sh
    displayName: Deploy Application

  - script: rm -f .runb.vars
    displayName: Cleanup
    condition: always()
```

### GitLab CI

```yaml
stages:
  - deploy

deploy:
  stage: deploy
  image: ubuntu:latest
  before_script:
    - apt-get update && apt-get install -y curl
    - curl -LO https://github.com/senhasegura/dsmcli/releases/latest/download/dsm-linux-amd64
    - chmod +x dsm-linux-amd64 && mv dsm-linux-amd64 /usr/local/bin/dsm
  script:
    - |
      dsm runb \
        --tool-name gitlab \
        --application $APPLICATION_NAME \
        --system $SYSTEM_NAME \
        --environment $CI_ENVIRONMENT_NAME
    - source .runb.vars
    - ./deploy.sh
  after_script:
    - rm -f .runb.vars
  variables:
    SENHASEGURA_URL: $SENHASEGURA_URL
    SENHASEGURA_CLIENT_ID: $SENHASEGURA_CLIENT_ID
    SENHASEGURA_CLIENT_SECRET: $SENHASEGURA_CLIENT_SECRET
```

---

## Workflows

### Workflow 1: Initial A2A Setup

```
1. Create Application
   Console: A2A > Applications > New
   - Name: app-integration
   - Authentication: OAuth 2.0
   - Status: Enabled

2. Configure Authorization
   Console: A2A > Authorizations > New
   - Application: app-integration
   - Module: PAM Core (or DSM)
   - Permission: Read/Write
   - IP Restriction: 10.0.0.0/8 (optional)
   - Credential filter: tag:production (optional)

3. Test Authentication
   curl -X POST "$URL/iso/oauth2/token" \
     -d "grant_type=client_credentials" \
     -d "client_id=$CLIENT_ID" \
     -d "client_secret=$CLIENT_SECRET"

4. Verify Access
   curl -X GET "$URL/api/pam/credential" \
     -H "Authorization: Bearer $TOKEN"
```

### Workflow 2: Kubernetes Secret Sync

```
1. Install External Secrets Operator
   helm install external-secrets external-secrets/external-secrets

2. Create Auth Secret
   kubectl create secret generic senhasegura-auth \
     --from-literal=clientId=xxx \
     --from-literal=clientSecret=xxx

3. Create SecretStore
   kubectl apply -f secretstore.yaml

4. Create ExternalSecret
   kubectl apply -f externalsecret.yaml

5. Verify Sync
   kubectl get externalsecret
   kubectl get secret db-secret -o yaml
```

### Workflow 3: Password Rotation Automation

```
1. Configure Execution Template
   Console: Executions > Templates
   - Template: Linux Password Change
   - Commands: passwd, chage
   - Verification: SSH login test

2. Create Execution Policy
   Console: Executions > Policies
   - Credentials: tag:linux-servers
   - Schedule: Every 30 days
   - Template: Linux Password Change
   - Notification: security@example.com

3. Monitor Executions
   Console: Executions > History
   - Filter by date/status
   - Review logs
   - Handle failures
```

---

## Security Best Practices

### Credential Management

```
DO:
- Use one credential per A2A authorization
- Apply IP restrictions to authorized networks only
- Enable automatic password rotation
- Use unique identifiers for credentials
- Audit access logs regularly

DON'T:
- Share A2A credentials across applications
- Disable IP restrictions in production
- Store credentials in source code
- Use weak or default passwords
- Ignore failed authentication alerts
```

### API Security

```python
# Good: Use environment variables
import os
client = A2A(
    base_url=os.environ["SENHASEGURA_URL"],
    client_id=os.environ["SENHASEGURA_CLIENT_ID"],
    client_secret=os.environ["SENHASEGURA_CLIENT_SECRET"]
)

# Good: Release custody after use
try:
    password = client.get_password(credential_id)
    # Use password
finally:
    client.release_custody(credential_id)
```

### Kubernetes Security

```yaml
# Use namespaced SecretStore when possible
apiVersion: external-secrets.io/v1beta1
kind: SecretStore  # Not ClusterSecretStore
metadata:
  name: app-secrets
  namespace: my-app  # Limit scope
spec:
  provider:
    senhasegura:
      # ...
---
# Restrict RBAC
apiVersion: rbac.authorization.k8s.io/v1
kind: Role
metadata:
  name: secret-reader
  namespace: my-app
rules:
  - apiGroups: [""]
    resources: ["secrets"]
    resourceNames: ["db-secret", "api-secret"]  # Specific secrets only
    verbs: ["get"]
```

---

## Troubleshooting

### Authentication Errors

| Error | Cause | Solution |
|-------|-------|----------|
| `401 Unauthorized` | Invalid/expired token | Request new access token |
| `403 Forbidden` | Insufficient permissions | Check A2A authorization |
| `invalid_client` | Wrong client_id/secret | Verify credentials in Console |
| `IP not allowed` | IP restriction | Add source IP to whitelist |

### DSM CLI Issues

```bash
# Debug mode
dsm runb --debug \
  --application myapp \
  --system prod \
  --environment prod

# Common fixes
# 1. Config file not found
export SENHASEGURA_CONFIG_FILE=/absolute/path/to/config.yaml

# 2. SSL certificate errors
# Add to config.yaml:
# SENHASEGURA_INSECURE: true  # Not recommended for production

# 3. Permission denied
chmod 600 ~/.senhasegura/config.yaml
```

### External Secrets Operator

```bash
# Check SecretStore status
kubectl describe secretstore senhasegura-dsm

# Check ExternalSecret status
kubectl describe externalsecret database-credentials

# View ESO logs
kubectl logs -n external-secrets -l app.kubernetes.io/name=external-secrets

# Common issues:
# - "could not get provider client": Check auth secret
# - "could not find secret": Verify secret identifier in DSM
# - "refresh failed": Check network/firewall to senhasegura
```

### API Response Codes

| Code | Meaning | Action |
|------|---------|--------|
| `200` | Success | Process response |
| `400` | Bad request | Check request format |
| `401` | Unauthorized | Re-authenticate |
| `403` | Forbidden | Check permissions |
| `404` | Not found | Verify resource ID |
| `429` | Rate limited | Implement backoff |
| `500` | Server error | Contact support |

---

## Quick Reference

### Environment Variables

```bash
# Core Authentication
SENHASEGURA_URL="https://senhasegura.example.com"
SENHASEGURA_CLIENT_ID="oauth2-client-id"
SENHASEGURA_CLIENT_SECRET="oauth2-client-secret"

# DSM CLI
SENHASEGURA_CONFIG_FILE="/path/to/config.yaml"
SENHASEGURA_MAPPING_FILE="/path/to/mapping.json"
SENHASEGURA_SECRETS_FILE=".runb.vars"

# Optional
SENHASEGURA_INSECURE="false"  # Skip TLS verify
SENHASEGURA_TIMEOUT="30"      # Request timeout
```

### Common API Patterns

```bash
# Get token
TOKEN=$(curl -s -X POST "$URL/iso/oauth2/token" \
  -d "grant_type=client_credentials" \
  -d "client_id=$CLIENT_ID" \
  -d "client_secret=$CLIENT_SECRET" | jq -r '.access_token')

# List credentials
curl -H "Authorization: Bearer $TOKEN" "$URL/api/pam/credential"

# Get password
curl -H "Authorization: Bearer $TOKEN" "$URL/iso/coe/senha?credentialId=123"

# Release custody
curl -X DELETE -H "Authorization: Bearer $TOKEN" \
  "$URL/iso/pam/credential/custody/123"
```

---

## Documentation Links

- [Official Documentation](https://docs.senhasegura.io/docs)
- [A2A Module](https://docs.senhasegura.io/docs/a2a)
- [DSM Documentation](https://docs.senhasegura.io/docs/devops-secret-manager)
- [MySafe](https://docs.senhasegura.io/docs/mysafe)
- [API Reference](https://docs.senhasegura.io/docs/api-a2a-pam-core)
- [DSM CLI GitHub](https://github.com/senhasegura/dsmcli)
- [External Secrets Integration](https://external-secrets.io/latest/provider/senhasegura-dsm/)
- [Community Forum](https://community.senhasegura.io/)
