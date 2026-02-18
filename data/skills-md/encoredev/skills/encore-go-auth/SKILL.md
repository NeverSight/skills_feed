---
name: encore-go-auth
description: Implement authentication with Encore Go.
---

# Encore Go Authentication

## Instructions

Encore Go provides a built-in authentication system using the `//encore:authhandler` annotation.

### 1. Create an Auth Handler

```go
package auth

import (
    "context"
    "encore.dev/beta/auth"
    "encore.dev/beta/errs"
)

// AuthParams defines what the auth handler receives
type AuthParams struct {
    Authorization string `header:"Authorization"`
}

// AuthData defines what authenticated requests have access to
type AuthData struct {
    UserID string
    Email  string
    Role   string
}

//encore:authhandler
func Authenticate(ctx context.Context, params *AuthParams) (auth.UID, *AuthData, error) {
    token := strings.TrimPrefix(params.Authorization, "Bearer ")
    
    payload, err := verifyToken(token)
    if err != nil {
        return "", nil, &errs.Error{
            Code:    errs.Unauthenticated,
            Message: "invalid token",
        }
    }
    
    return auth.UID(payload.UserID), &AuthData{
        UserID: payload.UserID,
        Email:  payload.Email,
        Role:   payload.Role,
    }, nil
}
```

### 2. Protect Endpoints

```go
package user

import "context"

// Protected endpoint - requires authentication
//encore:api auth method=GET path=/profile
func GetProfile(ctx context.Context) (*Profile, error) {
    // Only authenticated users reach here
}

// Public endpoint - no authentication required
//encore:api public method=GET path=/health
func Health(ctx context.Context) (*HealthResponse, error) {
    return &HealthResponse{Status: "ok"}, nil
}
```

### 3. Access Auth Data in Endpoints

```go
package user

import (
    "context"
    "encore.dev/beta/auth"
    myauth "myapp/auth"  // Import your auth package
)

//encore:api auth method=GET path=/profile
func GetProfile(ctx context.Context) (*Profile, error) {
    // Get the user ID
    userID, ok := auth.UserID()
    if !ok {
        // Should not happen with auth endpoint
    }
    
    // Get full auth data
    data := auth.Data().(*myauth.AuthData)
    
    return &Profile{
        UserID: string(userID),
        Email:  data.Email,
        Role:   data.Role,
    }, nil
}
```

## Auth Handler Signature

The auth handler must:
1. Have the `//encore:authhandler` annotation
2. Accept `context.Context` and a params struct pointer
3. Return `(auth.UID, *YourAuthData, error)`

```go
//encore:authhandler
func MyAuthHandler(ctx context.Context, params *Params) (auth.UID, *AuthData, error)
```

## Auth Handler Behavior

| Scenario | Returns | Result |
|----------|---------|--------|
| Valid credentials | `(uid, data, nil)` | Request authenticated |
| Invalid credentials | `("", nil, err)` with `errs.Unauthenticated` | 401 response |
| Other error | `("", nil, err)` | Request aborted |

## Common Auth Patterns

### JWT Token Validation

```go
import (
    "github.com/golang-jwt/jwt/v5"
    "encore.dev/config"
)

var secrets struct {
    JWTSecret config.String
}

func verifyToken(tokenString string) (*Claims, error) {
    token, err := jwt.ParseWithClaims(tokenString, &Claims{}, func(t *jwt.Token) (interface{}, error) {
        return []byte(secrets.JWTSecret()), nil
    })
    if err != nil {
        return nil, err
    }
    
    claims, ok := token.Claims.(*Claims)
    if !ok || !token.Valid {
        return nil, errors.New("invalid token")
    }
    
    return claims, nil
}
```

### API Key Authentication

```go
//encore:authhandler
func Authenticate(ctx context.Context, params *AuthParams) (auth.UID, *AuthData, error) {
    apiKey := params.Authorization
    
    user, err := db.QueryRow[User](ctx, `
        SELECT id, email, role FROM users WHERE api_key = $1
    `, apiKey)
    if err != nil {
        return "", nil, &errs.Error{
            Code:    errs.Unauthenticated,
            Message: "invalid API key",
        }
    }
    
    return auth.UID(user.ID), &AuthData{
        UserID: user.ID,
        Email:  user.Email,
        Role:   user.Role,
    }, nil
}
```

### Cookie-Based Auth

```go
type AuthParams struct {
    Cookie string `header:"Cookie"`
}

//encore:authhandler
func Authenticate(ctx context.Context, params *AuthParams) (auth.UID, *AuthData, error) {
    sessionID := parseCookie(params.Cookie, "session")
    if sessionID == "" {
        return "", nil, &errs.Error{
            Code:    errs.Unauthenticated,
            Message: "no session",
        }
    }
    
    session, err := getSession(ctx, sessionID)
    if err != nil || session.ExpiresAt.Before(time.Now()) {
        return "", nil, &errs.Error{
            Code:    errs.Unauthenticated,
            Message: "session expired",
        }
    }
    
    return auth.UID(session.UserID), &AuthData{
        UserID: session.UserID,
        Email:  session.Email,
        Role:   session.Role,
    }, nil
}
```

## Service-to-Service Auth

Auth data automatically propagates in internal service calls:

```go
package order

import (
    "context"
    "myapp/user"  // Import the user service
)

//encore:api auth method=GET path=/orders/:id
func GetOrderWithUser(ctx context.Context, params *GetOrderParams) (*OrderWithUser, error) {
    order, err := getOrder(ctx, params.ID)
    if err != nil {
        return nil, err
    }
    
    // Auth is automatically propagated to this call
    profile, err := user.GetProfile(ctx)
    if err != nil {
        return nil, err
    }
    
    return &OrderWithUser{Order: order, User: profile}, nil
}
```

## Guidelines

- Only one `//encore:authhandler` per application
- Return `auth.UID` as the first return value (user identifier)
- Return your custom `AuthData` struct as second value
- Use `auth.UserID()` to get the authenticated user ID
- Use `auth.Data()` and type assert to get full auth data
- Auth propagates automatically in service-to-service calls
- Keep auth handlers fast - they run on every authenticated request
