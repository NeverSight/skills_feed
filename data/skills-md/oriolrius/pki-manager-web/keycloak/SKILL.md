---
name: Keycloak
description: Expert guidance for Keycloak identity and access management including realm configuration, client setup, user federation, authentication flows, role-based access control, and integration with applications. Use this when setting up authentication, configuring SSO, managing users and roles, or integrating Keycloak with applications.
---

# Keycloak

Expert assistance with Keycloak identity and access management platform.

## Overview

Keycloak is an open-source Identity and Access Management (IAM) solution providing:
- Single Sign-On (SSO)
- Identity brokering and social login
- User federation (LDAP/Active Directory)
- Standard protocols (OAuth 2.0, OpenID Connect, SAML 2.0)
- Fine-grained authorization
- Admin console and account management

## Installation & Setup

### Docker (Quick Start)
```bash
# Run Keycloak
docker run -d \
  --name keycloak \
  -p 8080:8080 \
  -e KEYCLOAK_ADMIN=admin \
  -e KEYCLOAK_ADMIN_PASSWORD=admin \
  quay.io/keycloak/keycloak:latest start-dev

# With PostgreSQL
docker run -d \
  --name keycloak \
  -p 8080:8080 \
  -e KC_DB=postgres \
  -e KC_DB_URL=jdbc:postgresql://localhost/keycloak \
  -e KC_DB_USERNAME=keycloak \
  -e KC_DB_PASSWORD=password \
  -e KEYCLOAK_ADMIN=admin \
  -e KEYCLOAK_ADMIN_PASSWORD=admin \
  quay.io/keycloak/keycloak:latest start
```

### Docker Compose
```yaml
version: '3'

services:
  postgres:
    image: postgres:15
    environment:
      POSTGRES_DB: keycloak
      POSTGRES_USER: keycloak
      POSTGRES_PASSWORD: password
    volumes:
      - postgres_data:/var/lib/postgresql/data

  keycloak:
    image: quay.io/keycloak/keycloak:latest
    command: start
    environment:
      KC_DB: postgres
      KC_DB_URL: jdbc:postgresql://postgres/keycloak
      KC_DB_USERNAME: keycloak
      KC_DB_PASSWORD: password
      KEYCLOAK_ADMIN: admin
      KEYCLOAK_ADMIN_PASSWORD: admin
      KC_HOSTNAME: localhost
      KC_HOSTNAME_PORT: 8080
      KC_HOSTNAME_STRICT_HTTPS: false
      KC_HTTP_ENABLED: true
    ports:
      - "8080:8080"
    depends_on:
      - postgres

volumes:
  postgres_data:
```

### Production Setup
```bash
# Build with PostgreSQL support
docker run \
  -e KC_DB=postgres \
  -e KC_FEATURES=token-exchange,admin-fine-grained-authz \
  -e KC_HTTP_ENABLED=true \
  -e KC_HOSTNAME_STRICT_HTTPS=false \
  quay.io/keycloak/keycloak:latest build

# Run in production mode
docker run \
  -p 8443:8443 \
  -e KC_DB=postgres \
  -e KC_DB_URL=jdbc:postgresql://postgres/keycloak \
  -e KC_DB_USERNAME=keycloak \
  -e KC_DB_PASSWORD=password \
  -e KEYCLOAK_ADMIN=admin \
  -e KEYCLOAK_ADMIN_PASSWORD=admin \
  -e KC_HOSTNAME=auth.example.com \
  -e KC_HTTPS_CERTIFICATE_FILE=/opt/keycloak/conf/server.crt \
  -e KC_HTTPS_CERTIFICATE_KEY_FILE=/opt/keycloak/conf/server.key \
  quay.io/keycloak/keycloak:latest start
```

## Realm Configuration

### Create Realm
1. Login to admin console: http://localhost:8080/admin
2. Click "Create Realm" (top-left dropdown)
3. Enter realm name (e.g., "myapp")
4. Click "Create"

### Realm Settings
```
Realm Settings:
- General
  - Display name: My Application
  - HTML Display name: <b>My App</b>
  - Frontend URL: https://auth.example.com (optional)

- Login
  - User registration: Enable to allow self-registration
  - Edit username: Allow users to edit username
  - Forgot password: Enable password reset
  - Remember me: Allow remember me checkbox
  - Login with email: Allow email as username

- Keys
  - Active keys for signing tokens
  - Configure providers (RSA, ECDSA, HMAC)

- Email
  - From: noreply@example.com
  - Host: smtp.example.com
  - Port: 587
  - Enable authentication
  - Username/Password for SMTP

- Themes
  - Login theme: keycloak (or custom)
  - Account theme: keycloak
  - Admin console theme: keycloak
  - Email theme: keycloak

- Tokens
  - Access Token Lifespan: 5 minutes
  - Refresh Token Max Reuse: 0
  - SSO Session Idle: 30 minutes
  - SSO Session Max: 10 hours
```

## Client Configuration

### Create Client

**OpenID Connect Client**:
```
Client ID: my-app
Client Protocol: openid-connect
Root URL: http://localhost:3000

Settings:
- Client authentication: ON (for confidential clients)
- Authorization: OFF (unless using fine-grained authz)
- Valid redirect URIs:
  - http://localhost:3000/*
  - http://localhost:3000/api/auth/callback/keycloak
- Valid post logout redirect URIs:
  - http://localhost:3000
- Web origins: http://localhost:3000

Capability config:
- Client authentication: ON
- Authorization: OFF
- Standard flow: ON (Authorization Code Flow)
- Direct access grants: ON (Resource Owner Password Credentials)
- Implicit flow: OFF (deprecated)
- Service accounts roles: ON (for client credentials)
```

### Client Credentials
After creating client with authentication ON:
1. Go to "Credentials" tab
2. Copy "Client secret"
3. Use in application configuration

### Client Scopes
```
Create custom scope:
1. Clients > Client scopes > Create
2. Name: custom-scope
3. Protocol: openid-connect
4. Display on consent: OFF
5. Include in token scope: ON

Add mappers:
1. Mappers tab > Create
2. Mapper type: User Property
3. Property: email
4. Token Claim Name: email
5. Claim JSON Type: String

Assign to client:
1. Clients > [your-client] > Client scopes
2. Add available scope to Assigned default scopes
```

## User Management

### Create User
```
Admin Console > Users > Create user

Username: john.doe
Email: john@example.com
Email verified: ON
First name: John
Last name: Doe
Enabled: ON

Credentials:
- Set password
- Temporary: OFF (user won't be forced to change)
```

### User Attributes
```
Users > [user] > Attributes

Key: department
Value: engineering

Key: employee_id
Value: EMP-12345
```

### User Roles
```
1. Create roles:
   Realm roles > Create role
   - Name: admin
   - Name: user
   - Name: viewer

2. Assign to user:
   Users > [user] > Role mapping
   - Assign role: admin
```

### User Groups
```
1. Create group:
   Groups > Create group
   - Name: Developers

2. Add attributes to group:
   Groups > Developers > Attributes
   - team: backend

3. Assign roles to group:
   Groups > Developers > Role mapping
   - Assign: developer role

4. Add users to group:
   Users > [user] > Groups
   - Join: Developers
```

## Roles & Permissions

### Realm Roles
```
Realm roles > Create role

Name: super-admin
Description: Full system access

Composite roles:
- Add child roles (admin, user, viewer)
```

### Client Roles
```
Clients > [client] > Roles > Create role

Name: app-admin
Description: Application administrator

Use case: Application-specific roles
```

### Role Mappers
```
Client scopes > roles > Mappers > realm roles

Add to token:
- Token Claim Name: realm_access.roles
- Claim JSON Type: String
- Add to ID token: ON
- Add to access token: ON
- Add to userinfo: ON
```

## Authentication Flows

### Browser Flow (Default)
```
Authentication > Flows > Browser

Steps:
1. Cookie (SSO check)
2. Kerberos (optional)
3. Forms (username/password)
   - Username password form
   - OTP form (if enabled)
```

### Custom Authentication Flow
```
1. Duplicate existing flow:
   Flows > Browser > Duplicate

2. Customize:
   - Add execution
   - Set requirement (REQUIRED, ALTERNATIVE, DISABLED)

3. Bind to client:
   Clients > [client] > Advanced > Authentication flow overrides
   - Browser flow: [custom-flow]
```

### Two-Factor Authentication
```
1. Enable OTP:
   Authentication > Flows > Browser
   - Add execution: OTP Form
   - Requirement: CONDITIONAL

2. Configure OTP:
   Authentication > OTP Policy
   - Type: Time-based or Counter-based
   - Algorithm: SHA1, SHA256, SHA512
   - Digits: 6
   - Period: 30 seconds

3. Users enable OTP:
   Account console > Account security > Signing in
   - Set up Authenticator Application
```

## User Federation

### LDAP Integration
```
User Federation > Add provider > LDAP

Connection:
- Console display name: LDAP
- Edit mode: READ_ONLY or WRITEABLE
- Sync registrations: ON
- Vendor: Active Directory, Red Hat Directory Server, etc.
- Connection URL: ldap://ldap.example.com:389
- Users DN: ou=users,dc=example,dc=com
- Bind DN: cn=admin,dc=example,dc=com
- Bind credential: password

LDAP searching and updating:
- Custom user search filter: (objectClass=person)
- Search scope: Subtree

Synchronization:
- Batch size: 1000
- Full sync period: 604800 (weekly)
- Changed users sync period: 86400 (daily)

Test connection and authentication
```

### Custom User Storage SPI
```java
public class CustomUserStorageProvider implements UserStorageProvider {
    @Override
    public UserModel getUserById(String id, RealmModel realm) {
        // Fetch user from custom storage
    }

    @Override
    public UserModel getUserByUsername(String username, RealmModel realm) {
        // Lookup by username
    }

    @Override
    public UserModel getUserByEmail(String email, RealmModel realm) {
        // Lookup by email
    }
}
```

## Identity Providers

### Social Login (Google)
```
Identity Providers > Add provider > Google

Settings:
- Client ID: [from Google Console]
- Client secret: [from Google Console]
- Default scopes: openid profile email
- Store tokens: ON
- Stored tokens readable: ON

Mappers:
- Create mapper: Import from provider
- Sync mode: Import or Force
```

### SAML Provider
```
Identity Providers > Add provider > SAML

Settings:
- Service provider entity ID: my-app
- Single sign-on service URL: [from SAML provider]
- Name ID policy format: Email
- Principal type: Subject NameID
- Want AuthnRequests signed: ON

Import from URL or file for metadata
```

## Token Configuration

### Access Token
```
Clients > [client] > Settings > Advanced

Access Token Lifespan: 5 minutes
Client Session Idle: 30 minutes
Client Session Max: 10 hours

Include in token:
- Standard claims (sub, aud, iss, exp, iat)
- Custom claims via mappers
```

### Refresh Token
```
Realm Settings > Tokens

Refresh Token Max Reuse: 0
Revoke Refresh Token: ON
SSO Session Idle: 30 minutes
SSO Session Max: 10 hours
Offline Session Idle: 30 days
```

### Custom Claims
```
Client scopes > [scope] > Mappers > Create

Mapper type: User Attribute
User attribute: department
Token claim name: department
Claim JSON Type: String
Add to ID token: ON
Add to access token: ON
Add to userinfo: ON
```

## Admin API

### Get Admin Token
```bash
# Password grant
curl -X POST http://localhost:8080/realms/master/protocol/openid-connect/token \
  -d "client_id=admin-cli" \
  -d "username=admin" \
  -d "password=admin" \
  -d "grant_type=password"
```

### API Examples
```bash
# Get realm
curl -X GET http://localhost:8080/admin/realms/myapp \
  -H "Authorization: Bearer $TOKEN"

# Create user
curl -X POST http://localhost:8080/admin/realms/myapp/users \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "username": "john",
    "email": "john@example.com",
    "enabled": true,
    "firstName": "John",
    "lastName": "Doe"
  }'

# Get users
curl -X GET http://localhost:8080/admin/realms/myapp/users \
  -H "Authorization: Bearer $TOKEN"

# Assign role
curl -X POST http://localhost:8080/admin/realms/myapp/users/{userId}/role-mappings/realm \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '[{"id": "{roleId}", "name": "admin"}]'
```

## Application Integration

### Next.js with NextAuth
```typescript
// pages/api/auth/[...nextauth].ts
import NextAuth from "next-auth"
import KeycloakProvider from "next-auth/providers/keycloak"

export default NextAuth({
  providers: [
    KeycloakProvider({
      clientId: process.env.KEYCLOAK_CLIENT_ID!,
      clientSecret: process.env.KEYCLOAK_CLIENT_SECRET!,
      issuer: process.env.KEYCLOAK_ISSUER, // http://localhost:8080/realms/myapp
    }),
  ],
  callbacks: {
    async jwt({ token, account }) {
      if (account) {
        token.accessToken = account.access_token
        token.refreshToken = account.refresh_token
      }
      return token
    },
    async session({ session, token }) {
      session.accessToken = token.accessToken
      return session
    },
  },
})

// .env.local
KEYCLOAK_CLIENT_ID=my-app
KEYCLOAK_CLIENT_SECRET=secret
KEYCLOAK_ISSUER=http://localhost:8080/realms/myapp
```

### Node.js with keycloak-connect
```javascript
const session = require('express-session')
const Keycloak = require('keycloak-connect')

const memoryStore = new session.MemoryStore()
const keycloak = new Keycloak({ store: memoryStore }, {
  'realm': 'myapp',
  'auth-server-url': 'http://localhost:8080',
  'ssl-required': 'external',
  'resource': 'my-app',
  'credentials': {
    'secret': 'client-secret'
  }
})

app.use(session({
  secret: 'session-secret',
  resave: false,
  saveUninitialized: true,
  store: memoryStore
}))

app.use(keycloak.middleware())

// Protected route
app.get('/protected', keycloak.protect(), (req, res) => {
  res.json({ message: 'Protected resource' })
})

// Role-based protection
app.get('/admin', keycloak.protect('admin'), (req, res) => {
  res.json({ message: 'Admin resource' })
})
```

### React SPA
```typescript
import Keycloak from 'keycloak-js'

const keycloak = new Keycloak({
  url: 'http://localhost:8080',
  realm: 'myapp',
  clientId: 'my-app',
})

// Initialize
keycloak.init({
  onLoad: 'login-required',
  checkLoginIframe: false,
}).then((authenticated) => {
  if (authenticated) {
    console.log('User is authenticated')
    console.log('Token:', keycloak.token)
    console.log('Roles:', keycloak.realmAccess?.roles)
  }
})

// Auto-refresh token
keycloak.onTokenExpired = () => {
  keycloak.updateToken(30)
}

// API call with token
fetch('/api/data', {
  headers: {
    'Authorization': `Bearer ${keycloak.token}`
  }
})

// Logout
keycloak.logout({ redirectUri: 'http://localhost:3000' })

// Check role
if (keycloak.hasRealmRole('admin')) {
  // Show admin features
}
```

## Security Best Practices

1. **Use HTTPS in production** - Always enable SSL/TLS
2. **Strong client secrets** - Use cryptographically random secrets
3. **Limit token lifetime** - Short-lived access tokens (5-15 min)
4. **Refresh token rotation** - Enable refresh token reuse detection
5. **PKCE for SPAs** - Use Proof Key for Code Exchange
6. **Content Security Policy** - Proper CSP headers
7. **Rate limiting** - Protect against brute force
8. **Regular updates** - Keep Keycloak up to date
9. **Audit logging** - Enable and monitor event logs
10. **Role hierarchy** - Use composite roles for complexity

## Troubleshooting

### Token Validation Issues
```bash
# Decode JWT token
echo $TOKEN | cut -d. -f2 | base64 -d | jq

# Verify token signature
curl http://localhost:8080/realms/myapp/protocol/openid-connect/certs
```

### Connection Issues
```bash
# Check Keycloak health
curl http://localhost:8080/health

# Check realm endpoints
curl http://localhost:8080/realms/myapp/.well-known/openid-configuration
```

### User Login Issues
1. Check user is enabled
2. Verify email is verified (if required)
3. Check required actions (password reset, email verify)
4. Review authentication logs (Events > Login Events)

### CORS Issues
```
Clients > [client] > Settings
- Web origins: http://localhost:3000
- Valid redirect URIs: http://localhost:3000/*
```

## Common Tasks

### Export/Import Realm
```bash
# Export realm
docker exec keycloak /opt/keycloak/bin/kc.sh export \
  --dir /tmp/export \
  --realm myapp

# Import realm
docker exec keycloak /opt/keycloak/bin/kc.sh import \
  --file /tmp/export/myapp-realm.json
```

### Backup Database
```bash
# PostgreSQL backup
docker exec postgres pg_dump -U keycloak keycloak > keycloak-backup.sql

# Restore
docker exec -i postgres psql -U keycloak keycloak < keycloak-backup.sql
```

### Theme Customization
```
themes/
└── custom-theme/
    ├── login/
    │   ├── theme.properties
    │   ├── login.ftl
    │   └── resources/
    │       ├── css/
    │       └── img/
    └── account/
        └── ...

Realm Settings > Themes > Login theme: custom-theme
```

## Resources

- Docs: https://www.keycloak.org/documentation
- Admin REST API: https://www.keycloak.org/docs-api/latest/rest-api/
- Server Admin Guide: https://www.keycloak.org/docs/latest/server_admin/
- GitHub: https://github.com/keycloak/keycloak
