---
name: azure-ad-sso
description: Azure AD OAuth2/OIDC SSO integration for Kubernetes applications. Use when implementing Single Sign-On, configuring Azure AD App Registrations, restricting access by groups, or integrating tools (DefectDojo, Grafana, ArgoCD, Harbor, SonarQube) with Azure AD authentication.
---

# Azure AD SSO Integration Skill

## Overview

This skill provides comprehensive guidance for implementing Azure AD (Entra ID) OAuth2/OIDC Single Sign-On for applications deployed on Kubernetes clusters, including access restriction by Azure AD groups.

## Quick Reference

### Supported Applications

| Application | Provider | Redirect URI Pattern | Group Sync |
|-------------|----------|---------------------|------------|
| DefectDojo | `azuread-tenant-oauth2` | `/complete/azuread-tenant-oauth2/` | Yes |
| Grafana | `azuread` | `/login/azuread` | Yes |
| ArgoCD | `microsoft` (Dex) | `/api/dex/callback` | Yes |
| Harbor | `oidc` | `/c/oidc/callback` | Yes |
| SonarQube | `saml` or `oidc` | `/oauth2/callback/saml` | Yes |
| OAuth2 Proxy | `azure` | `/oauth2/callback` | Yes |
| Keycloak | `oidc` | `/realms/{realm}/broker/azure/endpoint` | Yes |

### Authentication Flow Decision

```
┌─────────────────────────────────────────────────────────────────┐
│                    Access Control Decision                       │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  Q: Who should access this application?                         │
│                                                                  │
│  ├─ Everyone in tenant ──► appRoleAssignmentRequired=false      │
│  │                                                               │
│  └─ Specific groups ────► appRoleAssignmentRequired=true        │
│                           + Assign groups to Enterprise App     │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

## Implementation Workflow

### Phase 1: Azure AD App Registration

```bash
# 1. Create App Registration
APP_NAME="<application>-<environment>"
REDIRECT_URI="https://<app-domain>/complete/<provider>/"

APP_ID=$(az ad app create \
  --display-name "$APP_NAME" \
  --sign-in-audience "AzureADMyOrg" \
  --web-redirect-uris "$REDIRECT_URI" \
  --query appId -o tsv)

echo "Application (client) ID: $APP_ID"

# 2. Get Tenant ID
TENANT_ID=$(az account show --query tenantId -o tsv)
echo "Directory (tenant) ID: $TENANT_ID"

# 3. Create Client Secret
SECRET=$(az ad app credential reset \
  --id $APP_ID \
  --append \
  --years 1 \
  --query password -o tsv)

echo "Client Secret: $SECRET"  # Save immediately!
```

### Phase 2: Enable Group Claims

```bash
# Enable security group claims in tokens
az ad app update --id $APP_ID --set groupMembershipClaims=SecurityGroup

# Add Group.Read.All permission (delegated)
az ad app permission add \
  --id $APP_ID \
  --api 00000003-0000-0000-c000-000000000000 \
  --api-permissions 5f8c59db-677d-491f-a6b8-5f174b11ec1d=Scope

# Grant admin consent
az ad app permission admin-consent --id $APP_ID
```

### Phase 3: Restrict Access by Group (CRITICAL)

```bash
# Get Service Principal object ID
SP_ID=$(az ad sp list --filter "appId eq '$APP_ID'" --query "[0].id" -o tsv)

# Enable user assignment requirement
az ad sp update --id $SP_ID --set appRoleAssignmentRequired=true

# Get the group ID to restrict access
GROUP_ID=$(az ad group show --group "G-Usuarios-<App>-Admin" --query id -o tsv)

# Assign group to the application (only these users can login)
az rest --method POST \
  --uri "https://graph.microsoft.com/v1.0/servicePrincipals/$SP_ID/appRoleAssignments" \
  --headers "Content-Type=application/json" \
  --body "{
    \"principalId\": \"$GROUP_ID\",
    \"principalType\": \"Group\",
    \"appRoleId\": \"00000000-0000-0000-0000-000000000000\",
    \"resourceId\": \"$SP_ID\"
  }"
```

### Phase 4: Store Secret in Key Vault

```bash
az keyvault secret set \
  --vault-name "<keyvault-name>" \
  --name "<app>-azuread-client-secret" \
  --value "$SECRET"
```

## Secret Management

### SecretProviderClass Template

```yaml
apiVersion: secrets-store.csi.x-k8s.io/v1
kind: SecretProviderClass
metadata:
  name: <app>-secrets
  namespace: <namespace>
spec:
  provider: azure
  parameters:
    usePodIdentity: "false"
    useVMManagedIdentity: "true"
    userAssignedIdentityID: "<managed-identity-client-id>"
    keyvaultName: "<keyvault-name>"
    tenantId: "<azure-tenant-id>"
    objects: |
      array:
        - |
          objectName: <app>-azuread-client-secret
          objectType: secret
          objectAlias: AZURE_AD_CLIENT_SECRET
  secretObjects:
    - secretName: <app>-azure-ad
      type: Opaque
      data:
        - objectName: AZURE_AD_CLIENT_SECRET
          key: client-secret
```

### Pod Volume Mount

```yaml
volumes:
  - name: secrets-store
    csi:
      driver: secrets-store.csi.k8s.io
      readOnly: true
      volumeAttributes:
        secretProviderClass: "<app>-secrets"

volumeMounts:
  - name: secrets-store
    mountPath: "/mnt/secrets-store"
    readOnly: true
```

## Application Configurations

### DefectDojo

```yaml
# Enable SSO
extraEnv:
  - name: DD_SOCIAL_AUTH_AZUREAD_TENANT_OAUTH2_ENABLED
    value: "True"
  - name: DD_SOCIAL_AUTH_AZUREAD_TENANT_OAUTH2_KEY
    value: "<client-id>"
  - name: DD_SOCIAL_AUTH_AZUREAD_TENANT_OAUTH2_TENANT_ID
    value: "<tenant-id>"
  - name: DD_SOCIAL_AUTH_AZUREAD_TENANT_OAUTH2_SECRET
    valueFrom:
      secretKeyRef:
        name: defectdojo
        key: DD_SOCIAL_AUTH_AZUREAD_TENANT_OAUTH2_SECRET
  # Group sync
  - name: DD_SOCIAL_AUTH_AZUREAD_TENANT_OAUTH2_GET_GROUPS
    value: "True"
  - name: DD_SOCIAL_AUTH_AZUREAD_TENANT_OAUTH2_CLEANUP_GROUPS
    value: "True"
  - name: DD_SOCIAL_AUTH_AZUREAD_TENANT_OAUTH2_GROUPS_FILTER
    value: "^G-Usuarios-DefectDojo-.*"
  # CRITICAL: For apps behind reverse proxy
  - name: DD_SECURE_PROXY_SSL_HEADER
    value: "True"
```

### Grafana

```yaml
grafana.ini:
  auth.azuread:
    enabled: true
    name: Azure AD
    allow_sign_up: true
    client_id: "<client-id>"
    client_secret: "${GF_AUTH_AZUREAD_CLIENT_SECRET}"
    scopes: openid email profile
    auth_url: https://login.microsoftonline.com/<tenant-id>/oauth2/v2.0/authorize
    token_url: https://login.microsoftonline.com/<tenant-id>/oauth2/v2.0/token
    allowed_groups: "<admin-group-id> <viewer-group-id>"
    role_attribute_path: contains(groups[*], '<admin-group-id>') && 'Admin' || 'Viewer'
```

### ArgoCD (via Dex)

```yaml
configs:
  cm:
    dex.config: |
      connectors:
        - type: microsoft
          id: microsoft
          name: Azure AD
          config:
            clientID: "<client-id>"
            clientSecret: $dex.azure.clientSecret
            tenant: "<tenant-id>"
            redirectURI: https://<argocd-domain>/api/dex/callback
            groups:
              - <admin-group-id>
  rbac:
    policy.csv: |
      g, <admin-group-id>, role:admin
```

### Harbor

```yaml
externalURL: https://harbor.<domain>
core:
  oidc:
    name: "azure"
    endpoint: "https://login.microsoftonline.com/<tenant-id>/v2.0"
    clientId: "<client-id>"
    clientSecret: "<from-secret>"
    scope: "openid,profile,email"
    groupsClaim: "groups"
    adminGroup: "<admin-group-id>"
    autoOnboard: true
```

## Troubleshooting

### Error Reference

| Error Code | Description | Solution |
|------------|-------------|----------|
| AADSTS50011 | Reply URL mismatch | Verify exact redirect URI including trailing slash |
| AADSTS50105 | User not assigned | Add user/group to Enterprise App assignments |
| AADSTS700016 | App not found | Check client ID and tenant ID |
| AADSTS7000218 | Secret expired | Rotate secret in Key Vault, restart pods |
| AADSTS90102 | Invalid redirect_uri | Check `DD_SECURE_PROXY_SSL_HEADER=True` for reverse proxy |
| AADSTS65001 | Consent not granted | Run `az ad app permission admin-consent` |

### Common Issues

#### Malformed redirect_uri (Django apps behind proxy)

**Symptom:** `redirect_uri=https,%20https://...`

**Root cause:** `DD_SECURE_PROXY_SSL_HEADER` set incorrectly

**Fix:**

```yaml
- name: DD_SECURE_PROXY_SSL_HEADER
  value: "True"  # NOT "HTTP_X_FORWARDED_PROTO,https"
```

#### Groups not syncing

```bash
# Verify group claims enabled
az ad app show --id <app-id> --query groupMembershipClaims

# Check API permissions
az ad app permission list --id <app-id>

# Verify group exists and user is member
az ad group member check --group "<group-name>" --member-id "<user-object-id>"
```

#### Secret not syncing from Key Vault

```bash
# Check SecretProviderClass
kubectl describe secretproviderclass <name> -n <namespace>

# Check CSI driver pods
kubectl get pods -n kube-system | grep secrets-store

# Check managed identity access
az keyvault show --name <vault> --query properties.accessPolicies
```

### Diagnostic Commands

```bash
# Test OAuth redirect
curl -sS -k -D - -o /dev/null "https://<app>/login/<provider>/" 2>&1 | grep -i location

# Check environment variables in pod
kubectl exec -n <ns> deploy/<app> -c <container> -- env | grep -i azure

# Decode JWT token (after login, from browser dev tools)
# Use https://jwt.io to decode and verify claims
```

## Security Best Practices

1. **Never hardcode secrets** - Always use Key Vault + CSI Driver
2. **Use managed identities** - Avoid service principal credentials
3. **Restrict access by group** - Enable `appRoleAssignmentRequired=true`
4. **Rotate secrets** - Set calendar reminders before expiration
5. **Use HTTPS only** - All redirect URIs must use HTTPS
6. **Single tenant** - Never use multi-tenant for internal apps
7. **Audit logging** - Enable Azure AD sign-in logs

## Environment Reference

| Environment | Key Vault | Managed Identity | Tenant ID |
|-------------|-----------|------------------|-----------|
| cafehyna-dev | `kv-cafehyna-dev-hlg` | `f1a14a8f-6d38-40a0-a935-3cdd91a25f47` | `3f7a3df4-f85b-4ca8-98d0-08b1034e6567` |
| cafehyna-hub | `kv-cafehyna-default` | `f1a14a8f-6d38-40a0-a935-3cdd91a25f47` | `3f7a3df4-f85b-4ca8-98d0-08b1034e6567` |
| cafehyna-prd | `kv-cafehyna-prd` | `f1a14a8f-6d38-40a0-a935-3cdd91a25f47` | `3f7a3df4-f85b-4ca8-98d0-08b1034e6567` |

## Detailed Reference

For complete implementation examples:

- **[references/azure-ad-sso-guide.md](references/azure-ad-sso-guide.md)** - Full guide with manifests
- **[references/app-configs.md](references/app-configs.md)** - Application-specific configurations
- **[references/troubleshooting.md](references/troubleshooting.md)** - Extended troubleshooting guide
